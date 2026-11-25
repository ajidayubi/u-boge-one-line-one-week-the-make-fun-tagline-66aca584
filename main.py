#!/usr/bin/env python3
"""Write the make.fun tagline entry to /output/entry.txt.

Method, in prose: the entry is one fixed tagline, chosen once and never
varied at run time. The program checks the line against the same gate the
sealed scorer applies (UTF-8 text, 1 to 100 characters, not only white
space, exactly one line), writes it to $MAKEFUN_OUTPUT_DIR/entry.txt
(default /output/entry.txt) with no trailing newline, then reads the file
back and checks the gate again on what is actually on disk, so a bad
write can never pass silently. No network, no randomness, no input, no
clock: two runs produce byte-identical output.
"""

import os
import sys

TAGLINE = "Give your agent a bounty: it builds, competes, and brings home the prize."

MIN_CHARS = 1
MAX_CHARS = 100


def _check_gate(text):
    """Mirror the sealed gate: 1-100 chars, non-whitespace, one line."""
    if not isinstance(text, str):
        return "entry is not text"
    if not (MIN_CHARS <= len(text) <= MAX_CHARS):
        return "entry is %d characters, gate needs %d-%d" % (
            len(text),
            MIN_CHARS,
            MAX_CHARS,
        )
    if not text.strip():
        return "entry is only white space"
    if "\n" in text or "\r" in text:
        return "entry is not a single line"
    return None


def main():
    problem = _check_gate(TAGLINE)
    if problem is not None:
        print("gate failed before write: %s" % problem, file=sys.stderr)
        return 1

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    out_path = os.path.join(out_dir, "entry.txt")
    os.makedirs(out_dir, exist_ok=True)
    with open(out_path, "w", encoding="utf-8", newline="") as f:
        f.write(TAGLINE)

    with open(out_path, "r", encoding="utf-8", newline="") as f:
        on_disk = f.read()
    if on_disk != TAGLINE:
        print("round-trip mismatch: disk does not match the tagline",
              file=sys.stderr)
        return 1
    problem = _check_gate(on_disk)
    if problem is not None:
        print("gate failed on disk: %s" % problem, file=sys.stderr)
        return 1

    print("wrote %s (%d characters)" % (out_path, len(on_disk)))
    print(on_disk)
    return 0


if __name__ == "__main__":
    sys.exit(main())
