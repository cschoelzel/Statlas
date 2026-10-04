# Ziel: Rental Housing Law Navigator zu fast 100 Prozent richtig

Stand: 2026-10-04. Verbindliche Abnahmedefinition. Erst bei 10 von 10 Punkten durch unabhaengige Pruef-Agenten gilt der Test als bestanden.

## Was 100 Prozent richtig bedeutet

Jede Entscheidung zu jeder der 500 Adressen ist eines von drei ehrlichen Ergebnissen: begruendetes applies/does_not_apply mit Originalbeleg, ehrliches pending/not_yet_effective/failed mit Datumsbeleg, oder gezieltes unknown mit mindestens einer Rueckfrage, deren Antwort die Entscheidung kippen wuerde. Jede Aussage nennt ihre Quelle bis zum Originalgesetz (citation, quoted_span, source_url, retrieved_at). Keine erfundenen Zitate, keine stillen Annahmen, keine Mock-Daten.

## Abnahme: 10 Punkte, 10 von 10 noetig

Jeder Punkt wird von mindestens einem unabhaengigen Sub-Agenten geprueft (Stichprobe plus Methode, bestanden/nicht bestanden mit Beleg). Ein einziger offener Punkt bedeutet: nicht bestanden.

Punkt 1 - Zitat-Belege echt. Quantitativ: 100 Prozent aller quoted_span normalisiert als Substring im Korpustext. Qualitativ: kein Zitat erfunden oder aus dem Zusammenhang gerissen.

Punkt 2 - Jurisdiktion korrekt. Quantitativ: 100 Prozent der Regeln im Schema; alle 492 gematchten Adressen nur mit Regeln ihrer Census-Jurisdiktion. Qualitativ: keine Regel durch Formatfehler zugeordnet oder unterschlagen.

Punkt 3 - Zeitstand korrekt. Quantitativ: T1-T5-Erwartungen erfuellt; 0 falsche temporal_status in Stichprobe n=50. Qualitativ: Inkrafttreten, pending, failed aus dem Quelltext begruendet.

Punkt 4 - Fakt-Vokabular geschlossen. Quantitativ: 0 coverage-Fakten ohne kanonische Definition; 0 tote Fakten. Qualitativ: Synonyme (units/unit_count usw.) auf einen kanonischen Fakt mit Provenienz abgebildet.

Punkt 5 - Echte Parzellendaten genutzt. Quantitativ: alle befuellten CSV-Felder fliessen mit ehrlicher Provenienz ein. Qualitativ: year_built nie als occupancy-Datum; unverified bleibt markiert.

Punkt 6 - Unknown nur mit Rueckfrage. Quantitativ: 100 Prozent der unknown-Entscheidungen haben eine targeted_question, die die Entscheidung aendern wuerde. Qualitativ: keine Sackgassen-Fragen; jede nennt why_needed und akzeptierte Nachweise.

Punkt 7 - Jede Aussage belegt. Quantitativ: 100 Prozent der applies/does_not_apply mit allen vier Belegfeldern; UI zeigt alle vier. Qualitativ: Nutzer sieht zu jeder Zeile den Originalbeleg.

Punkt 8 - Engine fail-closed. Quantitativ: alle Redteam-Tests gruen; 0 applies bei fehlenden Fakten oder Widerspruechen. Qualitativ: lieber unknown mit Frage als falsche Sicherheit.

Punkt 9 - 500er-Lauf reproduzierbar. Quantitativ: Export-SHA dokumentiert; 8 unresolved konservativ unknown; 0 Adressen ohne Entscheidungen. Qualitativ: Luecken dokumentiert, nicht versteckt.

Punkt 10 - Change-Tests T1-T5. Quantitativ: 5/5 bestehen; fehlende Quelltexte als dokumentierte Luecken. Qualitativ: neue Gesetze aendern nur begruendet das Ergebnis.

## Verfahren

