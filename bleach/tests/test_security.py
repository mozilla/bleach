from nose.tools import eq_

import bleach

"""More advanced security tests"""


def test_nested_script_tag():
    eq_('&lt;&lt;script&gt;script&gt;evil()&lt;&lt;/script&gt;/script&gt;',
        bleach.clean('<<script>script>evil()<</script>/script>'))
    eq_('&lt;&lt;x&gt;script&gt;evil()&lt;&lt;/x&gt;/script&gt;',
        bleach.clean('<<x>script>evil()<</x>/script>'))


def test_nested_script_tag_r():
    eq_('&lt;script&lt;script&gt;&gt;evil()&lt;/script&lt;&gt;&gt;',
        bleach.clean('<script<script>>evil()</script</script>>'))


def test_invalid_attr():
    IMG = ['img',]
    IMG_ATTR = ['src']

    eq_('<a href="test">test</a>',
        bleach.clean('<a onclick="evil" href="test">test</a>'))
    eq_('<img src="test"/>',
        bleach.clean('<img onclick="evil" src="test" />',
                     allowed_tags=IMG, allowed_attributes=IMG_ATTR))
    eq_('<img src="test"/>',
        bleach.clean('<img href="invalid" src="test" />',
                     allowed_tags=IMG, allowed_attributes=IMG_ATTR))
