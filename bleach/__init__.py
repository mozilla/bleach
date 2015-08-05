# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import logging
import re

import html5lib
from html5lib.sanitizer import HTMLSanitizer
from html5lib.serializer.htmlserializer import HTMLSerializer

from . import callbacks as linkify_callbacks
from .encoding import force_unicode
from .sanitizer import BleachSanitizer


VERSION = (1, 4, 2)
__version__ = '.'.join([str(n) for n in VERSION])

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

ALLOWED_PROTOCOLS = ['http', 'https', 'mailto']

TLDS = """abb abbott abogado ac academy accenture accountant accountants active
       actor ad ads adult ae aeg aero af afl ag agency ai aig airforce airtel
       al allfinanz alsace am amsterdam android ao apartments app aq
       aquarelle ar archi army arpa as asia associates at attorney au auction
       audio auto autos aw ax axa az azure ba band bank bar barcelona
       barclaycard barclays bargains bauhaus bayern bb bbc bbva bcn bd be
       beer bentley berlin best bet bf bg bh bharti bi bible bid bike bing
       bingo bio biz bj black blackfriday bloomberg blue bm bmw bn bnl
       bnpparibas bo boats bond boo boutique br bradesco bridgestone broker
       brother brussels bs bt budapest build builders business buzz bv bw by
       bz bzh ca cab cafe cal camera camp cancerresearch canon capetown
       capital caravan cards care career careers cars cartier casa cash
       casino cat catering cba cbn cc cd center ceo cern cf cfa cfd cg ch
       channel chat cheap chloe christmas chrome church ci cisco citic city
       ck cl claims cleaning click clinic clothing cloud club cm cn co coach
       codes coffee college cologne com commbank community company computer
       condos construction consulting contractors cooking cool coop corsica
       country coupons courses cr credit creditcard cricket crown crs cruises
       cu cuisinella cv cw cx cy cymru cyou cz dabur dad dance date dating
       datsun day dclk de deals degree delivery delta democrat dental dentist
       desi design dev diamonds diet digital direct directory discount dj dk
       dm dnp do docs dog doha domains doosan download drive durban dvag dz
       earth eat ec edu education ee eg email emerck energy engineer
       engineering enterprises epson equipment er erni es esq estate et eu
       eurovision eus events everbank exchange expert exposed express fail
       faith fan fans farm fashion feedback fi film finance financial
       firmdale fish fishing fit fitness fj fk flights florist flowers
       flsmidth fly fm fo foo football forex forsale forum foundation fr frl
       frogans fund furniture futbol fyi ga gal gallery game garden gb gbiz
       gd gdn ge gent genting gf gg ggee gh gi gift gifts gives gl glass gle
       global globo gm gmail gmo gmx gn gold goldpoint golf goo goog google
       gop gov gp gq gr graphics gratis green gripe gs gt gu guge guide
       guitars guru gw gy hamburg hangout haus healthcare help here hermes
       hiphop hitachi hiv hk hm hn hockey holdings holiday homedepot homes
       honda horse host hosting hoteles hotmail house how hr hsbc ht hu ibm
       icbc ice icu id ie ifm iinet il im immo immobilien in industries
       infiniti info ing ink institute insure int international investments
       io ipiranga iq ir irish is ist istanbul it itau iwc java jcb je jetzt
       jewelry jlc jll jm jo jobs joburg jp jprs juegos kaufen kddi ke kg kh
       ki kim kitchen kiwi km kn koeln komatsu kp kr krd kred kw ky kyoto kz
       la lacaixa lancaster land lasalle lat latrobe law lawyer lb lc lds
       lease leclerc legal lexus lgbt li liaison lidl life lighting limited
       limo link live lixil lk loan loans lol london lotte lotto love lr ls
       lt ltda lu lupin luxe luxury lv ly ma madrid maif maison man
       management mango market marketing markets marriott mba mc md me media
       meet melbourne meme memorial men menu mg mh miami microsoft mil mini
       mk ml mm mma mn mo mobi moda moe monash money montblanc mormon
       mortgage moscow motorcycles mov movie movistar mp mq mr ms mt mtn mtpc
       mu museum mv mw mx my mz na nadex nagoya name navy nc ne nec net
       netbank network neustar new news nexus nf ng ngo nhk ni nico ninja
       nissan nl no nokia np nr nra nrw ntt nu nyc nz office okinawa om omega
       one ong onl online ooo oracle orange org organic osaka otsuka ovh pa
       page panerai paris partners parts party pe pet pf pg ph pharmacy
       philips photo photography photos physio piaget pics pictet pictures
       pink pizza pk pl place play plumbing plus pm pn pohl poker porn post
       pr praxi press pro prod productions prof properties property ps pt pub
       pw py qa qpon quebec racing re realtor realty recipes red redstone
       rehab reise reisen reit ren rent rentals repair report republican rest
       restaurant review reviews rich ricoh rio rip ro rocks rodeo rs rsvp ru
       ruhr run rw ryukyu sa saarland sakura sale samsung sandvik
       sandvikcoromant sanofi sap sarl saxo sb sc sca scb schmidt
       scholarships school schule schwarz science scor scot sd se seat sener
       services sew sex sexy sg sh shiksha shoes show shriram si singles site
       sj sk ski sky skype sl sm sn sncf so soccer social software sohu solar
       solutions sony soy space spiegel spreadbetting sr srl st starhub
       statoil studio study style su sucks supplies supply support surf
       surgery suzuki sv swatch swiss sx sy sydney systems sz taipei
       tatamotors tatar tattoo tax taxi tc td team tech technology tel
       telefonica temasek tennis tf tg th thd theater tickets tienda tips
       tires tirol tj tk tl tm tn to today tokyo tools top toray toshiba
       tours town toyota toys tr trade trading training travel trust tt tui
       tv tw tz ua ubs ug uk university uno uol us uy uz va vacations vc ve
       vegas ventures versicherung vet vg vi viajes video villas vision vista
       vistaprint vlaanderen vn vodka vote voting voto voyage vu wales walter
       wang watch webcam website wed wedding weir wf whoswho wien wiki
       williamhill win windows wme work works world ws wtc wtf xbox xerox xin
       xn--11b4c3d xn--1qqw23a xn--30rr7y xn--3bst00m xn--3ds443g
       xn--3e0b707e xn--3pxu8k xn--42c2d9a xn--45brj9c xn--45q11c xn--4gbrim
       xn--55qw42g xn--55qx5d xn--6frz82g xn--6qq986b3xl xn--80adxhks
       xn--80ao21a xn--80asehdb xn--80aswg xn--90a3ac xn--90ais xn--9dbq2a
       xn--9et52u xn--b4w605ferd xn--c1avg xn--c2br7g xn--cg4bki
       xn--clchc0ea0b2g2a9gcd xn--czr694b xn--czrs0t xn--czru2d xn--d1acj3b
       xn--d1alf xn--estv75g xn--fhbei xn--fiq228c5hs xn--fiq64b xn--fiqs8s
       xn--fiqz9s xn--fjq720a xn--flw351e xn--fpcrj9c3d xn--fzc2c9e2c
       xn--gecrj9c xn--h2brj9c xn--hxt814e xn--i1b6b1a6a2e xn--imr513n
       xn--io0a7i xn--j1aef xn--j1amh xn--j6w193g xn--kcrx77d1x4a xn--kprw13d
       xn--kpry57d xn--kput3i xn--l1acc xn--lgbbat1ad8j xn--mgb9awbf
       xn--mgba3a4f16a xn--mgbaam7a8h xn--mgbab2bd xn--mgbayh7gpa
       xn--mgbbh1a71e xn--mgbc0a9azcg xn--mgberp4a5d4ar xn--mgbpl2fh
       xn--mgbx4cd0ab xn--mk1bu44c xn--mxtq1m xn--ngbc5azd xn--node xn--nqv7f
       xn--nqv7fs00ema xn--nyqy26a xn--o3cw4h xn--ogbpf8fl xn--p1acf xn--p1ai
       xn--pgbs0dh xn--pssy2u xn--q9jyb4c xn--qcka1pmc xn--rhqv96g
       xn--s9brj9c xn--ses554g xn--t60b56a xn--tckwe xn--unup4y
       xn--vermgensberater-ctb xn--vermgensberatung-pwb xn--vhquv xn--vuq861b
       xn--wgbh1c xn--wgbl6a xn--xhq521b xn--xkc2al3hye2a xn--xkc2dl3a5ee0h
       xn--y9a3aq xn--yfro4i67o xn--ygbi2ammx xn--zfr164b xxx xyz yachts
       yandex ye yodobashi yoga yokohama youtube yt za zip zm zone zuerich
       zw""".split()

