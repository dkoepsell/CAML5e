#!/usr/bin/env python3
import sys, json
from pathlib import Path

try:
    import yaml
except ImportError:
    print("Missing dependency: pyyaml. Install with: pip install pyyaml")
    sys.exit(2)

try:
    import jsonschema
except ImportError:
    print("Missing dependency: jsonschema. Install with: pip install jsonschema")
    sys.exit(2)

def load_yaml(p: Path):
    with p.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def load_json(p: Path):
    return json.loads(p.read_text(encoding="utf-8"))

def main(adventure_root: Path):
    repo_root = Path(__file__).resolve().parents[1]
    core_schema = load_json(repo_root / "schemas" / "caml-core.schema.json")
    dnd_schema = load_json(repo_root / "schemas" / "caml-5e.schema.json")

    ok = True
    for p in adventure_root.rglob("*.yaml"):
        obj = load_yaml(p)
        if not isinstance(obj, dict):
            continue
        if "id" not in obj or "type" not in obj:
            print(f"[WARN] Missing id/type: {p}")
            ok = False
            continue

        # Always validate core
        try:
            jsonschema.validate(obj, core_schema)
        except Exception as e:
            print(f"[FAIL] Core schema: {p}: {e}")
            ok = False

        # Validate 5e layer if ruleset is dnd5e
        if obj.get("ruleset") == "dnd5e":
            try:
                # Provide required fields if not present (best-effort for mixed objects)
                candidate = dict(obj)
                candidate.setdefault("ruleset","dnd5e")
                jsonschema.validate(candidate, dnd_schema)
            except Exception as e:
                print(f"[FAIL] 5e schema: {p}: {e}")
                ok = False

    print("Validation:", "OK" if ok else "FAILED")
    return 0 if ok else 1

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: validate.py <adventure_root>")
        sys.exit(1)
    sys.exit(main(Path(sys.argv[1]).resolve()))
