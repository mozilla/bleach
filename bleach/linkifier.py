from __future__ import unicode_literals
import re

from html5lib.filters.base import Filter

from bleach import allowed_protocols
from bleach.encoding import force_unicode
from bleach.utils import alphabetize_attributes


# FIXME(willkg): Move this to a constants module.
TLDS = """ac ad ae aero af ag ai al am an ao aq ar arpa as asia at au aw ax az
       ba bb bd be bf bg bh bi biz bj bm bn bo br bs bt bv bw by bz ca cat
       cc cd cf cg ch ci ck cl cm cn co com coop cr cu cv cx cy cz de dj dk
       dm do dz ec edu ee eg er es et eu fi fj fk fm fo fr ga gb gd ge gf gg
       gh gi gl gm gn gov gp gq gr gs gt gu gw gy hk hm hn hr ht hu id ie il
       im in info int io iq ir is it je jm jo jobs jp ke kg kh ki km kn kp
       kr kw ky kz la lb lc li lk lr ls lt lu lv ly ma mc md me mg mh mil mk
       ml mm mn mo mobi mp mq mr ms mt mu museum mv mw mx my mz na name nc ne
       net nf ng ni nl no np nr nu nz om org pa pe pf pg ph pk pl pm pn post
       pr pro ps pt pw py qa re ro rs ru rw sa sb sc sd se sg sh si sj sk sl
       sm sn so sr ss st su sv sx sy sz tc td tel tf tg th tj tk tl tm tn to
       tp tr travel tt tv tw tz ua ug uk us uy uz va vc ve vg vi vn vu wf ws
       xn xxx ye yt yu za zm zw""".split()

# Make sure that .com doesn't get matched by .co first
TLDS.reverse()


url_re = re.compile(
    r"""\(*  # Match any opening parentheses.
    \b(?<![@.])(?:(?:{0}):/{{0,3}}(?:(?:\w+:)?\w+@)?)?  # http://
    ([\w-]+\.)+(?:{1})(?:\:[0-9]+)?(?!\.\w)\b   # xx.yy.tld(:##)?
    (?:[/?][^\s\{{\}}\|\\\^\[\]`<>"]*)?
        # /path/zz (excluding "unsafe" chars from RFC 1738,
        # except for # and ~, which happen in practice)
    """.format('|'.join(allowed_protocols), '|'.join(TLDS)),
    re.IGNORECASE | re.VERBOSE | re.UNICODE)


proto_re = re.compile(r'^[\w-]+:/{0,3}', re.IGNORECASE)

email_re = re.compile(
    r"""(?<!//)
    (([-!#$%&'*+/=?^_`{0!s}|~0-9A-Z]+
        (\.[-!#$%&'*+/=?^_`{1!s}|~0-9A-Z]+)*  # dot-atom
    |^"([\001-\010\013\014\016-\037!#-\[\]-\177]
        |\\[\001-011\013\014\016-\177])*"  # quoted-string
    )@(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6})  # domain
    """,
    re.IGNORECASE | re.MULTILINE | re.VERBOSE)


