# Testing and Data Integrity

## Mocking Hardware

Build a fake SDK that records:

- call order;
- axis, channel, and endpoint arguments;
- raw return values;
- state transitions;
- wait and stop requests.

Use it to test startup, initialization frequency, motion preconditions, timeout
handling, reconnect, and shutdown. A test that only checks that a method exists
is insufficient.

For opaque SDK contracts, encode observed behavior as a compatibility test. If
the working program initializes once and sends one move command, the refactor
must not silently initialize on every point.

## Offline GUI Tests

Start the GUI without hardware and verify that:

- startup does not crash;
- unavailable devices have actionable messages;
- controls remain responsive;
- long operations do not block the event loop;
- saved settings survive restart;
- archive/package paths do not depend on the developer machine.

## Acquisition Data

Preserve provenance per run:

- source device and firmware;
- acquisition settings;
- objective and optical calibration identifiers;
- scan strategy and points;
- raw file directory;
- processing version and parameters;
- success, warnings, and failures.

Do not overwrite raw data during processing. When a processor deletes or moves
inputs, record that behavior explicitly and keep enough hashes or backups to
audit the result.

Raw unprocessed labels and color-corrected labels are different datasets. Select
one deliberately, document it in loader code and checkpoints, and never fall
back to the other file name because it happens to exist.

## Dataset Splits

Split by physical specimen, wafer, session, or acquisition batch when leakage
would invalidate the result. Adjacent crops from the same source must remain in
one split.

For automated preparation:

- reject missing image pairs before copying;
- verify dimensions;
- compute and log the quality metric used for filtering;
- write a manifest containing included and excluded items;
- use a fixed seed for reproducible assignment;
- refuse an impossible split rather than silently lowering thresholds.

## Completion Language

Use precise evidence terms:

- "static contract verified";
- "mock call order verified";
- "GUI startup verified";
- "package integrity verified";
- "real hardware not connected; motion not verified."

Do not collapse these into "tested" or "working."
