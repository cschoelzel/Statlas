# Gap-Resolution Batch REST (alle Docs ausserhalb A/B/C)

Ergebnis: 25 resolved, 10 offen (von 35 Gap-Leaves). DB nicht geschrieben; Fundstellen nur vorgeschlagen.

resolved + replacement=null heisst redundanter Platzhalter -> Leaf ersatzlos streichen und all-Kette kollabieren. Alle Zitate als normalisierter Substring im Doc verifiziert, <=300 Zeichen.

## D001-r001 / unresolved_legal_evidence_D001_1

Pfad: logic/coverage/all[1] | Status: resolved

Redundant: coverage nennt bereits Berkeley, residential dwelling, Competitor-Daten und Setzen/Empfehlen von Mieten; Exemptions decken aggregierte/anonyme Reports, Affordable-Housing und Marktforschung ab. Kein operativer Rest.strue

Ersatz: null (streichen bzw. offen)

Beleg: > It shall be unlawful for a landlord to use a coordinated pricing algorithm described in subsection A when setting rents or occupancy levels for residential dwelling units in the City of Berkeley.

## D003-r001 / unresolved_legal_evidence_D003_1

Pfad: logic/coverage/all[1] | Status: open

Offen: operativer Kern (Auskunft ueber/Verwendung von criminal history, inkl. Anzeigen, Bewerbung, Auswahl, Kuendigung, Miet-/Kautionshoehe) hat keinen kanonischen Fakt in rules.json. Exemptions sind modelliert. Benoetigt neuen Fakt, z.B. criminal_history_inquiry_or_adverse_use.

Ersatz: null (streichen bzw. offen)

Beleg: > The Fair Chance Access to Housing Ordinance prohibits rental housing providers in Berkeley from asking about and using criminal history and/or criminal background checks in their rental housing advertising, applications, tenant selection process, or decision-making.

## D022-r001 / unresolved_legal_evidence_D022_1

Pfad: logic/coverage/all[1] | Status: open

Offen: das verbotene Verhalten (use/distribute common pricing algorithm) hat keinen kanonischen Fakt; coverage enthaelt nur die abstrakten Begehungsformen (contract/combination/conspiracy, coercion). Benoetigt neuen Fakt, z.B. uses_or_distributes_common_pricing_algorithm.

Ersatz: null (streichen bzw. offen)

Beleg: > This bill would also make it unlawful for a person to use or distribute a common pricing algorithm as part of a contract, combination in the form of a trust, or conspiracy to restrain trade or commerce.

## D023-r001 / unresolved_legal_evidence_D023_1

Pfad: logic/coverage/all[1] | Status: resolved

Ersatz durch kanonischen Fakt landlord_terminating_tenancy: 12-Monats-Besatz und residential real property stehen bereits in coverage; der Gap war der Kuendigungs-Trigger.

Ersatz: {"fact": "landlord_terminating_tenancy", "op": "eq", "value": true}

Beleg: > after a tenant has continuously and lawfully occupied a residential real property for 12 months, the owner of the residential real property shall not terminate a tenancy without just cause, which shall be stated in the written notice to terminate tenancy.

## D023-r004 / unresolved_legal_evidence_D023_4

Pfad: logic/coverage/all[1] | Status: resolved

Ersatz durch landlord_terminating_tenancy: withdrawal und 12-Monats-Besatz stehen in coverage; der Gap war der Kuendigungs-Trigger (withdrawal ist no-fault just cause).

Ersatz: {"fact": "landlord_terminating_tenancy", "op": "eq", "value": true}

Beleg: > the owner of the residential real property shall not terminate a tenancy without just cause, which shall be stated in the written notice to terminate tenancy.

## D023-r008 / unresolved_legal_evidence_D023_8

Pfad: logic/coverage/all[1] | Status: resolved

Redundant: curable lease violation steht in coverage, notice/cure/cure-period-expiry stehen in procedure. Kein operativer Rest.

Ersatz: null (streichen bzw. offen)

Beleg: > Before an owner of residential real property issues a notice to terminate a tenancy for just cause that is a curable lease violation, the owner shall first give notice of the violation to the tenant with an opportunity to cure the violation

## D023-r012 / unresolved_legal_evidence_D023_12

Pfad: logic/coverage/all[1] | Status: open

Offen: waiver_of_section_1946_2_rights steht in coverage, aber die Rechtsfolge (Verzicht ist nichtig) hat keinen kanonischen Fakt und keine procedure. Benoetigt neuen Fakt, z.B. waiver_void_as_against_public_policy. Nicht streichen, sonst wuerde Verzicht als wirksam gelten.

Ersatz: null (streichen bzw. offen)

