---
name: web-search
description: "Perform accurate, efficient web research using the mcp-searxng MCP server. Use for fact-finding, news, documentation lookups, and comparisons that require citations. Includes rate-limit recovery steps for SearXNG."
compatibility: "Requires MCP server mcp-searxng with tools searxng_web_search and web_url_read. Optional: shell access with kubectl/argocd/curl for rate-limit recovery."
metadata:
  author: "codex"
  version: "0.1.0"
---

# Web Search Skill

## When to use this skill
Use this skill when the user asks for:
- Current events or time-sensitive information.
- Documentation or official guidance for technical topics.
- Product or service comparisons that require sources.
- Claims that need verification across multiple sources.
- Background or historical explanations with citations.

Do not use this skill when:
- The answer is already known from local context or files.
- The user only wants brainstorming or opinions.
- The user explicitly forbids web access.

## Tool interfaces (exact)
This skill assumes access to exactly these tools:
- `searxng_web_search` with inputs: `query` (required), `pageno` (optional), `time_range` (optional: day|month|year), `language` (optional, default all), `safesearch` (optional: 0|1|2).
- `web_url_read` with inputs: `url` (required), `startChar` (optional), `maxLength` (optional), `section` (optional), `paragraphRange` (optional), `readHeadings` (optional).

Important: `searxng_web_search` returns a formatted text block, not JSON. It must be parsed.

## Required workflow

### A) URL-first retrieval (when URLs are provided)
If the user message contains one or more URLs:
1) Do not use `WebFetch`/`Fetch`/`WebSearch`.
2) Call `web_url_read` for each URL.
3) If the content is truncated or the relevant section is missing, automatically re-read additional chunks using `startChar`/`maxLength` until the needed section is captured.
4) Only fall back to non-MCP retrieval if `web_url_read` fails, and only after asking the user to confirm.

### B) Intake and query shaping
1) Restate the user goal and constraints (timeframe, geography, version, budget).
2) Identify ambiguity and ask one concise clarifying question if needed; otherwise proceed with a labeled assumption.
3) Draft 3-6 queries:
   - Baseline query.
   - Synonyms or alternate names.
   - Authoritative sources query (site:gov, site:edu, or known publishers).
   - Recency-focused query if needed (set `time_range`).
   - Primary documentation query ("documentation", "spec", "release notes").
   - Optional disconfirming query ("problems", "limitations", "controversy").

### C) Search execution (searxng_web_search)
- Run the strongest 3-6 queries.
- Use `pageno=2` only if page 1 is weak or too homogeneous.
- Set `time_range` based on urgency:
  - day for breaking news.
  - month for recent changes.
  - year for stable topics where recency still matters.
- Use `language=all` unless the user requests a locale.
- Use `safesearch=0` by default unless the context requires stricter filtering.

### C) Result triage and de-duplication
- Parse the text output into entries: title, description, url, score.
- De-duplicate by URL and near-duplicate titles.
- Rank using relevance score, source credibility, recency, and topical diversity.
- Shortlist 3-7 URLs max.

### E) Deep reading (web_url_read)
For each shortlisted URL:
1) `web_url_read` with `readHeadings=true`.
2) Select the best heading and fetch with `section` plus `maxLength`.
3) If still too long, use `paragraphRange` or `startChar`/`maxLength` chunking.
4) Extract only the needed content.

### F) Synthesis and verification
- Cross-check critical claims with 2+ independent credible sources when stakes are high or numbers are involved.
- If sources conflict, present both and prioritize primary or official sources.

### G) Response format (user-facing)
1) Direct answer or recommendation (concise).
2) Key evidence (bullets, with dates if relevant).
3) Nuances, edge cases, or uncertainty.
4) Sources (simple list of exact URLs read via `web_url_read`).

### H) Failure modes and recovery
- If no results, broaden the query, remove time filters, or try synonyms.
- If a URL read returns empty, switch to a more accessible source.
- If paywalled, use other coverage or official summaries.

### I) Rate-limit recovery (SearXNG + VPN rotation)
Use this when search results return consistent 429/captcha errors or SearXNG fails repeatedly.

Run the recovery script (preferred, minimal context):
```
/home/sbuglione/.claude/skills/web-search/scripts/searxng_rate_limit_recovery.sh
```
The script swaps the active proxy pool first; if that fails it falls back to a full VPN rotate.

