# Gap-Resolution Batch B (D040-D043, Los Angeles RSO/JCO)

Ergebnis: 15 resolved, 5 offen (von 20 Gap-Leaves). DB nicht geschrieben; Fundstellen nur vorgeschlagen.

Hinweis: resolved + replacement=null heisst redundanter Platzhalter -> Leaf ersatzlos streichen und all-Kette kollabieren. Zitate <=300 Zeichen,Whitespace normalisiert.

## D040-r001 / unresolved_legal_evidence_D040_1

Pfad: logic.coverage.all[1] | Status: resolved

Entscheidung: Text nennt Kuendigung ohne just cause als operative Bedingung; kanonischer Fakt landlord_terminating_tenancy existiert bereits.

Ersatz: {"fact": "landlord_terminating_tenancy", "op": "eq", "value": true}

Beleg: > It prohibits terminations of tenancies without just cause and requires relocation assistance for no-fault evictions.

## D040-r006 / unresolved_legal_evidence_D040_6

Pfad: logic.coverage.all[1] | Status: resolved

Entscheidung: Redundant: LA + residential_building decken die Textbedingung ab; Pflichtdetails (Tenancy-Beginn, Eviction-Notice) sind Requirement, kein Coverage-Gate. Leaf ersatzlos streichen.

Ersatz: null (streichen bzw. offen)

Beleg: > Beginning August 20, 2025, landlords must post a Notice of Right to Counsel in a conspicuous common area of the residential building where the tenant resides.

## D041-r002 / unresolved_legal_evidence_D041_2

Pfad: logic.coverage.all[1] | Status: resolved

Entscheidung: Stichtag 2026-02-02 fehlt in Coverage; Muster wie D041-r005 mit kanonischem Fakt rent_increase_notice_date.

Ersatz: {"fact": "rent_increase_notice_date", "op": "gte", "value": "2026-02-02"}

Beleg: > Effective February 2, 2026, the landlord can no longer include an additional percentage increase for utilities.

## D041-r003 / unresolved_legal_evidence_D041_3

Pfad: logic.coverage.all[1] | Status: resolved

Entscheidung: Gleicher Stichtag wie D041-r002 (Typo additonal steht so im Korpus); kanonischer Datumsfakt.

Ersatz: {"fact": "rent_increase_notice_date", "op": "gte", "value": "2026-02-02"}

Beleg: > Effective February 2, 2026, an additonal 10% increase for an additional dependent added to the tenancy is no longer permitted.

## D041-r004 / unresolved_legal_evidence_D041_4

Pfad: logic.coverage.all[1] | Status: open

Entscheidung: Offen: 60-Tage-Fenster ab Kenntnis braucht Referenzdatum; kein kanonischer Fakt dafuer. Zusaetzlicher Mieter + Nicht-Dependent sind bereits abgedeckt, Leaf nicht er silent streichen (wuerde ueber-generalisieren).

Ersatz: null (streichen bzw. offen)

Beleg: > However, a 10% for an additional tenant is allowed (not a dependent) if moves into a rental unit: Landlords can increase the rent within 60 days of learning about the additional tenant.

## D041-r005 / unresolved_legal_evidence_D041_5

Pfad: logic.coverage.all[1] | Status: resolved

Entscheidung: Redundant: Zeitraum 2020-03-30 bis 2024-01-31 steht bereits als gte/lte-Leaves in Coverage. Leaf ersatzlos streichen.

Ersatz: null (streichen bzw. offen)

Beleg: > Effective March 30, 2020, through January 31, 2024, rent increases are prohibited for rental units subject to the Rent Stabilization Ordinance (RSO).

## D041-r007 / unresolved_legal_evidence_D041_7

Pfad: logic.coverage.all[1] | Status: open

Entscheidung: Offen: Erlaubnis zur monatlichen Umlage + 30-Tage-Notice lassen sich mit keinem kanonischen Fakt ausdruecken. Streichen wuerde die Regel auf alle RSO-Units verallgemeinern.

Ersatz: null (streichen bzw. offen)

Beleg: > The landlord may pass through 50% of the fee to the tenant every month rather than once a year. A 30-day notice must be given to the tenant to collect a rental surcharge of $1.61.

## D041-r008 / unresolved_legal_evidence_D041_8

Pfad: logic.coverage.all[1] | Status: open

Entscheidung: Offen: SCEP-Umlagehandlung hat keinen kanonischen Fakt. Nichts erfunden.

Ersatz: null (streichen bzw. offen)

Beleg: > Effective January 1, 2022, a landlord may collect 1/12 of 50% of the annual Systematic Code Enforcement Fee from the tenant of the rental unit per month.

## D041-r009 / unresolved_legal_evidence_D041_9

Pfad: logic.coverage.all[1] | Status: resolved

Entscheidung: Redundant: smoke_detector_installed steht bereits in Coverage und traegt die Textbedingung (Umbruch smoke/carbon im Korpus normalisiert). Leaf streichen.

Ersatz: null (streichen bzw. offen)

Beleg: > A $3.00 surcharge may be added to the rent for the installation and cost of a hard-wired smoke detector or a combination smoke/carbon monoxide detector.

