import csv
import json
import re
from pathlib import Path
from datetime import datetime
import logging

# Globale Regex-Definition
placeholder_pattern = re.compile(r'\{\{([^}]+)\}\}')

# ==============================================================================
# 1. KONFIGURATION & LOGGING
# ==============================================================================

SCRIPT_DIR = Path(__file__).parent
BASE_DIR = SCRIPT_DIR.parent

logging.basicConfig(
    filename='content_generator.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filemode='w'
)

CSV_LAYOUT_PATH = BASE_DIR / 'content_template_new_project/layout_extended_v2.csv'
TEMPLATES_DIR = BASE_DIR / 'templates/components'
OUTPUT_DIR = BASE_DIR / 'content_template_nach_update_modules'

OUTPUT_FILENAME_PREFIX = 'content_template'
GLOBAL_VARS_PATH = TEMPLATES_DIR / 'global_variables.csv'
LOCAL_VARS_PATH = TEMPLATES_DIR / 'local_variables.csv'

# ==============================================================================
# 2. HELFERFUNKTIONEN
# ==============================================================================

def load_global_variables(path):
    """Liest die globale Variablen-CSV und baut ein verschachteltes Dictionary."""
    global_vars = {}
    if not path.exists():
        logging.warning(f"Globale Variablen-Datei nicht gefunden unter '{path}'. Eine neue wird erstellt.")
        return global_vars

    with open(path, 'r', encoding='utf-8') as f:
        try:
            reader = csv.reader(f)
            header = next(reader, None)
            if not header:
                logging.info(f"'{path}' ist leer. Es werden neue globale Variablen gesammelt.")
                return global_vars
            
            if header[0].strip() != 'key' or header[1].strip() != 'value':
                logging.error(f"'{path}' hat einen ungültigen Header. Erwartet: 'key,value'.")
                raise ValueError("global_variables.csv muss 'key' und 'value' als Header haben.")

            for row in reader:
                if not row or len(row) < 2 or not row[0].strip(): continue
                key, value = row[0].strip(), row[1].strip()
                keys = key.split('.')
                d = global_vars
                for k in keys[:-1]:
                    d = d.setdefault(k, {})
                d[keys[-1]] = value
        except (StopIteration, IndexError):
            logging.info(f"'{path}' scheint leer oder unvollständig zu sein. Es werden neue globale Variablen gesammelt.")
            return global_vars
            
    logging.info(f"Globale Variablen aus '{path}' erfolgreich geladen.")
    return global_vars

