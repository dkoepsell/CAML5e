# CAML 2.0 Formal Invariants (Normative)

This document defines semantic constraints for CAML 2.0 that are not fully expressible in JSON Schema.
A CAML 2.0 validator MUST enforce these invariants.

Terminology
- Entity: an independent continuant in `world.entities.*`
- State fact: a dependent continuant in `state.facts`
- Role assignment: an externally grounded role in `roles.assignments`
- Process instance: an occurrent in `processes.catalog`
- Transition: a set of operations in `transitions.changes`
- Snapshot: an entry in `snapshots.timeline`

## I. Identity and Reference Invariants

I-1. Unique IDs
- All `id` values across the following sets MUST be unique within the document:
  - world entities (characters, locations, items, factions)
  - connections
  - state facts
  - role assignments
  - processes
  - transitions
  - snapshots
  - correspondence turns (if present)

I-2. Referential integrity
- Every reference (`ref`) to an entity MUST resolve to an existing world entity ID.
- Every `transition.caused_by` MUST resolve to an existing `processes.catalog[].id`.
- Every `snapshot.derived_from_transition` (if present) MUST resolve to an existing transition ID.
- Every `roles.assignments[].granted_by_process` (if present) MUST resolve to an existing process ID.
- Every `state.facts[].provenance.source_process` (if present) MUST resolve to an existing process ID.

I-3. Kind correctness
- References MUST be used in kind-correct positions:
  - `process_instance.location` MUST reference a location entity.
  - `connection.from` and `connection.to` MUST reference locations (unless a specific extended profile states otherwise).

## II. Layer Separation Invariants (BFO-aligned)

II-1. World is timeless
- `world` MUST NOT encode time, events, or changes.
- Any temporal or causal data MUST be represented in `processes`, `transitions`, or `snapshots`.

II-2. State is dependent
- Every `state_fact.bearer` MUST reference an existing entity.
- No state fact may exist without exactly one bearer.

II-3. Roles are dependent and revocable
- Every role assignment MUST have:
  - `holder` referencing an existing entity
  - `role` as a type label
- Every role assignment MUST include either:
  - `revocation` condition_set, or
  - a profile-level default revocation rule that is explicitly documented.
A validator MUST warn if `revocation` is absent.

II-4. Processes are occurrents
- Every process MUST have:
  - a `timebox` with `start_utc` < `end_utc`
  - at least one participant
- A process MUST NOT be used to store persistent state directly; persistent results MUST be expressed via transitions.

II-5. Transitions are the only mechanism of change
- Persistent changes to:
  - state facts
  - role assignments
  - entity creation/retirement
  - entity relocation (if modeled as persistent)
MUST occur only via `transitions.changes[].ops[]`.

## III. Causality Invariants

III-1. No free-floating change
- Every transition MUST specify `caused_by` referencing a process instance.
- A validator MUST reject any transition with a missing or unresolved `caused_by`.

III-2. Operation causality
- For each operation in a transition:
  - `add_state.fact.provenance.source_process` SHOULD equal the transition's `caused_by` (warning if absent or different).
  - `grant_role.assignment.granted_by_process` SHOULD equal the transition's `caused_by` (warning if absent or different).

III-3. Temporal alignment
- The transition is considered to occur at or after its causing process timebox.
- A validator MUST enforce:
  - If a snapshot references `derived_from_transition = T`,
    then `snapshot.time_utc` MUST be >= `process.timebox.end_utc` for `T.caused_by`.

## IV. State Coherence Invariants

IV-1. State fact type constraints
- For any given bearer, the profile MAY define cardinality constraints by `state_fact.type`.
- Absent a profile, the validator SHOULD warn on multiple concurrent state facts with the same `{bearer, type}` unless explicitly allowed.

IV-2. Updates require existence
- `update_state` and `remove_state` MUST reference an existing state fact ID at the moment of application.
Validator MUST reject if the target does not exist in the pre-state for that transition.

IV-3. Bearer immutability
- A state fact's `bearer` MUST NOT be changed via `update_state`.
To change bearer, the correct pattern is:
  - remove_state(old_fact_id)
  - add_state(new_fact_with_new_bearer)

IV-4. No floating validity intervals
- If `state_fact.validity.until_snapshot` is set, it MUST reference an existing snapshot.
- If both `since_snapshot` and `until_snapshot` are set, their ordering MUST be respected in the snapshots timeline.

## V. Role Coherence Invariants

V-1. Holder existence
- Role holders MUST exist at the time the role is granted.
Granting a role to a retired entity MUST be rejected.

V-2. Revocation enforcement
- If a role assignment has a `revocation` condition_set, then:
  - whenever the role is evaluated at a snapshot, if revocation conditions hold, the role MUST be considered inactive.
A validator MAY implement this as:
  - automatic role revocation transitions, or
  - computed role activity at query time.
The behavior MUST be consistent and documented.

V-3. Role uniqueness (optional profile rule)
- Profiles MAY require role uniqueness per role type (e.g., only one `CityGovernor` at a time).
Absent such a profile, the validator SHOULD warn, not reject.

## VI. Snapshot and Timeline Invariants

VI-1. Timeline ordering
- `snapshots.timeline` MUST be strictly increasing by `time_utc`.
- Snapshot IDs MUST be unique and stable.

VI-2. Hash integrity (if used)
- If hashes are used, a validator SHOULD verify they match canonicalized content.
If hashes are placeholders, validator MAY skip.

VI-3. Snapshot derivation
- If a snapshot has `derived_from_transition`, the referenced transition MUST exist.
- There SHOULD be a 1:1 mapping between applied transitions and derived snapshots in strict mode.

## VII. Correspondence Mode Invariants (if correspondence is present)

VII-1. Turn timeboxes non-overlap
- Turn timeboxes SHOULD NOT overlap unless explicitly allowed by the correspondence profile.

VII-2. Submission actors exist
- Every `submission.actor` MUST reference an existing character entity.

VII-3. Conflict policy declared
- A correspondence profile SHOULD specify a conflict policy (initiative, priority, random, DM arbitration).
If absent, validator MUST warn.

## VIII. Conformance Levels

- Level A (Structural): JSON Schema valid.
- Level B (Ontological): Structural + invariants II–VI satisfied.
- Level C (Correspondence): Ontological + invariants VII satisfied (if correspondence enabled).

A validator MUST report conformance level and any violations with references to JSON Pointer paths.
