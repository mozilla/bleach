# -*- coding: utf-8 -*-

from nose.tools import eq_

from bleach import Bleach

b = Bleach()


def test_japanese_safe_simple():
    eq_(u'ヘルプとチュートリアル', b.clean(u'ヘルプとチュートリアル'))
    eq_(u'ヘルプとチュートリアル', b.linkify(u'ヘルプとチュートリアル'))
    eq_(u'ヘルプとチュートリアル', b.bleach(u'ヘルプとチュートリアル'))


def test_japanese_strip():
    eq_(u'<em>ヘルプとチュートリアル</em>',
        b.clean(u'<em>ヘルプとチュートリアル</em>'))
    eq_(u'&lt;span&gt;ヘルプとチュートリアル&lt;/span&gt;',
        b.clean(u'<span>ヘルプとチュートリアル</span>'))

def test_russian_simple():
    eq_(u'Домашняя', b.clean(u'Домашняя'))
    eq_(u'Домашняя', b.linkify(u'Домашняя'))
    eq_(u'Домашняя', b.bleach(u'Домашняя'))

def test_mixed():
    eq_(u'Домашняяヘルプとチュートリアル',
        b.clean(u'Домашняяヘルプとチュートリアル'))

def test_mixed_linkify():
    eq_(u'Домашняя <a href="http://example.com" rel="nofollow">http://example.com</a> ヘルプとチュートリアル',
        b.linkify(u'Домашняя http://example.com ヘルプとチュートリアル'))
