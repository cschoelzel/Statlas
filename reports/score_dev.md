# Dev-Score-Stand (ehrlich, 2026-10-04)

Offizielles score.py ist im Starter-Pack (participant-final-no-hour16 3/) NICHT enthalten
(nur schema + submission_templates + dev/change_tests.json). Daher kein offizieller Dev-Lauf moeglich.

Ersatzmetrik (eigene Suite, lokal): 70+ Tests gruen, inkl. tests/test_spitzen_goal.py (S1-S6, S9-S10 PASS).
Ersatzmetrik (eigene Suite, lokal): 70+ Tests gruen, inkl. tests/test_spitzen_goal.py 15/16 (Stand 2026-10-04, Runde A+B unabhaengig validiert).
Einziger FAIL: S11 (README ohne Live-Demo-Link) — nur per echtem Deploy loesbar, kein Fake-Link.
Test-Hygiene: ResourceWarnings in test_spitzen_goal.py behoben (with-Blocks), Lauf mit -W error::ResourceWarning bestaetigt.
Geografie: 8/500 Adressen unresolved (A0098, A0128, A0295, A0346, A0352, A0376, A0380, A0384) — Census-Geocoder ohne Match trotz Retry, als unknown fail-closed, kein Raten.
T1/T2 ehrlich incomplete (CA-ALG-01, HOB-ALG-01, JC-ALG-01 fehlen im Korpus), T3 139 hypothetisch,
T4 105 pending, T5 correctly_empty. Sobald score.py eintrifft: hier Report nachtragen (Modul A/B/C Precision/Recall).
Runde C (2026-10-04, v3): Spitzen 15/16, Full 96/97, nur S11 ohne Deploy. Audits: 0-applies-Risiko, T1/T2 incomplete, T6 absent, SB763-Retry plus JC25-057 plus Hoboken offen. Goal v3 aktiv.
Runde D (2026-10-04): SB763-Retry 25s Timeout exit28, Datei weiter pending. Fingerprint 55cc89c7 MATCH. T1/T2 weiter incomplete, JC25-057 plus Hoboken offen (manuell, Suchlimit erreicht). Spitzen weiter 15/16.
Runde E (2026-10-04): Static-Export re-run 500/500 ok, A0001 decisions byte-identisch (82/82 MATCH). S11 weiter blocked ohne Remote (kein origin).
Runde F (2026-10-04): Demo ES/Confidence/Conflict/as-of/Disclaimer/Audit alle True. Extraktion Luecken: effective_date 72/177, sanctions 83/177, Quelle/Zitat 0. Pipeline weiter budget-blockiert.
Runde G (2026-10-04): P4-Root-Cause Quelle vs Operativ geklaert: data 367, output 348 (Gaps gestrippt per Design), Register 367/367 MATCH Quelle, Meta+Goal korrigiert.
Runde H (2026-10-04): T6-Readiness verifiziert: changes-Adapter generisch ueber change_tests (T1-T5, kein T6), Hour-16-Intake = T6-Case anhaengen plus Re-Export, S4b bleibt ehrlich absent.
Runde I (2026-10-04): Full-Suite 96/97, nur S11 ohne Deploy. P4-Meta nach Runde G stabil, kein Testbruch.
Runde J (2026-10-04): Video-Drehbuecher fertig (3x <=3Min, je mit Score-Schluss), Aufnahme blocked bis Deploy plus score.py.
Runde K (2026-10-04, v4): Spitzen 15/16, Full 96/97, nur S11 ohne Deploy. Parallel-Diff verifiziert: data/output je 177 (367 stale korrigiert), Exemptions begruendet gefuellt, Manifest 5b75466e, S5b Fingerprint PASS. v4 aktiv.
