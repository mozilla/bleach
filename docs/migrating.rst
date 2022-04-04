.. highlight:: python

=====================================
Migrating from the html5lib sanitizer
=====================================

The `html5lib <https://github.com/html5lib/html5lib-python>`_ module `deprecated
<https://github.com/html5lib/html5lib-python/blob/master/CHANGES.rst#11>`_ its
own sanitizer in version 1.1. The maintainers "recommend users migrate to
Bleach." This tracks the issues encountered in the migration.

Migration path
==============

If you upgrade to html5lib 1.1+, you may get deprecation warnings when using its
sanitizer. If you follow the recommendation and switch to Bleach for
sanitization, you'll need to spend time tuning the Bleach sanitizer to your
needs because the Bleach sanitizer has different goals and is not a drop-in
replacement for the html5lib one.

Here is an example of replacing the sanitization method:

.. code::

   fragment = "<a href='https://github.com'>good</a> <script>bad();</script>"

   import html5lib
   parser = html5lib.html5parser.HTMLParser()
   parsed_fragment = parser.parseFragment(fragment)
   print(html5lib.serialize(parsed_fragment, sanitize=True))
   
   # '<a href="https://github.com">good</a> &lt;script&gt;bad();&lt;/script&gt;'

   import bleach
   print(bleach.clean(fragment))

   # '<a href="https://github.com">good</a> &lt;script&gt;bad();&lt;/script&gt;'


Escaping differences
====================

While html5lib will leave 'single' and "double" quotes alone, Bleach will escape
them as the corresponding HTML entities (``'`` becomes ``&#39;`` and ``"``
becomes ``&#34;``). This should be fine in most rendering contexts.

Different allow lists
=====================

By default, html5lib and Bleach "allow" (i.e. don't sanitize) different sets of
HTML elements, HTML attributes, and CSS properties. For example, html5lib will
leave ``<u/>`` alone, while Bleach will sanitize it:

.. code::

   fragment = "<u>hi</u>"

   import html5lib
   parser = html5lib.html5parser.HTMLParser()
   parsed_fragment = parser.parseFragment(fragment)
   print(html5lib.serialize(parsed_fragment, sanitize=True))

   # '<u>hi</u>'

   print(bleach.clean(fragment))
   
   # '&lt;u&gt;hi&lt;/u&gt;'

If you wish to retain the sanitization behaviour with respect to specific HTML
elements, use the ``tags`` argument (see the :ref:`chapter on clean()
<clean-chapter>` for more info):

.. code::

   fragment = "<u>hi</u>"

   print(bleach.clean(fragment, tags=['u']))

   # '<u>hi</u>'

If you want to stick to the html5lib sanitizer's allow lists, get them from the
`sanitizer code
<https://github.com/html5lib/html5lib-python/blob/master/html5lib/filters/sanitizer.py>`_.
It's probably best to copy them as static lists (as opposed to importing the
module and reading them dynamically) because

* the lists are not part of the html5lib API
* the sanitizer module is already deprecated and might disappear
* importing the sanitizer module gives the deprecation warning (unless you take
  the effort to filter it)


.. code::

   import bleach

   from bleach.css_sanitizer import CSSSanitizer

   ALLOWED_ELEMENTS = ["b", "p", "div"]
   ALLOWED_ATTRIBUTES = ["style"]
   ALLOWED_CSS_PROPERTIES = ["color"]

   fragment = "some unsafe html"

   css_sanitizer = CSSSanitizer(allowed_css_properties=ALLOWED_CSS_PROPERTIES)
   safe_html = bleach.clean(
       fragment,
       tags=ALLOWED_ELEMENTS,
       attributes=ALLOWED_ATTRIBUTES,
       css_sanitizer=css_sanitizer,
   )
