from __future__ import unicode_literals
import re
from xml.sax.saxutils import unescape

import html5lib
from html5lib.constants import namespaces
from html5lib.filters import sanitizer
from html5lib.serializer import HTMLSerializer

from bleach.encoding import force_unicode
from bleach.utils import alphabetize_attributes


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


class Cleaner(object):
    """Cleaner for cleaning HTML fragments of malicious content

    This cleaner is a security-focused function whose sole purpose is to remove
    malicious content from a string such that it can be displayed as content in
    a web page.

    This cleaner is not designed to use to transform content to be used in
    non-web-page contexts.

    To use::

        from bleach.sanitizer import Cleaner

        cleaner = Cleaner()

        for text in all_the_yucky_things:
            sanitized = cleaner.clean(text)

    """

    def __init__(self, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES,
                 styles=ALLOWED_STYLES, protocols=ALLOWED_PROTOCOLS, strip=False,
                 strip_comments=True, filters=None):
        """Initializes a Cleaner

        :arg tags: whitelist of allowed tags; defaults to
            ``bleach.ALLOWED_TAGS``

        :arg attributes: whitelist of allowed attributes; defaults to
            ``bleach.ALLOWED_ATTRIBUTES``

        :arg styles: whitelist of allowed css; defaults to
            ``bleach.ALLOWED_STYLES``

        :arg protocols: whitelist of allowed protocols for links; defaults
            to ``bleach.ALLOWED_PROTOCOLS``

        :arg strip: whether or not to strip disallowed elements

        :arg strip_comments: whether or not to strip HTML comments

        :arg filters: list of html5lib Filter classes to pass streamed content through

            See http://html5lib.readthedocs.io/en/latest/movingparts.html#filters

            .. Warning::

               Using filters changes the output of ``bleach.Cleaner.clean``.
               Make sure the way the filters change the output are secure.

        """
        self.tags = tags
        self.attributes = attributes
        self.styles = styles
        self.protocols = protocols
        self.strip = strip
        self.strip_comments = strip_comments
        self.filters = filters or []

        self.parser = html5lib.HTMLParser(namespaceHTMLElements=False)
        self.walker = html5lib.getTreeWalker('etree')
        self.serializer = HTMLSerializer(
            quote_attr_values='always',
            omit_optional_tags=False,

            # Bleach has its own sanitizer, so don't use the html5lib one
            sanitize=False,

            # Bleach sanitizer alphabetizes already, so don't use the html5lib one
            alphabetical_attributes=False,
        )

    def clean(self, text):
        """Cleans text and returns sanitized result as unicode

        :arg str text: text to be cleaned

        :returns: sanitized text as unicode

        """
        if not text:
            return u''

        text = force_unicode(text)

        dom = self.parser.parseFragment(text)
        filtered = BleachSanitizerFilter(
            source=self.walker(dom),

            # Bleach-sanitizer-specific things
            allowed_attributes_map=self.attributes,
            strip_disallowed_elements=self.strip,
            strip_html_comments=self.strip_comments,

            # html5lib-sanitizer things
            allowed_elements=self.tags,
            allowed_css_properties=self.styles,
            allowed_protocols=self.protocols,
            allowed_svg_properties=[],
        )

        # Apply any filters after the BleachSanitizerFilter
        for filter_class in self.filters:
            filtered = filter_class(source=filtered)

        return self.serializer.render(filtered)


