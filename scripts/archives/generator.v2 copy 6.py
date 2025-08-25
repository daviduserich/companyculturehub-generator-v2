#!/usr/bin/env python3
"""
CompanyCultureHub Site Generator v2.5 (Correct Logic)
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
            print(f"⚠️  Komponente '{component_name}' nicht gefunden.")
            return f"<!-- Komponente '{component_name}' nicht gefunden -->"
        except Exception as e:
            print(f"❌ Fehler beim Laden von '{component_name}': {e}")
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

    def _process_list_in_component(self, component_html, section_data):
        for element in section_data:
            if isinstance(element, dict) and element.get('type') == 'list':
                list_id = element['id']
                pattern = re.compile(
                    rf'<!-- BEGIN_LIST_ITEM:{re.escape(list_id)} -->(.*?)<!-- END_LIST_ITEM:{re.escape(list_id)} -->',
                    re.DOTALL
                )
                match = pattern.search(component_html)
                if not match:
                    continue
                
                item_template = match.group(1)
                generated_html = ""
                for item in element.get('value', []):
                    item_html = item_template
                    item_mapping = {el['id']: el.get('value', '') for el in item.get('elements', [])}
                    item_html = self._replace_placeholders(item_html, item_mapping)
                    generated_html += item_html
                
                component_html = pattern.sub(generated_html, component_html)
        return component_html

    def generate_site(self, project_name):
        print(f"🚀 CompanyCultureHub Generator v2.5 gestartet für Projekt: {project_name}")
        
        project_dir = self.content_dir / project_name
        content_file = project_dir / "content.json"
        layout_file = project_dir / "layout.csv"

        if not all([project_dir.exists(), content_file.exists(), layout_file.exists()]):
            print(f"❌ Kritischer Fehler: Projekt-Verzeichnis oder Konfigurationsdateien nicht gefunden in {project_dir}")
            return False

        content_data = self.load_json_content(content_file)
        if not content_data: return False
        
        layout_plan = self.load_layout_plan(layout_file)
        if not layout_plan: return False
        print(f"✅ Bauplan '{layout_file.name}' geladen mit {len(layout_plan)} aktiven Komponenten.")

        # 1. Globale Variablen vorbereiten
        global_settings = content_data.get("global_settings", {})
        global_settings_flat = self._flatten_dict(global_settings)
        global_settings_flat["current_year"] = str(datetime.now().year)

        # 2. Erstelle ein Mapping für alle *einfachen* (nicht-Listen) page_content Elemente
        page_content_data = content_data.get("page_content", {})
        simple_content_mapping = {}
        for section_content in page_content_data.values():
            for elem in section_content:
                if elem.get('type') != 'list':
                    value = self._replace_placeholders(str(elem.get('value', '')), global_settings_flat)
                    simple_content_mapping[elem['id']] = value
        
        # 3. Kombiniere globales und einfaches Content-Mapping
        final_mapping = {**global_settings_flat, **simple_content_mapping}

        # 4. Baue die Seite Komponente für Komponente zusammen
        final_html_parts = []
        for item in layout_plan:
            component_name = item['component']
            data_source_key = item['data_source']
            
            component_html = self.load_component_template(component_name)
            
            component_html = self._replace_placeholders(component_html, final_mapping)
            
            section_data = page_content_data.get(data_source_key, [])
            component_html = self._process_list_in_component(component_html, section_data)

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
        if not project_folders:
            print("⚠️  Keine Projekt-Ordner im 'content'-Verzeichnis gefunden.")
            return
        for project_dir in project_folders:
            self.generate_site(project_dir.name)

def main():
    script_path = Path(__file__).resolve()
    project_base_dir = script_path.parent.parent
    parser = argparse.ArgumentParser(description='CompanyCultureHub Site Generator v2.5')
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
