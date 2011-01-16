# -*- coding: utf-8 -*-

from nose.tools import eq_

from bleach import clean, linkify


def test_japanese_safe_simple():
    eq_(u'ヘルプとチュートリアル', clean(u'ヘルプとチュートリアル'))
    eq_(u'ヘルプとチュートリアル', linkify(u'ヘルプとチュートリアル'))


def test_japanese_strip():
    eq_(u'<em>ヘルプとチュートリアル</em>',
        clean(u'<em>ヘルプとチュートリアル</em>'))
    eq_(u'&lt;span&gt;ヘルプとチュートリアル&lt;/span&gt;',
        clean(u'<span>ヘルプとチュートリアル</span>'))


def test_russian_simple():
    eq_(u'Домашняя', clean(u'Домашняя'))
    eq_(u'Домашняя', linkify(u'Домашняя'))


def test_mixed():
    eq_(u'Домашняяヘルプとチュートリアル',
        clean(u'Домашняяヘルプとチュートリアル'))


def test_mixed_linkify():
    eq_(u'Домашняя <a href="http://example.com" rel="nofollow">'
        u'http://example.com</a> ヘルプとチュートリアル',
        linkify(u'Домашняя http://example.com ヘルプとチュートリアル'))