# Make sure that .com doesn't get matched by .co first
TLDS.reverse()

PROTOCOLS = HTMLSanitizer.acceptable_protocols

url_re = re.compile(
    r"""\(*  # Match any opening parentheses.
    \b(?<![@.])(?:(?:{0}):/{{0,3}}(?:(?:\w+:)?\w+@)?)?  # http://
    ([\w-]+\.)+(?:{1})(?:\:\d+)?(?!\.\w)\b   # xx.yy.tld(:##)?
    (?:[/?][^\s\{{\}}\|\\\^\[\]`<>"]*)?
        # /path/zz (excluding "unsafe" chars from RFC 1738,
        # except for # and ~, which happen in practice)
    """.format('|'.join(PROTOCOLS), '|'.join(TLDS)),
    re.IGNORECASE | re.VERBOSE | re.UNICODE)

proto_re = re.compile(r'^[\w-]+:/{0,3}', re.IGNORECASE)

punct_re = re.compile(r'([\.,]+)$')

email_re = re.compile(
    r"""(?<!//)
    (([-!#$%&'*+/=?^_`{0!s}|~0-9A-Z]+
        (\.[-!#$%&'*+/=?^_`{1!s}|~0-9A-Z]+)*  # dot-atom
    |^"([\001-\010\013\014\016-\037!#-\[\]-\177]
        |\\[\001-011\013\014\016-\177])*"  # quoted-string
    )@(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6})\.?  # domain
    """,
    re.IGNORECASE | re.MULTILINE | re.VERBOSE)

