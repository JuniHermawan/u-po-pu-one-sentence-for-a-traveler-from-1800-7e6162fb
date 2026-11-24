#!/usr/bin/env python3
"""One Sentence for a Traveler from 1800 (entry v1).

Writes a single sentence (at most 200 characters) that explains the modern
internet to a time traveler who has just stepped out of the year 1800,
using only things a person from 1800 already knows: a road, towns,
letters, books, voices. No word coined after their time.

Output: $MAKEFUN_OUTPUT_DIR/entry.txt (default /output/entry.txt).
Python 3.13 standard library only; deterministic; no network; no randomness.

Version history:
  v1 - initial sentence, calibrated against the judge brief (see NOTES.md):
       proxy win rate 0.617 overall, 0.85 against the strong control.
  v2 - hardened the one-sentence gate: it now counts every sentence
       terminator (. ! ?) instead of only periods, and rejects leading /
       trailing whitespace and double spaces, so a stray extra sentence or
       padding can never slip through the gate unnoticed.
"""

import os
import sys

# The entry sentence: 182 characters, one sentence, no post-1800 words.
SENTENCE = (
    "Picture a single road joining every town on earth, down which "
    "letters, books, and voices fly faster than a blink, so anyone may "
    "read, write, and speak with anyone, anywhere, at once."
)

# Words coined after 1800 that must never appear in the sentence.
FORBIDDEN_WORDS = (
    "computer", "network", "digital", "online", "screen", "email",
    "website", "internet", "software", "data", "wire", "electric",
    "telegraph", "telephone", "video", "download", "browser",
)

MAX_CHARS = 200


def self_check(text):
    """Gate: the sealed scorer requires UTF-8 text of 1-200 characters,
    not only whitespace. Returns a list of failure messages (empty = pass).
    """
    failures = []
    if not (1 <= len(text) <= MAX_CHARS):
        failures.append("length %d outside 1-%d" % (len(text), MAX_CHARS))
    if not text.strip():
        failures.append("text is only whitespace")
    if text != text.strip() or "  " in text:
        failures.append("text has padding or double spaces")
    terminators = sum(text.count(mark) for mark in ".!?")
    if terminators != 1 or text[-1] not in ".!?":
        failures.append("text is not exactly one sentence")
    lowered = text.lower()
    for word in FORBIDDEN_WORDS:
        if word in lowered:
            failures.append("post-1800 word present: %s" % word)
    return failures


def main():
    failures = self_check(SENTENCE)
    if failures:
        for failure in failures:
            print("gate failed: %s" % failure, file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.txt")
    with open(out_path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(SENTENCE)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
