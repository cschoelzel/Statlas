# Engine-Live-Lookups pro Referenzfall-Gruppe, Runde 4 (2026-10-04)

Stichtag 2026-10-01, Befehl je Adresse: lookup mit address und as-of.

1. MOTION (D039, REF-MOTION): 0 Regeln extrahiert, Lookup A0001 (Los Angeles)
   liefert keinen D039-Treffer. Korrekt: Motion zur Pruefung, kein Verbot
   aus dieser Quelle. Erwartung ban_from_this_source=false erfuellt.

2. LA-RATE und UTILITY (D042, 7 Faelle): Lookup A0001 liefert D042-r002/r003/r004
   je unknown (fehlende Fakten bzw. offene Beweislage). Ehrlich statt geraten;
   D042-r001 braucht Parzellenfakt rso_covered_unit, nicht im Sample.

3. MA pending (D045/D046/D047, 3 Faelle): Lookup A0006 (Boston) liefert
   D045-r001 pending und D046-r001 pending. T4-Hypothese live belegt.
   D047 ohne eigene Regel per D047-Entscheidungsnotiz (Duplikat von D046).

4. FAIR (D069, 6 Faelle): Lookups A0002 (Hoboken), A0008 (Jersey City) und
   A0003 (Newark) liefern D069-r001 je not_yet_effective. T3-Zeitschiene
   live belegt; Conflict-Flags entfallen, solange T2-Regeln fehlen.

5. DEPOSIT (D007, 6 Faelle): D007 sind Berkeley-Stadtregeln, daher korrekterweise
   nicht in LA-Lookups. Lookup A0005 (Berkeley) liefert 14 D007-Regeln je
   unknown (fehlende Mietverhaeltnis-Fakten). Ehrlich statt geraten.

6. T5 negativ: changes.json T5 correctly_empty, kein Rent Cap in Boston/Cambridge.
   Negativbefund, kein Lookup noetig.
