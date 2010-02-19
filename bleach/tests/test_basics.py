from nose.tools import eq_

import bleach


def test_no_html():
    eq_('no html string', bleach.clean('no html string'))


def test_allowed_html():
    eq_('an <strong>allowed</strong> tag',
        bleach.clean('an <strong>allowed</strong> tag'))
    eq_('another <em>good</em> tag',
        bleach.clean('another <em>good</em> tag'))


def test_bad_html():
    eq_('a <em>fixed tag</em>',
        bleach.clean('a <em>fixed tag'))


def test_disallowed_html():
    eq_('a test',
        bleach.clean('a <script>safe()</script> test'))
    eq_('a test',
        bleach.clean('a <style>body{}</style> test'))