Beleg: > Any waiver of the rights under this section shall be void as contrary to public policy.

## D036-r002 / unresolved_legal_evidence_D036_2

Pfad: logic/coverage/all[1] | Status: resolved

Redundant: coverage (Jersey City + unit_count>=5) plus exemption (unit_count<=4) decken den Text voll ab (5+ Einheiten = rent-control-pflichtig).

Ersatz: null (streichen bzw. offen)

Beleg: > Please Note: All 1-4 Unit Properties are exempt from rent control

## D045-r001 / unresolved_legal_evidence_D045_r001

Pfad: logic/coverage/all[1] | Status: open

Offen: D045 ist reine Bill-Statusseite (H5222, an House Ways and Means verwiesen), ohne operativen Gesetzestext. Nichts belegbar, nichts ergaenzen.

Ersatz: null (streichen bzw. offen)

Beleg: > Bill reported favorably by committee and referred to the committee on House Ways and Means

## D046-r001 / unresolved_legal_evidence_D046_r001

Pfad: logic/coverage/all[1] | Status: open

Offen: D046 ist reine Bill-Statusseite (S2983, an Senate Ways and Means verwiesen), ohne operativen Gesetzestext. Nichts belegbar, nichts ergaenzen.

Ersatz: null (streichen bzw. offen)

Beleg: > Bill reported favorably by committee and referred to the committee on Senate Ways and Means

## D048-r001 / unresolved_legal_evidence_D048_1

Pfad: logic/coverage/all[1] | Status: resolved

Redundant: acceptance (municipality_accepts_chapter_40p), <10-Units-/400-USD-Exemptions, 6-Monats-Freiwilligkeit, verbotene Regelungsbereiche und kommunale Kompensation sind alle modelliert.

Ersatz: null (streichen bzw. offen)

Beleg: > No city or town may enact, maintain or enforce rent control of any kind, except that any city or town that accepts this chapter may adopt rent control regulation that provides

## D067-r030 / unresolved_legal_evidence_D067_30

Pfad: logic/coverage/all[1] | Status: resolved

Redundant: security_deposit_collected steht in coverage, seasonal<=125-Tage-Exemption ist modelliert; der Gap war der Zinsertrag-Anspruch selbst.

Ersatz: null (streichen bzw. offen)

Beleg: > The interest or earnings paid on the security deposit belongs to the tenant and shall be paid to the tenant in cash or credited toward rent due and owing on the renewal or anniversary of the tenant’s lease or on January 31

## D069-r001 / unresolved_legal_evidence_D069_1

Pfad: logic/coverage/all[1] | Status: resolved

Redundant: NJ + residential + (uses_coordinator_service OR performs_coordinating_function OR parallel_pricing) decken Sec. 4(a)/(b)/(e) ab; der Gap war das Verbots-Operative selbst.

Ersatz: null (streichen bzw. offen)

Beleg: > to receive, subscribe to, contract for, or otherwise exchange any form of consideration in return for the use of, the services of a coordinator

## D073-r001 / unresolved_legal_evidence_D073_1

Pfad: logic/coverage/all[1] | Status: resolved

Redundant: die 12 Scope-Leaves plus Exemptions decken den Anwendungsbereich ab; der Gap war der just-cause-Kuendigungsschutz als solcher.

Ersatz: null (streichen bzw. offen)

Beleg: > This Division protects the rights of tenants by requiring just cause for termination of a tenancy consistent with California Civil Code section 1946.2

## D073-r002 / unresolved_legal_evidence_D073_2

Pfad: logic/coverage/all[1] | Status: resolved

Ersatz durch landlord_terminating_tenancy: at-fault ground + curable violation stehen in coverage; der Gap war der Kuendigungs-Trigger.

Ersatz: {"fact": "landlord_terminating_tenancy", "op": "eq", "value": true}

Beleg: > If a landlord issues a termination notice for at-fault just cause, the landlord shall do the following

## D073-r004 / unresolved_legal_evidence_D073_4

Pfad: logic/coverage/all[1] | Status: resolved

Ersatz durch landlord_terminating_tenancy: withdrawal + good faith stehen in coverage; der Gap war der Besitzrueckforderungs-/Kuendigungs-Trigger.

Ersatz: {"fact": "landlord_terminating_tenancy", "op": "eq", "value": true}

Beleg: > The landlord seeks to recover possession to withdraw the residential rental property from the rental market.

## D073-r011 / unresolved_legal_evidence_D073_11

Pfad: logic/coverage/all[1] | Status: resolved

Redundant: tenant_exercised_protected_right + landlord_adverse_action_taken bilden die Retaliation-Definition exakt ab.

Ersatz: null (streichen bzw. offen)

