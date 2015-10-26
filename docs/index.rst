Welcome to Bleach's documentation!
==================================

Bleach is a whitelist-based HTML sanitization and text linkification library.
It is designed to take untrusted user input with *some* HTML.

Because Bleach uses html5lib_ to parse document fragments the same way browsers
do, it is extremely resilient to unknown attacks, much more so than
regular-expression-based sanitizers.

Bleach's ``linkify`` function is highly configurable and can be used to find,
edit, and filter links most other auto-linkers can't.

The version of bleach on GitHub_ is always the most up-to-date and the
``master`` branch should always work.

:Code:           https://github.com/mozilla/bleach
:Documentation:  https://bleach.readthedocs.org/
:Issue tracker:  https://github.com/mozilla/bleach/issues
:IRC:            ``#bleach`` on irc.mozilla.org
:License:        Apache License v2; see LICENSE file


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


Contents:
=========

.. toctree::
   :maxdepth: 2

   clean
   linkify
   goals


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. _html5lib: https://github.com/html5lib/html5lib-python
.. _GitHub: https://github.com/mozilla/bleach
.. _PyPI: https://pypi.python.org/pypi/bleach
