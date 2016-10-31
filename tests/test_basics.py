import six
import html5lib

import bleach


def test_empty():
    assert bleach.clean('') == ''


def test_nbsp():
    if six.PY3:
        expected = '\xa0test string\xa0'
    else:
        expected = six.u('\\xa0test string\\xa0')

    assert bleach.clean('&nbsp;test string&nbsp;') == expected


def test_comments_only():
    comment = '<!-- this is a comment -->'
    open_comment = '<!-- this is an open comment'
    assert bleach.clean(comment) == ''
    assert bleach.clean(open_comment) == ''
    assert bleach.clean(comment, strip_comments=False) == comment
    assert (
        bleach.clean(open_comment, strip_comments=False) ==
        '{0!s}-->'.format(open_comment)
    )


def test_with_comments():
    html = '<!-- comment -->Just text'
    assert 'Just text', bleach.clean(html) == 'Just text'
    assert bleach.clean(html, strip_comments=False) == html


def test_no_html():
    assert bleach.clean('no html string') == 'no html string'


def test_allowed_html():
    assert (
        bleach.clean('an <strong>allowed</strong> tag') ==
        'an <strong>allowed</strong> tag'
    )
    assert (
        bleach.clean('another <em>good</em> tag') ==
        'another <em>good</em> tag'
    )


def test_bad_html():
    assert (
        bleach.clean('a <em>fixed tag') ==
        'a <em>fixed tag</em>'
    )


def test_function_arguments():
    TAGS = ['span', 'br']
    ATTRS = {'span': ['style']}

    assert (
        bleach.clean('a <br/><span style="color:red">test</span>',
                     tags=TAGS, attributes=ATTRS) ==
        'a <br><span style="">test</span>'
    )


def test_named_arguments():
    ATTRS = {'a': ['rel', 'href']}
    s = ('<a href="http://xx.com" rel="alternate">xx.com</a>',
         '<a rel="alternate" href="http://xx.com">xx.com</a>')

    assert bleach.clean(s[0]) == '<a href="http://xx.com">xx.com</a>'
    # FIXME: This might not be needed if attribute order is stable now.
    assert bleach.clean(s[0], attributes=ATTRS) in s


def test_disallowed_html():
    assert (
        bleach.clean('a <script>safe()</script> test') ==
        'a &lt;script&gt;safe()&lt;/script&gt; test'
    )
    assert (
        bleach.clean('a <style>body{}</style> test') ==
        'a &lt;style&gt;body{}&lt;/style&gt; test'
    )


def test_bad_href():
    assert (
        bleach.clean('<em href="fail">no link</em>') ==
        '<em>no link</em>'
    )


def test_bare_entities():
    assert (
        bleach.clean('an & entity') ==
        'an &amp; entity'
    )
    assert (
        bleach.clean('an < entity') ==
        'an &lt; entity'
    )

    assert (
        bleach.clean('tag < <em>and</em> entity') ==
        'tag &lt; <em>and</em> entity'
    )

    assert (
        bleach.clean('&amp;') ==
        '&amp;'
    )


def test_escaped_entities():
    s = '&lt;em&gt;strong&lt;/em&gt;'
    assert bleach.clean(s) == s


def test_serializer():
    s = '<table></table>'
    assert bleach.clean(s, tags=['table']) == s
    assert bleach.linkify('<table>test</table>') == 'test<table></table>'
    assert bleach.clean('<p>test</p>', tags=['p']) == '<p>test</p>'


def test_no_href_links():
    s = '<a name="anchor">x</a>'
    assert bleach.linkify(s) == s


def test_weird_strings():
    s = '</3'
    assert bleach.clean(s) == ''


def test_xml_render():
    parser = html5lib.HTMLParser()
    assert bleach._render(parser.parseFragment('')) == ''


