import os
from pathlib import Path
from datetime import datetime

# ==============================================================================
# 1. KONFIGURATION (Angepasst an deine Ordnerstruktur)
# ==============================================================================

# Pfade werden relativ zum Skript-Speicherort definiert, um es robust zu machen.
# Annahme: Das Skript liegt in 'scripts/'.
SCRIPT_DIR = Path(__file__).resolve().parent
BASE_DIR = SCRIPT_DIR.parent  # Geht einen Ordner hoch zu 'companyculturehub-generator-v2/'

# Eingabe- und Ausgabe-Verzeichnisse
COMPONENTS_DIR = BASE_DIR / 'templates' / 'components'
OUTPUT_DIR = COMPONENTS_DIR / 'en_bloc_html_s'

# Verzeichnisse und Dateien, die beim Sammeln ignoriert werden sollen
EXCLUDE_DIRS = ['Archiv-Components', 'en_bloc_html_s']
EXCLUDE_FILES = ['global_variables.csv']

# ==============================================================================
# 2. KERNLOGIK: KOMPONENTEN-AGGREGATOR
# ==============================================================================

def aggregate_components():
    """
    Sammelt alle HTML-Komponenten-Dateien und fasst sie in einer einzigen
    Markdown-Datei zusammen, um sie leicht mit einem LLM teilen zu können.
    """
    print("Starte den Prozess zum Zusammenfassen der Komponenten...")

    # --- Schritt 1: Sicherstellen, dass das Ausgabe-Verzeichnis existiert ---
    try:
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    except OSError as e:
        print(f"FEHLER: Das Ausgabe-Verzeichnis '{OUTPUT_DIR}' konnte nicht erstellt werden: {e}")
        return

    # --- Schritt 2: Alle relevanten HTML-Dateien sammeln ---
    component_files = []
    for item in sorted(COMPONENTS_DIR.iterdir()):
        # Ignoriere ausgeschlossene Verzeichnisse
        if item.is_dir() and item.name in EXCLUDE_DIRS:
            continue
        # Ignoriere ausgeschlossene Dateien und alle Nicht-HTML-Dateien
        if item.is_file():
            if item.name in EXCLUDE_FILES or not item.name.endswith('.html'):
                continue
            component_files.append(item)

    if not component_files:
        print("Keine HTML-Komponenten zum Zusammenfassen gefunden. Prozess wird beendet.")
        return
        
    print(f"{len(component_files)} Komponenten gefunden. Beginne mit dem Zusammenbau des Dokuments...")

    # --- Schritt 3: Den Inhalt für die Markdown-Datei vorbereiten ---
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Einleitungstext, der den Kontext für das LLM erklärt
    intro_text = f"""# Komponenten-Zusammenzug (en bloc)

**Generiert am:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Kontext
Dieses Dokument enthält den gesamten HTML-Quellcode aller aktiven Webseiten-Module (Komponenten).
Diese Module werden von einem Python-Skript verwendet, um dynamisch eine vollständige JSON-Content-Vorlage für eine Webseite zu generieren.

Jedes Modul ist eine eigenständige HTML-Datei, die Platzhalter im Format `{{{{ placeholder_name }}}}` enthält.

**Zweck dieses Dokuments:**
Einem Large Language Model (LLM) einen vollständigen Überblick über alle vorhandenen Module zu geben, um Analysen, Vorschläge oder Code-Generierungen durchzuführen.

---"""

    # --- Schritt 4: Alle Dateien zu einem einzigen String zusammenfügen ---
    aggregated_content = [intro_text]
    for component_path in component_files:
        try:
            with open(component_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            block = f"""
## Modul: `{component_path.name}`

```html
{html_content.strip()}
```
"""
            aggregated_content.append(block)
        except Exception as e:
            print(f"Konnte Datei '{component_path.name}' nicht lesen: {e}")
            continue

    # --- Schritt 5: Die finale Markdown-Datei schreiben ---
    output_filename = f"en_bloc_components_{timestamp}.md"
    output_path = OUTPUT_DIR / output_filename

    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("\n".join(aggregated_content))
        print(f"\nProzess erfolgreich abgeschlossen!")
        print(f"Die zusammengefasste Datei wurde hier gespeichert:\n{output_path}")
    except Exception as e:
        print(f"FEHLER: Die Ausgabedatei '{output_path}' konnte nicht geschrieben werden: {e}")

# ==============================================================================
# 3. SKRIPT AUSFÜHREN
# ==============================================================================

if __name__ == "__main__":
    aggregate_components()