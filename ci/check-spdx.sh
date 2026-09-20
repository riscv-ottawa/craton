#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
#
# Checks that every source file declares its license, and declares the right one:
# Solderpad v2.1 for hardware, Apache-2.0 for everything else. Markdown is
# covered by the table in CONTRIBUTING.md, and everything under deps/ keeps its own license.

set -euo pipefail

status=0

# Solderpad v2.1 is an SPDX exception rather than a license of its own, so the
# hardware identifier is the expression the license's own appendix prescribes.
expected() {
  case "$1" in
    rtl/*|pd/*|fpga/*) echo "Apache-2.0 WITH SHL-2.1" ;;
    *) echo "Apache-2.0" ;;
  esac
}

checkable() {
  case "$1" in
    deps/*|LICENSE*) return 1 ;;
  esac
  case "$1" in
    *.sv|*.svh|*.v|*.vh|*.sdc|*.xdc|*.tcl|*.py|*.sh|*.rs|*.c|*.h|*.S|*.ld|\
    *.yml|*.yaml|*.toml|*.mk|Makefile|Dockerfile|*/Dockerfile) return 0 ;;
    *) return 1 ;;
  esac
}

while read -r file; do
  checkable "$file" || continue
  want="$(expected "$file")"
  got="$(grep -m1 -oE 'SPDX-License-Identifier:.*' "$file" \
         | sed -E 's/^SPDX-License-Identifier:[[:space:]]*//
                   s@[[:space:]]*(\*/|-->|\*)?[[:space:]]*$@@' || true)"
  if [ -z "$got" ]; then
    echo "no SPDX identifier: $file (expected $want)"
    status=1
  elif [ "$got" != "$want" ]; then
    echo "wrong SPDX identifier: $file declares $got, expected $want"
    status=1
  fi
done < <(git ls-files)

exit "$status"
