#!/usr/bin/python3

from setuptools import setup, find_packages

setup( name = 'bjarkan',
    version = '1.0',
    description = 'Bluetooth command line utility',
    long_description = open( 'README.md').read(),
    author = 'GetWellNetwork',
    license = 'BSD',
    url = 'https://github.com/willdeberry/bjarkan',
    packages = find_packages( exclude = ['contrib', 'docs', 'tests'] ),
    install_requires = [
        'pygobject>=3.18.2'
    ],
    entry_points = {
        'console_scripts': [
            'bjarkan = bjarkan.bjarkan:main'
        ],
    }
)
