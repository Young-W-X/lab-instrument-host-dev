# Release Management and Packaging

## Immutable Releases

Use one directory per release:

```text
releases/
  instrument-host-v2.7-20261021-01/
    bin/
    src/
    docs/
    VERSION.txt
    RELEASE_NOTES.md
    SHA256SUMS.txt
```

Never overwrite a published directory. A change creates a new version and build
number. Keep older releases available for rollback.

Record at least:

- version and build identifier;
- date and status;
- source baseline;
- intended external device/runtime dependencies;
- known validation gaps;
- executable hash.

## Build and Dependency Rules

- Build from the release's own source snapshot.
- Bundle only redistributable components and verify their inclusion.
- Declare SDKs, drivers, runtimes, licenses, and hardware that must exist on the
  target computer.
- Avoid absolute developer paths in defaults. Resolve configuration relative to
  the executable or an explicit CLI option.
- Keep configuration and calibration outside the executable; define whether
  upgrading preserves, migrates, or invalidates them.

## Release Verification

Run `scripts/check_release.py <release-directory>` and additionally verify:

1. a clean machine can start the application;
2. expected external DLLs or runtimes load;
3. configuration is written to the intended directory;
4. logs and capture directories are writable;
5. packaged hardware libraries are present;
6. no old process locks the artifact;
7. hardware validation remains explicitly open if no device is available.

## Handoff

Provide the exact executable path, version, hash, prerequisites, preserved
configuration files, and rollback path. Do not instruct users to overwrite a
deployment root when a versioned side-by-side install is possible.
