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
