#!/usr/bin/env python3
"""
CompanyCultureHub Site Generator v2.8 (Final Replacement Engine Fix)
"""

import json
import csv
import re
from pathlib import Path
from datetime import datetime
import argparse

class CompanyCultureHubGenerator:
    def __init__(self, base_dir):
        self.base_dir = Path(base_dir)
        self.templates_dir = self.base_dir / "templates"
        self.output_dir = self.base_dir / "docs"
        self.content_dir = self.base_dir / "content"
        self.output_dir.mkdir(exist_ok=True)

    def load_json_content(self, json_file):
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"❌ Fehler beim Laden der JSON-Datei: {json_file.name} - {e}")
            return None

    def load_layout_plan(self, layout_file):
        try:
            with open(layout_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                plan = [row for row in reader if row.get('enabled', 'false').lower() == 'true']
                return sorted(plan, key=lambda x: int(x.get('order', 0)))
        except Exception as e:
            print(f"❌ Fehler beim Laden der Layout-Datei: {layout_file.name} - {e}")
            return []

    def load_component_template(self, component_name):
        template_path = self.templates_dir / "components" / f"{component_name}.html"
        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            return f"<!-- Komponente '{component_name}' nicht gefunden -->"
        except Exception as e:
            return ""

    def _flatten_dict(self, data, parent_key='', sep='.'):
        items = {}
        for k, v in data.items():
            new_key = parent_key + sep + k if parent_key else k
            if isinstance(v, dict):
                items.update(self._flatten_dict(v, new_key, sep=sep))
            else:
                items[new_key] = v
        return items

    def _replace_placeholders(self, text, mapping):
        if not isinstance(text, str):
            return text
        for key, value in mapping.items():
            text = text.replace(f"{{{{{key}}}}}", str(value))
        return text


    def _recursive_replace(self, obj, mapping):
        # Diese neue Funktion durchläuft die gesamte Datenstruktur (JSON)
        # und ersetzt alle Platzhalter, bevor wir überhaupt an HTML denken.
        if isinstance(obj, dict):
            return {k: self._recursive_replace(v, mapping) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self._recursive_replace(elem, mapping) for elem in obj]
        elif isinstance(obj, str):
            # Iterative Ersetzung für verschachtelte Variablen
            for _ in range(5): # Sicherheitslimit
                original_text = obj
                for key, value in mapping.items():
                    obj = obj.replace(f"{{{{{key}}}}}", str(value))
                if obj == original_text:
                    break
            return obj
        else:
            return obj

    def generate_site(self, project_name):
        print(f"🚀 CompanyCultureHub Generator v2.8 gestartet für Projekt: {project_name}")
        
        project_dir = self.content_dir / project_name
        content_file = project_dir / "content.json"
        layout_file = project_dir / "layout.csv"

        if not all([project_dir.exists(), content_file.exists(), layout_file.exists()]):
            print(f"❌ Kritischer Fehler: Konfigurationsdateien nicht gefunden in {project_dir}")
            return False

        content_data = self.load_json_content(content_file)
        if not content_data: return False
        
        layout_plan = self.load_layout_plan(layout_file)
        if not layout_plan: return False
        print(f"✅ Bauplan '{layout_file.name}' geladen mit {len(layout_plan)} aktiven Komponenten.")

        # --- FINALE, KORREKTE VERARBEITUNGS-PIPELINE ---

        # 1. Erstelle eine flache Map aller globalen Variablen
        global_mapping = self._flatten_dict(content_data.get("global_settings", {}))
        global_mapping["current_year"] = str(datetime.now().year)

        # 2. Ersetze mit der neuen, rekursiven Funktion ALLE Platzhalter in der GESAMTEN content_data
        processed_content_data = self._recursive_replace(content_data, global_mapping)

        # 3. Erstelle eine finale, flache Map für die HTML-Ersetzung
        final_mapping = self._flatten_dict(processed_content_data)

        # 4. Baue die Seite zusammen
        final_html_parts = []
        for item in layout_plan:
            component_name = item['component']
            component_html = self.load_component_template(component_name)
            
            # Ersetze alle Platzhalter in der Komponente mit der finalen Map
            component_html = self._replace_placeholders(component_html, final_mapping)
            
            # Verarbeite die Listen
            data_source_key = item['data_source']
            section_data = processed_content_data.get("page_content", {}).get(data_source_key, [])
            
            for element in section_data:
                if isinstance(element, dict) and element.get('type') == 'list':
                    list_id = element['id']
                    pattern = re.compile(rf'<!-- BEGIN_LIST_ITEM:{re.escape(list_id)} -->(.*?)<!-- END_LIST_ITEM:{re.escape(list_id)} -->', re.DOTALL)
                    match = pattern.search(component_html)
                    if not match: continue
                    
                    item_template = match.group(1)
                    generated_items_html = ""
                    for list_item in element.get('value', []):
                        item_html = item_template
                        item_mapping = {el['id']: el.get('value', '') for el in list_item.get('elements', [])}
                        item_html = self._replace_placeholders(item_html, item_mapping)
                        generated_items_html += item_html
                    
                    component_html = pattern.sub(generated_items_html, component_html)

            final_html_parts.append(component_html)

        final_html = "\n".join(final_html_parts)
        
        output_path = self.output_dir / f"{project_name}.html"
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(final_html)
            print(f"✅ Website erfolgreich generiert: {output_path}")
            return True
        except Exception as e:
            print(f"❌ Fehler beim Speichern: {e}")
            return False

    def generate_all_sites(self):
        project_folders = [d for d in self.content_dir.iterdir() if d.is_dir()]
        for project_dir in project_folders:
            self.generate_site(project_dir.name)

def main():
    script_path = Path(__file__).resolve()
    project_base_dir = script_path.parent.parent
    parser = argparse.ArgumentParser(description='CompanyCultureHub Site Generator v2.8')
    parser.add_argument('--all', action='store_true', help='Alle Projekte im content-Ordner verarbeiten')
    parser.add_argument('--project', type=str, help='Nur ein spezifisches Projekt verarbeiten (Ordnername)')
    args = parser.parse_args()
    generator = CompanyCultureHubGenerator(base_dir=project_base_dir)
    if args.project:
        generator.generate_site(args.project)
    else:
        generator.generate_all_sites()

if __name__ == "__main__":
    main()
