#!/usr/bin/env python

import os
import re

from setuptools import setup, find_packages


def get_long_desc():
    with open("README.rst", encoding="utf-8") as fp:
        desc = fp.read()
    desc += "\n\n"
    with open("CHANGES", encoding="utf-8") as fp:
        desc += fp.read()
    return desc


def get_version():
    fn = os.path.join("bleach", "__init__.py")
    vsre = r"""^__version__ = ['"]([^'"]*)['"]"""
    with open(fn, encoding="utf-8") as fp:
        version_file = fp.read()
    return re.search(vsre, version_file, re.M).group(1)


INSTALL_REQUIRES = [
    # html5lib requirements
    "six>=1.9.0",
    "webencodings",
]


EXTRAS_REQUIRE = {
    "css": [
        "tinycss2>=1.1.0,<1.2",
    ],
    "dev": [
        "pip-tools==6.5.1",
        "pytest==7.1.1",
        "flake8==4.0.1",
        "tox==3.24.5",
        "sphinx==4.3.2",
        "twine==4.0.0",
        "wheel==0.37.1",
        "hashin==0.17.0",
        "black==22.3.0; implementation_name == 'cpython'",
        "mypy==0.942; implementation_name=='cpython'",
    ],
}


setup(
    name="bleach",
    version=get_version(),
    description="An easy safelist-based HTML-sanitizing tool.",
    long_description=get_long_desc(),
    maintainer="Will Kahn-Greene",
    maintainer_email="willkg@mozilla.com",
    url="https://github.com/mozilla/bleach",
    license="Apache Software License",
    packages=find_packages(),
    include_package_data=True,
    package_data={"": ["README.rst"]},
    zip_safe=False,
    python_requires=">=3.7",
    install_requires=INSTALL_REQUIRES,
    extras_require=EXTRAS_REQUIRE,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
