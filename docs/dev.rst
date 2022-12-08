==================
Bleach development
==================

Install for development
=======================

To install Bleach to make changes to it:

1. Clone the repo from GitHub::

       $ git clone git://github.com/mozilla/bleach.git

2. Create and activate a virtual environment.

3. Install Bleach and developer requirements into the virtual environment::

       $ pip install -r requirements-dev.txt


Code of conduct
===============

This project has a `code of conduct
<https://github.com/mozilla/bleach/blob/main/CODE_OF_CONDUCT.md>`_.


.. include:: ../CONTRIBUTING.rst


Docs
====

Docs are in ``docs/``. We use Sphinx. Docs are pushed to ReadTheDocs
via a GitHub webhook.


Testing
=======

Run::

    $ tox

That'll run Bleach tests in all the supported Python environments. Note that
you need the necessary Python binaries for them all to be tested.

Tests are run as GitHub actions for test and pull request events.


Release process
===============

1. Checkout main tip.

2. Check to make sure ``setup.py`` is correct and match requirements-wise.

3. Update version numbers in ``bleach/__init__.py``.

   1. Set ``__version__`` to something like ``2.0.0``. Use
      semver. Bump the minor version if a vendored library was
      unvendored or updated.
   2. Set ``__releasedate__`` to something like ``20120731``.

4. Update ``CONTRIBUTORS``, ``CHANGES``, ``MANIFEST.in`` and
   ``SECURITY.md`` as necessary.

5. Verify correctness.

   1. Run linting, tests, and everything else with tox::

         $ tox

   2. Build the docs::

         $ cd docs
         $ make html

   3. Run the doctests::

         $ cd docs/
         $ make doctest

   4. Verify the local vendored files (the second invocation should **not**
      exit with ``/tmp/vendor-test exists. Please remove.`` and the exit
      code should be zero)::

         $ make vendorverify

   5. Run any additional tests to verify everything else works

6. Commit the changes.

7. Push the changes to GitHub. This will cause Github Actions to run the tests.

8. After CI passes, create a signed tag for the release::

      $ git tag -s v0.4.0

   Copy the details from ``CHANGES`` into the tag comment.

9. Generate distribution files::

      $ python -m build

10. Sanity check the release contents and sizes::

       $ ls -lh dist/* # file sizes should be similar
       $ tar tvzf dist/bleach-${VERSION}.tar.gz
       $ unzip -v dist/bleach-${VERSION}-py2.py3-none-any.whl

11. Using a PyPI API token, upload dist files to PyPI::

       $ twine upload -r [REPO] dist/*

12. Push the new tag::

       $ git push --tags [REMOTE] main

    That will push the release to PyPI.

13. Blog posts, twitter, etc.
