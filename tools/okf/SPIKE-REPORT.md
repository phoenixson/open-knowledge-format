# Spike report — OKF mechanics & STE compatibility (2026-08-23)

**Goal:** validate, before any configuration investment (Libby, Orchestrator
KB work), that (a) the OKF bundle mechanics work as a standalone toolchain
and (b) the established STE document style can be wrapped as OKF concepts
**without conflicts**.

The spike was executed on a clean-room frame, then adopted into this fork as
the final container (see `docs/frame.md`). Evidence below is from that run,
re-verified against this repository.

## Gate A — mechanics (PASS)

| Check | Result |
|---|---|
| Upstream mechanics tests, trimmed toolchain | **22/22 passed** (test_document, test_index, test_viewer, test_web_fetcher) |
| `okf validate bundles/acme_retail` | 9 concepts, 0 errors; 8 human-reviewed, 1 unverified; exit 0 |
| `okf index bundles/acme_retail` | 6 index files regenerated offline (deterministic fallback) |
| `okf visualize bundles/acme_retail` | 9 concepts / 6 edges → self-contained `viz.html` (~43 KB) |

## Gate B — STE document-style compatibility (PASS)

Test artifact: `# Data Object: TaskCard` (an STE data-object seed) wrapped as
an OKF concept — metadata frontmatter-canonical (`type`, `title`,
`description`, `resource`, `kind`, `domain`, `standard_version`,
`generated`/`verified`, `status`, `stale_after`, `sources[]`); body carries
the STE H1, bold-label block, and `## Purpose/Fields/Example/Validation/
Relationships` sections.

| Check | Result |
|---|---|
| `okf validate` on the wrapped concept | 1 concept, 0 errors; human-reviewed; exit 0 |
| Round-trip fidelity | parse → serialize → parse: frontmatter + body byte-identical; ISO-8601 strings (`…T12:00:00-04:00`, `…T00:00:00Z`) survive **verbatim** (custom YAML loader, no YAML-1.1 timestamp coercion) |
| STE corpus extractor (unchanged, zero adapter) | full record: `type: data_object`, headers `{Kind, Domain, Source, Standard version}`, sections `[Purpose, Fields, Example, Validation, Relationships]` |

**Verdict: no conflict.** OKF's only hard requirement is `type`; extension
keys are first-class (SPEC §4.1: consumers MUST NOT reject unknowns); the STE
sections are ordinary body markdown.

## Findings

1. **`regenerate_indexes` overwrites curated index prose.** Treat `index.md`
   as a **generated artifact** — commit it, don't hand-edit (or add
   preserve-on-regen as a reshape).
2. **Upstream viewer does not skip `log.md`** (SPEC §3.1 reserved filename) —
   it renders as a phantom "Unknown" node in viz output. One-line fix,
   deferred to the reshape pass to keep the fork sync-clean
   (documented in `docs/frame.md`).
3. **The description synthesizer runs fully offline** — lazy genai import
   with a deterministic fallback. An LLM-backed version is a ~10-line adapt.

## Reshape candidates (operator's detailed review)

1. Patch viewer to skip `log.md` (accept the one-line divergence).
2. Richer `validate`: timestamp-format conformance, reserved-name checks,
   link-target resolution, frontmatter/body sync check.
3. STE corpus adapter: read `kind`/`domain`/`standard_version` from
   frontmatter → drop the body echo block (kills the only metadata
   duplication; frontmatter stays canonical either way).
4. Viewer palette: upstream hardcodes BigQuery colors; generic/STE palette.
5. Per-bundle `bundle_meta` declaration (SPEC §6): `okf_version`/frame/domain.

## Next steps

- Content repos: one private repo per domain bundle, 1:1 (first: `kb-lab`).
- Libby configuration — tooling = this CLI; contract = SPEC + intake rules.
- Orchestrator KB work — unchanged, after.
