from setuptools import setup

setup(
    name='bleach',
    version='0.3.1',
    description='An easy whitelist-based HTML-sanitizing tool.',
    long_description=open('README.rst').read(),
    author='James Socol',
    author_email='james@mozilla.com',
    url='http://github.com/jsocol/bleach',
    license='BSD',
    packages=['bleach'],
    include_package_data=True,
    package_data = { '': ['README.rst'] },
    zip_safe=False,
    install_requires=['html5lib'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Environment :: Web Environment :: Mozilla',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
