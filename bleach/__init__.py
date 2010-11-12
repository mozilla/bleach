import logging
import re

import html5lib
from html5lib.serializer.htmlserializer import HTMLSerializer
from sanitizer import BleachSanitizer
from encoding import force_unicode

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

ALLOWED_STYLES = BleachSanitizer.acceptable_css_properties

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


url_re = re.compile(r"""\b(?:[\w-]+:/{0,3})?  # http://
                    (?<!@)([\w-]+\.)+(?:%s)     # xx.yy.tld
                    (?:[/?][^\s\{\}\|\\\^\[\]`<>"\x80-\xFF\x00-\x1F\x7F]*)?
                        # /path/zz (excluding "unsafe" chars from RFC 1738,
                        # except for # and ~, which happen in practice)
                    \b                        # Break at a word boundary.
                    """ % u'|'.join(TLDS),
                    re.VERBOSE)
proto_re = re.compile(r'^[\w-]+:/{0,3}')


NODE_TEXT = 4  # the numeric ID of a text node in simpletree


class BleachHTMLParser(html5lib.HTMLParser):
    """HTML parser which adds support for changing more tokenizer options."""

    def parseFragment(self, stream, container="div", encoding=None,
                      parseMeta=False, useChardet=True, **kwargs):
        """Parse a HTML fragment into a well-formed tree fragment

        container - name of the element we're setting the innerHTML property
        if set to None, default to 'div'

        stream - a filelike object or string containing the HTML to be parsed

        The optional encoding parameter must be a string that indicates
        the encoding.  If specified, that encoding will be used,
        regardless of any BOM or later declaration (such as in a meta
        element)
        """
        self._parse(stream, True, container=container, encoding=encoding,
                    parseMeta=parseMeta, useChardet=useChardet, **kwargs)
        return self.tree.getFragment()


class BleachHTMLSerializer(HTMLSerializer):
    omit_optional_tags = False
    quote_attr_values = True
    use_trailing_solidus = True


class Bleach:

    def bleach(self, string):
        """A shortcut to clean and linkify a string in one quick motion.

        Trade-off: only default configuration options."""

        return self.linkify(self.clean(string))

    def clean(self, string, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES,
              strip=False, strip_comments=True, lowercase=False,
              styles=ALLOWED_STYLES, sanitizer_class=None,
              serializer_class=None):
        """Clean an HTML string and return it"""
        if not string:
            return u''
        elif string.startswith('<!--'):
            string = u' ' + string

        if not sanitizer_class:
            sanitizer_class = BleachSanitizer

        class s(sanitizer_class):
            allowed_elements = tags
            allowed_attributes = attributes
            allowed_css_properties = styles
            strip_disallowed_elements = strip
            strip_html_comments = strip_comments

        parser = BleachHTMLParser(tokenizer=s)

        tree = parser.parseFragment(string, lowercaseElementName=lowercase,
                                    lowercaseAttrName=lowercase)

        return render(tree, string, serializer_class=serializer_class).strip()

    def linkify(self, text, nofollow=True, serializer_class=None):
        """Convert URL-like strings in an HTML fragment to links.

        linkify() converts strings that look like URLs or domain names in a
        blob of text that may be an HTML fragment to links, while preserving
        (a) links already in the string, (b) urls found in attributes, and
        (c) email addresses.

        If the nofollow argument is True (the default) then rel="nofollow"
        will be added to links created by linkify() as well as links already
        found in the text.

        linkify() uses up to two filters on each link. For links created by
        linkify(), the href attribute is passed through Bleach.filter_url()
        and the text of the link is passed through filter_text(). For links
        already found in the document, the href attribute is passed through
        filter_url(), but the text is untouched.

        To implement custom filters, you should create a subclass of Bleach
        and override these functions.
        """
        if not text:
            return u''

        parser = html5lib.HTMLParser()

        forest = parser.parseFragment(text)

        if nofollow:
            rel = u' rel="nofollow"'
        else:
            rel = u''

        def linkify_nodes(tree):
            for node in tree.childNodes:
                if node.type == NODE_TEXT:
                    new_frag = re.sub(url_re, link_repl, node.toxml())
                    new_tree = parser.parseFragment(new_frag)
                    for n in new_tree.childNodes:
                        tree.insertBefore(n, node)
                    tree.removeChild(node)
                else:
                    if node.name == 'a':
                        if nofollow:
                            node.attributes['rel'] = 'nofollow'
                        try:
                            href = self.filter_url(node.attributes['href'])
                            node.attributes['href'] = href
                        except KeyError:
                            pass
                    else:
                        linkify_nodes(node)

        def link_repl(match):
            url = match.group(0)
            if re.search(proto_re, url):
                href = url
            else:
                href = u''.join(['http://', url])

            repl = u'<a href="%s"%s>%s</a>'

            return repl % (self.filter_url(href), rel,
                           self.filter_text(url))

        linkify_nodes(forest)

        return render(forest, text, serializer_class=serializer_class)

    def filter_url(self, url):
        """Applied to the href attribute of an autolinked URL"""
        return url

    def filter_text(self, url):
        """Applied to the innerText of an autolinked URL"""
        return url


def render(tree, source, serializer_class=None):
    """Try rendering as HTML, then XML, then give up."""
    try:
        return force_unicode(_serialize(tree,
                                        serializer_class=serializer_class))
    except Exception, e:
        log.error('HTML: %r ::: %r' % (e, source))
        try:
            return force_unicode(tree.toxml())
        except Exception, e:
            log.error('XML: %r ::: %r' % (e, source))
            return u''


def _serialize(domtree, serializer_class=None):
    if not serializer_class:
        serializer_class = BleachHTMLSerializer
    walker = html5lib.treewalkers.getTreeWalker('simpletree')
    stream = walker(domtree)
    serializer = serializer_class()
    return serializer.render(stream)
