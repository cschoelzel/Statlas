# Umsetzungsauftrag: Rental Housing Law Navigator

Stand: 3. Oktober 2026. Standard-Abfragedatum der Challenge: 1. Oktober 2026.

## 1. Ziel und ehrliche Fertigstellungsdefinition

Baue eine vollständige Engine für das vorhandene Challenge-Paket. Sie extrahiert Rechtswirkungen automatisiert, bestimmt rechtliche Zuständigkeiten, wendet strukturierte Regeln deterministisch an und erklärt jede Entscheidung anhand des Originalgesetzes. Bei entscheidenden Datenlücken stellt sie gezielte Fragen. Änderungen werden mit derselben Engine ausgewertet.

Ziel ist die stärkste nachweisbare Lösung innerhalb des definierten Bereichs. „Beste Engine überhaupt“ ist kein überprüfbares Abnahmekriterium. Eine Überlegenheitsbehauptung ist nur für einen dokumentierten Vergleich auf unabhängigen Fällen zulässig. Keine pauschale 99-%-Garantie für unbekannte Rechtsgebiete oder beliebig viele neue Regeln.

Das Implementierungsteam arbeitet selbstständig bis zur Erfüllung der Gates. Es darf fehlende Referenzprüfungen, Quellen oder Tests niemals durch erfundene Ergebnisse ersetzen. Bestehende Projekt-, Kosten- und Serverregeln gelten.

Projekt: `/Users/constantinscholzel/Documents/Projekte/Aktiv/hacknation26`

Challenge-Paket: `/Users/constantinscholzel/Documents/Projekte/Aktiv/hacknation26/participant-final-no-hour16 3`

Diese Datei ist ein Umsetzungsauftrag, kein Nachweis einer bereits implementierten oder validierten Engine.

## 2. Pflichtumfang und Priorisierung

- Module A, B und C; alle sechs Kategorien; drei Bundesstaaten und zehn Städte im Quellenbestand.
- Alle 500 Sample-Adressen; Santa Ana ist für Extraktion relevant, hat aber keine Sample-Adressen.
- Automatische Regelgewinnung aus Quellen, keine handcodierten Antworten auf Challenge-Tests.
- Geltendes Recht, zukünftige Wirksamkeit, pending und failed unterscheiden.
- Alle fünf Änderungstests T1–T5 erfüllen.
- Gültige `rules.json`, `lookups.json`, `changes.json`, Live-Demo und einseitige Methodennotiz.
- Originalbeleg, Abrufdatum, Abfragedatum, Konflikte und reproduzierbares Prüfprotokoll.
- Geforderter Hinweis zur fehlenden Rechtsberatung in allen Ergebnisansichten.

README, PDF, Schemas und Tests gemeinsam prüfen. Die README erlaubt A+B als Notfallminimum; Ziel dieses Auftrags bleibt A+B+C. Widersprüche dokumentieren, nicht stillschweigend auflösen. Die PDF nennt etwa Sanktionen; diese intern erfassen, auch wenn das Export-Schema kein Pflichtfeld dafür vorsieht.

Priorität: Pflichtumfang → korrekte Beweiskette → aktive Rückfragen → Änderungsansicht → weitere Extras. Keine USA-weite Erweiterung vor Erfüllung des Challenge-Umfangs.

## 3. Architektur

Zwei getrennte Abläufe:

**Vorbereitung:** Quelleninventar → gezielte Beschaffung → unveränderliche Dokumente → belegte Aussagen → strukturierte Regeln → automatische und fachliche Prüfung → versionierter Regelbestand.

**Anfrage:** Adresse + Abfragedatum → Zuständigkeit → räumliche Regelkandidaten → Status/Zeit/Coverage/Ausnahmen → Ergebnis oder gezielte Rückfrage → Neuberechnung → Beweiskette.

