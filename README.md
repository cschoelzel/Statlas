# Rental Housing Law Navigator (HackNation26 × RealPage)

Antwort auf eine Frage pro Adresse: welche Mietrechts-Regeln gelten hier heute, was aendert sich?
Module: A Extraktion (Korpus -> rules.json), B Lookup (Adresse -> Regeln mit Beleg), C Change-Tracking (T1-T6).

## Stand
- Korrektheit: 10/10 freigegeben (reports/ziel_100_prozent.md), Export-SHA siehe output/manifest.json
- Spitze: reports/ziel_spitze.md (16 Abnahmetests, v3), Tests: tests/test_spitzen_goal.py
- Dev-Score: reports/score_dev.md (offizielles score.py fehlt im Starter-Pack, Ersatzmetrik dokumentiert)
- Live-Demo-Link: TODO (deploy ausstehend) - Videos: reports/videos.md

## Repro
- python3 -m unittest discover -s tests
- Adressen: output/lookups.json (500), Regeln: output/rules.json, Changes: output/changes.json

## Architektur
- navigator/engine.py: fail-closed Regel-Evaluierung (lieber unknown + Frage als Raten)
- navigator/app.py: Lookup/Export mit Provenienz (facts.json)
- changes.py: T1-T6 inkl. hypothetically_affected + Konflikt-Flags
- web/: Demo (Suche -> Auswertung, as-of-Datum, Disclaimer)

## Limiten (ehrlich)
- T1/T2-Quellluecke (CA-ALG-01, HOB-ALG-01, JC-ALG-01 nicht im Korpus)
- T6 blockiert ohne Hour-16-Daten; 8 Adressen unresolved; 67+ Regeln mit Research-Fragen
- Not legal advice. Keine Rechtsberatung, nur Quellentransparenz.
