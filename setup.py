#!/usr/bin/python3

import os
from setuptools import setup, find_packages
import sys

sys.path.insert( 0, os.path.abspath( '.' ) )
import bjarkan

setup(
    name = bjarkan.__title__,
    version = bjarkan.__version__,
    description = bjarkan.__description__,
    long_description = open( 'README.rst' ).read(),
    keywords = 'bluez bluetooth cli',
    author = bjarkan.__author__,
    author_email = bjarkan.__author_email__,
    license = bjarkan.__copyright__,
    url = 'https://github.com/willdeberry/bjarkan',
    download_url = 'https://github.com/willdeberry/bjarkan',
    packages = find_packages( exclude = ['contrib', 'sphinx', 'docs', 'tests'] ),
    entry_points = {
        'console_scripts': [
            'bjarkan = bjarkan.cli:main'
        ],
    },
    classifiers = [
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators'
    ]
)