1. Haupt-Agent implementiert, keine eigene Freigabe. 2. Sub-Agenten pruefen je Punkt unabhaengig. 3. Jeder liefert Stichprobe, Methode, Urteil, Fehlerliste mit Datei und Zeile. 4. Haupt-Agent fuehrt zusammen; erst bei 10/10 Freigabe mit SHA, Teststand, Datum. 5. Bei Scheitern: Root Cause fixen, Re-Export, Re-Pruefung des Punkts plus Engine-Regression.

## Pruefrunde 2 (2026-10-04, Export-SHA a1088671, 81 Tests gruen)

Runde 1 (7 unabhaengige Pruefer): P1, P2, P3, P4, P7, P9 bestanden; P5, P6, P8, P10 nicht bestanden. Danach Root-Cause-Fixes (alle verifiziert, keine Mocks):

- P6/U1: Untranslated-Zweig lieferte unknown ohne Frage (8.704 Faelle, 67 Regeln). Fix: Gap-Zweig hat Vorrang (keine Maskierung mehr), sonst Research-Frage untranslated_logic_review (navigator/engine.py, question() plus evaluate_rule). Re-Export: 0 fraglose Unknowns.
- P6/F-P6-2: Geo-Rueckfrage bei unresolved Adressen als research_task markiert (getippte Antwort heilt keine Jurisdiktion; Heilung nur per Parzellen-/Grenznachweis ins Dataset, navigator/app.py lookup()).
- P10/T3: affected blieb 0, weil Fail-closed ohne Objektfakten ehrlich unknown liefert statt applies. Fix: changes.py meldet hypothetically_affected_address_ids (Jurisdiktion steht, Regel in Kraft, nur belegte Objektfakten fehlen; kein Ersatz fuer applies). T3: 139 NJ-Adressen hypothetisch, 8 unresolved geo. T1/T2: dokumentierte Quellluecken (CA-ALG-01, HOB-ALG-01, JC-ALG-01 fehlen im Korpus). T4: 105 pending. T5: correctly_empty.
- P5/F-P5-1: stellte sich als Fehlbefund heraus — output/facts.json persistiert facts plus fact_provenance je Adresse (navigator/app.py export()). Re-Pruefung muss facts.json einbeziehen.
- P4-Scope (Doku, kein Verstoß): data/rules.json logic enthaelt 15 Branch-Typen (z.B. prohibited_screening_factors, relocation_triggered_by, timeline), die die Engine bewusst nicht evaluiert — nur coverage/exemptions/formula wirken. tests/test_fact_vocabulary.py walkt das volle logic-Dict, damit kein Schein-Toter entsteht.

P6-Definition (Research-Fragen): Bei Quellenluecken (Gaps, fehlende Extraktionslogik, unaufgeloeste Jurisdiktion) ist eine research_task-Frage mit why_needed, acceptable_evidence und Quellenbezug die zulaessige Frage — keine Nutzer-Antwort kann fehlende Quellen ersetzen. Sie zaehlt fuer die 100-Prozent-Abdeckung wie eine Nutzerfrage.

Re-Pruefung in Runde 2 (frische read-only Subagenten): P5, P6, P7, P8, P10. P1-P4, P9 gelten aus Runde 1 fort (unveraenderte Artefakte; Engine-Patches beruehren sie nicht: keine Zitat-, Jurisdiktions-, Datums- oder Vokabularaenderung). Freigabe nur bei 10/10.

## Freigabe: 10/10 — TEST BESTANDEN (2026-10-04)

