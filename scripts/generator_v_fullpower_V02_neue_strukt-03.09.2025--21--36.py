
#!/usr/bin/env python3
"""
CompanyCultureHub HTML Generator v5.0
- Refactored for new, structured JSON format.
- Supports preview mode with placeholder assets.
- Ready for multi-style output.
"""
import json
import csv
import re
import shutil
from pathlib import Path
from datetime import datetime
import logging

# Annahme: injector.py existiert und hat eine `inject_data` Funktion.
# Wir versuchen, sie zu importieren, aber machen das Skript nicht davon abhängig,
# falls es für einen Testlauf nicht vorhanden ist.
try:
    from injector import inject_data
except ImportError:
    def inject_data(project_name, base_dir):
        print("   - ℹ️ 'injector.py' nicht gefunden. Überspringe Farb-Injektion.")
        return None

# ==============================================================================
# 1. KONFIGURATION & PFADE
# ==============================================================================
BASE_DIR = Path(__file__).resolve().parent.parent
CONTENT_DIR = BASE_DIR / "content"
TEMPLATES_DIR = BASE_DIR / "templates"
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
        return default
    try:
        with file_path.open(encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        logging.error(f"Fehler beim Parsen von JSON in {file_path}: {e}")
        return default

def find_newest_file(directory, pattern):
    """Findet die neueste Datei in einem Ordner, die einem Muster entspricht."""
    files = list(directory.glob(pattern))
    if not files:
        return None
    return max(files, key=lambda f: f.stat().st_mtime)

def replace_placeholders(html, data_dict):
    """Ersetzt alle {{key}} Platzhalter in einem HTML-String."""
    for key, value in data_dict.items():
        # Stelle sicher, dass der Wert ein String ist, um Fehler zu vermeiden
        html = html.replace(f"{{{{{key}}}}}", str(value))
    return html

# ==============================================================================
# 3. KERNLOGIK DES HTML-GENERATORS
# ==============================================================================

def generate_site_for_style(project_dir, style_name, content_data, layout_plan, placeholder_assets):
    """Generiert eine einzelne HTML-Datei für einen bestimmten Style."""
    project_name = project_dir.name
    print(f"   - 🎨 Generiere Seite für Style: '{style_name}'")

    # Lade die spezifische Style-Definition
    style_file = find_newest_file(project_dir, f"interpreted_styles_{style_name}*.json")
    style_data = load_json(style_file, {})
    
    # Baue das globale Mapping für Platzhalter
    global_mapping = {}
    global_mapping.update(style_data.get("design", {}).get("branding", {}))
    global_mapping.update(content_data.get("global_settings", {})) # Echte Daten überschreiben ggf. Defaults

    # Platzhalter für den Body-Tag
    theme_classes = style_data.get("theme_classes", "")
    global_mapping['theme_classes'] = theme_classes

    final_html = ""
    component_counters = {row['component']: 0 for row in layout_plan} # Zähler für jede Komponente

    for item in sorted(layout_plan, key=lambda x: int(x.get('order', 0))):
        component_name = item['component']
        
        # Hole die richtige Instanz der Komponente aus den content_data
        instance_index = component_counters[component_name]
        component_instances = content_data.get("page_content", {}).get(component_name, [])
        
        if instance_index >= len(component_instances):
            continue # Nicht genug Instanzen im Content-JSON, überspringe
            
        instance_data = component_instances[instance_index]
        component_counters[component_name] += 1 # Zähler für die nächste Instanz erhöhen

        # Lade das HTML-Template für die Komponente
        component_path = TEMPLATES_DIR / "components" / f"{component_name}.html"
        if not component_path.exists():
            logging.warning(f"Template für Komponente '{component_name}' nicht gefunden.")
            continue
        
        component_html = component_path.read_text(encoding='utf-8')

        # Ersetze lokale Platzhalter (z.B. headline, description)
        local_mapping = {k: v.get("value", "") for k, v in instance_data.items() if isinstance(v, dict)}
        component_html = replace_placeholders(component_html, local_mapping)

        # Ersetze Listen-Platzhalter
        for key, value in instance_data.items():
            if isinstance(value, list): # Annahme: Jedes Array ist eine Liste
                list_marker = f"{component_name}.{key}"
                pattern = re.compile(rf'<!-- BEGIN_LIST_ITEM:{re.escape(list_marker)} -->(.*?)<!-- END_LIST_ITEM:{re.escape(list_marker)} -->', re.DOTALL)
                match = pattern.search(component_html)
                if not match: continue
                
                item_template = match.group(1)
                generated_items_html = ""
                for list_item_data in value:
                    item_html = item_template
                    item_mapping = {k: v.get("value", "") for k, v in list_item_data.items()}
                    item_html = replace_placeholders(item_html, item_mapping)
                    generated_items_html += item_html
                component_html = pattern.sub(generated_items_html, component_html)

        # Ersetze globale Platzhalter (z.B. identity.company_name)
        # Dies geschieht am Ende, um sicherzustellen, dass alle lokalen Werte bereits gesetzt sind.
        # Wir flachen das globale Mapping für die einfache Ersetzung.
        flat_global_mapping = {}
        for section, data in global_mapping.items():
            if isinstance(data, dict):
                for key, value in data.items():
                    flat_global_mapping[f"{section}.{key}"] = value
        
        component_html = replace_placeholders(component_html, flat_global_mapping)
        
        # Fallback für Bilder (Vorschau-Modus)
        def image_fallback(match):
            # Wenn src leer ist (src=""), ersetze es durch einen Placeholder
            src_value = match.group(1)
            if not src_value:
                # Nutze den Komponentennamen, um den richtigen Bild-Pool zu finden
                asset_key = component_name
                if asset_key not in placeholder_assets:
                    asset_key = "culture_and_diversity" # Standard-Fallback
                
                urls = placeholder_assets.get(asset_key, {}).get("urls", [])
                if not urls: return 'src=""' # Kein Placeholder gefunden
                
                # Round-Robin-Prinzip
                placeholder_url = urls[instance_index % len(urls)]
                return f'src="{placeholder_url}"'
            return match.group(0) # Gib den Original-String zurück

        component_html = re.sub(r'src="([^"]*)"', image_fallback, component_html)

        final_html += component_html + "\n"

    # Speichere die fertige HTML-Datei
    output_path = OUTPUT_DIR / f"{project_name}_{style_name}.html"
    output_path.write_text(final_html, encoding='utf-8')
    print(f"   - ✅ Website erfolgreich generiert: {output_path}")


def main():
    """Hauptfunktion zur Steuerung des gesamten Generierungsprozesses."""
    print("--- STARTING HTML GENERATOR V5.0 ---")

    # === PHASE 1: AUFRÄUMEN ===
    print("\n[PHASE 1: AUFRÄUMEN]")
    docs_archive_dir = OUTPUT_DIR / "docs_archives"
    docs_archive_dir.mkdir(exist_ok=True)
    for f in OUTPUT_DIR.glob('*.html'):
        shutil.move(str(f), str(docs_archive_dir))
        logging.info(f"Archiviere alte HTML-Datei: {f.name}")
    print("   - ✅ Alte HTML-Dateien archiviert.")

    content_archive_dir = CONTENT_DIR / "processed_contents_archives"
    content_archive_dir.mkdir(exist_ok=True)
    for folder in CONTENT_DIR.glob('processed_*'):
        shutil.move(str(folder), str(content_archive_dir))
        logging.info(f"Archiviere verarbeitetes Projekt: {folder.name}")
    print("   - ✅ Verarbeitete Projekte archiviert.")

    # === PHASE 2: PROJEKTE VERARBEITEN ===
    print("\n[PHASE 2: SEITEN-GENERIERUNG]")
    projects_to_process = [d for d in CONTENT_DIR.iterdir() if d.is_dir() and not d.name.startswith('processed_') and d.name != "processed_contents_archives"]
    
    if not projects_to_process:
        print("   - ℹ️ Keine neuen Projekte zur Verarbeitung gefunden. Prozess beendet.")
        return

    # Lade die zentrale Placeholder-Asset-Datei
    placeholder_assets = load_json(TEMPLATES_DIR / "_placeholder_assets.json", {})

    for project_dir in projects_to_process:
        project_name = project_dir.name
        print(f"🚀 Verarbeite Projekt: {project_name}")

        # Finde die neueste Content-Datei (entweder die Anleitung oder eine befüllte)
        content_file = find_newest_file(project_dir, "project_template_*.json")
        if not content_file:
            logging.warning(f"Keine 'project_template_*.json' Datei in {project_name} gefunden. Überspringe.")
            continue
        
        content_data = load_json(content_file, {})
        
        # Lade den Layout-Plan
        layout_file = project_dir / "layout_extended_v2.csv"
        if not layout_file.exists():
            logging.warning(f"Keine 'layout_extended_v2.csv' in {project_name} gefunden. Überspringe.")
            continue
        layout_plan = [row for row in csv.DictReader(layout_file.open(encoding='utf-8')) if row.get('enabled', 'FALSE').upper() == 'TRUE']

        # Führe die Generierung für jeden gefundenen Style aus
        styles = ["classic", "classic_accents", "stylish", "hyper_stylish"]
        for style in styles:
            # Hier könnte der Injektor-Aufruf pro Style erfolgen, falls nötig
            # Fürs Erste nehmen wir an, die Style-Dateien existieren bereits
            generate_site_for_style(project_dir, style, content_data, layout_plan, placeholder_assets)

        # === PHASE 3: PROJEKT MARKIEREN ===
        new_name = f"processed_{project_name}_{datetime.now().strftime('%Y%m%d')}"
        processed_path = project_dir.parent / new_name
        project_dir.rename(processed_path)
        print(f"   - ✅ Projekt-Ordner markiert als: '{new_name}'")
        print("-" * 50)

if __name__ == "__main__":
    main()
