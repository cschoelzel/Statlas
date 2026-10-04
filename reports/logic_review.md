# Unabhängiger synthetischer Logik-Redteam

Stand: 2026-10-03. Prüfer hat nur Ziel §§7–12, Engine und öffentliche Tests gelesen; keine Implementierungsbegründung und keine anderen Reviewberichte. Keine Produktionsdatei geändert. Synthetische Fälle, kein Rechts-Goldbestand.

Ausgeführt: `python3 -m unittest discover -s tests -p test_redteam.py` (0,001 s): 6 Testmethoden, 1 bestanden, 5 fehlgeschlagen. Bestehende Methode prüft 18 unabhängige AND/OR-Wahrheitstabelle-Belegungen (je Ergebnis und relevante Missing-Menge). Vorher 5 minimale Regelprobes und 2 Regelreihenfolge-Probes ausgeführt.

| ID / Severity | Requirement | Minimaler Input / Expected / Actual | Status / Regression |
|---|---|---|---|
| R1 kritisch | §7 nicht ausdrückbare Regeln offen; keine unbegründete Sicherheit | CA-Regel `status=in_force` ohne `logic` oder `coverage_conditions`, Fakt `state=CA`; erwartet unknown, tatsächlich applies | confirmed; `test_missing_translation_is_unknown` |
| R2 kritisch | §7 Rechtsstatus getrennt, keine erfundene operative Pflicht | CA-Regel `status=withdrawn`, explizit coverage=True, exemptions=False; erwartet keinesfalls applies, tatsächlich applies | confirmed; `test_unrecognized_status_is_not_operative` |
| R3 kritisch | §7 operative Geltung separat, §12 Zeitstände | CA-Regel `effective_date=2025-01-01`, `operative_date=2027-01-01`, Abfrage 2026-10-01; erwartet not_yet_effective, tatsächlich applies | confirmed für fehlende operative-date-Unterstützung; `test_operative_date` |
| R4 hoch | §§7,12 widersprüchliche Fassungen/Datumswerte erhalten | effective_date=2027-01-01, candidates=[2025-01-01,2027-01-01], Abfrage 2026-10-01; erwartet unknown, tatsächlich not_yet_effective | confirmed; `test_conflicting_effective_date` |
| R5 hoch | §§7,12 gleiche Eingaben/irrelevante Reihenfolge deterministisch | Drei gültige CA-Regeln a→b→c, beide supersedes-Kanten mit evidence; [a,b,c] => c applies, [b,a,c] => c superseded. Erwartet gleiche IDs/Resultate unabhängig von Reihenfolge | confirmed; `test_interaction_order_invariance` |

Beweis: Die mitgelieferten Regressionen führen alle minimalen Eingaben aus und erzeugten die fünf angegebenen AssertionErrors. R3 verwendet eine plausible kanonische Feldbezeichnung; wenn der freigegebene Vertrag eine andere operative Feldbezeichnung festlegt, muss der Test daran angepasst werden. Das beobachtete Problem ist trotzdem fehlende operative Geltung in der Engine.

Nicht abgenommen: 20.000-Fälle-Gate, 1.000 unabhängige Rechts-/Objekt-Goldfälle, 100 Referenz-Frageszenarien und 100 vollständige Wiederholungsläufe. Die 18 Wahrheitstabellenbelegungen belegen nur den engen geprüften AND/OR-Bereich. Kuratierte Mutationsabnahme wurde nicht ausgeführt. Dieser Report bewertet keine Rechtsrichtigkeit extrahierter Normen.

Zusätzliche Robustheitsprobes (2 ausgeführt): `evaluate_formula({'op':'mul','args':[{'value':'1e999999'},{'value':'1e999999'}]}, {})` wirft unbehandelten `decimal.Overflow`; `evaluate_condition({'all':None},{})` wirft unbehandelten `TypeError`. Beide confirmed, severity mittel, Requirement §12 Verarbeitung/Parser-Ausfall. Erwartet kontrollierte Review-/Unknown-Diagnostik, tatsächlich kompletter Funktionsabbruch. Regressionen zunächst offen; gemeinsame Ursache Eingabevalidierung/Exception-Grenze. Summe ausgeführter separater Minimalprobes damit 9 (5 Regel-, 2 Reihenfolge-, 2 Robustheitsprobes).