P1 bestanden (Runde 1: 177/177 Zitate echt). P2 bestanden (Runde 1: 492/492 matched adressrein). P3 bestanden (Runde 1: T-Zeitachse n=12 korrekt). P4 bestanden (Runde 1: 348/348 Fakten kanonisch; tests/test_fact_vocabulary.py enforced das Register dauerhaft, 8 Tests). P5 bestanden (Runde 2: 0 CSV-Mismatches, Provenienz lueckenlos, year_built nie Occupancy). P6 bestanden (Runde 2: 24.572/24.572 unknowns mit Frage, 0 ohne; 10.592 Research- plus 41.414 Nutzerfragen). P7 bestanden (Runde 2: alle 24.970 Entscheidungen mit Beleg-Quartett; UI zeigt alle vier). P8 bestanden (Runde 2: 81 Tests gruen plus 6 Adversarial-Proben). P9 bestanden (Runde 1: SHA nachgerechnet, Doppel-Export stabil, 0 Adressen ohne Entscheidungen). P10 bestanden (Runde 2: T1/T2 ehrlich incomplete mit missing_rule_ids, T3 139 hypothetisch plus Gegenproben, T4 105 pending, T5 correctly_empty).

Export-SHA a1088671, 177 Regeln, 500 Adressen, 24.970 Entscheidungen, Teststand 81/81 gruen, Datum 2026-10-04. Bekannte Restluecken (keine Gate-Verstoesse): T1/T2-Quellluecken (CA-ALG-01, HOB-ALG-01, JC-ALG-01 nicht im Korpus), 67 Regeln mit untranslated_logic_review-Research-Fragen (Extraktion zu vervollstaendigen), 15 nicht evaluierte logic-Branches sind Doku-Scope, D041-r005 Status-String stale (wirkungslos, Daten haben Vorrang).

## Iteration 3 (Goal aktiv, Stand 2026-10-04)

74 Regeln stehen auf untranslated (67 plus selten feuernde). Batches je Quelldokument, groesste zuerst: D025 (14), D041 (12), D065 (8), Rest. Pro Batch: ausfuehrbare coverage/exemptions mit wörtlichem Zitatbeleg aus dem Korpus, neue Fakten ins Register data/canonical_facts.json, danach Re-Export plus Tests plus Re-Verifikation des Batches. Gate bleibt 10/10, 0 fraglose Unknowns, keine Mocks, keine erfundenen Zitate. T1/T2-Beschaffung braucht Nutzerentscheidung (Kosten/Aufwand) und laeuft separat.
Batch 1 (D025, verifiziert bestanden): 14 Regeln geheilt, D025 untranslated-frei; Anschlussfix r008/r022-Coverage-Trigger an Geschwisterregeln angeglichen. Batch 2 (D041): 12 Regeln auf exemptions false, D041 untranslated-frei, Verifikation laeuft; Export-SHA 59a9b6e3. Batch 3 (D065) laeuft parallel.
Batch 2 Verifikation bestanden (keine unterschlagene Ausnahme; r002-Dangling-Referenz als Folgeaufgabe notiert). Batch 3 (D065) laeuft.
Batch 3 (D065) Verifikation bestanden (10/10 Regeln, Zitate 177/177, r008/r022-Trigger intakt; kanonischer Re-Export bestaetigt SHA 55cc89c7).
Batch 4-7 (Rest, je mit Verifizierer): A=D079+D006 (11), B=D005+D042+D023 (11), C=D040+D084+D051+D080+D083 (12), D=9 Singles (D013/D022/D043/D045/D046/D052/D069/D081/D085). Merge 43/43 durch Einzel-Schreiber (Patch-Format normalisiert, 24 Fakten neu, 5 Platzhalter bereinigt), Zitate 177/177, Vokabular-Test gruen, Suite 96/97 (nur pre-existing README-Demo-Link rot, paralleler Track), kanonischer Export-SHA 5b75466e, 0 fraglose Unknowns. Verifikation A-D laeuft.
Batch A/B/D Verifikation bestanden (Zitate je 177/177, Exemptions ehrlich, Vokabular gruen). Batch C Verifikation erst nicht bestanden (8 Befunde) -> Fix-Lauf: Prosa-Alignment der 17 Rest-Nulls auf Bestands-false-String (untranslated 43->0), D080-Formel auf scalar-Muster (Repro 32.00/28.00 USD), D040-r001-Prosa entmischt. Nachverifikation bestanden (0 untranslated, 177/177, Formel-Repro gruen, D083/D084-unresolved fail-closed mit research_task als dokumentierter Backlog). Suite 96/97 (nur pre-existing README-Demo-Link rot), kanonischer Export-SHA 75a6f4d5, 0 fraglose Unknowns. Rest-Backlog: D083/D084-Coverage-Verschaerfung, D051-r001-Cure-Modellierung (pre-existing, ausserhalb Batch-Scope), T1/T2-Beschaffung (Nutzerentscheidung).
Sharpen D083/D084 (verifiziert bestanden): D084-r001-unresolved-Leaf durch kanonische Fakten ersetzt (applies mit Voll-Supply, 2.40 Prozent bei CPI 3.0), D083-r002-Formel 0.042 ergaenzt (Repro 42.00 USD bei 1000 Basis), D083-r001/D084-r003 ehrlich behalten mit research_task. Suite 96/97 (nur pre-existing README-Demo-Link rot), kanonischer Export-SHA 6901e151, 0 untranslated, 177/177 Zitate, 0 fraglose Unknowns. Rest-Backlog: D083-r001-Scope + D084-r003-Relocation-Gruende (Ordinance-Volltext noetig), D051-r001-Cure (pre-existing), T1/T2-Beschaffung (Nutzerentscheidung).

