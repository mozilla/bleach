#!/usr/bin/env python

import io
import os
import re

from setuptools import setup, find_packages


install_requires = [
    'packaging',
    'six>=1.9.0',
    # html5lib requirements
    'webencodings',
]


def get_long_desc():
    with io.open('README.rst', encoding='utf-8') as fp:
        desc = fp.read()
    desc += '\n\n'
    with io.open('CHANGES', encoding='utf-8') as fp:
        desc += fp.read()
    return desc


def get_version():
    fn = os.path.join('bleach', '__init__.py')
    vsre = r"""^__version__ = ['"]([^'"]*)['"]"""
    with io.open(fn, encoding='utf-8') as fp:
        version_file = fp.read()
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
    python_requires='>=3.6',
    install_requires=install_requires,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
