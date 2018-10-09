#!/usr/bin/env python

import codecs
import os
import re
import sys

from setuptools import setup, find_packages


setup_requires = []
if 'test' in sys.argv:
    # Only add pytest-runner to setup_requires if running tests
    setup_requires.append('pytest-runner>=2.0,<3dev')

tests_require = [
    'pytest>=3.0.0',
]

install_requires = [
    'six',
    # html5lib requirements
    'webencodings',
]


def get_long_desc():
    desc = codecs.open('README.rst', encoding='utf-8').read()
    desc += '\n\n'
    desc += codecs.open('CHANGES', encoding='utf-8').read()
    return desc


def get_version():
    fn = os.path.join('bleach', '__init__.py')
    vsre = r"""^__version__ = ['"]([^'"]*)['"]"""
    version_file = codecs.open(fn, mode='r', encoding='utf-8').read()
    return re.search(vsre, version_file, re.M).group(1)


setup(
    name='bleach',
    version=get_version(),
    description='An easy safelist-based HTML-sanitizing tool.',
    long_description=get_long_desc(),
    maintainer='Will Kahn-Greene',
    maintainer_email='willkg@mozilla.com',
    url='https://github.com/mozilla/bleach',
    license='Apache Software License',
    packages=find_packages(),
    include_package_data=True,
    package_data={'': ['README.rst']},
    zip_safe=False,
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*',
    install_requires=install_requires,
    setup_requires=setup_requires,
    tests_require=tests_require,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