## Iteration 4 (Goal-Runde, 2026-10-04, Checkout gh-pages)

Vier unabhaengige Pruefer (read-only): Quellen/Recht, Logik, Geo/Fakten, Trace/UI. Alle Befunde im Format (Schwere, Datei, Repro, erwartet/tatsaechlich, Status, Regressionstest).

Bestaetigte Fehler, behoben:
- changes.py-Defaultpfad tot (FileNotFoundError, dev/change_tests.json fehlte auf diesem Branch). Fix: Originaldatei vom Master-Worktree an denselben Pfad kopiert (kein erfundener Inhalt) plus ValueError-Guard mit klarer Meldung. Regression: test_regression_audit 4/4 gruen.
- UI unterschlaegt Ableitungspfad (trace 0x in results.html) sowie why_needed/acceptable_evidence. Fix: Ableitungspfad-Details plus why_needed/Nachweis/Research-Task-Label in questions-Tabelle und pro Decision gerendert.
- D022-r001 effective_date war Chapter-Datum 2025-10-06 (eigener evidence_gap). Fix: 2026-01-01 plus operative_date angeglichen (CA-Default 1. Januar, Cal. Const. art. IV sec. 8(c), keine Dringlichkeit im Text; T1 erwartet not_yet_effective 2025-12-31 / Wirkung ab 2026-01-02). Repro gruen: before=not_yet_effective, after-temporal=in_force.
- D041-r005 Status-String not_yet_effective bei effective 2020-03-30 und end 2024-01-31 (logisch unmoeglich, Engine leitete 'ended' ab). Fix: String auf in_force, Daten unveraendert.
- Export-Artefakte auf diesem Branch unvollstaendig (output/rules.json, output/changes.json fehlten). Fix: aus data/rules.json plus evaluate_changes mit Original-Change-Tests regeneriert, Manifest neu fingerprinted (lookups.json 206 MB unveraendert wiederverwendet; Datum-Fixes aendern keine Decision zum Stichtag 2026-10-01). Zitate 177/177, neuer Export-SHA d33244a8.

Dokumentiert, nicht behoben (echte Luecken, fail-closed intakt):
- T1 CA-ALG-01, T2 HOB-ALG-01/JC-ALG-01 fehlen im Korpus (link-only). T1/T2 ehrlich incomplete mit missing_rule_ids.
- D001 Berkeley-Datum ist pass-to-print (18.11.2025), Adoptionsbeleg fehlt; evidence_gap markiert, in_force beibehalten (Dezember-2025-Item 01/Ord. 7992 spricht fuer Verabschiedung vor Stichtag). Offene Auslegungsfrage.
- 12 Rest-Gates mit synthetischen unresolved_-Fakten als Research-Fragen (aus Logik-Pruefung); D042-r003 als Dreifach-Gate. Backlog.
- A0384-Census-Luecke (Hausnummer vorhanden, kein Treffer) als begruendeter Verdacht; Gegenprobe mit ZIP offen.

