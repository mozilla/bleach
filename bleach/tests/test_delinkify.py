from nose.tools import eq_

import bleach


def test_delinkify():
    eq_('test', bleach.delinkify('<a href="http://ex.mp">test</a>'))
    eq_('footestbar',
        bleach.delinkify('foo<a href="http://ex.mp">test</a>bar'))


def test_whitelist():
    html = '<a href="http://ex.mp">test</a>'
    eq_(html, bleach.delinkify(html, allow_domains=['ex.mp']))
    eq_('test', bleach.delinkify(html, allow_domains=['ex2.mp']))
    # Allow a single domain as a special case.
    eq_(html, bleach.delinkify(html, allow_domains='ex.mp'))


def test_nested_a():
    html = '<a href="http://ex.mp">test<a href="http://foo.bar">test</a></a>'
    eq_('testtest', bleach.delinkify(html))
    eq_('<a href="http://ex.mp">test</a>test',
        bleach.delinkify(html, allow_domains=['ex.mp']))


def test_nested_tag():
    html = '<a href="http://ex.mp">test<span>test</span></a>'
    eq_('test<span>test</span>', bleach.delinkify(html))


def test_a_name():
    """Don't screw with non-link <a> tags."""
    html = '<a name="foo">bar</a>'
    eq_(html, bleach.delinkify(html))


def test_relative():
    """Relative links are optionally OK."""
    html = 'some <a href="/foo/bar">link</a>'
    eq_('some link', bleach.delinkify(html))
    eq_(html, bleach.delinkify(html, allow_relative=True))


def test_protocol_relative():
    """Protocol-relative links aren't relative."""
    html = 'bad <a href="//ex.mp">link</a>'
    expect = 'bad link'
    eq_(expect, bleach.delinkify(html))
    eq_(expect, bleach.delinkify(html, allow_relative=True))
    eq_(html, bleach.delinkify(html, allow_domains='ex.mp'))
