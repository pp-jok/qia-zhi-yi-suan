# Capability Descriptor Contract

Discovery is not qualification. Create one descriptor for every available candidate considered in the current execution.

## Required fields

`schema_version`, `candidate_id`, `category`, `name`, `interface_type`, `operation`, `immutable_version`, `locality`, `availability`, `authorization_state`, `required_input_fields`, `returned_fields`, `supported_settings`, `engine_lineage`, `independence_status`, `qualification_status`, and `rejection_reasons` are required.

`category` is `time_normalization`, `bazi`, or `astrology`. `locality` is `local` or `remote`. An unknown `immutable_version` cannot pass qualification. `independence_status` is `independent`, `shared_lineage`, or `unverified`. `qualification_status` is `discovered`, `qualified`, `rejected`, or `blocked_authorization`.

## Independence

Different product names do not prove independence. A mandatory secondary result requires `independent`; `shared_lineage` and `unverified` do not pass.

## Boundary

Describe only capabilities already available to the agent. Do not install software, connect a service, or inspect unrelated projects to complete a descriptor.
