# CAML 2.0

CAML 2.0 is a second-generation refactor of the Canonical Adventure Markup Language (CAML).
It is designed to make game states explicit, auditable, and replayable, and it cleanly supports
correspondence (asynchronous) adventures.

CAML 2.0 separates the document into ontological layers:

- `world`: independent continuants (characters, locations, items, factions, and their static connections)
- `state`: dependent continuants (status facts that depend on a bearer)
- `roles`: role assignments (revocable, externally grounded)
- `processes`: occurrents (things that happen in time)
- `transitions`: the only place persistent change occurs
- `snapshots`: a timestamped timeline of campaign states

## Files

- `schemas/`: JSON Schema drafts for CAML 2.0
- `specs/caml2.invariants.md`: normative invariants enforced by validators (beyond JSON Schema)
- `examples/`: working example documents and patterns

## Conformance

- Level A: JSON Schema valid
- Level B: Level A + invariants II–VI satisfied
- Level C: Level B + correspondence invariants satisfied (if correspondence enabled)