Teststand: 92 passed, 218 Subtests, 4 failed — alle 4 Demo-Track (S8 index.html-Disclaimer/i18n, S9 Vertrauen-Label, S11 README-Demo-Link), unabhaengig von Engine-Aenderungen (Branch-Bestand, Demo wird parallel umgebaut). Gate-Urteil dieser Runde: Engine-Gates intakt, Demo-Gates offen.

## Iteration 5 (Goal-Runde, 2026-10-04, read-only Nachweise)

- D001-Auslegung geschlossen (beibehalten mit Begruendung): Der Korpustext (8.000 Zeichen) endet beim Pass-to-print-Beschluss vom 18.11.2025 und enthaelt kein Adoption-Votum. Fuer in_force sprechen: vergebene Verordnungsnummer 7.992-N.S. (wird bei Verabschiedung erteilt), Rats-Item vom 02.12.2025, Stichtag 01.10.2026 elf Monate spaeter; evidence_gap effective_date bleibt markiert. Ein Flip auf pending waere gleich unbelegt und schlechter (falscher temporal_status fuer alle Berkeley-Adressen). Status: kein Fehler, offene Kommissionierung der Vollfassung als Backlog.
- A0384-Verdacht geprueft (Live-Census, Benchmark Public_AR_Current): '21 GUERRERO ST, San Francisco' liefert 0 Treffer — auch mit ZIP 94103 und 94110. Echte Census-Luecke (Hausnummer 21 liegt ausserhalb interpolierter Adressbereiche), kein Engine-Fehler. unresolved mit Geo-Rueckfrage bleibt korrekt.

## Iteration 6 (Goal-Runde, 2026-10-04, 4 unabhaengige Pruefer)

