# CAML5e  
**Canonical Adventure Markup Language for D&D 5e**

CAML (Canonical Adventure Markup Language) is a structured format for authoring, running, and analyzing tabletop role-playing game adventures, with an initial focus on Dungeons & Dragons 5e.

This repository supports **two generations of CAML**:

- **CAML 1.x** – the original, human-friendly schema used for practical 5e adventure design  
- **CAML 2.0** – a second-generation, ontologically grounded refactor designed for explicit game state, correspondence play, and tooling

CAML does **not** replace D&D rules.  
It structures adventures, not mechanics.

---

## Repository Structure

```
CAML5e/
├─ caml-1.x/              # Legacy CAML (stable, unchanged)
├─ caml-2.0/              # CAML 2.0 (explicit, ontologically grounded)
│  ├─ schemas/
│  ├─ specs/
│  ├─ examples/
│  └─ README.md
│
├─ schemas/               # CAML 1.x schemas
├─ ontology/              # Ontology and BFO-related work (CAML 1.x era)
├─ examples/              # CAML 1.x examples
├─ exports/               # Export and transformation formats
├─ scripts/               # Utilities and helpers
├─ viewer/                # Visualization tools
├─ tools/validator-stub/  # Placeholder for CAML 2.0 validation tooling
├─ docs/                  # Design notes and version comparisons
│
├─ DM_QUICKSTART.md
├─ CAML Tech Spec.pdf
└─ README.md
```

---

## CAML 1.x (Legacy, Stable)

**CAML 1.x** is the original format developed for:

- practical DM use
- D&D 5e adventure modules
- structured but flexible worldbuilding
- notebook-style campaign management

It mixes entities, state, and events in a way that is easy for humans to read and write, and it remains fully supported.

If you are:
- writing a standard 5e adventure
- using CAML as enhanced DM notes
- not concerned with formal state tracking

→ **Use CAML 1.x**

---

## CAML 2.0 (Experimental, Structured)

**CAML 2.0** is a refactor of CAML that makes game state **explicit, auditable, and replayable**.

It introduces:

- explicit separation of:
  - world structure (entities)
  - dependent state (facts)
  - roles (revocable authority and position)
  - processes (events in time)
  - transitions (the only source of persistent change)
  - snapshots (time-indexed world states)
- formal invariants grounded in a minimal BFO-aligned ontology
- first-class support for correspondence (asynchronous) adventures
- traceability and post-hoc analysis
- a foundation for tooling, validation, and AI assistance

CAML 2.0 is **additive** and **non-breaking**.  
It does not alter any D&D 5e mechanics.

If you are:
- running long-form or asynchronous campaigns
- collaborating across multiple DMs
- building tools, validators, or simulations
- interested in formal game-state semantics

→ **Use CAML 2.0**

See `caml-2.0/README.md` for full details.

---

## Relationship Between CAML 1.x and 2.0

- CAML 1.x remains stable and supported
- CAML 2.0 lives in its own versioned directory
- No files are overwritten
- Migration from 1.x to 2.0 is possible but optional
- Both formats can coexist in the same campaign ecosystem

CAML 2.0 should be understood as **infrastructure**, not a replacement.

---

## Correspondence (Asynchronous) Play

CAML 2.0 explicitly supports correspondence-style adventures (analogous to correspondence chess), where:

- players submit structured actions asynchronously
- time is explicit
- conflicts are arbitrated deterministically
- world state can be paused, resumed, and audited

This is not reliably achievable with narrative-only formats.

---

## Status

- CAML 1.x: **Stable**
- CAML 2.0: **Draft (structurally complete, subject to iteration)**
- Validator tooling: **Planned**
- Migration tooling: **Planned**

---

## License

See `LICENSE`.

---

## Citation

If you use CAML in academic, educational, or published work, please see `CITATION.cff`.

---

## Philosophy (Brief)

CAML treats an adventure not as a script, but as a **stateful system that produces stories through play**.

CAML 2.0 makes that system explicit.

---

For questions, discussion, or contributions, open an issue or pull request.
