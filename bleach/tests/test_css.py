from functools import partial

from nose.tools import eq_

from bleach import clean


clean = partial(clean, tags=['p'], attributes=['style'])


def test_allowed_css():
    tests = (
        ('font-family: Arial; color: red; float: left; '
         'background-color: red;', 'color: red;', ['color']),
        ('border: 1px solid blue; color: red; float: left;', 'color: red;',
         ['color']),
        ('border: 1px solid blue; color: red; float: left;',
         'color: red; float: left;', ['color', 'float']),
        ('color: red; float: left; padding: 1em;', 'color: red; float: left;',
         ['color', 'float']),
        ('color: red; float: left; padding: 1em;', 'color: red;', ['color']),
        ('cursor: -moz-grab;', 'cursor: -moz-grab;', ['cursor']),
    )

    p = '<p style="%s">bar</p>'

    def check(input, output, styles):
        eq_(p % output, clean(p % input, styles=styles))

    for i, o, s in tests:
        yield check, i, o, s


def test_valid_css():
    """The sanitizer should fix missing CSS values."""
    styles = ['color', 'float']
    eq_('<p style="float: left;">foo</p>',
        clean('<p style="float: left; color: ">foo</p>', styles=styles))
    eq_('<p style="">foo</p>',
        clean('<p style="color: float: left;">foo</p>', styles=styles))
