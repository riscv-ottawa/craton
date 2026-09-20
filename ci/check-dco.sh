#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
#
# Every commit must contain a Developer Certificate of Origin sign-off.
# Usage: ci/check-dco.sh [<range>]   (default origin/main..HEAD)

set -euo pipefail

range="${1:-origin/main..HEAD}"
status=0

while read -r sha; do
  [ -n "$sha" ] || continue
  if ! git show -s --format=%B "$sha" | grep -qiE '^Signed-off-by: .+ <.+@.+>'; then
    echo "no sign-off: $sha $(git show -s --format=%s "$sha")"
    status=1
  fi
done < <(git rev-list "$range")

if [ "$status" -ne 0 ]; then
  echo
  echo "Add one with 'git commit -s', or 'git rebase --signoff $range' for a branch."
fi

exit "$status"
