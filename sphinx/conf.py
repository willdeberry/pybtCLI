#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# https://wwoods.github.io/2016/06/09/easy-sphinx-documentation-without-the-boilerplate/
# was immensely helpful *and should be the fucking out-of-the-box default experience* when
# turning on autodoc and autosummary

# http://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html
# for API docstring formatting

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.

import os
import sys

sys.path.insert( 0, os.path.abspath( '..' ) )

import bjarkan

language = None

project = bjarkan.__title__
copyright = bjarkan.__copyright__
author = bjarkan.__author__
version = bjarkan.__version__
release = version

templates_path = [ '_templates' ]
exclude_patterns = [ '_templates' ]
source_suffix = '.rst'
master_doc = project
pygments_style = 'sphinx'
todo_include_todos = False


extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.napoleon'
]

autoclass_content = 'class'
autodoc_member_order = 'bysource'
autodoc_default_flags = [
    'members', # include non-private members
    'undoc-members', # include members without a docstring
    #'private-members', # include _private and __private
    #'special-members', # include __special__ members
    #'inherited-members', # include members inherited from the base class
    'show-inheritance', # include the inheritance hierarchy of a class
]

autodoc_mock_imports = [
    'dbus',
    'dbus.mainloop.glib',
    'dbus.mainloop.glib.DBusGMainLoop',
    'dbus.service',
    'gi.repository',
    'gi.repository.GObject',
]

autosummary_generate = True

napoleon_numpy_docstring = False  # Force consistency, leave only Google
napoleon_use_rtype = False    # More legible

html_theme = 'sphinx_rtd_theme'

