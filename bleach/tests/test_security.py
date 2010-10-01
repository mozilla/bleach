from nose.tools import eq_

from bleach import Bleach

"""More advanced security tests"""
b = Bleach()


def test_nested_script_tag():
    eq_('&lt;&lt;script&gt;script&gt;evil()&lt;&lt;/script&gt;/script&gt;',
        b.clean('<<script>script>evil()<</script>/script>'))
    eq_('&lt;&lt;x&gt;script&gt;evil()&lt;&lt;/x&gt;/script&gt;',
        b.clean('<<x>script>evil()<</x>/script>'))


def test_nested_script_tag_r():
    eq_('&lt;script&lt;script&gt;&gt;evil()&lt;/script&lt;&gt;&gt;',
        b.clean('<script<script>>evil()</script</script>>'))


def test_invalid_attr():
    IMG = ['img', ]
    IMG_ATTR = ['src']

    eq_('<a href="test">test</a>',
        b.clean('<a onclick="evil" href="test">test</a>'))
    eq_('<img src="test" />',
        b.clean('<img onclick="evil" src="test" />',
                tags=IMG, attributes=IMG_ATTR))
    eq_('<img src="test" />',
        b.clean('<img href="invalid" src="test" />',
                tags=IMG, attributes=IMG_ATTR))


def test_unquoted_attr():
    eq_('<abbr title="mytitle">myabbr</abbr>',
        b.clean('<abbr title=mytitle>myabbr</abbr>'))


def test_unquoted_event_handler():
    eq_('<a href="http://xx.com">xx.com</a>',
        b.clean('<a href="http://xx.com" onclick=foo()>xx.com</a>'))


def test_invalid_attr_value():
    eq_('&lt;img src="javascript:alert(\'XSS\');"&gt;',
        b.clean('<img src="javascript:alert(\'XSS\');">'))


def test_invalid_href_attr():
    eq_('<a>xss</a>',
        b.clean('<a href="javascript:alert(\'XSS\')">xss</a>'))


def test_invalid_tag_char():
    eq_('&lt;script xss="" src="http://xx.com/xss.js"&gt;&lt;/script&gt;',
        b.clean('<script/xss src="http://xx.com/xss.js"></script>'))
    eq_('&lt;script src="http://xx.com/xss.js"&gt;&lt;/script&gt;',
        b.clean('<script/src="http://xx.com/xss.js"></script>'))


def test_unclosed_tag():
    eq_('&lt;script src="http://xx.com/xss.js&amp;lt;b"&gt;',
        b.clean('<script src=http://xx.com/xss.js<b>'))
    eq_('&lt;script src="http://xx.com/xss.js" &lt;b=""&gt;',
        b.clean('<script src="http://xx.com/xss.js"<b>'))
    eq_('&lt;script src="http://xx.com/xss.js" &lt;b=""&gt;',
        b.clean('<script src="http://xx.com/xss.js" <b>'))
