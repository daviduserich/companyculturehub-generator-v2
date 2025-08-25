#!/usr/bin/env python3
"""
CompanyCultureHub Site Generator v2.3 (Final Fix)
- Robusterer Ausführungs-Kontext
- Korrekte Verarbeitungspipeline
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
            print(f"⚠️  Komponenten-Template nicht gefunden: {template_path}")
            return f"<!-- Komponente '{component_name}' nicht gefunden -->"
        except Exception as e:
            print(f"❌ Fehler beim Laden des Komponenten-Templates: {template_path.name} - {e}")
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

    def _process_lists_in_template(self, html_content, list_data_array, full_mapping):
        processed_html = html_content
        for list_data in list_data_array:
            if not isinstance(list_data, dict) or list_data.get('type') != 'list':
                continue

            list_id = list_data['id']
            pattern = re.compile(
                rf'<!-- BEGIN_LIST_ITEM:{re.escape(list_id)} -->(.*?)<!-- END_LIST_ITEM:{re.escape(list_id)} -->',
                re.DOTALL
            )
            match = pattern.search(processed_html)
            if not match:
                continue
            
            item_template = match.group(1)
            generated_html = ""

            for item in list_data.get('value', []):
                item_html = item_template
                item_mapping = {element['id']: element.get('value', '') for element in item.get('elements', [])}
                item_html = self._replace_placeholders(item_html, item_mapping)
                generated_html += item_html
            
            processed_html = pattern.sub(generated_html, processed_html)
        return processed_html

    def generate_site(self, project_name):
        print(f"🚀 CompanyCultureHub Generator v2.3 gestartet für Projekt: {project_name}")
        
        project_dir = self.content_dir / project_name
        content_file = project_dir / "content.json"
        layout_file = project_dir / "layout.csv"

        if not content_file.exists() or not layout_file.exists():
            print(f"❌ Kritischer Fehler: content.json oder layout.csv nicht in {project_dir} gefunden.")
            return False

        content_data = self.load_json_content(content_file)
        if not content_data: return False
        
        layout_plan = self.load_layout_plan(layout_file)
        if not layout_plan: return False

        # 1. Erstelle ein komplettes Mapping aller verfügbaren Daten
        global_settings_flat = self._flatten_dict(content_data.get("global_settings", {}))
        page_content_data = content_data.get("page_content", {})
        
        # 2. Ersetze globale Variablen in den page_content-Werten
        page_content_processed = {
            section: [
                {**elem, 'value': self._replace_placeholders(elem.get('value', ''), global_settings_flat)}
                if elem.get('type') != 'list' else elem
                for elem in content
            ]
            for section, content in page_content_data.items()
        }
        
        # 3. Erstelle das finale Mapping
        final_mapping = {**global_settings_flat}
        for section_content in page_content_processed.values():
            for elem in section_content:
                if elem.get('type') != 'list':
                    final_mapping[elem['id']] = elem.get('value')
        final_mapping["current_year"] = str(datetime.now().year)

        # 4. Bereite die Listendaten vor
        list_data = [elem for section in page_content_processed.values() for elem in section if elem.get('type') == 'list']

        # 5. Baue die Seite zusammen
        final_html_parts = []
        for item in layout_plan:
            component_name = item['component']
            component_html = self.load_component_template(component_name)
            
            component_html = self._replace_placeholders(component_html, final_mapping)
            component_html = self._process_lists_in_template(component_html, list_data, final_mapping)

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

# --- KORRIGIERTER AUFRUF ---
def main():
    # Finde das Hauptverzeichnis des Projekts, egal von wo das Skript aufgerufen wird
    script_path = Path(__file__).resolve()
    project_base_dir = script_path.parent.parent

    parser = argparse.ArgumentParser(description='CompanyCultureHub Site Generator v2.3')
    parser.add_argument('--all', action='store_true', help='Alle Projekte im content-Ordner verarbeiten')
    parser.add_argument('--project', type=str, help='Nur ein spezifisches Projekt verarbeiten (Ordnername)')
    
    args = parser.parse_args()
    
    # Erstelle eine Instanz des Generators mit dem korrekten Basispfad
    generator = CompanyCultureHubGenerator(base_dir=project_base_dir)
    
    if args.project:
        generator.generate_site(args.project)
    else:
        generator.generate_all_sites()

if __name__ == "__main__":
    main()