Kleinste saubere Umsetzung: vorhandenen Projektstack nutzen; sonst kleiner Backend-Prozess, SQLite beziehungsweise strukturierte Dateien und einfache Oberfläche. Keine Vektordatenbank, Microservices oder Agentenplattform ohne nachgewiesenen Bedarf. Bekannte Dokumente anhand von IDs, Abschnitten und Kategorien adressieren.

Trenne Datenmodelle für Quellen, Aussagen, Regeln, Fakten, Entscheidungen, Rückfragen und Freigaben. Ableitungen müssen bis zur Originalquelle zurückverfolgbar sein.

## 4. Quellenbeschaffung vor der Extraktion

### 4.1 Inventar und eingefrorener Rechtsstand

Erfasse alle 87 Manifest-Einträge. Aktueller lokaler Bestand: 54 Texte und 33 Quellen ohne gelieferten Text. Behandle diese Zahlen als zu prüfenden Ausgangszustand.

Pro Quelle speichern: Dokument-ID, URL, Herausgeber, Dokumenttyp, Abrufdatum, Quellengültigkeit, Rechtsstand, Originaldatei, eigenen SHA256, Textdatei und Parser-/OCR-Version. Den vorhandenen Manifest-Hash als separaten `upstream_hash` erhalten; seine Bedeutung ist nicht geklärt, daher keine ungeprüfte Integritätsbestätigung.

Beschaffungsstatus: `full_text_ready`, `landing_page_only`, `missing`, `access_restricted`. Davon getrennt Interpretationsstatus und Quellenkonflikte führen.

Eine heute abgerufene konsolidierte Fassung kann vom angefragten historischen Rechtsstand abweichen. Historische Fassung, Änderungshistorie oder belastbare zeitliche Zuordnung beschaffen. Abrufdatum niemals als Inkrafttreten verwenden.

### 4.2 Bright Data gezielt einsetzen

Die vom Nutzer angegebene Verbindung zuerst anhand der verfügbaren Werkzeuge beziehungsweise lokalen Konfiguration verifizieren. Keine Keys ausgeben, keine Verbindung behaupten, die nicht geprüft wurde. Fehlt der Zugriff, eine konkrete Zugriffslücke melden.

Mit Suche und Abruf zunächst Originaltexte und amtliche Alternativen finden. Suchtreffer und Snippets sind Suchhilfen, keine Rechtsbelege. Beschaffung erfolgt zielgerichtet, nicht als breiter Scrape.

Prioritäten:

| Priorität | Quellen |
|---|---|
| 1 | Hoboken D032–D034; Newark D070–D072 |
| 1 | CA-Kernstatuten D017–D021; NJ-Kernstatuten D061–D064 |
| 1 | Volltexte zu MA-Bills D045–D047: vorhandene Seiten enthalten überwiegend Status/History |
| 2 | MA-CORI D056; LA-Code D038; San-Diego-Codes D074–D075 |
| 2 | Amtlichen Santa-Ana-Algorithmus-Beschluss suchen, sofern für die Extraktion erforderlich |

Vor Abruf Redundanz prüfen: D069 enthält bereits amtlichen NJ-FAIR-Act-Text; nicht jede fehlende Sekundärquelle muss erneut beschafft werden.

Nutzungsbedingungen beachten. Das Paket markiert Code-Publisher zur Terms-Prüfung. Bright Data ersetzt diese Prüfung nicht. Bei eingeschränktem Zugriff amtliche alternative PDFs, Beschlussarchive oder zulässige Einzelabrufe bevorzugen.

Pro Jurisdiktion und Kategorie einen Abdeckungsbericht erstellen: geprüft, nur teilweise belegt, fehlende Texte, unklare Auslegung. „Keine Regel gefunden“ ist nicht gleich „keine Verpflichtung vorhanden“.

## 5. Anthropic-Extraktion und 25-€-Budget

### 5.1 Fähigkeiten und Modellwahl verifizieren