If shell access is not available, fall back to a lighter search strategy:
- Reduce queries to 1-2, wait 30-60 seconds between searches, and keep `time_range` broad.

If shell access is not available, fall back to a lighter search strategy:
- Reduce queries to 1-2, wait 30-60 seconds between searches, and keep `time_range` broad.

## Common pitfalls
- Treating search results as authoritative without reading them.
- Over-fetching pages instead of using headings and sections.
- Failing to note date/region context for news or pricing.
- Using a single source for factual claims.

## Examples

### 1) Breaking news
User: "What happened with the ExampleTech outage today?"

Queries to run:
```
searxng_web_search({"query":"ExampleTech outage today","time_range":"day"})
searxng_web_search({"query":"ExampleTech status update site:example.com","time_range":"day"})
searxng_web_search({"query":"ExampleTech outage report","time_range":"day"})
```

Shortlist criteria:
- Official status page or press release.
- Reputable news coverage with timestamps.

Read flow:
```
web_url_read({"url":"https://example.com/status","readHeadings":true})
web_url_read({"url":"https://example.com/status","section":"Incident summary","maxLength":4000})
```

Output: direct status summary, evidence bullets with timestamps, then sources.

### 2) Technical documentation lookup
User: "How do I enable logical replication in ProductDB 16?"

Queries to run:
```
searxng_web_search({"query":"ProductDB 16 logical replication documentation"})
searxng_web_search({"query":"ProductDB 16 logical replication site:docs.example.com"})
searxng_web_search({"query":"ProductDB logical replication settings"})
```

Shortlist criteria:
- Official docs.
- Release notes for version 16.

Read flow:
```
web_url_read({"url":"https://docs.example.com/productdb/16/replication","readHeadings":true})
web_url_read({"url":"https://docs.example.com/productdb/16/replication","section":"Configuration","maxLength":6000})
```

Output: steps and required parameters with citations.

### 3) Comparing products or services
User: "Compare ServiceA vs ServiceB pricing in 2025."

Queries to run:
```
searxng_web_search({"query":"ServiceA pricing 2025 site:servicea.example.com"})
searxng_web_search({"query":"ServiceB pricing 2025 site:serviceb.example.com"})
searxng_web_search({"query":"ServiceA vs ServiceB pricing comparison"})
```

Shortlist criteria:
- Official pricing pages.
- One reputable comparison source.

Read flow:
```
web_url_read({"url":"https://servicea.example.com/pricing","readHeadings":true})
web_url_read({"url":"https://servicea.example.com/pricing","section":"Plans","maxLength":5000})
```

Output: side-by-side bullets, note plan differences and dates.

### 4) Resolving conflicting claims
User: "Is ProductX end-of-life this year?"

Queries to run:
```
searxng_web_search({"query":"ProductX end of life announcement"})
searxng_web_search({"query":"ProductX support policy site:productx.example.com"})
searxng_web_search({"query":"ProductX EOL date"})
```

Shortlist criteria:
- Official lifecycle policy.
- Press release or release notes.
- Reputable news coverage.

Read flow:
```
web_url_read({"url":"https://productx.example.com/lifecycle","readHeadings":true})
web_url_read({"url":"https://productx.example.com/lifecycle","section":"End of life","maxLength":4000})
```

Output: cite official policy and reconcile discrepancies.

### 5) Historical/background explainer
User: "Why was ProtocolY created?"

Queries to run:
```
searxng_web_search({"query":"ProtocolY origin paper"})
searxng_web_search({"query":"ProtocolY specification history"})
searxng_web_search({"query":"ProtocolY background site:standards.example.org"})
```

Shortlist criteria:
- Original paper or spec.
- Standards body history.

Read flow:
```
web_url_read({"url":"https://standards.example.org/protocoly","readHeadings":true})
web_url_read({"url":"https://standards.example.org/protocoly","section":"History","maxLength":5000})
```

Output: summarize motivations with citations.

## Edge cases
- JS-heavy pages: prefer PDFs or static docs.
- Duplicate mirror sites: pick the primary source.
- Unknown region: ask or label assumption.

## See also
- references/TOOLING.md
- references/SEARCH_PLAYBOOK.md
- references/SOURCE_QUALITY.md
- references/CITATION_STYLE.md
- references/TROUBLESHOOTING.md
