# This file only contains a selection of the most common options. For a full
# list see the documentation:
#
# https://www.sphinx-doc.org/en/master/usage/configuration.html


# -- Path setup --------------------------------------------------------------

import os
import sys

# Add parent directory so we can import bleach
sys.path.insert(0, os.path.abspath('..'))

import bleach  # noqa

# -- Project information -----------------------------------------------------

project = "Bleach"
copyright = "2012-2015, James Socol; 2015-2017, Mozilla Foundation"
author = "Mozilla Foundation"


# -- General configuration -----------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ['sphinx.ext.autodoc', 'sphinx.ext.viewcode', 'sphinx.ext.doctest']

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build']

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.
version = bleach.__version__
# The full version, including alpha/beta/rc tags.
release = bleach.__version__ + ' ' + bleach.__releasedate__

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# Display the class docstring and __init__ docstring concatenated
autoclass_content = 'both'
# Reduce complexity of function signatures by not evaluating the argument
# default values.
# NOTE(willkg) This is experimental in Sphinx 4.
autodoc_preserve_defaults = True


# -- Options for HTML output ---------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
html_theme = 'alabaster'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# Custom sidebar templates, maps document names to template names.
html_sidebars = {
    '**': [
        'about.html',
        'navigation.html',
        'relations.html',
        'searchbox.html',
    ]
}
