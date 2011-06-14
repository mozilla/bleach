======
Bleach
======

Bleach is an HTML sanitizing library that escapes or strips markup and
attributes based on a white list. Bleach can also linkify text safely, applying
filters that Django's ``urlize`` filter cannot, and optionally setting ``rel``
attributes, even on links already in the text.

The version on `github <http://github.com/jsocol/bleach>`_ is the most
up-to-date and contains the latest bug fixes.


Basic Use
=========

The simplest way to use Bleach is::

    >>> import bleach

    >>> bleach.clean('an <script>evil()</script> example')
    u'an &lt;script&gt;evil()&lt;/script&gt; example'

    >>> bleach.linkify('an http://example.com url')
    u'an <a href="http://example.com" rel="nofollow">http://example.com</a> url

*NB:* Bleach accepts bytestrings or unicode, but it **always** returns unicode.


Customizing Bleach
==================

Both ``clean()`` and ``linkify()`` can take several optional keyword arguments
to customize their behavior.


``clean()``
-----------

+--------------------+-------------------------------------------------------+
| ``tags``           | A whitelist of HTML tags. Must be a list. Defaults to |
|                    | ``bleach.ALLOWED_TAGS``.                              |
+--------------------+-------------------------------------------------------+
| ``attributes``     | A whitelist of HTML attributes. Either a list, in     |
|                    | which case all attributes are allowed on all elements,|
|                    | or a dict, with tag names as keys and lists of allowed|
|                    | attributes as values. Or it is possible to pass a     |
|                    | callable instead of a list that accepts name and value|
|                    | of attribute and returns True of False. Defaults to   |
|                    | ``bleach.ALLOWED_ATTRIBUTES``.                        |
+--------------------+-------------------------------------------------------+
| ``styles``         | A whitelist of allowed CSS properties within a        |
|                    | ``style`` attribute. (Note that ``style`` attributes  |
|                    | are not allowed by default.) Must be a list. Defaults |
|                    | to ``[]``.                                            |
+--------------------+-------------------------------------------------------+
| ``strip``          | Strip disallowed HTML instead of escaping it. A       |
|                    | boolean. Defaults to ``False``.                       |
+--------------------+-------------------------------------------------------+
| ``strip_comments`` | Strip HTML comments. A boolean. Defaults to ``True``. |
+--------------------+-------------------------------------------------------+


``linkify()``
-------------

+-----------------------+----------------------------------------------------+
| ``nofollow``          | Add ``rel="nofollow"`` to non-relative links (both |
|                       | created by ``linkify()`` and those already present |
|                       | in the text). Defaults to ``True``.                |
+-----------------------+----------------------------------------------------+
| ``filter_url``        | A callable through which the ``href`` attribute of |
|                       | links (both created by ``linkify()`` and already   |
|                       | present in the text) will be passed. Must accept a |
|                       | single argument and return a string.               |
+-----------------------+----------------------------------------------------+
| ``filter_text``       | A callable through which the text of links (only   |
|                       | those created by ``linkify``) will be passed. Must |
|                       | accept a single argument and return a string.      |
+-----------------------+----------------------------------------------------+
| ``skip_pre``          | Do not create new links inside ``<pre>`` sections. |
|                       | Still follows ``nofollow``.                        |
+-----------------------+----------------------------------------------------+
| ``parse_email``       | Linkify email addresses with ``mailto:``. Defaults |
|                       | ``False``.                                         |
+-----------------------+----------------------------------------------------+


Contributors
============

https://github.com/jsocol/bleach/contributors
