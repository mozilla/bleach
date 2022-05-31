===============
Goals of Bleach
===============

This document lists the goals and non-goals of Bleach. My hope is that by
focusing on these goals and explicitly listing the non-goals, the project will
evolve in a stronger direction.

.. contents::


Goals
=====


Always take a allowed-list-based approach
-----------------------------------------

Bleach should always take a allowed-list-based approach to markup filtering.
Specifying disallowed lists is error-prone and not future proof.

For example, you should have to opt-in to allowing the ``onclick`` attribute,
not opt-out of all the other ``on*`` attributes. Future versions of HTML may add
new event handlers, like ``ontouch``, that old disallow would not prevent.


Main goal is to sanitize input of malicious content
---------------------------------------------------

The primary goal of Bleach is to sanitize user input that is allowed to contain
*some* HTML as markup and is to be included in the content of a larger page
in an HTML context.

Examples of such content might include:

* User comments on a blog.

* "Bio" sections of a user profile.

* Descriptions of a product or application.

These examples, and others, are traditionally prone to security issues like XSS
or other script injection, or annoying issues like unclosed tags and invalid
markup. Bleach will take a proactive, allowed-list-only approach to allowing
HTML content, and will use the HTML5 parsing algorithm to handle invalid markup.

See the :ref:`chapter on clean() <clean-chapter>` for more info.


Safely create links
-------------------

The secondary goal of Bleach is to provide a mechanism for finding or altering
links (``<a>`` tags with ``href`` attributes, or things that look like URLs or
email addresses) in text.

While Bleach itself will always operate on a allowed-list-based security model,
the :ref:`linkify() method <linkify-chapter>` is flexible enough to allow the
creation, alteration, and removal of links based on an extremely wide range of
use cases.

Bleach does not try to verify the validity or safety of the domains
linked to beyond being well-formed (see :ref:`Linkifying text
fragments <linkify-chapter>` for details).


Non-Goals
=========

Bleach is designed to work with fragments of HTML by untrusted users. Some
non-goal use cases include:


Sanitize complete HTML documents
--------------------------------

Bleach's ``clean`` is not for sanitizing entire HTML documents. Once you're
creating whole documents, you have to allow so many tags that a disallow-list
approach (e.g. forbidding ``<script>`` or ``<object>``) may be more appropriate.


Sanitize for use in HTML attributes, CSS, JSON, xhtml, SVG, or other contexts
-----------------------------------------------------------------------------

Bleach's ``clean`` is used for sanitizing content to be used in an HTML
context--not for HTML attributes, CSS, JSON, xhtml, SVG, or other contexts.

For example, this is a safe use of ``clean`` output in an HTML context::

    <p>
      {{ bleach.clean(user_bio) }}
    </p>


This is a **not safe** use of ``clean`` output in an HTML attribute::

    <body data-bio="{{ bleach.clean(user_bio) }}">


If you need to use the output of ``bleach.clean()`` in an HTML attribute, you
need to pass it through your template library's escape function. For example,
Jinja2's ``escape`` or ``django.utils.html.escape`` or something like that.

If you need to use the output of ``bleach.clean()`` in any other context,
you need to pass it through an appropriate sanitizer/escaper for that
context.


Remove all HTML or transforming content for some non-web-page purpose
---------------------------------------------------------------------

There are much faster tools available if you want to remove or escape all HTML
from a document.


Clean up after trusted users
----------------------------

Bleach is powerful but it is not fast. If you trust your users, trust them and
don't rely on Bleach to clean up their mess.


Make malicious content look pretty or sane
------------------------------------------

Malicious content is designed to be malicious. Making it safe is a design goal
of Bleach. Making it pretty or sane-looking is not.

If you want your malicious content to look pretty, you should pass it through
Bleach to make it safe and then do your own transform afterwards.


Allow arbitrary styling
-----------------------

There are a number of interesting CSS properties that can do dangerous things,
like Opera's ``-o-link``. Painful as it is, if you want your users to be able to
change nearly anything in a ``style`` attribute, you should have to opt into
this.

Usage with Javascript frameworks and template languages
-------------------------------------------------------

A number of Javascript frameworks and template languages allow `XSS
via Javascript Gadgets <http://sebastian-lekies.de/slides/appsec2017.pdf>`_.
While Bleach usually produces output safe for these contexts, it is
not tested against them nor guaranteed to produce safe output.  Check
that bleach properly strips or escapes language-specific syntax like
``data-bind`` attributes for Knockout.js or ``ng-*`` attributes from
Angular templates before using bleach-sanitized output with your
framework or template language.

Protect against CSS-based XSS attacks in legacy browsers
--------------------------------------------------------

Bleach will not protect against CSS-based XSS vectors that only worked
in legacy IE, Opera, or Netscape/Mozilla/Firefox browsers. For
example, it will not remove ``expression`` or ``url`` functions in CSS
component values in style elements or attributes and `other vectors
<https://html5sec.org/#css>`_.


Protect against privacy, cross site, or HTTP leaks
--------------------------------------------------

Bleach does not prevent output from fingerprinting users or leaking
information about users via requests to external sites. For example,
it will not remove CSS Media Queries or tracking pixels.

See also:

* `browser leaks <https://browserleaks.com/>`__
* `HTTP leaks <https://github.com/cure53/HTTPLeaks>`__
* `XS leaks <https://xsleaks.dev/>`__

Bleach vs html5lib
==================

Bleach is built upon html5lib_, and html5lib has `a built-in sanitizer filter
<https://html5lib.readthedocs.io/en/latest/html5lib.filters.html#module-html5lib.filters.sanitizer>`_,
so why use Bleach?

* Bleach's API is simpler.
* Bleach's sanitizer allows a map to be provided for ``ALLOWED_ATTRIBUTES``,
  giving you a lot more control over sanitizing attributes: you can sanitize
  attributes for specific tags, you can sanitize based on value, etc.
* Bleach's sanitizer always alphabetizes attributes, but uses an alphabetizer
  that works with namespaces — the html5lib one is broken in that regard.
* Bleach's sanitizer always quotes attribute values because that's the safe
  thing to do. The html5lib one makes that configurable. In this case, Bleach
  doesn't make something configurable that isn't safe.
* Bleach's sanitizer has a very restricted set of ``ALLOWED_PROTOCOLS`` by
  default. html5lib has a much more expansive one that Bleach's authors claim is
  less safe.
* ``html5lib.filters.sanitizer.Filter``'s ``sanitize_css`` is broken and doesn't
  work.

.. _html5lib: https://github.com/html5lib/html5lib-python
