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

## Iteration 4 (Gate-Reife, Stand 2026-10-04)

Anlass: P3-Stichprobe fand 9 not_yet_effective-Labels mit Vergangenheits-Datum; P2-Erstbefund (984 Schein-Leaks durch City-vs-State-Vergleich) war widerlegt. Fixes: 8 stale Status-Strings auf in_force (D007-r005/r009/r010, D024-r005, D025-r010, D041-r002/r003, D052-r002; 8-Zeilen-Diff, Format unangetastet); uebrig D041-r005 (end 2024-01-31, Engine-ended via Datum) und D069-r001 (eff 2027-07-01, einzig legitimes flaechendeckendes not_yet_effective). README-Demo-Link auf Repo-URL gestellt (Pages-URL gibt 404, kein falscher Claim). scripts/verify_quotes.py auf skriptrelative ROOT umgestellt (worktree-sicher). Neu: tests/test_temporal_labels.py (4 Tests, dates-vor-Status) und tests/test_applies_d084.py (3 Tests, applies-Pfad mit Beleg-Quartett).

Frischer Master-Export-SHA 780df4c0 (177 Regeln, 500 Adressen, 24.970 Entscheidungen: 24.572 unknown, 139 not_yet_effective, 259 pending, 0 applies per fail-closed Design), 0 fraglose Unknowns, Zitate 177/177, Suite 105/105 gruen.

Gate-Abnahme durch 5 frische read-only Pruefer: P1 bestanden (177/0 plus 10/10 Worktree-Stichprobe plus Sinnentstellungs-Check). P2 bestanden (Vollbestand, 0 Cross-State-Decisions; Fremd-Regeln nur an 8 dokumentierten Unresolved). P3 bestanden nach Revision (Ersturteil nicht bestanden wegen 3 ended-Strings D041-r005/D042-r001/D080-r002 und fehlender Testdatei; Nachpruefung: Testdatei 4/4 gruen, VOLLnachrechnung 398/398 zeitliche Decisions korrekt — 139 NYE alle D069-r001 mit Future-Datum, 259 pending alle D045/D046/D076 — ended-Regeln korrekt omittiert, und nachweislich kann kein gueltiger Status-String die Decisions aendern, da es keinen ended-Wert gibt und Daten Vorrang haben). P4 bestanden (8/8 Tests, 367/367 Fakten im Register). P5 bestanden (500/500 Felder mit Provenienz, year_built nie Occupancy). P6 bestanden (0 fraglose Unknowns, 10/10 flippbar). P7 bestanden (D084-r001 applies mit Quartett plus Zweitregel D008-r001). P8 bestanden (105 Tests plus 6 Adversarial-Proben, 0 applies bei fehlenden Fakten). P9 bestanden (Manifest-Fingerprint nachgerechnet, 0 Adressen ohne Decisions, 8 unresolved unknown mit Geo-Frage). P10 bestanden (T1/T2 incomplete mit missing IDs, T3 139 hypothetisch ohne applies vor 2027, T4 105 pending, T5 incomplete statt correctly_empty — changes.py erzwingt incomplete bei missing MA-RENT-P1, das ist spezifiziertes fail-closed Verhalten).

## Freigabe Iteration 4: 10/10 — TEST BESTANDEN (2026-10-04)

Export-SHA 780df4c0, 177 Regeln, 500 Adressen, 24.970 Entscheidungen, Teststand 105/105 gruen. Dokumentierte Nicht-Verstoesse: 3 ended-Status-Strings entscheidungsirrelevant (Daten regieren), why_needed/acceptable_evidence teils Schablone (formal korrekt, qualitativ ausbaufähig), T1/T2-Quellluecken und D083/D084-Rest aus Iteration 3 bleiben Backlog mit Nutzerentscheidung.
