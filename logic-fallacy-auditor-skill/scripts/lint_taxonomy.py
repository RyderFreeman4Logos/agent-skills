#!/usr/bin/env python3
from __future__ import annotations
from load_taxonomy import load_taxonomy

items = load_taxonomy()["fallacies"]
assert len(items) == 65, f"expected 65 fallacies, got {len(items)}"
ids = [x["id"] for x in items]
assert len(ids) == len(set(ids)), "duplicate ids"
for x in items:
    for k in ("id", "name_zh", "name_en", "definition", "diagnostic_question"):
        assert x.get(k), f"{x.get('id')}: missing {k}"
print("taxonomy OK: 65 unique concepts")
