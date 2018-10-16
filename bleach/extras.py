from bleach.html5lib_shim import Filter
from bleach.sanitizer import (
    ALLOWED_ATTRIBUTES,
    ALLOWED_PROTOCOLS,
    ALLOWED_STYLES,
    ALLOWED_TAGS,
    Cleaner,
)


TAG_TREE_TAGS = ('script', 'style', )


class TagTreeFilter(Filter):

    def __init__(self, source, tags_strip_content=TAG_TREE_TAGS):
        """
        Creates a TagTreeFilter instance.

        This instance will strip the tag and the content tree of tags appearing
        in ``tags_strip_content``.

        :arg Treewalker source: stream
        :arg list tags_strip_content: a list of tags which should be stripped
                                      along with their content/children.
        """
        if not tags_strip_content:
            raise ValueError('must submit `tags_strip_content`')
        self.tags_strip_content = [t.lower() for t in tags_strip_content]
        self._in_strip_content = 0
        return super(TagTreeFilter, self).__init__(source)

    def __iter__(self):
        for token in Filter.__iter__(self):
            _name = token.get('name', '').lower()
            if _name in self.tags_strip_content:
                if token.get('type') == 'StartTag':
                    self._in_strip_content += 1
                elif token.get('type') == 'EndTag':
                    self._in_strip_content -= 1
                continue
            if self._in_strip_content:
                continue
            yield token


def clean_strip_content(
    text, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES,
    styles=ALLOWED_STYLES, protocols=ALLOWED_PROTOCOLS, strip=False,
    strip_comments=True, tags_strip_content=TAG_TREE_TAGS, filters=None,
):
    # whitelist the tags we want to strip, so they can be filtered out
    tags = [t.lower() for t in tags]
    tags_strip_content = [t.lower() for t in tags_strip_content]
    for t in tags_strip_content:
        if t not in tags:
            tags.append(t)
    # ensure we apply the `TagTreeFilter` defined above
    if filters is None:
        filters = [TagTreeFilter, ]
    elif TagTreeFilter not in filters:
        filters.append(TagTreeFilter)
    cleaner = Cleaner(
        tags=tags,
        attributes=attributes,
        styles=styles,
        protocols=protocols,
        strip=strip,
        strip_comments=strip_comments,
        filters=filters,
    )
    return cleaner.clean(text)


__all__ = ('TAG_TREE_TAGS',
           'TagTreeFilter',
           'clean_strip_content',
           )