def test_stripping():
    assert (
        bleach.clean('a test <em>with</em> <b>html</b> tags', strip=True) ==
        'a test <em>with</em> <b>html</b> tags'
    )
    assert (
        bleach.clean('a test <em>with</em> <img src="http://example.com/"> <b>html</b> tags', strip=True) ==
        'a test <em>with</em>  <b>html</b> tags'
    )

    s = '<p><a href="http://example.com/">link text</a></p>'
    assert (
        bleach.clean(s, tags=['p'], strip=True) ==
        '<p>link text</p>'
    )
    s = '<p><span>multiply <span>nested <span>text</span></span></span></p>'
    assert (
        bleach.clean(s, tags=['p'], strip=True) ==
        '<p>multiply nested text</p>'
    )

    s = ('<p><a href="http://example.com/"><img src="http://example.com/">'
         '</a></p>')
    assert (
        bleach.clean(s, tags=['p', 'a'], strip=True) ==
        '<p><a href="http://example.com/"></a></p>'
    )


def test_allowed_styles():
    ATTR = ['style']
    STYLE = ['color']
    blank = '<b style=""></b>'
    s = '<b style="color: blue;"></b>'
    assert bleach.clean('<b style="top:0"></b>', attributes=ATTR) == blank
    assert bleach.clean(s, attributes=ATTR, styles=STYLE) == s
    assert (
        bleach.clean('<b style="top: 0; color: blue;"></b>', attributes=ATTR, styles=STYLE) ==
        s
    )


def test_idempotent():
    """Make sure that applying the filter twice doesn't change anything."""
    dirty = '<span>invalid & </span> < extra http://link.com<em>'

    clean = bleach.clean(dirty)
    assert bleach.clean(clean) == clean

    possible_outs = (
        '<span>invalid &amp; </span> &lt; extra <a rel="nofollow" href="http://link.com">http://link.com</a><em></em>',
        '<span>invalid &amp; </span> &lt; extra <a href="http://link.com" rel="nofollow">http://link.com</a><em></em>'
    )
    linked = bleach.linkify(dirty)
    assert bleach.linkify(linked) in possible_outs


def test_rel_already_there():
    """Make sure rel attribute is updated not replaced"""
    linked = ('Click <a href="http://example.com" rel="tooltip">'
              'here</a>.')
    link_good = (('Click <a href="http://example.com" rel="tooltip nofollow">'
                  'here</a>.'),
                 ('Click <a rel="tooltip nofollow" href="http://example.com">'
                  'here</a>.'))

    assert bleach.linkify(linked) in link_good
    assert bleach.linkify(link_good[0]) in link_good


def test_lowercase_html():
    """We should output lowercase HTML."""
    dirty = '<EM CLASS="FOO">BAR</EM>'
    clean = '<em class="FOO">BAR</em>'
    assert bleach.clean(dirty, attributes=['class']) == clean


def test_wildcard_attributes():
    ATTR = {
        '*': ['id'],
        'img': ['src'],
    }
    TAG = ['img', 'em']
    dirty = ('both <em id="foo" style="color: black">can</em> have '
             '<img id="bar" src="foo"/>')
    clean = ('both <em id="foo">can</em> have <img src="foo" id="bar">',
             'both <em id="foo">can</em> have <img id="bar" src="foo">')
    assert bleach.clean(dirty, tags=TAG, attributes=ATTR) in clean


def test_sarcasm():
    """Jokes should crash.<sarcasm/>"""
    dirty = 'Yeah right <sarcasm/>'
    clean = 'Yeah right &lt;sarcasm/&gt;'
    assert bleach.clean(dirty) == clean


def test_user_defined_protocols_valid():
    valid_href = '<a href="my_protocol://more_text">allowed href</a>'
    assert bleach.clean(valid_href, protocols=['my_protocol']) == valid_href


def test_user_defined_protocols_invalid():
    invalid_href = '<a href="http://xx.com">invalid href</a>'
    cleaned_href = '<a>invalid href</a>'
    assert bleach.clean(invalid_href, protocols=['my_protocol']) == cleaned_href
