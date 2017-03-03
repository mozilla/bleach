from __future__ import unicode_literals
from collections import OrderedDict
import re
from xml.sax.saxutils import unescape

from html5lib.constants import namespaces
from html5lib.filters import sanitizer


def _attr_key(attr):
    """Returns appropriate key for sorting attribute names

    Attribute names are a tuple of ``(namespace, name)`` where namespace can be
    ``None`` or a string. These can't be compared in Python 3, so we conver the
    ``None`` to an empty string.

    """
    key = (attr[0][0] or ''), attr[0][1]
    print(key)
    return key


class BleachSanitizerFilter(sanitizer.Filter):
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
                    token['data'] = OrderedDict(
                        [(key, val) for key, val in sorted(token['data'].items(), key=_attr_key)]
                    )
                return self.disallowed_token(token)

        elif token_type == 'Comment':
            if not self.strip_html_comments:
                return token

        else:
            return token

    def allow_token(self, token):
        if 'data' in token:
            allowed_attributes = self.allowed_attributes_map.get(token['name'], [])
            if not callable(allowed_attributes):
                allowed_attributes += self.wildcard_attributes

            # Drop any attributes that aren't allowed
            attrs = {}
            for namespaced_name, val in token['data'].items():
                namespace, name = namespaced_name

                # See if we should dump the attribute
                if callable(allowed_attributes):
                    if not allowed_attributes(name, val):
                        # DROP!
                        continue

                elif name not in allowed_attributes:
                    # DROP!
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
                        # DROP!
                        continue

                # Drop values in svg attrs with non-local IRIs
                if namespaced_name in self.svg_attr_val_allows_ref:
                    new_val = re.sub(r'url\s*\(\s*[^#\s][^)]+?\)',
                                     ' ',
                                     unescape(val))
                    new_val = new_val.strip()
                    if not new_val:
                        # DROP!
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

            # Alphabetize attributes
            token['data'] = OrderedDict(
                [(key, val) for key, val in sorted(attrs.items(), key=_attr_key)]
            )
        return token

    def sanitize_css(self, style):
        """html5lib sanitizer filter replacement to fix issues"""
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
