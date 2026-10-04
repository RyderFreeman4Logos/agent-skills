#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path

p = Path(__file__).resolve().parents[1] / "references" / "fallacies.json"
data = json.loads(p.read_text(encoding="utf-8"))
items = data["fallacies"]
assert len(items) == 65, f"expected 65 fallacies, got {len(items)}"
ids = [x["id"] for x in items]
assert len(ids) == len(set(ids)), "duplicate ids"
for x in items:
    for k in ("id", "name_zh", "name_en", "definition", "diagnostic_question"):
        assert x.get(k), f"{x.get('id')}: missing {k}"
print("taxonomy OK: 65 unique concepts")
