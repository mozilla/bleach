import html5lib
from html5lib import sanitizer

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

ALLOWED_ATTRIBUTES = [
    'href',
    'title',
]

def clean(string, tags=None, attributes=None):
    """Clean an HTML string and return it"""

    if tags is None:
        tags = ALLOWED_TAGS

    if attributes is None:
        attributes = ALLOWED_ATTRIBUTES

    class s(sanitizer.HTMLSanitizer):
        allowed_elements = tags
        allowed_attributes = attributes

    parser = html5lib.HTMLParser(tokenizer=s)

    return parser.parseFragment(string).toxml()