## D041-r010 / unresolved_legal_evidence_D041_10

Pfad: logic.coverage.all[1] | Status: resolved

Entscheidung: Coverage hatte nur RSO-Status; at-fault-Grund fehlt. Kanonischer Fakt at_fault_just_cause_ground_exists existiert.

Ersatz: {"fact": "at_fault_just_cause_ground_exists", "op": "eq", "value": true}

Beleg: > Tenant is at-fault. Failure to pay rent. Failure to fix or address a violation of the rental agreement. Creating a nuisance or causing damage to the rental unit.

## D041-r011 / unresolved_legal_evidence_D041_11

Pfad: logic.coverage.all[1] | Status: resolved

Entscheidung: No-fault-Charakter fehlt in Coverage; kanonischer Fakt eviction_is_no_fault existiert (vgl. D041-r013/r014). Auf 300 Zeichen gekuerzt.

Ersatz: {"fact": "eviction_is_no_fault", "op": "eq", "value": true}

Beleg: > Tenant is not at-fault. The owner or immediate family member will move into the rental unit. Demolition and permanent removal from the rental market. Government order. Conversion to affordable housing.

## D041-r013 / unresolved_legal_evidence_D041_13

Pfad: logic.coverage.all[1] | Status: resolved

Entscheidung: Redundant: LA + RSO + eviction_is_no_fault decken die Bedingung voll ab. Leaf streichen.

Ersatz: null (streichen bzw. offen)

Beleg: > No-fault evictions require the payment of relocation assistance.

## D041-r014 / unresolved_legal_evidence_D041_14

Pfad: logic.coverage.all[1] | Status: resolved

Entscheidung: Fristen sind Requirement, kein Coverage-Gate; Coverage-Tripel ist vollstaendig. Leaf streichen.

Ersatz: null (streichen bzw. offen)

Beleg: > Give the tenant a 30-day and 60-day written notice (some evictions require 120-day notice or up to a 1-year extension).

## D041-r015 / unresolved_legal_evidence_D041_15

Pfad: logic.coverage.all[1] | Status: resolved

Entscheidung: Duennes, aber wortwoertliches Heading-Zitat; Coverage (LA + RSO + security_deposit_collected) traegt die Regel. Leaf streichen.

Ersatz: null (streichen bzw. offen)

Beleg: > Interest Payments on Security Deposits.

## D041-r016 / unresolved_legal_evidence_D041_16

Pfad: logic.coverage.all[1] | Status: resolved

Entscheidung: Coverage (LA + unit_subject_to_rso=false) spiegelt den Text exakt. Leaf streichen.

Ersatz: null (streichen bzw. offen)

Beleg: > Even if your property is not covered under the Rent Stabilization Ordinance, you and your tenants have rights and responsibilities under the Just Cause Ordinance.

## D042-r002 / unresolved_legal_evidence_D042_2

Pfad: logic.coverage.all[1] | Status: resolved

Entscheidung: Wie D041-r002, belegt aus D042-Text; kanonischer Datumsfakt.

Ersatz: {"fact": "rent_increase_notice_date", "op": "gte", "value": "2026-02-02"}

Beleg: > Beginning February 2, 2026, a landlord can no longer include any additional percentage increase for utilities.

## D042-r003 / unresolved_legal_evidence_D042_3

Pfad: logic.coverage.all[1] | Status: open

Entscheidung: Offen: kleiner-als-10-Prozent-Schwelle hat keinen kanonischen Fakt (rent_increase_planned allein waere Unter-Spezifikation). Nichts erfunden.

Ersatz: null (streichen bzw. offen)

Beleg: > State law requires landlords to provide 30 days written advance notice of rent increases of less than 10%.

## D042-r003 / unresolved_legal_condition_state_notice_exemption

Pfad: logic.exemptions | Status: open

Entscheidung: Offen: D042-Text enthaelt keine Ausnahme zur 30-Tage-Notice; Exemption-Leaf unbelegt, kein Ersatz.

Ersatz: null (streichen bzw. offen)

Beleg: > (kein Beleg im Korpus)

## D043-r006 / unresolved_legal_evidence_D043_6

Pfad: logic.coverage.all[1] | Status: resolved

Entscheidung: Coverage (LA + relocation_assistance_required) plus Exemptions (beide agency/order-Fakten) decken Text voll ab. Leaf streichen.

Ersatz: null (streichen bzw. offen)

Beleg: > A landlord may offset the accumulated rent against any relocation assistance, unless the relocation assistance is owed because a termination of tenancy is required by a governmental agency order to vacate or comply with an issued order for an unpermitted dwelling.

## D043-r014 / unresolved_legal_evidence_D043_14

Pfad: logic.coverage.all[1] | Status: resolved

Entscheidung: Coverage-Fakt tentative_parcel_map_approved_for_condo_conversion spiegelt den Text exakt. Leaf streichen.

Ersatz: null (streichen bzw. offen)

Beleg: > If the City of Los Angeles Planning Department has approved a tentative parcel or tract map for a condominium conversion, the tenant may elect to relocate without receiving a Notice to Terminate Tenancy from the landlord.
