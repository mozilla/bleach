from nose.tools import eq_

from bleach import Bleach

bl = Bleach()


def test_bleach_shortcut():
    eq_('&lt; escaped and <a href="http://linkified.com" rel="nofollow">linkified.com</a>',
        bl.bleach('< escaped and linkified.com'))


def test_bleach_with_href():
    """Make sure an explicit link doesn't get linkified as well."""
    eq_(u'<a href="http://xx.com" rel="nofollow" title="xx">xx</a> '
        u'<a href="http://yy.com" rel="nofollow">http://yy.com</a>',
        bl.bleach('<a title="xx" href="http://xx.com">xx</a> http://yy.com'))
    eq_('<a href="http://xx.com" rel="nofollow">http://xx.com</a>',
        bl.bleach('<a href="http://xx.com">http://xx.com</a>'))
