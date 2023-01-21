.. _linkify-chapter:
.. highlight:: python

=========================
Linkifying text fragments
=========================

Bleach comes with several tools for searching text for links, URLs, and email
addresses and letting you specify how those links are rendered in HTML.

For example, you could pass in text and have all URL things converted into
HTML links.

It works by parsing the text as HTML and building a document tree. In this
way, you're guaranteed to get valid HTML back without weird things like
having URLs in tag attributes getting linkified.

.. note::

   If you plan to sanitize/clean the text and linkify it, you should do that
   in a single pass using :ref:`LinkifyFilter <linkify-LinkifyFilter>`. This
   is faster and it'll use the list of allowed tags from clean.

.. note::

   You may pass a ``string`` or ``unicode`` object, but Bleach will always
   return ``unicode``.

.. note::

   By default `linkify` **does not** attempt to protect users from bad
   or deceptive links including:

   * links to malicious or deceptive domains
   * shortened or tracking links
   * deceptive links using internationalized domain names (IDN) that
     resemble legitimate domains for `IDN homograph attacks
     <https://en.wikipedia.org/wiki/IDN_homograph_attack>`_ (font
     styling, background color, and other context is unavailable)

   We recommend using additional callbacks or other controls to check
   these properties.

.. autofunction:: bleach.linkify

Callbacks for adjusting attributes (``callbacks``)
==================================================

The second argument to ``linkify()`` is a list or other iterable of callback
functions. These callbacks can modify links that exist and links that are being
created, or remove them completely.

Each callback will get the following arguments::

    def my_callback(attrs, new=False):

The ``attrs`` argument is a dict of attributes of the ``<a>`` tag. Keys of the
``attrs`` dict are namespaced attr names. For example ``(None, 'href')``. The
``attrs`` dict also contains a ``_text`` key, which is the innerText of the
``<a>`` tag.

The ``new`` argument is a boolean indicating if the link is new (e.g. an email
address or URL found in the text) or already existed (e.g. an ``<a>`` tag found
in the text).

The callback must return a dict of attributes (including ``_text``) or ``None``.
The new dict of attributes will be passed to the next callback in the list.

If any callback returns ``None``, new links will not be created and existing
links will be removed leaving the innerText left in its place.

The default callback adds ``rel="nofollow"``. See ``bleach.callbacks`` for some
included callback functions.

This defaults to ``bleach.linkifier.DEFAULT_CALLBACKS``.


.. autodata:: bleach.linkifier.DEFAULT_CALLBACKS


.. versionchanged:: 2.0

   In previous versions of Bleach, the attribute names were not namespaced.


Setting Attributes
------------------

For example, you could add a ``title`` attribute to all links:

.. doctest::

   >>> from bleach.linkifier import Linker

   >>> def set_title(attrs, new=False):
   ...     attrs[(None, 'title')] = 'link in user text'
   ...     return attrs
   ...
   >>> linker = Linker(callbacks=[set_title])
   >>> linker.linkify('abc http://example.com def')
   'abc <a href="http://example.com" title="link in user text">http://example.com</a> def'


This would set the value of the ``title`` attribute, stomping on a previous value
if there was one.

Here's another example that makes external links open in a new tab and look like
an external link:

.. doctest::

   >>> from urllib.parse import urlparse
   >>> from bleach.linkifier import Linker

   >>> def set_target(attrs, new=False):
   ...     p = urlparse(attrs[(None, 'href')])
   ...     if p.netloc not in ['my-domain.com', 'other-domain.com']:
   ...         attrs[(None, 'target')] = '_blank'
   ...         attrs[(None, 'class')] = 'external'
   ...     else:
   ...         attrs.pop((None, 'target'), None)
   ...     return attrs
   ...
   >>> linker = Linker(callbacks=[set_target])
   >>> linker.linkify('abc http://example.com def')
   'abc <a href="http://example.com" target="_blank" class="external">http://example.com</a> def'


Removing Attributes
-------------------

You can easily remove attributes you don't want to allow, even on existing
links (``<a>`` tags) in the text. (See also :ref:`clean() <clean-chapter>` for
sanitizing attributes.)

.. doctest::

   >>> from bleach.linkifier import Linker

   >>> def allowed_attrs(attrs, new=False):
   ...     """Only allow href, target, rel and title."""
   ...     allowed = [
   ...         (None, 'href'),
   ...         (None, 'target'),
   ...         (None, 'rel'),
   ...         (None, 'title'),
   ...         '_text',
   ...     ]
   ...     return dict((k, v) for k, v in attrs.items() if k in allowed)
   ...
   >>> linker = Linker(callbacks=[allowed_attrs])
   >>> linker.linkify('<a style="font-weight: super bold;" href="http://example.com">link</a>')
   '<a href="http://example.com">link</a>'


Or you could remove a specific attribute, if it exists:

