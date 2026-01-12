# Troubleshooting

## SEARXNG_URL misconfigured
Symptoms:
- Immediate failures or empty search results for all queries.
Actions:
- Verify MCP server configuration and base URL.
- Run a known-good query to validate connectivity.

## Rate limiting (429)
Actions:
- Reduce query volume.
- Add small delays between searches.
- Retry with fewer queries and narrower scope.
- If persistent, run `/home/sbuglione/.claude/skills/web-search/scripts/searxng_rate_limit_recovery.sh`.

## 403/404 errors
Actions:
- Prefer alternate sources.
- Try a different site with the same claim.
- Confirm the URL is current.

## Timeouts
Actions:
- Use simpler pages or official docs.
- Try `readHeadings=true` first, then a smaller section.

## Empty HTML-to-Markdown conversions
Actions:
- Use a static or PDF source for the same claim.
- Try a mirror or alternative documentation site.

## Reducing token usage
- Start with `readHeadings=true`.
- Use `section` for targeted reads.
- Use `paragraphRange` for specific segments.
- Use `startChar`/`maxLength` for chunking long pages.
