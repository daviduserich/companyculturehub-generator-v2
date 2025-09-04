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
# 2. KERNLOGIK: KOMPONENTEN-AGGREGATOR (HTML + JSON)
# ==============================================================================

def aggregate_components():
    """
    Sammelt alle HTML-Komponenten-Dateien und fasst sie in einer einzigen
    Markdown-Datei zusammen. Erstellt zusätzlich eine zweite Datei mit den
    entsprechenden JSON-Dateien (nur für HTML-Dateien, die auch existieren).
    """
    print("Starte den Prozess zum Zusammenfassen der Komponenten...")

    # --- Schritt 1: Sicherstellen, dass das Ausgabe-Verzeichnis existiert ---
    try:
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    except OSError as e:
        print(f"FEHLER: Das Ausgabe-Verzeichnis '{OUTPUT_DIR}' konnte nicht erstellt werden: {e}")
        return

    # --- Schritt 2: Alle relevanten HTML-Dateien sammeln ---
    html_files = []
    for item in sorted(COMPONENTS_DIR.iterdir()):
        # Ignoriere ausgeschlossene Verzeichnisse
        if item.is_dir() and item.name in EXCLUDE_DIRS:
            continue
        # Ignoriere ausgeschlossene Dateien und alle Nicht-HTML-Dateien
        if item.is_file():
            if item.name in EXCLUDE_FILES or not item.name.endswith('.html'):
                continue
            html_files.append(item)

    if not html_files:
        print("Keine HTML-Komponenten zum Zusammenfassen gefunden. Prozess wird beendet.")
        return
        
    print(f"{len(html_files)} HTML-Komponenten gefunden.")

    # --- Schritt 3: Entsprechende JSON-Dateien finden ---
    json_files = []
    for html_file in html_files:
        # Erstelle den Namen der entsprechenden JSON-Datei
        json_filename = html_file.stem + '.json'  # .stem entfernt die Dateiendung
        json_path = COMPONENTS_DIR / json_filename
        
        if json_path.exists():
            json_files.append(json_path)
            print(f"  ✓ {html_file.name} → {json_filename} gefunden")
        else:
            print(f"  ⚠ {html_file.name} → {json_filename} NICHT gefunden")

    print(f"{len(json_files)} entsprechende JSON-Dateien gefunden.")

    # --- Schritt 4: Zeitstempel für beide Dateien ---
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # --- Schritt 5: HTML en_bloc Datei erstellen ---
    create_html_en_bloc(html_files, timestamp)
    
    # --- Schritt 6: JSON en_bloc Datei erstellen ---
    if json_files:
        create_json_en_bloc(json_files, timestamp)
    else:
        print("Keine JSON-Dateien zum Zusammenfassen gefunden.")

def create_html_en_bloc(html_files, timestamp):
    """Erstellt die HTML en_bloc Datei"""
    print("\nErstelle HTML en_bloc Datei...")
    
    # Einleitungstext für HTML-Datei
    intro_text = f"""# HTML-Komponenten-Zusammenzug (en bloc)

**Generiert am:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Kontext
Dieses Dokument enthält den gesamten HTML-Quellcode aller aktiven Webseiten-Module (Komponenten).
Diese Module werden von einem Python-Skript verwendet, um dynamisch eine vollständige JSON-Content-Vorlage für eine Webseite zu generieren.

Jedes Modul ist eine eigenständige HTML-Datei, die Platzhalter im Format `{{{{ placeholder_name }}}}` enthält.

**Zweck dieses Dokuments:**
Einem Large Language Model (LLM) einen vollständigen Überblick über alle vorhandenen HTML-Module zu geben, um Analysen, Vorschläge oder Code-Generierungen durchzuführen.

**Anzahl der Module:** {len(html_files)}

---"""

    # Alle HTML-Dateien zusammenfügen
    aggregated_content = [intro_text]
    for html_path in html_files:
        try:
            with open(html_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            block = f"""
## HTML-Modul: `{html_path.name}`

```html
{html_content.strip()}
```
"""
            aggregated_content.append(block)
        except Exception as e:
            print(f"Konnte HTML-Datei '{html_path.name}' nicht lesen: {e}")
            continue

    # HTML-Datei schreiben
    html_output_filename = f"en_bloc_components_HTML_{timestamp}.md"
    html_output_path = OUTPUT_DIR / html_output_filename

    try:
        with open(html_output_path, 'w', encoding='utf-8') as f:
            f.write("\n".join(aggregated_content))
        print(f"✓ HTML en_bloc Datei erstellt: {html_output_path}")
    except Exception as e:
        print(f"FEHLER: HTML-Ausgabedatei '{html_output_path}' konnte nicht geschrieben werden: {e}")

def create_json_en_bloc(json_files, timestamp):
    """Erstellt die JSON en_bloc Datei"""
    print("Erstelle JSON en_bloc Datei...")
    
    # Einleitungstext für JSON-Datei
    intro_text = f"""# JSON-Komponenten-Zusammenzug (en bloc)

**Generiert am:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Kontext
Dieses Dokument enthält alle JSON-Konfigurationsdateien der aktiven Webseiten-Module (Komponenten).
Diese JSON-Dateien enthalten die Datenstrukturen und Konfigurationen, die für die entsprechenden HTML-Module verwendet werden.

**Zweck dieses Dokuments:**
Einem Large Language Model (LLM) einen vollständigen Überblick über alle vorhandenen JSON-Datenstrukturen zu geben, um Analysen, Vorschläge oder Code-Generierungen durchzuführen.

**Anzahl der JSON-Module:** {len(json_files)}

**Hinweis:** Diese Datei enthält nur JSON-Dateien, für die auch entsprechende HTML-Module existieren.

---"""

    # Alle JSON-Dateien zusammenfügen
    aggregated_content = [intro_text]
    for json_path in json_files:
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                json_content = f.read()
            
            block = f"""
## JSON-Modul: `{json_path.name}`

```json
{json_content.strip()}
```
"""
            aggregated_content.append(block)
        except Exception as e:
            print(f"Konnte JSON-Datei '{json_path.name}' nicht lesen: {e}")
            continue

    # JSON-Datei schreiben
    json_output_filename = f"en_bloc_components_JSON_{timestamp}.md"
    json_output_path = OUTPUT_DIR / json_output_filename

    try:
        with open(json_output_path, 'w', encoding='utf-8') as f:
            f.write("\n".join(aggregated_content))
        print(f"✓ JSON en_bloc Datei erstellt: {json_output_path}")
    except Exception as e:
        print(f"FEHLER: JSON-Ausgabedatei '{json_output_path}' konnte nicht geschrieben werden: {e}")

# ==============================================================================
# 3. SKRIPT AUSFÜHREN
# ==============================================================================

if __name__ == "__main__":
    aggregate_components()
    print(f"\nProzess erfolgreich abgeschlossen!")
    print(f"Beide en_bloc Dateien wurden hier gespeichert:\n{OUTPUT_DIR}")