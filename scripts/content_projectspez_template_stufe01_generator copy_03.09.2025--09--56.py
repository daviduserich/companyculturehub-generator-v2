import csv
import json
import re
from pathlib import Path
from datetime import datetime
import logging
import argparse
import sys

# ... (Der obere Teil mit argparse und der Pfad-Abfrage bleibt exakt gleich) ...
# START COPY-PASTE HIER

# ==============================================================================
# 1. INTERAKTIVE & DYNAMISCHE PROJEKTPFAD-ERMITTLUNG
# ==============================================================================
parser = argparse.ArgumentParser(
    description="Generiert ein maßgeschneidertes Content-Template für ein spezifisches Projekt.",
    formatter_class=argparse.RawTextHelpFormatter
)
parser.add_argument(
    "project_path", type=str, nargs="?",
    help="Der vollständige Pfad zum Projektordner.\n"
         "Dieser Ordner muss eine 'layout_extended_v2.csv' enthalten.\n"
         "Beispielaufruf: python content_generator.py /pfad/zum/projekt"
)
args = parser.parse_args()

if args.project_path:
    project_path_str = args.project_path
    print(f"Projektpfad '{project_path_str}' wurde über Kommandozeile erkannt.")
else:
    print("="*60, "\nINTERAKTIVER MODUS: KEIN PROJEKTPFAD ANGEGEBEN\n", "="*60)
    print("Dieses Skript benötigt den Pfad zu einem Projektordner.")
    print("Der angegebene Ordner muss eine 'layout_extended_v2.csv' enthalten.\n")
    project_path_str = input("Bitte geben Sie jetzt den vollständigen Pfad zum Projektordner ein und drücken Sie Enter:\n> ")

PROJECT_DIR = Path(project_path_str).resolve()

if not PROJECT_DIR.is_dir():
    print(f"\nFEHLER: Der angegebene Pfad '{PROJECT_DIR}' ist kein gültiger Ordner.")
    sys.exit(1)

CSV_LAYOUT_PATH = PROJECT_DIR / 'layout_extended_v2.csv'
if not CSV_LAYOUT_PATH.exists():
    print(f"\nFEHLER: Im Ordner '{PROJECT_DIR}' wurde keine 'layout_extended_v2.csv' gefunden.")
    sys.exit(1)

print(f"Verarbeite Projekt in: {PROJECT_DIR}\n")

# ==============================================================================
# 2. KONFIGURATION & PFADE
# ==============================================================================
SCRIPT_DIR = Path(__file__).parent.resolve()
BASE_DIR = SCRIPT_DIR.parent
TEMPLATES_DIR = BASE_DIR / 'templates/components'

# NEU: Angepasster Output-Dateiname und Speicherort
OUTPUT_FILENAME_PREFIX = 'project_template_Stufe01_Anleitung'
# Die Datei wird jetzt direkt im Projektordner gespeichert, nicht in einem 'output' Unterordner.
OUTPUT_DIR = PROJECT_DIR 

logging.basicConfig(
    filename=OUTPUT_DIR / 'content_generator.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filemode='w'
)
placeholder_pattern = re.compile(r'\{\{([^}]+)\}\}')

