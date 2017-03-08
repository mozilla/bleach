import re
import sys

from setuptools import setup, find_packages
from distutils.util import convert_path

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
    'html5lib>=0.99999999',
]


def get_long_desc():
    desc = open('README.rst').read()
    desc += '\n\n'
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
