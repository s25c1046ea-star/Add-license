# Copyright (c) 2026 Your Name
# SPDX-License-Identifier: MIT
"""Generate formatted excuse lines from situation memos read from stdin."""

from __future__ import annotations

import argparse
import json
import random
import sys
from typing import Sequence

TEMPLATES: dict[str, list[str]] = {
    "mild": [
        "{topic}の対応に手間取り、予定より少し遅れてしまいました。",
        "{topic}の確認作業が長引いたため、ご連絡が遅くなりました。",
        "{topic}の段取りを見直していたところ、時間がかかってしまいました。",
        "{topic}の関連資料を突き合わせていたら、思いのほか時間を要しました。",
    ],
    "dramatic": [
        "{topic}を巡る予期せぬ事態が重なり、時空の狭間で足止めを食らいました。",
        "{topic}の解決に全力を注いだ結果、気づけば時計の針が大きく進んでいました。",
        "{topic}の難局を突破するため極限の集中を要し、報告が遅延しました。",
        "{topic}にまつわる不可解なトラブルが連鎖し、復旧に時間を奪われました。",
    ],
}
def generate_excuse(topic: str, level: str, rng: random.Random) -> str:
    """Generate a single excuse string for a given topic and severity level."""
    cleaned = topic.strip()
    if not cleaned:
        raise ValueError("Input line must not be empty or whitespace-only.")
    candidates = TEMPLATES[level]
    template = rng.choice(candidates)
    return template.format(topic=cleaned)
def build_parser() -> argparse.ArgumentParser:
    """Create the CLI argument parser."""
    parser = argparse.ArgumentParser(
        prog="excuse-gen",
        description="Read situation memos from stdin and output formatted excuses to stdout.",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Random seed for reproducible output (recommended for testing).",
    )
    parser.add_argument(
        "--level",
        choices=("mild", "dramatic"),
        default="mild",
        help="Excuse tone level: 'mild' or 'dramatic' (default: mild).",
    )
    parser.add_argument(
        "--format",
        choices=("text", "tsv", "json"),
        default="text",
        dest="output_format",
        help="Output format: 'text', 'tsv', or 'json' (default: text).",
    )
    parser.add_argument(
        "--allow-empty",
        action="store_true",
        help="Skip empty lines instead of treating them as errors.",
    )
    return parser


def process_stream(
    lines: Sequence[str] | object,
    seed: int | None = None,
    level: str = "mild",
    output_format: str = "text",
    allow_empty: bool = False,
) -> list[str]:
    """Process an iterable of input lines and return formatted stdout lines."""
    rng = random.Random(seed)
    rendered: list[str] = []

    for line_no, raw_line in enumerate(lines, start=1):
        text = str(raw_line).rstrip("\r\n")
        if not text.strip():
            if allow_empty:
                continue
            raise ValueError(f"Line {line_no} is empty.")

        excuse = generate_excuse(text, level=level, rng=rng)
        if output_format == "text":
            rendered.append(excuse)
        elif output_format == "tsv":
            safe_topic = text.replace("\t", " ")
            safe_excuse = excuse.replace("\t", " ")
            rendered.append(f"{safe_topic}\t{safe_excuse}")
        elif output_format == "json":
            payload = {
                "input": text,
                "level": level,
                "excuse": excuse,
            }
            rendered.append(json.dumps(payload, ensure_ascii=False))
        else:
            raise ValueError(f"Unsupported output format: {output_format}")

    return rendered
def main(argv: Sequence[str] | None = None) -> int:
    """CLI entry point."""
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        output_lines = process_stream(
            sys.stdin,
            seed=args.seed,
            level=args.level,
            output_format=args.output_format,
            allow_empty=args.allow_empty,
        )
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    for item in output_lines:
        print(item, file=sys.stdout)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())