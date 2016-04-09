#!/usr/bin/python3

from setuptools import setup, find_packages

setup( name = 'bjarkan',
    version = '1.1.0',
    description = 'Bluetooth command line utility',
    long_description = open( 'README.rst' ).read(),
    keywords = 'bluez bluetooth cli',
    author = 'GetWellNetwork',
    author_email = 'willdeberry@gmail.com',
    maintainer = 'Will DeBerry',
    maintainer_email = 'willdeberry@gmail.com',
    license = 'Copyright 2016 GetWellNetwork, Inc., BSD copyright and disclaimer apply',
    url = 'https://github.com/willdeberry/bjarkan',
    download_url = 'https://github.com/willdeberry/bjarkan',
    packages = find_packages( exclude = ['contrib', 'docs', 'tests'] ),
    install_requires = [
        'pygobject>=3.18.2'
    ],
    entry_points = {
        'console_scripts': [
            'bjarkan = bjarkan.bjarkan:main'
        ],
    },
    classifiers = [
        'Programming Language :: Python',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators'
    ]
)
