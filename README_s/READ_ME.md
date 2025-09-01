🏢 CompanyCultureHub Generator (v4.2)
Eine automatisierte Engine zur Generierung von Employer Branding Landing Pages. Sie integriert Farben, Schriftarten und Inhalte aus dem ersten Repo (color-extraction-engine) und erzeugt CI-kongruente Webseiten basierend auf modularen Templates. Das System ist praxisnah, mit Aufräum-Logik und GitHub Pages-Hosting.
✨ Features

Automatisierte Generierung: Aus content.json, layout.csv und injizierten Design-Daten (aus Repo 1) entsteht eine HTML-Seite.
Theming-Engine: Granulare Kontrolle über Stile (z. B. classic vs. stylish) via Presets oder manuelle Optionen.
Injektion von CI-Elementen: Farben/Schriftarten aus color_definitions.json werden automatisch integriert.
Aufräum- und Archivierung: Alte Dateien werden archiviert, verarbeitete Projekte markiert.
Multi-Projekt-Support: Jeder Ordner in content/ ist ein separates Projekt.
Kostenloses Hosting: GitHub Pages für Live-Schaltung.

🚀 Quick-Start

Neues Projekt initialisieren:
python scripts/init_new_project.py


Erstellt content/new-project-bitte_befuellen/ mit Vorlagen (content.json, layout.csv).
Benenne den Ordner um (z. B. content/mein_projekt/).


Farben/Schriftarten aus Repo 1 injizieren:

Kopiere color_definitions.json aus Repo 1 in den Projekt-Ordner.

python scripts/injector.py --project mein_projekt


Erzeugt content_color_injected.json.


Inhalte anpassen: Bearbeite content.json (Texte, Überschriften) und layout.csv (Reihenfolge der Komponenten).

Seite generieren:
python scripts/generator_v_fullpower.py


Aufräumt alte Dateien, generiert docs/mein_projekt.html, markiert Projekt als processed_*.


Live schalten: Commit und push → GitHub Actions deployt auf GitHub Pages.


📁 Projektstruktur
companyculturehub-generator-v2/
├── content/                          # Projekt-Ordner (jeder Unterordner = ein Projekt)
│   ├── content_template_new_project/ # Vorlage (content.json, layout.csv)
│   ├── proceed_contents_archives/    # Archivierte Projekte
│   └── mein_projekt/                 # Beispiel: content.json, layout.csv, color_definitions.json
├── docs/                             # Generierte Outputs (GitHub Pages)
│   ├── assets/images/                # Bilder/Logos
│   └── docs_archives/                # Archivierte HTML
├── scripts/                          # Skripte
│   ├── init_new_project.py           # Initialisiert neue Projekte
│   ├── injector.py                   # Injiziert Design-Daten
│   ├── generator_v_fullpower.py      # Generiert HTML
│   └── archives/                     # Alte Skripte
├── templates/                        # HTML-Vorlagen
│   ├── components/                   # Modulare Sektionen (z. B. hero_section.html)
│   └── archives/                     # Alte Templates
├── requirements.txt                  # Dependencies
└── docs/                             # Dokumentation (z. B. THEMING_ENGINE_GUIDE.md)

🔄 Workflow

Projekt erstellen: Nutze init_new_project.py für Vorlage.
Design injizieren: injector.py kombiniert color_definitions.json (aus Repo 1) mit content.json.
Generierung: generator_v_fullpower.py:
Phase 1 (Aufräumen): Archiviert alte HTML in docs/docs_archives/ und Projekte in content/proceed_contents_archives/.
Phase 2 (Generierung): Liest injizierte Daten, füllt Templates aus, wendet Theming an (z. B. CSS-Klassen basierend auf presentation_style).
Phase 3 (Markieren): Benennt Projekt-Ordner zu processed_*.


Hosting: Push → GitHub Pages.

Integration mit Repo 1: Outputs aus Repo 1 werden in injector.py verwendet; erweitere für bessere Harmonie (z. B. automatische Gradient-Generierung).
🛠️ Troubleshooting

Kein Design injiziert: Stelle sicher, dass color_definitions.json im Projekt-Ordner liegt.
Veraltete Dateien: Führe generator_v_fullpower.py aus, um aufzuräumen.
Styling-Probleme: Überprüfe theme_options in content.json (siehe THEMING_ENGINE_GUIDE.md).

Siehe docs/PRAXIS_TIPPS.md für detaillierte Tipps.
📈 Geplante Features

Automatische Farb-Harmonisierung (z. B. "fade-up" Gradients für dunkle Paletten).
Logo-Extraktion aus Repo 1.
Batch-Generierung aller Projekte.

🤝 Beitragen
Fork → Branch → Commit → Pull Request.
📄 Lizenz
MIT License.