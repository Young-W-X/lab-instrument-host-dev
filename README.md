# Lab Instrument Host Development

A Codex skill for building and maintaining host-PC software for laboratory
instruments. It focuses on the parts that usually fail after the demo works:
vendor SDK discovery, motion safety, camera synchronization, calibration
semantics, deterministic tests, and immutable releases.

The workflow is derived from real integration work involving piezo stages,
optical objective switching, industrial cameras, autofocus systems, batch image
acquisition, restoration pipelines, and machine-vision post-processing.

## Install

Copy this directory into your Codex skills directory:

```bash
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R lab-instrument-host-dev "${CODEX_HOME:-$HOME/.codex}/skills/"
```

Restart or reload Codex, then invoke:

```text
Use $lab-instrument-host-dev to integrate this instrument SDK and build a safe,
testable host application.
```

## What It Emphasizes

- Verify the installed SDK and known-working program before changing sequences.
- Bring hardware up from read-only discovery to bounded motion.
- Keep transport, device APIs, orchestration, GUI, and processing separate.
- Preserve units, axis signs, limits, trigger timing, and calibration provenance.
- Use mocks to verify behavior when hardware is unavailable.
- Release versioned artifacts with manifests and explicit validation gaps.

## Repository Layout

```text
SKILL.md
agents/openai.yaml
references/
  device-bringup.md
  motion-camera-integration.md
  testing-and-data.md
  release-management.md
scripts/
  check_release.py
```

## Validate

```bash
python scripts/check_release.py /path/to/a/release
```

The script verifies required release structure and every path/hash in
`SHA256SUMS.txt`.

## Contributing

Add guidance only when it changes engineering decisions or prevents a concrete
class of failure. Keep vendor manuals out of the repository; record instead how
to find and verify the relevant contract.

## License

MIT. See [LICENSE](LICENSE).