Vor Implementierung die aktuellen offiziellen Anthropic-Dokumentationen für Citations, Structured Outputs, PDF Support, Message Batches, Token Counting und Pricing prüfen. API-Verfügbarkeit im Nutzeraccount prüfen. Keine ungeprüften Modellnamen, Preise oder angenommenen Rabatte fest verdrahten.

Citations dienen zur Auswahl von Fundstellen; Structured Outputs zur Schemaeinhaltung. Beide sind in der bisher geprüften Dokumentation nicht gemeinsam nutzbar: zwei Aufrufe einplanen und aktuelle Kompatibilität prüfen.

PDFs zuerst mit vorhandenem Text verarbeiten; visuelle Verarbeitung für wichtige Tabellen oder Layoutfragen verwenden. Scans benötigen OCR und OCR-Qualitätsprüfung. Native Textzitate stehen bei reinen Scan-PDFs nicht automatisch zur Verfügung. Seiten-/Absatzbezug sowie Originalansicht erhalten.

### 5.2 Budgetverwaltung

25 € sind als Anthropic-Budget autorisiert; diese spezielle Erlaubnis geht einer allgemeinen Free-Credits-Regel vor. Bright-Data-Kosten sind dadurch nicht automatisch autorisiert. Vor kostenpflichtiger Beschaffung deren Kosten und vorhandene Freigabe prüfen.

Planungsobergrenzen:

| Zweck | Budget |
|---|---:|
| Schwieriger Pilot und Modellvergleich | 3 € |
| Gesamtextraktion | 8 € |
| Prüfung und gezielte Korrektur | 9 € |
| Reserve | 5 € |

Gesamtobergrenze 25 €. Phasenbudget nur innerhalb dieser Grenze umverteilen und dokumentieren. Vor jedem Batch Tokens und maximale Ausgabe schätzen. Bereits reservierte Kosten laufender Jobs mitzählen. Wechselkurs und Gebühren berücksichtigen, damit USD-Abrechnung die Euro-Grenze nicht überschreitet.

Tokens, Kosten, Dokument, Modell-ID, Prompt-Version und Ergebnisstatus protokollieren. Fehlerwiederholungen begrenzen; erfolgreiche Ergebnisse cachen. Keine Keys im Protokoll. Keine neuen Aufträge starten, wenn Restbudget einschließlich Reservierungen nicht reicht. Nach kostenrelevanten Aktionen Kosten und Input-/Output-Token berichten.

Batch-Verarbeitung nur nutzen, wenn Frist und verfügbare Funktionen passen; den dokumentierten Preisvorteil aktuell prüfen. Ein Budget ist kein Auftrag, Credits vollständig aufzubrauchen.

### 5.3 Extraktionsablauf

1. Einen Pilot mit 8–12 schwierigen Dokumenten wählen: Ausnahmen, Tabellen, Querverweise, historische Zahlen, Bill-Seiten und Motion.
2. Mindestens zwei im Account verfügbare geeignete Modellkonfigurationen auf identischen Ausschnitten vergleichen. Belegtreue und Ausnahmeerkennung vor Preis oder eloquenter Ausgabe priorisieren.
3. Originaltext in zusammenhängende Rechtsabschnitte zerlegen. Definitionen, Ausnahmen und Querverweise zusammenführen; fehlende Verweise sichtbar machen.
4. Im Citations-Schritt atomare Aussagen sammeln: Normadressat, Verpflichtung, räumlicher Bereich, Voraussetzungen, Ausnahmen, Werte, Zeitklauseln, Status und Beziehungen.
5. Im Structured-Outputs-Schritt diese belegten Aussagen in die erlaubte Regelsprache übersetzen. Originalbelege unverändert verknüpfen. Zitate nicht erneut generieren lassen.
6. Quelltext, Fundstelle, Zahlen, Einheiten, Schema und Querverweise automatisch prüfen.
7. Ein separater kritischer Prüflauf vergleicht die vorgeschlagene Regel mit dem vollständigen relevanten Text: Welche Ausnahme fehlt? Welche Verknüpfung wurde verändert? Welche Datumsannahme ist unbelegt?
8. Nur fehlerhafte oder unsichere Teile erneut bearbeiten. Allgemeine Extraktion nicht blind mehrfach wiederholen.
9. Neue oder wesentlich geänderte Rechtsinterpretationen fachlich prüfen. Ohne externe fachliche Prüfung verbleibende Freigabelücke ausdrücklich markieren.

