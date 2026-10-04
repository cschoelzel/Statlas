# Statlas

Live demo: https://cschoelzel.github.io/Statlas/

## Try the demo

1. Open the demo link
2. Type Los Angeles, Berkeley, Boston or Hoboken in search
3. Pick an address suggestion
4. Keep the preset date or set your own date, then open result
5. You see every rule with applies, not applies, unclear or not yet effective
6. Every result shows the exact quote it came from
7. Switch DE, EN or ES in header

## How I built it

1. I collected 54 official texts in one corpus
2. I turned them into 177 rules, each with its exact quote
3. I mapped 500 addresses to jurisdiction with Census data, 492 matched
4. I wrote a small engine with yes, no and unclear, missing facts stay unclear
5. I exported all results as static files so Pages runs with no server

## Where this goes next

1. Full US coverage with the same pipeline, new laws plug in as new rules
2. Alerts for property teams when a rule changes for their addresses
3. API so existing tools can query per address and date
4. Unclear cases turn clear as I add more sourced facts

## Why it fits the criteria

1. Technical depth: full pipeline from source text to address result, tested and reproducible
2. Innovation: every result carries proof, unclear results name the missing fact
3. Impact: 500 addresses ready, built to scale to full US plus alerts plus API
4. Presentation: runs on Pages, search plus date plus result in under a minute, three languages

## Run the self test

Run all checks:

    python3 -m pytest tests/ -q

Rerun the benchmark:

    PYTHONPATH=. python3 scripts/benchmark.py

Look up one address:

    python3 -m navigator.app lookup --address A0001 --as-of 2026-10-01

Or open web/index.html straight in the browser.
