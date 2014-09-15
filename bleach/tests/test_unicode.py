# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from nose.tools import eq_

from bleach import clean, linkify
from bleach.tests.tools import in_


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
    in_(('Домашняя <a href="http://example.com" rel="nofollow">'
         'http://example.com</a> ヘルプとチュートリアル',
         'Домашняя <a rel="nofollow" href="http://example.com">'
         'http://example.com</a> ヘルプとチュートリアル'),
        linkify('Домашняя http://example.com ヘルプとチュートリアル'))


def test_url_utf8():
    """Allow UTF8 characters in URLs themselves."""
    outs = ('<a href="{0!s}" rel="nofollow">{0!s}</a>',
            '<a rel="nofollow" href="{0!s}">{0!s}</a>')

    out = lambda url: [x.format(url) for x in outs]

    tests = (
        ('http://éxámplé.com/', out('http://éxámplé.com/')),
        ('http://éxámplé.com/íàñá/', out('http://éxámplé.com/íàñá/')),
        ('http://éxámplé.com/íàñá/?foo=bar',
         out('http://éxámplé.com/íàñá/?foo=bar')),
        ('http://éxámplé.com/íàñá/?fóo=bár',
         out('http://éxámplé.com/íàñá/?fóo=bár')),
    )

    def check(test, expected_output):
        in_(expected_output, linkify(test))

    for test, expected_output in tests:
        yield check, test, expected_output
