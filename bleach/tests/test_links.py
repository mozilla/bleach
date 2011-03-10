import urllib

from nose.tools import eq_

from bleach import linkify, url_re


def filter_url(url):
    return u'http://bouncer/?u=%s' % urllib.quote_plus(url)


def test_url_re():
    def no_match(s):
        match = url_re.search(s)
        if match:
            assert not match, 'matched %s' % s[slice(*match.span())]
    yield no_match, 'just what i am looking for...it'


def test_empty():
    eq_('', linkify(''))


def test_simple_link():
    eq_('a <a href="http://example.com" rel="nofollow">http://example.com'
        '</a> link',
        linkify('a http://example.com link'))
    eq_('a <a href="https://example.com" rel="nofollow">https://example.com'
        '</a> link',
        linkify('a https://example.com link'))


def test_trailing_slash():
    eq_('<a href="http://example.com/" rel="nofollow">http://example.com/</a>',
       linkify('http://example.com/'))
    eq_('<a href="http://example.com/foo/" rel="nofollow">'
        'http://example.com/foo/</a>',
       linkify('http://example.com/foo/'))
    eq_('<a href="http://example.com/foo/bar/" rel="nofollow">'
        'http://example.com/foo/bar/</a>',
       linkify('http://example.com/foo/bar/'))


def test_mangle_link():
    eq_('<a href="http://bouncer/?u=http%3A%2F%2Fexample.com" rel="nofollow">'
        'http://example.com</a>',
        linkify('http://example.com', filter_url=filter_url))


def test_email_link():
    eq_('a james@example.com mailto',
        linkify('a james@example.com mailto'))


def test_tlds():
    eq_('<a href="http://example.com" rel="nofollow">example.com</a>',
        linkify('example.com'))
    eq_('<a href="http://example.co.uk" rel="nofollow">example.co.uk</a>',
        linkify('example.co.uk'))
    eq_('<a href="http://example.edu" rel="nofollow">example.edu</a>',
        linkify('example.edu'))
    eq_('example.xxx', linkify('example.xxx'))
    eq_(' brie', linkify(' brie'))
    eq_('<a href="http://bit.ly/fun" rel="nofollow">bit.ly/fun</a>',
        linkify('bit.ly/fun'))


def test_escaping():
    eq_('&lt; unrelated', linkify('< unrelated'))


def test_nofollow_off():
    eq_('<a href="http://example.com">example.com</a>',
        linkify(u'example.com', nofollow=False))


def test_link_in_html():
    eq_('<i><a href="http://yy.com" rel="nofollow">http://yy.com</a></i>',
        linkify('<i>http://yy.com</i>'))
    eq_('<em><strong><a href="http://xx.com" rel="nofollow">http://xx.com</a>'
        '</strong></em>',
        linkify('<em><strong>http://xx.com</strong></em>'))


def test_links_https():
    eq_('<a href="https://yy.com" rel="nofollow">https://yy.com</a>',
        linkify('https://yy.com'))


def test_add_rel_nofollow():
    """Verify that rel="nofollow" is added to an existing link"""
    eq_('<a href="http://yy.com" rel="nofollow">http://yy.com</a>',
        linkify('<a href="http://yy.com">http://yy.com</a>'))


def test_url_with_path():
    eq_('<a href="http://example.com/path/to/file" rel="nofollow">'
        'http://example.com/path/to/file</a>',
        linkify('http://example.com/path/to/file'))


def test_link_ftp():
    eq_('<a href="ftp://ftp.mozilla.org/some/file" rel="nofollow">'
        'ftp://ftp.mozilla.org/some/file</a>',
        linkify('ftp://ftp.mozilla.org/some/file'))


def test_link_query():
    eq_('<a href="http://xx.com/?test=win" rel="nofollow">'
        'http://xx.com/?test=win</a>',
        linkify('http://xx.com/?test=win'))
    eq_('<a href="http://xx.com/?test=win" rel="nofollow">'
        'xx.com/?test=win</a>',
        linkify('xx.com/?test=win'))
    eq_('<a href="http://xx.com?test=win" rel="nofollow">'
        'xx.com?test=win</a>',
        linkify('xx.com?test=win'))


def test_link_fragment():
    eq_('<a href="http://xx.com/path#frag" rel="nofollow">'
        'http://xx.com/path#frag</a>',
        linkify('http://xx.com/path#frag'))


def test_link_entities():
    eq_('<a href="http://xx.com/?a=1&amp;b=2" rel="nofollow">'
        'http://xx.com/?a=1&amp;b=2</a>',
        linkify('http://xx.com/?a=1&b=2'))


def test_escaped_html():
    """If I pass in escaped HTML, it should probably come out escaped."""
    s = '&lt;em&gt;strong&lt;/em&gt;'
    eq_(s, linkify(s))

# Not supported at this time
# TODO:
# - Can this pass eventually?
#def test_link_http_complete():
#    eq_('<a href="https://user:pass@ftp.mozilla.com/x/y.exe?a=b&amp;c=d'
#        '&amp;e#f">https://user:pass@ftp.mozilla.com/x/y.exe?a=b&amp;'
#        'c=d&amp;e#f</a>',
#        linkify('https://user:pass@ftp.mozilla.org/x/y.exe?a=b&c=d&e#f'))


def test_non_url():
    """document.vulnerable should absolutely not be linkified."""
    s = 'document.vulnerable'
    eq_(s, linkify(s))


def test_javascript_url():
    """javascript: urls should never be linkified."""
    s = 'javascript:document.vulnerable'
    eq_(s, linkify(s))


def test_unsafe_url():
    """Any unsafe char ({}[]<>, etc.) in the path should end URL scanning."""
    eq_('All your{"<a href="http://xx.yy.com/grover.png" '
                     'rel="nofollow">xx.yy.com/grover.png</a>"}base are',
        linkify('All your{"xx.yy.com/grover.png"}base are'))


def test_skip_pre():
    """Skip linkification in <pre> tags."""
    simple = 'http://xx.com <pre>http://xx.com</pre>'
    linked = ('<a href="http://xx.com" rel="nofollow">http://xx.com</a> '
              '<pre>http://xx.com</pre>')
    all_linked = ('<a href="http://xx.com" rel="nofollow">http://xx.com</a> '
                  '<pre><a href="http://xx.com" rel="nofollow">http://xx.com'
                  '</a></pre>')
    eq_(linked, linkify(simple, skip_pre=True))
    eq_(all_linked, linkify(simple))

    already_linked = '<pre><a href="http://xx.com">xx</a></pre>'
    nofollowed = '<pre><a href="http://xx.com" rel="nofollow">xx</a></pre>'
    eq_(nofollowed, linkify(already_linked))
    eq_(nofollowed, linkify(already_linked, skip_pre=True))


def test_libgl():
    """libgl.so.1 should not be linkified."""
    eq_('libgl.so.1', linkify('libgl.so.1'))


def test_end_of_sentence():
    """example.com. should match."""
    eq_('<a href="http://example.com" rel="nofollow">example.com</a>.',
        linkify('example.com.'))
