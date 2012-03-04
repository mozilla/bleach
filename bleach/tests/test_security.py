"""More advanced security tests"""

from nose.tools import eq_

from bleach import clean


def test_nested_script_tag():
    eq_('&lt;&lt;script&gt;script&gt;evil()&lt;&lt;/script&gt;/script&gt;',
        clean('<<script>script>evil()<</script>/script>'))
    eq_('&lt;&lt;x&gt;script&gt;evil()&lt;&lt;/x&gt;/script&gt;',
        clean('<<x>script>evil()<</x>/script>'))


def test_nested_script_tag_r():
    eq_('&lt;script&lt;script&gt;&gt;evil()&lt;/script&lt;&gt;&gt;',
        clean('<script<script>>evil()</script</script>>'))


def test_invalid_attr():
    IMG = ['img', ]
    IMG_ATTR = ['src']

    eq_('<a href="test">test</a>',
        clean('<a onclick="evil" href="test">test</a>'))
    eq_('<img src="test">',
        clean('<img onclick="evil" src="test" />',
                tags=IMG, attributes=IMG_ATTR))
    eq_('<img src="test">',
        clean('<img href="invalid" src="test" />',
                tags=IMG, attributes=IMG_ATTR))


def test_unquoted_attr():
    eq_('<abbr title="mytitle">myabbr</abbr>',
        clean('<abbr title=mytitle>myabbr</abbr>'))


def test_unquoted_event_handler():
    eq_('<a href="http://xx.com">xx.com</a>',
        clean('<a href="http://xx.com" onclick=foo()>xx.com</a>'))


def test_invalid_attr_value():
    eq_('&lt;img src="javascript:alert(\'XSS\');"&gt;',
        clean('<img src="javascript:alert(\'XSS\');">'))


def test_invalid_href_attr():
    eq_('<a>xss</a>',
        clean('<a href="javascript:alert(\'XSS\')">xss</a>'))


def test_invalid_filter_attr():
    IMG = ['img', ]
    IMG_ATTR = {'img': lambda n, v: n == 'src' and v == "http://example.com/"}

    eq_('<img src="http://example.com/">',
        clean('<img onclick="evil" src="http://example.com/" />',
                tags=IMG, attributes=IMG_ATTR))

    eq_('<img>', clean('<img onclick="evil" src="http://badhost.com/" />',
                       tags=IMG, attributes=IMG_ATTR))


def test_invalid_tag_char():
    eq_('&lt;script xss="" src="http://xx.com/xss.js"&gt;&lt;/script&gt;',
        clean('<script/xss src="http://xx.com/xss.js"></script>'))
    eq_('&lt;script src="http://xx.com/xss.js"&gt;&lt;/script&gt;',
        clean('<script/src="http://xx.com/xss.js"></script>'))


def test_unclosed_tag():
    eq_('&lt;script src="http://xx.com/xss.js&amp;lt;b"&gt;',
        clean('<script src=http://xx.com/xss.js<b>'))
    eq_('&lt;script src="http://xx.com/xss.js" &lt;b=""&gt;',
        clean('<script src="http://xx.com/xss.js"<b>'))
    eq_('&lt;script src="http://xx.com/xss.js" &lt;b=""&gt;',
        clean('<script src="http://xx.com/xss.js" <b>'))


def test_strip():
    """Using strip=True shouldn't result in malicious content."""
    s = '<scri<script>pt>alert(1)</scr</script>ipt>'
    eq_('pt&gt;alert(1)ipt&gt;', clean(s, strip=True))
    s = '<scri<scri<script>pt>pt>alert(1)</script>'
    eq_('pt&gt;pt&gt;alert(1)', clean(s, strip=True))


def test_strip_script_contents():
    """Using strip_script_content=True will remove a script completely."""
    tests = (
        ('<p>Hello '
            '<script>function know_how(to) { alert("Write JavaScript"); }'
            '</script>'
        '</p>', '&lt;p&gt;Hello &lt;/p&gt;'),
        ('<p>Hello '
            '<scr<script>function know_how(to) { alert("Write JavaScript"); }'
            '<script></script></scr>'
        '</p>', '&lt;p&gt;Hello &lt;/scr&gt;&lt;/p&gt;'),
        ('<p>My dear '
            '<scr<script>function know_how(to) { alert("<script>"); }'
            '<script></script></scr>'
        '</p>', '&lt;p&gt;My dear &lt;/scr&gt;&lt;/p&gt;')
    )

    def check(teststr, expected_output):
        eq_(expected_output, clean(teststr, strip_script_content=True))

    for test, output in tests:
        yield check, test, output


def test_strip_with_strip_script_contents():
    """Test the combination of strip=True with strip_script_contents=True."""
    tests = (
        # (input, expected output)
        ('<p>A legitimate test '
            '<script>function know_how(to) { alert("Write JS"); }'
            '</script>'
            '<a href="example.com/">This is a test link.</a>'
            '<span> with a test span and <div>div</div></span>.'
         '</p>',
         'A legitimate test This is a test link. with a test span and div.'),
        ('<p>This is an easy one too '
            '<script>document.write(somevar)</script>'
            '<a href="example.com/">This is a test link.</a>'
            '<span> with a test span and <div>div</div></span>.'
         '</p>',
         'This is an easy one too This is a test link. '
         'with a test span and div.'),
        # Tests with <script> tags inside <script> tags.
        ('<p>Good bye. '
            '<script>function die(gotohell) { <script>alert("With you bad '
                '<script> javascript skills."); }'
            '</script>'
            '<a href="example.com/">This is a test link.</a>'
            '<span> with a test span and <div>div</div></span>.'
        '</p>', 'Good bye. This is a test link. with a test span and div.'),
        ('<p>Get lost. '
            '<script>function die(gotohell) { <script>alert("With your bad '
                '<script> javascript </script>skills."); }'
            '</script></script>'
            '<a href="example.com/">This is a test link.</a>'
            '<span> with a test span and <div>div</div></span>.'
        '</p>', 'Get lost. This is a test link. with a test span and div.'),
    )

    def check(teststr, expected_output):
        eq_(expected_output, clean(teststr, tags=[], strip=True,
                                   strip_script_content=True))

    for test, output in tests:
        yield check, test, output


def test_nasty():
    """Nested, broken up, multiple tags, are still foiled!"""
    test = ('<scr<script></script>ipt type="text/javascript">alert("foo");</'
            '<script></script>script<del></del>>')
    expect = (u'&lt;scr&lt;script&gt;&lt;/script&gt;ipt type="text/javascript"'
              u'&gt;alert("foo");&lt;/script&gt;script&lt;del&gt;&lt;/del&gt;'
              u'&gt;')
    eq_(expect, clean(test))
