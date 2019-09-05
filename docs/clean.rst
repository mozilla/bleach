.. _clean-chapter:
.. highlightlang:: python

=========================
Sanitizing text fragments
=========================

:py:func:`bleach.clean` is Bleach's HTML sanitization method.

Given a fragment of HTML, Bleach will parse it according to the HTML5 parsing
algorithm and sanitize any disallowed tags or attributes. This algorithm also
takes care of things like unclosed and (some) misnested tags.

You may pass in a ``string`` or a ``unicode`` object, but Bleach will always
return ``unicode``.

.. Note::

   :py:func:`bleach.clean` is for sanitizing HTML **fragments** and not entire
   HTML documents.


.. Warning::

   :py:func:`bleach.clean` is for sanitising HTML fragments to use in an HTML
   context--not for HTML attributes, CSS, JSON, xhtml, SVG, or other contexts.

   For example, this is a safe use of ``clean`` output in an HTML context::

     <p>
       {{ bleach.clean(user_bio) }}
     </p>


   This is a **not safe** use of ``clean`` output in an HTML attribute::

     <body data-bio="{{ bleach.clean(user_bio) }}">


   If you need to use the output of ``bleach.clean()`` in an HTML attribute, you
   need to pass it through your template library's escape function. For example,
   Jinja2's ``escape`` or ``django.utils.html.escape`` or something like that.

   If you need to use the output of ``bleach.clean()`` in any other context,
   you need to pass it through an appropriate sanitizer/escaper for that
   context.


.. autofunction:: bleach.clean


Allowed tags (``tags``)
=======================

The ``tags`` kwarg specifies the allowed set of HTML tags. It should be a list,
tuple, or other iterable. Any HTML tags not in this list will be escaped or
stripped from the text.

For example:

.. doctest::

   >>> import bleach

   >>> bleach.clean(
   ...     '<b><i>an example</i></b>',
   ...     tags=['b'],
   ... )
   '<b>&lt;i&gt;an example&lt;/i&gt;</b>'


The default value is a relatively conservative list found in
``bleach.sanitizer.ALLOWED_TAGS``.


.. autodata:: bleach.sanitizer.ALLOWED_TAGS


Allowed Attributes (``attributes``)
===================================

The ``attributes`` kwarg lets you specify which attributes are allowed. The
value can be a list, a callable or a map of tag name to list or callable.

The default value is also a conservative dict found in
``bleach.sanitizer.ALLOWED_ATTRIBUTES``.


.. autodata:: bleach.sanitizer.ALLOWED_ATTRIBUTES

.. versionchanged:: 2.0

   Prior to 2.0, the ``attributes`` kwarg value could only be a list or a map.


As a list
---------

The ``attributes`` value can be a list which specifies the list of attributes
allowed for any tag.

For example:

.. doctest::

   >>> import bleach

   >>> bleach.clean(
   ...     '<p class="foo" style="color: red; font-weight: bold;">blah blah blah</p>',
   ...     tags=['p'],
   ...     attributes=['style'],
   ...     styles=['color'],
   ... )
   '<p style="color: red;">blah blah blah</p>'


As a dict
---------

The ``attributes`` value can be a dict which maps tags to what attributes they can have.

You can also specify ``*``, which will match any tag.

For example, this allows "href" and "rel" for "a" tags, "alt" for the "img" tag
and "class" for any tag (including "a" and "img"):

.. doctest::

   >>> import bleach

   >>> attrs = {
   ...     '*': ['class'],
   ...     'a': ['href', 'rel'],
   ...     'img': ['alt'],
   ... }

   >>> bleach.clean(
   ...    '<img alt="an example" width=500>',
   ...    tags=['img'],
   ...    attributes=attrs
   ... )
   '<img alt="an example">'


Using functions
---------------

You can also use callables that take the tag, attribute name and attribute value
and returns ``True`` to keep the attribute or ``False`` to drop it.

You can pass a callable as the attributes argument value and it'll run for
every tag/attr.

For example:

.. doctest::

   >>> import bleach

   >>> def allow_h(tag, name, value):
   ...     return name[0] == 'h'

   >>> bleach.clean(
   ...    '<a href="http://example.com" title="link">link</a>',
   ...    tags=['a'],
   ...    attributes=allow_h,
   ... )
   '<a href="http://example.com">link</a>'


You can also pass a callable as a value in an attributes dict and it'll run for
attributes for specified tags:

.. doctest::

   >>> from six.moves.urllib.parse import urlparse
   >>> import bleach

   >>> def allow_src(tag, name, value):
   ...     if name in ('alt', 'height', 'width'):
   ...         return True
   ...     if name == 'src':
   ...         p = urlparse(value)
   ...         return (not p.netloc) or p.netloc == 'mydomain.com'
   ...     return False

   >>> bleach.clean(
   ...    '<img src="http://example.com" alt="an example">',
   ...    tags=['img'],
   ...    attributes={
   ...        'img': allow_src
   ...    }
   ... )
   '<img alt="an example">'


.. versionchanged:: 2.0

   In previous versions of Bleach, the callable took an attribute name and a
   attribute value. Now it takes a tag, an attribute name and an attribute
   value.


Allowed styles (``styles``)
===========================

If you allow the ``style`` attribute, you will also need to specify the allowed
styles users are allowed to set, for example ``color`` and ``background-color``.

