# flake8: noqa
"""
Shim module between Bleach and html5lib. This makes it easier to upgrade the
html5lib library without having to change a lot of code.
"""

from __future__ import unicode_literals

import re
import string

import six

from bleach._vendor.html5lib import (
    HTMLParser,
    getTreeWalker,
)
from bleach._vendor.html5lib.constants import (
    entities,
    namespaces,
    prefixes,
    tokenTypes,
)
from bleach._vendor.html5lib.constants import _ReparseException as ReparseException
from bleach._vendor.html5lib.filters.base import Filter
from bleach._vendor.html5lib.filters.sanitizer import allowed_protocols
from bleach._vendor.html5lib.filters.sanitizer import Filter as SanitizerFilter
from bleach._vendor.html5lib._inputstream import HTMLInputStream
from bleach._vendor.html5lib.serializer import HTMLSerializer
from bleach._vendor.html5lib._tokenizer import HTMLTokenizer
from bleach._vendor.html5lib._trie import Trie


#: Map of entity name to expanded entity
ENTITIES = entities

#: Trie of html entity string -> character representation
ENTITIES_TRIE = Trie(ENTITIES)


class InputStreamWithMemory(object):
    """Wraps an HTMLInputStream to remember what characters we've seen

    It didn't make sense to implement our own HTMLInputStream, so this
    wraps the existing ones and keeps track of what we've seen so far. We
    do this so we can provide the original string the stream had in the case
    where Bleach's cleaner is going to escape a disallowed tag so we can
    escape the original string.

    """
    def __init__(self, inner_stream):
        self._inner_stream = inner_stream
        self._buffer = []

    @property
    def errors(self):
        return self._inner_stream.errors

    def reset(self):
        return self._inner_stream.reset()

    def position(self):
        return self._inner_stream.position()

    def char(self):
        c = self._inner_stream.char()
        # char() can return None if EOF, so ignore that
        if c:
            self._buffer.append(c)
        return c

    def charsUntil(self, characters, opposite=False):
        chars = self._inner_stream.charsUntil(characters, opposite=opposite)
        self._buffer.extend(list(chars))
        return chars

    def unget(self, char):
        if self._buffer:
            self._buffer.pop(-1)
        return self._inner_stream.unget(char)

    def stream_history(self):
        return self._buffer


def get_recent_tag_string(stream_history, token):
    """Find the original text for the tag

    This goes back through the stream we've tokenized for the most recent
    complete HTML tag-like thing as it existed in the stream. It assumes that
    the current character in the stream ias a >.

    :arg list stream_history: list of characters to look through
    :arg dict token: the tag token we're looking for in the stream

    :returns: original tag from < to >

    """
    name_reversed = list(reversed(token['name']))
    if token['type'] == tokenTypes['EndTag']:
        name_reversed.append('/')
    name_reversed_len = len(name_reversed)

    quotey_things = '"\''
    pile = []
    in_quotes = []
    for c in reversed(stream_history):
        if in_quotes:
            if c == in_quotes[-1]:
                in_quotes.pop(-1)
            elif c in quotey_things:
                in_quotes.append(c)

            pile.append(c)

        elif c in quotey_things:
            in_quotes.append(c)
            pile.append(c)

        elif c == '<':
            if pile[-name_reversed_len:] == name_reversed:
                pile.append(c)
                break
            else:
                pile.append(c)
        else:
            pile.append(c)

    pile.reverse()
    ret = six.text_type('').join(pile)
    return ret


