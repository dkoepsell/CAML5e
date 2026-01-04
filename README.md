# CAML-5e: Canonical Adventure Markup Language (Core + D&D 5e Layer)

This repository drop-in provides:

- **CAML Core**: system-agnostic adventure/archive schema
- **CAML-5e**: D&D 5e mechanics layer (structured, exportable)
- **BFO-aligned OWL skeleton** (Turtle)
- **PlantUML architecture diagram**
- **Example adventure pack** (minimal but complete)
- **Foundry VTT export mapping spec** (field-level mapping)
- **Validation + indexing script** (YAML -> JSON index, basic schema checks)

## What this is (and is not)

CAML models an adventure as a **structured possibility space**:
- Locations, NPCs, items, encounters
- Conditions (gates) and outcomes (state changes)
- Modular components you can reuse and version

CAML-5e adds a **rules layer** for 5e mechanics:
- Ability scores, skills, saves, actions
- Spells, conditions, damage
- Resources and rest events

### Licensing boundary

This repo contains **schemas and structures**. It does **not** include non-SRD Wizards text.
If you want to bundle SRD-derived spell/monster lists, add them as separate packs under `packs/`
with proper **CC BY 4.0** attribution.

## Folder layout

- `schemas/` JSON Schemas
- `ontology/` OWL (Turtle) skeleton, BFO-aligned
- `puml/` PlantUML diagrams
- `examples/` A minimal working adventure archive (YAML)
- `exports/` Export mapping specs (start with Foundry)
- `scripts/` Utility scripts (index/validate)

## Quick start

1) Install Python deps (optional): `pip install pyyaml jsonschema`
2) Build an index for an adventure:
```bash
python scripts/build_index.py examples/adventure-minimal
```
3) Validate key files (best-effort):
```bash
python scripts/validate.py examples/adventure-minimal
```

## IDs

CAML uses stable identifiers like:
- `location.ruined_tower`
- `npc.bandit_captain`
- `encounter.night_ambush`

These are intended to be durable across versions for diffs and references.

## Authoring notes

- Keep prose in `description` fields and journals/handouts.
- Keep mechanics in the `ruleset: dnd5e` layer.
- Keep branching in `gates` and `outcomes` (state transitions).

---

Generated on 2026-01-04.

## Graph visualizer (encounter + gate graph)

1) Build a graph for an adventure:
```bash
python scripts/build_graph.py examples/adventure-dungeon-srd
```
2) Open the viewer:
- `viewer/graph.html`
- default path points at `examples/adventure-dungeon-srd/graph.json`

## Procedural remix tool

Safely recombines CAML components into a new pack while making encounter gates satisfiable.

Example:
```bash
python scripts/remix.py --out examples/remix-output --seed 123 --pick 2 examples/adventure-minimal examples/adventure-dungeon-srd
python scripts/build_graph.py examples/remix-output
```
