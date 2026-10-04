# Third-Party Notices

The project source and Skill are released under the repository's MIT License.

## Runtime dependency

- **PyYAML** (`>=6,<7`) — YAML parsing; MIT License.

## Development and test dependency

- **pytest** (`>=8,<9`) — test runner; MIT License. It is optional and is not a
  runtime dependency of the installed package.

## Explicitly not bundled

The wheel and Skill do not bundle Swiss Ephemeris, pyswisseph, another chart
calculator, native shared libraries, fonts, proprietary text corpora, user
birth data, or output from an external calculation provider. The Skill directs
the executing agent to discover and invoke an authorized external calculation
capability; that capability is not redistributed by this project.
