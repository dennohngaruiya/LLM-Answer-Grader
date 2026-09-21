"""grader.cli — command line entry point.

Examples
--------
  python -m grader evaluate data/sample_outputs.json
  python -m grader evaluate cases.json --html report.html --md report.md --json report.json
  python -m grader evaluate cases.json --fail-under 75      # CI gate (exit 1 if below)
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .report import to_html, to_json, to_markdown
from .scorer import evaluate_many


def _load(path: str) -> list[dict]:
    data = json.loads(Path(path).read_text())
    if isinstance(data, dict) and "cases" in data:
        data = data["cases"]
    if not isinstance(data, list):
        raise SystemExit("input must be a JSON list of cases, or {\"cases\": [...]}")
    return data


def cmd_evaluate(args: argparse.Namespace) -> int:
    cards = evaluate_many(_load(args.input))
    if not cards:
        print("no cases found", file=sys.stderr)
        return 2

    if args.html:
        Path(args.html).write_text(to_html(cards))
    if args.md:
        Path(args.md).write_text(to_markdown(cards))
    if args.json:
        Path(args.json).write_text(to_json(cards))

    # always print the markdown summary to stdout so the tool is useful in a terminal
    print(to_markdown(cards))

    avg = sum(c.total for c in cards) / len(cards)
    if args.fail_under is not None and avg < args.fail_under:
        print(f"\n✗ average {avg:.1f} is below the required {args.fail_under}", file=sys.stderr)
        return 1
    print(f"\n✓ {len(cards)} case(s) graded · average {avg:.1f}/100")
    return 0


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="grader", description="Give AI answers a report card.")
    sub = p.add_subparsers(dest="cmd", required=True)

    e = sub.add_parser("evaluate", help="grade a JSON file of cases")
    e.add_argument("input", help="path to cases JSON")
    e.add_argument("--html", help="write a self-contained HTML report here")
    e.add_argument("--md", help="write a Markdown report here")
    e.add_argument("--json", help="write machine-readable results here")
    e.add_argument("--fail-under", type=float, default=None,
                   help="exit 1 if the average score is below this (for CI)")
    e.set_defaults(func=cmd_evaluate)

    args = p.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
