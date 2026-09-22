# Qualified Facts Runtime Hardening v0.3.7

## Frozen semantic boundary

This release changes no Primitive, mapping, state resolver, alignment,
calibration, holdout, or production authorization. Core Profile remains a
candidate `primitive_only` preview.

## Public facts route

`build-core-profile` accepts only a qualified `deterministic-facts-v1` packet.
It requires non-empty provenance and passed `structure`, `methodology`,
`provenance`, `internal_consistency`, `time_scope`, and
`independent_comparison` validation results. Envelope fact mode and methodology
versions must agree with the normalized fact content.

The CLI derives `project_verified` assurance after this qualification gate.
It exposes no caller-selected assurance parameter. The internal chart-facts
codec remains an adapter/test transport and is not a public qualification
contract.

## Presentation and fact scope

Compound context scopes are localized tag by tag, so `pressure+work` renders as
`压力情境、工作与任务推进` without leaking internal keys. Known birth time and
hour-pillar availability are independent facts: a time-sensitive packet may
omit an hour pillar, while a stable-only packet may not contain one.

## Freeze condition

The qualified facts route, fact scope, direction matrix, summary schema, birth
mode vocabulary, package verification, and CI form the frozen Core Portrait
baseline. Signature and all higher semantic layers remain disabled pending a
separate product review.
