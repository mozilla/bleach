from nose.tools import eq_

import bleach

"""More advanced security tests"""


def test_nested_script_tag():
    eq_('', bleach.clean('<<script>script>evil_func()<</script>/script>'))
    eq_('', bleach.clean('<<x>script>evil_func()<</x>/script>'))


def test_nested_script_tag_r():
    eq_('', bleach.clean('<script<script>>evil()</script</script>>'))


def test_invalid_attr():
    eq_('<a href="test">test</a>',
        bleach.clean('<a onclick="evil" href="test">test</a>'))
    eq_('<img src="test" />',
        bleach.clean('<img onclick="evil" src="test" />'))
    eq_('<img src="test" />',
        bleach.clean('<img href="invalid" src="test" />'))
