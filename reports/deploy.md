# Deploy-Plan Live-Demo (S11, Stand 2026-10-04)

Status: lokales Git-Repo initialisiert und committet (9141b7d), Arbeitsbaum sauber. Remote/Push und Hosting noch offen.

## Befund: Demo braucht aktuell einen Server
- web/results.html laedt Auswertungen per fetch vom lokalen Server (python3 -m navigator.app serve, 127.0.0.1:8765).
- Reines Static-Hosting (z.B. GitHub Pages) zeigt die Seiten, aber keine Live-Auswertung ohne Backend oder Static-Export.

## Optionen
A) Kleiner Hoster mit Python (z.B. Render/Railway/VM): Repo pushen, Server laufen lassen, URL in README + videos.md eintragen.
B) Static-Export bauen [UMGESETZT 2026-10-04]: scripts/export_static_demo.py (500 Adressen, byte-identisch zum Live-Lookup) + results.html-Fallback auf web/data/*.json (generiert, git-ignored). Noch zu tun: pushen, Pages aktivieren, Link in README.

## Naechste Schritte (brauchen dich)
1. GitHub-Repo anlegen (Vorschlag: rental-housing-law-navigator).
2. git remote add origin <url> && git push -u origin main (braucht deine GitHub-Anmeldung).
3. Option A oder B waehlen.