class BleachSanitizerFilter(sanitizer.Filter):
    """html5lib Filter that sanitizes text

    This filter can be used anywhere html5lib filters can be used.

    """
    def __init__(self, source, allowed_attributes_map,
                 strip_disallowed_elements=False, strip_html_comments=True,
                 **kwargs):

        if isinstance(allowed_attributes_map, dict):
            self.wildcard_attributes = allowed_attributes_map.get('*', [])
            self.allowed_attributes_map = allowed_attributes_map
        else:
            self.wildcard_attributes = allowed_attributes_map
            self.allowed_attributes_map = {}

        self.strip_disallowed_elements = strip_disallowed_elements
        self.strip_html_comments = strip_html_comments

        return super(BleachSanitizerFilter, self).__init__(source, **kwargs)

    def sanitize_token(self, token):
        """Sanitize a token either by HTML-encoding or dropping.

        Unlike sanitizer.Filter, allowed_attributes can be a dict of {'tag':
        ['attribute', 'pairs'], 'tag': callable}.

        Here callable is a function with two arguments of attribute name and
        value. It should return true of false.

        Also gives the option to strip tags instead of encoding.

        """
        token_type = token['type']
        if token_type in ['StartTag', 'EndTag', 'EmptyTag']:
            if token['name'] in self.allowed_elements:
                return self.allow_token(token)

            elif self.strip_disallowed_elements:
                pass

            else:
                if 'data' in token:
                    # Alphabetize the attributes before calling .disallowed_token()
                    # so that the resulting string is stable
                    token['data'] = alphabetize_attributes(token['data'])
                return self.disallowed_token(token)

        elif token_type == 'Comment':
            if not self.strip_html_comments:
                return token

        else:
            return token

    def allow_token(self, token):
        """Handles the case where we're allowing the tag"""
        if 'data' in token:
            allowed_attributes = self.allowed_attributes_map.get(token['name'], [])
            if not callable(allowed_attributes):
                allowed_attributes += self.wildcard_attributes

            # Loop through all the attributes and drop the ones that are not
            # allowed, are unsafe or break other rules. Additionally, fix
            # attribute values that need fixing.
            #
            # At the end of this loop, we have the final set of attributes
            # we're keeping.
            attrs = {}
            for namespaced_name, val in token['data'].items():
                namespace, name = namespaced_name

                # Drop attributes that are not explicitly allowed
                if callable(allowed_attributes):
                    if not allowed_attributes(name, val):
                        continue

                elif name not in allowed_attributes:
                    continue

                # Look at attributes that have uri values
                if namespaced_name in self.attr_val_is_uri:
                    val_unescaped = re.sub(
                        "[`\000-\040\177-\240\s]+",
                        '',
                        unescape(val)).lower()

                    # Remove replacement characters from unescaped characters.
                    val_unescaped = val_unescaped.replace("\ufffd", "")

                    # Drop attributes with uri values that have protocols that
                    # aren't allowed
                    if (re.match(r'^[a-z0-9][-+.a-z0-9]*:', val_unescaped) and
                            (val_unescaped.split(':')[0] not in self.allowed_protocols)):
                        continue

                # Drop values in svg attrs with non-local IRIs
                if namespaced_name in self.svg_attr_val_allows_ref:
                    new_val = re.sub(r'url\s*\(\s*[^#\s][^)]+?\)',
                                     ' ',
                                     unescape(val))
                    new_val = new_val.strip()
                    if not new_val:
                        continue

                    else:
                        # Replace the val with the unescaped version because
                        # it's a iri
                        val = new_val

                # Drop href and xlink:href attr for svg elements with non-local IRIs
                if (None, token['name']) in self.svg_allow_local_href:
                    if namespaced_name in [(None, 'href'), (namespaces['xlink'], 'href')]:
                        if re.search(r'^\s*[^#\s]', val):
                            continue

                # If it's a style attribute, sanitize it
                if namespaced_name == (None, u'style'):
                    val = self.sanitize_css(val)

                # At this point, we want to keep the attribute, so add it in
                attrs[namespaced_name] = val

            token['data'] = alphabetize_attributes(attrs)

        return token

    def sanitize_css(self, style):
        """Sanitizes css in style tags"""
        # disallow urls
        style = re.compile('url\s*\(\s*[^\s)]+?\s*\)\s*').sub(' ', style)

        # gauntlet

        # Validate the css in the style tag and if it's not valid, then drop
        # the whole thing.
        parts = style.split(';')
        gauntlet = re.compile(
            r"""^([-/:,#%.'"\sa-zA-Z0-9!]|\w-\w|'[\s\w]+'\s*|"[\s\w]+"|\([\d,%\.\s]+\))*$"""
        )

        for part in parts:
            if not gauntlet.match(part):
                return ''

        if not re.match("^\s*([-\w]+\s*:[^:;]*(;\s*|$))*$", style):
            return ''

        clean = []
        for prop, value in re.findall('([-\w]+)\s*:\s*([^:;]*)', style):
            if not value:
                continue

            if prop.lower() in self.allowed_css_properties:
                clean.append(prop + ': ' + value + ';')

            elif prop.lower() in self.allowed_svg_properties:
                clean.append(prop + ': ' + value + ';')

        return ' '.join(clean)
