"""Command-line entry point for randline-cli."""
from __future__ import annotations

import argparse
import sys
from typing import List, Optional

from .core import reservoir_sample


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="randline-cli",
        description="Pick N random lines from a file or stdin, without replacement, "
        "using single-pass reservoir sampling.",
    )
    parser.add_argument("file", nargs="?", help="Path to read lines from (default: stdin)")
    parser.add_argument(
        "-n", "--number", type=int, default=1, help="Number of lines to pick (default: 1)"
    )
    parser.add_argument(
        "--seed", type=int, default=None, help="Random seed, for reproducible output"
    )
    return parser


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.number < 0:
        print("randline-cli: error: -n/--number must be non-negative", file=sys.stderr)
        return 2

    try:
        fh = open(args.file, "r", encoding="utf-8") if args.file else sys.stdin
    except OSError as exc:
        print(f"randline-cli: error: {exc}", file=sys.stderr)
        return 2

    try:
        lines = (line.rstrip("\n") for line in fh)
        selected = reservoir_sample(lines, args.number, seed=args.seed)
    finally:
        if args.file:
            fh.close()

    for line in selected:
        print(line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
