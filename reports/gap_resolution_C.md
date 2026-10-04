# Gap-Resolution Batch C - Screening und Fees (D005, D006, D007, D008, D009, D052, D065)

Datenbank NICHT geschrieben (data/rules.json unveraendert). Vorschlaege nur in /tmp/gapfix_C.json.

## Methode

Alle 54 Luecken sitzen an logic/coverage/all[1] als zusaetzliche Konjunktion all([BASE, GAP]). Zwei Typen:
Typ A (53 Faelle): GAP wird durch ein Duplikat eines bereits in BASE geforderten, korpusbelegten kanonischen Leafs ersetzt. all([X, X]) ist exakt aequivalent zu X: semantikerhaltend, entfernt nur den dauerhaften unknown-Zwang. Kein neuer Faktname, keine erfundene Bedingung.
Typ B (1 Fall, D006-r011): GAP wird durch echte Bedingung shared_kitchen_or_bath ersetzt (kanonisch, bereits in Exemptions derselben Regel verwendet, korpusbelegt). Verengt ueberbreite Coverage auf den Regelgegenstand.
Offen (replacement=null) bleibt nur, was der Korpus nicht hergibt - hier: nichts.

## D005-r002 (A, resolved)
- Pfad: logic/coverage/all[1] / Gap: unresolved_legal_evidence_D005_2
- Entscheidung: Duplikat {"fact": "screening_fee_charged", "op": "eq", "value": true}
- Begruendung: Korpus regelt Rechte bei gezahlter Screening-Fee; Basis fordert screening_fee_charged bereits, Duplikat ist semantikerhaltend.
- Zitat: Prospective tenants should expect to receive a copy of their credit report within 7 days of receipt by the landlord, a receipt for the fee paid and an itemized list of any out-of-pocket expenses and time spent by the landlord on the screening, and a refund of any unused portion of the fee.

## D005-r003 (A, resolved)
- Pfad: logic/coverage/all[1] / Gap: unresolved_legal_evidence_D005_3
- Entscheidung: Duplikat {"fact": "reusable_screening_report_provided", "op": "eq", "value": true}
- Begruendung: Korpus verlangt Nutzung des Reusable-Reports; Basis fordert reusable_screening_report_provided bereits, Duplikat ist semantikerhaltend.
- Zitat: If the tenant provides a reusable screening report, the landlord must use it.

## D005-r004 (A, resolved)
- Pfad: logic/coverage/all[1] / Gap: unresolved_legal_evidence_D005_4
- Entscheidung: Duplikat {"fact": "prospective_tenant_application", "op": "eq", "value": true}
- Begruendung: Korpus belegt Fee-Verbot bei Bewerbung ohne verfuegbare Einheit; Basis fordert prospective_tenant_application bereits, Duplikat ist semantikerhaltend. Ausloeser steht zusaetzlich als Exemption rental_unit_available=false.
- Zitat: The landlord cannot charge a prospective tenant a screening fee if no rental unit is actually available.

## D005-r005 (A, resolved)
- Pfad: logic/coverage/all[1] / Gap: unresolved_legal_evidence_D005_5
- Entscheidung: Duplikat {"fact": "screening_fee_charged", "op": "eq", "value": true}
- Begruendung: Korpus belegt Rueckgabepflicht bei erhobener Fee; Basis fordert screening_fee_charged bereits, Duplikat ist semantikerhaltend.
- Zitat: The landlord must also return a screening fee to any applicant not selected, or have a policy under which they review applications in the order received and the first qualified applicant gets the unit.

## D005-r009 (A, resolved)
- Pfad: logic/coverage/all[1] / Gap: unresolved_legal_evidence_D005_9
- Entscheidung: Duplikat {"fact": "residential_rental_agreement", "op": "eq", "value": true}
- Begruendung: Korpus belegt Anwendbarkeit auf alle Wohnraummietvertraege; Basis fordert residential_rental_agreement bereits, Duplikat ist semantikerhaltend.
- Zitat: Chapter 13.78 applies to all residential rental agreements regardless of any contractual language in any rental agreement or lease to the contrary.

