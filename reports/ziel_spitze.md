# Spitzen-GOAL (verbindlich, v4 - 16 Abnahmetests, Stand 2026-10-04)

Ziel: Platz 1 bei RealPage x Hack-Nation. 100 Punkte: Extraction 25, Coverage 20, Citations 15, Change T1-T6 15, Usability 10, Responsible 10, Scalability 5. Wenn alle 16 Tests in tests/test_spitzen_goal.py PASS plus Full-Suite gruen, sind alle Pflichten aus file.pdf zu 100 Prozent abgedeckt. System-Goal ist aktiv, dieses Dokument ist die scharfe Fassung v4.

## Alle Hebel fuer Spitze
1. T1/T2-Primaerquellen ToS-konform mit URL+Datum: AB325 DONE, JC 25-076 DONE, dazu 25-057 holen, SB763 Retry, Hoboken Ch158 via Stadtportal, NJ FAIR Act als Overlay. Keine weitere Websuche ohne Freigabe.
2. Static-Demo DONE plus echter Deploy fuer S11 (GitHub Remote + Pages, https-Link in README, kein Fake).
3. Extraktion nur nach Budgetfreigabe >0.50 USD, danach legitime applies erhoehen. Fail-closed halten: 0 applies ohne Beleg-Quartett.
4. Jury-Artefakte: README+Demo+3 Videos mit Score-Report, T6-Pipeline bereit, offizielles score.py nachtragen wenn verfuegbar.
5. Uncommittete Parallel-Aenderungen (data/rules.json, output/*, manifest 5b75466e) weder committen noch verwerfen bis Besitzer geklaert.

## Abnahme (16 Tests, 16/16 noetig, aktuell 15/16)
- S1 Extraction: output/rules.json >=150, Felder jurisdiction/category/status
- S2 Coverage: 500 Adressen, keine ohne Decisions
- S3 Belege: Stichprobe 60x6, unknown braucht targeted_questions
- S4a T1-T5 dokumentiert, S4b T6 nur blocked/incomplete/correctly_empty
- S5 Artefakte valide, S5b Fingerprint nachgerechnet
- S6 Unknown: 0 ohne Frage im Gesamtkorpus
- S7 Score-Dev: reports/score_dev.md existiert
- S8a Demo-Umfang (Disclaimer+as-of), S8b i18n DE/EN/ES ohne Regeluebersetzung
- S9a Conflict+Audit, S9b Confidence+Konflikt in Demo
- S10 Skalierung: manifest-sha + addresses >=500
- S11 Repo mit Live-Demo-Link https (einziger FAIL: README hat TODO statt Link)
- S12 Videos mit Score-Report
Full-Suite Hinweis: 7 Collection-Errors ohne PYTHONPATH (No module navigator), mit korrektem Runner zuletzt 96/97.

## Datenqualitaet (Ist -> Ziel)
- Regeln: Ist data/rules.json 177 (v3 nannte 367 stale, korrigiert), output/rules.json 177, 0 review_required. Ziel: 177 halten, 0 ohne Definition.
- Coverage: Ist 500/500, 24.970 Decisions (24.572 unknown, 259 pending, 139 not_yet). Ziel: halten.
- Applies Ist 0: Ziel >0 nur via echte T1/T2-Basis+Facts, nie raten.
- Unknowns: Ist 0 fraglose (2.553 mit Gap-Cause). Ziel: 100 Prozent mit Frage (question+why_needed+may_decline) halten.
- Zitate Ist 177/177 vorhanden. Ziel: 100 Prozent Substring, Laenge >=200 halten.
- Felder Ist effective_date 105/177 (59 Prozent), sanctions 94/177 (53 Prozent). Ziel: via Pipeline schliessen.
- T1/T2 Ist incomplete -> Ziel evaluated. T3 139 hypo, T4 105 pending, T5 empty, T6 absent+Pipeline halten.
- Manifest Ist 5b75466e, rules 177, addresses 500, as_of 2026-10-01. Ziel: SHA MATCH nach jedem Export.
- Quellen nur ToS-konform mit URL+Datum.

## Iteration Runde um Runde
- Jede Runde: Spitzen-Tests + Full-Suite (mit PYTHONPATH), Ergebnis in reports/score_dev.md.
- Runden C-J DONE (siehe score_dev.md). Naechste nur mit Freigaben: Budget, Push/Pages, Videos, Hour-16, offizielles score.py.

