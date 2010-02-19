from copy import copy

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

def clean(string, allowed_tags=None, allowed_attributes=None):
    """Clean an HTML string and return it"""

    if allowed_tags is None:
        allowed_tags = ALLOWED_TAGS

    if allowed_attributes is None:
        allowed_attributes = ALLOWED_ATTRIBUTES

    s = copy(sanitizer.HTMLSanitizer)

    s.allowed_elements = allowed_tags
    s.allowed_attributes = allowed_attributes

    parser = html5lib.HTMLParser(tokenizer=s)

    return parser.parseFragment(string).toxml()