The default value is an empty list. In other words, the ``style`` attribute will
be allowed but no style declaration names will be allowed.

For example, to allow users to set the color and font-weight of text:

.. doctest::

   >>> import bleach

   >>> tags = ['p', 'em', 'strong']
   >>> attrs = {
   ...     '*': ['style']
   ... }
   >>> styles = ['color', 'font-weight']

   >>> bleach.clean(
   ...     '<p style="font-weight: heavy;">my html</p>',
   ...     tags=tags,
   ...     attributes=attrs,
   ...     styles=styles
   ... )
   '<p style="font-weight: heavy;">my html</p>'


Default styles are stored in ``bleach.sanitizer.ALLOWED_STYLES``.

.. autodata:: bleach.sanitizer.ALLOWED_STYLES


Allowed protocols (``protocols``)
=================================

If you allow tags that have attributes containing a URI value (like the ``href``
attribute of an anchor tag, you may want to adapt the accepted protocols.

For example, this sets allowed protocols to http, https and smb:

.. doctest::

   >>> import bleach

   >>> bleach.clean(
   ...     '<a href="smb://more_text">allowed protocol</a>',
   ...     protocols=['http', 'https', 'smb']
   ... )
   '<a href="smb://more_text">allowed protocol</a>'


This adds smb to the Bleach-specified set of allowed protocols:

.. doctest::

   >>> import bleach

   >>> bleach.clean(
   ...     '<a href="smb://more_text">allowed protocol</a>',
   ...     protocols=bleach.ALLOWED_PROTOCOLS + ['smb']
   ... )
   '<a href="smb://more_text">allowed protocol</a>'


Default protocols are in ``bleach.sanitizer.ALLOWED_PROTOCOLS``.

.. autodata:: bleach.sanitizer.ALLOWED_PROTOCOLS


Stripping markup (``strip``)
============================

By default, Bleach *escapes* tags that aren't specified in the allowed tags list
and invalid markup. For example:

.. doctest::

   >>> import bleach

   >>> bleach.clean('<span>is not allowed</span>')
   '&lt;span&gt;is not allowed&lt;/span&gt;'

   >>> bleach.clean('<b><span>is not allowed</span></b>', tags=['b'])
   '<b>&lt;span&gt;is not allowed&lt;/span&gt;</b>'


If you would rather Bleach stripped this markup entirely, you can pass
``strip=True``:

.. doctest::

   >>> import bleach

   >>> bleach.clean('<span>is not allowed</span>', strip=True)
   'is not allowed'

   >>> bleach.clean('<b><span>is not allowed</span></b>', tags=['b'], strip=True)
   '<b>is not allowed</b>'


Stripping comments (``strip_comments``)
=======================================

By default, Bleach will strip out HTML comments. To disable this behavior, set
``strip_comments=False``:

.. doctest::

   >>> import bleach

   >>> html = 'my<!-- commented --> html'

   >>> bleach.clean(html)
   'my html'

   >>> bleach.clean(html, strip_comments=False)
   'my<!-- commented --> html'


Using ``bleach.sanitizer.Cleaner``
==================================

If you're cleaning a lot of text or you need better control of things, you
should create a :py:class:`bleach.sanitizer.Cleaner` instance.

.. autoclass:: bleach.sanitizer.Cleaner
   :members:

.. versionadded:: 2.0


html5lib Filters (``filters``)
------------------------------

Bleach sanitizing is implemented as an html5lib filter. The consequence of this
is that we can pass the streamed content through additional specified filters
after the :py:class:`bleach.sanitizer.BleachSanitizingFilter` filter has run.

This lets you add data, drop data and change data as it is being serialized back
to a unicode.

Documentation on html5lib Filters is here:
http://html5lib.readthedocs.io/en/latest/movingparts.html#filters

Trivial Filter example:

.. doctest::

   >>> from bleach.sanitizer import Cleaner
   >>> from bleach.html5lib_shim import Filter

   >>> class MooFilter(Filter):
   ...     def __iter__(self):
   ...         for token in Filter.__iter__(self):
   ...             if token['type'] in ['StartTag', 'EmptyTag'] and token['data']:
   ...                 for attr, value in token['data'].items():
   ...                     token['data'][attr] = 'moo'
   ...             yield token
   ...
   >>> ATTRS = {
   ...     'img': ['rel', 'src']
   ... }
   ...
   >>> TAGS = ['img']
   >>> cleaner = Cleaner(tags=TAGS, attributes=ATTRS, filters=[MooFilter])
   >>> dirty = 'this is cute! <img src="http://example.com/puppy.jpg" rel="nofollow">'
   >>> cleaner.clean(dirty)
   'this is cute! <img rel="moo" src="moo">'


.. Warning::

   Filters change the output of cleaning. Make sure that whatever changes the
   filter is applying maintain the safety guarantees of the output.

.. versionadded:: 2.0


Using ``bleach.sanitizer.BleachSanitizerFilter``
================================================

``bleach.clean`` creates a ``bleach.sanitizer.Cleaner`` which creates a
``bleach.sanitizer.BleachSanitizerFilter`` which does the sanitizing work.

``BleachSanitizerFilter`` is an html5lib filter and can be used anywhere you can
use an html5lib filter.

.. autoclass:: bleach.sanitizer.BleachSanitizerFilter


.. versionadded:: 2.0
