#!/usr/bin/env python3
"""
CompanyCultureHub Site Generator v2.4 (Ultimate Debugging Edition)
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
        print("✅ Generator initialisiert.")
        print(f"   - Base Dir: {self.base_dir}")
        print(f"   - Content Dir: {self.content_dir}")

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

    def _process_lists_in_template(self, html_content, list_data_array):
        processed_html = html_content
        for list_data in list_data_array:
            if not isinstance(list_data, dict) or list_data.get('type') != 'list':
                continue

            list_id = list_data['id']
            print(f"   🔍 Suche nach Liste mit ID: {list_id}")
            pattern = re.compile(
                rf'<!-- BEGIN_LIST_ITEM:{re.escape(list_id)} -->(.*?)<!-- END_LIST_ITEM:{re.escape(list_id)} -->',
                re.DOTALL
            )
            match = pattern.search(processed_html)
            if not match:
                print(f"      - ⚠️ Liste '{list_id}' im Template nicht gefunden.")
                continue
            
            item_template = match.group(1)
            generated_html = ""
            print(f"      - ✅ Liste '{list_id}' gefunden. Verarbeite {len(list_data.get('value', []))} Elemente.")

            for i, item in enumerate(list_data.get('value', [])):
                item_html = item_template
                item_mapping = {element['id']: element.get('value', '') for element in item.get('elements', [])}
                item_html = self._replace_placeholders(item_html, item_mapping)
                generated_html += item_html
                print(f"         - Element {i+1} verarbeitet.")
            
            processed_html = pattern.sub(generated_html, processed_html)
        return processed_html

    def generate_site(self, project_name):
        print(f"\n🚀 Starte Generierung für Projekt: {project_name}")
        
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

        # --- DEBUGGING: Schritt 1 ---
        print("\n--- DEBUG: Schritt 1: Finale Daten-Map erstellen ---")
        global_settings = content_data.get("global_settings", {})
        page_content = content_data.get("page_content", {})
        
        # Ersetze globale Variablen in den page_content-Werten
        page_content_string = json.dumps(page_content)
        global_settings_flat = self._flatten_dict(global_settings)
        page_content_string = self._replace_placeholders(page_content_string, global_settings_flat)
        page_content_string = self._replace_placeholders(page_content_string, {"current_year": str(datetime.now().year)})
        page_content_processed = json.loads(page_content_string)

        # Erstelle das finale Mapping
        final_mapping = {**global_settings_flat}
        for section_content in page_content_processed.values():
            for elem in section_content:
                if elem.get('type') != 'list':
                    final_mapping[elem['id']] = elem.get('value')
        final_mapping["current_year"] = str(datetime.now().year)
        
        print("   - ✅ Finale Daten-Map erstellt. Beispiel-Eintrag 'identity.company_name':", final_mapping.get('identity.company_name'))
        print("   - ✅ Beispiel-Eintrag 'EB-Sec1-C1-E1':", final_mapping.get('EB-Sec1-C1-E1'))

        # Bereite die Listendaten vor
        list_data = [elem for section in page_content_processed.values() for elem in section if elem.get('type') == 'list']
        print(f"   - ✅ {len(list_data)} Listen zur Verarbeitung gefunden.")

        # --- DEBUGGING: Schritt 2 ---
        print("\n--- DEBUG: Schritt 2: Seite aus Komponenten zusammensetzen ---")
        final_html_parts = []
        for item in layout_plan:
            component_name = item['component']
            print(f"➡️  Verarbeite Komponente: '{component_name}'")
            component_html = self.load_component_template(component_name)
            
            # Ersetze zuerst die einfachen Platzhalter
            component_html = self._replace_placeholders(component_html, final_mapping)
            
            # Verarbeite dann die Listen
            component_html = self._process_lists_in_template(component_html, list_data)

            final_html_parts.append(component_html)

        final_html = "\n".join(final_html_parts)
        
        output_path = self.output_dir / f"{project_name}.html"
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(final_html)
            print(f"\n✅ Website erfolgreich generiert: {output_path}")
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

    parser = argparse.ArgumentParser(description='CompanyCultureHub Site Generator v2.4')
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
