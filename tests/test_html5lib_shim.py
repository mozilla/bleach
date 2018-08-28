import pytest

from bleach import html5lib_shim


@pytest.mark.parametrize('data, expected', [
    # Strings without character entities pass through as is
    ('', ''),
    ('abc', 'abc'),

    # Handles character entities--both named and numeric
    ('&nbsp;', u'\xa0'),
    ('&#32;', ' '),
    ('&#x20;', ' '),

    # Handles ambiguous ampersand
    ('&xx;', '&xx;'),

    # Handles multiple entities in the same string
    ('this &amp; that &amp; that', 'this & that & that'),
])
def test_convert_entities(data, expected):
    assert html5lib_shim.convert_entities(data) == expected
