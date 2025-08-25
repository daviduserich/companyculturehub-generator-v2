#!/usr/bin/env python3
"""
CompanyCultureHub Site Generator v2.2 (Bugfix Release)
- Korrigierte Listenverarbeitung
- Korrigierte Variablenersetzung
"""

import json
import csv
import re
from pathlib import Path
from datetime import datetime
import argparse

class CompanyCultureHubGenerator:
    def __init__(self, templates_dir="templates", output_dir="docs", content_dir="content"):
        self.base_dir = Path(__file__).resolve().parent.parent
        self.templates_dir = self.base_dir / templates_dir
        self.output_dir = self.base_dir / output_dir
        self.content_dir = self.base_dir / content_dir
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
        # KORREKTUR: Ersetzt alle Platzhalter in einem Text mit den Werten aus einem Mapping.
        for key, value in mapping.items():
            text = text.replace(f"{{{{{key}}}}}", str(value))
        return text

    def _process_lists_in_template(self, html_content, list_data_array, full_mapping):
        # KORREKTUR: Diese Funktion wurde komplett überarbeitet, um den Logikfehler zu beheben.
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
                item_html = item_template # Wichtig: Bei jeder Iteration die saubere Vorlage nehmen
                item_mapping = {element['id']: element.get('value', '') for element in item.get('elements', [])}
                
                # Ersetze Platzhalter innerhalb des Listenelements
                item_html = self._replace_placeholders(item_html, item_mapping)
                generated_html += item_html
            
            processed_html = pattern.sub(generated_html, processed_html)
        return processed_html

    def generate_site(self, project_name):
        print(f"🚀 CompanyCultureHub Generator v2.2 gestartet für Projekt: {project_name}")
        
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

        # --- KORREKTUR: Vereinfachte und korrekte Verarbeitungsreihenfolge ---
        
        # 1. Erstelle ein komplettes Mapping aller verfügbaren Daten
        global_settings_flat = self._flatten_dict(content_data.get("global_settings", {}))
        page_content_flat = {elem['id']: elem.get('value') for section in content_data.get("page_content", {}).values() for elem in section if elem.get('type') != 'list'}
        
        full_data_mapping = {**global_settings_flat, **page_content_flat}
        full_data_mapping["current_year"] = str(datetime.now().year)

        # 2. Ersetze alle Variablen in den Werten selbst (z.B. {{identity.company_name}} in einem Text)
        final_mapping = {k: self._replace_placeholders(str(v), full_data_mapping) for k, v in full_data_mapping.items()}

        # 3. Bereite die Listendaten separat vor
        list_data = {elem['id']: elem for section in content_data.get("page_content", {}).values() for elem in section if elem.get('type') == 'list'}

        # 4. Baue die Seite zusammen
        final_html_parts = []
        for item in layout_plan:
            component_name = item['component']
            component_html = self.load_component_template(component_name)
            
            # Ersetze zuerst die einfachen Platzhalter in der Komponente
            component_html = self._replace_placeholders(component_html, final_mapping)
            
            # Verarbeite dann die Listen, falls welche in dieser Komponente sind
            component_html = self._process_lists_in_template(component_html, list(list_data.values()), final_mapping)

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
    parser = argparse.ArgumentParser(description='CompanyCultureHub Site Generator v2.2')
    parser.add_argument('--all', action='store_true', help='Alle Projekte im content-Ordner verarbeiten')
    parser.add_argument('--project', type=str, help='Nur ein spezifisches Projekt verarbeiten (Ordnername)')
    
    args = parser.parse_args()
    
    generator = CompanyCultureHubGenerator()
    
    if args.project:
        generator.generate_site(args.project)
    else:
        generator.generate_all_sites()

if __name__ == "__main__":
    main()

