#!/usr/bin/env python3
"""
Procedural remix tool: safely recombine CAML components into a new pack.

Safety policy (practical):
- Only include encounters whose gate requirements are satisfiable by:
  - starting tags/items, OR
  - outcomes of included encounters (addTag / set / transfer)
- If an encounter requires an item (party.has(item.X)), the remixer
  ensures that item is included and added to startingItems unless
  an included outcome transfers/grants it (transfer item to party not yet modeled).

Usage:
  python scripts/remix.py --out examples/remix-output \
      --seed 123 \
      --pick 2 \
      examples/adventure-minimal examples/adventure-dungeon-srd

Notes:
- This is SRD-safe by default because it only copies YOUR YAML entries.
- Extend the gate/outcome parsers as you add more expression forms.
"""
import argparse, random, shutil, re
from pathlib import Path

try:
    import yaml
except ImportError:
    print("Missing dependency: pyyaml. Install with: pip install pyyaml")
    raise SystemExit(2)

ITEM_REQ_RE = re.compile(r"party\.has\(\s*(item\.[a-zA-Z0-9_.-]+)\s*\)")
TAG_RE = re.compile(r"^[a-zA-Z0-9_.:-]+$")

def load_yaml(p: Path):
    with p.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def dump_yaml(obj, p: Path):
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("w", encoding="utf-8") as f:
        yaml.safe_dump(obj, f, sort_keys=False, allow_unicode=True)

def iter_objs(roots):
    for root in roots:
        for p in Path(root).rglob("*.yaml"):
            obj = load_yaml(p)
            if isinstance(obj, dict) and "id" in obj and "type" in obj:
                yield obj, p

def gate_reqs(enc):
    req_tags, req_items, req_facts = set(), set(), set()
    gates = enc.get("gates")
    if not isinstance(gates, dict):
        return req_tags, req_items, req_facts

    exprs = []
    if isinstance(gates.get("all"), list): exprs += gates["all"]
    if isinstance(gates.get("any"), list): exprs += gates["any"]
    if gates.get("not") is not None: exprs += [gates["not"]]

    for e in exprs:
        if isinstance(e, str):
            m = ITEM_REQ_RE.search(e)
            if m:
                req_items.add(m.group(1))
                continue
            if TAG_RE.match(e.strip()):
                req_tags.add(e.strip())
                continue
            # unknown expression; treat as fact-like requirement token
            req_facts.add(e.strip())
        elif isinstance(e, dict) and {"fact","op","value"}.issubset(e.keys()):
            req_facts.add(f"{e['fact']} {e['op']} {e['value']!r}")
        else:
            req_facts.add(str(e))
    return req_tags, req_items, req_facts

def produces(enc):
    prod_tags, prod_sets = set(), set()
    outs = enc.get("outcomes", {})
    if not isinstance(outs, dict):
        return prod_tags, prod_sets
    for _k, steps in outs.items():
        if not isinstance(steps, list): continue
        for st in steps:
            if isinstance(st, dict) and "addTag" in st:
                prod_tags.add(st["addTag"])
            if isinstance(st, dict) and "set" in st:
                prod_sets.add(st["set"])
    return prod_tags, prod_sets

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("roots", nargs="+", help="Adventure roots to remix from")
    ap.add_argument("--out", required=True, help="Output folder for remixed adventure")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--pick", type=int, default=3, help="How many encounters to target")
    args = ap.parse_args()

    rnd = random.Random(args.seed)

    roots = [Path(r).resolve() for r in args.roots]
    out = Path(args.out).resolve()

    # collect all objects by id
    by_id = {}
    by_type = {}
    path_by_id = {}
    for obj, p in iter_objs(roots):
        by_id[obj["id"]] = obj
        path_by_id[obj["id"]] = p
        by_type.setdefault(obj["type"], []).append(obj["id"])

    encounters = [eid for eid in by_type.get("Encounter", [])]
    if not encounters:
        raise SystemExit("No Encounter entries found in sources.")

    targets = rnd.sample(encounters, k=min(args.pick, len(encounters)))

    included = set()
    starting_tags = set()
    starting_items = set()

    # include targets and close under prerequisites
    # We do a fixed-point pass:
    # - include encounter
    # - add required items to startingItems (if not otherwise provided)
    # - require tags; if tags not yet satisfiable, include encounters that produce them if available
    # - repeat until stable
    def include_enc(eid):
        if eid in included: return
        included.add(eid)

    for t in targets:
        include_enc(t)

    # helper: find encounter that produces a tag
    tag_producers = {}
    for eid in encounters:
        prod_tags, _ = produces(by_id[eid])
        for tg in prod_tags:
            tag_producers.setdefault(tg, []).append(eid)

    changed = True
    while changed:
        changed = False
        current_tags = set(starting_tags)
        # accumulate tags produced by included encounters (optimistic)
        for eid in list(included):
            prod_tags, _ = produces(by_id[eid])
            current_tags |= prod_tags

        for eid in list(included):
            req_tags, req_items, req_facts = gate_reqs(by_id[eid])

            # items: seed them (safe default)
            for it in req_items:
                if it not in starting_items:
                    starting_items.add(it)
                    changed = True

            # tags: if not available, try to include a producer
            missing = [tg for tg in req_tags if tg not in current_tags]
            for tg in missing:
                prods = tag_producers.get(tg, [])
                if prods:
                    choice = prods[0]
                    if choice not in included:
                        include_enc(choice)
                        changed = True
                else:
                    # no producer; seed as starting tag to avoid unsatisfiable gate
                    starting_tags.add(tg)
                    changed = True

    # now include referenced participants and occursAt
    for eid in list(included):
        e = by_id[eid]
        loc = e.get("occursAt")
        if isinstance(loc, str) and loc in by_id:
            included.add(loc)
        for pid in e.get("participants", []) or []:
            if isinstance(pid, str) and pid in by_id:
                included.add(pid)

    # include all items that are required
    for it in list(starting_items):
        if it in by_id:
            included.add(it)

    # include module template
    module = {
        "id": f"module.remix_{args.seed}",
        "type": "AdventureModule",
        "name": f"Remix Pack (seed {args.seed})",
        "description": "Procedurally remixed CAML adventure pack. Gates were made satisfiable via starting tags/items and prerequisite encounters.",
        "tags": ["remix","generated"],
        "startingTags": sorted(starting_tags),
        "startingItems": sorted(starting_items),
    }

    # write output structure
    if out.exists():
        shutil.rmtree(out)
    (out/"locations").mkdir(parents=True)
    (out/"npcs").mkdir(parents=True)
    (out/"items").mkdir(parents=True)
    (out/"encounters").mkdir(parents=True)
    (out/"rules").mkdir(parents=True)

    dump_yaml(module, out/"module.yaml")

    # copy included YAML objects into type folders
    type_folder = {
        "Location":"locations",
        "NPC":"npcs",
        "PC":"npcs",
        "Item":"items",
        "Encounter":"encounters",
        "StateFact":"rules",
        "Quest":"quests",
        "Faction":"factions",
        "Handout":"handouts",
    }

    for oid in sorted(included):
        obj = by_id.get(oid)
        if not obj: 
            continue
        t = obj.get("type")
        folder = type_folder.get(t)
        if not folder:
            # skip unknown types for now
            continue
        dump_yaml(obj, out/folder/(oid.split(".",1)[-1] + ".yaml"))

    print("Remix written to:", out)
    print("Included objects:", len(included))
    print("Starting tags:", sorted(starting_tags))
    print("Starting items:", sorted(starting_items))
    print("Tip: build graph -> python scripts/build_graph.py", out)

if __name__ == "__main__":
    main()