## D006-r001 (A, resolved)
- Pfad: logic/coverage/all[1] / Gap: unresolved_legal_evidence_D006_1
- Entscheidung: Duplikat {"fact": "unit_type_fully_covered", "op": "eq", "value": true}
- Begruendung: Korpus bindet AGA an voll abgedeckte Einheiten (5%-Cap); Basis fordert unit_type_fully_covered bereits, Duplikat ist semantikerhaltend.
- Zitat: Units that are fully covered will have a rent ceiling, meaning rent increases will be limited by the Annual General Adjustment set by the Rent Board each year.

## D006-r002 (A, resolved)
- Pfad: logic/coverage/all[1] / Gap: unresolved_legal_evidence_D006_2
- Entscheidung: Duplikat {"fact": "rent_increase_type", "op": "eq", "value": "capital_improvement_petition"}
- Begruendung: Korpus belegt Petition nur fuer abgeschlossene Improvements; Basis fordert rent_increase_type bereits, Duplikat ist semantikerhaltend.
- Zitat: Landlords can only file a petition for rent increases for completed capital improvements (they can no longer petition to have rent increases preliminarily authorized for planned capital improvements).

## D006-r004 (A, resolved)
- Pfad: logic/coverage/all[1] / Gap: unresolved_legal_evidence_D006_4
- Entscheidung: Duplikat {"fact": "eviction_ground", "op": "eq", "value": "nonpayment_of_rent"}
- Begruendung: Korpus belegt FMR-Schwelle bei Nonpayment-Eviction; Basis fordert eviction_ground bereits, Duplikat ist semantikerhaltend.
- Zitat: For a landlord to evict a tenant for nonpayment of rent, the tenant must owe an amount of rental debt equal to or greater than one month of the Fair Market Rent (FMR) value for a unit of equivalent size

## D006-r005 (A, resolved)
- Pfad: logic/coverage/all[1] / Gap: unresolved_legal_evidence_D006_5
- Entscheidung: Duplikat {"fact": "fixed_term_lease_expired", "op": "eq", "value": true}
- Begruendung: Korpus belegt Verbot der Eviction nach Fixtermin-Ablauf; Basis fordert fixed_term_lease_expired bereits, Duplikat ist semantikerhaltend.
- Zitat: A landlord cannot evict a tenant for failing to sign a substantially similar lease upon expiration of a fixed-term lease.

## D006-r009 (A, resolved)
- Pfad: logic/coverage/all[1] / Gap: unresolved_legal_evidence_D006_9
- Entscheidung: Duplikat {"fact": "tenant_organizing_activity", "op": "eq", "value": true}
- Begruendung: Korpus belegt Organizing-Recht; Basis fordert tenant_organizing_activity bereits, Duplikat ist semantikerhaltend.
- Zitat: Tenants who live on certain properties now have an enforceable right to create tenant associations, and engage in organizing activities.

## D006-r011 (B, resolved)
- Pfad: logic/coverage/all[1] / Gap: unresolved_legal_evidence_D006_11
- Entscheidung: echte Bedingung {"fact": "shared_kitchen_or_bath", "op": "eq", "value": true}
- Begruendung: Echte Bedingung: Regelgegenstand sind Shared-Facility-Einheiten; Fakt ist kanonisch (bereits in Exemptions derselben Regel verwendet) und korpusbelegt. Verengt ueberbreite Coverage auf den Regelgegenstand.
- Zitat: Where the tenant shares a kitchen or bath facilities with the landlord, the unit will be exempt from the Rent Ordinance only if the landlord lived in a unit on the same property at the start of the tenancy.

