from functools import partial

import pytest

from bleach import clean


clean = partial(clean, tags=['p'], attributes=['style'])


@pytest.mark.parametrize('data, styles, expected', [
    (
        'font-family: Arial; color: red; float: left; background-color: red;',
        ['color'],
        'color: red;'
    ),
    (
        'border: 1px solid blue; color: red; float: left;',
        ['color'],
        'color: red;'
    ),
    (
        'border: 1px solid blue; color: red; float: left;',
        ['color', 'float'],
        'color: red; float: left;'
    ),
    (
        'color: red; float: left; padding: 1em;',
        ['color', 'float'],
        'color: red; float: left;'
    ),
    (
        'color: red; float: left; padding: 1em;',
        ['color'],
        'color: red;'
    ),
    (
        'cursor: -moz-grab;',
        ['cursor'],
        'cursor: -moz-grab;'
    ),
    (
        'color: hsl(30,100%,50%);',
        ['color'],
        'color: hsl(30,100%,50%);'
    ),
    (
        'color: rgba(255,0,0,0.4);',
        ['color'],
        'color: rgba(255,0,0,0.4);'
    ),
    (
        "text-overflow: ',' ellipsis;",
        ['text-overflow'],
        "text-overflow: ',' ellipsis;"
    ),
    (
        'text-overflow: "," ellipsis;',
        ['text-overflow'],
        'text-overflow: "," ellipsis;'
    ),
    (
        'font-family: "Arial";',
        ['font-family'],
        'font-family: "Arial";'
    ),
])
def test_allowed_css(data, styles, expected):

    p_single = '<p style="{0!s}">bar</p>'
    p_double = "<p style='{0!s}'>bar</p>"

    if '"' in data:
        assert clean(p_double.format(data), styles=styles) == p_double.format(expected)
    else:
        assert clean(p_single.format(data), styles=styles) == p_single.format(expected)


def test_valid_css():
    """The sanitizer should fix missing CSS values."""
    styles = ['color', 'float']
    assert (
        clean('<p style="float: left; color: ">foo</p>', styles=styles) ==
        '<p style="float: left;">foo</p>'
    )
    assert (
        clean('<p style="color: float: left;">foo</p>', styles=styles) ==
        '<p style="">foo</p>'
    )


def test_style_hang():
    """The sanitizer should not hang on any inline styles"""
    style = [
        'margin-top: 0px;',
        'margin-right: 0px;',
        'margin-bottom: 1.286em;',
        'margin-left: 0px;',
        'padding-top: 15px;',
        'padding-right: 15px;',
        'padding-bottom: 15px;',
        'padding-left: 15px;',
        'border-top-width: 1px;',
        'border-right-width: 1px;',
        'border-bottom-width: 1px;',
        'border-left-width: 1px;',
        'border-top-style: dotted;',
        'border-right-style: dotted;',
        'border-bottom-style: dotted;',
        'border-left-style: dotted;',
        'border-top-color: rgb(203, 200, 185);',
        'border-right-color: rgb(203, 200, 185);',
        'border-bottom-color: rgb(203, 200, 185);',
        'border-left-color: rgb(203, 200, 185);',
        'background-image: initial;',
        'background-attachment: initial;',
        'background-origin: initial;',
        'background-clip: initial;',
        'background-color: rgb(246, 246, 242);',
        'overflow-x: auto;',
        'overflow-y: auto;',
        'font: italic small-caps bolder condensed 16px/3 cursive;',
        'background-position: initial initial;',
        'background-repeat: initial initial;'
    ]
    html = '<p style="%s">Hello world</p>' % ' '.join(style)
    styles = [
        'border', 'float', 'overflow', 'min-height', 'vertical-align',
        'white-space',
        'margin', 'margin-left', 'margin-top', 'margin-bottom', 'margin-right',
        'padding', 'padding-left', 'padding-top', 'padding-bottom',
        'padding-right',
        'background',
        'background-color',
        'font', 'font-size', 'font-weight', 'text-align', 'text-transform',
    ]

    expected = (
        '<p style="'
        'margin-top: 0px; '
        'margin-right: 0px; '
        'margin-bottom: 1.286em; '
        'margin-left: 0px; '
        'padding-top: 15px; '
        'padding-right: 15px; '
        'padding-bottom: 15px; '
        'padding-left: 15px; '
        'background-color: rgb(246, 246, 242); '
        'font: italic small-caps bolder condensed 16px/3 cursive;'
        '">Hello world</p>'
    )

    assert clean(html, styles=styles) == expected
