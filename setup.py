#!/usr/bin/python3

from setuptools import setup, find_packages

setup( name = 'bjarkan',
    version = '1.1.9',
    description = 'Bluetooth command line utility',
    long_description = open( 'README.rst' ).read(),
    keywords = 'bluez bluetooth cli',
    author = 'GetWellNetwork',
    author_email = 'willdeberry@gmail.com',
    license = 'Copyright 2016 GetWellNetwork, Inc., BSD copyright and disclaimer apply',
    url = 'https://github.com/willdeberry/bjarkan',
    download_url = 'https://github.com/willdeberry/bjarkan',
    packages = find_packages( exclude = ['contrib', 'docs', 'tests'] ),
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
