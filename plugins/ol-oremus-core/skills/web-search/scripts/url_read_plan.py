#!/usr/bin/env python3
"""Plan a staged read for web_url_read based on headings.

Usage:
  Provide a JSON object with keys:
    - url
    - headings (list of strings)
    - maxLength (optional)

Outputs a simple plan indicating which heading to read and a fallback.
"""

import json
import sys


def choose_heading(headings):
    if not headings:
        return None
    # Prefer headings with common summary keywords.
    keywords = ("summary", "overview", "introduction", "abstract", "results", "conclusion")
    for h in headings:
        lh = h.lower()
        if any(k in lh for k in keywords):
            return h
    return headings[0]


def main():
    data = json.load(sys.stdin)
    url = data.get("url")
    headings = data.get("headings", [])
    max_len = data.get("maxLength", 6000)
    chosen = choose_heading(headings)
    plan = {
        "url": url,
        "readHeadings": True,
        "section": chosen,
        "maxLength": max_len,
        "fallback": "If section is too long, use paragraphRange or startChar/maxLength chunking."
    }
    json.dump(plan, sys.stdout, ensure_ascii=True, indent=2)


if __name__ == "__main__":
    main()
