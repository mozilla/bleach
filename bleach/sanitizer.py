import re
from xml.sax.saxutils import escape, unescape

from html5lib.constants import tokenTypes
from html5lib.sanitizer import HTMLSanitizerMixin
from html5lib.tokenizer import HTMLTokenizer


class BleachSanitizerMixin(HTMLSanitizerMixin):
    """Mixin to replace sanitize_token() with a more flexible version."""

    def sanitize_token(self, token):
        if token['type'] in (tokenTypes['StartTag'], tokenTypes['EndTag'],
                             tokenTypes['EmptyTag']):
            if token['name'] in self.allowed_elements:
                if 'data' in token:
                    if isinstance(self.allowed_attributes, dict):
                        allowed_attributes = self.allowed_attributes.get(
                            token['name'], [])
                    else:
                        allowed_attributes = self.allowed_attributes
                    attrs = dict([(name, val) for name, val in
                                  token['data'][::-1]
                                  if name in allowed_attributes])
                    for attr in self.attr_val_is_uri:
                        if not attr in attrs:
                            continue
                        val_unescaped = re.sub("[`\000-\040\177-\240\s]+", '',
                                               unescape(attrs[attr])).lower()
                        # Remove replacement characters from unescaped
                        # characters.
                        val_unescaped = val_unescaped.replace(u"\ufffd", "")
                        if (re.match(r'^[a-z0-9][-+.a-z0-9]*:', val_unescaped)
                            and (val_unescaped.split(':')[0] not in
                                 self.allowed_protocols)):
                            del attrs[attr]
                    for attr in self.svg_attr_val_allows_ref:
                        if attr in attrs:
                            attrs[attr] = re.sub(r'url\s*\(\s*[^#\s][^)]+?\)',
                                                 ' ',
                                                 unescape(attrs[attr]))
                    if (token['name'] in self.svg_allow_local_href and
                        'xlink:href' in attrs and
                        re.search(r'^\s*[^#\s].*', attrs['xlink:href'])):
                        del attrs['xlink:href']
                    if 'style' in attrs:
                        attrs['style'] = self.sanitize_css(attrs['style'])
                    token['data'] = [(name, val) for name, val in
                                     attrs.items()]
                return token
            elif self.strip_disallowed_elements:
                pass
            else:
                if token['type'] == tokenTypes['EndTag']:
                    token['data'] = '</%s>' % token['name']
                elif token['data']:
                    attrs = ''.join([' %s="%s"' % (k, escape(v)) for k, v in
                                    token['data']])
                    token['data'] = '<%s%s>' % (token['name'], attrs)
                else:
                    token['data'] = '<%s>' % token['name']
                if token['selfClosing']:
                    token['data'] = token['data'][:-1] + '/>'
                token['type'] = tokenTypes['Characters']
                del token["name"]
                return token
        elif token['type'] == tokenTypes['Comment']:
            if not self.strip_html_comments:
                return token
        else:
            return token


class BleachSanitizer(HTMLTokenizer, BleachSanitizerMixin):
    def __init__(self, stream, encoding=None, parseMeta=True, useChardet=True,
                 lowercaseElementName=True, lowercaseAttrName=True):
        HTMLTokenizer.__init__(self, stream, encoding, parseMeta, useChardet,
                               lowercaseElementName, lowercaseAttrName)

    def __iter__(self):
        for token in HTMLTokenizer.__iter__(self):
            token = self.sanitize_token(token)
            if token:
                yield token
