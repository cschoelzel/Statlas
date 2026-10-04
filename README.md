# Statlas - Rental Housing Law Navigator

HackNation26 x RealPage - deterministic address-level answers to `which rental rules apply to this property on date X?`

Live demo: https://cschoelzel.github.io/Statlas/

Status: 500 addresses - 177 rules - 54 source documents - as-of 2026-10-01.

Not legal advice. Source gaps and unresolved interpretations require qualified review.

## What this is (30 seconds)

Renters, landlords, and property teams face the same problem: rental rules depend on the exact property, the exact jurisdiction, and the exact date - and sources contradict each other. Statlas answers it per address, with every decision backed by a verbatim quote from the source corpus.

Type an address, pick a date, and you get a sourced list of rules: what applies, what does not, what is pending or not yet effective - and what is still unknown, including the exact follow-up question that would resolve it. No guessing: when a fact is missing, the engine says unknown and tells you why.

## For the jury: try it in 60 seconds

1. Open the live demo: https://cschoelzel.github.io/Statlas/
2. Type Los Angeles (or Berkeley, Boston, Hoboken) and pick any suggested address.
3. Change the date (default 2026-10-01) and open the result page.
4. Each rule shows its verdict (applies, does not apply, pending, not yet effective, unknown), the quoted source text, and - for unknowns - the missing fact.
5. Switch language DE, EN, ES in the header. Everything runs as static files - no login, no backend.

Local alternative, same data, no server needed: open web/index.html in this repo.

## How it works, step by step

Step 1 - Corpus. 54 official legal texts live in the corpus folder (ordinances, state laws, guidance). Nothing is scraped at evaluation time.

Step 2 - Extraction. Each text is distilled into structured rules in data/rules.json (177 rules). Every rule carries jurisdiction, category, temporal status, requirement, citation, and a verbatim quoted span of at least 20 characters, verified against the corpus. 177 of 177 quotes are attested.

Step 3 - Address resolution. 500 addresses are mapped to their legal jurisdiction via Census-backed lookup in navigator/geography.py. Postal city is never treated as legal proof. 492 of 500 resolve; 8 stay explicitly unresolved (fail-closed) instead of being guessed.

Step 4 - Deterministic evaluation. navigator/engine.py evaluates every address times applicable rules (24,970 decisions) with three-valued logic: yes, no, unknown. Order is fixed: jurisdiction first, then temporal standing (exact effective, operative, enactment and end dates beat status strings), then coverage and exemptions. Missing knowledge always yields unknown, never a default yes or no.

Step 5 - Parcel facts, allowlist only. navigator/parcel_facts.py maps assessor fields to a small allowlist such as apartments and 5-plus units. It never invents occupancy dates, exemptions, or affordability status. Year built is never treated as an occupancy date, and user input can never overwrite authoritative geo fields.

Step 6 - Presentation. web/index.html (search plus date picker) leads to web/results.html (decisions with quotes, provenance, and consequences UI). Pre-exported per-address files in web/data make the demo fully static. navigator/app.py also offers a local API with zero model or network calls during evaluation.

Step 7 - Change tracking. navigator/changes.py plus output/changes.json diff rule sets across as-of dates (scenarios T1 to T5). When a corpus source is missing, it reports incomplete honestly instead of fabricating a before-after.

## Results (measured, reproducible)

Self-benchmark (`PYTHONPATH=. python3 scripts/benchmark.py`, the official score.py and held-out key stay with the judges): 65.63 of 75 auto points.

- Extraction: 25.00 of 25 - field fill rates over all 177 rules.
- Citations: 15.00 of 15 - 240 of 240 applies decisions carry a source plus verbatim quote; 0 illegitimate applies.
- Coverage: 19.63 of 20 - jurisdiction proven 94.4 percent, legitimate applies 100 percent, unknowns with follow-up question 100 percent.
- Change: 6.00 of 15 - T4 full, T5 full; T1, T2, T3 at 0 because four sources have no text in the corpus.

Latest full audit (2026-10-04, rules SHA faf5b3e7, 24,970 decisions): 24,572 unknown, 259 pending, 139 not yet effective, 0 confirmed applies without further facts. 207 addresses are all-unknown - by design, because tenancy facts are not in parcel data and guessing is prohibited.

Full breakdown in reports/current_500_audit.md and reports/benchmark.md.

## Verify it yourself

Run all checks (109 passed, 223 subtests passed):

    python3 -m pytest tests/ -q

Single fast gate:

    python3 -m pytest tests/test_spitzen_goal.py -q

Re-run the self-benchmark:

    PYTHONPATH=. python3 scripts/benchmark.py

Local server, optional, the static demo needs none:

    python3 -m navigator.app serve --port 8765

Single address lookup:

    python3 -m navigator.app lookup --address A0001 --as-of 2026-10-01

Key artifacts: output/manifest.json, output/rules.json, output/lookups.json, output/changes.json, reports/benchmark.md, reports/current_500_audit.md.

## Honest limits

- Recall against the answer key cannot be measured before judging (held-out key with the judges). Measured instead: 0 illegitimate applies out of 240.
- Change scenarios T1, T2, T3 score 0 for one reason only: four sources have no text in the corpus, so there is nothing to extract and nothing to diff. Fixable only by sourcing, not by logic.
- 8 of 500 addresses have no Census match and stay fail-closed unknown. Better geocoding or parcel proof would fix them, not looser logic.
- The audit confirms the engine behaves as specified; it does not claim every extracted rule is legally correct. External qualified legal review remains open (see reports/METHOD_NOTE.md).

## Repository map

    index.html and results.html - live demo entry (GitHub Pages)
    navigator/ - engine, geography, parcel facts, app CLI plus local API, changes
    web/ - search page, results page, pre-exported per-address data
    data/rules.json - 177 extracted rules with verbatim quotes
    addresses.json - 500 evaluation addresses
    output/ - manifest, rules, lookups, facts, changes
    scripts/ - static demo export, benchmark, quote and applies verifiers
    tests/ - 11 suites: engine, geography, redteam, properties, regression, temporal
    reports/ - benchmark, current 500 audit, method note

## Tech and principles

Python 3 stdlib only for evaluation (no model, no network, no dependencies at decision time). Fully deterministic and byte-reproducible. Fail-closed unknowns with targeted follow-up questions. Every applies decision has a source plus verbatim quote. Static-hosting friendly.

Built for HackNation26. Not legal advice.