def write_missing_global_variables(path, missing_keys, existing_keys):
    """Schreibt neue globale Variablen in die CSV-Datei."""
    new_keys_to_add = sorted(list(set(missing_keys) - set(existing_keys)))
    if not new_keys_to_add:
        return
        
    is_empty_file = not path.exists() or path.stat().st_size == 0
    
    with open(path, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if is_empty_file:
            writer.writerow(['key', 'value'])
            logging.info(f"Neue globale Variablen-Datei '{path}' erstellt oder Header zu leerer Datei hinzugefügt.")
        
        for key in new_keys_to_add:
            writer.writerow([key, "BITTE HIER WERT ERGÄNZEN"])
            logging.info(f"Fehlender globaler Schlüssel '{key}' wurde zu '{path}' hinzugefügt.")

def load_local_variables(path):
    """Liest die lokale Variablen-CSV und baut ein Dictionary pro Komponente."""
    local_vars = {}
    if not path.exists():
        logging.warning(f"Lokale Variablen-Datei nicht gefunden unter '{path}'. Eine neue wird erstellt.")
        return local_vars

    with open(path, 'r', encoding='utf-8') as f:
        try:
            reader = csv.DictReader(f)
            if not reader.fieldnames or set(['component', 'key', 'value']) - set(reader.fieldnames):
                logging.error(f"'{path}' hat einen ungültigen Header. Erwartet: 'component,key,value'.")
                raise ValueError("local_variables.csv muss 'component', 'key', 'value' als Header haben.")

            for row in reader:
                if not row['component'] or not row['key']: continue
                component = row['component'].strip()
                key = row['key'].strip()
                value = row['value'].strip()
                local_vars.setdefault(component, {})[key] = value
        except (StopIteration, IndexError):
            logging.info(f"'{path}' scheint leer oder unvollständig zu sein. Es werden neue lokale Variablen gesammelt.")
            return local_vars
            
    logging.info(f"Lokale Variablen aus '{path}' erfolgreich geladen.")
    return local_vars

def write_missing_local_variables(path, missing_vars):
    """Schreibt neue lokale Variablen in die CSV-Datei."""
    if not missing_vars:
        return
        
    is_empty_file = not path.exists() or path.stat().st_size == 0
    
    with open(path, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if is_empty_file:
            writer.writerow(['component', 'key', 'value'])
            logging.info(f"Neue lokale Variablen-Datei '{path}' erstellt oder Header zu leerer Datei hinzugefügt.")
        
        for component, keys in missing_vars.items():
            for key in keys:
                writer.writerow([component, key, f"Beispielwert für {key}"])
                logging.info(f"Fehlender lokaler Schlüssel '{key}' für '{component}' wurde zu '{path}' hinzugefügt.")

def get_value_from_globals(path_str, global_vars):
    """Holt einen verschachtelten Wert aus dem global_vars Dictionary."""
    keys = path_str.split('.')
    d = global_vars
    for key in keys:
        if isinstance(d, dict) and key in d:
            d = d[key]
        else:
            return None
    return d

def get_existing_global_keys(path):
    """Liest nur die Schlüssel aus der bestehenden global_variables.csv."""
    if not path.exists():
        return set()
    
    keys = set()
    with open(path, 'r', encoding='utf-8') as f:
        try:
            reader = csv.reader(f)
            next(reader, None)
            for row in reader:
                if row and len(row) > 0:
                    keys.add(row[0].strip())
        except (StopIteration, IndexError):
            return set()
    return keys

def extract_list_placeholders(html_content, list_marker):
    """Extrahiert Platzhalter innerhalb eines BEGIN_LIST_ITEM-Blocks."""
    pattern = re.compile(rf'<!-- BEGIN_LIST_ITEM:{list_marker} -->(.*?)<!-- END_LIST_ITEM:{list_marker} -->', re.DOTALL)
    match = pattern.search(html_content)
    if match:
        block_content = match.group(1)
        return set(p.strip() for p in placeholder_pattern.findall(block_content))
    return set()

def validate_coverage(all_placeholders, section_content, found_global_keys, component, local_vars):
    """Validiert, ob alle Platzhalter abgedeckt sind (lokal oder global)."""
    covered_local = set(item['name'] for item in section_content if 'name' in item)
    covered_global = set(found_global_keys)
    allowed_local = set(local_vars.get(component, {}).keys())
    covered = covered_local.union(covered_global)
    uncovered = all_placeholders - covered - allowed_local
    if uncovered:
        logging.warning(f"Unabgedeckte Platzhalter in '{component}': {uncovered}")
        return False
    return True

# ==============================================================================
# 3. KERNLOGIK: CONTENT-GENERATOR
# ==============================================================================

def generate_content_template():
    logging.info("Starte Content-Generierungsprozess...")

    # --- Schritt 1: Eingabedateien laden ---
    try:
        with open(CSV_LAYOUT_PATH, 'r', encoding='utf-8') as f:
            layout = list(csv.DictReader(f))
        logging.info(f"Layout-CSV '{CSV_LAYOUT_PATH}' erfolgreich geladen.")
    except FileNotFoundError:
        logging.error(f"FEHLER: Layout-CSV nicht gefunden unter: '{CSV_LAYOUT_PATH}'. Prozess wird abgebrochen.")
        print(f"FEHLER: Layout-CSV nicht gefunden unter: '{CSV_LAYOUT_PATH}'.")
        return

    global_vars = load_global_variables(GLOBAL_VARS_PATH)
    existing_global_keys = get_existing_global_keys(GLOBAL_VARS_PATH)
    found_global_keys = []

    # --- Schritt 2: Lokale Variablen laden ---
    local_vars = load_local_variables(LOCAL_VARS_PATH)
    missing_local_vars = {}

    # --- Schritt 3: JSON-Grundstruktur aufbauen ---
    content = {
        "metadata": {
            "generated_at": datetime.now().isoformat(), "generator_version": "v3.1-final",
            "csv_source": str(CSV_LAYOUT_PATH)
        },
        "global_settings": global_vars, "page_content": {}
    }

    # --- Schritt 4: Jede Komponente aus dem Layout verarbeiten ---
    for row in layout:
        component = row.get('component')
        if not component or row.get('enabled', 'TRUE').upper() != 'TRUE':
            if component: logging.info(f"Komponente '{component}' ist deaktiviert und wird übersprungen.")
            continue
        
        logging.info(f"Verarbeite Komponente: '{component}'")
        
        html_filename = f"{component}.html"
        if not (TEMPLATES_DIR / html_filename).exists() and (TEMPLATES_DIR / f"{component}_section.html").exists():
            html_filename = f"{component}_section.html"
        
        html_path = TEMPLATES_DIR / html_filename
        if not html_path.exists():
            logging.warning(f"Kein HTML-Template für '{component}' unter '{html_path}' gefunden. Komponente wird übersprungen.")
            continue

        html_content = html_path.read_text(encoding='utf-8')
        all_placeholders = set(p.strip() for p in placeholder_pattern.findall(html_content))
        
        section_content = []
        if 'styling_default' in row and row['styling_default']:
            section_content.append({
                "id": f"EB-{component.capitalize()}-styling",
                "name": "styling_default",
                "value": row['styling_default']
            })
        
        processed_local_keys = set()
        list_placeholders = {}

        # Zuerst alle erwarteten lokalen Platzhalter aus local_vars verarbeiten
        allowed_keys = set(local_vars.get(component, {}).keys())
        missing_local_vars[component] = set()
        for local_key in allowed_keys:
            if local_key.endswith('_list'): continue
            if local_key in processed_local_keys: continue

            value = local_vars[component].get(local_key, f"Beispielwert für {local_key}")
            if "image_url" in local_key: value = f"assets/images/{component}_image.png"
            elif "map_url" in local_key: value = f"assets/images/{component}_map.png"

            for sub_placeholder in placeholder_pattern.findall(value):
                if '.' in sub_placeholder:
                    global_val = get_value_from_globals(sub_placeholder, global_vars)
                    if global_val:
                        value = value.replace(f"{{{{{sub_placeholder}}}}}", global_val)

            section_content.append({
                "id": f"EB-{component.capitalize()}-{local_key}",
                "name": local_key,
                "value": value
            })
            processed_local_keys.add(local_key)

        # Dann Listen-Marker finden und extrahieren
        list_marker_pattern = re.compile(r'BEGIN_LIST_ITEM:(\w+\.\w+)')
        for marker in list_marker_pattern.findall(html_content):
            sub_placeholders = extract_list_placeholders(html_content, marker)
            if sub_placeholders:
                list_placeholders[marker] = sub_placeholders
                example_item = {sub: local_vars.get(component, {}).get(sub, f"Beispielwert für {sub}") for sub in sub_placeholders}
                section_content.append({
                    "id": f"EB-{component.capitalize()}-{marker}",
                    "name": marker.split('.')[-1],
                    "type": "list",
                    "value": [example_item]
                })
                processed_local_keys.update(sub_placeholders)

        # Zusätzliche Platzhalter prüfen und ggf. als neu markieren
        for placeholder in all_placeholders:
            if placeholder.startswith(('BEGIN_', 'END_')) or placeholder in processed_local_keys: continue
            if '.' in placeholder:
                found_global_keys.append(placeholder)
                continue
            if placeholder not in allowed_keys:
                missing_local_vars[component].add(placeholder)

        content["page_content"][component] = section_content

        if not validate_coverage(all_placeholders, section_content, found_global_keys, component, local_vars):
            logging.error(f"Validierung fehlgeschlagen für Komponente '{component}'. Überprüfen Sie die Platzhalter.")

    # --- Schritt 5: Globale und lokale Variablen aktualisieren und JSON speichern ---
    write_missing_global_variables(GLOBAL_VARS_PATH, found_global_keys, existing_global_keys)
    write_missing_local_variables(LOCAL_VARS_PATH, missing_local_vars)

    output_path = OUTPUT_DIR / f'{OUTPUT_FILENAME_PREFIX}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(content, f, indent=2, ensure_ascii=False)
    
    logging.info(f"Prozess abgeschlossen. JSON-Datei wurde hier gespeichert: '{output_path}'")
    print(f"Prozess erfolgreich abgeschlossen. Output in '{output_path}'")

# ==============================================================================
# 4. SKRIPT AUSFÜHREN
# ==============================================================================
if __name__ == "__main__":
    generate_content_template()