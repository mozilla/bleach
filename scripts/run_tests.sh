#!/bin/bash

# Make sure we're running from the bleach repository directory and
# not this directory.
THISDIR=$(basename `pwd`)
if [[ "${THISDIR}" == "scripts" ]]; then
    cd ..
fi

MODE=${1:-test}

case "${MODE}" in
  test)
    pytest
    ;;
  lint)
    flake8 setup.py tests/ bleach/ tests_website/
    ;;
  vendorverify)
    ./scripts/vendor_verify.sh
    ;;
  docs)
    tox -e docs
    ;;
  format)
    black --target-version=py37 --exclude=_vendor setup.py bleach/ tests/ tests_website/
    ;;
  format-check)
    black --target-version=py37 --check --diff --exclude=_vendor setup.py bleach/ tests/ tests_website/
    ;;
  check-reqs)
    python -m venv ./tmpvenv/
    ./tmpvenv/bin/pip install -U pip
    ./tmpvenv/bin/install '.[dev]'
    ./tmpvenv/bin/pip list -o
    rm -rf ./tmpvenv/
    ;;
  *)
    echo "Unknown mode $MODE."
    exit 1
esac
