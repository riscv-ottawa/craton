# Project Craton

Craton is an RV32 microcontroller for real-time and RTOS workloads: a system on chip (SoC) with a fork of the OpenHW Foundation CORE-V CV32E40X at its heart.
The design targets FPGA(s) for validation only and then silicon as the end goal.

## About this repository

Everything for Project Craton lives in this repo: the RTL, verification environment, software, FPGA and physical design flows, and the documentation book.
The external dependencies under `deps/` are the exception.
For example, Craton forks the CV32E40X and its design-verification environment into repositories of their own, then pins both here under `deps/`.

Things under `deps/` are git submodules, so clone with `git clone --recurse-submodules`, or run `git submodule update --init` in a clone you already have.

You may notice nothing much else is here yet in this repo.
This repository currently holds licensing, the contribution policy, a documentation shell, and the two pinned forks.
The rest will be added here as progress is made.

## Documentation

`docs/` is an [mdBook](https://github.com/rust-lang/mdBook), published to GitHub Pages.
Build it locally with `mdbook serve docs`.

## License

Hardware is under the Solderpad Hardware License v2.1, in `LICENSE.hardware`, and software, tooling and documentation under Apache-2.0, in `LICENSE.software`.
Every source file declares which of the two applies with an SPDX identifier, and [CONTRIBUTING.md](CONTRIBUTING.md) gives the path-by-path rule (which is enforced by CI).

The core this project forks, the CORE-V CV32E40X, is under the Solderpad Hardware License v0.51, and the fork keeps those terms in its own repository.

## Contributing

Contributions must arrive as pull requests, carry a Developer Certificate of Origin sign-off, and require one approving review after CI checks pass.
See [CONTRIBUTING.md](CONTRIBUTING.md), and [MAINTAINERS.md](MAINTAINERS.md) for who reviews.
