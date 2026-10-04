# Statlas

Rental Housing Law Navigator. I built this for HackNation26 x RealPage.

Live demo: https://cschoelzel.github.io/Statlas/

500 addresses. 177 rules. 54 source documents. Date: 2026-10-01.
Not legal advice.

## Try the demo

1. Open https://cschoelzel.github.io/Statlas/
2. Type Los Angeles, Berkeley, Boston or Hoboken into the search field.
3. Pick one of the suggested addresses.
4. Set a date. 2026-10-01 is the default. Then open the result.
5. You will see every matching rule with its result: applies, does not apply, pending, not yet effective, or unknown.
6. Each result shows the exact quote it came from. Unknown results tell you which fact is missing.
7. Use DE, EN or ES in the header to switch language.

No login. No backend. It all runs as static files.

## How I built it

1. I collected 54 official legal texts into a corpus.
2. I turned them into 177 structured rules. Each rule carries the word for word quote it came from.
3. I mapped 500 addresses to their legal jurisdiction with Census data. 492 matched. The other 8 stay marked unclear.
4. I wrote a small rule engine with three outcomes: yes, no, unclear. A missing fact means unclear. It never guesses.
5. I added parcel facts from assessor records, only where the mapping is safe.
6. I saved every address result as a static file, so the demo works without a server.

## Results

My own benchmark gives 65.63 of 75 points: extraction 25 of 25, citations 15 of 15, coverage 19.63 of 20, change 6 of 15. All 240 applies decisions carry a source quote. Full numbers are in reports/benchmark.md and reports/current_500_audit.md.

## Run it yourself

Run all checks:

    python3 -m pytest tests/ -q

Run only the fast gate:

    python3 -m pytest tests/test_spitzen_goal.py -q

Rerun the benchmark:

    PYTHONPATH=. python3 scripts/benchmark.py

Look up a single address:

    python3 -m navigator.app lookup --address A0001 --as-of 2026-10-01

Start the local server (optional, the demo needs none):

    python3 -m navigator.app serve --port 8765

Or open web/index.html straight in the browser. Same data, no server needed.
