from html5lib.filters.base import Filter
import pytest

import bleach
from bleach.sanitizer import Cleaner


def test_empty():
    assert bleach.clean('') == ''


def test_nbsp():
    assert bleach.clean('&nbsp;test string&nbsp;') == '&nbsp;test string&nbsp;'


def test_comments_only():
    comment = '<!-- this is a comment -->'
    assert bleach.clean(comment) == ''
    assert bleach.clean(comment, strip_comments=False) == comment

    open_comment = '<!-- this is an open comment'
    assert bleach.clean(open_comment) == ''
    assert (
        bleach.clean(open_comment, strip_comments=False) ==
        '{0!s}-->'.format(open_comment)
    )


def test_with_comments():
    text = '<!-- comment -->Just text'
    assert bleach.clean(text) == 'Just text'
    assert bleach.clean(text, strip_comments=False) == text


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

    text = 'a <br/><span style="color:red">test</span>'
    assert (
        bleach.clean(text, tags=TAGS, attributes=ATTRS) ==
        'a <br><span style="">test</span>'
    )


def test_named_arguments():
    ATTRS = {'a': ['rel', 'href']}

    text = '<a href="http://xx.com" rel="alternate">xx.com</a>'
    assert bleach.clean(text) == '<a href="http://xx.com">xx.com</a>'
    assert (
        bleach.clean(text, attributes=ATTRS) ==
        '<a href="http://xx.com" rel="alternate">xx.com</a>'
    )


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


@pytest.mark.parametrize('text, expected', [
    ('an & entity', 'an &amp; entity'),
    ('an < entity', 'an &lt; entity'),
    ('tag < <em>and</em> entity', 'tag &lt; <em>and</em> entity'),
])
def test_bare_entities(text, expected):
    assert bleach.clean(text) == expected


@pytest.mark.parametrize('text, expected', [
    # Test character entities
    ('&amp;', '&amp;'),
    ('&nbsp;', '&nbsp;'),
    ('&lt;em&gt;strong&lt;/em&gt;', '&lt;em&gt;strong&lt;/em&gt;'),

    # Test character entity at beginning of string
    ('&amp;is cool', '&amp;is cool'),

    # Test it at the end of the string
    ('cool &amp;', 'cool &amp;'),

    # Test bare ampersands and entities at beginning
    ('&&amp; is cool', '&amp;&amp; is cool'),

    # Test entities and bare ampersand at end
    ('&amp; is cool &amp;&', '&amp; is cool &amp;&amp;'),

    # Test missing semi-colon means we don't treat it like an entity
    ('this &amp that', 'this &amp;amp that'),

    # Test a thing that looks like a character entity, but isn't because it's
    # missing a ; (&curren)
    (
        'http://example.com?active=true&current=true',
        'http://example.com?active=true&amp;current=true'
    ),

    # Test entities in HTML attributes
    (
        '<a href="?art&amp;copy">foo</a>',
        '<a href="?art&amp;copy">foo</a>'
    ),
    (
        '<a href="?this=&gt;that">foo</a>',
        '<a href="?this=&gt;that">foo</a>'
    ),
    (
        '<a href="http://example.com?active=true&current=true">foo</a>',
        '<a href="http://example.com?active=true&amp;current=true">foo</a>'
    ),

    # Test numeric entities
    ('&#39;', '&#39;'),
    ('&#34;', '&#34;'),
    ('&#123;', '&#123;'),
    ('&#x0007b;', '&#x0007b;'),
    ('&#x0007B;', '&#x0007B;'),

    # Test non-numeric entities
    ('&#', '&amp;#'),
    ('&#<', '&amp;#&lt;')
])
def test_character_entities(text, expected):
    assert bleach.clean(text) == expected


def test_weird_strings():
    s = '</3'
    assert bleach.clean(s) == ''


