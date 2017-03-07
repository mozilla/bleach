from html5lib.filters.base import Filter
import pytest
import six

import bleach
from bleach.sanitizer import Cleaner


class TestClean:
    def test_empty(self):
        assert bleach.clean('') == ''

    def test_nbsp(self):
        if six.PY3:
            expected = '\xa0test string\xa0'
        else:
            expected = six.u('\\xa0test string\\xa0')

        assert bleach.clean('&nbsp;test string&nbsp;') == expected

    def test_comments_only(self):
        comment = '<!-- this is a comment -->'
        open_comment = '<!-- this is an open comment'
        assert bleach.clean(comment) == ''
        assert bleach.clean(open_comment) == ''
        assert bleach.clean(comment, strip_comments=False) == comment
        assert (
            bleach.clean(open_comment, strip_comments=False) ==
            '{0!s}-->'.format(open_comment)
        )

    def test_with_comments(self):
        html = '<!-- comment -->Just text'
        assert 'Just text', bleach.clean(html) == 'Just text'
        assert bleach.clean(html, strip_comments=False) == html

    def test_no_html(self):
        assert bleach.clean('no html string') == 'no html string'

    def test_allowed_html(self):
        assert (
            bleach.clean('an <strong>allowed</strong> tag') ==
            'an <strong>allowed</strong> tag'
        )
        assert (
            bleach.clean('another <em>good</em> tag') ==
            'another <em>good</em> tag'
        )

    def test_bad_html(self):
        assert (
            bleach.clean('a <em>fixed tag') ==
            'a <em>fixed tag</em>'
        )

    def test_function_arguments(self):
        TAGS = ['span', 'br']
        ATTRS = {'span': ['style']}

        assert (
            bleach.clean('a <br/><span style="color:red">test</span>',
                         tags=TAGS, attributes=ATTRS) ==
            'a <br><span style="">test</span>'
        )

    def test_named_arguments(self):
        ATTRS = {'a': ['rel', 'href']}

        text = '<a href="http://xx.com" rel="alternate">xx.com</a>'

        assert bleach.clean(text) == '<a href="http://xx.com">xx.com</a>'
        assert (
            bleach.clean(text, attributes=ATTRS) ==
            '<a href="http://xx.com" rel="alternate">xx.com</a>'
        )

    def test_disallowed_html(self):
        assert (
            bleach.clean('a <script>safe()</script> test') ==
            'a &lt;script&gt;safe()&lt;/script&gt; test'
        )
        assert (
            bleach.clean('a <style>body{}</style> test') ==
            'a &lt;style&gt;body{}&lt;/style&gt; test'
        )

    def test_bad_href(self):
        assert (
            bleach.clean('<em href="fail">no link</em>') ==
            '<em>no link</em>'
        )

    def test_bare_entities(self):
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

    def test_escaped_entities(self):
        s = '&lt;em&gt;strong&lt;/em&gt;'
        assert bleach.clean(s) == s

    def test_weird_strings(self):
        s = '</3'
        assert bleach.clean(s) == ''

    def test_stripping(self):
        assert (
            bleach.clean('a test <em>with</em> <b>html</b> tags', strip=True) ==
            'a test <em>with</em> <b>html</b> tags'
        )
        assert (
            bleach.clean('a test <em>with</em> <img src="http://example.com/"> <b>html</b> tags',
                         strip=True) ==
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

        s = '<p><a href="http://example.com/"><img src="http://example.com/"></a></p>'
        assert (
            bleach.clean(s, tags=['p', 'a'], strip=True) ==
            '<p><a href="http://example.com/"></a></p>'
        )

    def test_allowed_styles(self):
        ATTRS = ['style']
        STYLE = ['color']
        blank = '<b style=""></b>'
        s = '<b style="color: blue;"></b>'
        assert bleach.clean('<b style="top:0"></b>', attributes=ATTRS) == blank
        assert bleach.clean(s, attributes=ATTRS, styles=STYLE) == s
        assert (
            bleach.clean('<b style="top: 0; color: blue;"></b>', attributes=ATTRS, styles=STYLE) ==
            s
        )

    def test_lowercase_html(self):
        """We should output lowercase HTML."""
        dirty = '<EM CLASS="FOO">BAR</EM>'
        clean = '<em class="FOO">BAR</em>'
        assert bleach.clean(dirty, attributes=['class']) == clean

    def test_attributes_callable(self):
        """Verify attributes can take a callable"""
        ATTRS = lambda tag, name, val: name == 'title'
        TAGS = ['a']

        assert (
            bleach.clean(u'<a href="/foo" title="blah">example</a>', tags=TAGS, attributes=ATTRS) ==
            u'<a title="blah">example</a>'
        )

    def test_attributes_wildcard(self):
        """Verify attributes[*] works"""
        ATTRS = {
            '*': ['id'],
            'img': ['src'],
        }
        TAGS = ['img', 'em']
        dirty = ('both <em id="foo" style="color: black">can</em> have '
                 '<img id="bar" src="foo"/>')
        assert (
            bleach.clean(dirty, tags=TAGS, attributes=ATTRS) ==
            'both <em id="foo">can</em> have <img id="bar" src="foo">'
        )

    def test_attributes_wildcard_callable(self):
        """Verify attributes[*] callable works"""
        ATTRS = {
            '*': lambda tag, name, val: name == 'title'
        }
        TAGS = ['a']

        assert (
            bleach.clean(u'<a href="/foo" title="blah">example</a>', tags=TAGS, attributes=ATTRS) ==
            u'<a title="blah">example</a>'
        )

    def test_attributes_tag_callable(self):
        """Verify attributes[tag] callable works"""
        def img_test(tag, name, val):
            return name == 'src' and val.startswith('https')

        ATTRS = {
            'img': img_test,
        }
        TAGS = ['img']

        assert (
            bleach.clean('foo <img src="http://example.com" alt="blah"> baz', tags=TAGS,
                         attributes=ATTRS) ==
            u'foo <img> baz'
        )
        assert (
            bleach.clean('foo <img src="https://example.com" alt="blah"> baz', tags=TAGS,
                         attributes=ATTRS) ==
            u'foo <img src="https://example.com"> baz'
        )

    def test_attributes_tag_list(self):
        """Verify attributes[tag] list works"""
        ATTRS = {
            'a': ['title']
        }
        TAGS = ['a']

        assert (
            bleach.clean(u'<a href="/foo" title="blah">example</a>', tags=TAGS, attributes=ATTRS) ==
            u'<a title="blah">example</a>'
        )

    def test_attributes_list(self):
        """Verify attributes list works"""
        ATTRS = ['title']
        TAGS = ['a']

        assert (
            bleach.clean(u'<a href="/foo" title="blah">example</a>', tags=TAGS, attributes=ATTRS) ==
            u'<a title="blah">example</a>'
        )

    def test_svg_attr_val_allows_ref(self):
        """Unescape values in svg attrs that allow url references"""
        # Local IRI, so keep it
        text = '<svg><rect fill="url(#foo)" /></svg>'
        TAGS = ['svg', 'rect']
        ATTRS = {
            'rect': ['fill'],
        }
        assert (
            bleach.clean(text, tags=TAGS, attributes=ATTRS) ==
            '<svg><rect fill="url(#foo)"></rect></svg>'
        )

        # Non-local IRI, so drop it
        text = '<svg><rect fill="url(http://example.com#foo)" /></svg>'
        TAGS = ['svg', 'rect']
        ATTRS = {
            'rect': ['fill'],
        }
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
    def test_svg_allow_local_href(self, text, expected):
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
    def test_svg_allow_local_href_nonlocal(self, text, expected):
        """Drop non-local hrefs for svg elements"""
        TAGS = ['svg', 'pattern']
        ATTRS = {
            'pattern': ['id', 'href'],
        }
        assert bleach.clean(text, tags=TAGS, attributes=ATTRS) == expected

    @pytest.mark.xfail(reason='html5lib >= 0.99999999: changed API')
    def test_sarcasm(self):
        """Jokes should crash.<sarcasm/>"""
        dirty = 'Yeah right <sarcasm/>'
        clean = 'Yeah right &lt;sarcasm/&gt;'
        assert bleach.clean(dirty) == clean

    def test_user_defined_protocols_valid(self):
        valid_href = '<a href="myprotocol://more_text">allowed href</a>'
        assert bleach.clean(valid_href, protocols=['myprotocol']) == valid_href

    def test_user_defined_protocols_invalid(self):
        invalid_href = '<a href="http://xx.com">invalid href</a>'
        cleaned_href = '<a>invalid href</a>'
        assert bleach.clean(invalid_href, protocols=['my_protocol']) == cleaned_href

    def test_filters(self):
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
        dirty = 'this is cute! <img src="http://example.com/puppy.jpg" rel="nofollow">'

        cleaner = Cleaner(tags=TAGS, attributes=ATTRS, filters=[MooFilter])

        assert (
            cleaner.clean(dirty) ==
            'this is cute! <img rel="moo" src="moo">'
        )


def test_clean_idempotent():
    """Make sure that applying the filter twice doesn't change anything."""
    dirty = '<span>invalid & </span> < extra http://link.com<em>'

    assert bleach.clean(bleach.clean(dirty)) == bleach.clean(dirty)


class TestCleaner:
    def test_basics(self):
        TAGS = ['span', 'br']
        ATTRS = {'span': ['style']}

        cleaner = Cleaner(tags=TAGS, attributes=ATTRS)

        assert (
            cleaner.clean('a <br/><span style="color:red">test</span>') ==
            'a <br><span style="">test</span>'
        )
