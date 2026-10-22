#!/usr/bin/env python3
"""Check the structural and hash integrity of an instrument release."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path


REQUIRED = ("bin", "src", "docs", "VERSION.txt", "RELEASE_NOTES.md",
            "SHA256SUMS.txt")


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("release")
    args = parser.parse_args()
    root = Path(args.release).resolve()
    if not root.is_dir():
        raise SystemExit(f"release directory not found: {root}")

    problems = []
    for name in REQUIRED:
        if not (root / name).exists():
            problems.append(f"missing required entry: {name}")

    manifest = root / "SHA256SUMS.txt"
    checked = 0
    if manifest.is_file():
        for line_number, raw in enumerate(
                manifest.read_text(encoding="utf-8-sig").splitlines(), 1):
            line = raw.strip()
            if not line:
                continue
            parts = line.split(None, 1)
            if len(parts) != 2:
                problems.append(
                    f"SHA256SUMS.txt:{line_number}: expected HASH  PATH")
                continue
            expected, relative = parts
            relative = relative.replace("\\", "/").lstrip("*")
            candidate = (root / relative).resolve()
            try:
                candidate.relative_to(root)
            except ValueError:
                problems.append(
                    f"SHA256SUMS.txt:{line_number}: path escapes release")
                continue
            if not candidate.is_file():
                problems.append(f"missing hashed file: {relative}")
                continue
            actual = digest(candidate)
            if actual.lower() != expected.lower():
                problems.append(f"hash mismatch: {relative}")
            checked += 1

    if problems:
        for problem in problems:
            print("ERROR:", problem)
        raise SystemExit(1)
    print(f"Release structure OK: {root}")
    print(f"Hashed files verified: {checked}")


if __name__ == "__main__":
    main()
