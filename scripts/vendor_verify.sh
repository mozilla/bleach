#!/bin/bash

# Install vendored packages into /tmp and then compare with what's in
# bleach/_vendor/.

DEST=/tmp/vendor-test

if [[ -e "${DEST}" ]]; then
    echo "${DEST} exists. Please remove."
    exit 1
fi

mkdir "${DEST}"

# Get versions of pip and python
pip --version

# Install vendored dependencies into temp directory
pip install --no-binary all --no-compile --no-deps -r bleach/_vendor/vendor.txt --target "${DEST}"

# Diff contents of temp directory and bleach/_vendor/ excluding vnedoring
# infrastructure
diff -r \
    --exclude="__init__.py" \
    --exclude="README.rst" \
    --exclude="vendor.txt" \
    --exclude="pip_install_vendor.sh" \
    --exclude="__pycache__" \
    bleach/_vendor/ "${DEST}"

# If everything is cool, then delete the temp directory
if [ $? == 0 ]; then
    rm -rf "${DEST}"
fi
