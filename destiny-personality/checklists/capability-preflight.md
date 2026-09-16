# Capability Preflight Checklist

- [ ] Confirm the selected execution profile before inspecting capabilities.
- [ ] Confirm calculation configuration for that profile before discovery.
- [ ] For the strict profile, require complete calculation configuration and return `CONFIG_GAP` at `CALCULATION_CONFIG_CHECKED` when incomplete.
- [ ] For the controlled profile, require `CALCULATION_BASELINE_CHECKED`; classify each missing advanced asset as a required fatal dependency or a safely omitted `CONFIG_LIMITATION`.
- [ ] Discover available candidates for every required logical category. Do not install or connect anything.
- [ ] Build one capability descriptor for every candidate considered.
- [ ] Verify every applicable methodology setting with `schemas/compatibility-evidence.md`.
- [ ] Reject candidates lacking an immutable operation version or any exact setting match.
- [ ] Check independence before selecting a mandatory secondary candidate.
- [ ] Prefer a qualified local candidate.
- [ ] Obtain remote-data authorization for the current execution before sending case data.
- [ ] Invoke the selected capability only after every earlier applicable item passes.
- [ ] Preserve a calculation envelope before normalization.
- [ ] Validate the primary fact packet or controlled fact basis before deciding whether independent confirmation is required.
- [ ] In strict, check the comparison policy before any secondary invocation. In controlled inference, do not claim confirmation, correction, or resolution without that policy.