Modell-Selbstprüfung ist kein unabhängiger Goldstandard. Typgültige Ausgabe, gültige Zitatposition und hohe Modellwahrscheinlichkeit beweisen weder Vollständigkeit noch richtige Auslegung.

## 6. Jev als begrenzte Entscheidungskomponente

Jev für atomare Klassifikationen und Kandidatenauswahl einsetzen: Dokumenttyp, Status, Aussageart, Belegspanne, Faktenfeld, Operator, Wertkandidat und logische Beziehung. Erlaubte Antworten enthalten `insufficient_evidence` und bei Bedarf `conflicting_evidence`.

Parser erzeugt Kandidaten für Daten, Zahlen und Originalspannen; Jev wählt IDs. Code übernimmt die Originalwerte. Score nicht als exakten gesetzlichen Zahlenwert behandeln. Konfidenzen auf eigenen Referenzfällen auswerten, keine pauschale Freigabeschwelle als Richtigkeitsgarantie verwenden.

Jev ist optional, falls Zugang oder Budget fehlen. Der feste Interpreter muss ohne Jev und ohne Anthropic-API auswerten können. Weder Jev-Wiederholbarkeit noch Kalibrierung ohne eigene Prüfung behaupten.

## 7. Internes Regelmodell und Interpreter

Pro Regel unter anderem speichern: ID, Version, Kategorie, Zuständigkeits-ID, Wirkung, Rechtsstatus, Verabschiedung, Inkrafttreten, operative Geltung, Ablauf, Voraussetzungen, Ausnahmen, Formeln, Belege, Konflikte und Freigabestatus.

Erlaubte Bausteine: `eq`, `in`, `lt`, `lte`, `gt`, `gte`, `all`, `any`, `not`, Datumsintervalle und ausdrücklich erlaubte arithmetische Operationen. Dezimalarithmetik für Geld/Prozent. Einheiten und Bezugsgrößen typisieren. Kein generierter ausführbarer Code.

Interne Auswertung: Zuständigkeit AND zeitliche Wirksamkeit AND Voraussetzungen AND NOT Ausnahme. Fehlende Daten erzeugen dreiwertige Logik, nicht Default-False:

- wahr AND unbekannt = unbekannt;
- falsch AND unbekannt = falsch;
- wahr OR unbekannt = wahr;
- falsch OR unbekannt = unbekannt;
- NOT unbekannt = unbekannt.

Nicht ausdrückbare Regeln erhalten einen offenen Übersetzungsstatus; sie dürfen nicht still vereinfacht werden. Unsicherheit aus einer Ausnahme nur weitertragen, wenn diese entscheidungsrelevant ist.

Interaktionen getrennt und auf konkrete Rechtswirkungen beziehen. Keine pauschale Vorrangregel „Stadt schlägt Staat“. Unklare Preemption nicht automatisch als Aufhebung ausgeben. Bei NJ FAIR Act die von T3 erwarteten möglichen Konflikte anzeigen.

Auswertungsdimensionen separat halten. Exportadapter bildet sie auf das Challenge-Schema ab. Intern `does_not_apply` dokumentieren; laut Abgabeformat nicht einschlägige Regeln aus Lookups weglassen. Failed-Vorhaben im Regelbestand erhalten, aber keine geltende Verpflichtung daraus erzeugen.

Quellen-, Regel- und Entscheidungsversionen unveränderlich erhalten. Gültigkeit im Recht von Bekanntwerden im System unterscheiden. Gleiche eingefrorene Eingaben erzeugen dasselbe kanonische Ergebnis und dieselbe Fragenauswahl.