Beleg: > Retaliation means any threat or any other adverse action against a tenant for exercising or attempting to exercise any right guaranteed under this Division.

## D076-r001 / unresolved_legal_evidence_D076_1

Pfad: logic/coverage/all[1] | Status: resolved

Redundant: San Diego + residential rental stehen in coverage, aggregierte-historische-Daten- und Affordable-Guideline-Exemptions sind modelliert.

Ersatz: null (streichen bzw. offen)

Beleg: > It is unlawful for a landlord to use an algorithmic device to set rental rates or occupancy levels for residential rental property.

## D079-r001 / unresolved_legal_evidence_D079_1

Pfad: logic/coverage/all[1] | Status: resolved

Ersatz durch landlord_terminating_tenancy: covered unit steht in coverage; der Gap war der Eviction-Trigger mit dominant-motive-Qualifier.

Ersatz: {"fact": "landlord_terminating_tenancy", "op": "eq", "value": true}

Beleg: > In order to evict a tenant from a rental unit covered by the Rent Ordinance, a landlord must have a just cause reason that is the dominant motive for pursuing the eviction.

## D079-r002 / unresolved_legal_evidence_D079_2

Pfad: logic/coverage/all[1] | Status: resolved

Ersatz durch landlord_terminating_tenancy: der konkrete Grund (non-payment/late/bounced/cure) steht in coverage; der Gap war der Eviction-Trigger.

Ersatz: {"fact": "landlord_terminating_tenancy", "op": "eq", "value": true}

Beleg: > In order to evict a tenant from a rental unit covered by the Rent Ordinance, a landlord must have a just cause reason that is the dominant motive for pursuing the eviction.

## D079-r004 / unresolved_legal_evidence_D079_4

Pfad: logic/coverage/all[1] | Status: resolved

Ersatz durch landlord_terminating_tenancy: renewal-refusal/access-refusal-Gruende stehen in coverage; der Gap war der Eviction-Trigger.

Ersatz: {"fact": "landlord_terminating_tenancy", "op": "eq", "value": true}

Beleg: > In order to evict a tenant from a rental unit covered by the Rent Ordinance, a landlord must have a just cause reason that is the dominant motive for pursuing the eviction.

## D079-r006 / unresolved_legal_evidence_D079_6

Pfad: logic/coverage/all[1] | Status: resolved

Ersatz durch landlord_terminating_tenancy: condo-conversion/demolition-Gruende stehen in coverage; der Gap war der Eviction-Trigger.

Ersatz: {"fact": "landlord_terminating_tenancy", "op": "eq", "value": true}

Beleg: > In order to evict a tenant from a rental unit covered by the Rent Ordinance, a landlord must have a just cause reason that is the dominant motive for pursuing the eviction.

## D079-r007 / unresolved_legal_evidence_D079_7

Pfad: logic/coverage/all[1] | Status: resolved

Ersatz durch landlord_terminating_tenancy: capital-improvement/substantial-rehab-Gruende stehen in coverage; der Gap war der Eviction-Trigger.

Ersatz: {"fact": "landlord_terminating_tenancy", "op": "eq", "value": true}

Beleg: > In order to evict a tenant from a rental unit covered by the Rent Ordinance, a landlord must have a just cause reason that is the dominant motive for pursuing the eviction.

## D079-r008 / unresolved_legal_evidence_D079_8

Pfad: logic/coverage/all[1] | Status: resolved

Ersatz durch landlord_terminating_tenancy: Ellis-Act/lead-remediation-Gruende stehen in coverage; der Gap war der Eviction-Trigger.

Ersatz: {"fact": "landlord_terminating_tenancy", "op": "eq", "value": true}

Beleg: > In order to evict a tenant from a rental unit covered by the Rent Ordinance, a landlord must have a just cause reason that is the dominant motive for pursuing the eviction.

## D080-r001 / unresolved_legal_evidence_D080_1

Pfad: logic/coverage/all[1] | Status: open

Offen: Stichtags-Fenster (2026-03-01 bis 2027-02-28) und Satz (1.6%) sind operativ, aber kein kanonischer Datumsfakt passt als Single-Leaf und die Formel traegt bereits 1.6% ohne Periode. Benoetigt Datums-Range-Fakt, z.B. increase_effective_date im Fenster.

Ersatz: null (streichen bzw. offen)

Beleg: > For rent-controlled units, the annual allowable increase amount effective March 1, 2026 through February 28, 2027 is 1.6%.

## D080-r002 / unresolved_legal_evidence_D080_2

Pfad: logic/coverage/all[1] | Status: open

Offen: wie D080-r001 fuer Vorjahresfenster (2025-03-01 bis 2026-02-28, 1.4%). Benoetigt Datums-Range-Fakt.

