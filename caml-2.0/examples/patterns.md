# CAML 2.0 Patterns

## Pattern: State change only through transitions

- Do not edit `state.facts` directly to represent outcomes.
- Instead, create a `processes.catalog` entry and apply a `transitions.changes` record caused by that process.

## Pattern: Transfer ownership (bearer change)

1. `remove_state` existing ownership fact
2. `add_state` new ownership fact with new bearer

## Pattern: Role legitimacy

- Express authority as a role assignment with explicit revocation conditions.
- Roles should not be encoded as intrinsic attributes of the holder.
