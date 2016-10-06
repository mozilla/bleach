import six
import html5lib

import bleach
from bleach.tests.tools import in_


def test_empty():
    assert '' == bleach.clean('')


def test_nbsp():
    if six.PY3:
        expected = '\xa0test string\xa0'
    else:
        expected = six.u('\\xa0test string\\xa0')

    assert expected == bleach.clean('&nbsp;test string&nbsp;')


def test_comments_only():
    comment = '<!-- this is a comment -->'
    open_comment = '<!-- this is an open comment'
    assert '' == bleach.clean(comment)
    assert '' == bleach.clean(open_comment)
    assert comment == bleach.clean(comment, strip_comments=False)
    assert '{0!s}-->'.format(open_comment) == \
        bleach.clean(open_comment,
                     strip_comments=False)


def test_with_comments():
    html = '<!-- comment -->Just text'
    assert 'Just text' == bleach.clean(html)
    assert html == bleach.clean(html, strip_comments=False)


def test_no_html():
    assert 'no html string' == bleach.clean('no html string')


def test_allowed_html():
    assert 'an <strong>allowed</strong> tag' == \
        bleach.clean('an <strong>allowed</strong> tag')
    assert 'another <em>good</em> tag' == \
        bleach.clean('another <em>good</em> tag')


def test_bad_html():
    assert 'a <em>fixed tag</em>' == \
        bleach.clean('a <em>fixed tag')


def test_function_arguments():
    TAGS = ['span', 'br']
    ATTRS = {'span': ['style']}

    assert 'a <br><span style="">test</span>' == \
        bleach.clean('a <br/><span style="color:red">test</span>',
                     tags=TAGS, attributes=ATTRS)


def test_named_arguments():
    ATTRS = {'a': ['rel', 'href']}
    s = ('<a href="http://xx.com" rel="alternate">xx.com</a>',
         '<a rel="alternate" href="http://xx.com">xx.com</a>')

    assert '<a href="http://xx.com">xx.com</a>' == bleach.clean(s[0])
    in_(s, bleach.clean(s[0], attributes=ATTRS))


def test_disallowed_html():
    assert 'a &lt;script&gt;safe()&lt;/script&gt; test' == \
        bleach.clean('a <script>safe()</script> test')
    assert 'a &lt;style&gt;body{}&lt;/style&gt; test' == \
        bleach.clean('a <style>body{}</style> test')


def test_bad_href():
    assert '<em>no link</em>' == \
        bleach.clean('<em href="fail">no link</em>')


def test_bare_entities():
    assert 'an &amp; entity' == bleach.clean('an & entity')
    assert 'an &lt; entity' == bleach.clean('an < entity')
    assert 'tag &lt; <em>and</em> entity' == \
        bleach.clean('tag < <em>and</em> entity')
    assert '&amp;' == bleach.clean('&amp;')


def test_escaped_entities():
    s = '&lt;em&gt;strong&lt;/em&gt;'
    assert s == bleach.clean(s)


def test_serializer():
    s = '<table></table>'
    assert s == bleach.clean(s, tags=['table'])
    assert 'test<table></table>' == bleach.linkify('<table>test</table>')
    assert '<p>test</p>' == bleach.clean('<p>test</p>', tags=['p'])


def test_no_href_links():
    s = '<a name="anchor">x</a>'
    assert s == bleach.linkify(s)


def test_weird_strings():
    s = '</3'
    assert bleach.clean(s) == ''


def test_xml_render():
    parser = html5lib.HTMLParser()
    assert bleach._render(parser.parseFragment('')) == ''


def test_stripping():
    assert 'a test <em>with</em> <b>html</b> tags' == \
        bleach.clean('a test <em>with</em> <b>html</b> tags', strip=True)
    assert 'a test <em>with</em>  <b>html</b> tags' == \
        bleach.clean('a test <em>with</em> <img src="http://example.com/"> '
                     '<b>html</b> tags', strip=True)

    s = '<p><a href="http://example.com/">link text</a></p>'
    assert '<p>link text</p>' == bleach.clean(s, tags=['p'], strip=True)
    s = '<p><span>multiply <span>nested <span>text</span></span></span></p>'
    assert '<p>multiply nested text</p>' == \
        bleach.clean(s, tags=['p'], strip=True)

    s = ('<p><a href="http://example.com/"><img src="http://example.com/">'
         '</a></p>')
    assert '<p><a href="http://example.com/"></a></p>' == \
        bleach.clean(s, tags=['p', 'a'], strip=True)


def test_allowed_styles():
    ATTR = ['style']
    STYLE = ['color']
    blank = '<b style=""></b>'
    s = '<b style="color: blue;"></b>'
    assert blank == bleach.clean('<b style="top:0"></b>', attributes=ATTR)
    assert s == bleach.clean(s, attributes=ATTR, styles=STYLE)
    assert s == bleach.clean('<b style="top: 0; color: blue;"></b>',
                             attributes=ATTR, styles=STYLE)


def test_idempotent():
    """Make sure that applying the filter twice doesn't change anything."""
    dirty = '<span>invalid & </span> < extra http://link.com<em>'

    clean = bleach.clean(dirty)
    assert clean == bleach.clean(clean)

    linked = bleach.linkify(dirty)
    assert linked == bleach.linkify(linked)


def test_rel_already_there():
    """Make sure rel attribute is updated not replaced"""
    linked = ('Click <a href="http://example.com" rel="tooltip">'
              'here</a>.')
    link_good = (('Click <a href="http://example.com" rel="tooltip nofollow">'
                  'here</a>.'),
                 ('Click <a rel="tooltip nofollow" href="http://example.com">'
                  'here</a>.'))

    in_(link_good, bleach.linkify(linked))
    in_(link_good, bleach.linkify(link_good[0]))


def test_lowercase_html():
    """We should output lowercase HTML."""
    dirty = '<EM CLASS="FOO">BAR</EM>'
    clean = '<em class="FOO">BAR</em>'
    assert clean == bleach.clean(dirty, attributes=['class'])


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
    in_(clean, bleach.clean(dirty, tags=TAG, attributes=ATTR))


def test_sarcasm():
    """Jokes should crash.<sarcasm/>"""
    dirty = 'Yeah right <sarcasm/>'
    clean = 'Yeah right &lt;sarcasm/&gt;'
    assert clean == bleach.clean(dirty)


def test_user_defined_protocols_valid():
    valid_href = '<a href="my_protocol://more_text">allowed href</a>'
    assert valid_href == bleach.clean(valid_href, protocols=['my_protocol'])


def test_user_defined_protocols_invalid():
    invalid_href = '<a href="http://xx.com">invalid href</a>'
    cleaned_href = '<a>invalid href</a>'
    assert cleaned_href == \
        bleach.clean(invalid_href, protocols=['my_protocol'])
