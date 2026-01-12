# Tooling Reference

This skill uses the MCP server mcp-searxng with two tools.
Optional operational tools (when available):
- `kubectl` for SearXNG/rotator diagnostics and manual rotation.
- `argocd` for sync checks (core mode).
- `curl` for rotator health/metrics endpoints.
- `/home/sbuglione/.claude/skills/web-search/scripts/searxng_rate_limit_recovery.sh` for one-shot recovery.

## Tool A: searxng_web_search
Purpose: search the web via SearXNG.

Inputs:
- query (string, required)
- pageno (number, optional, default 1)
- time_range (string, optional): one of day, month, year
- language (string, optional, default all)
- safesearch (string, optional, default 0)
  - 0: none, 1: moderate, 2: strict

Output behavior:
- Returns a single formatted text block, not JSON.
- Each result is a group of lines:
  - Title: ...
  - Description: ...
  - URL: ...
  - Relevance Score: ...
- Groups are separated by blank lines.

## Tool B: web_url_read
Purpose: fetch a URL and convert HTML to Markdown.

Inputs:
- url (string, required)
- startChar (number, optional, >= 0)
- maxLength (number, optional, >= 1)
- section (string, optional)
- paragraphRange (string, optional), e.g., "1-5", "3", "10-"
- readHeadings (boolean, optional)

Operational notes:
- Fetch timeout is around 10 seconds.
- JS-heavy pages may convert to empty text.
- Repeated reads are often faster due to caching.

## Parsing guidance for searxng_web_search output
- Split groups on blank lines.
- For each group, extract Title, Description, URL, Relevance Score.
- Handle missing fields gracefully (skip or mark as unknown).
- Strip extra whitespace.
