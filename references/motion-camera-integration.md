# Motion, Camera, and Calibration Integration

## Physical Contract

Document before implementation:

- axis indices and names;
- physical units and conversion from device units;
- positive direction and image-space direction;
- minimum, maximum, backlash, speed, acceleration, and settle time;
- home method, home direction, and limit behavior;
- emergency-stop behavior;
- output channel, polarity, pulse width, and electrical interface.

Reject out-of-range targets in software before issuing a device command. If the
controller independently owns soft limits, do not imply that the host settings
replace them.

## Motion State

Use explicit states such as disconnected, opening, identified, enabled, idle,
moving, homing, capturing, stopping, and faulted.

- Allow commands only from valid states.
- Do not run multiple workers against one instrument handle.
- A user stop must reach the device, not merely set a GUI flag.
- Keep configuration separate from motion commands.
- Verify completion with the controller's status API or the documented wait.

Prefer point-to-point motion for first integration. Add interpolation or
continuous-motion triggering only after speed, settling, and output timing are
validated.

## Camera and Optics

- Query actual exposure, gain, white-balance, and trigger capabilities.
- Disable automatic exposure, gain, and white balance before manual imaging.
- For white balance, use a neutral target under representative illumination.
  Store one channel set per optical path when transmission differs.
- Use the same illumination, exposure family, and focal plane for calibration
  and production.
- Keep trigger mode, exposure, and motion timing compatible. A pulse only
  requests an exposure; it does not guarantee the frame is complete before the
  next move.

## Focus

Distinguish three operations:

- **search:** autofocus to find a focus within a range;
- **calibration:** operator accepts a final focal plane;
- **production:** restore the accepted configuration after each lens change.

Store which quantity the production workflow uses. A relative offset applies to
the autofocus result from the same operation. An absolute position only makes
sense when the stage zero and sample reference are stable. Do not mix them.

After a lens, objective, filter, or focal-plane change:

1. wait for mechanical movement to complete;
2. apply the lens-specific exposure and optical calibration;
3. run the documented focus sequence;
4. apply any configured offset or absolute target exactly once;
5. wait for stability;
6. acquire.

## Scan Planning

For circular samples, prefer a serpentine raster clipped to the valid circle
when rectangular images must be stitched. Set center, radius, edge exclusion,
field of view, overlap, and rotation alignment explicitly.

Estimate point count and path length before motion. A request that implies tens
of thousands of stops may be a planning error; surface the estimate before
starting.

Keep original images, metadata, reconstruction outputs, and metrics in separate
paths. Record the scan plan and calibration identifiers with each run.