Ersatz: null (streichen bzw. offen)

Beleg: > The annual allowable increase amount effective March 1, 2025 through February 28, 2026 is 1.4%.

## D081-r001 / unresolved_legal_evidence_D081_1

Pfad: logic/coverage/all[1] | Status: resolved

Redundant: SF + algorithmic-rent-setter-device stehen in coverage; der Gap war das Verbots-Operative selbst.

Ersatz: null (streichen bzw. offen)

Beleg: > The law prohibits the sale or use of algorithmic devices to set rents or manage occupancy levels for residential units in San Francisco.

## D083-r001 / unresolved_legal_evidence_D083_1

Pfad: logic/coverage/all[1] | Status: open

Offen: Datumsspannen stehen in coverage, aber der operative Satz (1.6%) hat keinen Fakt und keine formula. Benoetigt Raten-Fakt/formula, z.B. allowable_increase_percent.

Ersatz: null (streichen bzw. offen)

Beleg: > Allowable Rent Increase: 1.6% for March 1, 2026 - February 28, 2027

## D083-r002 / unresolved_legal_evidence_D083_2

Pfad: logic/coverage/all[1] | Status: open

Offen: wie r001 fuer Kautionsertrag (4.2%). Benoetigt Raten-Fakt/formula, z.B. security_deposit_interest_percent.

Ersatz: null (streichen bzw. offen)

Beleg: > Security Deposit Interest: 4.2% for March 1, 2026 - February 28, 2027

## D084-r001 / unresolved_legal_evidence_D084_1

Pfad: logic/coverage/all[1] | Status: resolved

Ersatz durch property_type_is_residential_rental: Seite regelt Santa-Ana-Mietstabilisierung; formula (min 3%, 0.8xCPI) traegt den Cap.

Ersatz: {"fact": "property_type_is_residential_rental", "op": "eq", "value": true}

Beleg: > Your landlord can only raise your rent by a certain amount each year. The increase cannot be more than 3% of your current rent or 80% of the Consumer Price Index (CPI) change, whichever is less.

## D084-r002 / unresolved_legal_evidence_D084_2

Pfad: logic/coverage/all[1] | Status: resolved

Ersatz durch landlord_terminating_tenancy: just-cause-Gruende stehen in valid_just_cause_reasons; der Gap war der Eviction-Trigger.

Ersatz: {"fact": "landlord_terminating_tenancy", "op": "eq", "value": true}

Beleg: > Your landlord must have a valid reason to evict you. This could be for not paying rent, breaking the lease, or if the landlord wants to move into the property themselves.

## D084-r003 / unresolved_legal_condition_eviction_reason_trigger

Pfad: logic/relocation_triggered_by | Status: open

Offen: relocation_triggered_by braucht den ausloesenden no-fault-Grund (Owner-Einzug, Ruecknahme, Abriss/Remodel laut D085-Text), aber kein kanonischer Fakt bildet ihn ab. Benoetigt neuen Fakt, z.B. no_fault_eviction_trigger_for_relocation.

Ersatz: null (streichen bzw. offen)

Beleg: > If your landlord evicts you for certain reasons, they might have to help pay for your moving costs.

## D085-r001 / unresolved_legal_evidence_D085_1

Pfad: logic/coverage/all[1] | Status: resolved

Redundant: Santa Ana + residential rental + CO-/Mobilehome-Stichtage + formula (min 3%, 0.8xCPI-12mo) decken den Text voll ab.

Ersatz: null (streichen bzw. offen)

Beleg: > Increase in residential rents are limited to the lower of 3% per year, or 80% of the percent change in the Consumer Price Index over the most recent 12-month period.

## D085-r002 / unresolved_legal_evidence_D085_2

Pfad: logic/coverage/all[1] | Status: resolved

Redundant: coverage plus relief_process (fair-return-evidence, 60 Tage) decken den Text ab.

Ersatz: null (streichen bzw. offen)

Beleg: > Any owner of residential rental property or a mobile home park may petition for relief from the cap, but will need to provide evidence that a rate increase in excess of the annual allowance is necessary to provide a fair and reasonable return

## D085-r004 / unresolved_legal_evidence_D085_4

Pfad: logic/coverage/all[1] | Status: resolved

Ersatz durch landlord_terminating_tenancy: 30-Tage-Besatz steht in coverage, Exemptions sind modelliert; der Gap war der Kuendigungs-Trigger.

Ersatz: {"fact": "landlord_terminating_tenancy", "op": "eq", "value": true}

Beleg: > After 30 days, an owner shall not terminate a tenancy without just cause, which shall be stated in a written notice.
