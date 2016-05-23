from setuptools import setup, find_packages

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

setup(
    name='bleach',
    version='1.4.3',
    description='An easy whitelist-based HTML-sanitizing tool.',
    long_description=open('README.rst').read(),
    author='James Socol',
    author_email='me@jamessocol.com',
    url='http://github.com/jsocol/bleach',
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
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
