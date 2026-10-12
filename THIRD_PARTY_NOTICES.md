# Third-Party Notices

The project source and Skill are released under the repository's MIT License.

## Runtime dependency

- **PyYAML** (`>=6,<7`) — YAML parsing; MIT License.
- **lunar_python** (`1.4.8`) — solar/lunar calendar and Four Pillars data;
  MIT License.
- **astronomy-engine** (`2.1.19`) — geocentric astronomical positions and
  sidereal time; MIT License.

## Development and test dependency

- **pytest** (`>=8,<9`) — test runner; MIT License. It is optional and is not a
  runtime dependency of the installed package.

## Explicitly not bundled

The wheel and Skill do not bundle Swiss Ephemeris or pyswisseph (their
AGPL/commercial dual-license terms are not silently adopted), native shared
libraries, fonts, proprietary text corpora, user birth data, or output from an
external calculation provider. The v0.7 local provider is pure Python and its
MIT-licensed runtime dependencies are declared above.
