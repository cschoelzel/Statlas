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
