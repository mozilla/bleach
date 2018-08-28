#!/bin/bash

# Install vendored packages into /tmp and then compare with what's in
# bleach/_vendor/.

DEST=/tmp/vendor-test

if [[ -e "${DEST}" ]]; then
    echo "${DEST} exists. Please remove."
    exit 1
fi

mkdir "${DEST}"

pip install --no-binary all --no-compile --no-deps -r bleach/_vendor/vendor.txt --target "${DEST}"

diff -r \
    --exclude="__init__.py" \
    --exclude="README.rst" \
    --exclude="vendor.txt" \
    --exclude="pip_install_vendor.sh" \
    --exclude="__pycache__" \
    bleach/_vendor/ "${DEST}"