## 8. Geografie und Objektfakten

Census oder geeignete amtliche Quellen für Adressauflösung verwenden. Tatsächliche Gemeinde, County und Bundesstaat bestimmen; Poststadt nicht als Zuständigkeit übernehmen. Koordinatenqualität beachten: interpolierte Straßenposition ist kein bestätigter Gebäudepunkt.

Bundesstaat-/Gemeindemismatch zurückweisen. Auffällige ZIPs mit dokumentiertem Versuch ohne ZIP bearbeiten. Keine Hausnummer erfinden. An Stadtgrenzen, bei Straßenzentroiden und widersprüchlichen Treffern besseren amtlichen Grundstücks-/Gebäudenachweis suchen oder Unsicherheit erhalten.

Faktenebenen: Adresse, Grundstück, Gebäude, Wohnung, Eigentümer, Mietverhältnis. Jede Angabe erhält Herkunft, Stand und Status: amtlich belegt, importiert, Nutzerangabe, abgeleitet oder widersprüchlich.

Baujahr ist kein genaues Certificate-of-Occupancy-Datum. Proxies ausdrücklich kennzeichnen; nicht aus einem Jahr den 1. Januar erzeugen. Aktive Rückfragen zu Tenant- oder Owner-Fakten nur stellen, wenn die einschlägige Regel sie benötigt.

## 9. Beweiskette, aktive Fragen und Oberfläche

Jede Ausgabe zeigt: Originalzitat und Fundstelle → normalisierte Bedingung → Fakt mit Herkunft → Teilergebnis → Gesamtentscheidung. Quelle, Quellenversion, Abrufdatum und Abfragedatum sind zugänglich. Modellgenerierte Erklärungen dürfen keine zusätzlichen Rechtsbehauptungen einführen.

Der Motor findet offene Fakten, deren mögliche Antworten das Ergebnis verändern können. Frage nicht nach irrelevanten Daten. Bei mehreren offenen Bedingungen berücksichtigen, dass erst eine Kombination zusätzlicher Antworten entscheiden kann; nicht jede Frage einzeln auf unmittelbaren Statuswechsel beschränken.

Wähle kleine, hilfreiche Fragefolgen; bündle Fakten, die mehrere Regeln klären. Rangfolge zunächst mit festen Kriterien: Entscheidungsrelevanz, Anzahl geklärter Regeln, Beschaffungsaufwand und deterministischer Tie-Breaker.

Jede Frage erklärt: fehlender Fakt, betroffene Regel/Ausnahme, Fundstelle und benötigte Belegqualität. Nutzerangaben nicht zu amtlichen Nachweisen aufwerten. Bei Ablehnung, Nichtwissen oder Widerspruch Unsicherheit erhalten. Keine Rechtsauslegung durch eine Gebäudefrage scheinbar auflösen.

Drei Ansichten: Objektprüfung, Portfolio-Prüfliste, Vorher/Nachher-Änderungsansicht. Zusätzlich Quellenabdeckung und offene fachliche Prüfungen sichtbar machen.

## 10. Unabhängiger Referenzbestand

`gold_rules`: unabhängig geprüfte Rechtswirkungen mit allen entscheidenden Bedingungen, Ausnahmen, Zeitständen und Quellen. `gold_cases`: echte verifizierte Objektfakten und erwartete Ergebnisse. Entwicklungsfälle, eingefrorene Testfälle und synthetische Fälle getrennt halten.

Referenzen ohne Kenntnis der Engine-Ausgabe erstellen. Zwei unabhängige Bewertungen und fachliche Klärung von Uneinigkeit anstreben. Bei fehlenden Personen oder Nachweisen ist diese Abnahme offen, nicht bestanden. Für den Hackathon einen kleineren ehrlich ausgewiesenen Referenzbestand liefern; das volle Qualitätsziel bleibt separat bestehen.

