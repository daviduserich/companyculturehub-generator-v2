#!/usr/bin/env python3
"""
CompanyCultureHub Site Generator v4.0 (With Dynamic Theming Engine)
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

    print("--- STARTING GENERATOR V4.0 (DYNAMIC THEMING) ---")

    for project_dir in content_dir.iterdir():
        if not project_dir.is_dir(): continue

        project_name = project_dir.name
        print(f"🚀 Processing project: {project_name}")
        
        # ... (Logik zum Finden der content.json bleibt gleich) ...
        injected_content_file = project_dir / "content_color_injected.json"
        original_content_file = project_dir / "content.json"
        
        if injected_content_file.exists():
            content_file = injected_content_file
            print("   - ℹ️ Using 'content_color_injected.json'.")
        elif original_content_file.exists():
            content_file = original_content_file
            print("   - ℹ️ Using standard 'content.json'.")
        else:
            continue

        layout_file = project_dir / "layout.csv"
        if not layout_file.exists(): continue

        content_data = json.load(content_file.open(encoding='utf-8'))
        
        # === NEU: THEMING ENGINE LOGIK ===
        # 1. Definiere die "Rezepte" (Presets)
        presets = {
            "classic": { "bg": "solid", "card": "shadow", "btn": "rounded", "anim": "subtle" },
            "stylish": { "bg": "gradient", "card": "glass", "btn": "pill", "anim": "playful" }
        }
        
        # 2. Lese den Stil aus der content.json (mit "classic" als sicherem Fallback)
        style_choice = content_data.get("global_settings", {}).get("design", {}).get("presentation_style", "classic")
        chosen_preset = presets.get(style_choice, presets["classic"])
        
        # 3. Baue den String für die Body-Klassen zusammen
        theme_classes_str = f"bg-{chosen_preset['bg']} card-{chosen_preset['card']} btn-{chosen_preset['btn']} anim-{chosen_preset['anim']}"
        print(f"   - 🎨 Applying theme preset '{style_choice}': {theme_classes_str}")
        # === ENDE DER THEMING ENGINE LOGIK ===

        # ... (Logik für die final_mapping bleibt gleich) ...
        final_mapping = {}
        global_settings = content_data.get("global_settings", {})
        final_mapping.update(flatten_dict(global_settings))
        page_content = content_data.get("page_content", {})
        page_content_map = {}
        for section_name, elements in page_content.items():
            if isinstance(elements, list):
                for elem in elements:
                    if isinstance(elem, dict) and 'name' in elem and 'value' in elem and elem.get('type') != 'list':
                        key = f"{section_name}.{elem['name']}"
                        page_content_map[key] = elem.get('value', '')
        final_mapping.update(page_content_map)
        
        # Füge die neuen Theme-Klassen zur Mapping-Tabelle hinzu
        final_mapping['theme_classes'] = theme_classes_str

        # ... (Rest der Ersetzungs- und Bau-Logik bleibt exakt gleich) ...
        for _ in range(5):
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

        final_html = ""
        layout_plan = list(csv.DictReader(layout_file.open(encoding='utf-8')))
        enabled_components = [row for row in layout_plan if row.get('enabled', 'false').lower() == 'true']
        
        print(f"   - 🏗️ Assembling {len(enabled_components)} components...")
        for item in sorted(enabled_components, key=lambda x: int(x.get('order', 0))):
            component_name = item['component']
            component_path = templates_dir / "components" / f"{component_name}.html"
            if not component_path.exists(): continue
            component_html = component_path.read_text(encoding='utf-8')
            for key, value in final_mapping.items():
                component_html = component_html.replace(f"{{{{{key}}}}}", str(value))
            data_source_key = item['data_source']
            section_data = page_content.get(data_source_key, [])
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
                        for key, value in item_mapping.items():
                            item_html = item_html.replace(f"{{{{{key}}}}}", str(value))
                        generated_items_html += item_html
                    component_html = pattern.sub(generated_items_html, component_html)
            final_html += component_html + "\n"
        
        output_path = output_dir / f"{project_name}.html"
        output_path.write_text(final_html, encoding='utf-8')
        print(f"   - ✅ Website successfully generated: {output_path}")
        print("-" * 40)

if __name__ == "__main__":
    main()
