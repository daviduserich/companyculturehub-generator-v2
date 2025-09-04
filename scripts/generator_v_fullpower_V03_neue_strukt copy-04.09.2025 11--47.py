#!/usr/bin/env python3
"""
CompanyCultureHub HTML Generator v5.1 (Final)
- Reads the new, structured Stufe02 JSON format.
- Fully supports preview mode with placeholder texts and images.
- Generates all four styling variants from the project folder.
"""
import json
import csv
import re
import shutil
from pathlib import Path
from datetime import datetime
import logging

# ==============================================================================
# 1. KONFIGURATION & PFADE
# ==============================================================================
BASE_DIR = Path(__file__).resolve().parent.parent
CONTENT_DIR = BASE_DIR / "content"
TEMPLATES_DIR = BASE_DIR / "templates"
COMPONENTS_DIR = TEMPLATES_DIR / "components"
OUTPUT_DIR = BASE_DIR / "docs"
OUTPUT_DIR.mkdir(exist_ok=True)

# Logging einrichten
LOG_FILE = OUTPUT_DIR / "html_generator.log"
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filemode='w')

# ==============================================================================
# 2. HELFERFUNKTIONEN
# ==============================================================================

def load_json(file_path, default=None):
    """Lädt eine JSON-Datei sicher."""
    if not file_path.exists():
        logging.warning(f"JSON-Datei nicht gefunden: {file_path}")
        return default if default is not None else {}
    try:
        with file_path.open(encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        logging.error(f"Fehler beim Parsen von JSON in {file_path}: {e}")
        return default if default is not None else {}

def find_newest_file(directory, pattern):
    """Findet die neueste Datei in einem Ordner, die einem Muster entspricht."""
    try:
        return max(directory.glob(pattern), key=lambda f: f.stat().st_mtime)
    except ValueError:
        return None

def flatten_dict(d, parent_key='', sep='.'):
    """Macht ein verschachteltes Dictionary flach."""
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)
def replace_placeholders(html, data_dict):
    """Ersetzt alle {{key}} Platzhalter in einem HTML-String."""
    for key, value in data_dict.items():
        # Stelle sicher, dass der Wert ein String ist, um Fehler zu vermeiden
        html = html.replace(f"{{{{{key}}}}}", str(value))
    return html

# ==============================================================================
# 3. KERNLOGIK DES HTML-GENERATORS
# ==============================================================================

def generate_site_for_style(project_dir, style_name, content_data, layout_plan, placeholder_assets, global_defaults):
    """Generiert eine einzelne HTML-Datei für einen bestimmten Style."""
    project_name = project_dir.name
    print(f"   - 🎨 Generiere Seite für Style: '{style_name}'")

    # === Schritt A: Baue das finale Mapping für Platzhalter ===
    final_mapping = {}
    
    # 1. Globale Defaults als Basis
    final_mapping.update(flatten_dict(global_defaults))

    # 2. Echte globale Daten aus dem Projekt überschreiben die Defaults
    if "global_settings" in content_data:
         final_mapping.update(flatten_dict(content_data["global_settings"]))

    # 3. Style-spezifische Klassen hinzufügen
    style_file = find_newest_file(project_dir, f"interpreted_styles_{style_name}*.json")
    style_data = load_json(style_file)
    final_mapping['theme_classes'] = style_data.get("theme_classes", "")
    
    # 4. Globale Farbdefinitionen für CSS-Variablen
    colors_file = find_newest_file(project_dir, "interpreted_colors*.json")
    colors_data = load_json(colors_file)
    if "colors" in colors_data:
        final_mapping.update(flatten_dict(colors_data["colors"], parent_key="design.branding"))

    final_html = ""
    component_counters = {row['component']: 0 for row in layout_plan}

    for item in sorted(layout_plan, key=lambda x: int(x.get('order', 0))):
        component_name = item['component']
        
        instance_index = component_counters[component_name]
        component_instances = content_data.get("page_content", {}).get(component_name, [])
        
        if instance_index >= len(component_instances):
            continue
            
        instance_data = component_instances[instance_index]
        component_counters[component_name] += 1

        component_path = COMPONENTS_DIR / f"{component_name}.html"
        if not component_path.exists():
            continue
        
        component_html = component_path.read_text(encoding='utf-8')

        # === Schritt B: Ersetze Platzhalter im HTML-Template ===

        # 1. Lokale Platzhalter (headline, description, etc.)
        # Wir erstellen ein Mapping nur für diese Instanz
        local_mapping = {}
        for key, data in instance_data.items():
            if isinstance(data, dict) and "value" in data:
                # Wenn der Wert leer ist, nutze den Beispielwert aus der Definition
                value = data["value"] if data["value"] else data.get("example_value", "")
                local_mapping[f"{component_name}.{key}"] = value
        
        component_html = replace_placeholders(component_html, local_mapping)

        # 2. Listen-Platzhalter (values_list, etc.)
        for key, list_data in instance_data.items():
            if isinstance(list_data, list):
                list_marker = f"{component_name}.{key}"
                pattern = re.compile(rf'<!-- BEGIN_LIST_ITEM:{re.escape(list_marker)} -->(.*?)<!-- END_LIST_ITEM:{re.escape(list_marker)} -->', re.DOTALL)
                match = pattern.search(component_html)
                if not match: continue
                
                item_template = match.group(1)
                generated_items_html = ""
                for list_item in list_data:
                    item_html = item_template
                    item_mapping = {k: (v["value"] if v["value"] else v.get("example_value", "")) for k, v in list_item.items()}
                    item_html = replace_placeholders(item_html, item_mapping)
                    generated_items_html += item_html
                component_html = pattern.sub(generated_items_html, component_html)

        # 3. Fallback für Bilder (Vorschau-Modus)
        def image_fallback(match):
            key = match.group(1) # Der Platzhalter-Name, z.B. "hero_section.image_url"
            # Wenn der Platzhalter noch existiert (also nicht durch einen echten Wert ersetzt wurde)
            if key in component_html:
                asset_key = key.split('.')[0] # z.B. "hero_section"
                urls = placeholder_assets.get(asset_key, {}).get("urls", [])
                if not urls: return "" # Kein Placeholder gefunden
                
                # Round-Robin-Prinzip
                placeholder_url = urls[instance_index % len(urls)]
                return placeholder_url
            return "" # Sollte nicht passieren, aber als Sicherheit

        component_html = re.sub(r'src="{{([^"]*image_url[^"]*)}}"', image_fallback, component_html)
        component_html = re.sub(r'src="{{([^"]*map_url[^"]*)}}"', image_fallback, component_html)

        # 4. Globale Platzhalter (letzter Schritt)
        component_html = replace_placeholders(component_html, final_mapping)

        final_html += component_html + "\n"

    # Speichere die fertige HTML-Datei
    output_path = OUTPUT_DIR / f"{project_name}_{style_name}.html"
    output_path.write_text(final_html, encoding='utf-8')
    print(f"   - ✅ Website erfolgreich generiert: {output_path}")