class BleachHTMLTokenizer(HTMLTokenizer):
    """Tokenizer that doesn't consume character entities"""
    def __init__(self, stream, parser=None, **kwargs):
        # Stomp on the HTMLTokenizer __init__ in order to wrap the stream.
        self.stream = InputStreamWithMemory(HTMLInputStream(stream, **kwargs))

        # Do all the things the HTMLTokenizer does in __init__
        self.parser = parser
        self.escapeFlag = False
        self.lastFourChars = []
        self.state = self.dataState
        self.escape = False
        self.currentToken = None

    def __iter__(self):
        last_error_token = None

        for token in super(BleachHTMLTokenizer, self).__iter__():
            if last_error_token is not None:
                token_name = token['data'].lower().strip()
                if ((last_error_token['data'] == 'expected-closing-tag-but-got-char' and
                     token_name not in self.parser.tags)):
                    # We've got either a malformed tag or a pseudo-tag or
                    # something that html5lib wants to turn into a malformed
                    # comment which Bleach clean() will drop so we interfere
                    # with the token stream to handle it more correctly.
                    #
                    # If this is an allowed tag, it's malformed and we just let
                    # the html5lib parser deal with it--we don't enter into this
                    # block.
                    #
                    # If this is not an allowed tag, then we convert it to
                    # characters and it'll get escaped in the sanitizer.

                    # Create a fake EndTag token so get_recent_tag_string works right
                    fake_end_tag = {'type': tokenTypes['EndTag'], 'name': token['data']}
                    token['data'] = get_recent_tag_string(
                        self.stream.stream_history(), fake_end_tag
                    )
                    token['type'] = tokenTypes['Characters']
                    yield token

                else:
                    yield last_error_token
                    yield token

                last_error_token = None
                continue

            # If the token is a ParseError, we hold on to it so we can get the
            # next token and potentially fix it.
            if token['type'] == tokenTypes['ParseError']:
                last_error_token = token
                continue

            yield token

    def consumeEntity(self, allowedChar=None, fromAttribute=False):
        # We don't want to consume and convert entities, so this overrides the
        # html5lib tokenizer's consumeEntity so that it's now a no-op.
        #
        # However, when that gets called, it's consumed an &, so we put that in
        # the stream.
        if fromAttribute:
            self.currentToken['data'][-1][1] += '&'

        else:
            self.tokenQueue.append({"type": tokenTypes['Characters'], "data": '&'})

    def emitCurrentToken(self):
        token = self.currentToken

        if ((self.parser.tags is not None and
             token['type'] in (tokenTypes['StartTag'], tokenTypes['EndTag']) and
             token['name'].lower() not in self.parser.tags)):
            # If this is a start/end tag for a tag that's not in our allowed
            # list, then it gets stripped or escaped. In both of these cases
            # it gets converted to a Characters token.
            if self.parser.strip:
                # If we're stripping the token, we just throw in an empty
                # string token.
                new_data = ''

            else:
                # If we're escaping the token, we want to escape the exact
                # original string. Since tokenizing also normalizes data
                # and this is a tag-like thing, we've lost some information.
                # So we go back through the stream to get the original
                # string and use that.
                new_data = get_recent_tag_string(self.stream.stream_history(), token)

            new_token = {
                'type': tokenTypes['Characters'],
                'data': new_data
            }

            self.currentToken = new_token
            self.tokenQueue.append(new_token)
            self.state = self.dataState
            return

        super(BleachHTMLTokenizer, self).emitCurrentToken()


class BleachHTMLParser(HTMLParser):
    """Parser that uses BleachHTMLTokenizer"""
    def __init__(self, tags, strip, **kwargs):
        """
        :arg tags: list of allowed tages--everything else is either stripped or
            escaped; if None, then this doesn't look at tags at all
        :arg strip: whether to strip disallowed tags (True) or escape them (False);
            if tags=None, then this doesn't have any effect

        """
        self.tags = [tag.lower() for tag in tags] if tags is not None else None
        self.strip = strip
        super(BleachHTMLParser, self).__init__(**kwargs)

    def _parse(self, stream, innerHTML=False, container='div', scripting=False, **kwargs):
        # Override HTMLParser so we can swap out the tokenizer for our own.
        self.innerHTMLMode = innerHTML
        self.container = container
        self.scripting = scripting
        self.tokenizer = BleachHTMLTokenizer(stream, parser=self, **kwargs)
        self.reset()

        try:
            self.mainLoop()
        except ReparseException:
            self.reset()
            self.mainLoop()


def convert_entity(value):
    """Convert an entity (minus the & and ; part) into what it represents

    This handles numeric, hex, and text entities.

    :arg value: the string (minus the ``&`` and ``;`` part) to convert

    :returns: unicode character or None if it's an ambiguous ampersand that
        doesn't match a character entity

    """
    if value[0] == '#':
        if value[1] in ('x', 'X'):
            return six.unichr(int(value[2:], 16))
        return six.unichr(int(value[1:], 10))

    return ENTITIES.get(value, None)


