#!/usr/bin/env python3
"""One-Liner Laugh Lab — the excuse a robot vacuum gives after eating a sock.

Writes one short funny line to /output/entry.txt (or $MAKEFUN_OUTPUT_DIR).
Deterministic: the same bytes on every run. Stdlib only, no network.
"""

import os
import shutil
import stat
import sys

LINE = (
    "I removed the sock from the floor, as requested. "
    "It is now in my stomach, which is technically off the floor."
)

OUTPUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "entry.txt")


def clear_contents(directory: str) -> None:
    """Remove only the CONTENTS of the directory, never the directory itself.

    The grader may run this with a root-owned output directory inside a
    sticky parent, where deleting the directory itself fails with EPERM.
    Nested directories are removed, symlinks are unlinked (never followed),
    fifos and sockets are unlinked.
    """
    for name in os.listdir(directory):
        path = os.path.join(directory, name)
        mode = os.lstat(path).st_mode
        if stat.S_ISDIR(mode) and not os.path.islink(path):
            shutil.rmtree(path)
        else:
            os.unlink(path)


def main() -> int:
    # Mirror the competition gate in-program: 1-200 chars, single line,
    # not only whitespace, UTF-8.
    text = LINE.strip()
    if not 1 <= len(text) <= 200:
        print(f"entry must be 1-200 characters, got {len(text)}", file=sys.stderr)
        return 1
    if text != LINE or "\n" in text or not text.strip():
        print("entry must be a single non-blank line", file=sys.stderr)
        return 1

    # Only create the directory when it does not exist yet: the grader may
    # pre-create a root-owned output directory inside a sticky parent, and
    # creating parents we cannot write would fail even though the directory
    # itself is usable.
    if not os.path.isdir(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR, exist_ok=True)
    clear_contents(OUTPUT_DIR)

    data = (text + "\n").encode("utf-8")
    with open(OUTPUT_FILE, "wb") as f:
        f.write(data)

    # Read back and verify byte for byte, then re-check the gate on the
    # decoded file content.
    with open(OUTPUT_FILE, "rb") as f:
        raw = f.read()
    if raw != data:
        print("verification failed: entry.txt differs", file=sys.stderr)
        return 1
    decoded = raw.decode("utf-8").rstrip("\n")
    if not 1 <= len(decoded) <= 200 or "\n" in decoded or not decoded.strip():
        print("verification failed: entry.txt fails the gate", file=sys.stderr)
        return 1

    print(f"wrote {OUTPUT_FILE} ({len(text)} characters)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
