from __future__ import unicode_literals

from functools import partial

import pytest

from bleach import clean


clean = partial(clean, tags=['p'], attributes=['style'])


@pytest.mark.parametrize('data, styles, expected', [
    (
        '<p style="font-family: Arial; color: red; float: left; background-color: red;">bar</p>',
        ['color'],
        '<p style="color: red;">bar</p>'
    ),
    (
        '<p style="border: 1px solid blue; color: red; float: left;">bar</p>',
        ['color'],
        '<p style="color: red;">bar</p>'
    ),
    (
        '<p style="border: 1px solid blue; color: red; float: left;">bar</p>',
        ['color', 'float'],
        '<p style="color: red; float: left;">bar</p>'
    ),
    (
        '<p style="color: red; float: left; padding: 1em;">bar</p>',
        ['color', 'float'],
        '<p style="color: red; float: left;">bar</p>'
    ),
    (
        '<p style="color: red; float: left; padding: 1em;">bar</p>',
        ['color'],
        '<p style="color: red;">bar</p>'
    ),
    # Handle leading - in attributes
    (
        '<p style="cursor: -moz-grab;">bar</p>',
        ['cursor'],
        '<p style="cursor: -moz-grab;">bar</p>'
    ),
    # Handle () in attributes
    (
        '<p style="color: hsl(30,100%,50%);">bar</p>',
        ['color'],
        '<p style="color: hsl(30,100%,50%);">bar</p>',
    ),
    (
        '<p style="color: rgba(255,0,0,0.4);">bar</p>',
        ['color'],
        '<p style="color: rgba(255,0,0,0.4);">bar</p>',
    ),
    # Handle ' in attributes
    (
        '<p style="text-overflow: \',\' ellipsis;">bar</p>',
        ['text-overflow'],
        '<p style="text-overflow: \',\' ellipsis;">bar</p>'
    ),
    # Handle " in attributes
    (
        '<p style=\'text-overflow: "," ellipsis;\'>bar</p>',
        ['text-overflow'],
        '<p style=\'text-overflow: "," ellipsis;\'>bar</p>'
    ),
    (
        '<p style=\'font-family: "Arial";\'>bar</p>',
        ['font-family'],
        '<p style=\'font-family: "Arial";\'>bar</p>'
    ),
    # Handle non-ascii characters in attributes
    (
        '<p style="font-family: \u30e1\u30a4\u30ea\u30aa; color: blue;">bar</p>',
        ['color'],
        '<p style="color: blue;">bar</p>'
    ),
])
def test_allowed_css(data, styles, expected):
    assert clean(data, styles=styles) == expected


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


@pytest.mark.parametrize('data, expected', [
    # No url--unchanged
    (
        '<p style="background: #00D;">foo</p>',
        '<p style="background: #00D;">foo</p>'
    ),

    # Verify urls with no quotes, single quotes, and double quotes are all dropped
    (
        '<p style="background: url(topbanner.png) #00D;">foo</p>',
        '<p style="background: #00D;">foo</p>'
    ),
    (
        '<p style="background: url(\'topbanner.png\') #00D;">foo</p>',
        '<p style="background: #00D;">foo</p>'
    ),
    (
        '<p style=\'background: url("topbanner.png") #00D;\'>foo</p>',
        '<p style="background: #00D;">foo</p>'
    ),

    # Verify urls with spacing
    (
        '<p style="background: url(  \'topbanner.png\') #00D;">foo</p>',
        '<p style="background: #00D;">foo</p>'
    ),
    (
        '<p style="background: url(\'topbanner.png\'  ) #00D;">foo</p>',
        '<p style="background: #00D;">foo</p>'
    ),
    (
        '<p style="background: url(  \'topbanner.png\'  ) #00D;">foo</p>',
        '<p style="background: #00D;">foo</p>'
    ),
    (
        '<p style="background: url (  \'topbanner.png\'  ) #00D;">foo</p>',
        '<p style="background: #00D;">foo</p>'
    ),

    # Verify urls with character entities
    (
        '<p style="background: url&#x09;(\'topbanner.png\') #00D;">foo</p>',
        '<p style="background: #00D;">foo</p>'
    ),

])
def test_urls(data, expected):
    assert clean(data, styles=['background']) == expected


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


@pytest.mark.parametrize('data, styles, expected', [
    (
        '<p style="font-family: Droid Sans, serif; white-space: pre-wrap;">text</p>',
        ['font-family', 'white-space'],
        '<p style="font-family: Droid Sans, serif; white-space: pre-wrap;">text</p>'
    ),
    (
        '<p style="font-family: &quot;Droid Sans&quot;, serif; white-space: pre-wrap;">text</p>',
        ['font-family', 'white-space'],
        '<p style=\'font-family: "Droid Sans", serif; white-space: pre-wrap;\'>text</p>'
    ),
])
def test_css_parsing_with_entities(data, styles, expected):
    """The sanitizer should be ok with character entities"""
    assert clean(data, tags=['p'], attributes={'p': ['style']}, styles=styles) == expected
