from nose.tools import eq_
import urllib

from bleach import Bleach

b = Bleach()


class cleach(Bleach):
    def filter_url(self, url):
        return u'http://bouncer/?u=%s' % urllib.quote_plus(url)

    def filter_email_display(self, email):
        return 'dogs'+email

c = cleach()


def test_simple_link():
    eq_('a <a href="http://example.com" rel="nofollow">http://example.com</a> link',
        b.linkify('a http://example.com link'))
    eq_('a <a href="https://example.com" rel="nofollow">https://example.com</a> link',
        b.linkify('a https://example.com link'))


def test_mangle_link():
    eq_('<a href="http://bouncer/?u=http%3A%2F%2Fexample.com" rel="nofollow">http://example.com</a>',
        c.linkify('http://example.com'))


def test_email_link():
    eq_('a <a href="mailto:james@example.com">james@example.com</a> mailto',
        b.linkify('a james@example.com mailto'))


def test_mangle_email():
    eq_('a <a href="mailto:james@example.com">dogsjames@example.com</a> mailto',
        c.linkify('a james@example.com mailto'))


def test_tlds():
    eq_('<a href="http://example.com" rel="nofollow">example.com</a>',
        b.linkify('example.com'))
    eq_('<a href="http://example.co.uk" rel="nofollow">example.co.uk</a>',
        b.linkify('example.co.uk'))
    eq_('<a href="http://example.edu" rel="nofollow">example.edu</a>',
        b.linkify('example.edu'))
    eq_('example.xxx', b.linkify('example.xxx'))


def test_no_escaping():
    eq_('< unrelated', b.linkify('< unrelated'))
