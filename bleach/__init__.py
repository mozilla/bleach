import logging
import re

import html5lib
from html5lib.serializer.htmlserializer import HTMLSerializer

from encoding import force_unicode
from sanitizer import BleachSanitizer


VERSION = (1, 0, 3)
__version__ = '.'.join(map(str, VERSION))

__all__ = ['clean', 'linkify']

log = logging.getLogger('bleach')

ALLOWED_TAGS = [
    'a',
    'abbr',
    'acronym',
    'b',
    'blockquote',
    'code',
    'em',
    'i',
    'li',
    'ol',
    'strong',
    'ul',
]

ALLOWED_ATTRIBUTES = {
    'a': ['href', 'title'],
    'abbr': ['title'],
    'acronym': ['title'],
}

ALLOWED_STYLES = []

TLDS = """ac ad ae aero af ag ai al am an ao aq ar arpa as asia at au aw ax az
       ba bb bd be bf bg bh bi biz bj bm bn bo br bs bt bv bw by bz ca cat
       cc cd cf cg ch ci ck cl cm cn co com coop cr cu cv cx cy cz de dj dk
       dm do dz ec edu ee eg er es et eu fi fj fk fm fo fr ga gb gd ge gf gg
       gh gi gl gm gn gov gp gq gr gs gt gu gw gy hk hm hn hr ht hu id ie il
       im in info int io iq ir is it je jm jo jobs jp ke kg kh ki km kn kp
       kr kw ky kz la lb lc li lk lr ls lt lu lv ly ma mc md me mg mh mil mk
       ml mm mn mo mobi mp mq mr ms mt mu museum mv mw mx my mz na name nc ne
       net nf ng ni nl no np nr nu nz om org pa pe pf pg ph pk pl pm pn pr pro
       ps pt pw py qa re ro rs ru rw sa sb sc sd se sg sh si sj sk sl sm sn so
       sr st su sv sy sz tc td tel tf tg th tj tk tl tm tn to tp tr travel tt
       tv tw tz ua ug uk us uy uz va vc ve vg vi vn vu wf ws xn ye yt yu za zm
       zw""".split()

TLDS.reverse()

url_re = re.compile(r"""\b(?<![@.])(?:\w[\w-]*:/{0,3}(?:(?:\w+:)?\w+@)?)?
                                                                      # http://
                    ([\w-]+\.)+(?:%s)(?!\.\w)\b   # xx.yy.tld
                    (?:[/?][^\s\{\}\|\\\^\[\]`<>"\x80-\xFF\x00-\x1F\x7F]*)?
                        # /path/zz (excluding "unsafe" chars from RFC 1738,
                        # except for # and ~, which happen in practice)
                    """ % u'|'.join(TLDS),
                    re.VERBOSE)

proto_re = re.compile(r'^[\w-]+:/{0,3}')

email_re = re.compile(
    r"(?<!//)"
    r"(([-!#$%&'*+/=?^_`{}|~0-9A-Z]+(\.[-!#$%&'*+/=?^_`{}|~0-9A-Z]+)*"  # dot-atom
    r'|^"([\001-\010\013\014\016-\037!#-\[\]-\177]|\\[\001-011\013\014\016-\177])*"' # quoted-string
    r')@(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6})\.?', flags=re.I|re.M)  # domain

NODE_TEXT = 4  # The numeric ID of a text node in simpletree.

identity = lambda x: x  # The identity function.


def clean(text, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES,
          styles=ALLOWED_STYLES, strip=False, strip_comments=True):
    """Clean an HTML fragment and return it"""
    if not text:
        return u''
    elif text.startswith('<!--'):
        text = u' ' + text

    class s(BleachSanitizer):
        allowed_elements = tags
        allowed_attributes = attributes
        allowed_css_properties = styles
        strip_disallowed_elements = strip
        strip_html_comments = strip_comments

    parser = html5lib.HTMLParser(tokenizer=s)

    return _render(parser.parseFragment(text), text).strip()


def linkify(text, nofollow=True, filter_url=identity,
            filter_text=identity, skip_pre=False, parse_email=False):
    """Convert URL-like strings in an HTML fragment to links.

    linkify() converts strings that look like URLs or domain names in a
    blob of text that may be an HTML fragment to links, while preserving
    (a) links already in the string, (b) urls found in attributes, and
    (c) email addresses.

    If the nofollow argument is True (the default) then rel="nofollow"
    will be added to links created by linkify() as well as links already
    found in the text.

    linkify() uses up to two filters on each link. For links created by
    linkify(), the href attribute is passed through filter_url()
    and the text of the link is passed through filter_text(). For links
    already found in the document, the href attribute is passed through
    filter_url(), but the text is untouched.
    """

    if not text:
        return u''

    parser = html5lib.HTMLParser()

    forest = parser.parseFragment(text)

    if nofollow:
        rel = u' rel="nofollow"'
    else:
        rel = u''

    def replace_nodes(tree, new_frag, node):
        new_tree = parser.parseFragment(new_frag)
        for n in new_tree.childNodes:
            tree.insertBefore(n, node)
        tree.removeChild(node)

    def linkify_nodes(tree, parse_text=True):
        for node in tree.childNodes:
            if node.type == NODE_TEXT and parse_text:
                new_frag = node.toxml()
                if parse_email:
                    new_frag = re.sub(email_re, email_repl, new_frag)
                    if new_frag != node.toxml():
                        replace_nodes(tree, new_frag, node)
                        linkify_nodes(tree, False)
                        continue
                new_frag = re.sub(url_re, link_repl, new_frag)
                replace_nodes(tree, new_frag, node)
            elif node.name == 'a':
                if 'href' in node.attributes:
                    if nofollow:
                        node.attributes['rel'] = 'nofollow'
                    href = node.attributes['href']
                    node.attributes['href'] = filter_url(href)
            elif skip_pre and node.name == 'pre':
                linkify_nodes(node, False)
            else:
                linkify_nodes(node)

    def email_repl(match):
        repl = u'<a href="mailto:%(mail)s">%(mail)s</a>'
        return repl % {'mail': match.group(0).replace('"', '&quot;')}

    def link_repl(match):
        url = match.group(0)
        if re.search(proto_re, url):
            href = url
        else:
            href = u''.join(['http://', url])

        repl = u'<a href="%s"%s>%s</a>'

        return repl % (filter_url(href), rel, filter_text(url))

    linkify_nodes(forest)

    return _render(forest, text)


def _render(tree, source):
    """Try rendering as HTML, then XML, then give up."""
    try:
        return force_unicode(_serialize(tree))
    except Exception, e:
        log.error('HTML: %r ::: %r' % (e, source))
        try:
            return force_unicode(tree.toxml())
        except Exception, e:
            log.error('XML: %r ::: %r' % (e, source))
            return u''


def _serialize(domtree):
    walker = html5lib.treewalkers.getTreeWalker('simpletree')
    stream = walker(domtree)
    serializer = HTMLSerializer(quote_attr_values=True,
                                omit_optional_tags=False)
    return serializer.render(stream)
