#!/usr/bin/env python3
import sys, json
from pathlib import Path

try:
    import yaml
except ImportError:
    print("Missing dependency: pyyaml. Install with: pip install pyyaml")
    sys.exit(2)

def load_yaml(p: Path):
    with p.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def main(root: Path):
    entries = []
    for p in root.rglob("*.yaml"):
        obj = load_yaml(p)
        if not isinstance(obj, dict) or "id" not in obj or "type" not in obj:
            continue
        obj["_path"] = str(p.relative_to(root))
        entries.append(obj)

    index = {
        "root": str(root),
        "count": len(entries),
        "byType": {},
        "entries": entries,
    }
    for e in entries:
        index["byType"].setdefault(e["type"], 0)
        index["byType"][e["type"]] += 1

    out = root / "index.json"
    out.write_text(json.dumps(index, indent=2), encoding="utf-8")
    print(f"Wrote {out} with {len(entries)} entries")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: build_index.py <adventure_root>")
        sys.exit(1)
    main(Path(sys.argv[1]).resolve())
