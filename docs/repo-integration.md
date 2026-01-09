# Repo Integration Notes

## Suggested layout (additive)
- Keep existing CAML 1.x files intact
- Add:
  - `caml-2.0/` (this directory)
  - optional: `tools/validator/` and `tools/migrate/`

## Versioning
- Tag initial merge as `caml-2.0-draft`
- Add a changelog when schemas evolve

## Publishing schemas
- If you later publish schemas to GitHub Pages, update the `$id` fields accordingly.
