# Changelog

All notable changes to forge are documented here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and versions follow [Semantic Versioning](https://semver.org/).

## [0.1.0] - 2026-10-15

### Added
- Four skills forming the flow `define → plan → build → verify`.
- Per-project working language (`Working language:` in `CLAUDE.md`): skills are written in English and talk and write artifacts in the project's language.
- Living functional docs: `build` consolidates each closed feature into `docs/functional/<domain>.md`. `define`, `plan` and `verify` read them as the source of truth for current behavior.
- Close sequence in `build`: closing commit, consolidation gate, and removal of the work folder, recoverable from git.
- Documentation (`docs/`) and a complete fictional example (`examples/volume-discount/`).