## D006-r012 (A, resolved)
- Pfad: logic/coverage/all[1] / Gap: unresolved_legal_evidence_D006_12
- Entscheidung: Duplikat {"fact": "eviction_type", "op": "eq", "value": "owner_move_in"}
- Begruendung: Korpus belegt jaehrliche Inflationsanpassung der Owner-Move-In-Hilfen; Basis fordert eviction_type bereits, Duplikat ist semantikerhaltend.
- Zitat: The Rent Board must make inflationary adjustments to owner move-in eviction relocation assistance amounts each year.

## D007-r001 (A, resolved)
- Pfad: logic/coverage/all[1] / Gap: unresolved_legal_evidence_D007_1
- Entscheidung: Duplikat {"fact": "tenancy_start_date", "op": "gte", "value": "2024-07-01"}
- Begruendung: Korpus belegt 1-Monats-Cap ab 1.7.2024; Basis fordert tenancy_start_date bereits, Duplikat ist semantikerhaltend.
- Zitat: Starting July 1, 2024, many landlords may only charge one month of rent for unfurnished and furnished units

## D007-r002 (A, resolved)
- Pfad: logic/coverage/all[1] / Gap: unresolved_legal_evidence_D007_2
- Entscheidung: Duplikat {"fact": "landlord_properties_owned", "op": "eq", "value": 2}
- Begruendung: Korpus belegt Small-Owner-Ausnahme (2 Properties, max 4 Units); Basis fordert landlord_properties_owned bereits, Duplikat ist semantikerhaltend.
- Zitat: landlords who own only two rental properties with no more than four residential units total can charge up to two months rent for furnished and unfurnished units

## D007-r005 (A, resolved)
- Pfad: logic/coverage/all[1] / Gap: unresolved_legal_evidence_D007_5
- Entscheidung: Duplikat {"fact": "tenancy_start_date", "op": "gte", "value": "2025-07-01"}
- Begruendung: Korpus belegt Fotopflicht ab 1.7.2025; Basis fordert tenancy_start_date bereits, Duplikat ist semantikerhaltend.
- Zitat: For tenancies that begin on or after July 1, 2025, a landlord must photograph the unit immediately before or at the start of a new tenancy to document the condition of the unit.

## D007-r006 (A, resolved)
- Pfad: logic/coverage/all[1] / Gap: unresolved_legal_evidence_D007_6
- Entscheidung: Duplikat {"fact": "tenancy_stage", "op": "eq", "value": "last_two_weeks"}
- Begruendung: Korpus belegt Walk-Through in den letzten zwei Wochen; Basis fordert tenancy_stage bereits, Duplikat ist semantikerhaltend.
- Zitat: landlords must offer a walk-through inspection during the last two weeks of a tenancy to identify any items that need repair/cleaning.

## D007-r007 (A, resolved)
- Pfad: logic/coverage/all[1] / Gap: unresolved_legal_evidence_D007_7
- Entscheidung: Duplikat {"fact": "unit_vacated", "op": "eq", "value": true}
- Begruendung: Korpus belegt 21-Tage-Rueckgabe nach Leerzug; Basis fordert unit_vacated bereits, Duplikat ist semantikerhaltend.
- Zitat: All or any remaining portion of a security deposit must be returned within 21 days after the tenant/s leave the unit vacant.

## D007-r008 (A, resolved)
- Pfad: logic/coverage/all[1] / Gap: unresolved_legal_evidence_D007_8
- Entscheidung: Duplikat {"fact": "deductions_made", "op": "eq", "value": true}
- Begruendung: Korpus belegt Itemized-Statement bei Abzuegen; Basis fordert deductions_made bereits, Duplikat ist semantikerhaltend.
- Zitat: If deductions were made, the landlord must give the tenant a written statement itemizing the amount of and and purpose for any security deposit deductions

## D007-r009 (A, resolved)
- Pfad: logic/coverage/all[1] / Gap: unresolved_legal_evidence_D007_9
- Entscheidung: Duplikat {"fact": "repairs_deducted", "op": "eq", "value": true}
- Begruendung: Korpus belegt Repair-Nachweis ab 1.1.2025; Basis fordert repairs_deducted bereits, Duplikat ist semantikerhaltend.
- Zitat: Starting January 1, 2025, landlords must provide proof that necessary repairs were completed.

