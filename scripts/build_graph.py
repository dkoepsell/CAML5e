#!/usr/bin/env python3
"""
Build an Encounter + Gate graph for a CAML adventure.

Outputs:
- graph.json: nodes + links suitable for viewer/graph.html

Graph model (simple, useful):
- Encounter nodes: type=encounter
- Requirement nodes:
  - tag:<TAG> (gate requires a tag)
  - item:<ITEM_ID> (gate requires party.has(item.*))
  - fact:<FACT_NAME> (structured gate uses fact/op/value)
- Outcome nodes:
  - tag:<TAG> (encounter produces tag via addTag)
  - set:<EXPR> (encounter sets a state expression)

Edges:
- req -> encounter (requires)
- encounter -> out (produces)
"""
import sys, json, re
from pathlib import Path

try:
    import yaml
except ImportError:
    print("Missing dependency: pyyaml. Install with: pip install pyyaml")
    sys.exit(2)

TAG_RE = re.compile(r"^[a-zA-Z0-9_.:-]+$")  # allow area.cleared etc
ITEM_REQ_RE = re.compile(r"party\.has\(\s*(item\.[a-zA-Z0-9_.-]+)\s*\)")

def load_yaml(p: Path):
    with p.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def extract_gate_requirements(gates):
    """Return list of requirement node ids."""
    reqs = []
    if not isinstance(gates, dict):
        return reqs
    exprs = []
    if "all" in gates and isinstance(gates["all"], list):
        exprs += gates["all"]
    if "any" in gates and isinstance(gates["any"], list):
        exprs += gates["any"]
    if "not" in gates and gates["not"] is not None:
        exprs += [gates["not"]]

    for e in exprs:
        if isinstance(e, str):
            m = ITEM_REQ_RE.search(e)
            if m:
                reqs.append(f"item:{m.group(1)}")
                continue
            # treat bare tags like "area.cleared"
            if TAG_RE.match(e.strip()):
                reqs.append(f"tag:{e.strip()}")
                continue
            reqs.append(f"expr:{e.strip()}")
        elif isinstance(e, dict) and {"fact","op","value"}.issubset(e.keys()):
            fact = str(e.get("fact"))
            op = str(e.get("op"))
            val = e.get("value")
            reqs.append(f"fact:{fact} {op} {val!r}")
        else:
            reqs.append(f"expr:{str(e)}")
    return reqs

def extract_outcomes(outcomes):
    outs = []
    if not isinstance(outcomes, dict):
        return outs
    for _k, steps in outcomes.items():
        if not isinstance(steps, list):
            continue
        for st in steps:
            if isinstance(st, dict) and "addTag" in st:
                outs.append(f"tag:{st['addTag']}")
            elif isinstance(st, dict) and "set" in st:
                outs.append(f"set:{st['set']}")
            elif isinstance(st, dict) and "inc" in st:
                by = st.get("by", 1)
                outs.append(f"inc:{st['inc']} by {by}")
            elif isinstance(st, dict) and "dec" in st:
                by = st.get("by", 1)
                outs.append(f"dec:{st['dec']} by {by}")
            elif isinstance(st, dict) and "transfer" in st:
                tr = st.get("transfer", {})
                outs.append(f"transfer:{tr}")
            elif isinstance(st, dict) and "removeTag" in st:
                outs.append(f"tag:-{st['removeTag']}")
    return outs

def main(root: Path):
    nodes = {}
    links = []

    # collect YAML objects
    objs = []
    for p in root.rglob("*.yaml"):
        obj = load_yaml(p)
        if isinstance(obj, dict) and "id" in obj and "type" in obj:
            obj["_path"] = str(p.relative_to(root))
            objs.append(obj)

    # encounters only for this graph
    encounters = [o for o in objs if o.get("type") == "Encounter"]

    def add_node(nid, ntype, label=None, meta=None):
        if nid not in nodes:
            nodes[nid] = {
                "id": nid,
                "type": ntype,
                "label": label if label is not None else nid,
                "meta": meta or {}
            }

    for e in encounters:
        eid = e["id"]
        add_node(eid, "encounter", e.get("name", eid), {"path": e.get("_path","")})

        # gates
        for r in extract_gate_requirements(e.get("gates")):
            add_node(r, "requirement", r.split(":",1)[1] if ":" in r else r, {})
            links.append({"source": r, "target": eid, "type": "requires"})

        # outcomes
        for o in extract_outcomes(e.get("outcomes")):
            otype = "outcome"
            if o.startswith("tag:"):
                otype = "tag"
            add_node(o, otype, o.split(":",1)[1] if ":" in o else o, {})
            links.append({"source": eid, "target": o, "type": "produces"})

    graph = {
        "root": str(root),
        "nodes": list(nodes.values()),
        "links": links
    }

    out = root / "graph.json"
    out.write_text(json.dumps(graph, indent=2), encoding="utf-8")
    print(f"Wrote {out} with {len(graph['nodes'])} nodes, {len(graph['links'])} links")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: build_graph.py <adventure_root>")
        sys.exit(1)
    main(Path(sys.argv[1]).resolve())
