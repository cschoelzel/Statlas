"""Spitzen-Goal Abnahmetests S1-S12 (Runde 1)."""
import json, os, unittest
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def P(*a): return os.path.join(ROOT, *a)
def J(*a):
    with open(P(*a)) as f: return json.load(f)
class S1Extraction(unittest.TestCase):
    def test_rules_schema_und_menge(self):
        rules = J("output", "rules.json")
        self.assertIsInstance(rules, list)
        self.assertGreaterEqual(len(rules), 150, "Regelbasis zu klein")
        for r in rules[:30]:
            for f in ("jurisdiction", "category", "status"):
                self.assertIn(f, r, "Feld fehlt: " + f)
class S2Coverage(unittest.TestCase):
    def test_500_adressen_mit_entscheidungen(self):
        lk = J("output", "lookups.json")["lookups"]
        self.assertGreaterEqual(len(lk), 500)
        leere = [a for a, d in lk.items() if not d]
        self.assertEqual(leere, [], "Adressen ohne Entscheidungen")
class S3Belege(unittest.TestCase):
    def test_entscheidungen_tragen_beleg_oder_frage(self):
        lk = J("output", "lookups.json")["lookups"]
        n = 0
        for a, dec in list(lk.items())[:60]:
            for d in dec[:6]:
                n += 1
                if d.get("result") == "unknown":
                    self.assertTrue(d.get("targeted_questions"), "fragloses unknown")
                else:
                    self.assertIn("explanation", d)
        self.assertGreater(n, 0)
class S4Changes(unittest.TestCase):
    def test_t1_t5_dokumentiert(self):
        ch = J("output", "changes.json")
        for t in ("T1", "T2", "T3", "T4", "T5"):
            self.assertIn(t, ch, t + " fehlt")
            self.assertIn("status", ch[t])
    def test_t6_luecke_benannt(self):
        ch = J("output", "changes.json")
        ok = ("T6" not in ch) or (ch.get("T6", {}).get("status") in ("blocked", "incomplete", "correctly_empty"))
        self.assertTrue(ok, "T6 ohne Hour-16-Daten darf nicht bestehen")
class S5Artefakte(unittest.TestCase):
    def test_pflichtdateien_valide(self):
        for f in ("rules.json", "lookups.json", "changes.json", "manifest.json"):
            self.assertTrue(J("output", f), "output/" + f + " leer")
        m = J("output", "manifest.json")
        self.assertIn("sha256", m)
        self.assertIn("disclaimer", m)
class S6UnknownFragen(unittest.TestCase):
    def test_kein_fragloses_unknown(self):
        lk = J("output", "lookups.json")["lookups"]
        bad = [(a, d.get("team_rule_id")) for a, dec in lk.items() for d in dec if d.get("result") == "unknown" and not d.get("targeted_questions")]
        self.assertEqual(bad, [], "fraglose unknowns vorhanden")
class S7ScoreDev(unittest.TestCase):
    def test_score_lauf_dokumentiert(self):
        self.assertTrue(os.path.exists(P("reports", "score_dev.md")), "reports/score_dev.md fehlt")
class S8Demo(unittest.TestCase):
    def test_demo_mindestumfang(self):
        with open(P("web", "index.html")) as f:
            html = f.read()
        self.assertIn("Not legal advice", html, "Demo ohne Disclaimer")
        self.assertTrue(("as of" in html) or ("as_of" in html), "Demo ohne as-of/Stichtag")
    def test_i18n_toggle_ohne_regeluebersetzung(self):
        with open(P("web", "index.html")) as f:
            idx = f.read()
        with open(P("web", "results.html")) as f:
            res = f.read()
        for html in (idx, res):
            self.assertIn("lang-toggle", html)
            self.assertIn("rhn-lang", html)
            self.assertIn("data-lang-btn", html)
            self.assertGreaterEqual(html.count("data-lang-btn"), 3)
            self.assertIn(">EN<", html)
            self.assertIn(">DE<", html)
            self.assertIn(">ES<", html)
            self.assertIn("localStorage", html)
            self.assertIn("data-i18n", html)
        self.assertIn("Legal texts shown in original (EN) only.", idx)
        self.assertIn("legalNoteRes", res)
        for frag in ("rule.title", "rule.requirement", "quoted_span", "d.explanation"):
            self.assertIn(frag, res)
            self.assertNotIn("t(" + frag, res)
            self.assertNotIn("translate(" + frag, res)
            self.assertNotIn("I18N[" + frag, res)
class S9Responsible(unittest.TestCase):
    def test_conflict_flag_und_audit(self):
        lk = J("output", "lookups.json")["lookups"]
        probe = lk[sorted(lk)[0]][0]
        self.assertIn("conflict_flag", probe)
        self.assertTrue(os.path.exists(P("reports", "ziel_100_prozent.md")), "Audit-Basis fehlt")
    def test_demo_zeigt_confidence_und_konflikt(self):
        with open(P("web", "results.html")) as f:
            html = f.read()
        self.assertIn("Vertrauen:", html, "Demo ohne Confidence-Anzeige")
        self.assertIn("conflict-banner", html, "Demo ohne Konflikt-Banner")
        self.assertIn("conflict_flag", html, "Demo wertet conflict_flag nicht aus")
class S10Skalierung(unittest.TestCase):
    def test_manifest_stempel(self):
        import re
        m = J("output", "manifest.json")
        self.assertRegex(m.get("sha256", ""), r"[0-9a-f]{8,}")
        self.assertGreaterEqual(m.get("addresses", 0), 500)
class S5bFingerprint(unittest.TestCase):
    def test_manifest_fingerprint_nachgerechnet(self):
        import hashlib, sys
        sys.path.insert(0, P())
        from navigator.app import canonical
        rules = J("output", "rules.json")
        lookups = J("output", "lookups.json")["lookups"]
        changes = J("output", "changes.json")
        fp = hashlib.sha256(canonical({"rules": rules, "lookups": lookups, "changes": changes}).encode()).hexdigest()
        self.assertEqual(fp, J("output", "manifest.json")["sha256"],
                         "Manifest-SHA stimmt nicht mit Re-Export ueberein (Methode: navigator/app.py export())")

class S11Repo(unittest.TestCase):
    def test_readme_mit_demo_link(self):
        cand = [c for c in [P("README.md"), P("participant-final-no-hour16 3", "README.md")] if os.path.exists(c)]
        self.assertTrue(cand, "kein README im Repo")
        with open(cand[0]) as f:
            content = f.read()
        self.assertRegex(content, r"https?://", "README ohne Demo-Link")
class S12Videos(unittest.TestCase):
    def test_video_nachweise(self):
        self.assertTrue(os.path.exists(P("reports", "videos.md")), "reports/videos.md fehlt")
if __name__ == "__main__":
    unittest.main()
