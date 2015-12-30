.. _clean-chapter:
.. highlightlang:: python

==================
``bleach.clean()``
==================

``clean()`` is Bleach's HTML sanitization method.

.. autofunction:: bleach.clean


Given a fragment of HTML, Bleach will parse it according to the HTML5 parsing
algorithm and sanitize any disallowed tags or attributes. This algorithm also
takes care of things like unclosed and (some) misnested tags.

.. note::
   You may pass in a ``string`` or a ``unicode`` object, but Bleach will
   always return ``unicode``.


Tag Whitelist
=============

The ``tags`` kwarg is a whitelist of allowed HTML tags. It should be a list,
tuple, or other iterable. Any other HTML tags will be escaped or stripped from
the text.

For example:

.. doctest::

   >>> import bleach

   >>> bleach.clean(
   ...     u'<b><i>an example</i></b>',
   ...     tags=['b'],
   ... )
   u'<b>&lt;i&gt;an example&lt;/i&gt;</b>'


The default value is a relatively conservative list found in
``bleach.ALLOWED_TAGS``.


Attribute Whitelist
===================

The ``attributes`` kwarg is a whitelist of attributes. It can be a list, in
which case the attributes are allowed for any tag, or a dictionary, in which
case the keys are tag names (or a wildcard: ``*`` for all tags) and the values
are lists of allowed attributes.

For example:

.. doctest::

   >>> import bleach

   >>> attrs = {
   ...     '*': ['class'],
   ...     'a': ['href', 'rel'],
   ...     'img': ['alt'],
   ... }

   >>> bleach.clean(
   ...    u'<img alt="an example" width=500>',
   ...    tags=['img'],
   ...    attributes=attrs
   ... )
   u'<img alt="an example">'


In this case, ``class`` is allowed on any allowed element (from the ``tags``
argument), ``<a>`` tags are allowed to have ``href`` and ``rel`` attributes,
and so on.

The default value is also a conservative dict found in
``bleach.ALLOWED_ATTRIBUTES``.


Callable Filters
----------------

You can also use a callable (instead of a list) in the ``attributes`` kwarg. If
the callable returns ``True``, the attribute is allowed. Otherwise, it is
stripped. For example:

.. doctest::

    >>> from urlparse import urlparse
    >>> import bleach

    >>> def filter_src(name, value):
    ...     if name in ('alt', 'height', 'width'):
    ...         return True
    ...     if name == 'src':
    ...         p = urlparse(value)
    ...         return (not p.netloc) or p.netloc == 'mydomain.com'
    ...     return False

    >>> bleach.clean(
    ...    u'<img src="http://example.com" alt="an example">',
    ...    tags=['img'],
    ...    attributes={
    ...        'img': filter_src
    ...    }
    ... )
    u'<img alt="an example">'


Styles Whitelist
================

If you allow the ``style`` attribute, you will also need to whitelist styles
users are allowed to set, for example ``color`` and ``background-color``.

The default value is an empty list, i.e., the ``style`` attribute will be
allowed but no values will be.

For example, to allow users to set the color and font-weight of text:

.. doctest::

   >>> import bleach

   >>> tags = ['p', 'em', 'strong']
   >>> attrs = {
   ...     '*': ['style']
   ... }
   >>> styles = ['color', 'font-weight']

   >>> bleach.clean(
   ...     u'<p style="font-weight: heavy;">my html</p>',
   ...     tags=tags,
   ...     attributes=attrs,
   ...     styles=styles
   ... )
   u'<p style="font-weight: heavy;">my html</p>'


Default styles are stored in ``bleach.ALLOWED_STYLES``.


Protocol Whitelist
==================

If you allow tags that have attributes containing a URI value (like the ``href``
attribute of an anchor tag, you may want to adapt the accepted protocols. The
default list only allows ``http``, ``https`` and ``mailto``.

For example, this sets allowed protocols to http, https and smb:

.. doctest::

   >>> import bleach

   >>> bleach.clean(
   ...     '<a href="smb://more_text">allowed protocol</a>',
   ...     protocols=['http', 'https', 'smb']
   ... )
   u'<a href="smb://more_text">allowed protocol</a>'


This adds smb to the bleach-specified set of allowed protocols:

.. doctest::

   >>> import bleach

   >>> bleach.clean(
   ...     '<a href="smb://more_text">allowed protocol</a>',
   ...     protocols=bleach.ALLOWED_PROTOCOLS + ['smb']
   ... )
   u'<a href="smb://more_text">allowed protocol</a>'


Default protocols are in ``bleach.ALLOWED_PROTOCOLS``.


Stripping Markup
================

By default, Bleach *escapes* disallowed or invalid markup. For example:

.. doctest::

   >>> import bleach

   >>> bleach.clean('<span>is not allowed</span>')
   u'&lt;span&gt;is not allowed&lt;/span&gt;'


If you would rather Bleach stripped this markup entirely, you can pass
``strip=True``:

.. doctest::

   >>> import bleach

   >>> bleach.clean('<span>is not allowed</span>', strip=True)
   u'is not allowed'


Stripping Comments
==================

By default, Bleach will strip out HTML comments. To disable this behavior, set
``strip_comments=False``:

.. doctest::

   >>> import bleach
   >>> html = 'my<!-- commented --> html'

   >>> bleach.clean(html)
   u'my html'

   >>> bleach.clean(html, strip_comments=False)
   u'my<!-- commented --> html'