.. doctest::

   >>> from bleach.linkifier import Linker

   >>> def remove_title(attrs, new=False):
   ...     attrs.pop((None, 'title'), None)
   ...     return attrs
   ...
   >>> linker = Linker(callbacks=[remove_title])
   >>> linker.linkify('<a href="http://example.com">link</a>')
   '<a href="http://example.com">link</a>'

   >>> linker.linkify('<a title="bad title" href="http://example.com">link</a>')
   '<a href="http://example.com">link</a>'


Altering Attributes
-------------------

You can alter and overwrite attributes, including the link text, via the
``_text`` key, to, for example, pass outgoing links through a warning page, or
limit the length of text inside an ``<a>`` tag.

Example of shortening link text:

.. doctest::

   >>> from bleach.linkifier import Linker

   >>> def shorten_url(attrs, new=False):
   ...     """Shorten overly-long URLs in the text."""
   ...     # Only adjust newly-created links
   ...     if not new:
   ...         return attrs
   ...     # _text will be the same as the URL for new links
   ...     text = attrs['_text']
   ...     if len(text) > 25:
   ...         attrs['_text'] = text[0:22] + '...'
   ...     return attrs
   ...
   >>> linker = Linker(callbacks=[shorten_url])
   >>> linker.linkify('http://example.com/longlonglonglonglongurl')
   '<a href="http://example.com/longlonglonglonglongurl">http://example.com/lon...</a>'


Example of switching all links to go through a bouncer first:

.. doctest::

   >>> from urllib.parse import quote, urlparse
   >>> from bleach.linkifier import Linker

   >>> def outgoing_bouncer(attrs, new=False):
   ...     """Send outgoing links through a bouncer."""
   ...     href_key = (None, 'href')
   ...     p = urlparse(attrs.get(href_key, None))
   ...     if p.netloc not in ['example.com', 'www.example.com', '']:
   ...         bouncer = 'http://bn.ce/?destination=%s'
   ...         attrs[href_key] = bouncer % quote(attrs[href_key])
   ...     return attrs
   ...
   >>> linker = Linker(callbacks=[outgoing_bouncer])
   >>> linker.linkify('http://example.com')
   '<a href="http://example.com">http://example.com</a>'

   >>> linker.linkify('http://foo.com')
   '<a href="http://bn.ce/?destination=http%3A//foo.com">http://foo.com</a>'


Preventing Links
----------------

A slightly more complex example is inspired by Crate_, where strings like
``models.py`` are often found, and linkified. ``.py`` is the ccTLD for
Paraguay, so ``example.py`` may be a legitimate URL, but in the case of a site
dedicated to Python packages, odds are it is not. In this case, Crate_ could
write the following callback:

.. doctest::

   >>> from bleach.linkifier import Linker

   >>> def dont_linkify_python(attrs, new=False):
   ...     # This is an existing link, so leave it be
   ...     if not new:
   ...         return attrs
   ...     # If the TLD is '.py', make sure it starts with http: or https:.
   ...     # Use _text because that's the original text
   ...     link_text = attrs['_text']
   ...     if link_text.endswith('.py') and not link_text.startswith(('http:', 'https:')):
   ...         # This looks like a Python file, not a URL. Don't make a link.
   ...         return None
   ...     # Everything checks out, keep going to the next callback.
   ...     return attrs
   ...
   >>> linker = Linker(callbacks=[dont_linkify_python])
   >>> linker.linkify('abc http://example.com def')
   'abc <a href="http://example.com">http://example.com</a> def'

   >>> linker.linkify('abc models.py def')
   'abc models.py def'


.. _Crate: https://crate.io/


Removing Links
--------------

If you want to remove certain links, even if they are written in the text with
``<a>`` tags, have the callback return ``None``.

For example, this removes any ``mailto:`` links:

.. doctest::

   >>> from bleach.linkifier import Linker

   >>> def remove_mailto(attrs, new=False):
   ...     if attrs[(None, 'href')].startswith('mailto:'):
   ...         return None
   ...     return attrs
   ...
   >>> linker = Linker(callbacks=[remove_mailto])
   >>> linker.linkify('<a href="mailto:janet@example.com">mail janet!</a>')
   'mail janet!'


Skipping links in specified tag blocks (``skip_tags``)
======================================================

``<pre>`` tags are often special, literal sections. If you don't want to create
any new links within a ``<pre>`` section, pass ``skip_tags=['pre']``.

This works for ``code``, ``div`` and any other blocks you want to skip over.


.. versionchanged:: 2.0

   This used to be ``skip_pre``, but this makes it more general.


Linkifying email addresses (``parse_email``)
============================================

By default, :py:func:`bleach.linkify` does not create ``mailto:`` links for
email addresses, but if you pass ``parse_email=True``, it will. ``mailto:``
links will go through exactly the same set of callbacks as all other links,
whether they are newly created or already in the text, so be careful when
writing callbacks that may need to behave differently if the protocol is
``mailto:``.


