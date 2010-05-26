from nose.tools import eq_

from bleach import Bleach

b = Bleach()


def test_no_html():
    eq_('no html string', b.clean('no html string'))


def test_allowed_html():
    eq_('an <strong>allowed</strong> tag',
        b.clean('an <strong>allowed</strong> tag'))
    eq_('another <em>good</em> tag',
        b.clean('another <em>good</em> tag'))


def test_bad_html():
    eq_('a <em>fixed tag</em>',
        b.clean('a <em>fixed tag'))


def test_function_arguments():
    TAGS = ['span']
    ATTRS = {'span': ['style']}

    eq_('a <span style="color: red;">test</span>',
        b.clean('a <span style="color:red">test</span>',
                     tags=TAGS, attributes=ATTRS))


def test_named_arguments():
    ATTRS = {'a': ['rel', 'href']}
    s = u'<a href="http://xx.com" rel="alternate">xx.com</a>'
    eq_('<a href="http://xx.com">xx.com</a>', b.clean(s))
    eq_(s, b.clean(s, attributes=ATTRS))


def test_disallowed_html():
    eq_('a &lt;script&gt;safe()&lt;/script&gt; test',
        b.clean('a <script>safe()</script> test'))
    eq_('a &lt;style&gt;body{}&lt;/style&gt; test',
        b.clean('a <style>body{}</style> test'))


def test_bad_href():
    eq_('<em>no link</em>',
        b.clean('<em href="fail">no link</em>'))


def test_bare_entities():
    eq_('an &amp; entity', b.clean('an & entity'))
    eq_('an &lt; entity', b.clean('an < entity'))
    eq_('tag &lt; <em>and</em> entity', b.clean('tag < <em>and</em> entity'))
    eq_('&amp;', b.clean('&amp;'))


def test_escaped_entities():
    s = u'&lt;em&gt;strong&lt;/em&gt;'
    eq_(s, b.clean(s))


def test_serializer():
    s = u'<table></table>'
    eq_(s, b.clean(s, tags=['table']))
    eq_(u'test<table></table>', b.linkify(u'<table>test</table>'))
