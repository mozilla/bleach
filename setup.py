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
    # >= 8 9s because of breaking API change
    # the 'pre' suffix is needed for supporting '1.0b*' versions
    'html5lib>=0.99999999pre,!=1.0b1,!=1.0b2,!=1.0b3,!=1.0b4,!=1.0b5,!=1.0b6,!=1.0b7,!=1.0b8',
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
    url='http://github.com/mozilla/bleach',
    license='Apache Software License',
    packages=find_packages(),
    include_package_data=True,
    package_data={'': ['README.rst']},
    zip_safe=False,
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
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
