# okf — frame CLI (delta on the open-knowledge-format fork)

Lean CLI over the upstream `bundle/` mechanics: **validate / index /
visualize**. No ADK, no BigQuery, no Google dependencies — `pyyaml` +
`markdownify` only. Lives in `tools/okf/` so no upstream file is touched
(sync purity rule, see `docs/frame.md`).

## Setup

```sh
uv venv tools/okf/.venv
uv pip install -p tools/okf/.venv/bin/python pyyaml markdownify
```

## Usage

```sh
tools/okf/.venv/bin/python tools/okf/cli.py validate <bundle-root>
tools/okf/.venv/bin/python tools/okf/cli.py index <bundle-root>
tools/okf/.venv/bin/python tools/okf/cli.py visualize --bundle <bundle-root> [--name "..."]
```

- `validate` — parse + validate every concept (required `type` key; reports
  trust tiers and stale concepts; exit 1 on errors).
- `index` — regenerate `index.md` files (progressive disclosure; offline
  deterministic fallback for directory descriptions).
- `visualize` — write a self-contained `viz.html` graph (nodes carry
  trust/stale/verified/sources; edges are markdown links).

The CLI self-locates the fork's `src/reference_agent` package (repo-root
`src/` on `sys.path`), so it works without installing the fork's own
pyproject — which would pull `google-adk` and `google-cloud-bigquery`.

## Fixtures

- `fixtures/ste-compat/` — Gate-B proof: an STE-style document
  (`# Data Object: TaskCard`) wrapped as an OKF concept, showing the
  document-style compatibility validated in the 2026-08-23 spike.
  See `SPIKE-REPORT.md`.

## Upstream CLI comparison

| | upstream `reference-agent` | this `okf` |
|---|---|---|
| `enrich` (ADK/BigQuery) | yes | no (not needed) |
| `visualize` | yes | yes (same generator) |
| `validate` / `index` | library-only | CLI subcommands |
| deps | google-adk, bigquery, pydantic, markdownify, pyyaml | pyyaml, markdownify |
