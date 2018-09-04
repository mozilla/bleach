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
from bleach._vendor.html5lib.serializer import HTMLSerializer
from bleach._vendor.html5lib._tokenizer import HTMLTokenizer
from bleach._vendor.html5lib._trie import Trie


#: Map of entity name to expanded entity
ENTITIES = entities

#: Trie of html entity string -> character representation
ENTITIES_TRIE = Trie(ENTITIES)


class BleachHTMLTokenizer(HTMLTokenizer):
    """Tokenizer that doesn't consume character entities"""
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


class BleachHTMLParser(HTMLParser):
    """Parser that uses BleachHTMLTokenizer"""
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
