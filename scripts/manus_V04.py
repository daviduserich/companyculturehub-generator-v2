#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HTML Generator v4.0 - Vollständige Version mit korrigierter Farb- und Style-Integration
Nutzt ALLE vorhandenen Farb-Daten aus den JSON-Dateien
"""

import os
import json
import csv
import glob
import re
from datetime import datetime

def main():
    print("🚀 HTML Generator v4.0 gestartet - Mit korrigierter Farb-Integration")
    print("=" * 80)
    
    # Schritt 1: Pfade definieren
    try:
        print("📁 Schritt 1: Pfade definieren...")


        content_base_dir = "/workspaces/companyculturehub-generator-v2/content"
        templates_dir = "/workspaces/companyculturehub-generator-v2/templates"
        components_dir = "/workspaces/companyculturehub-generator-v2/templates/components"
        output_dir = "/workspaces/companyculturehub-generator-v2/docs"


        #print(f"   ✓ Projektordner: {project_dir}")
        print(f"   ✓ Templates: {templates_dir}")
        print(f"   ✓ Komponenten: {components_dir}")
        print(f"   ✓ Ausgabe: {output_dir}")
        
        # Ausgabeordner erstellen falls nicht vorhanden
        os.makedirs(output_dir, exist_ok=True)
        print(f"   ✓ Ausgabeordner bereit")
        
    except Exception as e:
        print(f"💥 FATALER FEHLER in Schritt 1: {e}")
        return False
    
    # Schritt 2: Projekt-Erkennung
    try:
        print("\n🔍 Schritt 2: Projekt-Erkennung...")
        
        # Finde alle Projekt-Ordner




        project_dirs = [d for d in os.listdir(content_base_dir) 
                       if os.path.isdir(os.path.join(content_base_dir, d)) 
                       and not d.endswith('_archives')]









        print(f"   📁 Gefundene Projekte: {project_dirs}")
        
        if not project_dirs:
            print("💥 FATALER FEHLER: Keine Projekt-Ordner im content-Verzeichnis gefunden.")
            return False
        
        # Sammle alle verfügbaren Stile aus allen Projekten
        available_styles = set()
        
        for project_name in project_dirs:
            project_dir = os.path.join(content_base_dir, project_name)
            style_pattern = os.path.join(project_dir, "interpreted_styles_*.json")
            style_files = glob.glob(style_pattern)
            
            for file_path in style_files:
                filename = os.path.basename(file_path)
                
                # Extrahiere alles zwischen "interpreted_styles_" und dem letzten "_"
                match = re.search(r'interpreted_styles_(.+)_\d{8}_\d{6}\.json', filename)

                if match:
                    style_name = match.group(1)
                    available_styles.add(style_name)
        
        available_styles = list(available_styles)
        print(f"   🎨 Verfügbare Stile: {available_styles}")
        
        if not available_styles:
            print("💥 FATALER FEHLER: Keine gültigen Stil-Namen gefunden.")
            return False

        
        print(f"   🎨 Verfügbare Stile: {available_styles}")
        
    except Exception as e:
        print(f"💥 FATALER FEHLER in Schritt 2: {e}")
        return False
    
    # Schritt 3: HTML- und JSON-Sammlungen laden
    try:
        print("\n📚 Schritt 3: HTML- und JSON-Sammlungen laden...")
        
        # Lade HTML-Sammlung und JSON Sammlung

        # Dynamische Erkennung der Sammlung-Dateien
        # Suche in mehreren möglichen Verzeichnissen
        possible_dirs = [
            "/workspaces/companyculturehub-generator-v2/upload",
            "/workspaces/companyculturehub-generator-v2/templates/components/en_bloc_html_s",
            "/workspaces/companyculturehub-generator-v2/templates/components"
        ]

        html_components_file = None
        json_components_file = None

        for search_dir in possible_dirs:
            if os.path.exists(search_dir):
                html_pattern = os.path.join(search_dir, "en_bloc_components_HTML_*.md")
                json_pattern = os.path.join(search_dir, "en_bloc_components_JSON_*.md")
                
                html_files = glob.glob(html_pattern)
                json_files = glob.glob(json_pattern)
                
                if html_files and json_files:
                    html_components_file = max(html_files, key=os.path.getmtime)
                    json_components_file = max(json_files, key=os.path.getmtime)
                    print(f"   📁 Gefunden in: {search_dir}")
                    break

        if not html_components_file or not json_components_file:
            print("💥 FEHLER: Komponenten-Dateien nicht gefunden!")
            return False


        # Nimm die neueste Datei (falls mehrere vorhanden)
        html_components_file = max(html_files, key=os.path.getmtime)
        json_components_file = max(json_files, key=os.path.getmtime)

        print(f"   📄 HTML-Datei: {os.path.basename(html_components_file)}")
        print(f"   📄 JSON-Datei: {os.path.basename(json_components_file)}")










        
        if not os.path.exists(html_components_file):
            print(f"💥 FEHLER: HTML-Komponenten-Datei nicht gefunden: {html_components_file}")
            return False
        
        if not os.path.exists(json_components_file):
            print(f"💥 FEHLER: JSON-Komponenten-Datei nicht gefunden: {json_components_file}")
            return False
        
        with open(html_components_file, 'r', encoding='utf-8') as f:
            html_components_content = f.read()
        
        with open(json_components_file, 'r', encoding='utf-8') as f:
            json_components_content = f.read()
        
        print(f"   ✓ HTML-Sammlung geladen: {len(html_components_content)} Zeichen")
        print(f"   ✓ JSON-Sammlung geladen: {len(json_components_content)} Zeichen")
        
    except Exception as e:
        print(f"💥 FATALER FEHLER in Schritt 3: {e}")
        return False
    
    # Schritt 4: Module aus Sammlungen extrahieren
    try:
        print("\n🧩 Schritt 4: Module aus Sammlungen extrahieren...")
        
        def extract_html_modules(content):
            """Extrahiert HTML-Module aus der Sammlung"""
            modules = {}
            # Pattern: ## HTML-Modul: `modulname.html`
            pattern = r'## HTML-Modul: `([^`]+)\.html`\s*\n```html\n(.*?)\n```'
            matches = re.findall(pattern, content, re.DOTALL)
            
            for module_name, html_content in matches:
                modules[module_name] = html_content.strip()
                print(f"   ✓ HTML-Modul extrahiert: {module_name} ({len(html_content)} Zeichen)")
            
            return modules
        
        def extract_json_schemas(content):
            """Extrahiert JSON-Schemas aus der Sammlung"""
            schemas = {}
            # Pattern: ## JSON-Modul: `modulname.json`
            pattern = r'## JSON-Modul: `([^`]+)\.json`\s*\n```json\n(.*?)\n```'
            matches = re.findall(pattern, content, re.DOTALL)
            
            for module_name, json_content in matches:
                try:
                    schema_data = json.loads(json_content.strip())
                    schemas[module_name] = schema_data
                    print(f"   ✓ JSON-Schema extrahiert: {module_name} ({len(schema_data)} Felder)")
                except json.JSONDecodeError as e:
                    print(f"   ⚠️  JSON-Schema fehlerhaft: {module_name} - {e}")
                    schemas[module_name] = {}
            
            return schemas
        
        html_modules = extract_html_modules(html_components_content)
        json_schemas = extract_json_schemas(json_components_content)
        
        print(f"   📦 HTML-Module extrahiert: {len(html_modules)}")
        print(f"   📋 JSON-Schemas extrahiert: {len(json_schemas)}")
        
    except Exception as e:
        print(f"💥 FATALER FEHLER in Schritt 4: {e}")
        return False
    
    # Schritt 5: Haupt-Schleife für jeden Stil
    # Schritt 5: Projekt-Erkennung
    # project_dirs bereits in Schritt 2 definiert - verwende die gefilterte Version

    
    print(f"🔍 Gefundene Projekte: {project_dirs}")
    
    generated_files = []
    
    for project_name in project_dirs:
        project_dir = os.path.join(content_base_dir, project_name)
        print(f"\n📁 Verarbeite Projekt: {project_name}")
        
        for style_name in available_styles:


            print(f"\n🎯 Verarbeite Stil: {style_name}")
            print("-" * 50)
        
            try:
                # Schritt 5.1: Stil-spezifische Pfade definieren
                print(f"📂 Schritt 5.1: Stil-spezifische Pfade für '{style_name}'...")
                
                def find_newest_file(pattern):
                    """Findet die neueste Datei basierend auf einem Muster"""
                    files = glob.glob(pattern)
                    if not files:
                        return None
                    # Sortiere nach Änderungsdatum (neueste zuerst)
                    files.sort(key=os.path.getmtime, reverse=True)
                    return files[0]
                
                # Basis-Dateien (stil-unabhängig)
                defaults_path = os.path.join(components_dir, "_defaults.json")
                layout_path = os.path.join(project_dir, "layout_extended_v2.csv")
                placeholder_assets_path = os.path.join(project_dir, "_placeholder_assets.json")
                
                # Farb-Dateien (KORRIGIERT: Auch ohne Zeitstempel suchen)
                colors_pattern_timestamped = os.path.join(project_dir, f"interpreted_colors_*.json")
                colors_pattern_simple = os.path.join(project_dir, "interpreted_colors.json")
                
                # Stil-spezifische Dateien
               
                project_template_pattern = os.path.join(project_dir, f"project_template_Stufe02_Styled_{style_name}_*.json")

        
                text_colors_pattern = os.path.join(project_dir, f"interpreted_text_colors_*.json")

                # Exakte Suche - nur Dateien die genau dem style_name entsprechen
                styles_pattern = os.path.join(project_dir, f"interpreted_styles_{style_name}_*.json")


                project_template_path = find_newest_file(project_template_pattern)
                
                # KORRIGIERT: Farb-Dateien richtig finden
                colors_path = find_newest_file(colors_pattern_timestamped)
                if not colors_path and os.path.exists(colors_pattern_simple):
                    colors_path = colors_pattern_simple
                
                text_colors_path = find_newest_file(text_colors_pattern)
                styles_path = find_newest_file(styles_pattern)
                
                print(f"   ✓ Defaults: {os.path.basename(defaults_path) if os.path.exists(defaults_path) else 'FEHLT'}")
                print(f"   ✓ Layout: {os.path.basename(layout_path) if os.path.exists(layout_path) else 'FEHLT'}")
                print(f"   ✓ Placeholder Assets: {os.path.basename(placeholder_assets_path) if os.path.exists(placeholder_assets_path) else 'FEHLT'}")
                print(f"   ✓ Project Template: {os.path.basename(project_template_path) if project_template_path else 'FEHLT'}")
                print(f"   ✓ Colors: {os.path.basename(colors_path) if colors_path else 'FEHLT'}")
                print(f"   ✓ Text Colors: {os.path.basename(text_colors_path) if text_colors_path else 'FEHLT'}")
                print(f"   ✓ Styles: {os.path.basename(styles_path) if styles_path else 'FEHLT'}")
                
                # Prüfe kritische Dateien
                critical_files = [
                    ("Layout CSV", layout_path),
                    ("Styles JSON", styles_path)
                ]
                
                missing_files = []
                for name, path in critical_files:
                    if not path or not os.path.exists(path):
                        missing_files.append(name)
                
                if missing_files:
                    print(f"💥 FEHLER für Stil '{style_name}': Kritische Dateien fehlen: {', '.join(missing_files)}")
                    continue
                
            except Exception as e:
                print(f"💥 FEHLER in Schritt 5.1 für Stil '{style_name}': {e}")
                continue
            
            try:
                # Schritt 5.2: Layout-Module laden
                print(f"🧩 Schritt 5.2: Layout-Module laden für '{style_name}'...")
                
                active_modules = []
                with open(layout_path, 'r', encoding='utf-8') as f:
                    csv_reader = csv.DictReader(f)
                    for row in csv_reader:
                        # Prüfe sowohl 'enabled' als auch 'active' Spalten
                        enabled = row.get('enabled', row.get('active', '')).strip().upper()
                        if enabled == 'TRUE':
                            # Verwende 'component' als Modulname (entspricht der CSV-Struktur)
                            module_name = row.get('component', '').strip()
                            if module_name:
                                active_modules.append(module_name)
                                print(f"   ✓ Aktives Modul: {module_name}")
                
                print(f"   📦 Aktive Module gesamt: {len(active_modules)}")
                
                if not active_modules:
                    print(f"💥 FEHLER für Stil '{style_name}': Keine aktiven Module in Layout gefunden")
                    continue
                
            except Exception as e:
                print(f"💥 FEHLER in Schritt 5.2 für Stil '{style_name}': {e}")
                continue
            
            try:
                # Schritt 5.3: Daten sammeln und Schema-Integration
                print(f"📊 Schritt 5.3: Daten sammeln und Schema-Integration für '{style_name}'...")
                
                final_mapping = {}
                
                # Lade Basis-Defaults
                if os.path.exists(defaults_path):
                    with open(defaults_path, 'r', encoding='utf-8') as f:
                        defaults_data = json.load(f)
                        final_mapping.update(defaults_data)
                        print(f"   ✓ Defaults geladen: {len(defaults_data)} Einträge")
                
                # Lade Project Template (falls vorhanden)
                if project_template_path and os.path.exists(project_template_path):
                    with open(project_template_path, 'r', encoding='utf-8') as f:
                        project_data = json.load(f)
                        final_mapping.update(project_data)
                        print(f"   ✓ Project Template geladen: {len(project_data)} Einträge")
                
                # Lade Placeholder Assets (falls vorhanden)
                if os.path.exists(placeholder_assets_path):
                    with open(placeholder_assets_path, 'r', encoding='utf-8') as f:
                        assets_data = json.load(f)
                        final_mapping.update(assets_data)
                        print(f"   ✓ Placeholder Assets geladen: {len(assets_data)} Einträge")
                
                # **KORRIGIERT: Farben richtig laden und verarbeiten**
                colors_data = {}
                if colors_path and os.path.exists(colors_path):
                    with open(colors_path, 'r', encoding='utf-8') as f:
                        colors_raw = json.load(f)
                        colors_data = colors_raw
                        final_mapping.update(colors_raw)
                        print(f"   ✓ Colors geladen: {len(colors_raw)} Einträge")
                        print(f"      🎨 Farb-Daten: {colors_raw}")
                
                # Lade Text-Farben (falls vorhanden)
                text_colors_data = {}
                if text_colors_path and os.path.exists(text_colors_path):
                    with open(text_colors_path, 'r', encoding='utf-8') as f:
                        text_colors_raw = json.load(f)
                        text_colors_data = text_colors_raw
                        final_mapping.update(text_colors_raw)
                        print(f"   ✓ Text Colors geladen: {len(text_colors_raw)} Einträge")
                
                # **KORRIGIERT: Styles richtig laden und verarbeiten**
                styles_data = {}
                if styles_path and os.path.exists(styles_path):
                    with open(styles_path, 'r', encoding='utf-8') as f:
                        styles_raw = json.load(f)
                        styles_data = styles_raw
                        final_mapping.update(styles_raw)
                        print(f"   ✓ Styles geladen: {len(styles_raw)} Einträge")
                        print(f"      🎨 Style-Daten: {list(styles_raw.keys())}")
                
                # JSON-Schema-Integration
                print(f"   🔗 Schema-Integration für aktive Module...")
                schema_integrated_count = 0
                
                for module_name in active_modules:
                    if module_name in json_schemas:
                        schema = json_schemas[module_name]
                        
                        # Integriere Schema-Daten in final_mapping
                        module_namespace = f"{module_name}"
                        
                        def integrate_schema_recursive(schema_obj, namespace):
                            """Rekursive Integration von Schema-Daten"""
                            integrated_data = {}
                            
                            for key, value in schema_obj.items():
                                full_key = f"{namespace}.{key}"
                                
                                if isinstance(value, dict):
                                    if 'example_value' in value:
                                        # Einzelnes Feld mit example_value
                                        integrated_data[full_key] = value.get('example_value', '')
                                    elif 'description' in value and not any(k in value for k in ['example_value', 'value']):
                                        # Verschachteltes Objekt (z.B. benefits_list)
                                        nested_data = integrate_schema_recursive(value, full_key)
                                        integrated_data.update(nested_data)
                                    else:
                                        # Anderes verschachteltes Objekt
                                        nested_data = integrate_schema_recursive(value, full_key)
                                        integrated_data.update(nested_data)
                            
                            return integrated_data
                        
                        schema_data = integrate_schema_recursive(schema, module_namespace)
                        final_mapping.update(schema_data)
                        schema_integrated_count += 1
                        
                        print(f"      ✓ Schema integriert: {module_name} ({len(schema_data)} Felder)")
                    else:
                        print(f"      ⚠️  Kein Schema gefunden: {module_name}")
                
                print(f"   📋 Schemas integriert: {schema_integrated_count}/{len(active_modules)}")
                print(f"   📋 Gesamt-Mapping: {len(final_mapping)} Einträge")
                
            except Exception as e:
                print(f"💥 FEHLER in Schritt 5.3 für Stil '{style_name}': {e}")
                continue
            
            try:
                # Schritt 5.4: HTML-Rohbau zusammensetzen
                print(f"🏗️  Schritt 5.4: HTML-Rohbau zusammensetzen für '{style_name}'...")
                

                # Intelligente Header-Erstellung
                if 'technik_header_section' in active_modules and 'technik_header_section' in html_modules:
                    # Verwende technik_header_section als Basis
                    technik_header_html = html_modules['technik_header_section']
                    
                    # Extrahiere nur <head>-Inhalt (ohne <!DOCTYPE> und <html>)
                  
                    head_match = re.search(r'<head>(.*?)</head>', technik_header_html, re.DOTALL)
                    if head_match:
                        head_content = head_match.group(1)
                        
                        # Erstelle vollständiges HTML mit technik_header <head> + CSS
                        header_html = f"""<!DOCTYPE html>
    <html lang="de">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
    {head_content}
        {{{{GENERATED_STYLE_BLOCK}}}}
    </head>
    <body class="{{{{BODY_CLASSES}}}}">"""
                        
                        print(f"   ✓ Intelligenter Header mit technik_header_section erstellt")
                        
                        # technik_header_section aus active_modules entfernen (bereits verwendet)
                        active_modules = [m for m in active_modules if m != 'technik_header_section']
                    else:
                        # Fallback wenn <head> nicht gefunden
                        header_html = """<!DOCTYPE html>
    <html lang="de">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{{SITE_TITLE}}</title>
        {{GENERATED_STYLE_BLOCK}}
    </head>
    <body class="{{BODY_CLASSES}}">"""
                        print(f"   ⚠️  technik_header_section <head> nicht gefunden, verwende Fallback")
                else:
                    # Fallback Header (wie bisher)
                    header_html = """<!DOCTYPE html>
    <html lang="de">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{{SITE_TITLE}}</title>
        {{GENERATED_STYLE_BLOCK}}
    </head>
    <body class="{{BODY_CLASSES}}">"""
                    print(f"   ⚠️  technik_header_section nicht verfügbar, verwende Fallback")












                # Module zusammensetzen
                body_html = ""
                modules_added = 0
                
                for module_name in active_modules:
                    if module_name in html_modules:
                        module_html = html_modules[module_name]
                        body_html += module_html + "\n\n"
                        modules_added += 1
                        print(f"   ✓ Modul hinzugefügt: {module_name} ({len(module_html)} Zeichen)")
                    else:
                        # Fallback für fehlende Module
                        fallback_html = f"<!-- Modul {module_name} nicht gefunden -->"
                        body_html += fallback_html + "\n\n"
                        print(f"   ⚠️  Modul nicht gefunden, Fallback verwendet: {module_name}")
                
                # Footer
                footer_html = """
    </body>
    </html>"""
                
                # Vollständiges HTML zusammensetzen
                full_html = header_html + "\n\n" + body_html + footer_html
                
                print(f"   🏗️  HTML-Rohbau erstellt: {len(full_html)} Zeichen")
                print(f"   📦 Module hinzugefügt: {modules_added}/{len(active_modules)}")
                
            except Exception as e:
                print(f"💥 FEHLER in Schritt 5.4 für Stil '{style_name}': {e}")
                continue
            
            try:
                # **SCHRITT 5.5: KORRIGIERTE CSS-BLOCK-GENERIERUNG MIT FARBEN**
                print(f"🎨 Schritt 5.5: CSS-Block generieren mit Farb-Integration für '{style_name}'...")
                
                css_variables = []
                
                # **NEU: Farb-Variablen aus colors_data extrahieren**
                if colors_data and 'colors' in colors_data:
                    color_mapping = colors_data['colors']
                    print(f"   🎨 Verarbeite Farb-Palette: {list(color_mapping.keys())}")
                    

                    # Module-kompatible CSS-Variablen
                    css_variables.extend([
                        f"    --color-primary: {color_mapping.get('primary_color', '#FF5733')};",
                        f"    --color-secondary: {color_mapping.get('secondary_color', '#C70039')};",
                        f"    --color-accent: {color_mapping.get('accent_color', '#900C3F')};",
                        f"    --text-on-primary: white;",
                        f"    --text-on-secondary: white;",
                        f"    --text-on-accent: white;"
                    ])
                    print(f"      ✓ Module-kompatible Farb-Variablen erstellt")



                # **NEU: Modul-spezifische Farben aus styles_data extrahieren**
                if styles_data and 'styles' in styles_data:
                    style_mapping = styles_data['styles']
                    print(f"   🎨 Verarbeite Modul-Styles: {len(style_mapping)} Module")
                    
                    for module_name, module_styles in style_mapping.items():
                        if isinstance(module_styles, dict):
                            # Background-Farben
                            if 'background_color' in module_styles:
                                bg_color = module_styles['background_color']
                                if isinstance(bg_color, str) and bg_color.startswith('#'):
                                    css_var_name = f"--{module_name.replace('_', '-')}-bg"
                                    css_variables.append(f"    {css_var_name}: {bg_color};")
                                    print(f"      ✓ Modul-Farbe: {css_var_name} = {bg_color}")
                
                # Basis-CSS-Variablen hinzufügen
                default_css_vars = [
                    "    --font-family: 'Inter', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;",
                    "    --font-size-base: 16px;",
                    "    --font-size-h1: 3rem;",
                    "    --font-size-h2: 2.5rem;",
                    "    --font-size-h3: 2rem;",
                    "    --spacing-section-large: 80px;",
                    "    --spacing-section-medium: 60px;",
                    "    --spacing-section-small: 40px;",
                    "    --border-radius: 8px;",
                    "    --box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);"
                ]
                
                css_variables.extend(default_css_vars)
                

                
                # Vollständiger CSS-Block
                generated_style_block = f"""<style>
    :root {{
    {chr(10).join(css_variables)}
    }}

    /* Basis-Styles */
    body {{
        margin: 0;
        padding: 0;
        font-family: var(--font-family);
        font-size: var(--font-size-base);
        line-height: 1.6;
        color: var(--text-color, #333);
    }}

    .container {{
        max-width: 1200px;
        margin: 0 auto;
        padding: 0 20px;
    }}

    .section-header {{
        text-align: center;
        margin-bottom: 40px;
    }}

    .section-header h2 {{
        font-size: var(--font-size-h2);
        margin-bottom: 20px;
        color: var(--primary-color, #333);
    }}

    .section-header .description {{
        font-size: 1.2rem;
        opacity: 0.9;
        color: var(--secondary-color, #666);
    }}

    /* Responsive Design */
    @media (max-width: 768px) {{
        .section-header h2 {{
            font-size: 2rem;
        }}
        
        .container {{
            padding: 0 15px;
        }}
    }}

    
    /* Modul-spezifische Styles werden automatisch generiert */

    </style>"""
                
                # CSS-Block in final_mapping hinzufügen
                final_mapping['GENERATED_STYLE_BLOCK'] = generated_style_block
                
                # Standard-Platzhalter hinzufügen
                if 'SITE_TITLE' not in final_mapping:
                    final_mapping['SITE_TITLE'] = f"Karriere-Website - {style_name.title()} Style"
                

                
                # Stil-spezifische Body-Klassen für Module-Architektur
                style_classes = {
                    'classic': 'bg-solid card-shadow anim-subtle',
                    'classic_accents': 'bg-solid card-shadow anim-subtle',
                    'stylish': 'bg-gradient card-glass anim-playful',
                    'hyper_stylish': 'bg-gradient card-glass anim-playful'
                }
                final_mapping['BODY_CLASSES'] = style_classes.get(style_name, 'bg-solid card-flat anim-subtle')


                print(f"   ✅ CSS-Block generiert: {len(generated_style_block)} Zeichen")
                print(f"   🎨 CSS-Variablen: {len(css_variables)}")

                print(f"   🎨 Basis-CSS: Vollständig generiert")
                
            except Exception as e:
                print(f"💥 FEHLER in Schritt 5.5 für Stil '{style_name}': {e}")
                continue
            
            try:
                # Schritt 5.6: Iterative Platzhalter-Ersetzung
                print(f"🔄 Schritt 5.6: Platzhalter-Ersetzung für '{style_name}'...")
                
                def replace_placeholders(text, mapping, max_iterations=10):
                    """Iterative Platzhalter-Ersetzung"""
                    for iteration in range(max_iterations):
                        original_text = text
                        
                        # Finde alle {{...}} Platzhalter
                        placeholders = re.findall(r'\{\{([^}]+)\}\}', text)
                        
                        if not placeholders:
                            print(f"      ✓ Iteration {iteration + 1}: Keine Platzhalter mehr gefunden")
                            break
                        
                        replaced_count = 0
                        for placeholder in placeholders:
                            placeholder_key = placeholder.strip()
                            if placeholder_key in mapping:
                                old_placeholder = f"{{{{{placeholder}}}}}"
                                new_value = str(mapping[placeholder_key])
                                text = text.replace(old_placeholder, new_value)
                                replaced_count += 1
                        
                        print(f"      ✓ Iteration {iteration + 1}: {replaced_count} Platzhalter ersetzt")
                        
                        # Wenn keine Änderungen mehr, beenden
                        if text == original_text:
                            print(f"      ✓ Konvergenz erreicht nach {iteration + 1} Iterationen")
                            break
                    
                    # Prüfe auf verbleibende Platzhalter
                    remaining_placeholders = re.findall(r'\{\{([^}]+)\}\}', text)
                    if remaining_placeholders:
                        print(f"      ⚠️  Verbleibende Platzhalter: {remaining_placeholders[:5]}...")
                    
                    return text
                
                # Führe Ersetzung durch
                final_html = replace_placeholders(full_html, final_mapping)
                
                print(f"   ✓ Platzhalter-Ersetzung abgeschlossen")
                print(f"   📄 Finale HTML-Größe: {len(final_html)} Zeichen")
                
            except Exception as e:
                print(f"💥 FEHLER in Schritt 5.6 für Stil '{style_name}': {e}")
                continue
            
            try:
                # Schritt 5.7: Datei speichern
                print(f"💾 Schritt 5.7: Datei speichern für '{style_name}'...")
                
                output_filename = f"DEF_88_{style_name}_v4.html"
                output_path = os.path.join(output_dir, output_filename)
                
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(final_html)
                
                generated_files.append(output_path)
                
                print(f"   ✅ Datei gespeichert: {output_filename}")
                print(f"   📍 Pfad: {output_path}")
                print(f"   📊 Größe: {len(final_html)} Zeichen")
                
            except Exception as e:
                print(f"💥 FEHLER in Schritt 5.7 für Stil '{style_name}': {e}")
                continue
            
            print(f"✅ Stil '{style_name}' erfolgreich verarbeitet!")
    
    # Abschluss
    print("\n" + "=" * 80)
    print("🎉 HTML-Generierung mit Farb-Integration abgeschlossen!")
    print(f"📊 Verarbeitete Stile: {len(available_styles)}")
    print(f"✅ Erfolgreich generierte Dateien: {len(generated_files)}")
    
    for file_path in generated_files:
        filename = os.path.basename(file_path)
        file_size = os.path.getsize(file_path)
        print(f"   📄 {filename} ({file_size:,} Bytes)")
    
    return len(generated_files) > 0

if __name__ == "__main__":
    success = main()
    if success:
        print("\n🏆 MISSION ERFOLGREICH! Der Generator mit vollständiger Farb-Integration funktioniert.")
    else:
        print("\n💥 MISSION FEHLGESCHLAGEN! Bitte Fehler prüfen.")

