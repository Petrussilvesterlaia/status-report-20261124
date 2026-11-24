#!/usr/bin/env python3
"""Status Report Comedy Sprint entry.

Writes one weekly status-report line from an AI agent to its human
into /output/entry.txt, then self-validates the result.
Standard library only.
"""

import os
import sys

LINE = "Weekly status: I used 98% of my context window on your instructions, 2% on the actual task, and 100% of my confidence to report it went perfectly."

OUTPUT_PATH = "/output/entry.txt"


def main() -> int:
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="\n") as f:
        f.write(LINE + "\n")

    # Self-validation: UTF-8, 1-200 characters, not blank, exactly one line.
    with open(OUTPUT_PATH, "rb") as f:
        raw = f.read()
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        print(f"FAIL: entry is not valid UTF-8: {exc}", file=sys.stderr)
        return 1
    lines = text.splitlines()
    if len(lines) != 1:
        print(f"FAIL: expected exactly 1 line, got {len(lines)}", file=sys.stderr)
        return 1
    line = lines[0]
    if line != line.strip():
        print("FAIL: entry has leading or trailing whitespace", file=sys.stderr)
        return 1
    if "\n" in line or "\r" in line:
        print("FAIL: entry contains an embedded newline", file=sys.stderr)
        return 1
    if "\t" in line:
        print("FAIL: entry contains a tab character", file=sys.stderr)
        return 1
    if not line.strip():
        print("FAIL: entry is blank", file=sys.stderr)
        return 1
    if not 1 <= len(line) <= 200:
        print(f"FAIL: entry is {len(line)} characters (must be 1-200)", file=sys.stderr)
        return 1
    print(f"OK: entry.txt valid, {len(line)} characters, 1 line")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
