# Semantic Snapshot Stability Design

**Date:** 2026-09-14  
**Status:** Approved by standing authorization  
**Scope:** Development CLI validation-to-fingerprint consistency only

## Problem

The semantic CLI currently validates YAML and then rereads the files to build
their fingerprint. A file changed in that interval could make the report bind
to bytes that were not accepted by the loaders.

## Decision

Use a conservative two-pass sequence:

1. load and validate the runtime and semantic bundle;
2. compute fingerprint A;
3. load and validate both sets again;
4. compute fingerprint B;
5. require A and B to be equal;
6. emit the second validation result with fingerprint B.

If either pass fails, preserve its existing `ConfigError`. If both validation
passes succeed but the fingerprints differ, return `CONFIG_VALUE_ERROR` with
the message `configuration files changed during validation; retry with an
immutable candidate snapshot`. The CLI emits no stdout on any failure.

This approach is preferred over advisory file locks, which are not a portable
trust boundary, and over refactoring every loader to consume a shared in-memory
byte snapshot, which would widen the change beyond the current need.

The files are small build-time configuration assets, so the second validation
pass is acceptable. No performance optimization is introduced.

## Boundaries

- The command remains read-only.
- No semantic values, approval records, or production assets are created.
- Stable bytes prove only which validated bytes produced the report.
- Human review and explicit project-owner approval remain independent.
- The distributable Skill does not invoke or depend on this CLI.

## Tests

- stable fingerprints cause two ordered validation passes and one success;
- different fingerprints return `CONFIG_VALUE_ERROR` and empty stdout;
- a first-pass loader failure still prevents all fingerprinting;
- existing `validate-config` behavior remains byte-for-byte compatible.

