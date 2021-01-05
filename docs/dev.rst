==================
Bleach development
==================

Install for development
=======================

To install Bleach to make changes to it:

1. Clone the repo from GitHub::

       $ git clone git://github.com/mozilla/bleach.git

2. Create a virtual environment using whatever method you want.

3. Install Bleach into the virtual environment such that you can see
   changes::

       $ pip install -e .


.. include:: ../CONTRIBUTING.rst


.. include:: ../CODE_OF_CONDUCT.rst


Docs
====

Docs are in ``docs/``. We use Sphinx. Docs are pushed to ReadTheDocs
via a GitHub webhook.


Testing
=======

Run::

    $ tox

That'll run Bleach tests in all the supported Python environments. Note
that you need the necessary Python binaries for them all to be tested.

Tests are run as github actions for test and pull request events.


Release process
===============

1. Checkout master tip.

2. Check to make sure ``setup.py`` and ``requirements-dev.txt`` are
   correct and match requirements-wise.

3. Update version numbers in ``bleach/__init__.py``.

   1. Set ``__version__`` to something like ``2.0.0``. Use semver.
   2. Set ``__releasedate__`` to something like ``20120731``.

4. Update ``CONTRIBUTORS``, ``CHANGES`` and ``MANIFEST.in``.

5. Verify correctness.

   1. Run tests with tox::

         $ tox

   2. Build the docs::

         $ cd docs
         $ make html

   3. Run the doctests (in Python 3)::

         $ cd docs/
         $ make doctest

   4. Verify everything works

6. Commit the changes.

7. Push the changes to GitHub. This will cause Github Actions to run the tests.

8. After CI passes, create a signed tag for the release::

     $ git tag -s v0.4.0

   Copy the details from ``CHANGES`` into the tag comment.

9. Generate distribution files::

     $ python setup.py sdist bdist_wheel

10. Upload them to PyPI::

      $ twine upload dist/*

11. Push the new tag::

      $ git push --tags official master

    That will push the release to PyPI.

12. Blog posts, twitter, etc.
