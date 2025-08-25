#!/usr/bin/env python3
"""
CompanyCultureHub Site Generator v2.7 (Radically Simplified & Corrected)
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




    def _replace_all_placeholders(self, text, mapping):
        # Diese Funktion ersetzt iterativ, bis keine Platzhalter mehr übrig sind.
        # Das löst das Problem der verschachtelten Variablen wie {{seo.title}} -> {{identity.company_name}}
        if not isinstance(text, str):
            return text
        
        # Füge dynamische Werte hinzu, die nicht in der JSON stehen
        extended_mapping = mapping.copy()
        extended_mapping["current_year"] = str(datetime.now().year)

        # Iteriere, um verschachtelte Ersetzungen aufzulösen
        for _ in range(5): # Maximal 5 Durchläufe, um Endlosschleifen zu vermeiden
            found_placeholder = False
            for key, value in extended_mapping.items():
                placeholder = f"{{{{{key}}}}}"
                if placeholder in text:
                    text = text.replace(placeholder, str(value))
                    found_placeholder = True
            if not found_placeholder:
                break # Keine Platzhalter mehr gefunden, Schleife beenden
        return text

    def generate_site(self, project_name):
        print(f"🚀 CompanyCultureHub Generator v2.7 gestartet für Projekt: {project_name}")
        
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

        # --- NEUE, VEREINFACHTE VERARBEITUNGS-PIPELINE ---

        # 1. Baue EINE EINZIGE, komplette Daten-Map für alles.
        final_mapping = {}
        # Zuerst die globalen Einstellungen (flach geklopft)
        global_settings = content_data.get("global_settings", {})
        final_mapping.update(self._flatten_dict(global_settings))
        
        # Dann die einfachen page_content Elemente
        page_content_data = content_data.get("page_content", {})
        for section_content in page_content_data.values():
            for elem in section_content:
                if elem.get('type') != 'list':
                    final_mapping[elem['id']] = elem.get('value', '')

        # 2. Füge alle Komponenten zu einem einzigen grossen HTML-String zusammen.
        full_html_template = ""
        for item in layout_plan:
            full_html_template += self.load_component_template(item['component']) + "\n"

        # 3. Ersetze ALLE Platzhalter (inkl. verschachtelter) im gesamten HTML.
        processed_html = self._replace_all_placeholders(full_html_template, final_mapping)

        # 4. Verarbeite die Listen im bereits teilweise ersetzten HTML.
        for section_name, section_content in page_content_data.items():
            for element in section_content:
                if isinstance(element, dict) and element.get('type') == 'list':
                    list_id = element['id']
                    pattern = re.compile(
                        rf'<!-- BEGIN_LIST_ITEM:{re.escape(list_id)} -->(.*?)<!-- END_LIST_ITEM:{re.escape(list_id)} -->',
                        re.DOTALL
                    )
                    match = pattern.search(processed_html)
                    if not match: continue
                    
                    item_template = match.group(1)
                    generated_items_html = ""
                    for item in element.get('value', []):
                        item_html = item_template
                        item_mapping = {el['id']: el.get('value', '') for el in item.get('elements', [])}
                        item_html = self._replace_all_placeholders(item_html, item_mapping)
                        generated_items_html += item_html
                    
                    processed_html = pattern.sub(generated_items_html, processed_html)

        # 5. Speichere das finale Ergebnis.
        output_path = self.output_dir / f"{project_name}.html"
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(processed_html)
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
    parser = argparse.ArgumentParser(description='CompanyCultureHub Site Generator v2.7')
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