class LinkifyFilter(Filter):
    """html5lib filter that linkifies text

    This will do the following:

    * convert email addresses into links
    * convert urls into links
    * edit existing links by running them through callbacks--the default is to
      add a ``rel="nofollow"``

    This filter can be used anywhere html5lib filters can be used.

    """
    def __init__(self, source, callbacks=None, skip_pre=False, parse_email=False):
        super(LinkifyFilter, self).__init__(source)

        self.callbacks = callbacks or []
        self.skip_pre = skip_pre
        self.parse_email = parse_email

    def apply_callbacks(self, attrs, is_new):
        """Given an attrs dict and an is_new bool, runs through callbacks

        Callbacks can return an adjusted attrs dict or None. In the case of
        None, we stop going through callbacks and return that and the link gets
        dropped.

        """
        for cb in self.callbacks:
            attrs = cb(attrs, is_new)
            if attrs is None:
                return None
        return attrs

    def extract_character_data(self, token_list):
        """Extracts and squashes character sequences in a token stream"""
        # FIXME(willkg): This is a terrible idea. What it does is drop all the
        # tags from the token list and merge the Characters and SpaceCharacters
        # tokens into a single text.
        #
        # So something like this::
        #
        #     "<span>" "<b>" "some text" "</b>" "</span>"
        #
        # gets converted to "some text".
        #
        # This gets used to figure out the ``_text`` fauxttribute value for
        # linkify callables.
        #
        # I'm not really sure how else to support that ``_text`` fauxttribute and
        # maintain some modicum of backwards compatability with previous versions
        # of Bleach.

        out = []
        for token in token_list:
            token_type = token['type']
            if token_type in ['Characters', 'SpaceCharacters']:
                out.append(token['data'])

        return u''.join(out)

    def handle_email_addresses(self, src_iter):
        """Handle email addresses in character tokens"""
        for token in src_iter:
            if token['type'] == 'Characters':
                text = token['data']
                new_tokens = []
                end = 0

                # For each email address we find in the text
                for match in email_re.finditer(text):
                    if match.start() > end:
                        new_tokens.append(
                            {u'type': u'Characters', u'data': text[end:match.start()]}
                        )

                    # Run attributes through the callbacks to see what we
                    # should do with this match
                    attrs = {
                        (None, u'href'): u'mailto:%s' % match.group(0),
                        u'_text': match.group(0)
                    }
                    attrs = self.apply_callbacks(attrs, True)

                    if attrs is None:
                        # Just add the text--but not as a link
                        new_tokens.append(
                            {u'type': u'Characters', u'data': match.group(0)}
                        )

                    else:
                        # Add an "a" tag for the new link
                        _text = attrs.pop(u'_text', '')
                        attrs = alphabetize_attributes(attrs)
                        new_tokens.extend([
                            {u'type': u'StartTag', u'name': u'a', u'data': attrs},
                            {u'type': u'Characters', u'data': force_unicode(_text)},
                            {u'type': u'EndTag', u'name': 'a'}
                        ])
                    end = match.end()

                if new_tokens:
                    # Yield the adjusted set of tokens and then continue
                    # through the loop
                    if end < len(text):
                        new_tokens.append({u'type': u'Characters', u'data': text[end:]})

                    for new_token in new_tokens:
                        yield new_token

                    continue

            yield token

    def strip_non_url_bits(self, fragment):
        """Strips non-url bits from the url

        This accounts for over-eager matching by the regex.

        """
        prefix = suffix = ''

        while fragment:
            # Try removing ( from the beginning and, if it's balanced, from the
            # end, too
            if fragment.startswith(u'('):
                prefix = prefix + u'('
                fragment = fragment[1:]

                if fragment.endswith(u')'):
                    suffix = u')' + suffix
                    fragment = fragment[:-1]
                continue

            # Now try extraneous things from the end. For example, sometimes we
            # pick up ) at the end of a url, but the url is in a parenthesized
            # phrase like:
            #
            #     "i looked at the site (at http://example.com)"

            if fragment.endswith(u')') and u'(' not in fragment:
                fragment = fragment[:-1]
                suffix = u')' + suffix
                continue

            # Handle commas
            if fragment.endswith(u','):
                fragment = fragment[:-1]
                suffix = u',' + suffix
                continue

            # Handle periods
            if fragment.endswith(u'.'):
                fragment = fragment[:-1]
                suffix = u'.' + suffix
                continue

            # Nothing matched, so we're done
            break

        return fragment, prefix, suffix

    def handle_links(self, src_iter):
        """Handle links in character tokens"""
        for token in src_iter:
            if token['type'] == 'Characters':
                text = token['data']
                new_tokens = []
                end = 0

                for match in url_re.finditer(text):
                    if match.start() > end:
                        new_tokens.append(
                            {u'type': u'Characters', u'data': text[end:match.start()]}
                        )

                    url = match.group(0)
                    prefix = suffix = ''

                    # Sometimes we pick up too much in the url match, so look for
                    # bits we should drop and remove them from the match
                    url, prefix, suffix = self.strip_non_url_bits(url)

                    # If there's no protocol, add one
                    if re.search(proto_re, url):
                        href = url
                    else:
                        href = u'http://%s' % url

                    attrs = {
                        (None, u'href'): href,
                        u'_text': url
                    }
                    attrs = self.apply_callbacks(attrs, True)

                    if attrs is None:
                        # Just add the text
                        new_tokens.append(
                            {u'type': u'Characters', u'data': prefix + url + suffix}
                        )

                    else:
                        # Add the "a" tag!

                        if prefix:
                            new_tokens.append(
                                {u'type': u'Characters', u'data': prefix}
                            )

                        _text = attrs.pop(u'_text', '')
                        attrs = alphabetize_attributes(attrs)

                        new_tokens.extend([
                            {u'type': u'StartTag', u'name': u'a', u'data': attrs},
                            {u'type': u'Characters', u'data': force_unicode(_text)},
                            {u'type': u'EndTag', u'name': 'a'},
                        ])

                        if suffix:
                            new_tokens.append(
                                {u'type': u'Characters', u'data': suffix}
                            )

                    end = match.end()

                if new_tokens:
                    # Yield the adjusted set of tokens and then continue
                    # through the loop
                    if end < len(text):
                        new_tokens.append({u'type': u'Characters', u'data': text[end:]})

                    for new_token in new_tokens:
                        yield new_token

                    continue

            yield token

    def __iter__(self):
        in_a = False
        in_pre = False

        token_buffer = []

        for token in super(LinkifyFilter, self).__iter__():
            if in_a:
                # Handle the case where we're in an "a" tag--we want to buffer tokens
                # until we hit an end "a" tag.
                if token['type'] == 'EndTag' and token['name'] == 'a':
                    # We're no longer in an "a" tag, so we get all the things we
                    # need to apply callbacks and then figure out what to do with
                    # this "a" tag.
                    in_a = False
                    a_token = token_buffer[0]
                    if a_token['data']:
                        attrs = a_token['data']
                    else:
                        attrs = {}

                    text = self.extract_character_data(token_buffer)
                    attrs['_text'] = text

                    attrs = self.apply_callbacks(attrs, False)
                    if attrs is None:
                        # We're dropping the "a" tag and everything else and replacing
                        # it with character data. So emit that token.
                        yield {'type': 'Characters', 'data': text}

                    else:
                        new_text = attrs.pop('_text', '')
                        # FIXME(willkg): add nofollow here
                        a_token['data'] = alphabetize_attributes(attrs)

                        if text == new_text:
                            # The callbacks didn't change the text, so we yield the
                            # new "a" token, then whatever else was there, then the
                            # end "a" token
                            yield a_token
                            for mem in token_buffer[1:]:
                                yield mem
                            yield token

                        else:
                            # If the callbacks changed the text, then we're going
                            # to drop all the tokens between the start and end "a"
                            # tags and replace it with the new text
                            yield a_token
                            yield {'type': 'Characters', 'data': force_unicode(new_text)}
                            yield token

                    token_buffer = []
                    continue

                else:
                    token_buffer.append(token)
                    continue

            elif token['type'] in ['StartTag', 'EmptyTag']:
                if token['name'] == 'pre' and self.skip_pre:
                    # The "pre" tag starts a "special mode" where we don't linkify
                    # anything.
                    in_pre = True

                elif token['name'] == 'a':
                    # The "a" tag is special--we switch to a slurp mode and
                    # slurp all the tokens until the end "a" tag and then
                    # figure out what to do with them there.
                    in_a = True
                    token_buffer.append(token)

                    # We buffer the start tag, so we don't want to yield it,
                    # yet
                    continue

            elif in_pre and self.skip_pre:
                # NOTE(willkg): We put this clause here since in_a and
                # switching in and out of in_a takes precedence.
                if token['type'] == 'EndTag' and token['name'] == 'pre':
                    in_pre = False

            elif not in_a and not in_pre and token['type'] == 'Characters':
                new_stream = iter([token])
                if self.parse_email:
                    new_stream = self.handle_email_addresses(new_stream)

                new_stream = self.handle_links(new_stream)

                for token in new_stream:
                    yield token

                # We've already yielded this token, so continue
                continue

            yield token
