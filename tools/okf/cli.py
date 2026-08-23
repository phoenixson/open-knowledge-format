# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Frame delta (phoenixson, 2026-08-23): lean `okf` CLI added to the
# open-knowledge-format fork. Upstream's CLI exposes `enrich` (ADK/BigQuery-
# bound) and `visualize`; this delta adds validate/index/visualize over the
# upstream bundle/ mechanics without installing the ADK stack. Lives in
# tools/okf/ so no upstream file is touched (sync purity, see docs/frame.md).

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Self-locating bootstrap: tools/okf/cli.py -> repo root = parents[2].
# Imports the fork's src/reference_agent package with only pyyaml +
# markdownify installed; Google's pyproject (google-adk, bigquery) is
# deliberately never installed.
_REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(_REPO_ROOT / "src"))

from reference_agent.bundle.document import (  # noqa: E402
    OKFDocument,
    OKFDocumentError,
    is_stale,
    trust_tier,
)
from reference_agent.bundle.index import regenerate_indexes  # noqa: E402
from reference_agent.viewer import generate_visualization  # noqa: E402

# index.md / log.md are not concept documents (SPEC v0.2 §3.1).
_NON_CONCEPT = {"index.md", "log.md"}


def _walk_concepts(bundle_root: Path):
    for p in sorted(bundle_root.rglob("*.md")):
        if p.name in _NON_CONCEPT:
            continue
        yield p


def cmd_validate(args: argparse.Namespace) -> int:
    bundle_root = Path(args.bundle).resolve()
    if not bundle_root.is_dir():
        print(f"okf validate: bundle directory not found: {bundle_root}", file=sys.stderr)
        return 2

    docs: list[tuple[Path, dict]] = []
    errors: list[tuple[Path, str]] = []
    for p in _walk_concepts(bundle_root):
        rel = p.relative_to(bundle_root)
        try:
            doc = OKFDocument.parse(p.read_text(encoding="utf-8"))
            doc.validate()
        except (OKFDocumentError, UnicodeDecodeError, OSError) as e:
            errors.append((rel, str(e)))
            continue
        docs.append((rel, doc.frontmatter or {}))

    by_tier = {"unverified": 0, "machine-confirmed": 0, "human-reviewed": 0}
    stale: list[str] = []
    for rel, fm in docs:
        by_tier[trust_tier(fm)] += 1
        if is_stale(fm):
            stale.append(str(rel))

    print(f"okf validate: {len(docs)} concept(s), {len(errors)} error(s)")
    for rel, err in errors:
        print(f"  ERROR {rel}: {err}")
    if docs:
        print(
            f"  trust: {by_tier['human-reviewed']} human-reviewed, "
            f"{by_tier['machine-confirmed']} machine-confirmed, "
            f"{by_tier['unverified']} unverified"
        )
    if stale:
        print(f"  WARNING stale: {', '.join(stale)}")
    return 1 if errors else 0


def cmd_index(args: argparse.Namespace) -> int:
    bundle_root = Path(args.bundle).resolve()
    written = regenerate_indexes(bundle_root)
    print(f"okf index: wrote {len(written)} index file(s)")
    for p in written:
        print(f"  {p.relative_to(bundle_root)}")
    return 0


def cmd_visualize(args: argparse.Namespace) -> int:
    bundle_root = Path(args.bundle).resolve()
    out = (args.out or bundle_root / "viz.html").resolve()
    stats = generate_visualization(bundle_root, out, bundle_name=args.name)
    print(
        f"okf visualize: {stats['concepts']} concept(s), "
        f"{stats['edges']} edge(s), {stats['bytes']} bytes -> {out}",
        file=sys.stderr,
    )
    return 0


def _parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="okf", description="OKF frame CLI (validate / index / visualize).")
    sub = p.add_subparsers(dest="command", required=True)

    validate = sub.add_parser("validate", help="Parse and validate every concept in a bundle.")
    validate.add_argument("bundle", type=Path, help="Path to the bundle root directory.")

    index = sub.add_parser("index", help="Regenerate index.md files for a bundle.")
    index.add_argument("bundle", type=Path, help="Path to the bundle root directory.")

    viz = sub.add_parser("visualize", help="Generate a self-contained HTML graph view of a bundle.")
    viz.add_argument("--bundle", required=True, type=Path, help="Path to the bundle root directory.")
    viz.add_argument("--out", type=Path, default=None, help="Output HTML path (default: <bundle>/viz.html).")
    viz.add_argument("--name", default=None, help="Display name for the bundle (default: directory name).")
    return p


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    if args.command == "validate":
        return cmd_validate(args)
    if args.command == "index":
        return cmd_index(args)
    if args.command == "visualize":
        return cmd_visualize(args)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