## D007-r010 (A, resolved)
- Pfad: logic/coverage/all[1] / Gap: unresolved_legal_evidence_D007_10
- Entscheidung: Duplikat {"fact": "repairs_or_cleaning_deducted", "op": "eq", "value": true}
- Begruendung: Korpus belegt Post-Possession-Fotos ab 1.4.2025; Basis fordert repairs_or_cleaning_deducted bereits, Duplikat ist semantikerhaltend.
- Zitat: Starting April 1, 2025, landlords must take photographs of a unit after regaining possession, but before any repairs or cleaning for which the landlord intends to make a deduction from the security deposit.

## D007-r011 (A, resolved)
- Pfad: logic/coverage/all[1] / Gap: unresolved_legal_evidence_D007_11
- Entscheidung: Duplikat {"fact": "deduction_reason", "op": "eq", "value": "rent_default"}
- Begruendung: Korpus erlaubt Abzug fuer Mietrueckstand; Basis fordert deduction_reason bereits, Duplikat ist semantikerhaltend.
- Zitat: A landlord may deduct only the amount that is reasonably necessary to: Cover rent default

## D007-r012 (A, resolved)
- Pfad: logic/coverage/all[1] / Gap: unresolved_legal_evidence_D007_12
- Entscheidung: Duplikat {"fact": "deduction_reason", "op": "eq", "value": "tenant_caused_damage"}
- Begruendung: Korpus erlaubt Abzug fuer Tenant-Schaeden jenseits normaler Abnutzung; Basis fordert deduction_reason bereits, Duplikat ist semantikerhaltend.
- Zitat: Repair damages caused by a tenant or a tenant's guest other than normal wear and tear

## D007-r013 (A, resolved)
- Pfad: logic/coverage/all[1] / Gap: unresolved_legal_evidence_D007_13
- Entscheidung: Duplikat {"fact": "deduction_reason", "op": "eq", "value": "cleaning"}
- Begruendung: Korpus erlaubt Reinigungsabzug (Tenancies ab 1.1.2003); Basis fordert deduction_reason bereits, Duplikat ist semantikerhaltend.
- Zitat: Clean the unit to return it to the same level of cleanliness as at the start of the tenancy (for tenancies beginning after January 1, 2003)

## D007-r014 (A, resolved)
- Pfad: logic/coverage/all[1] / Gap: unresolved_legal_evidence_D007_14
- Entscheidung: Duplikat {"fact": "lease_allows_deduction", "op": "eq", "value": true}
- Begruendung: Korpus erlaubt Abzug bei Lease-Erlaubnis; Basis fordert lease_allows_deduction bereits, Duplikat ist semantikerhaltend.
- Zitat: If allowed by the lease, cover the cost of restoring or replacing personal property (including keys) or furniture, excluding ordinary wear and tear

## D007-r015 (A, resolved)
- Pfad: logic/coverage/all[1] / Gap: unresolved_legal_evidence_D007_15
- Entscheidung: Duplikat {"fact": "cleaning_type", "op": "in", "value": ["professional_carpet_cleaning", "professional_cleaning_services"]}
- Begruendung: Korpus schraenkt Profi-Reinigungskosten ein; Basis fordert cleaning_type bereits, Duplikat ist semantikerhaltend.
- Zitat: The landlord cannot require a tenant to pay for, or assert a claim against the tenant or the security deposit for professional carpet cleaning or other professional cleaning services, unless reasonably necessary to return the premises

## D007-r016 (A, resolved)
- Pfad: logic/coverage/all[1] / Gap: unresolved_legal_evidence_D007_16
- Entscheidung: Duplikat {"fact": "unit_covered_by_rent_ordinance", "op": "in", "value": ["fully_covered", "partially_covered"]}
- Begruendung: Korpus belegt Deposit-Zinsen fuer covered Units; Basis fordert unit_covered_by_rent_ordinance bereits, Duplikat ist semantikerhaltend.
- Zitat: For tenancies in units fully or partially covered by Berkeley Rent Ordinance, landlords must pay tenants interest on their security deposit at the end of each year

