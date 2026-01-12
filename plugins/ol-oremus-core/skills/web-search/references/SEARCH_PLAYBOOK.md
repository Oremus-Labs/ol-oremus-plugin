# Search Playbook

## 1) Intake checklist
- Confirm timeframe (today, last week, 2025, etc.).
- Confirm geography or locale if relevant.
- Identify product/version (avoid wrong docs).
- Note budget or pricing tier if comparing services.

## 2) Query templates
Start with 3-6 queries:
- Baseline: "<topic>".
- Synonym/alt name: "<topic>" OR "<alternate>".
- Authoritative: "<topic> site:gov" or known official domains.
- Recency: "<topic>" with time_range set.
- Docs/specs: "<topic> documentation" or "<topic> specification".
- Disconfirming: "<topic> problems" or "<topic> limitations".

## 3) Execution guidance
- Use `time_range=day` for breaking news.
- Use `time_range=month` for recently changed policies.
- Use `time_range=year` for stable topics with recent changes.
- If results are weak, broaden queries and remove time filter.

## 4) Shortlisting rubric
Pick 3-7 results, prioritizing:
- Primary sources (official docs, standards, press releases).
- Reputable independent outlets.
- Recency when the question is time-sensitive.

## 5) Deep read strategy
- Always run `readHeadings=true` first.
- Pull only the relevant section with `section` + `maxLength`.
- If needed, use `paragraphRange` for targeted extracts.

## 6) Synthesis
- Lead with the answer.
- Provide 3-6 evidence bullets with dates.
- Note uncertainties and limitations.
- Provide sources as a simple list of exact URLs read.
