# CAML 1.x vs CAML 2.0 (Quick Orientation)

## CAML 1.x
- Adventure data mixes entities, state, and events
- Excellent for human use, hard for strict tooling
- Implicit causality and time

## CAML 2.0
- Explicit ontological layers (world/state/roles/processes/transitions/snapshots)
- All persistent change occurs via transitions caused by processes
- Designed for correspondence play, traceability, and validation

## Migration approach (recommended)
- Keep CAML 1.x stable
- Add CAML 2.0 as `/caml-2.0`
- Provide a 1.x -> 2.0 mapping script later (best-effort), and a validator for invariants