## D008-r001 (A, resolved)
- Pfad: logic/coverage/all[1] / Gap: unresolved_legal_evidence_D008_1
- Entscheidung: Duplikat {"fact": "tenancy_start_date", "op": "lt", "value": "2025-01-01"}
- Begruendung: Korpus schliesst Tenancies ab 1.1.2025 von der 2026-AGA aus; Basis fordert tenancy_start_date bereits, Duplikat ist semantikerhaltend.
- Zitat: The 2026 AGA may not adjust tenants' rents when their tenancy began on or after January 1, 2025, and who had their rents set pursuant to the Costa-Hawkins Rental Housing Act.

## D009-r001 (A, resolved)
- Pfad: logic/coverage/all[1] / Gap: unresolved_legal_evidence_D009_1
- Entscheidung: Duplikat {"fact": "legal_city", "op": "eq", "value": "Berkeley"}
- Begruendung: Coverage ist Disjunktion (pre-1980 multifamily ODER pre-1996 single-family ODER Rooming-House); Duplikat eines Zweig-Fakts wuerde verengen. legal_city gilt in jedem Zweig und ist korpusbelegt (Berkeley-Guide), daher semantikerhaltend.
- Zitat: Most units in multifamily properties built before 1980 Fully Covered Yes Yes Yes Yes

## D009-r005 (A, resolved)
- Pfad: logic/coverage/all[1] / Gap: unresolved_legal_evidence_D009_5
- Entscheidung: Duplikat {"fact": "legal_city", "op": "eq", "value": "Berkeley"}
- Begruendung: Coverage ist Disjunktion ueber Coverage-Status; legal_city gilt in jedem Zweig und ist korpusbelegt (Berkeley-Guide), daher semantikerhaltend.
- Zitat: New construction: units that were built and received a Certificate of Occupancy after June 1980 Partially Covered Yes No Yes Yes

## D052-r001 (A, resolved)
- Pfad: logic/coverage/all[1] / Gap: unresolved_legal_evidence_D052_1
- Entscheidung: Duplikat {"fact": "state", "op": "eq", "value": "MA"}
- Begruendung: Section 15B gilt statewide fuer residential leases; Deposit-Cap ist korpusbelegt; state-MA-Duplikat ist semantikerhaltend.
- Zitat: no lessor or agent of the lessor may require a tenant or prospective tenant to pay any amount in excess of the following: (i) rent for the first full month of occupancy

## D052-r002 (A, resolved)
- Pfad: logic/coverage/all[1] / Gap: unresolved_legal_evidence_D052_2
- Entscheidung: Duplikat {"fact": "state", "op": "eq", "value": "MA"}
- Begruendung: Fee-in-lieu-Ermoeglichung ist korpusbelegt; state-MA-Duplikat ist semantikerhaltend.
- Zitat: the executive office of housing and livable communities may promulgate regulations to authorize a lessor and a tenant or prospective tenant to agree to the payment of a fee in lieu of payment of a security deposit

## D052-r003 (A, resolved)
- Pfad: logic/coverage/all[1] / Gap: unresolved_legal_evidence_D052_3
- Entscheidung: Duplikat {"fact": "state", "op": "eq", "value": "MA"}
- Begruendung: Key und Lock ist einzige zusaetzliche Vorauszahlung neben Miete und Deposit; korpusbelegt; state-MA-Duplikat ist semantikerhaltend.
- Zitat: (iv) the purchase and installation cost for a key and lock.

## D052-r004 (A, resolved)
- Pfad: logic/coverage/all[1] / Gap: unresolved_legal_evidence_D052_4
- Entscheidung: Duplikat {"fact": "state", "op": "eq", "value": "MA"}
- Begruendung: Separate-Account-Pflicht ist korpusbelegt; state-MA-Duplikat ist semantikerhaltend.
- Zitat: shall be held in a separate, interest-bearing account in a bank, located within the commonwealth under such terms as will place such deposit beyond the claim of creditors of the lessor

