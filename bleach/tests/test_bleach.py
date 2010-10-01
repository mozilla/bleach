from nose.tools import eq_

from bleach import Bleach

bl = Bleach()


def test_bleach_shortcut():
    eq_('&lt; escaped and <a href="http://linkified.com" rel="nofollow">'
        'linkified.com</a>', bl.bleach('< escaped and linkified.com'))


def test_bleach_with_href():
    """Make sure an explicit link doesn't get linkified as well."""
    eq_(u'<a href="http://xx.com" rel="nofollow" title="xx">xx</a> '
        u'<a href="http://yy.com" rel="nofollow">http://yy.com</a>',
        bl.bleach('<a title="xx" href="http://xx.com">xx</a> http://yy.com'))
    eq_('<a href="http://xx.com" rel="nofollow">http://xx.com</a>',
        bl.bleach('<a href="http://xx.com">http://xx.com</a>'))


def test_idempotent():
    """Make sure that applying the filter twice doesn't change anything."""
    dirty = u'<span>invalid & </span> < extra http://link.com<em>'

    clean = bl.clean(dirty)
    eq_(clean, bl.clean(clean))

    bleached = bl.bleach(dirty)
    eq_(bleached, bl.bleach(bleached))

    linked = bl.linkify(dirty)
    eq_(linked, bl.linkify(linked))


def test_escaped_html():
    s = u'&lt;em&gt;strong&lt;/em&gt;'
    eq_(s, bl.bleach(s))


def test_self_closing():
    """Self closing tags are untouched."""
    eq_('<img />', bl.clean('<img />', tags=['img']))
