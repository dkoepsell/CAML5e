# CAML-5e: DM Quick Start (1 Page)

**What this is:**  
CAML-5e is a way to prep and run D&D adventures as **structured possibilities**, not scripts.  
You write *what could happen*, under *what conditions*, and let play decide the rest.

You do **not** need to code, model logic, or understand schemas to use this.

---

## The Core Idea (Read This First)

> **An adventure is a set of things that might happen, plus the conditions under which they happen.**

That’s it.

Instead of:
- “The party is ambushed on the road…”

You write:
- “An ambush *can* occur **if** the party has the key **and** it’s night.”

CAML just makes that explicit and reusable.

---

## What You Actually Edit

Everything is plain text **YAML**. Think “Markdown with structure.”

### Typical folders
```
adventure/
  module.yaml          ← overview
  locations/           ← places
  npcs/                ← people & monsters
  items/               ← loot & keys
  encounters/          ← scenes that may occur
```

You can open these in:
- VS Code  
- Obsidian  
- Any text editor  

---

## The Only 3 Files You Must Understand

### 1) `module.yaml` (the cover page)

```yaml
id: module.sunken_crypt
type: AdventureModule
name: The Sunken Crypt
description: A short dungeon with branching outcomes.
```

This tells you what the adventure *is*. That’s all.

---

### 2) An encounter file (what *might* happen)

```yaml
id: encounter.night_ambush
type: Encounter
occursAt: location.forest_path
participants: [npc.bandit_captain]

gates:
  all:
    - "party.has(item.obsidian_key)"
    - "area.night"

outcomes:
  success:
    - addTag: area.cleared
  failure:
    - transfer:
        item: item.obsidian_key
        to: npc.bandit_captain
```

**Read this like English:**
- This ambush only exists if the party has the key and it’s night.
- If they win, the area is cleared.
- If they lose, the bandit takes the key.

Nothing here forces the ambush to happen.

---

### 3) NPCs and items (stat blocks live here)

```yaml
id: npc.bandit_captain
type: NPC
ruleset: dnd5e
abilities: {str: 15, dex: 14, con: 14, int: 11, wis: 12, cha: 14}
actions:
  - name: Scimitar
    damage: [{dice: "1d6+2", type: slashing}]
```

Use as much or as little 5e detail as you want.

---

## How You Use This at the Table

### Before the session
1. Read `module.yaml`
2. Skim `encounters/`
3. Open the **graph viewer**:
   - `viewer/graph.html`
   - This shows what depends on what

You now understand the entire adventure logic at a glance.

---

### During play
- Do **not** follow a script  
- Ask: *“Have the conditions for this encounter been met?”*  
- If yes, it’s available  
- If no, it doesn’t exist (yet)  

You improvise narration as usual.

CAML only tracks **state**:
- who has what  
- what areas are cleared  
- what’s changed  

---

## Remixing (the fun part)

You can generate a new adventure by recombining pieces:

```bash
python scripts/remix.py --pick 2 examples/adventure-minimal examples/adventure-dungeon-srd
```

This creates a new pack where:
- encounter prerequisites still make sense  
- nothing is unreachable  
- required items/tags are seeded automatically  

Then:
```bash
python scripts/build_graph.py examples/remix-output
```

Open the graph. Run it.

---

## What You Don’t Need to Worry About

You can ignore:
- OWL  
- schemas  
- validation scripts  
- formal logic  

Those exist so tools don’t break later.

If you can read structured notes, you can use CAML.

---

## When CAML Is Especially Good

- Sandbox campaigns  
- Branching dungeons  
- Faction-heavy worlds  
- Reusable homebrew  
- Improvisational DMs who hate railroading  

---

## One-Sentence Summary

> **CAML lets you prep an adventure once, then play it a hundred different ways without rewriting it.**
