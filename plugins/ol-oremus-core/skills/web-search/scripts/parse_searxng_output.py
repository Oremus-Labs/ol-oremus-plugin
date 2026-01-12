#!/usr/bin/env python3
"""Parse searxng_web_search formatted output into JSON.

Input: text via stdin.
Output: JSON list of results.
"""

import json
import sys


def parse_blocks(text):
    blocks = [b.strip() for b in text.strip().split("\n\n") if b.strip()]
    results = []
    for block in blocks:
        item = {"title": None, "description": None, "url": None, "score": None}
        for line in block.splitlines():
            if line.startswith("Title:"):
                item["title"] = line[len("Title:"):].strip()
            elif line.startswith("Description:"):
                item["description"] = line[len("Description:"):].strip()
            elif line.startswith("URL:"):
                item["url"] = line[len("URL:"):].strip()
            elif line.startswith("Relevance Score:"):
                item["score"] = line[len("Relevance Score:"):].strip()
        if item["url"] or item["title"]:
            results.append(item)
    return results


def main():
    text = sys.stdin.read()
    data = parse_blocks(text)
    json.dump(data, sys.stdout, ensure_ascii=True, indent=2)


if __name__ == "__main__":
    main()
