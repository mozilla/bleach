# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import logging
import re

import html5lib
from html5lib.filters import sanitizer
from html5lib.filters.sanitizer import allowed_protocols
from html5lib.serializer import HTMLSerializer

from bleach import callbacks as linkify_callbacks
from bleach.encoding import force_unicode
from bleach.linkifier import LinkifyFilter
from bleach.sanitizer import BleachSanitizerFilter
from bleach.version import __version__, VERSION # flake8: noqa

__all__ = ['Cleaner', 'clean', 'linkify']

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())

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

ETREE_TAG = lambda x: "".join(['{http://www.w3.org/1999/xhtml}', x])
# a simple routine that returns the tag name with the namespace prefix
# as returned by etree's Element.tag attribute

DEFAULT_CALLBACKS = [linkify_callbacks.nofollow]


class Cleaner(object):
    """Cleaner for cleaning HTML fragments of malicious content

    This cleaner is a security-focused function whose sole purpose is to remove
    malicious content from a string such that it can be displayed as content in
    a web page.

    This cleaner is not designed to use to transform content to be used in
    non-web-page contexts.

    To use::

        from bleach import Cleaner

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


def clean(text, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES,
          styles=ALLOWED_STYLES, protocols=ALLOWED_PROTOCOLS, strip=False,
          strip_comments=True, filters=None):
    """Clean an HTML fragment of malicious content and return it

    This function is a security-focused function whose sole purpose is to
    remove malicious content from a string such that it can be displayed as
    content in a web page.

    This function is not designed to use to transform content to be used in
    non-web-page contexts.

    Example::

        import bleach

        better_text = bleach.clean(yucky_text)


    .. Note::

       If you're cleaning a lot of text and passing the same argument
       values, consider caching a ``Cleaner`` instance.

    :arg text: the text to clean

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

           Using filters changes the output of
           ``bleach.Cleaner.clean``. Make sure the way the filters
           change the output are secure.

    :returns: cleaned text as unicode

    """
    cleaner = Cleaner(
        tags=tags,
        attributes=attributes,
        styles=styles,
        protocols=protocols,
        strip=strip,
        strip_comments=strip_comments,
        filters=filters,
    )
    return cleaner.clean(text)


def linkify(text, callbacks=DEFAULT_CALLBACKS, skip_pre=False, parse_email=False):
    """Convert URL-like strings in an HTML fragment to links

    ``linkify()`` converts strings that look like URLs, domain names and email
    addresses in text that may be an HTML fragment to links, while preserving:

    1. links already in the string
    2. urls found in attributes
    3. email addresses

    ``linkify()`` does a best-effort approach and tries to recover from bad
    situations due to crazy text.

    """
    parser = html5lib.HTMLParser(namespaceHTMLElements=False)
    walker = html5lib.getTreeWalker('etree')
    serializer = HTMLSerializer(
        quote_attr_values='always',
        omit_optional_tags=False,

        # Bleach has its own sanitizer, so don't use the html5lib one
        sanitize=False,

        # Bleach sanitizer alphabetizes already, so don't use the html5lib one
        alphabetical_attributes=False,
    )

    text = force_unicode(text)

    if not text:
        return u''

    dom = parser.parseFragment(text)
    filtered = LinkifyFilter(
        source=walker(dom),
        callbacks=callbacks,
        skip_pre=skip_pre,
        parse_email=parse_email
    )
    return serializer.render(filtered)