Testtrennung nach Dokument/Regelfamilie organisieren; dieselbe Norm nicht durch leicht veränderte Ausschnitte in Entwicklung und Test verteilen. Zusätzliche Objektfälle derselben Regel prüfen Anwendung, sind aber keine unabhängigen Extraktionsnachweise.

Goldlabels nicht aus T1–T5, Modellantworten oder der eigenen Engine ableiten. Diese fünf Tests sind Challenge-Regressionen. Neue Fehler zunächst auf dem Entwicklungssatz beheben, danach einen neuen unabhängigen abschließenden Testsatz nutzen; wiederholtes Optimieren auf dem Holdout entwertet ihn.

## 11. Quantitative Abnahme

| Gate | Anforderung |
|---|---|
| Quellen | 87/87 inventarisiert; alle verfügbaren Volltexte verarbeitet; jede Lücke und reine Landingpage sichtbar |
| Regelfundstellen | Jede veröffentlichte Bedingung, Ausnahme und Formel belegt; 100 % der Textzitate technisch geprüft |
| Referenzregeln | Mindestens 60 fachlich geprüfte eigenständige Rechtswirkungen, sofern vorhanden; andernfalls alle vorhandenen. Alle Kategorien/Städte im Abdeckungsbericht |
| Adressen/Export | 500/500 eindeutige IDs; Schema-/Referenzprüfung ohne Fehler |
| Änderungen | T1–T5 vollständig bestanden, einschließlich Konflikt- und Negativfällen |
| Goldfälle | Mindestens 1.000 unabhängig annotierte Objekt-Regel-Datum-Fälle aus mindestens 100 echten Objekten; alle neun Sample-Städte vertreten |
| Entscheidungsqualität | Mindestens 99 % exakte Ergebnisse auf eingefrorenem Gold-Testset; Zahl, Nenner und Fehlerarten berichten |
| Regelvollständigkeit | Mindestens 99 % Recall der relevanten Rechtswirkungen im Referenzbereich; übersehene Regeln zählen als Fehler |
| Kritische Fehler | Kein bekannter ungelöster kritischer Fehler im freigegebenen Umfang: erfundene Pflicht, falscher Rechtsstatus, verlorene entscheidende Ausnahme oder unbegründete Sicherheit |
| Logik/Edge-Cases | Mindestens 20.000 sinnvoll unterschiedliche synthetische und eigenschaftsbasierte Fälle; alle bestanden |
| Rückfragen | Mindestens 100 Referenzszenarien inklusive Mehrfachbedingungen, Ablehnung und Nachweisbedarf; relevante Fragen und richtige Neuberechnung |
| Reproduzierbarkeit | 100 vollständige Läufe mit eingefrorenen Eingaben ohne Abweichung der kanonischen Ergebnisse |
| Leistung | Auswertung aller 500 Objekte in unter fünf Sekunden auf dokumentierter Zielhardware; ohne Netz/Modell, mit vorbereitetem Regelbestand |
| Budget | Anthropic-Abrechnung plus reservierte Aufträge innerhalb 25 €; Bright Data separat ausgewiesen |

Anwendung, Extraktion, Geografie und Ende-zu-Ende getrennt messen. Reporte Kategorie-/Stadt-Ergebnisse, False Positives, False Negatives, korrekte Unknowns, unnötige Unknowns und definitive Entscheidungsquote. „Alles unbekannt“ kann die Abnahme nicht bestehen. Entscheidungsquote nicht künstlich erhöhen, wenn Referenzfakten fehlen.

Zusätzlich Formeln, Zeitstände und Konfliktflags prüfen; richtige Statuslabels allein genügen nicht. Gesamtdurchschnitt darf Fehler in schwach geprüften Kategorien nicht verdecken.

