import re

from setuptools import setup, find_packages
from distutils.util import convert_path

install_requires = [
    'six',
    'html5lib>=0.999,<0.99999999',
]

try:
    from collections import OrderedDict  # noqa
except ImportError:
    # We don't use ordereddict, but html5lib does when you request
    # alpha-sorted attributes and on Python 2.6 and it doesn't specify it
    # as a dependency (see
    # https://github.com/html5lib/html5lib-python/pull/177)
    install_requires.append('ordereddict')


def get_long_desc():
    desc = open('README.rst').read()
    desc += open('CHANGES').read()
    return desc


def get_version():
    version_path = convert_path('bleach/version.py')
    with open(version_path) as version_file:
        for line in version_file:
            if line.startswith('VERSION = '):
                match = re.search(r'[(](\d+), (\d+), (\d+)[)]$', line)
                return '{0!s}.{1!s}.{2!s}'.format(
                    match.group(1),
                    match.group(2),
                    match.group(3)
                )


setup(
    name='bleach',
    version=get_version(),
    description='An easy whitelist-based HTML-sanitizing tool.',
    long_description=get_long_desc(),
    maintainer='Jannis Leidel, Will Kahn-Greene',
    url='http://github.com/mozilla/bleach',
    license='Apache Software License',
    packages=find_packages(),
    include_package_data=True,
    package_data={'': ['README.rst']},
    zip_safe=False,
    install_requires=install_requires,
    tests_require=[
        'nose>=1.3',
    ],
    test_suite='nose.collector',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