NODE_TEXT = 4  # The numeric ID of a text node in simpletree.

ETREE_TAG = lambda x: "".join(['{http://www.w3.org/1999/xhtml}', x])
# a simple routine that returns the tag name with the namespace prefix
# as returned by etree's Element.tag attribute

DEFAULT_CALLBACKS = [linkify_callbacks.nofollow]


def clean(text, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES,
          styles=ALLOWED_STYLES, protocols=ALLOWED_PROTOCOLS, strip=False,
          strip_comments=True):
    """Clean an HTML fragment and return it"""
    if not text:
        return ''

    text = force_unicode(text)

    class s(BleachSanitizer):
        allowed_elements = tags
        allowed_attributes = attributes
        allowed_css_properties = styles
        allowed_protocols = protocols
        strip_disallowed_elements = strip
        strip_html_comments = strip_comments

    parser = html5lib.HTMLParser(tokenizer=s)

    return _render(parser.parseFragment(text))


def linkify(text, callbacks=DEFAULT_CALLBACKS, skip_pre=False,
            parse_email=False, tokenizer=HTMLSanitizer):
    """Convert URL-like strings in an HTML fragment to links.

    linkify() converts strings that look like URLs or domain names in a
    blob of text that may be an HTML fragment to links, while preserving
    (a) links already in the string, (b) urls found in attributes, and
    (c) email addresses.
    """
    text = force_unicode(text)

    if not text:
        return ''

    parser = html5lib.HTMLParser(tokenizer=tokenizer)

    forest = parser.parseFragment(text)
    _seen = set([])

    def replace_nodes(tree, new_frag, node, index=0):
        """
        Doesn't really replace nodes, but inserts the nodes contained in
        new_frag into the treee at position index and returns the number
        of nodes inserted.
        If node is passed in, it is removed from the tree
        """
        count = 0
        new_tree = parser.parseFragment(new_frag)
        # capture any non-tag text at the start of the fragment
        if new_tree.text:
            if index == 0:
                tree.text = tree.text or ''
                tree.text += new_tree.text
            else:
                tree[index - 1].tail = tree[index - 1].tail or ''
                tree[index - 1].tail += new_tree.text
        # the put in the tagged elements into the old tree
        for n in new_tree:
            if n.tag == ETREE_TAG('a'):
                _seen.add(n)
            tree.insert(index + count, n)
            count += 1
        # if we got a node to remove...
        if node is not None:
            tree.remove(node)
        return count

    def strip_wrapping_parentheses(fragment):
        """Strips wrapping parentheses.

        Returns a tuple of the following format::

            (string stripped from wrapping parentheses,
             count of stripped opening parentheses,
             count of stripped closing parentheses)
        """
        opening_parentheses = closing_parentheses = 0
        # Count consecutive opening parentheses
        # at the beginning of the fragment (string).
        for char in fragment:
            if char == '(':
                opening_parentheses += 1
            else:
                break

        if opening_parentheses:
            newer_frag = ''
            # Cut the consecutive opening brackets from the fragment.
            fragment = fragment[opening_parentheses:]
            # Reverse the fragment for easier detection of parentheses
            # inside the URL.
            reverse_fragment = fragment[::-1]
            skip = False
            for char in reverse_fragment:
                # Remove the closing parentheses if it has a matching
                # opening parentheses (they are balanced).
                if (char == ')' and
                        closing_parentheses < opening_parentheses and
                        not skip):
                    closing_parentheses += 1
                    continue
                # Do not remove ')' from the URL itself.
                elif char != ')':
                    skip = True
                newer_frag += char
            fragment = newer_frag[::-1]

        return fragment, opening_parentheses, closing_parentheses

    def apply_callbacks(attrs, new):
        for cb in callbacks:
            attrs = cb(attrs, new)
            if attrs is None:
                return None
        return attrs

    def _render_inner(node):
        out = ['' if node.text is None else node.text]
        for subnode in node:
            out.append(_render(subnode))
            if subnode.tail:
                out.append(subnode.tail)
        return ''.join(out)

    def linkify_nodes(tree, parse_text=True):
        children = len(tree)
        current_child = -1
        # start at -1 to process the parent first
        while current_child < len(tree):
            if current_child < 0:
                node = tree
                if parse_text and node.text:
                    new_txt = old_txt = node.text
                    if parse_email:
                        new_txt = re.sub(email_re, email_repl, node.text)
                        if new_txt and new_txt != node.text:
                            node.text = ''
                            adj = replace_nodes(tree, new_txt, None, 0)
                            children += adj
                            current_child += adj
                            linkify_nodes(tree, True)
                            continue

                    new_txt = re.sub(url_re, link_repl, new_txt)
                    if new_txt != old_txt:
                        node.text = ''
                        adj = replace_nodes(tree, new_txt, None, 0)
                        children += adj
                        current_child += adj
                        continue
            else:
                node = tree[current_child]

            if parse_text and node.tail:
                new_tail = old_tail = node.tail
                if parse_email:
                    new_tail = re.sub(email_re, email_repl, new_tail)
                    if new_tail != node.tail:
                        node.tail = ''
                        adj = replace_nodes(tree, new_tail, None,
                                            current_child + 1)
                        # Insert the new nodes made from my tail into
                        # the tree right after me. current_child+1
                        children += adj
                        continue

                new_tail = re.sub(url_re, link_repl, new_tail)
                if new_tail != old_tail:
                    node.tail = ''
                    adj = replace_nodes(tree, new_tail, None,
                                        current_child + 1)
                    children += adj

            if node.tag == ETREE_TAG('a') and not (node in _seen):
                if not node.get('href', None) is None:
                    attrs = dict(node.items())

                    _text = attrs['_text'] = _render_inner(node)

                    attrs = apply_callbacks(attrs, False)

                    if attrs is None:
                        # <a> tag replaced by the text within it
                        adj = replace_nodes(tree, _text, node,
                                            current_child)
                        current_child -= 1
                        # pull back current_child by 1 to scan the
                        # new nodes again.
                    else:
                        text = force_unicode(attrs.pop('_text'))
                        for attr_key, attr_val in attrs.items():
                            node.set(attr_key, attr_val)

                        for n in reversed(list(node)):
                            node.remove(n)
                        text = parser.parseFragment(text)
                        node.text = text.text
                        for n in text:
                            node.append(n)
                        _seen.add(node)

            elif current_child >= 0:
                if node.tag == ETREE_TAG('pre') and skip_pre:
                    linkify_nodes(node, False)
                elif not (node in _seen):
                    linkify_nodes(node, True)

            current_child += 1

    def email_repl(match):
        addr = match.group(0).replace('"', '&quot;')
        link = {
            '_text': addr,
            'href': 'mailto:{0!s}'.format(addr),
        }
        link = apply_callbacks(link, True)

        if link is None:
            return addr

        _href = link.pop('href')
        _text = link.pop('_text')

        repl = '<a href="{0!s}" {1!s}>{2!s}</a>'
        attr = '{0!s}="{1!s}"'
        attribs = ' '.join(attr.format(k, v) for k, v in link.items())
        return repl.format(_href, attribs, _text)

    def link_repl(match):
        url = match.group(0)
        open_brackets = close_brackets = 0
        if url.startswith('('):
            _wrapping = strip_wrapping_parentheses(url)
            url, open_brackets, close_brackets = _wrapping
        end = ''
        m = re.search(punct_re, url)
        if m:
            end = m.group(0)
            url = url[0:m.start()]
        if re.search(proto_re, url):
            href = url
        else:
            href = ''.join(['http://', url])

        link = {
            '_text': url,
            'href': href,
        }

        link = apply_callbacks(link, True)

        if link is None:
            return '(' * open_brackets + url + ')' * close_brackets

        _text = link.pop('_text')
        _href = link.pop('href')

        repl = '{0!s}<a href="{1!s}" {2!s}>{3!s}</a>{4!s}{5!s}'
        attr = '{0!s}="{1!s}"'
        attribs = ' '.join(attr.format(k, v) for k, v in link.items())

        return repl.format('(' * open_brackets,
                           _href, attribs, _text, end,
                           ')' * close_brackets)

    try:
        linkify_nodes(forest)
    except RuntimeError as e:
        # If we hit the max recursion depth, just return what we've got.
        log.exception('Probable recursion error: {0!r}'.format(e))

    return _render(forest)


def _render(tree):
    """Try rendering as HTML, then XML, then give up."""
    return force_unicode(_serialize(tree))


def _serialize(domtree):
    walker = html5lib.treewalkers.getTreeWalker('etree')
    stream = walker(domtree)
    serializer = HTMLSerializer(quote_attr_values=True,
                                alphabetical_attributes=True,
                                omit_optional_tags=False)
    return serializer.render(stream)