def test_stripping():
    text = 'a test <em>with</em> <b>html</b> tags'
    assert (
        bleach.clean(text, strip=True) ==
        'a test <em>with</em> <b>html</b> tags'
    )

    text = 'a test <em>with</em> <img src="http://example.com/"> <b>html</b> tags'
    assert (
        bleach.clean(text, strip=True) ==
        'a test <em>with</em>  <b>html</b> tags'
    )

    text = '<p><a href="http://example.com/">link text</a></p>'
    assert (
        bleach.clean(text, tags=['p'], strip=True) ==
        '<p>link text</p>'
    )
    text = '<p><span>multiply <span>nested <span>text</span></span></span></p>'
    assert (
        bleach.clean(text, tags=['p'], strip=True) ==
        '<p>multiply nested text</p>'
    )

    text = '<p><a href="http://example.com/"><img src="http://example.com/"></a></p>'
    assert (
        bleach.clean(text, tags=['p', 'a'], strip=True) ==
        '<p><a href="http://example.com/"></a></p>'
    )


def test_allowed_styles():
    ATTRS = ['style']
    STYLE = ['color']

    assert (
        bleach.clean('<b style="top:0"></b>', attributes=ATTRS) ==
        '<b style=""></b>'
    )

    text = '<b style="color: blue;"></b>'
    assert bleach.clean(text, attributes=ATTRS, styles=STYLE) == text

    text = '<b style="top: 0; color: blue;"></b>'
    assert (
        bleach.clean(text, attributes=ATTRS, styles=STYLE) ==
        '<b style="color: blue;"></b>'
    )


def test_lowercase_html():
    """We should output lowercase HTML."""
    assert (
        bleach.clean('<EM CLASS="FOO">BAR</EM>', attributes=['class']) ==
        '<em class="FOO">BAR</em>'
    )


def test_attributes_callable():
    """Verify attributes can take a callable"""
    ATTRS = lambda tag, name, val: name == 'title'
    TAGS = ['a']

    text = u'<a href="/foo" title="blah">example</a>'
    assert (
        bleach.clean(text, tags=TAGS, attributes=ATTRS) ==
        u'<a title="blah">example</a>'
    )


def test_attributes_wildcard():
    """Verify attributes[*] works"""
    ATTRS = {
        '*': ['id'],
        'img': ['src'],
    }
    TAGS = ['img', 'em']

    text = 'both <em id="foo" style="color: black">can</em> have <img id="bar" src="foo"/>'
    assert (
        bleach.clean(text, tags=TAGS, attributes=ATTRS) ==
        'both <em id="foo">can</em> have <img id="bar" src="foo">'
    )


def test_attributes_wildcard_callable():
    """Verify attributes[*] callable works"""
    ATTRS = {
        '*': lambda tag, name, val: name == 'title'
    }
    TAGS = ['a']

    assert (
        bleach.clean(u'<a href="/foo" title="blah">example</a>', tags=TAGS, attributes=ATTRS) ==
        u'<a title="blah">example</a>'
    )


def test_attributes_tag_callable():
    """Verify attributes[tag] callable works"""
    def img_test(tag, name, val):
        return name == 'src' and val.startswith('https')

    ATTRS = {
        'img': img_test,
    }
    TAGS = ['img']

    text = 'foo <img src="http://example.com" alt="blah"> baz'
    assert (
        bleach.clean(text, tags=TAGS, attributes=ATTRS) ==
        u'foo <img> baz'
    )
    text = 'foo <img src="https://example.com" alt="blah"> baz'
    assert (
        bleach.clean(text, tags=TAGS, attributes=ATTRS) ==
        u'foo <img src="https://example.com"> baz'
    )


def test_attributes_tag_list():
    """Verify attributes[tag] list works"""
    ATTRS = {
        'a': ['title']
    }
    TAGS = ['a']

    assert (
        bleach.clean(u'<a href="/foo" title="blah">example</a>', tags=TAGS, attributes=ATTRS) ==
        u'<a title="blah">example</a>'
    )


def test_attributes_list():
    """Verify attributes list works"""
    ATTRS = ['title']
    TAGS = ['a']

    text = u'<a href="/foo" title="blah">example</a>'
    assert (
        bleach.clean(text, tags=TAGS, attributes=ATTRS) ==
        u'<a title="blah">example</a>'
    )


def test_svg_attr_val_allows_ref():
    """Unescape values in svg attrs that allow url references"""
    # Local IRI, so keep it
    TAGS = ['svg', 'rect']
    ATTRS = {
        'rect': ['fill'],
    }

    text = '<svg><rect fill="url(#foo)" /></svg>'
    assert (
        bleach.clean(text, tags=TAGS, attributes=ATTRS) ==
        '<svg><rect fill="url(#foo)"></rect></svg>'
    )

    # Non-local IRI, so drop it
    TAGS = ['svg', 'rect']
    ATTRS = {
        'rect': ['fill'],
    }
    text = '<svg><rect fill="url(http://example.com#foo)" /></svg>'
    assert (
        bleach.clean(text, tags=TAGS, attributes=ATTRS) ==
        '<svg><rect></rect></svg>'
    )


