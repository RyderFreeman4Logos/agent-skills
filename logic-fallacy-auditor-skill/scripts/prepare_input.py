#!/usr/bin/env python3
"""Normalize line endings and emit stable line-numbered JSON for fallacy analysis."""

from __future__ import annotations
import argparse
import hashlib
import json
import sys
from pathlib import Path


def read_text(path: str | None) -> str:
    if path:
        return Path(path).read_text(encoding="utf-8")
    return sys.stdin.read()


def normalize(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    # Preserve paragraph/line structure, trim trailing whitespace only.
    return "\n".join(line.rstrip() for line in text.split("\n")).strip("\n")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("input", nargs="?", help="UTF-8 input file; stdin if omitted")
    ap.add_argument("--chunk-lines", type=int, default=80)
    ap.add_argument("--overlap-lines", type=int, default=8)
    args = ap.parse_args()

    text = normalize(read_text(args.input))
    lines = text.split("\n") if text else []
    numbered = [{"line": i + 1, "text": line} for i, line in enumerate(lines)]

    chunk_lines = max(1, args.chunk_lines)
    overlap = max(0, min(args.overlap_lines, chunk_lines - 1))
    step = chunk_lines - overlap
    chunks = []
    for start in range(0, len(lines), step):
        end = min(len(lines), start + chunk_lines)
        chunks.append({
            "chunk_id": len(chunks) + 1,
            "start_line": start + 1,
            "end_line": end,
            "text": "\n".join(lines[start:end]),
        })
        if end == len(lines):
            break

    payload = {
        "sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
        "line_count": len(lines),
        "text": text,
        "lines": numbered,
        "chunks": chunks,
    }
    json.dump(payload, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
