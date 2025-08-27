#!/usr/bin/env python3
"""
CompanyCultureHub Site Generator v3.4 (Final - With Corrected Mapping Logic)
"""
import json, csv, re, argparse
from pathlib import Path

def flatten_dict(d, parent_key='', sep='.'):
    """Flattens a nested dictionary."""
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)

def main():
    """Main function to generate a static site from content and templates."""
    base_dir = Path(__file__).resolve().parent.parent
    content_dir = base_dir / "content"
    templates_dir = base_dir / "templates"
    output_dir = base_dir / "docs"
    output_dir.mkdir(exist_ok=True)

    print("--- STARTING GENERATOR V3.4 (FINAL) ---")

    for project_dir in content_dir.iterdir():
        if not project_dir.is_dir(): continue

        project_name = project_dir.name
        print(f"🚀 Processing project: {project_name}")
        
        content_file = project_dir / "content.json"
        layout_file = project_dir / "layout.csv"
        if not content_file.exists() or not layout_file.exists(): continue

        content_data = json.load(content_file.open(encoding='utf-8'))
        
        # 1. Erstelle eine Map für alle einfachen Werte
        final_mapping = {}
        global_settings = content_data.get("global_settings", {})
        final_mapping.update(flatten_dict(global_settings))
        
        page_content = content_data.get("page_content", {})
        page_content_map = {}
        
        # === KORREKTUR: Stelle sicher, dass ALLE name/value Paare erfasst werden ===
        # Die Logik iteriert jetzt durch alle Sektionen und sammelt jedes Element,
        # das ein 'name' und 'value' Paar hat, aber keine Liste ist.
        for section_name, elements in page_content.items():
            if isinstance(elements, list):
                for elem in elements:
                    if isinstance(elem, dict) and 'name' in elem and 'value' in elem and elem.get('type') != 'list':
                        key = f"{section_name}.{elem['name']}"
                        page_content_map[key] = elem.get('value', '')
        final_mapping.update(page_content_map)
        # === ENDE DER KORREKTUR ===
        
        # 2. Ersetze verschachtelte Variablen (z.B. {{identity.company_name}} in Texten)
        for _ in range(5): # Iteriere mehrmals, um alle Ebenen aufzulösen
            is_dirty = False
            for key, value in final_mapping.items():
                if isinstance(value, str):
                    original_value = value
                    for map_key, map_value in final_mapping.items():
                        placeholder = f"{{{{{map_key}}}}}"
                        if placeholder in value:
                            value = value.replace(placeholder, str(map_value))
                    if original_value != value:
                        final_mapping[key] = value
                        is_dirty = True
            if not is_dirty:
                break
        print("   - ✅ Resolved all variables.")

        # 3. Baue die Seite zusammen
        final_html = ""
        layout_plan = list(csv.DictReader(layout_file.open(encoding='utf-8')))
        enabled_components = [row for row in layout_plan if row.get('enabled', 'false').lower() == 'true']
        
        print(f"   - 🏗️ Assembling {len(enabled_components)} components...")
        for item in sorted(enabled_components, key=lambda x: int(x.get('order', 0))):
            component_name = item['component']
            component_path = templates_dir / "components" / f"{component_name}.html"
            if not component_path.exists(): continue

            component_html = component_path.read_text(encoding='utf-8')
            
            # 4. Ersetze zuerst die einfachen Platzhalter in der Komponente
            for key, value in final_mapping.items():
                component_html = component_html.replace(f"{{{{{key}}}}}", str(value))

            # 5. Verarbeite die Listen in dieser Komponente
            data_source_key = item['data_source']
            section_data = page_content.get(data_source_key, [])
            
            for element in section_data:
                if isinstance(element, dict) and element.get('type') == 'list':
                    list_id = f"{data_source_key}.{element['name']}"
                    print(f"      - 🔍 Found list '{list_id}'. Processing...")
                    pattern = re.compile(rf'<!-- BEGIN_LIST_ITEM:{re.escape(list_id)} -->(.*?)<!-- END_LIST_ITEM:{re.escape(list_id)} -->', re.DOTALL)
                    match = pattern.search(component_html)
                    
                    if not match:
                        print(f"         - ⚠️ WARNING: List block for '{list_id}' not found in component '{component_name}'.")
                        continue
                    
                    item_template = match.group(1)
                    generated_items_html = ""
                    for list_item in element.get('value', []):
                        item_html = item_template
                        item_mapping = {el['name']: el.get('value', '') for el in list_item.get('elements', [])}
                        
                        for key, value in item_mapping.items():
                            item_html = item_html.replace(f"{{{{{key}}}}}", str(value))
                        generated_items_html += item_html
                    
                    component_html = pattern.sub(generated_items_html, component_html)
                    print(f"         - ✅ List '{list_id}' processed successfully.")

            final_html += component_html + "\n"
        
        # 6. Speichern
        output_path = output_dir / f"{project_name}.html"
        output_path.write_text(final_html, encoding='utf-8')
        print(f"   - ✅ Website successfully generated: {output_path}")
        print("-" * 40)

if __name__ == "__main__":
    main()
