# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from bleach.linkifier import (
    DEFAULT_CALLBACKS,
    Linker,
    LinkifyFilter,
)
from bleach.sanitizer import (
    ALLOWED_ATTRIBUTES,
    ALLOWED_PROTOCOLS,
    ALLOWED_STYLES,
    ALLOWED_TAGS,
    BleachSanitizerFilter,
    Cleaner,
)
from bleach.version import __version__, VERSION # flake8: noqa

__all__ = ['clean', 'linkify']


def clean(text, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES,
          styles=ALLOWED_STYLES, protocols=ALLOWED_PROTOCOLS, strip=False,
          strip_comments=True):
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

       If you're cleaning a lot of text and passing the same argument values or
       you want more configurability, consider using a
       :py:class:`bleach.sanitizer.Cleaner` instance.

    :arg str text: the text to clean

    :arg list tags: whitelist of allowed tags; defaults to
        ``bleach.ALLOWED_TAGS``

    :arg dict attributes: whitelist of allowed attributes; defaults to
        ``bleach.ALLOWED_ATTRIBUTES``

    :arg list styles: whitelist of allowed css; defaults to
        ``bleach.ALLOWED_STYLES``

    :arg list protocols: whitelist of allowed protocols for links; defaults
        to ``bleach.ALLOWED_PROTOCOLS``

    :arg bool strip: whether or not to strip disallowed elements

    :arg bool strip_comments: whether or not to strip HTML comments

    :returns: cleaned text as unicode

    """
    cleaner = Cleaner(
        tags=tags,
        attributes=attributes,
        styles=styles,
        protocols=protocols,
        strip=strip,
        strip_comments=strip_comments,
    )
    return cleaner.clean(text)


def linkify(text, callbacks=DEFAULT_CALLBACKS, skip_pre=False, parse_email=False):
    """Convert URL-like strings in an HTML fragment to links

    This function converts strings that look like URLs, domain names and email
    addresses in text that may be an HTML fragment to links, while preserving:

    1. links already in the string
    2. urls found in attributes
    3. email addresses

    linkify does a best-effort approach and tries to recover from bad
    situations due to crazy text.

    .. Note::

       If you're linking a lot of text and passing the same argument values or
       you want more configurability, consider using a
       :py:class:`bleach.linkifier.Linker` instance.

    .. Note::

       If you have text that you want to clean and then linkify, consider using
       the :py:class:`bleach.linkifier.LinkifyFilter` as a filter in the clean
       pass. That way you're not parsing the HTML twice.

    :arg str text: the text to linkify

    :arg list callbacks: list of callbacks to run when adjusting tag attributes

    :arg bool skip_pre: whether or not to skip linkifying text in a ``pre`` tag

    :arg bool parse_email: whether or not to linkify email addresses

    :returns: linkified text as unicode

    """
    linker = Linker(
        callbacks=callbacks,
        skip_pre=skip_pre,
        parse_email=parse_email
    )
    return linker.linkify(text)
