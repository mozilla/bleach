from nose.tools import eq_

import bleach

def test_no_html():
    eq_('no html string',bleach.clean('no html string'))

