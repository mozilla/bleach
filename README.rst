======
Bleach
======

.. image:: https://travis-ci.org/mozilla/bleach.png?branch=master
   :target: https://travis-ci.org/mozilla/bleach

.. image:: https://badge.fury.io/py/bleach.svg
   :target: http://badge.fury.io/py/bleach

Bleach is a allowed-list-based HTML sanitizing library that escapes or strips
markup and attributes.

Bleach can also linkify text safely, applying filters that Django's ``urlize``
filter cannot, and optionally setting ``rel`` attributes, even on links already
in the text.

Bleach is intended for sanitizing text from *untrusted* sources. If you find
yourself jumping through hoops to allow your site administrators to do lots of
things, you're probably outside the use cases. Either trust those users, or
don't.

Because it relies on html5lib_, Bleach is as good as modern browsers at dealing
with weird, quirky HTML fragments. And *any* of Bleach's methods will fix
unbalanced or mis-nested tags.

The version on GitHub_ is the most up-to-date and contains the latest bug
fixes. You can find full documentation on `ReadTheDocs`_.

:Code:           https://github.com/mozilla/bleach
:Documentation:  https://bleach.readthedocs.io/
:Issue tracker:  https://github.com/mozilla/bleach/issues
:IRC:            ``#bleach`` on irc.mozilla.org
:License:        Apache License v2; see LICENSE file


Reporting Bugs
==============

For regular bugs, please report them `in our issue tracker
<https://github.com/mozilla/bleach/issues>`_.

If you believe that you've found a security vulnerability, please `file a secure
bug report in our bug tracker
<https://bugzilla.mozilla.org/enter_bug.cgi?assigned_to=nobody%40mozilla.org&product=Webtools&component=Bleach-security&groups=webtools-security>`_
or send an email to *security AT mozilla DOT org*.

For more information on security-related bug disclosure and the PGP key to use
for sending encrypted mail or to verify responses received from that address,
please read our wiki page at
`<https://www.mozilla.org/en-US/security/#For_Developers>`_.


Installing Bleach
=================

Bleach is available on PyPI_, so you can install it with ``pip``::

    $ pip install bleach

Or with ``easy_install``::

    $ easy_install bleach


Upgrading Bleach
================

.. warning::

   Before doing any upgrades, read through `Bleach Changes
   <https://bleach.readthedocs.io/en/latest/changes.html>`_ for backwards
   incompatible changes, newer versions, etc.


Basic use
=========

The simplest way to use Bleach is:

.. code-block:: python

    >>> import bleach

    >>> bleach.clean('an <script>evil()</script> example')
    u'an &lt;script&gt;evil()&lt;/script&gt; example'

    >>> bleach.linkify('an http://example.com url')
    u'an <a href="http://example.com" rel="nofollow">http://example.com</a> url


Bleach vs html5lib
==================

Bleach is built upon html5lib_, and html5lib has `a built-in sanitizer <https://github.com/html5lib/html5lib-python/blob/1.0b10/html5lib/serializer.py#L148>`_, so why use Bleach?

* Bleach's API is simpler.
* Bleach's sanitizer allows a map to be provided for ``ALLOWED_ATTRIBUTES``, giving you a lot more control over sanitizing attributes: you can sanitize attributes for specific tags, you can sanitize based on value, etc.
* Bleach's sanitizer always alphabetizes attributes, but uses an alphabetizer that works with namespaces — the html5lib one is broken in that regard.
* Bleach's sanitizer always quotes attribute values because that's the safe thing to do. The html5lib one makes that configurable. In this case, Bleach doesn't make something configurable that isn't safe.
* Bleach's sanitizer has a very restricted set of ``ALLOWED_PROTOCOLS`` by default. html5lib has a much more expansive one that Bleach's authors claim is less safe.
* ``html5lib.filters.sanitizer.Filter``'s ``sanitize_css`` is broken and doesn't work.


.. _html5lib: https://github.com/html5lib/html5lib-python
.. _GitHub: https://github.com/mozilla/bleach
.. _ReadTheDocs: https://bleach.readthedocs.io/
.. _PyPI: http://pypi.python.org/pypi/bleach
