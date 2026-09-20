#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
#
# Build the book, and fail if mdBook complains about something.
# Usage: ci/check-book.sh [<book dir>]   (default docs)

set -euo pipefail

book="${1:-docs}"
log="$(mktemp)"
trap 'rm -f "${log}"' EXIT

mdbook build "${book}" 2>&1 | tee "${log}"

if grep -qE '^[[:space:]]*ERROR' "${log}"; then
  echo
  echo "mdbook logged the errors above and still exited 0; the book is not clean."
  exit 1
fi
