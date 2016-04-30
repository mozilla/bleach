======
Bleach
======

.. image:: https://travis-ci.org/mozilla/bleach.png?branch=master
   :target: https://travis-ci.org/mozilla/bleach

.. image:: https://badge.fury.io/py/Bleach.svg
   :target: http://badge.fury.io/py/Bleach

Bleach is a whitelist-based HTML sanitizing library that escapes or strips
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

Or by cloning the repo from GitHub_::

    $ git clone git://github.com/mozilla/bleach.git

Then install it by running::

    $ python setup.py install


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


.. _html5lib: https://github.com/html5lib/html5lib-python
.. _GitHub: https://github.com/mozilla/bleach
.. _ReadTheDocs: https://bleach.readthedocs.io/
.. _PyPI: http://pypi.python.org/pypi/bleach


