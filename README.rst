Bleach
======

Bleach is an HTML sanitizing library designed to strip disallowed tags and
attributes based on a whitelist, and can additionally autolinkify URLs in text
with an extra filter layer that Django's ``urlize`` filter doesn't have.


Basic Use
---------

The simplest way to use Bleach::

    >>> from bleach import Bleach

    >>> bl = Bleach()

    >>> bl.clean('an <script>evil()</script> example')
    'an &lt;script&gt;evil()&lt;/script&gt; example'

    # to linkify URLs and email addresses, use
    >>> bl.linkify('a http://example.com url')
    'a <a href="http://example.com" rel="nofollow">http://example.com</a> url'

``clean()`` also fixes up some common errors::

    >>> from bleach import Bleach

    >>> bl = Bleach()

    >>> bl.clean('unbalanced <em>tag')
    'unbalanced <em>tag</em>'


Advanced Use
------------

Bleach is relatively configurable.


Clean - Advanced
^^^^^^^^^^^^^^^^

``clean()`` takes up to two optional arguments, ``tags`` and ``attributes``,
which are instructions on what tags and attributes to allow, respectively.

``tags`` is a list of whitelisted tags::

    >>> from bleach import Bleach

    >>> bl = Bleach()

    >>> TAGS = ['b', 'em', 'i', 'strong']

    >>> bl.clean('<abbr>not allowed</abbr>', tags=TAGS)
    '&lt;abbr&gt;not allowed&lt;/abbr&gt;'

``attributes`` is either a list or, more powerfully, a dict of allowed
attributes. If a list is used, it is applied to all allowed tags, but if a
dict is use, the keys are tag names, and the values are lists of attributes
allowed for that tag.

For example::

    >>> from bleach import Bleach

    >>> bl = Bleach()

    >>> ATTRS = {'a': ['href']}

    >>> bl.clean('<a href="/" title="fail">link</a>', attributes=ATTRS)
    '<a href="/">link</a>'


Linkify - Advanced
^^^^^^^^^^^^^^^^^^

If you pass ``nofollow=False`` to ``linkify()``, links will not be created with
``rel="nofollow"``. By default, ``nofollow`` is ``True``. If ``nofollow`` is
``True``, then links found in the text will have their ``rel`` attributes set
to ``nofollow`` as well, otherwise the attribute will not be modified.

Configuring ``linkify()`` is somewhat more complicated. ``linkify()`` passes data
through different **filters** before returning the string. By default, these
filters do nothing, but if you subclass ``Bleach``, you can override them.

All the filters take and return a single string.


filter_url
**********

``filter_url(self, url)`` is applied to URLs before they are put into the ``href``
attribute of the link. If you need these links to go through a redirect or
outbound script, ``filter_url()`` is the function to override.

For example::

    import urllib

    from bleach import Bleach

    class MyBleach(Bleach):
        def filter_url(self, url):
            return 'http://example.com/bounce?u=%s' % urllib.quote(url)

Now, use ``MyBleach`` instead of ``Bleach`` and ``linkify()`` will route urls
through your bouncer.


filter_text
******************

This filter is applied to the link text of linkified URLs.