Using ``bleach.linkifier.Linker``
=================================

If you're linking a lot of text and passing the same argument values or you
need more configurability, consider using a :py:class:`bleach.linkifier.Linker`
instance.

.. doctest::

   >>> from bleach.linkifier import Linker

   >>> linker = Linker(skip_tags={'pre'})
   >>> linker.linkify('a b c http://example.com d e f')
   'a b c <a href="http://example.com" rel="nofollow">http://example.com</a> d e f'


It includes optional keyword arguments to specify allowed top-level
domains (TLDs) and URL protocols/schemes:

.. doctest::

   >>> from bleach.linkifier import Linker, build_url_re

   >>> only_fish_tld_url_re = build_url_re(tlds=['fish'])
   >>> linker = Linker(url_re=only_fish_tld_url_re)

   >>> linker.linkify('com TLD does not link https://example.com')
   'com TLD does not link https://example.com'
   >>> linker.linkify('fish TLD links https://example.fish')
   'fish TLD links <a href="https://example.fish" rel="nofollow">https://example.fish</a>'


   >>> only_https_url_re = build_url_re(protocols=['https'])
   >>> linker = Linker(url_re=only_https_url_re)

   >>> linker.linkify('gopher does not link gopher://example.link')
   'gopher does not link gopher://example.link'
   >>> linker.linkify('https links https://example.com/')
   'https links <a href="https://example.com/" rel="nofollow">https://example.com/</a>'


Specify localized TLDs with and without punycode encoding to handle
both formats:

.. doctest::

   >>> from bleach.linkifier import Linker, build_url_re

   >>> linker = Linker(url_re=build_url_re(tlds=['рф']))
   >>> linker.linkify('https://xn--80aaksdi3bpu.xn--p1ai/ https://дайтрафик.рф/')
   'https://xn--80aaksdi3bpu.xn--p1ai/ <a href="https://дайтрафик.рф/" rel="nofollow">https://дайтрафик.рф/</a>'

   >>> puny_linker = Linker(url_re=build_url_re(tlds=['рф', 'xn--p1ai']))
   >>> puny_linker.linkify('https://xn--80aaksdi3bpu.xn--p1ai/ https://дайтрафик.рф/')
   '<a href="https://xn--80aaksdi3bpu.xn--p1ai/" rel="nofollow">https://xn--80aaksdi3bpu.xn--p1ai/</a> <a href="https://дайтрафик.рф/" rel="nofollow">https://дайтрафик.рф/</a>'


Similarly, using ``build_email_re`` with the ``email_re`` argument to
customize recognized email TLDs:

.. doctest::

   >>> from bleach.linkifier import Linker, build_email_re

   >>> only_fish_tld_url_re = build_email_re(tlds=['fish'])
   >>> linker = Linker(email_re=only_fish_tld_url_re, parse_email=True)

   >>> linker.linkify('does not link email: foo@example.com')
   'does not link email: foo@example.com'
   >>> linker.linkify('links email foo@example.fish')
   'links email <a href="mailto:foo@example.fish">foo@example.fish</a>'


:ref:`LinkifyFilter <linkify-LinkifyFilter>` also accepts these options.

.. autoclass:: bleach.linkifier.Linker
   :members:


.. versionadded:: 2.0

.. _linkify-LinkifyFilter:

Using ``bleach.linkifier.LinkifyFilter``
========================================

``bleach.linkify`` works by parsing an HTML fragment and then running it through
the ``bleach.linkifier.LinkifyFilter`` when walking the tree and serializing it
back into text.

You can use this filter wherever you can use an html5lib Filter. This lets you
use it with ``bleach.Cleaner`` to clean and linkify in one step.

For example, using all the defaults:

.. doctest::

   >>> from functools import partial

   >>> from bleach import Cleaner
   >>> from bleach.linkifier import LinkifyFilter

   >>> cleaner = Cleaner(tags={'pre'})
   >>> cleaner.clean('<pre>http://example.com</pre>')
   '<pre>http://example.com</pre>'

   >>> cleaner = Cleaner(tags={'pre'}, filters=[LinkifyFilter])
   >>> cleaner.clean('<pre>http://example.com</pre>')
   '<pre><a href="http://example.com" rel="nofollow">http://example.com</a></pre>'


And passing parameters to ``LinkifyFilter``:

.. doctest::

   >>> from functools import partial

   >>> from bleach.sanitizer import Cleaner
   >>> from bleach.linkifier import LinkifyFilter

   >>> cleaner = Cleaner(
   ...     tags={'pre'},
   ...     filters=[partial(LinkifyFilter, skip_tags={'pre'})]
   ... )
   ...
   >>> cleaner.clean('<pre>http://example.com</pre>')
   '<pre>http://example.com</pre>'


.. autoclass:: bleach.linkifier.LinkifyFilter


.. versionadded:: 2.0
