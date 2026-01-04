# Foundry VTT Export Mapping (CAML -> Foundry Documents)

This is a practical mapping spec you can implement in an exporter.

## Core mappings

### CAML Location -> Foundry Scene + Journal
- `Location.name` -> Scene name
- `Location.description` -> JournalEntry content
- `Location.connections` -> Journal links + Scene notes

### CAML NPC (ruleset:dnd5e) -> Foundry Actor (dnd5e system)
- `abilities` -> `system.abilities`
- `defenses.ac.value` -> `system.attributes.ac.value`
- `defenses.hp.max` -> `system.attributes.hp.max`
- `actions[]` -> either:
  - Items (weapon actions) attached to Actor, or
  - inline action notes, depending on your module style

### CAML Item -> Foundry Item
- `Item.name` -> Item name
- `Item.description` -> Item description/journal
- tags -> Item flags

### CAML Encounter -> Foundry Journal Entry + (optional) RollTable
- Encounters are best represented as Journal Entries (GM-facing)
- If you want automation, generate RollTables for outcomes and gates

## Versioning

- Keep stable CAML ids as Foundry flags:
  - `flags.caml.id = "npc.bandit_captain"`
  - `flags.caml.type = "NPC"`
