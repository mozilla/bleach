from nose.tools import eq_

import bleach


def test_simple_link():
    eq_('a <a href="http://example.com" rel="nofollow">http://example.com</a> link',
        bleach.linkify('a http://example.com link'))
    eq_('a <a href="https://example.com" rel="nofollow">https://example.com</a> link',
        bleach.linkify('a https://example.com link'))


def test_prefix_link():
    eq_('<a href="http://bouncer/?u=http%3A%2F%2Fexample.com" rel="nofollow">http://example.com</a>',
        bleach.linkify('http://example.com', prefix='http://bouncer/?u='))


def test_email_link():
    eq_('a <a href="mailto:james@example.com">james@example.com</a> mailto',
        bleach.linkify('a james@example.com mailto'))


def test_email_with_prefix():
    eq_('a <a href="mailto:james@example.com">james@example.com</a> mailto',
        bleach.linkify('a james@example.com mailto', prefix='http://bouncer/?u='))