## D052-r005 (A, resolved)
- Pfad: logic/coverage/all[1] / Gap: unresolved_legal_evidence_D052_5
- Entscheidung: Duplikat {"fact": "tenancy_duration_years", "op": "gte", "value": 1}
- Begruendung: Korpus belegt 1-Jahr-Schwelle fuer Zinszahlung; Basis fordert tenancy_duration_years bereits, Duplikat ist semantikerhaltend.
- Zitat: who holds a security deposit for a period of one year or longer from the commencement of the term of the tenancy

## D052-r006 (A, resolved)
- Pfad: logic/coverage/all[1] / Gap: unresolved_legal_evidence_D052_6
- Entscheidung: Duplikat {"fact": "state", "op": "eq", "value": "MA"}
- Begruendung: Receipt-Pflicht ist korpusbelegt; state-MA-Duplikat ist semantikerhaltend.
- Zitat: who receives a security deposit from a tenant or prospective tenant shall give said tenant or prospective tenant at the time of receiving such security deposit a receipt indicating the amount of such security deposit

## D052-r007 (A, resolved)
- Pfad: logic/coverage/all[1] / Gap: unresolved_legal_evidence_D052_7
- Entscheidung: Duplikat {"fact": "state", "op": "eq", "value": "MA"}
- Begruendung: Statement-of-Condition (10 Tage) ist korpusbelegt; state-MA-Duplikat ist semantikerhaltend.
- Zitat: upon receipt of such security deposit, or within ten days after commencement of the tenancy, whichever is later, furnish to such tenant or prospective tenant a separate written statement of the present condition of the premises to be leased or rented

## D052-r008 (A, resolved)
- Pfad: logic/coverage/all[1] / Gap: unresolved_legal_evidence_D052_8
- Entscheidung: Duplikat {"fact": "state", "op": "eq", "value": "MA"}
- Begruendung: 30-Tage-Rueckgabe ist korpusbelegt; state-MA-Duplikat ist semantikerhaltend.
- Zitat: The lessor shall, within thirty days after the termination of occupancy under a tenancy-at-will or the end of the tenancy as specified in a valid written lease agreement, return to the tenant the security deposit or any balance thereof

## D052-r009 (A, resolved)
- Pfad: logic/coverage/all[1] / Gap: unresolved_legal_evidence_D052_9
- Entscheidung: Duplikat {"fact": "state", "op": "eq", "value": "MA"}
- Begruendung: Itemized-Damages-Liste unter Eid ist korpusbelegt; state-MA-Duplikat ist semantikerhaltend.
- Zitat: shall provide to the tenant within such thirty days an itemized list of damages, sworn to by the lessor or his agent under pains and penalties of perjury, itemizing in precise detail the nature of the damage

## D052-r010 (A, resolved)
- Pfad: logic/coverage/all[1] / Gap: unresolved_legal_evidence_D052_10
- Entscheidung: Duplikat {"fact": "state", "op": "eq", "value": "MA"}
- Begruendung: Pre-existing-Damage-Verbot ist korpusbelegt; state-MA-Duplikat ist semantikerhaltend.
- Zitat: No amount shall be deducted from the security deposit for any damage to the dwelling unit which was listed in the separate written statement of the present condition

## D052-r012 (A, resolved)
- Pfad: logic/coverage/all[1] / Gap: unresolved_legal_evidence_D052_12
- Entscheidung: Duplikat {"fact": "state", "op": "eq", "value": "MA"}
- Begruendung: Deposit-Transfer bei Sale ist korpusbelegt; state-MA-Duplikat ist semantikerhaltend.
- Zitat: Whenever a lessor who receives a security deposit transfers his interest in the dwelling unit for which the security deposit is held, whether by sale, assignment, death

