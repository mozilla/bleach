#!/bin/bash

BLEACH_VENDOR_DIR=${BLEACH_VENDOR_DIR:-"."}
DEST=${DEST:-"."}

pip install --no-binary all --no-compile --no-deps -r "${BLEACH_VENDOR_DIR}/vendor.txt" --target "${DEST}"