def main():
    """Hauptfunktion zur Steuerung des gesamten Generierungsprozesses."""
    print("--- STARTING HTML GENERATOR V5.1 (Final) ---")

    # === PHASE 1: AUFRÄUMEN ===
    print("\n[PHASE 1: AUFRÄUMEN]")
    # ... (Code für Phase 1 bleibt unverändert)
    docs_archive_dir = OUTPUT_DIR / "docs_archives"; docs_archive_dir.mkdir(exist_ok=True)
    for f in OUTPUT_DIR.glob('*.html'):
        destination_path = docs_archive_dir / f.name
        if destination_path.exists():
            destination_path = destination_path.with_name(f"{f.stem}_{datetime.now().strftime('%Y%m%d_%H%M%S')}{f.suffix}")
        shutil.move(str(f), str(destination_path))
    print("   - ✅ Alte HTML-Dateien archiviert.")
    content_archive_dir = CONTENT_DIR / "processed_contents_archives"; content_archive_dir.mkdir(exist_ok=True)
    for folder in CONTENT_DIR.iterdir():
        if folder.is_dir() and folder.name.startswith('processed_'):
            if folder.name == content_archive_dir.name: continue
            destination_path = content_archive_dir / folder.name
            if destination_path.exists():
                destination_path = destination_path.with_name(f"{folder.name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
            shutil.move(str(folder), str(destination_path))
    print("   - ✅ Verarbeitete Projekte archiviert.")

    # === PHASE 2: PROJEKTE VERARBEITEN ===
    print("\n[PHASE 2: SEITEN-GENERIERUNG]")
    projects_to_process = [d for d in CONTENT_DIR.iterdir() if d.is_dir() and not d.name.startswith('processed_') and d.name != "processed_contents_archives"]
    
    if not projects_to_process:
        print("   - ℹ️ Keine neuen Projekte zur Verarbeitung gefunden. Prozess beendet.")
        return

    # Lade zentrale Defaults und Placeholders
    placeholder_assets = load_json(COMPONENTS_DIR / "_placeholder_assets.json")
    global_defaults = load_json(COMPONENTS_DIR / "_defaults.json")

    for project_dir in projects_to_process:
        project_name = project_dir.name
        print(f"🚀 Verarbeite Projekt: {project_name}")

        layout_file = project_dir / "layout_extended_v2.csv"
        if not layout_file.exists(): continue
        layout_plan = [row for row in csv.DictReader(layout_file.open(encoding='utf-8')) if row.get('enabled', 'FALSE').upper() == 'TRUE']

        # Verarbeite jede gefundene Stufe02-Datei
        for content_file in project_dir.glob("project_template_Stufe02_Styled_*.json"):
            content_data = load_json(content_file)


            style_name_match = re.search(r"_Styled_(.+?)_\d+", content_file.name)
            if not style_name_match:
                logging.warning(f"Konnte Style-Namen aus '{content_file.name}' nicht extrahieren. Überspringe.")
                continue
            style_name = style_name_match.group(1)











            generate_site_for_style(project_dir, style_name, content_data, layout_plan, placeholder_assets, global_defaults)

        # === PHASE 3: PROJEKT MARKIEREN ===
        new_name = f"processed_{project_name}_{datetime.now().strftime('%Y%m%d')}"
        project_dir.rename(project_dir.parent / new_name)
        print(f"   - ✅ Projekt-Ordner markiert als: '{new_name}'")
        print("-" * 50)

if __name__ == "__main__":
    # Wir fügen eine _defaults.json hinzu, falls sie nicht existiert, um Fehler zu vermeiden
    if not (COMPONENTS_DIR / "_defaults.json").exists():
        (COMPONENTS_DIR / "_defaults.json").write_text(json.dumps({
            "identity": {"company_name": "Ihre Firma AG"},
            "design": {"logo": {"url": ""}},
            "links": {"career_page_url": "#", "application_form_url": "#", "imprint_url": "#", "privacy_url": "#", "contact_url": "#"},
            "labels": {"career_button_text": "Offene Stellen", "application_button_text": "Initiativbewerbung", "imprint_text": "Impressum", "privacy_text": "Datenschutz", "contact_text": "Kontakt"},
            "project_config": {"canonical_url": "#"}
        }, indent=2))
    main()

