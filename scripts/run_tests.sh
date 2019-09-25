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
    pytest ;;
  lint)
    flake8 bleach/ ;;
  vendorverify)
    ./scripts/vendor_verify.sh ;;
  docs)
    tox -e docs ;;
  *)
    echo "Unknown mode $MODE."
    exit 1
esac
