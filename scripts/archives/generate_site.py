#!/usr/bin/env python3
"""
CompanyCultureHub Site Generator
Automatisches Mapping von JSON-Daten auf HTML-Template
"""

import json
import os
import re
import shutil
from pathlib import Path
from datetime import datetime
import argparse

class CompanyCultureHubGenerator:
    def __init__(self, template_path="templates/employer_branding_template.html", 
                 output_dir="docs", content_dir="content"):
        # Pfade relativ zum Repository-Root setzen
        self.base_dir = Path(__file__).resolve().parent.parent
        self.template_path = self.base_dir / template_path
        self.output_dir = self.base_dir / output_dir
        self.content_dir = self.base_dir / content_dir
        
        # Erstelle Output-Verzeichnis falls nicht vorhanden
        self.output_dir.mkdir(exist_ok=True)
        
    def load_json_content(self, json_file):
        """Lädt JSON-Content aus Datei"""
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"❌ Fehler beim Laden der JSON-Datei: {e}")
            return None
    
    def load_template(self):
        """Lädt HTML-Template"""
        try:
            with open(self.template_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"❌ Fehler beim Laden des Templates: {e}")
            return None
    
    def extract_placeholders(self, template):
        """Extrahiert alle Platzhalter aus dem Template"""
        pattern = r'\{\{([^}]+)\}\}'
        placeholders = re.findall(pattern, template)
        return list(set(placeholders))  # Entferne Duplikate
    
    def map_content_to_template(self, template, content_data):
        """Ersetzt Platzhalter im Template mit JSON-Daten"""
        content = content_data.get("employer_branding_content", {})
        
        mappings = {}
        for section_content in content.values():
            if isinstance(section_content, dict):
                mappings.update(section_content)

        result_html = template
        placeholders = self.extract_placeholders(template)
        
        for placeholder in placeholders:
            if placeholder in mappings:
                replacement = str(mappings[placeholder])
                result_html = result_html.replace(f'{{{{{placeholder}}}}}', replacement)
        
        return result_html
    
    def generate_site(self, json_file, output_filename="index.html"):
        """Generiert Website aus JSON-Daten"""
        print(f"🚀 CompanyCultureHub Generator gestartet für {json_file.name}")
        
        content_data = self.load_json_content(json_file)
        if not content_data:
            return False
        
        template = self.load_template()
        if not template:
            return False
        
        result_html = self.map_content_to_template(template, content_data)
        
        output_path = self.output_dir / output_filename
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(result_html)
            print(f"✅ Website erfolgreich generiert: {output_path}")
            return True
        except Exception as e:
            print(f"❌ Fehler beim Speichern: {e}")
            return False
    
    def generate_multiple_sites(self):
        """Generiert Websites für alle JSON-Dateien im Content-Verzeichnis"""
        json_files = list(self.content_dir.glob("*.json"))
        
        if not json_files:
            print("⚠️  Keine JSON-Dateien im Content-Verzeichnis gefunden")
            return
        
        for json_file in json_files:
            company_name = json_file.stem
            output_filename = f"{company_name}.html"
            self.generate_site(json_file, output_filename)
        
        self.create_index_page()
    
    def create_index_page(self):
        """Erstellt eine Index-Seite mit Links zu allen generierten Websites"""
        html_files = [f for f in self.output_dir.glob("*.html") if f.name != "index.html"]
        
        if not html_files:
            return
        
        # Die CSS-Klammern {} müssen mit {{}} escaped werden, damit .format() sie ignoriert
        index_html = """<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <title>CompanyCultureHub - Generated Sites</title>
    <style>
        body {{ font-family: sans-serif; max-width: 800px; margin: 40px auto; padding: 20px; }}
        h1 {{ text-align: center; }}
        ul {{ list-style: none; padding: 0; }}
        li {{ margin: 15px 0; padding: 15px; border: 1px solid #ddd; border-radius: 5px; }}
        a {{ text-decoration: none; font-weight: bold; font-size: 1.2em; }}
        .timestamp {{ color: #666; font-size: 0.9em; }}
    </style>
</head>
<body>
    <h1>🏢 CompanyCultureHub Sites</h1>
    <div><strong>Last updated:</strong> {timestamp}</div>
    <ul>{site_links}</ul>
</body>
</html>"""
        
        site_links = ""
        for html_file in sorted(html_files):
            company_name = html_file.stem.replace("_", " ").title()
            site_links += f'<li><a href="{html_file.name}">{company_name}</a><div class="timestamp">File: {html_file.name}</div></li>'
        
        final_html = index_html.format(
            timestamp=datetime.now().strftime("%d.%m.%Y %H:%M:%S"),
            site_links=site_links
        )
        
        index_path = self.output_dir / "index.html"
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(final_html)
        print(f"📋 Index-Seite erstellt: {index_path}")

def main():
    parser = argparse.ArgumentParser(description='CompanyCultureHub Site Generator')
    parser.add_argument('--all', action='store_true', help='Alle JSON-Dateien im content-Ordner verarbeiten')
    args = parser.parse_args()
    
    generator = CompanyCultureHubGenerator()
    
    if args.all:
        generator.generate_multiple_sites()
    else:
        generator.generate_multiple_sites()

if __name__ == "__main__":
    main()