99 % sind ein Ziel im Referenzbereich, keine globale Garantie. Konfidenzintervalle mit begründeter Stichproben-/Cluster-Methode ausweisen. 299 unabhängige fehlerfreie Bernoulli-Fälle ergeben ungefähr eine einseitige exakte 95-%-Untergrenze von 99 %; diese Aussage gilt nur, wenn Unabhängigkeit und Repräsentativität tatsächlich vorliegen. Tausende Varianten derselben Norm rechtfertigen sie nicht.

## 12. Systematische Edge-Case- und Fehlersuche

Mindestens folgende Familien abdecken; deterministische Seeds und Fehlerminimierung verwenden:

1. Zeit: Tag vor/am/nach Beginn und Ende, Schaltjahr, Monatswechsel, relative Monatsklauseln, abweichende operative Geltung, zukünftige und historische Abfragen.
2. Grenzen: Zahl unmittelbar unter/auf/über Schwelle, Dezimalpräzision, min/max-Formeln, falsche Einheiten, fehlender CPI, abgelaufene Jahreswerte.
3. Ausnahmen: jede einzeln, Kombinationen, verschachtelte UND/ODER, doppelte Negation, fehlender relevanter beziehungsweise irrelevanter Fakt, mehrere gleichzeitig offene Fakten.
4. Quellen: Motion, Bill, verabschiedetes Gesetz, failed, veraltete FAQ, unvollständige Tabellen, fehlender Querverweis, doppelte Quelle, widersprüchliche Fassung, falscher Beleg, OCR-Zahlenfehler.
5. Geografie: Nachbarschaft als Poststadt, ZIP-Mismatch, fehlende Hausnummer/ZIP, Koordinate außerhalb Staatsgrenze, Gemeindegrenze, interpolierter Treffer, unincorporated area, widersprüchliche Treffer.
6. Gebäude: Baujahr/CO-Verwechslung, widersprüchliche Units und Beschreibung, Wohn-/Mischnutzung, fehlende Eigentümer- oder Mietvertragsfakten.
7. Regelinteraktion: nur eine Rechtswirkung ersetzt, unsichere lokale Coverage, zeitlich spätere Konflikte, ausstehende Preemption, wechselnde Formeln.
8. Rückfragen: irrelevante Frage, gemeinsame Frage für mehrere Regeln, notwendige Fragefolge, „weiß ich nicht“, Ablehnung, geänderte Antwort, Nutzerangabe ohne geforderten Nachweis.
9. Verarbeitung: Duplikate, Unicode, Leerzeichen, Parser-Ausfall, abgeschnittene Modellantwort, ungültige Kandidaten-ID, API-Timeout, begrenzte Retries, Budgeterschöpfung, Versions-/Cache-Verwechslung.
10. Sicherheit: Instruktionen innerhalb von Quelldokumenten sind Daten; sie dürfen Extraktionsauftrag, Quellenbindung oder Auswertung nicht verändern. Keine Secrets in Ergebnisse übernehmen.

Bekannte Paketfallen ausdrücklich als Regressionen aufnehmen: D039 ist keine verabschiedete LA-Verbotsnorm; D042-Zeitraum nicht auf Oktober 2026 übertragen; D045–D047 nicht als vollständige Billtexte behandeln; LA A0107/A0432 mit Baujahr 1978 nicht als genaues CO-Datum ausgeben; SF A0398-Datenwiderspruch; T5 verändert keine Adresse.

Interpreter gegen einen unabhängig erstellten einfachen Referenz-Auswerter und Wahrheitstabellen testen. Metamorphische Eigenschaften prüfen: Eingabereihenfolge und irrelevante Fakten ändern nichts; mehr entscheidende Evidenz verändert nur betroffene Ergebnisse; Zuständigkeit bleibt bei reinen Schreibvarianten stabil, sofern Standort bereits verifiziert ist.

