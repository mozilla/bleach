from nose.tools import eq_

from bleach import Bleach

bl = Bleach()


def test_bleach_shortcut():
    eq_('&lt; escaped and <a href="http://linkified.com" rel="nofollow">linkified.com</a>',
        bl.bleach('< escaped and linkified.com'))


def test_bleach_with_href():
    """Make sure an explicit link doesn't get linkified as well."""
    eq_(u'<a href="http://xx.com" title="xx">xx</a> '
        u'<a href="http://yy.com" rel="nofollow">http://yy.com</a>',
        bl.bleach('<a title="xx" href="http://xx.com">xx</a> http://yy.com'))
