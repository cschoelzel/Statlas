"""Ehrliche Parzellen-Facts aus Assessor use_code/use_description.

Nur positive Facts per Allowlist, unverified. Keine Default-False auf
Exemptions, kein year_built->COO, keine Events geraten."""
import re

ALLOW_CODES = {
    "0500", "0501", "050C", "050V", "0551",  # CA apartments
    "A5", "A15",  # CA apartment codes
    "7700", "7200", "7800",  # Alameda apartments
    "111", "112", "120", "A",  # MA (A nur ohne elderly-Text)
    "4C",  # NJ apartments
}
SANDAG_CODES = {"14", "15", "16"}

_APT = re.compile(r"apartment")
_FIVE_PLUS = re.compile(r"(five or more|5\s*\+|5 or more|five\+)")
_TIC = re.compile(r"\btic\b")


def _code(address):
    return str(address.get("use_code") or "").strip().upper()


def _desc(address):
    return str(address.get("use_description") or "").lower()


def _excluded(code, desc):
    if code == "FS5" or "fs5" in desc:
        return True
    if _TIC.search(desc):
        return True
    if "elderly" in desc:
        return True
    if code in ("A", "118") and "elder" in desc:
        return True
    return False


def derive_parcel_facts(address, existing_facts=None):
    """Leite Wohn-Facts aus use_code/use_description ab. Nie raten."""
    address = address or {}
    existing_facts = existing_facts or {}
    code = _code(address)
    desc = _desc(address)
    if not code and not desc:
        return {}
    if _excluded(code, desc):
        return {}
    residential = False
    if code in ALLOW_CODES:
        residential = True
    elif code in SANDAG_CODES and _FIVE_PLUS.search(desc):
        residential = True
    elif _APT.search(desc) or _FIVE_PLUS.search(desc):
        # Expliziter Apartment-/5+-Text ohne Code reicht fuer Wohn-Fact.
        residential = True
    if not residential:
        return {}
    out = {"is_residential_property": True}
    # unit_type wird bewusst NICHT abgeleitet: Das Feld mischt in den Regeln
    # physische Typen ('apartment', D041) und Rechtsstatus ('rent_controlled',
    # D080) sowie Oberbegriffe ('residential_dwelling', D001). Ein
    # abgeleitetes 'apartment' wuerde dort per exaktem Stringvergleich zu
    # falschem does_not_apply statt korrektem unknown fuehren. Apartments
    # sind belegbar keine Mobilheime, daher nur is_mobilehome=False.
    if _APT.search(desc):
        out["is_mobilehome"] = False
    if "mixed" not in desc:
        out["property_type"] = "residential_rental"
        out["property_type_is_residential_rental"] = True
    count = existing_facts.get("unit_count", existing_facts.get("units"))
    try:
        count = int(count)
    except (TypeError, ValueError):
        count = None
    if (count is not None and count >= 5) or _FIVE_PLUS.search(desc):
        out["rental_property_type"] = "multifamily_5_plus"
    return out
