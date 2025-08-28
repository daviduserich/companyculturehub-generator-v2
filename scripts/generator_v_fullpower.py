#!/usr/bin/env python3
"""
CompanyCultureHub Site Generator v4.2 (Final - mit intelligentem Aufräumen & Umbenennen)
"""
import json, csv, re, argparse, shutil
from pathlib import Path
from datetime import datetime

# Import der Injektor-Funktion
import sys
sys.path.append(str(Path(__file__).parent))
from injector import inject_data



def flatten_dict(d, parent_key='', sep='.'):
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)

def main():
    base_dir = Path(__file__).resolve().parent.parent
    content_dir = base_dir / "content"
    templates_dir = base_dir / "templates"
    output_dir = base_dir / "docs"
    output_dir.mkdir(exist_ok=True)

    print("--- STARTING GENERATOR V4.2 (Final) ---")

    # === PHASE 1: AUFRÄUMEN (genau nach deinem Konzept) ===
    print("\n[PHASE 1: AUFRÄUMEN]")
    
    # 1. Archiviere alte HTML-Dateien
    docs_archive_dir = output_dir / "docs_archives"
    docs_archive_dir.mkdir(exist_ok=True)
    html_files_to_archive = list(output_dir.glob('*.html'))
    if html_files_to_archive:
        print(f"   - 🧹 Archiviere {len(html_files_to_archive)} alte HTML-Dateien...")
        for f in html_files_to_archive:
            shutil.move(str(f), str(docs_archive_dir))
    else:
        print("   - ℹ️ Keine alten HTML-Dateien zum Archivieren gefunden.")

    # 2. Archiviere als "processed_" markierte Projekt-Ordner
    content_archive_dir = content_dir / "proceed_contents_archives"
    content_archive_dir.mkdir(exist_ok=True)
    processed_folders = list(content_dir.glob('processed_*'))
    if processed_folders:
        print(f"   - 🧹 Archiviere {len(processed_folders)} bereits verarbeitete Projekt-Ordner...")
        for folder in processed_folders:
            shutil.move(str(folder), str(content_archive_dir))
    else:
        print("   - ℹ️ Keine verarbeiteten Projekt-Ordner zum Archivieren gefunden.")
    
    print("   - ✅ Aufräumen abgeschlossen.")
    # === ENDE PHASE 1 ===

    print("\n[PHASE 2: SEITEN-GENERIERUNG]")
    # Finde alle Projekte, die NICHT das Archiv selbst sind
    projects_to_process = [d for d in content_dir.iterdir() if d.is_dir() and d.name != content_archive_dir.name]
    
    if not projects_to_process:
        print("   - ℹ️ Keine neuen Projekte zur Verarbeitung gefunden. Prozess beendet.")
        return


    for project_dir in projects_to_process:
        project_name = project_dir.name
        print(f"🚀 Verarbeite Projekt: {project_name}")
        
        # NEU: Injektor-Aufruf VOR der HTML-Generierung
        print(f"   - 💉 Starte Farb-Injektion...")
        try:
            inject_data(project_name, base_dir)
            print(f"   - ✅ Farb-Injektion abgeschlossen")
        except Exception as e:
            print(f"   - ⚠️ Farb-Injektion fehlgeschlagen: {e}")
        
        # Bestehender Code (bleibt unverändert)
        injected_content_file = project_dir / "content_color_injected.json"    
        original_content_file = project_dir / "content.json"
        if injected_content_file.exists(): content_file = injected_content_file
        elif original_content_file.exists(): content_file = original_content_file
        else: continue
        layout_file = project_dir / "layout.csv"
        if not layout_file.exists(): continue
        content_data = json.load(content_file.open(encoding='utf-8'))
        presets = {"classic": {"bg": "solid", "card": "shadow", "btn": "rounded", "anim": "subtle"}, "stylish": {"bg": "gradient", "card": "glass", "btn": "pill", "anim": "playful"}}
        style_choice = content_data.get("global_settings", {}).get("design", {}).get("presentation_style", "classic")
        chosen_preset = presets.get(style_choice, presets["classic"])
        theme_classes_str = f"bg-{chosen_preset['bg']} card-{chosen_preset['card']} btn-{chosen_preset['btn']} anim-{chosen_preset['anim']}"
        final_mapping = {}
        global_settings = content_data.get("global_settings", {})
        final_mapping.update(flatten_dict(global_settings))
        page_content = content_data.get("page_content", {})
        page_content_map = {}
        if isinstance(page_content, dict):
            for section_name, elements in page_content.items():
                if isinstance(elements, list):
                    for elem in elements:
                        if isinstance(elem, dict) and 'name' in elem and 'value' in elem and elem.get('type') != 'list':
                            key = f"{section_name}.{elem['name']}"
                            page_content_map[key] = elem.get('value', '')
        final_mapping.update(page_content_map)
        final_mapping['theme_classes'] = theme_classes_str
        for _ in range(5):
            is_dirty = False
            for key, value in final_mapping.items():
                if isinstance(value, str):
                    original_value = value
                    for map_key, map_value in final_mapping.items():
                        placeholder = f"{{{{{map_key}}}}}"
                        if placeholder in value: value = value.replace(placeholder, str(map_value))
                    if original_value != value:
                        final_mapping[key] = value
                        is_dirty = True
            if not is_dirty: break
        final_html = ""
        layout_plan = list(csv.DictReader(layout_file.open(encoding='utf-8')))
        enabled_components = [row for row in layout_plan if row.get('enabled', 'false').lower() == 'true']
        for item in sorted(enabled_components, key=lambda x: int(x.get('order', 0))):
            component_name = item['component']
            component_path = templates_dir / "components" / f"{component_name}.html"
            if not component_path.exists(): continue
            component_html = component_path.read_text(encoding='utf-8')
            for key, value in final_mapping.items(): component_html = component_html.replace(f"{{{{{key}}}}}", str(value))
            data_source_key = item['data_source']
            section_data = page_content.get(data_source_key, [])
            if isinstance(section_data, list):
                for element in section_data:
                    if isinstance(element, dict) and element.get('type') == 'list':
                        list_id = f"{data_source_key}.{element['name']}"
                        pattern = re.compile(rf'<!-- BEGIN_LIST_ITEM:{re.escape(list_id)} -->(.*?)<!-- END_LIST_ITEM:{re.escape(list_id)} -->', re.DOTALL)
                        match = pattern.search(component_html)
                        if not match: continue
                        item_template = match.group(1)
                        generated_items_html = ""
                        for list_item in element.get('value', []):
                            item_html = item_template
                            item_mapping = {el['name']: el.get('value', '') for el in list_item.get('elements', [])}
                            for key, value in item_mapping.items(): item_html = item_html.replace(f"{{{{{key}}}}}", str(value))
                            generated_items_html += item_html
                        component_html = pattern.sub(generated_items_html, component_html)
            final_html += component_html + "\n"
        
        output_path = output_dir / f"{project_name}.html"
        output_path.write_text(final_html, encoding='utf-8')
        print(f"   - ✅ Website erfolgreich generiert: {output_path}")
        
        # === PHASE 3: PROJEKT MARKIEREN (genau nach deinem Konzept) ===
        new_name = f"processed_{project_name}"
        processed_path = project_dir.parent / new_name
        project_dir.rename(processed_path)
        print(f"   - ✅ Projekt-Ordner markiert als: '{new_name}'")
        print("-" * 40)

if __name__ == "__main__":
    main()
