"""More advanced security tests"""

from bleach import clean


def test_nested_script_tag():
    assert '&lt;&lt;script&gt;script&gt;evil()'
    '&lt;&lt;/script&gt;/script&gt;' == \
        clean('<<script>script>evil()<</script>/script>')
    assert '&lt;&lt;x&gt;script&gt;evil()&lt;&lt;/x&gt;/script&gt;' == \
        clean('<<x>script>evil()<</x>/script>')


def test_nested_script_tag_r():
    assert '&lt;script&lt;script&gt;&gt;evil()&lt;/script&lt;&gt;&gt;' == \
        clean('<script<script>>evil()</script</script>>')


def test_invalid_attr():
    IMG = ['img', ]
    IMG_ATTR = ['src']

    assert '<a href="test">test</a>' == \
        clean('<a onclick="evil" href="test">test</a>')
    assert '<img src="test">' == \
        clean('<img onclick="evil" src="test" />',
              tags=IMG, attributes=IMG_ATTR)
    assert '<img src="test">' == \
        clean('<img href="invalid" src="test" />',
              tags=IMG, attributes=IMG_ATTR)


def test_unquoted_attr():
    assert '<abbr title="mytitle">myabbr</abbr>' == \
        clean('<abbr title=mytitle>myabbr</abbr>')


def test_unquoted_event_handler():
    assert '<a href="http://xx.com">xx.com</a>' == \
        clean('<a href="http://xx.com" onclick=foo()>xx.com</a>')


def test_invalid_attr_value():
    assert '&lt;img src="javascript:alert(\'XSS\');"&gt;' == \
        clean('<img src="javascript:alert(\'XSS\');">')


def test_invalid_href_attr():
    assert '<a>xss</a>' == \
        clean('<a href="javascript:alert(\'XSS\')">xss</a>')


def test_invalid_filter_attr():
    IMG = ['img', ]
    IMG_ATTR = {'img': lambda n, v: n == 'src' and v == "http://example.com/"}

    assert '<img src="http://example.com/">' == \
        clean('<img onclick="evil" src="http://example.com/" />',
              tags=IMG, attributes=IMG_ATTR)

    assert '<img>' == clean('<img onclick="evil" src="http://badhost.com/" />',
                            tags=IMG, attributes=IMG_ATTR)


def test_invalid_tag_char():
    assert '&lt;script xss="" '
    'src="http://xx.com/xss.js"&gt;&lt;/script&gt;' == \
        clean('<script/xss src="http://xx.com/xss.js"></script>')
    assert '&lt;script src="http://xx.com/xss.js"&gt;&lt;/script&gt;' == \
        clean('<script/src="http://xx.com/xss.js"></script>')


def test_unclosed_tag():
    assert '&lt;script src="http://xx.com/xss.js&amp;lt;b"&gt;' == \
        clean('<script src=http://xx.com/xss.js<b>')
    assert '&lt;script src="http://xx.com/xss.js" &lt;b=""&gt;' == \
        clean('<script src="http://xx.com/xss.js"<b>')
    assert '&lt;script src="http://xx.com/xss.js" &lt;b=""&gt;' == \
        clean('<script src="http://xx.com/xss.js" <b>')


def test_strip():
    """Using strip=True shouldn't result in malicious content."""
    s = '<scri<script>pt>alert(1)</scr</script>ipt>'
    assert 'pt&gt;alert(1)ipt&gt;' == clean(s, strip=True)
    s = '<scri<scri<script>pt>pt>alert(1)</script>'
    assert 'pt&gt;pt&gt;alert(1)' == clean(s, strip=True)


def test_nasty():
    """Nested, broken up, multiple tags, are still foiled!"""
    test = ('<scr<script></script>ipt type="text/javascript">alert("foo");</'
            '<script></script>script<del></del>>')
    expect = ('&lt;scr&lt;script&gt;&lt;/script&gt;ipt type="text/javascript"'
              '&gt;alert("foo");&lt;/script&gt;script&lt;del&gt;&lt;/del&gt;'
              '&gt;')
    assert expect == clean(test)


def test_poster_attribute():
    """Poster attributes should not allow javascript."""
    tags = ['video']
    attrs = {'video': ['poster']}
    test = '<video poster="javascript:alert(1)"></video>'
    expect = '<video></video>'
    assert expect == clean(test, tags=tags, attributes=attrs)
    ok = '<video poster="/foo.png"></video>'
    assert ok == clean(ok, tags=tags, attributes=attrs)


def test_feed_protocol():
    assert '<a>foo</a>' == clean('<a href="feed:file:///tmp/foo">foo</a>')
