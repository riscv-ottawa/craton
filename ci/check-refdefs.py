#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Check that every reference-style link label the book uses is defined in
docs/src/refs.md, and that every definition is used.

External links are written `[text][label]` or `[label][]`, with the URL defined
once in docs/src/refs.md and pulled into each page by `{{#include ./refs.md}}`.
mdBook renders an undefined label silently, as the literal text `[label]`, so a typo
will result as visible breakage with no build error. This script catches these.

Run from the repository root:

    python3 ci/check-refdefs.py

Exits non-zero if a used label has no definition, or if a definition is never used.
"""

import pathlib
import re
import sys

SRC = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path("docs/src")
REFS = SRC / "refs.md"

if not SRC.is_dir():
    sys.exit(f"book source not found at {SRC}")

# A definition line looks like:
#   [label]: https://example.com/...
defined = []
if REFS.is_file():
    for line in REFS.read_text().splitlines():
        m = re.match(r"^\[([^\]]+)\]:", line)
        if m:
            defined.append(m.group(1).strip().lower())
defined_set = set(defined)

# Match reference-style link usages. Both permitted forms end in a second pair
# of brackets, which is what makes them unambiguous:
#   [text][label]   -> label is group 2
#   [label][]       -> label is group 2 is empty, so group 1
# Inline links, images and alert markers cannot match, since none of them is
# followed by `[`. Inline code can, so it is stripped: a fenced example is
# skipped by the caller, but `[text][label]` written inline is not an occurrence.
USAGE = re.compile(r"\[([^\]]+)\]\[([^\]]*)\]")
INLINE_CODE = re.compile(r"`[^`]*`")

used = {}  # label -> ["file:line", ...]


def strip_noise(line):
    return INLINE_CODE.sub("", line)


for md in sorted(SRC.rglob("*.md")):
    if md == REFS:
        continue
    in_fence = False
    for i, raw in enumerate(md.read_text().splitlines(), 1):
        stripped = raw.strip()
        if stripped.startswith(("```", "~~~")):
            in_fence = not in_fence
            continue
        if in_fence or stripped.startswith("{{#include"):
            continue
        for m in USAGE.finditer(strip_noise(raw)):
            label = (m.group(2) or m.group(1)).strip().lower()
            if label:
                used.setdefault(label, []).append(f"{md.relative_to(SRC)}:{i}")

undefined = {label: at for label, at in used.items() if label not in defined_set}
unused = [label for label in defined if label not in used]

status = 0
if undefined:
    print(f"Undefined reference labels ({len(undefined)}):")
    for label in sorted(undefined):
        print(f"  [{label}]  used at {', '.join(undefined[label])}")
    print(f"\nAdd definitions to {REFS}, or fix the typo.")
    status = 1

if unused:
    print(f"Defined-but-unused labels in {REFS} ({len(unused)}):")
    for label in sorted(unused):
        print(f"  [{label}]")
    print("\nRemove dead entries, or they drift from what the book actually links.")
    status = 1

if not status:
    print(
        f"OK: {len(used)} labels used across the book, "
        f"{len(defined_set)} defined in {REFS}, all resolve."
    )
sys.exit(status)