# ==============================================================================
# 3. HELFERFUNKTIONEN (unverändert)
# ==============================================================================
def load_field_definitions(component_name, definitions_dir):
    json_path = definitions_dir / f"{component_name}.json"
    if not json_path.exists():
        logging.warning(f"Keine Definitionsdatei für '{component_name}' unter '{json_path}' gefunden.")
        return {}
    with open(json_path, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            logging.error(f"Fehler beim Parsen der JSON-Datei: '{json_path}'")
            return {}

def get_definition_for_placeholder(placeholder, definitions, use_example_values=False):
    keys = placeholder.split('.')
    d = definitions
    for key in keys:
        if isinstance(d, dict) and key in d:
            d = d[key]
        else:
            return {"description": f"FEHLER: Keine Definition für '{placeholder}' gefunden.", "value": ""}
    
    # NEU: Logik für den Vorschau-Modus
    final_value = d.get("example_value", "") if use_example_values else d.get("value", "")

    return {"description": d.get("description", f"Container-Element für '{placeholder}'."), "value": final_value}

# ==============================================================================
# 4. KERNLOGIK: DER INTELLIGENTE CONTENT-GENERATOR
# ==============================================================================
def generate_content_template():
    logging.info(f"Starte Content-Generierungsprozess für Projekt: {PROJECT_DIR}")
    
    # ... (Der Rest der Funktion bleibt gleich, aber wir passen den Output-Pfad am Ende an)
    # ... (Komplette `generate_content_template` Funktion von oben hier einfügen)

    # --- Schritt 1: Projekt-Layout laden ---
    try:
        with open(CSV_LAYOUT_PATH, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(line for line in f if line.strip())
            layout = [row for row in reader]
        logging.info(f"Projekt-Layout-CSV '{CSV_LAYOUT_PATH}' erfolgreich geladen.")
    except Exception as e:
        logging.error(f"FEHLER beim Lesen der CSV-Datei: {e}")
        print(f"FEHLER beim Lesen der CSV-Datei: {e}")
        return

    # --- Schritt 2: JSON-Grundstruktur aufbauen ---
    content = {
        "metadata": {
            "generated_at": datetime.now().isoformat(),
            "generator_version": "v5.1-final-audited-naming",
            "layout_source": str(CSV_LAYOUT_PATH)
        },
        "page_content": {}
    }

    # --- Schritt 3: Jede Komponente aus dem Projekt-Layout verarbeiten ---
    for row in layout:
        component = row.get('component')
        if not component or row.get('enabled', 'FALSE').upper() != 'TRUE':
            continue

        logging.info(f"Verarbeite Komponente: '{component}'")
        definitions = load_field_definitions(component, TEMPLATES_DIR)
        html_path = TEMPLATES_DIR / f"{component}.html"
        if not html_path.exists():
            logging.warning(f"Kein HTML-Template für '{component}' gefunden. Komponente wird übersprungen.")
            continue
        html_content = html_path.read_text(encoding='utf-8')
        all_placeholders = set(p.strip() for p in placeholder_pattern.findall(html_content))

        instance_count = int(row.get('max_count', 0))
        if instance_count == 0: continue
        content["page_content"][component] = []

        for i in range(1, instance_count + 1):
            instance_content = {}
            processed_placeholders = set()
            list_marker_pattern = re.compile(r'BEGIN_LIST_ITEM:([\w_]+)')
            for list_name in list_marker_pattern.findall(html_content):
                list_item_count = int(row.get('max_list_items', 0))
                list_content = []
                list_block_pattern = re.compile(rf'<!-- BEGIN_LIST_ITEM:{list_name} -->(.*?)<!-- END_LIST_ITEM:{list_name} -->', re.DOTALL)
                list_block_match = list_block_pattern.search(html_content)
                if not list_block_match: continue
                list_item_placeholders = set(placeholder_pattern.findall(list_block_match.group(1)))
                for j in range(1, list_item_count + 1):
                    list_item_content = {}
                    for placeholder in list_item_placeholders:
                        definition_key = f"{list_name}.{placeholder}"
                        list_item_content[placeholder] = get_definition_for_placeholder(definition_key, definitions)
                    list_content.append(list_item_content)
                instance_content[list_name] = list_content
                processed_placeholders.update(list_item_placeholders)
                processed_placeholders.add(f'BEGIN_LIST_ITEM:{list_name}')
                processed_placeholders.add(f'END_LIST_ITEM:{list_name}')
            for placeholder in all_placeholders:
                if placeholder in processed_placeholders or '.' in placeholder: continue
                instance_content[placeholder] = get_definition_for_placeholder(placeholder, definitions)
                processed_placeholders.add(placeholder)
            content["page_content"][component].append(instance_content)

    # --- Schritt 4: Finale JSON-Datei speichern (mit neuem Namen und Ort) ---
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_filename = f'{OUTPUT_FILENAME_PREFIX}_{timestamp}.json'
    output_path = OUTPUT_DIR / output_filename
    
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(content, f, indent=2, ensure_ascii=False)
        logging.info(f"Prozess abgeschlossen. Template wurde hier gespeichert: '{output_path}'")
        print(f"Prozess erfolgreich abgeschlossen. Output in '{output_path}'")
    except Exception as e:
        logging.error(f"FEHLER beim Schreiben der JSON-Datei: {e}")
        print(f"FEHLER beim Schreiben der JSON-Datei: {e}")

# ==============================================================================
# 5. SKRIPT AUSFÜHREN
# ==============================================================================
if __name__ == "__main__":
    generate_content_template()