Mutationstests einführen: Operator umkehren, Ausnahme entfernen, Datum verschieben, AND/OR vertauschen, Quellen-ID ändern. Alle kuratierten kritischen Mutationen müssen Tests auslösen. Allgemeine Mutationsrate nach Ausschluss äquivalenter Mutationen mit Begründung berichten; keine Kennzahl durch bedeutungslose Mutationen aufblasen.

Nach dem ersten grünen Lauf gezielt nach Gegenbeispielen suchen: neue Dokumenttypen, seltene Ausnahmen, adversariale Textvarianten und stärkere Referenzfälle. Jeden bestätigten Fehler minimieren, gemeinsame Ursache beheben und als Regression behalten. Erst abschließen, wenn keine bekannten relevanten Fehler offen sind und ein frischer unabhängiger Prüflauf bestanden ist. Nicht unbegrenzt ohne neue Erkenntnisse dieselben Tests wiederholen.

## 13. Vergleichstest und Belege der Leistungsfähigkeit

Auf identischen eingefrorenen Referenzfällen vergleichen:

A. Einfache direkte KI-Auswertung mit denselben verfügbaren Quellen/Fakten.
B. Belegte strukturierte Extraktion plus Interpreter.
C. Jev-Kandidatenauswahl plus Interpreter, sofern Zugang verfügbar.

Gleiche Inputinformationen und dokumentierte Budgets verwenden. Qualität, Belegtreue, Vollständigkeit, Unsicherheit, Kosten und Laufzeit getrennt berichten. Keine unterschiedliche Quellenversorgung als Modellvorteil verkaufen. Ein externer Anbieter ist nur bei tatsächlich vergleichbarer Ausgabe ein sinnvoller zusätzlicher Benchmark.

Keinen universellen Sieger behaupten. Formuliere nach dem Vergleich exakt, in welchem Testbereich die Engine welche Verbesserung erreicht.

## 14. Vorgehen, Ausführung und finale Lieferung

1. Anforderungen/Quellen inventarisieren; Zugänge und Preise prüfen; Kostenplan erstellen.
2. Unabhängige kleine Referenzfälle auswählen, schwierigen Pilot durchführen, Extraktionskonfiguration entscheiden.
3. Quellenlücken gezielt schließen; zeitlich passende Fassungen einfrieren.
4. Belegte Aussagen und Regeln extrahieren; parallel Interpreter, Exportadapter und Faktenmodell bauen.
5. 500 Adressen prüfen; T1–T5; Quellen- und Datenlücken korrigieren.
6. Beweiskette, aktive Fragen und Änderungsansicht fertigstellen.
7. Breite synthetische Tests, Mutationen, unabhängige Goldprüfung und Gegenbeispielsuche ausführen.
8. Nach Korrekturen gezielt regressieren; frischen Abschlusslauf, Vergleich und Bericht erstellen.

Für 24 Stunden den Pilot und Kern früh abschließen; mindestens die letzten fünf Stunden für Validierung und Demo reservieren. Große Referenzannotation und volle Qualitätsabnahme können über den Hackathon hinausgehen. Kleine ehrlich belegte Ergebnisse sind besser als erfundene Großtests; offene Gates bleiben offen.

Mac für Entwicklung und kurze Checks. Umfangreiche Tests, Scraping und lange Jobs gemäß Projektregeln auf `gymscraper-act`. Lange SSH-Jobs in benannten Fenstern der Session `codex`; Anschlussbefehl ausgeben. Budget-/Kostenaufträge protokollieren. Parallelisierung nur für unabhängige Arbeitspakete.

Finale Lieferung: ausführbare Engine und UI, Exportdateien, eingefrorener Quellen-/Regelstand, Beweisketten, Quellenabdeckung, Referenzbestände, Testberichte mit Seeds, Benchmark, Kostenbericht, Methodennotiz und kurze Demo.

Fertigstellungsbericht trennt implementiert, getestet, fachlich verifiziert und offen. Kein Gate aufgrund eines fehlenden Budgets, einer fehlenden Annotation oder einer herannahenden Deadline als bestanden markieren.
