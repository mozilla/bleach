"""More advanced security tests"""

import os

import pytest
import six

from bleach import clean


def test_escaped_entities():
    # html5lib unescapes character entities, so these would become ' and "
    # which makes it possible to break out of html attributes.
    #
    # Verify that bleach.clean() doesn't unescape entities.
    assert (
        clean('&#39;&#34;') ==
        '&#39;&#34;'
    )


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
        '&lt;script&lt;script&gt;&gt;evil()&gt;&lt;/script&lt;script&gt;'
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
    IMG_ATTR = {
        'img': lambda tag, name, val: name == 'src' and val == "http://example.com/"
    }

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
        clean('<script/xss src="http://xx.com/xss.js"></script>') in
        [
            '&lt;script src="http://xx.com/xss.js" xss=""&gt;&lt;/script&gt;',
            '&lt;script xss="" src="http://xx.com/xss.js"&gt;&lt;/script&gt;'
        ]
    )
    assert (
        clean('<script/src="http://xx.com/xss.js"></script>') ==
        '&lt;script src="http://xx.com/xss.js"&gt;&lt;/script&gt;'
    )


def test_unclosed_tag():
    assert (
        clean('<script src=http://xx.com/xss.js<b>') ==
        '&lt;script src="http://xx.com/xss.js&lt;b"&gt;&lt;/script&gt;'
    )
    assert (
        clean('<script src="http://xx.com/xss.js"<b>') in
        [
            '&lt;script src="http://xx.com/xss.js" &lt;b=""&gt;&lt;/script&gt;',
            '&lt;script &lt;b="" src="http://xx.com/xss.js"&gt;&lt;/script&gt;'
        ]
    )
    assert (
        clean('<script src="http://xx.com/xss.js" <b>') in
        [
            '&lt;script src="http://xx.com/xss.js" &lt;b=""&gt;&lt;/script&gt;',
            '&lt;script &lt;b="" src="http://xx.com/xss.js"&gt;&lt;/script&gt;'
        ]
    )


def test_strip():
    """Using strip=True shouldn't result in malicious content."""
    s = '<scri<script>pt>alert(1)</scr</script>ipt>'
    assert clean(s, strip=True) == 'pt&gt;alert(1)ipt&gt;'
    s = '<scri<scri<script>pt>pt>alert(1)</script>'
    assert clean(s, strip=True) == 'pt&gt;pt&gt;alert(1)'


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


@pytest.mark.parametrize('data, expected', [
    # Convert bell
    ('1\a23', '1?23'),

    # Convert backpsace
    ('1\b23', '1?23'),

    # Convert formfeed
    ('1\v23', '1?23'),

    # Convert vertical tab
    ('1\f23', '1?23'),

    # Convert a bunch of characters in a string
    ('import y\bose\bm\bi\bt\be\b', 'import y?ose?m?i?t?e?'),
])
def test_invisible_characters(data, expected):
    assert clean(data) == expected


def get_tests():
    """Retrieves regression tests from data/ directory

    :returns: list of ``(filename, filedata)`` tuples

    """
    datadir = os.path.join(os.path.dirname(__file__), 'data')
    tests = [
        os.path.join(datadir, fn) for fn in os.listdir(datadir)
        if fn.endswith('.test')
    ]
    # Sort numerically which makes it easier to iterate through them
    tests.sort(key=lambda x: int(os.path.basename(x).split('.', 1)[0]))

    testcases = [
        (fn, open(fn, 'r').read()) for fn in tests
    ]

    return testcases


@pytest.mark.parametrize('fn, text', get_tests())
def test_regressions(fn, text):
    """Regression tests for clean so we can see if there are issues"""
    expected = six.text_type(open(fn + '.out', 'r').read())

    # NOTE(willkg): This strips input and expected which makes it easier to
    # maintain the files. If there comes a time when the input needs whitespace
    # at the beginning or end, then we'll have to figure out something else.
    assert clean(text.strip()) == expected.strip()