## D052-r014 (A, resolved)
- Pfad: logic/coverage/all[1] / Gap: unresolved_legal_evidence_D052_14
- Entscheidung: Duplikat {"fact": "state", "op": "eq", "value": "MA"}
- Begruendung: Advance-Rent-Transfer ist korpusbelegt; state-MA-Duplikat ist semantikerhaltend.
- Zitat: the lessor shall credit an amount equal to such rental advance together with any interest which has accrued thereon for the benefit of the tenant

## D052-r015 (A, resolved)
- Pfad: logic/coverage/all[1] / Gap: unresolved_legal_evidence_D052_15
- Entscheidung: Duplikat {"fact": "state", "op": "eq", "value": "MA"}
- Begruendung: 30-Tage-Penalty-Verbot ist korpusbelegt; state-MA-Duplikat ist semantikerhaltend.
- Zitat: No lease or other rental agreement shall impose any interest or penalty for failure to pay rent until thirty days after such rent shall have been due.

## D052-r016 (A, resolved)
- Pfad: logic/coverage/all[1] / Gap: unresolved_legal_evidence_D052_16
- Entscheidung: Duplikat {"fact": "state", "op": "eq", "value": "MA"}
- Begruendung: Advance-Rent-Verbot nach Tenancy-Beginn ist korpusbelegt; state-MA-Duplikat ist semantikerhaltend.
- Zitat: No lessor or successor in interest shall at any time subsequent to the commencement of a tenancy demand rent in advance in excess of the current month's rent

## D052-r017 (A, resolved)
- Pfad: logic/coverage/all[1] / Gap: unresolved_legal_evidence_D052_17
- Entscheidung: Duplikat {"fact": "state", "op": "eq", "value": "MA"}
- Begruendung: Deposit-Eigentum und Trennungsverbot ist korpusbelegt; state-MA-Duplikat ist semantikerhaltend.
- Zitat: A security deposit shall continue to be the property of the tenant making such deposit, shall not be commingled with the assets of the lessor

## D065-r002 (A, resolved)
- Pfad: logic/coverage/all[1] / Gap: unresolved_legal_evidence_D065_2
- Entscheidung: Duplikat {"fact": "application_fee_required", "op": "eq", "value": true}
- Begruendung: Korpus belegt Pre-Fee-Disclosure; Basis fordert application_fee_required bereits, Duplikat ist semantikerhaltend.
- Zitat: Prior to accepting any application fee, a housing provider shall disclose in writing to the applicant whether the eligibility criteria of the housing provider include the review and consideration of criminal history

## D065-r003 (A, resolved)
- Pfad: logic/coverage/all[1] / Gap: unresolved_legal_evidence_D065_3
- Entscheidung: Duplikat {"fact": "rental_property_type", "op": "ne", "value": "owner_occupied_1_to_4_units"}
- Begruendung: Fair-Chance-Act gilt fuer Rental-Dwelling-Units exkl. owner-occupied 1-4 Units; Carve-out ist korpusbelegt (Definitions-Sektion); Duplikat ist semantikerhaltend.
- Zitat: Rental dwelling unit means a dwelling unit offered for rent by a housing provider for residential purposes, other than a dwelling unit in an owner-occupied premises of not more than four dwelling units.

## D065-r004 (A, resolved)
- Pfad: logic/coverage/all[1] / Gap: unresolved_legal_evidence_D065_4
- Entscheidung: Duplikat {"fact": "rental_property_type", "op": "ne", "value": "owner_occupied_1_to_4_units"}
- Begruendung: Korpus belegt verbotene Record-Typen; Carve-out ist korpusbelegt; Duplikat ist semantikerhaltend.
- Zitat: A housing provider shall not, either before or after the issuance of a conditional offer, evaluate an applicant based on any of the following types of criminal records: (1) arrests or charges that have not resulted in a criminal conviction

