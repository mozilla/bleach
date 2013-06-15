# -*- coding: utf-8 -*-

from nose.tools import eq_

from bleach import clean, linkify


def test_japanese_safe_simple():
    eq_('ヘルプとチュートリアル', clean('ヘルプとチュートリアル'))
    eq_('ヘルプとチュートリアル', linkify('ヘルプとチュートリアル'))


def test_japanese_strip():
    eq_('<em>ヘルプとチュートリアル</em>',
        clean('<em>ヘルプとチュートリアル</em>'))
    eq_('&lt;span&gt;ヘルプとチュートリアル&lt;/span&gt;',
        clean('<span>ヘルプとチュートリアル</span>'))


def test_russian_simple():
    eq_('Домашняя', clean('Домашняя'))
    eq_('Домашняя', linkify('Домашняя'))


def test_mixed():
    eq_('Домашняяヘルプとチュートリアル',
        clean('Домашняяヘルプとチュートリアル'))


def test_mixed_linkify():
    eq_('Домашняя <a href="http://example.com" rel="nofollow">'
        'http://example.com</a> ヘルプとチュートリアル',
        linkify('Домашняя http://example.com ヘルプとチュートリアル'))


def test_url_utf8():
    """Allow UTF8 characters in URLs themselves."""
    out = '<a href="%(url)s" rel="nofollow">%(url)s</a>'

    tests = (
        ('http://éxámplé.com/', out % {'url': 'http://éxámplé.com/'}),
        ('http://éxámplé.com/íàñá/',
                out % {'url': 'http://éxámplé.com/íàñá/'}),
        ('http://éxámplé.com/íàñá/?foo=bar',
            out % {'url': 'http://éxámplé.com/íàñá/?foo=bar'}),
        ('http://éxámplé.com/íàñá/?fóo=bár',
            out % {'url': 'http://éxámplé.com/íàñá/?fóo=bár'}),
    )

    def check(test, expected_output):
        eq_(expected_output, linkify(test))

    for test, expected_output in tests:
        yield check, test, expected_output
