"""More advanced security tests"""

from bleach import clean


def test_nested_script_tag():
    assert (
        clean('<<script>script>evil()<</script>/script>') ==
        '&lt;&lt;script&gt;script&gt;evil()&lt;&lt;/script&gt;/script&gt;'
    )
    assert (
        clean('<<x>script>evil()<</x>/script>') ==
        '&lt;&lt;x&gt;script&gt;evil()&lt;&lt;/x&gt;/script&gt;'
    )


def test_nested_script_tag_r():
    assert (
        clean('<script<script>>evil()</script</script>>') ==
        '&lt;script&lt;script&gt;&gt;evil()&lt;/script&lt;&gt;&gt;'
    )


def test_invalid_attr():
    IMG = ['img', ]
    IMG_ATTR = ['src']

    assert (
        clean('<a onclick="evil" href="test">test</a>') ==
        '<a href="test">test</a>'
    )
    assert (
        clean('<img onclick="evil" src="test" />', tags=IMG, attributes=IMG_ATTR) ==
        '<img src="test">'
    )
    assert (
        clean('<img href="invalid" src="test" />', tags=IMG, attributes=IMG_ATTR) ==
        '<img src="test">'
    )


def test_unquoted_attr():
    assert (
        clean('<abbr title=mytitle>myabbr</abbr>') ==
        '<abbr title="mytitle">myabbr</abbr>'
    )


def test_unquoted_event_handler():
    assert (
        clean('<a href="http://xx.com" onclick=foo()>xx.com</a>') ==
        '<a href="http://xx.com">xx.com</a>'
    )


def test_invalid_attr_value():
    assert (
        clean('<img src="javascript:alert(\'XSS\');">') ==
        '&lt;img src="javascript:alert(\'XSS\');"&gt;'
    )


def test_invalid_href_attr():
    assert (
        clean('<a href="javascript:alert(\'XSS\')">xss</a>') ==
        '<a>xss</a>'
    )


def test_invalid_filter_attr():
    IMG = ['img', ]
    IMG_ATTR = {'img': lambda n, v: n == 'src' and v == "http://example.com/"}

    assert (
        clean('<img onclick="evil" src="http://example.com/" />', tags=IMG, attributes=IMG_ATTR) ==
        '<img src="http://example.com/">'
    )
    assert (
        clean('<img onclick="evil" src="http://badhost.com/" />', tags=IMG, attributes=IMG_ATTR) ==
        '<img>'
    )


def test_invalid_tag_char():
    assert (
        clean('<script/xss src="http://xx.com/xss.js"></script>') ==
        '&lt;script xss="" src="http://xx.com/xss.js"&gt;&lt;/script&gt;'
    )
    assert (
        clean('<script/src="http://xx.com/xss.js"></script>') ==
        '&lt;script src="http://xx.com/xss.js"&gt;&lt;/script&gt;'
    )


def test_unclosed_tag():
    assert (
        clean('<script src=http://xx.com/xss.js<b>') ==
        '&lt;script src="http://xx.com/xss.js&amp;lt;b"&gt;'
    )
    assert (
        clean('<script src="http://xx.com/xss.js"<b>') ==
        '&lt;script src="http://xx.com/xss.js" &lt;b=""&gt;'
    )
    assert (
        clean('<script src="http://xx.com/xss.js" <b>') ==
        '&lt;script src="http://xx.com/xss.js" &lt;b=""&gt;'
    )


def test_strip():
    """Using strip=True shouldn't result in malicious content."""
    s = '<scri<script>pt>alert(1)</scr</script>ipt>'
    assert clean(s, strip=True) == 'pt&gt;alert(1)ipt&gt;'
    s = '<scri<scri<script>pt>pt>alert(1)</script>'
    assert clean(s, strip=True) == 'pt&gt;pt&gt;alert(1)'


def test_nasty():
    """Nested, broken up, multiple tags, are still foiled!"""
    test = ('<scr<script></script>ipt type="text/javascript">alert("foo");</'
            '<script></script>script<del></del>>')
    expect = ('&lt;scr&lt;script&gt;&lt;/script&gt;ipt type="text/javascript"'
              '&gt;alert("foo");&lt;/script&gt;script&lt;del&gt;&lt;/del&gt;'
              '&gt;')
    assert clean(test) == expect


def test_poster_attribute():
    """Poster attributes should not allow javascript."""
    tags = ['video']
    attrs = {'video': ['poster']}
    test = '<video poster="javascript:alert(1)"></video>'
    assert clean(test, tags=tags, attributes=attrs) == '<video></video>'
    ok = '<video poster="/foo.png"></video>'
    assert clean(ok, tags=tags, attributes=attrs) == ok


def test_feed_protocol():
    assert clean('<a href="feed:file:///tmp/foo">foo</a>') == '<a>foo</a>'
