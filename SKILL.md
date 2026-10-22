---
name: lab-instrument-host-dev
description: Develop, debug, and release host-PC software for laboratory instruments involving vendor SDKs, serial or network transports, motion axes, cameras, autofocus, calibration, scanning, and post-processing. Use when integrating or repairing instrument control software; omit for generic desktop GUI work with no hardware interaction.
metadata:
  short-description: Build safe, maintainable lab instrument control software
---

# Lab Instrument Host Development

## Desired Outcome

Produce instrument software that a lab can operate safely and reproduce from
source: correct device sequences, explicit calibration semantics, observable
errors, deterministic tests, and releases that cannot be confused with older
builds.

## Non-Negotiables

- Treat motion, illumination, lasers, heaters, and actuators as potentially
  hazardous. Prefer read-only discovery before enable, enable before motion,
  and small bounded motion before homing or scanning.
- Verify behavior against the installed SDK and the customer's working
  executable. Do not invent protocol details, enum values, node types, retries,
  or coordinate signs.
- Separate discovery, device access, sequencing, GUI state, and post-processing.
  A GUI callback must not become the owner of a hardware state machine.
- Never claim hardware validation when the device is absent. State the exact
  evidence level: source inspection, mock test, offline UI test, or real device.
- Preserve working user data and calibrations. Save units, axis mapping, and
  provenance; use explicit schema versions and migrations.

## Workflow

1. **Define acceptance evidence.** Identify the instrument, transport, axes,
   outputs, user workflow, and what can be physically damaged. Separate software
   acceptance from hardware acceptance.
2. **Inventory authoritative artifacts.** Inspect vendor headers, export tables,
   sample applications, configuration files, logs, and any known-working host
   executable before changing call sequences.
3. **Recover the working behavior.** For opaque executables, inspect packaged
   modules, imported DLL functions, symbolic names, UI strings, and logs. Write
   down the observed state and call sequence. Reproduce that baseline before
   adding convenience behavior.
4. **Map the device contract.** Record address and transport, device identity,
   enum capabilities, value ranges, units, axis and I/O mapping, command return
   semantics, timeouts, and recovery behavior.
5. **Design the layers.** Use transport -> SDK adapter -> instrument service ->
   orchestration -> GUI. Expose typed operations and machine-readable errors.
6. **Bring hardware up incrementally.** Use the ladder in
   [references/device-bringup.md](references/device-bringup.md).
7. **Implement motion and imaging explicitly.** Apply the invariants in
   [references/motion-camera-integration.md](references/motion-camera-integration.md).
8. **Validate without and then with hardware.** Use recorded SDK mocks and
   contract tests as described in
   [references/testing-and-data.md](references/testing-and-data.md).
9. **Release immutably.** Follow
   [references/release-management.md](references/release-management.md) and run
   `scripts/check_release.py` before delivery.

## Engineering Rules

### Device Access

- Keep one command owner per physical instrument. Serialize access with a lock
  at the device service, not in scattered callbacks.
- Check every SDK return code. Preserve raw codes and contextual messages in the
  log; avoid collapsing failures into a generic boolean.
- Use bounded polling with a deadline. Do not replace a verified wait with
  arbitrary sleep except where the vendor sequence explicitly requires it.
- Keep an emergency-stop path independent of normal worker queues when the SDK
  provides one.

### Reference-Program Alignment

- When the user asks for exact compatibility, make the known-working sequence
  the baseline. Do not add retries, alternate absolute-position recovery,
  current-position shortcuts, or extra initialization unless evidence requires
  it.
- Compare initialization frequency, wait timing, error recovery, and parameter
  writes, not just function names.
- Record why each deviation exists. "Cleaner code" is not a reason to alter a
  validated instrument sequence.

### Calibration and Configuration

- Store parameters per physical configuration key, such as objective, lens,
  channel, or probe.
- Include units in UI labels and persistence keys. Keep raw device values and
  converted physical values distinguishable.
- Persist both operator intent and derived values when ambiguity matters.
- Validate saved data against device ranges and current scale. Reject stale
  calibration schemas rather than silently applying them.
- Apply configuration only after the relevant device reaches the state required
  for that value. Confirm the accepted/read-back value when available.

### GUI Integration

- Keep long SDK operations off the GUI thread, but marshal status updates through
  the GUI framework's signal/event mechanism.
- Log both operator actions and device responses. A moving instrument with no
  command trail is not diagnosable.
- Expose current state, units, ranges, selected calibration, and safety-critical
  assumptions near the controls they affect.
- Distinguish saved settings, preview-applied settings, and device-confirmed
  values.

## Testing and Completion

At minimum, verify:

- SDK imports and symbol binding;
- exact call order for initialization and motion;
- range, unit, sign, and state validation;
- stop, timeout, disconnect, and reconnect paths;
- GUI startup without hardware;
- persistence and migration of calibration data;
- package dependencies and release hashes.

Use mock drivers to assert observable behavior and state transitions. Test
meaningful invariants rather than matching log wording. If real hardware is
required but unavailable, finish what can be tested and explicitly leave the
hardware-dependent acceptance item open.

## Reference Routing

- Read [references/device-bringup.md](references/device-bringup.md) when
  identifying an SDK, reference executable, protocol, or first hardware session.
- Read
  [references/motion-camera-integration.md](references/motion-camera-integration.md)
  when implementing axes, triggers, cameras, autofocus, scanning, or calibration.
- Read [references/testing-and-data.md](references/testing-and-data.md) when
  building mocks, validating acquisition, or separating raw and processed data.
- Read [references/release-management.md](references/release-management.md)
  before packaging, versioning, or handing software to another lab computer.