def convert_entities(text):
    """Converts all found entities in the text

    :arg text: the text to convert entities in

    :returns: unicode text with converted entities

    """
    if '&' not in text:
        return text

    new_text = []
    for part in next_possible_entity(text):
        if not part:
            continue

        if part.startswith('&'):
            entity = match_entity(part)
            if entity is not None:
                converted = convert_entity(entity)

                # If it's not an ambiguous ampersand, then replace with the
                # unicode character. Otherwise, we leave the entity in.
                if converted is not None:
                    new_text.append(converted)
                    remainder = part[len(entity) + 2:]
                    if part:
                        new_text.append(remainder)
                    continue

        new_text.append(part)

    return u''.join(new_text)


def match_entity(stream):
    """Returns first entity in stream or None if no entity exists

    Note: For Bleach purposes, entities must start with a "&" and end with
    a ";". This ignoresambiguous character entities that have no ";" at the
    end.

    :arg stream: the character stream

    :returns: ``None`` or the entity string without "&" or ";"

    """
    # Nix the & at the beginning
    if stream[0] != '&':
        raise ValueError('Stream should begin with "&"')

    stream = stream[1:]

    stream = list(stream)
    possible_entity = ''
    end_characters = '<&=;' + string.whitespace

    # Handle number entities
    if stream and stream[0] == '#':
        possible_entity = '#'
        stream.pop(0)

        if stream and stream[0] in ('x', 'X'):
            allowed = '0123456789abcdefABCDEF'
            possible_entity += stream.pop(0)
        else:
            allowed = '0123456789'

        # FIXME(willkg): Do we want to make sure these are valid number
        # entities? This doesn't do that currently.
        while stream and stream[0] not in end_characters:
            c = stream.pop(0)
            if c not in allowed:
                break
            possible_entity += c

        if possible_entity and stream and stream[0] == ';':
            return possible_entity
        return None

    # Handle character entities
    while stream and stream[0] not in end_characters:
        c = stream.pop(0)
        if not ENTITIES_TRIE.has_keys_with_prefix(possible_entity):
            break
        possible_entity += c

    if possible_entity and stream and stream[0] == ';':
        return possible_entity

    return None


AMP_SPLIT_RE = re.compile('(&)')


def next_possible_entity(text):
    """Takes a text and generates a list of possible entities

    :arg text: the text to look at

    :returns: generator where each part (except the first) starts with an
        "&"

    """
    for i, part in enumerate(AMP_SPLIT_RE.split(text)):
        if i == 0:
            yield part
        elif i % 2 == 0:
            yield '&' + part


class BleachHTMLSerializer(HTMLSerializer):
    """HTMLSerializer that undoes & -> &amp; in attributes"""
    def escape_base_amp(self, stoken):
        """Escapes just bare & in HTML attribute values"""
        # First, undo escaping of &. We need to do this because html5lib's
        # HTMLSerializer expected the tokenizer to consume all the character
        # entities and convert them to their respective characters, but the
        # BleachHTMLTokenizer doesn't do that. For example, this fixes
        # &amp;entity; back to &entity; .
        stoken = stoken.replace('&amp;', '&')

        # However, we do want all bare & that are not marking character
        # entities to be changed to &amp;, so let's do that carefully here.
        for part in next_possible_entity(stoken):
            if not part:
                continue

            if part.startswith('&'):
                entity = match_entity(part)
                # Only leave entities in that are not ambiguous. If they're
                # ambiguous, then we escape the ampersand.
                if entity is not None and convert_entity(entity) is not None:
                    yield '&' + entity + ';'

                    # Length of the entity plus 2--one for & at the beginning
                    # and and one for ; at the end
                    part = part[len(entity) + 2:]
                    if part:
                        yield part
                    continue

            yield part.replace('&', '&amp;')

    def serialize(self, treewalker, encoding=None):
        """Wrap HTMLSerializer.serialize and conver & to &amp; in attribute values

        Note that this converts & to &amp; in attribute values where the & isn't
        already part of an unambiguous character entity.

        """
        in_tag = False
        after_equals = False

        for stoken in super(BleachHTMLSerializer, self).serialize(treewalker, encoding):
            if in_tag:
                if stoken == '>':
                    in_tag = False

                elif after_equals:
                    if stoken != '"':
                        for part in self.escape_base_amp(stoken):
                            yield part

                        after_equals = False
                        continue

                elif stoken == '=':
                    after_equals = True

                yield stoken
            else:
                if stoken.startswith('<'):
                    in_tag = True
                yield stoken
