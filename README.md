# 🏢 CompanyCultureHub Generator

Dieses Projekt generiert automatisch ansprechende "Employer Branding"-Webseiten aus einfachen JSON-Datendateien. Es nutzt GitHub Actions, um den Prozess vom Hochladen der Inhalte bis zur Live-Schaltung der Webseite vollständig zu automatisieren.

## ✨ Features

- **Vollautomatisch:** JSON-Datei hochladen → Webseite wird live geschaltet.
- **Multi-Client-fähig:** Jede JSON-Datei im `content`-Ordner wird zu einer eigenen HTML-Seite.
- **Zentrale Vorlage:** Alle Seiten basieren auf einem einzigen, leicht anpassbaren HTML-Template.
- **Kostenloses Hosting:** Nutzt GitHub Pages für schnelles und kostenloses Hosting.
- **Einfache Inhaltsverwaltung:** Keine HTML-Kenntnisse für die Inhaltspflege nötig – nur JSON.

---

## 🚀 Quick-Start: Eine neue Firmenseite hinzufügen

1.  **JSON-Datei erstellen:** Kopiere eine bestehende JSON-Datei (z.B. `content/example_hilbrand.json`) oder erstelle eine neue. Der Dateiname wird Teil der URL (z.B. `neue_firma.json` wird zu `neue_firma.html`).
2.  **Inhalte anpassen:** Bearbeite die Texte, Bildpfade und Links in deiner neuen JSON-Datei.
3.  **Bilder hochladen:** Lade die benötigten Bilder in den Ordner `docs/assets/images/` hoch.
4.  **Dateien hochladen:**
    - Öffne das Projekt in einem **Codespace**.
    - Führe im Terminal `git pull origin main` aus.
    - Lade deine neue JSON-Datei in den `content`-Ordner hoch.
    - Committe und pushe die Änderungen mit einer Nachricht (z.B. "feat: Add new company page for [Firmenname]").
5.  **Fertig!** Die GitHub Action startet automatisch, baut die neue Seite und fügt sie zur `index.html`-Übersichtsseite hinzu. Nach ca. 2 Minuten ist die neue Seite live.

---

## 📂 Projektstruktur

- **`.github/workflows/`**: Enthält den GitHub Actions Workflow, der alles automatisiert.
- **`content/`**: **Hier lebst du!** In diesem Ordner werden die JSON-Dateien für die einzelnen Firmenseiten abgelegt.
- **`docs/`**: Das Zielverzeichnis. Hier landen die fertigen HTML-Seiten und alle öffentlichen Assets (Bilder, etc.). Dieser Ordner wird von GitHub Pages veröffentlicht.
- **`scripts/`**: Enthält das zentrale Python-Skript, das die Magie vollbringt und die Seiten generiert.
- **`templates/`**: Enthält die HTML-Vorlage, die als Schablone für alle Seiten dient.