@pytest.mark.parametrize('text, expected', [
    (
        '<svg><pattern id="patt1" href="#patt2"></pattern></svg>',
        '<svg><pattern href="#patt2" id="patt1"></pattern></svg>'
    ),
    (
        '<svg><pattern id="patt1" xlink:href="#patt2"></pattern></svg>',
        # NOTE(willkg): Bug in html5lib serializer drops the xlink part
        '<svg><pattern id="patt1" href="#patt2"></pattern></svg>'
    ),
])
def test_svg_allow_local_href(text, expected):
    """Keep local hrefs for svg elements"""
    TAGS = ['svg', 'pattern']
    ATTRS = {
        'pattern': ['id', 'href'],
    }
    assert bleach.clean(text, tags=TAGS, attributes=ATTRS) == expected


@pytest.mark.parametrize('text, expected', [
    (
        '<svg><pattern id="patt1" href="https://example.com/patt"></pattern></svg>',
        '<svg><pattern id="patt1"></pattern></svg>'
    ),
    (
        '<svg><pattern id="patt1" xlink:href="https://example.com/patt"></pattern></svg>',
        '<svg><pattern id="patt1"></pattern></svg>'
    ),
])
def test_svg_allow_local_href_nonlocal(text, expected):
    """Drop non-local hrefs for svg elements"""
    TAGS = ['svg', 'pattern']
    ATTRS = {
        'pattern': ['id', 'href'],
    }
    assert bleach.clean(text, tags=TAGS, attributes=ATTRS) == expected


@pytest.mark.xfail(reason='html5lib >= 0.99999999: changed API')
def test_sarcasm():
    """Jokes should crash.<sarcasm/>"""
    dirty = 'Yeah right <sarcasm/>'
    clean = 'Yeah right &lt;sarcasm/&gt;'
    assert bleach.clean(dirty) == clean


def test_user_defined_protocols_valid():
    valid_href = '<a href="myprotocol://more_text">allowed href</a>'
    assert bleach.clean(valid_href, protocols=['myprotocol']) == valid_href


def test_user_defined_protocols_invalid():
    invalid_href = '<a href="http://xx.com">invalid href</a>'
    cleaned_href = '<a>invalid href</a>'
    assert bleach.clean(invalid_href, protocols=['my_protocol']) == cleaned_href


def test_filters():
    # Create a Filter that changes all the attr values to "moo"
    class MooFilter(Filter):
        def __iter__(self):
            for token in Filter.__iter__(self):
                if token['type'] in ['StartTag', 'EmptyTag'] and token['data']:
                    for attr, value in token['data'].items():
                        token['data'][attr] = 'moo'

                yield token

    ATTRS = {
        'img': ['rel', 'src']
    }
    TAGS = ['img']

    cleaner = Cleaner(tags=TAGS, attributes=ATTRS, filters=[MooFilter])

    dirty = 'this is cute! <img src="http://example.com/puppy.jpg" rel="nofollow">'
    assert (
        cleaner.clean(dirty) ==
        'this is cute! <img rel="moo" src="moo">'
    )


def test_clean_idempotent():
    """Make sure that applying the filter twice doesn't change anything."""
    dirty = '<span>invalid & </span> < extra http://link.com<em>'
    assert bleach.clean(bleach.clean(dirty)) == bleach.clean(dirty)


def test_only_text_is_cleaned():
    some_text = 'text'
    some_type = int
    no_type = None

    assert bleach.clean(some_text) == some_text

    with pytest.raises(TypeError):
        bleach.clean(some_type)

    with pytest.raises(TypeError):
        bleach.clean(no_type)


class TestCleaner:
    def test_basics(self):
        TAGS = ['span', 'br']
        ATTRS = {'span': ['style']}

        cleaner = Cleaner(tags=TAGS, attributes=ATTRS)

        assert (
            cleaner.clean('a <br/><span style="color:red">test</span>') ==
            'a <br><span style="">test</span>'
        )
