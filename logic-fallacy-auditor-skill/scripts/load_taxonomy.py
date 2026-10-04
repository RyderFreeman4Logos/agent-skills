#!/usr/bin/env python3
"""Assemble the taxonomy from the manifest-declared JSON parts."""
from __future__ import annotations
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "references" / "fallacies.json"


def load_taxonomy() -> dict:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    parts = manifest.get("parts")
    if not isinstance(parts, list) or not parts:
        raise ValueError("taxonomy manifest must list JSON data parts")

    fallacies = []
    for name in parts:
        if not isinstance(name, str) or Path(name).name != name:
            raise ValueError(f"invalid taxonomy part name: {name!r}")
        data = json.loads((MANIFEST.parent / name).read_text(encoding="utf-8"))
        if not isinstance(data, list):
            raise ValueError(f"taxonomy part must contain a JSON list: {name}")
        fallacies.extend(data)

    taxonomy = {key: value for key, value in manifest.items() if key != "parts"}
    taxonomy["fallacies"] = fallacies
    return taxonomy


if __name__ == "__main__":
    json.dump(load_taxonomy(), sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
