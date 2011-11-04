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


def test_domain_match():
    tests = (
        ('ex.mp', 'ex.mp', True),
        ('ex.mp', '*.ex.mp', True),
        ('test.ex.mp', '*.ex.mp', True),
        ('test.ex.mp', 'ex.mp', False),
        ('test.test.ex.mp', '*.ex.mp', False),
        ('test.test.ex.mp', '**.ex.mp', True),
        ('wrong.mp', 'ex.mp', False),
        ('wrong.mp', '*.ex.mp', False),
        ('really.wrong.mp', 'ex.mp', False),
        ('really.wrong.mp', '*.ex.mp', False),
        ('really.very.wrong.mp', '*.ex.mp', False),
        ('EX.mp', 'ex.mp', True),  # Domains are case-insensitive.
        ('ex.mp', 'an.ex.mp', False),
        ('ex.mp', '*.an.ex.mp', False),
        ('an.ex.am.pl', 'an.*.am.pl', True),
        ('a.ex.am.pl', 'an.*.am.pl', False),
        ('ex.am.pl', 'an.*.am.pl', False),
    )

    def _check(t, c, v):
        eq_(v, bleach._domain_match(t, c))

    for t, c, v in tests:
        yield _check, t, c, v


def test_double_star():
    assert bleach._domain_match('ex.mp', '**.ex.mp')
    try:
        bleach._domain_match('ex.mp', 'an.**.ex.mp')
    except bleach.ValidationError:
        pass
    else:
        assert False, '_domain_match should not accept an.**.ex.mp'


def test_allow_subdomains():
    domains = ('ex.mp', '*.exa.mp', 'an.exam.pl', '*.my.examp.le')
    html = (
        ('<a href="http://an.ex.mp">bad</a>', 'bad'),
        ('<a href="http://exa.mp">good</a>', None),
        ('<a href="http://an.exa.mp">good</a>', None),
        ('<a href="http://an.exam.pl">good</a>', None),
        ('<a href="http://another.exam.pl">bad</a>', 'bad'),
        ('<a href="http://a.bad.examp.le">bad</a>', 'bad'),
        ('<a href="http://a.very.bad.examp.le">bad</a>', 'bad'),
    )

    def _check(html, text):
        output = bleach.delinkify(html, allow_domains=domains)
        eq_(html if text is None else text, output)

    for t, o in html:
        yield _check, t, o


def test_mailto_allow_example():
    # example.com is allowed, while ex.mp is not.
    html = ('<a href="mailto:test@example.com">Unchanged</a> '
            '<a href="mailto:test@ex.mp">mail</a>')
    expect = '<a href="mailto:test@example.com">Unchanged</a> mail'
    eq_(expect, bleach.delinkify(html, allow_domains=['example.com']))


def test_mailto_allow_all():
    html = ('<a href="mailto:test@example.com">Unchanged</a> '
            '<a href="mailto:test@ex.mp">mail</a>')
    eq_(html, bleach.delinkify(html, allow_mailto=True))


def test_mailto_disallow_all():
    html = ('<a href="mailto:test@example.com">Unchanged</a> '
            '<a href="mailto:test@ex.mp">mail</a>')
    expect = 'Unchanged mail'
    eq_(expect, bleach.delinkify(html, allow_mailto=False,
                                 allow_domains=['ex.mp']))


def test_mailto_allow_some():
    html = ('<a href="mailto:root@ex.mp?subject=foo">a</a>'
            '<a href="mailto:inv@alid.com?subject=wtf">b</a>'
            '<a href="mailto:Hah%20%3Celse%40evil.com%3E?subject=ow">c</a> '
            '<a href="mailto:BadGuy%20%3Csomeone%40evil.com%3E">d</a>')
    eq_('<a href="mailto:root@ex.mp?subject=foo">a</a>bc d',
        bleach.delinkify(html, allow_domains=['ex.mp']))


def test_parse_mailto():
    """mailto: headers are properly split into emails and rest of headers."""
    expected = {'emails': ['asd'], 'headers': {}}
    actual = bleach._parse_mailto('?to=asd')
    eq_(expected, actual)

    expected = {'emails': ['asd'], 'headers': {'wha': ['tever']}}
    actual = bleach._parse_mailto('?to=asd&wha=tever')
    eq_(expected, actual)

    expected = {'emails': ['z', 'asd'], 'headers': {'wha': ['tever']}}
    actual = bleach._parse_mailto('z?to=asd&wha=tever')
    eq_(expected, actual)

    expected = {'emails': ['z', 'asd@fgh'], 'headers': {'wha': ['tever']}}
    # to: header decoded is "Blah <asd@fgh>"
    actual = bleach._parse_mailto('z?to=Blah%20%3Casd%40fgh%3E&wha=tever')
    eq_(expected, actual)


def test_rebuild_mailto():
    eq_('mailto:test@ex.mp', bleach._rebuild_mailto(['test@ex.mp'], {}))
    eq_('mailto:test@ex.mp%2C%20test2@ex.mp?subject=foo',
        bleach._rebuild_mailto(['test@ex.mp', 'test2@ex.mp'],
                               {'subject': ['foo']}))
