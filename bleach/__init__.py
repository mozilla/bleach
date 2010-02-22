import re
import string
import urllib

from django.utils.safestring import SafeData, mark_safe
from django.utils.encoding import force_unicode
from django.utils.http import urlquote
from django.utils.html import escape

import html5lib
from sanitizer import BleachSanitizer

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

# Configuration for linkify() function.
LEADING_PUNCTUATION  = ['(', '<', '&lt;']
TRAILING_PUNCTUATION = ['.', ',', ')', '>', '\n', '&gt;']

TLDS = (
    'com',
    'org',
    'net',
    'edu',
    'gov',
    'co.uk',
    'co.au',
    'ie',
)

word_split_re = re.compile(r'(\s+)')
punctuation_re = re.compile('^(?P<lead>(?:%s)*)(?P<middle>.*?)(?P<trail>(?:%s)*)$' % \
    ('|'.join([re.escape(x) for x in LEADING_PUNCTUATION]),
    '|'.join([re.escape(x) for x in TRAILING_PUNCTUATION])))
simple_email_re = re.compile(r'^\S+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9._-]+$')


class Bleach:


    def bleach(self, string):
        """A shortcut to clean and linkify a string in one quick motion.

        Trade-off: only default configuration options."""

        return self.linkify(self.clean(string))


    def clean(self, string, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES):
        """Clean an HTML string and return it"""

        class s(BleachSanitizer):
            allowed_elements = tags
            allowed_attributes = attributes

        parser = html5lib.HTMLParser(tokenizer=s)

        return force_unicode(parser.parseFragment(string).toxml())


    def linkify(self, text, trim_url_limit=None, nofollow=True, autoescape=False):
        """
        Converts any URLs in text into clickable links.

        Works on http://, https://, www. links and links ending in .org, .net or
        .com. Links can have trailing punctuation (periods, commas, close-parens)
        and leading punctuation (opening parens) and it'll still do the right
        thing.

        If trim_url_limit is not None, the URLs in link text longer than this limit
        will truncated to trim_url_limit-3 characters and appended with an elipsis.

        If nofollow is True, the URLs in link text will get a rel="nofollow"
        attribute.

        If autoescape is True, the link text and URLs will get autoescaped.
        """

        trim_url = lambda x, limit=trim_url_limit: limit is not None and (len(x) > limit and ('%s...' % x[:max(0, limit - 3)])) or x
        safe_input = isinstance(text, SafeData)
        words = word_split_re.split(force_unicode(text))
        nofollow_attr = nofollow and ' rel="nofollow"' or ''
        for i, word in enumerate(words):
            match = None
            if '.' in word or '@' in word or ':' in word:
                match = punctuation_re.match(word)
            if match:
                lead, middle, trail = match.groups()
                # Make URL we want to point to.
                url = None
                is_email = False
                ends_with_tld = False
                for  tld in TLDS:
                    if middle.endswith('.'+tld):
                        ends_with_tld = True

                if middle.startswith('http://') or middle.startswith('https://'):
                    url = urlquote(middle, safe='/&=:;#?+*')
                elif middle.startswith('www.') or ('@' not in middle and \
                        middle and middle[0] in string.ascii_letters + string.digits and \
                        ends_with_tld):
                    url = urlquote('http://%s' % middle, safe='/&=:;#?+*')
                elif '@' in middle and not ':' in middle and simple_email_re.match(middle):
                    is_email = True
                    url = 'mailto:%s' % self.filter_email(middle)
                    nofollow_attr = ''
                # Make link.
                if url:
                    trimmed = trim_url(middle)
                    if autoescape and not safe_input:
                        lead, trail = escape(lead), escape(trail)
                        url, trimmed = escape(url), escape(trimmed)

                    if not is_email:
                        _url = self.filter_url(url)
                        _trimmed = self.filter_url_display(trimmed)
                    else:
                        _url = url
                        _trimmed = self.filter_email_display(trimmed)

                    middle = '<a href="%s"%s>%s</a>' % (_url, nofollow_attr, _trimmed)
                    words[i] = mark_safe('%s%s%s' % (lead, middle, trail))
                else:
                    if safe_input:
                        words[i] = mark_safe(word)
                    elif autoescape:
                        words[i] = escape(word)
            elif safe_input:
                words[i] = mark_safe(word)
            elif autoescape:
                words[i] = escape(word)
        return u''.join(words)


    def filter_url(self, url):
        """Applied to the href attribute of an autolinked URL"""
        return url


    def filter_url_display(self, url):
        """Applied to the innerText of an autolinked URL

        Included for completeness."""
        return url


    def filter_email(self, email):
        """Applied to an email address before its prepended with
        'mailto:'"""
        return email


    def filter_email_display(self, email):
        """Applied to the innerText of an autolinked email address"""
        return email