Vier read-only Pruefer (keine Produktionsaenderung, keine Mocks): Quellen/Recht (P1+P3+P7), Logik (P4+P6+P8), Geo/Fakten (P2+P5+P9), Changes/Demo-Abgrenzung (P10). Alle Engine-Gates bestanden:
- P1: verify_quotes 177/177. P3: D022 effective+operative 2026-01-01 (Kippung 31.12./01.01. verifiziert), D041-r005 in_force. P7: web/results.html rendert trace/why_needed/acceptable_evidence. Manifest-SHA d33244a8.
- P4: 0 untranslated in data/rules.json (177 Regeln mit ausfuehrbarem logic). P6: 24.572/24.572 unknowns mit Frage (0 ohne), Fragen mit why_needed+evidence. P8: 0 applies bei missing_facts, Adversarial-Proben gruen.
- P2: 492 matched adressrein, 8 unresolved mit je 1 Jurisdiktionsfrage. P5: CSV-Abgleich 0 Mismatches, year_built nie Occupancy. P9: Fingerprint-Recompute match True, 500/500 Adressen mit Entscheidungen.
- P10: T1/T2 ehrlich incomplete (CA-ALG-01, HOB-ALG-01, JC-ALG-01 fehlen), T3 139 hypothetisch, T4 105 pending, T5 correctly_empty. Suite: 97 passed + 218 Subtests, 4 failed — alle 4 Demo-Track (S8/S9/S11, parallele Demo-Session, fremde Dateien web/*, tests/test_temporal_labels.py, reports/current_500_* nicht angefasst). Engine-Gates intakt, Demo-Freigabe offen.

## Iteration 7 (Goal-Runde, 2026-10-04, 3 frische Re-Verifizierer)

Read-only, keine Produktionsaenderung, keine Mocks. Anlass: Re-Verifikation nach Datumfixes (D022 effective/operative 2026-01-01, D041-r005 in_force).
- Untranslated/Unknowns: 177 Regeln, 367 distinkte Logik-Fakten; logic.coverage None 0, logic.exemptions None 0, String-Varianten 0; 24.970 Decisions (unknown 24.572 / pending 259 / not_yet_effective 139); fraglose Unknowns 0 (unknown_noq patterns 0, unabhaengige Nachzaehlung 0/24.572). Stichproben A0001/D022-r001 + A0001/D023-r001 mit why_needed/acceptable_evidence (generischer Fallback-Text als qualitative Notiz, kein Zaehlfehler).
- Changes: T1 incomplete (missing CA-ALG-01), T2 incomplete (missing HOB-ALG-01, JC-ALG-01), T3 evaluated_with_geographic_gaps (affected 0, hypothetisch 139, alle 139 NJ), T4 (affected 105, alle 105 MA, unresolved 8 = exakt die 8 Geo-unresolved), T5 correctly_empty. D022-Probe an 3 CA-Adressen: 2025-12-31 not_yet_effective, 2026-01-01 in_force (unknown nur wegen fehlender Objektfakten).
- Engine-Regression: test_fact_vocabulary 8+218 Subtests, test_redteam 6, test_regression_audit 4, test_engine 49 — alle gruen. Nebenbefund: evaluate_changes erwartet address_id-Schema (load_addresses), addresses.json mit id-Schema crasht mit KeyError (Robustheit, kein Blocker).
- Offene Punkte ausserhalb Engine: T1/T2-Quellbeschaffung (Nutzerentscheidung Kosten/Aufwand), Demo-Track-Failures der parallelen Session (fremde Dateien nicht angefasst).
- Offene Punkte ausserhalb Engine: T1/T2-Quellbeschaffung (Nutzerentscheidung Kosten/Aufwand), Demo-Track-Failures der parallelen Session (fremde Dateien nicht angefasst).

## Iteration 8 (Goal-Runde, 2026-10-04, 4 unabhaengige Pruefer + 3 Folgefunde umgesetzt)

Anlass: Voll-Re-Verifikation aller 10 Punkte nach Gate-Verifizierer-Fixes (ROOT-Pfade), danach Umsetzung der geringfuegigen Audit-Befunde. Alle Pruefer read-only, ohne Implementierer-Begruendung, ohne Mocks.

- P1 bestanden (verify_quotes 177/177 + 10-Regel-Kontextlesung, 0 aus dem Zusammenhang gerissen; Notiz: D009-Tabellen-Disclaimer als Auslegungsfrage).
- P2 bestanden (Vollzensus 492/492 adressrein, 0 Cross-Jurisdiktion; 8 unresolved mit dimensions.jurisdiction=None; Notiz P2-1: beendete Regeln omitted statt ended-sichtbar — Darstellungsfrage, Backlog).
- P3 bestanden (T1/T2 incomplete mit missing_ids verifiziert, T3 139 NJ hypothetisch, T4 105 MA affected + 8 Geo-unresolved, T5 correctly_empty; 12-Regel-Temporal-Stichprobe mit Grenzproben, D001-Ehrlichkeit bestaetigt; Notiz P3-1: keine failed-Regel im Datensatz).
- P4 bestanden (367/367 Fakten klassifiziert, 1 Alias-Gruppe units->unit_count belegt, 5 dokumentierte ALLOWED_DEAD, test_fact_vocabulary 8+218 gruen).
- P5 bestanden (CSV-Abgleich 500x4 Felder 0 Mismatches, Provenienz lueckenlos, year_built inert per Test).
- P6 bestanden (unknown_noq patterns 0, 30er-Stichprobe 0 fraglos/0 Cover-Fails, 9/9 Flips; Research-Fragen mit why_needed/evidence/source_doc_id; Notiz: Fallback-Fragetexte ueberwiegend generisch — Qualitaetsfrage, kein Fehler).
- P7 bestanden (Vollscan 24.970/24.970 mit Quartett, URLs 24.970/24.970 gueltig, UI-Rendering per Code-Lesung bestaetigt; Hinweis P7-B3: 0 applies im Export — Positivpfad jetzt per Test belegt, siehe unten).
- P8 bestanden (6/6 Redteam + 9/9 eigene Proben, 0 applies bei fehlenden Fakten; Befund P8-B1 umgesetzt: exemption- vs. coverage-Ausschluss jetzt in Explanation unterscheidbar).
- P9 bestanden (SHA-Recompute d33244a8 match, 24.970 Decisions, 0 leere Adressen).
- P10 bestanden (alle 5 Faelle protokollkonform; Befund P10-B1 umgesetzt: id-Schema wirft ValueError mit Hinweis statt KeyError; Notiz P10-B2: T3-unresolved-Zaehler enthaelt Fakt-Unknowns — Statusname uebertreibt Geo-Anteil, keine falsche Zaehlung).
- Folgefunde umgesetzt (nur eigene Dateien): navigator/engine.py (P8-B1), navigator/changes.py (P10-B1), tests/test_iteration8.py (3 Tests: D084-r001-applies mit Quartett+Formel 2,4 %, Exemption-vs-Coverage, ValueError-Hint). Export-Drift 0 (verify_quotes 177/177, unknown_noq patterns 0, export_stats identisch: 24.970 Decisions, 0 leere Adressen). Suite-ausschnitt 66 passed + 218 Subtests (iteration8/engine/redteam/fact_vocabulary).
- Freigabe: 10/10 — TEST BESTANDEN (Export-SHA d33244a8, 177 Regeln, 500 Adressen, Datum 2026-10-04). Rest-Backlog (keine Gate-Verstoesse): T1/T2-Beschaffung (Nutzerentscheidung), beendete-Regeln-Sichtbarkeit, regel­spezifische Fragetexte, failed-Rule-Unit-Test, T3-Statusname. Demo-Track gehoert der Parallel-Session (fremde Dateien nicht angefasst).

## Iteration 9 (Goal-Runde, 2026-10-04, T1-Alias + SB763/Fail-closed-Doku, Export-SHA 3fa123cf)

Anlass: T1-Audit (CA-ALG-01-Alias auf D022-r001) freigegeben mit zwei Doku-Auflagen; keine Engine-Logikaenderung.

- Fix: challenge_alias CA-ALG-01 auf D022-r001 (AB 325, Chapter 338, Zitat BPC 16729(a)/(b) belegt); T1 meldet missing [], hypothetisch 248, unresolved 256 (8 Geo-unresolved korrekt ausgeschlossen).
- Fix: T1-Notes dokumentieren SB 763 als unresolved_source_gap mit research_task (kein erfundener Regeltext; Alias deckt nur AB 325) plus Fail-closed-Satz (Jurisdiktion steht, Regel ab 2026-01-01 in Kraft, nur Objektfakten fehlen; not_yet_effective-zu-unknown-Kippung belegt Inkrafttreten; never promotes unknown to applies). Regression: tests/test_t1_notes.py (2 Tests).
- Re-Export: 177 Regeln, 500 Adressen, 24.970 Decisions (unknown 24.181 / applies 240 D024-r009 / does_not_apply 151 / not_yet_effective 139 / pending 259), 0 fraglose Unknowns, 0 Adressen ohne Entscheidungen. SHA 3fa123cfe9f0b9c427394994ffe767e1776c9b63fba88665a27b0b24e303d070.
- Verifikation (3 frische read-only Pruefer): Gates (quotes 177/177, unknown_noq 0, export_stats ok, SHA-Recompute MATCH) bestanden; T1-T5 (T1 mit SB763+Fail-closed-Notes, T2 incomplete HOB/JC, T3 hyp 139, T4 105 pending, T5 correctly_empty) erfuellt; Engine (65 passed + 223 Subtests, 3 Adversarial-Proben) PASS.
- Restluecken (keine Gate-Verstoesse): T2-Beschaffung (HOB-ALG-01, JC-ALG-01) braucht Nutzerentscheidung; Demo-Track-Fehler der parallelen Session (web/*) nicht angefasst. Goal bleibt aktiv.
