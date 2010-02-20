from nose.tools import eq_

from bleach import Bleach

bl = Bleach()


def test_bleach_shortcut():
    eq_('&lt; escaped and <a href="http://linkified.com" rel="nofollow">linkified.com</a>',
        bl.bleach('< escaped and linkified.com'))
