# Contributing to Craton

Craton is an RV32 microcontroller for real-time and RTOS workloads, built in the open.
Every change to it is reviewed before merging.
This document covers how a change is made, what it has to contain, and how it gets into `main`.

## How to make changes

In summary: fork the repository, work on a branch, and open a pull request.

A pull request merges when it has one approving review and its CI checks pass.
The maintainers who can give reviews are listed in [MAINTAINERS.md](MAINTAINERS.md).

If possible, split large changes into smaller commits that each do one thing.
Write the subject as `<type>(<scope>): <description>` and separate it from the body with a blank line.
The `<type>` is one of `feat`, `fix`, `refactor`, `test`, `docs` or `chore`, and `<scope>` names the block or directory the change touches.

Here are some contrived examples, for reference:

```
feat(dma): add descriptor fetch to the frontend
fix(soc): correct debug port reset polarity
test(dma): cover unaligned descriptor lengths
docs(pd): record the post-route hold result
chore(deps): bump the CV32E40X fork to 3a1f9c2
```

In each pull request, make sure to clearly state what the change(s) do and what you tested/verified.
If the checks pass locally, say so; if you ran a simulation or a flow, show the output; if something is done but has not been run or tested, say that rather than leaving a reviewer to assume that it has.

## Sign your work

Every commit carries a `Signed-off-by` line, which `git commit -s` adds for you.
The line certifies that you wrote the change or otherwise have the right to submit it under this repository's licenses, and it is the Developer Certificate of Origin 1.1, published at <https://developercertificate.org/>.
There is no contributor license agreement and no copyright assignment.

Taking one of the examples from above, a complete commit message would become:

```
chore(deps): bump the CV32E40X fork to 3a1f9c2

Lorem ipsum dolor sit amet consectetur adipiscing elit.
Doloribus ipsam ab aliquam quia odit deleniti consequatur.
Ducimus ut corporis minima.

Signed-off-by: Your Name <you@example.com>
```

A commit without a sign-off will be denied by CI.

## Licenses and SPDX

Hardware is licensed under the Solderpad Hardware License v2.1 and everything else under Apache-2.0.

| Path                                        | License               | SPDX identifier           |
| ------------------------------------------- | --------------------- | ------------------------- |
| `rtl/`, `pd/`, `fpga/`                      | Solderpad v2.1        | `Apache-2.0 WITH SHL-2.1` |
| `sw/`, `dv/`, `ci/`, `containers/`, `docs/` | Apache-2.0            | `Apache-2.0`              |
| `deps/`                                     | each dependency's own | unchanged, do not edit    |

Every new source file declares its license on one of its first lines:

```systemverilog
// SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1
```

```python
# SPDX-License-Identifier: Apache-2.0
```

A file that declares nothing or a license that the table above does NOT define will be denied by CI.
The only exception is for markdown files, which are just covered by the table above instead of per-file headers.
Files under `deps/` must keep the terms they already have, do not edit them.

## Where things go

| Directory     | What belongs there                                                                                          |
| ------------- | ----------------------------------------------------------------------------------------------------------- |
| `rtl/`        | RTL the project writes: the interrupt controller, the SoC, the DMA frontend, the peripherals, the top level |
| `dv/`         | the tandem testing, regression, assertions, and covergroups                                                 |
| `sw/`         | boot ROM, test programs, and RTOS bring-up                                                                  |
| `fpga/`       | board configuration, wrappers, and constraints                                                              |
| `pd/`         | the physical flow, floorplan, constraints, and the layout consistency check                                 |
| `containers/` | container image definitions, there will be at least one for simulation and one for the physical flow        |
| `deps/`       | external sources, pinned as submodules                                                                      |
| `docs/`       | the documentation/book                                                                                      |
| `ci/`         | continuous integration scripts                                                                              |

Craton forks the CORE-V CV32E40X in a repository of its own, kept up-to-date and rebased on upstream, and pins it here under `deps/`.
A change to the core belongs in the fork, not in this tree.

## Style

RTL follows the [lowRISC Verilog style guide](https://github.com/lowRISC/style-guides/blob/master/VerilogCodingStyle.md).

For writing documentation, code comments, commit messages, pull requests, and reviews: write plainly and directly, state facts, and give justification where needed.
Drafting with an AI tool is fine, but the result is still fully yours, so read every line and rewrite what you would not have otherwise written.
Remember, the required sign-off will say YOU take responsibility for the change.

## Documentation

`docs/` is an mdBook, and its source tree mirrors the repo source itself: `docs/src/rtl/`, `docs/src/dv/`, `docs/src/pd/`, `docs/src/fpga/` and `docs/src/sw/` document the directories they are named after, exceptions being made for `docs/src/getting-started/` and `docs/src/project/`.

For each component or hardware block, it is recommended to provide the following small set of pre-defined pages at the very least:

| Page                     | What it carries                                                            |
| ------------------------ | -------------------------------------------------------------------------- |
| `README.md`              | what the block is, the features it has, and a paragraph describing it      |
| `theory-of-operation.md` | how it works and why it is built that way, ideally with a block diagram    |
| `programmers-guide.md`   | how to drive it: initialization sequences, worked examples, error handling |
| `interfaces.md`          | the ports, parameters and interrupts it presents to an integrator          |
| `registers.md`           | its register map                                                           |

You may find inspiration on style and format from the [Diátaxis](https://diataxis.fr/) method.
Documentation that spans multiple blocks rather than a single one generally goes under `docs/src/project/`.

Each new page must be added to `docs/src/SUMMARY.md`. Read the [mdBook documentation](https://rust-lang.github.io/mdBook/) for more information.

For actual writing, try your best to write one sentence per line, avoiding line breaks mid-sentence.
This greatly helps when it comes time to code review.

External links are written [reference-style](https://www.markdownlang.com/basic/links.html#reference-style-links), with URLs defined once centrally in `docs/src/refs.md` as `[label]: https://example.com/`.

Each page using label(s) must end with the include that lets mdBook resolve them:

```
{{#include ./refs.md}}        # from docs/src/*.md
{{#include ../refs.md}}       # from docs/src/<part>/*.md
```

Try your best to reuse existing labels rather than defining duplicates.

## Definition of done

A change is ready to merge when:

- Checks (e.g., those under `ci/`) relating to the specific change pass locally and in CI.
- Every commit is signed off, and every new source file declares an appropriate license.
- Every technical claim relates or directly references real source code or specification section.
- New doc pages are listed in `docs/src/SUMMARY.md`, and new external links are defined in `docs/src/refs.md`.
- The pull request says what the change does, what was verified, and what was not.