## D065-r006 (A, resolved)
- Pfad: logic/coverage/all[1] / Gap: unresolved_legal_evidence_D065_6
- Entscheidung: Duplikat {"fact": "considering_allowed_criminal_record", "op": "eq", "value": true}
- Begruendung: Korpus belegt Individualized-Assessment; Basis fordert considering_allowed_criminal_record bereits, Duplikat ist semantikerhaltend.
- Zitat: The housing provider shall perform an individualized assessment of the application in light of the following factors: (a) the nature and severity of the criminal offense

## D065-r007 (A, resolved)
- Pfad: logic/coverage/all[1] / Gap: unresolved_legal_evidence_D065_7
- Entscheidung: Duplikat {"fact": "conditional_offer_issued", "op": "eq", "value": true}
- Begruendung: Korpus belegt Withdrawal-Standard nach Conditional-Offer; Basis fordert conditional_offer_issued bereits, Duplikat ist semantikerhaltend.
- Zitat: A housing provider may withdraw a conditional offer based on an applicant's criminal record only if the housing provider determines, by preponderance of the evidence, that the withdrawal is necessary to fulfill a substantial, legitimate, and nondiscriminatory interest.

## D065-r008 (A, resolved)
- Pfad: logic/coverage/all[1] / Gap: unresolved_legal_evidence_D065_8
- Entscheidung: Duplikat {"fact": "conditional_offer_withdrawn", "op": "eq", "value": true}
- Begruendung: Korpus belegt Withdrawal-Notice; Basis fordert conditional_offer_withdrawn bereits, Duplikat ist semantikerhaltend.
- Zitat: If a housing provider withdraws a conditional offer, the housing provider shall provide the applicant with written notification that includes, with specificity, the reason or reasons for the withdrawal

## D065-r010 (A, resolved)
- Pfad: logic/coverage/all[1] / Gap: unresolved_legal_evidence_D065_10
- Entscheidung: Duplikat {"fact": "rental_property_type", "op": "ne", "value": "owner_occupied_1_to_4_units"}
- Begruendung: Korpus belegt Ad-Verbot; Carve-out ist korpusbelegt; Duplikat ist semantikerhaltend.
- Zitat: A housing provider shall not knowingly or purposefully publish any housing advertisement that explicitly provides that the housing provider will not consider any applicant who has been arrested or convicted

## D065-r011 (A, resolved)
- Pfad: logic/coverage/all[1] / Gap: unresolved_legal_evidence_D065_11
- Entscheidung: Duplikat {"fact": "rental_property_type", "op": "ne", "value": "owner_occupied_1_to_4_units"}
- Begruendung: Korpus belegt Application- und Inquiry-Verbot; Carve-out ist korpusbelegt; Duplikat ist semantikerhaltend.
- Zitat: shall not print, publish, circulate, issue, display, post, or mail, or cause to be printed, published, circulated, issued, displayed, posted or mailed any statement, advertisement, publication or sign

## D065-r015 (A, resolved)
- Pfad: logic/coverage/all[1] / Gap: unresolved_legal_evidence_D065_15
- Entscheidung: Duplikat {"fact": "rental_property_type", "op": "ne", "value": "owner_occupied_1_to_4_units"}
- Begruendung: Korpus belegt Complaint-Weg statt Court; Carve-out ist korpusbelegt; Duplikat ist semantikerhaltend.
- Zitat: An action that alleges a violation of this act shall not be initiated by any person in court. The director, or an applicant or prospective applicant who believes that a housing provider has violated a provision of this act, may file a complaint

## D065-r017 (A, resolved)
- Pfad: logic/coverage/all[1] / Gap: unresolved_legal_evidence_D065_17
- Entscheidung: Duplikat {"fact": "violation_found", "op": "eq", "value": true}
- Begruendung: Korpus belegt Penalty-Tiers; Basis fordert violation_found bereits, Duplikat ist semantikerhaltend.
- Zitat: A housing provider who violates a provision of this act shall be liable for the following applicable penalties: (1) an amount not to exceed $1,000 if the housing provider has not committed any prior violation within the five-year period

## Totals: resolved=54, open=0