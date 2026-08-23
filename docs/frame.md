# The frame — container for OKF tooling

This fork of [`GoogleCloudPlatform/open-knowledge-format`](https://github.com/GoogleCloudPlatform/open-knowledge-format)
is the **tooling container ("the frame")** for the knowledge base. The
knowledge itself lives elsewhere, in per-domain content repositories.

## Architecture

- **Container (this repo):** OKF tooling — upstream mechanics (`SPEC.md`,
  `src/reference_agent` bundle/viewer/web) plus this repo's delta. Public,
  Apache-2.0, native upstream tracking via `git pull upstream`.
- **Content:** one private repository per domain bundle, always 1:1
  (`kb-lab`, `kb-personal`, …). Pure markdown/YAML — no code, no tooling.
  Each repository is its own access boundary: a domain can be published
  independently without exposing any other (operating-system- and
  platform-level views and security).

The container/content split is deliberate:

- **Isolation** — domains (e.g. lab vs personal) are physically distinct
  repositories; nothing crosses the boundary by construction.
- **Flexibility** — each domain clones, versions, and syncs independently.
- **Tooling lifecycle** — upstream changes merge into the container without
  churning any content repository.

## Why a fork, not a derived copy

Native upstream sync: Google's validator and spec changes arrive via
`git pull upstream`, with no maintenance burden of a hand-maintained copy.

## Sync purity rule

**Upstream files are never edited in this repository.** Our delta lives in
non-colliding directories, so `git pull upstream` stays conflict-free by
construction:

```
tools/okf/            CLI (validate/index/visualize) + fixtures + spike report
docs/                 this document
```

## Delta layout

| Path | Purpose |
|---|---|
| `tools/okf/cli.py` | `okf` CLI; self-locating (imports `src/reference_agent` via repo-root `src/`). Needs only `pyyaml` + `markdownify`; the fork's own pyproject (google-adk, bigquery) is never installed |
| `tools/okf/README.md` | setup + usage |
| `tools/okf/fixtures/ste-compat/` | Gate-B fixture: an STE-style document as an OKF concept |
| `tools/okf/SPIKE-REPORT.md` | spike evidence (2026-08-23) |
| `docs/frame.md` | this document |

## Usage

See `tools/okf/README.md`. The upstream sample bundles (`bundles/`) double as
reference fixtures for the CLI.

## Reshape candidates (under review)

1. ~~Patch the upstream viewer to skip `log.md`~~ **DONE (2026-08-23):**
   upstream's viewer only skipped `index.md`, so `log.md` rendered as a
   phantom "Unknown" node. One-line divergence applied in the fork
   (`viewer/generator.py` `_walk_concepts`); `acme_retail` visualize now
   reports 9 concepts (was 10). If upstream ever rewrites that walker,
   expect a trivial merge conflict.
2. Richer `validate`: timestamp-format conformance, reserved-name checks,
   link-target resolution, frontmatter/body metadata sync.
3. STE corpus adapter: read `kind`/`domain`/`standard_version` from
   frontmatter instead of the body echo block (removes the only metadata
   duplication).
4. Viewer palette: upstream hardcodes BigQuery colors; a generic palette.
5. Per-bundle `bundle_meta` declaration (SPEC §6).

## Attribution

Fork of `GoogleCloudPlatform/open-knowledge-format` at commit `ad30107c`
(Apache-2.0; Copyright 2026 Google LLC — see `LICENSE.md`). The `tools/okf/`
delta is by phoenixson, 2026-08-23.
