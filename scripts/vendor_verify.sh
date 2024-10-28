#!/bin/bash

set -e

# Install vendored packages into /tmp and then compare with what's in
# bleach/_vendor/.

export DEST=/tmp/vendor-test
export BLEACH_VENDOR_DIR=bleach/_vendor

if [[ -e "${DEST}" ]]; then
    echo "${DEST} exists. Please remove."
    exit 1
fi

mkdir "${DEST}"

# Get diagnostic information
pip --version
echo "DEST: ${DEST}"
echo "BLEACH_VENDOR_DIR: ${BLEACH_VENDOR_DIR}"

# Copy patch files to dest directory
cp bleach/_vendor/*.patch "${DEST}"

# Install vendored dependencies into temp directory
bleach/_vendor/vendor_install.sh

# Diff contents of temp directory and bleach/_vendor/ excluding vendoring
# infrastructure
echo "diffing directory trees..."
diff -r \
    --exclude="__init__.py" \
    --exclude="README.rst" \
    --exclude="vendor.txt" \
    --exclude="vendor_install.sh" \
    --exclude="__pycache__" \
    --exclude="RECORD" \
    bleach/_vendor/ "${DEST}"

# Go through all RECORD files and compare sorted versions; RECORD files are
# unsorted and occasionally diff poorly
for fn in $(cd bleach/_vendor/; find . -name RECORD); do
    echo "diffing bleach/_vendor/${fn} and ${DEST}/${fn} ..."
    diff <(sort bleach/_vendor/${fn}) <(sort ${DEST}/${fn})
done

# If everything is cool, then delete the temp directory
LASTEXIT=$?
if [ ${LASTEXIT} -eq 0 ]; then
    rm -rf "${DEST}"
fi

exit ${LASTEXIT}
