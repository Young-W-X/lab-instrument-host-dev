# Device Discovery and Safe Bring-Up

## Evidence Inventory

Collect the smallest set of authoritative artifacts:

- installed SDK headers and exported symbols;
- vendor examples written for the same DLL/firmware generation;
- device XML, configuration files, and logs;
- the customer's known-working executable and its version;
- transport mapping and device-manager/OS evidence;
- error-code definitions and firmware release notes.

If the only behavior source is a compiled program, inspect it statically before
launching it:

- imported DLLs and function names;
- embedded UI labels, configuration keys, and paths;
- packaged Python modules or resources;
- call-order clues from strings, logs, and sample code;
- connection endpoints and axis names.

Do not treat generic SDK enum definitions as proof that a camera or controller
implements every enum value. Query supported values at runtime when possible.

## Working Sequence Baseline

Write a short behavior table before editing:

| Stage | Reference behavior | Evidence |
|---|---|---|
| open transport | function, endpoint, timeout | header/import/log |
| identify/enable | function order and preconditions | reference executable |
| initialize | parameter writes, homing, status checks | vendor example |
| action | command, wait, recovery | known-working program |
| close | stop order and resource release | SDK documentation |

Reproduce that baseline first. Add robustness one change at a time and test the
same observable state sequence.

## Bring-Up Ladder

Use only the steps permitted by the instrument and available safety systems:

1. Confirm the OS sees the intended transport. Distinguish the vendor device
   from similarly named Bluetooth or virtual serial ports.
2. Open the connection and identify the device. Do not move anything.
3. Read status, firmware, serial number, positions, ranges, and supported enum
   values.
4. Enable one subsystem at a time and verify its reported state.
5. Perform a small, slow, bounded motion on one axis with emergency stop ready.
6. Repeat for each axis and verify sign, units, limits, and repeatability.
7. Verify outputs electrically before connecting them to a camera or actuator.
8. Test homing and recovery only after direction and limit behavior are known.
9. Run a short synchronized acquisition, then a representative scan.

Log the command, parameters, raw return code, interpreted error, elapsed time,
and resulting state for each step.

## Failure Handling

- Port timeout and access denial are different. Report both accurately.
- A successful command plus unchanged position may mean "already there" or may
  mean "not configured." Decide from the device contract, not guesswork.
- Do not repeatedly write flash or EEPROM during every motion.
- Reconnect logic must reset cached state; stale "initialized" flags are unsafe.
- If a stop or recovery path is uncertain, leave normal operation unavailable
  and surface the blocker.
