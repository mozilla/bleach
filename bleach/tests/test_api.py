from nose.tools import eq_

import bleach


def test_clean():
    s = 'a <em>string</em> with <script>html();</script>'
    escaped = 'a <em>string</em> with &lt;script&gt;html();&lt;/script&gt;'
    stripped = 'a <em>string</em> with html();'
    style = 'a <em style="color: blue;">color</em>'
    eq_(escaped, bleach.clean(s))
    eq_(stripped, bleach.clean(s, strip=True))
    eq_(style, bleach.clean(style, attributes=['style'], styles=['color']))


def test_linkify():
    s = 'a http://github.com link'
    linked = ('a <a href="http://github.com" rel="nofollow">http://github.com'
              '</a> link')
    mangled = 'a <a href="http://github.com">http:...</a> link'
    filter_text = lambda x: x[0:5] + '...'
    eq_(linked, bleach.linkify(s))
    eq_(mangled, bleach.linkify(s, nofollow=False, filter_text=filter_text))
