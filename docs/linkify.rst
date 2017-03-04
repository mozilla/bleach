.. _linkify-chapter:
.. highlightlang:: python

=========================
Linkifying text fragments
=========================

``linkify()`` searches text for links, URLs, and email addresses and lets you
control how and when those links are rendered.

``linkify()`` works by building a document tree, so it's guaranteed never to do
weird things to URLs in attribute values, can modify the value of attributes on
``<a>`` tags, and can even do things like skip ``<pre>`` sections.

By default, ``linkify()`` will perform some sanitization, only allowing a set of
"safe" tags. Because it uses the HTML5 parsing algorithm, it will always handle
things like unclosed tags.

.. note::

   You may pass a ``string`` or ``unicode`` object, but Bleach will always
   return ``unicode``.

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


Setting Attributes
------------------

For example, to set ``rel="nofollow"`` on all links found in the text, a simple
(and included) callback might be::

    def set_nofollow(attrs, new=False):
        attrs[(None, 'rel')] = 'nofollow'
        return attrs


This would set the value of the ``rel`` attribute, stomping on a previous value
if there was one.

You could also make external links open in a new tab or set a class::

    from urlparse import urlparse

    def set_target(attrs, new=False):
        p = urlparse(attrs[(None, 'href')])
        if p.netloc not in ['my-domain.com', 'other-domain.com']:
            attrs[(None, 'target')] = '_blank'
            attrs[(None, 'class')] = 'external'
        else:
            attrs.pop((None, 'target'), None)
        return attrs


Removing Attributes
-------------------

You can easily remove attributes you don't want to allow, even on existing
links (``<a>`` tags) in the text. (See also :ref:`clean() <clean-chapter>` for
sanitizing attributes.)

::

    def allowed_attributes(attrs, new=False):
        """Only allow href, target, rel and title."""
        allowed = [(None, 'href'), (None, 'target'),
                   (None, 'rel'), (None, 'title')]
        return dict((k, v) for k, v in attrs.items() if k in allowed)


Or you could remove a specific attribute, if it exists::

    def remove_title1(attrs, new=False):
        attrs.pop((None, 'title'), None)
        return attrs

    def remove_title2(attrs, new=False):
        if (None, 'title') in attrs:
            del attrs[(None, 'title')]
        return attrs


Altering Attributes
-------------------

You can alter and overwrite attributes, including the link text, via the
``_text`` key, to, for example, pass outgoing links through a warning page, or
limit the length of text inside an ``<a>`` tag.

::

    def shorten_url(attrs, new=False):
        """Shorten overly-long URLs in the text."""
        if not new:  # Only looking at newly-created links.
            return attrs

        # _text will be the same as the URL for new links.
        text = attrs['_text']
        if len(text) > 25:
            attrs['_text'] = text[0:22] + '...'
        return attrs

::

    from urllib2 import quote
    from urlparse import urlparse

    def outgoing_bouncer(attrs, new=False):
        """Send outgoing links through a bouncer."""
        p = urlparse((None, attrs['href']))
        if p.netloc not in ['my-domain.com', 'www.my-domain.com', '']:
            bouncer = 'http://outgoing.my-domain.com/?destination=%s'
            attrs[(None, 'href')] = bouncer % quote(attrs['href'])
        return attrs


Preventing Links
----------------

A slightly more complex example is inspired by Crate_, where strings like
``models.py`` are often found, and linkified. ``.py`` is the ccTLD for
Paraguay, so ``example.py`` may be a legitimate URL, but in the case of a site
dedicated to Python packages, odds are it is not. In this case, Crate_ could
write the following callback::

    def dont_linkify_python(attrs, new=False):
        if not new:  # This is an existing <a> tag, leave it be.
            return attrs

        # If the TLD is '.py', make sure it starts with http: or https:
        href = attrs[(None, 'href')]
        if href.endswith('.py') and not href.startswith(('http:', 'https:')):
            # This looks like a Python file, not a URL. Don't make a link.
            return None

        # Everything checks out, keep going to the next callback.
        return attrs


Removing Links
--------------

If you want to remove certain links, even if they are written in the text with
``<a>`` tags, you can still return ``None``::

    def remove_mailto(attrs, new=False):
        """Remove any mailto: links."""
        if attrs[(None, 'href')].startswith('mailto:'):
            return None
        return attrs


Skipping links in pre blocks (``skip_pre``)
===========================================

``<pre>`` tags are often special, literal sections. If you don't want to create
any new links within a ``<pre>`` section, pass ``skip_pre=True``.

.. note::
   Though new links will not be created, existing links created with ``<a>``
   tags will still be passed through all the callbacks.


Linkifying email addresses (``parse_email``)
============================================

By default, ``linkify()`` does not create ``mailto:`` links for email
addresses, but if you pass ``parse_email=True``, it will. ``mailto:`` links
will go through exactly the same set of callbacks as all other links, whether
they are newly created or already in the text, so be careful when writing
callbacks that may need to behave differently if the protocol is ``mailto:``.


Using ``bleach.linkifier.LinkifyFilter``
========================================

``bleach.linkify`` works by paring an HTML fragment and then running it through
the ``bleach.linkifier.LinkifyFilter`` when walking the tree and serializing it
back into text.

You can use this filter wherever you can use an html5lib Filter. For example, you
could use it with ``bleach.Cleaner`` to clean and linkify in one step.

For example, using all the defaults:

.. doctest::

   >>> from functools import partial

   >>> from bleach import Cleaner
   >>> from bleach.linkifier import LinkifyFilter

   >>> cleaner = Cleaner(tags=['pre'])
   >>> cleaner.clean('<pre>http://example.com</pre>')
   u'<pre>http://example.com</pre>'

   >>> cleaner = Cleaner(tags=['pre'], filters=[LinkifyFilter])
   >>> cleaner.clean('<pre>http://example.com</pre>')
   u'<pre><a href="http://example.com">http://example.com</a></pre>'


And passing parameters to ``LinkifyFilter``:

.. doctest::

   >>> from functools import partial

   >>> from bleach import Cleaner
   >>> from bleach.linkifier import LinkifyFilter

   >>> cleaner = Cleaner(
   ...     tags=['pre'],
   ...     filters=[partial(LinkifyFilter, skip_pre=True)]
   ... )
   ...
   >>> cleaner.clean('<pre>http://example.com</pre>')
   u'<pre>http://example.com</pre>'


.. _Crate: https://crate.io/
