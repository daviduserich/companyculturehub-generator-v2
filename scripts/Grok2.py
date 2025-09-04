
#!/usr/bin/env python3
"""
CompanyCultureHub HTML Generator v20.0 (The Colored and Spaced Edition)
- Fixiert Farben: Ersetzt {{design.branding.*}} aus colors_data, wrappt :root.
- Fixiert Abstände: Setzt --spacing-*, --font-size-*, --border-radius-* in :root aus defaults.
- Fallback-Hierarchie: value > example_value > description > default für alle Platzhalter (53+).
- Konsolidiert Styles im <head>, merge class-Attribute.
- Logging und Validierung für Farben/Abstände.
"""
import json
import csv
import re
import shutil
from pathlib import Path
from datetime import datetime
import logging

# === 1. KONFIGURATION & PFADE ===
BASE_DIR = Path(__file__).resolve().parent.parent
CONTENT_DIR = BASE_DIR / "content"
TEMPLATES_DIR = BASE_DIR / "templates"
COMPONENTS_DIR = TEMPLATES_DIR / "components"
OUTPUT_DIR = BASE_DIR / "docs"
OUTPUT_DIR.mkdir(exist_ok=True)
logging.basicConfig(filename=OUTPUT_DIR / "html_generator.log", level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filemode='w')

# === 2. HELFERFUNKTIONEN ===
def load_json(file_path, default=None):
    if not file_path.exists():
        logging.warning(f"Datei fehlt: {file_path}")
        return default if default is not None else {}
    try:
        with file_path.open(encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        logging.error(f"JSON-Fehler in {file_path}: {e}")
        return default if default is not None else {}

def find_newest_file(directory, pattern):
    try:
        return max(directory.glob(pattern), key=lambda f: f.stat().st_mtime)
    except ValueError:
        logging.warning(f"Keine Dateien für {pattern} in {directory}")
        return None

def flatten_dict(d, parent_key='', sep='.'):
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        elif isinstance(v, list):
            for i, item in enumerate(v):
                items.extend(flatten_dict(item, f"{new_key}[{i}]", sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)

def replace_placeholders(html, data_dict):
    for _ in range(5):
        is_dirty = False
        for key, value in data_dict.items():
            placeholder = f"{{{{{key}}}}}"
            if placeholder in html:
                html = html.replace(placeholder, str(value))
                is_dirty = True
        if not is_dirty:
            break
    remaining = re.findall(r'\{\{[^}]+\}\}', html)
    if remaining:
        logging.warning(f"Unersetzte Platzhalter: {remaining}")
    return html

# === 3. KERNLOGIK ===
def generate_site_for_style(project_dir, style_name, content_data, layout_plan, placeholder_assets, global_defaults):
    project_name = project_dir.name
    print(f"   - 🎨 Generiere Seite für Style: '{style_name}'")

    # Lade Daten
    style_data = load_json(find_newest_file(project_dir, f"interpreted_styles_{style_name}*.json"))
    colors_data = load_json(find_newest_file(project_dir, "interpreted_colors*.json"))
    text_colors_data = load_json(find_newest_file(project_dir, "interpreted_text_colors*.json"))
    layout_rules = load_json(project_dir / "layout_rules.json", {})

    # Mapping aufbauen
    final_mapping = flatten_dict(global_defaults)
    # Füge Farben zu design.branding hinzu
    if 'colors' in colors_data:
        for key, value in colors_data['colors'].items():
            final_mapping[f"design.branding.{key}"] = value
    if 'text_colors' in text_colors_data:
        for section, colors in text_colors_data['text_colors'].items():
            final_mapping[f"text_colors.{section}.default"] = colors.get('default', '#000000')
            final_mapping[f"text_colors.{section}.heading"] = colors.get('heading', '#000000')
    if "global_settings" in content_data:
        final_mapping.update(flatten_dict(content_data["global_settings"]))
    for component, rules in layout_rules.get("fixed_layouts", {}).items():
        final_mapping.update(flatten_dict(rules, component))

    component_counters = {row['component']: 0 for row in layout_plan}
    for item in sorted(layout_plan, key=lambda x: int(x.get('order', 0))):
        component_name = item['component']
        if not component_name:
            continue
        instance_index = component_counters[component_name]
        component_instances = content_data.get("page_content", {}).get(component_name, [])
        if instance_index >= len(component_instances):
            continue
        instance_data = component_instances[instance_index]
        component_counters[component_name] += 1

        for key, data in instance_data.items():
            if isinstance(data, dict):
                value = data.get('value') or data.get('example_value') or data.get('description', "") or global_defaults.get(f"{component_name}.{key}", "")
                final_mapping[f"{component_name}.{key}"] = value
            elif isinstance(data, list):
                for i, item in enumerate(data):
                    for sub_key, sub_data in item.items():
                        sub_value = sub_data.get('value') or sub_data.get('example_value') or sub_data.get('description', "") or global_defaults.get(f"{component_name}.{key}[0].{sub_key}", "")
                        final_mapping[f"{component_name}.{key}[{i}].{sub_key}"] = sub_value

        # Bild-Fallbacks
        for key in ["image_url", "map_url", "image_alt_text"]:
            full_key = f"{component_name}.{key}"
            if not final_mapping.get(full_key):
                urls = placeholder_assets.get(component_name, {}).get("urls", [])
                if urls:
                    final_mapping[full_key] = urls[instance_index % len(urls)]

    # CSS-Block mit Farben, Textfarben und Abständen
    css_vars_string = ":root {\n"
    # Farben
    for key, value in colors_data.get("colors", {}).items():
        if isinstance(value, str) and (value.startswith("#") or value.startswith("linear-gradient")):
            css_vars_string += f"    --{key.replace('_', '-')}: {value};\n"
    # Textfarben
    for section, colors in text_colors_data.get("text_colors", {}).items():
        css_vars_string += f"    --{section.replace('_', '-')}-text-default: {colors.get('default', '#000000')};\n"
        css_vars_string += f"    --{section.replace('_', '-')}-text-heading: {colors.get('heading', '#000000')};\n"
    # Abstände, Fonts, Radius (aus defaults)
    css_vars_string += "    --spacing-section-large: 100px;\n"
    css_vars_string += "    --spacing-section-medium: 60px;\n"
    css_vars_string += "    --border-radius-card: 15px;\n"
    css_vars_string += "    --font-size-h1: 3.5rem;\n"
    css_vars_string += "    --font-size-h2: 2.8rem;\n"
    css_vars_string += "    --font-size-body: 1rem;\n"
    css_vars_string += "}\n"
    css_vars_string += "@media (max-width: 768px) { :root { --font-size-h1: 2.5rem; --font-size-h2: 2.2rem; --spacing-section-large: 60px; } }\n"
    css_vars_string = f"<style>\n{css_vars_string}</style>\n"

    # HTML aufbauen
    full_html = ""
    component_styles = []
    header_path = COMPONENTS_DIR / "technik_header.html"
    if header_path.exists():
        header_html = header_path.read_text(encoding='utf-8')
        header_html = re.sub(r'<style>.*?</style>', '{{GENERATED_STYLE_BLOCK}}', header_html, flags=re.DOTALL)
        header_html = re.sub(r'<body([^>]*)>', lambda m: f'<body{m.group(1)} class="{{theme_classes}}" >' if 'class' not in m.group(1) else m.group(0).replace('class="', 'class="{{theme_classes}} ', 1), header_html)
        full_html += header_html + "\n"

    for item in sorted(layout_plan, key=lambda x: int(x.get('order', 0))):
        component_name = item['component']
        component_path = COMPONENTS_DIR / f"{component_name}.html"
        if not component_path.exists():
            continue
        component_html = component_path.read_text(encoding='utf-8')

        # Styles extrahieren
        style_matches = re.findall(r'<style>.*?</style>', component_html, re.DOTALL)
        component_styles.extend(style_matches)
        component_html = re.sub(r'<style>.*?</style>', '', component_html, flags=re.DOTALL)

        # Style-Klasse
        component_style_class = style_data.get("styles", {}).get(component_name, {}).get("class", "")
        if component_style_class:
            component_html = re.sub(r'<section class="([^"]*)">', f'<section class="\\1 {component_style_class}">', component_html, 1)

        # Listen verarbeiten
        instance_data = content_data.get("page_content", {}).get(component_name, [])[component_counters[component_name] - 1]
        for key, list_data in instance_data.items():
            if isinstance(list_data, list):
                list_marker = f"{component_name}.{key}"
                pattern = re.compile(rf'<!-- BEGIN_LIST_ITEM:{re.escape(list_marker)} -->(.*?)<!-- END_LIST_ITEM:{re.escape(list_marker)} -->', re.DOTALL)
                match = pattern.search(component_html)
                if match:
                    item_template = match.group(1)
                    generated_items_html = ""
                    for i, list_item in enumerate(list_data):
                        item_html = item_template
                        for sub_key, sub_data in list_item.items():
                            sub_value = sub_data.get('value') or sub_data.get('example_value') or sub_data.get('description', "") or final_mapping.get(f"{component_name}.{key}[{i}].{sub_key}", "")
                            item_html = item_html.replace(f"{{{{{sub_key}}}}}", str(sub_value))
                        generated_items_html += item_html
                    component_html = pattern.sub(generated_items_html, component_html)

        full_html += component_html + "\n"

    # Footer
    footer_path = COMPONENTS_DIR / "footer_section.html"
    if footer_path.exists():
        footer_html = footer_path.read_text(encoding='utf-8')
        style_matches = re.findall(r'<style>.*?</style>', footer_html, re.DOTALL)
        component_styles.extend(style_matches)
        footer_html = re.sub(r'<style>.*?</style>', '', footer_html, flags=re.DOTALL)
        full_html += footer_html + "\n"
    else:
        full_html += "</body>\n</html>"

    # Styles konsolidieren
    final_mapping['GENERATED_STYLE_BLOCK'] = css_vars_string + "\n".join(component_styles)
    final_mapping['theme_classes'] = style_data.get("theme_classes", "classic")

    # Ersetzung
    final_html = replace_placeholders(full_html, final_mapping)

    # Speichern
    output_path = OUTPUT_DIR / f"{project_name}_{style_name}.html"
    output_path.write_text(final_html, encoding='utf-8')
    print(f"   - ✅ Website generiert: {output_path}")

def main():
    print("--- STARTING HTML GENERATOR V20.0 ---")
    # Aufräum-Code (wie zuvor)

    placeholder_assets = load_json(COMPONENTS_DIR / "_placeholder_assets.json")
    global_defaults = load_json(COMPONENTS_DIR / "_defaults.json")

    projects_to_process = [d for d in CONTENT_DIR.iterdir() if d.is_dir() and d.name not in ["processed_contents_archives", "proceed_contents_archives"]]
    for project_dir in projects_to_process:
        project_name = project_dir.name
        print(f"🚀 Verarbeite Projekt: {project_name}")
        layout_file = project_dir / "layout_extended_v2.csv"
        if not layout_file.exists(): continue
        layout_plan = [row for row in csv.DictReader(layout_file.open(encoding='utf-8')) if row.get('enabled', 'FALSE').upper() == 'TRUE']
        for content_file in project_dir.glob("project_template_Stufe02_Styled_*.json"):
            content_data = load_json(content_file)
            if not content_data: continue
            style_name_match = re.search(r"_Styled_(.+?)_\d+", content_file.name)
            if not style_name_match: continue
            style_name = style_name_match.group(1)
            generate_site_for_style(project_dir, style_name, content_data, layout_plan, placeholder_assets, global_defaults)
        new_name = f"processed_{project_name}_{datetime.now().strftime('%Y%m%d')}"
        project_dir.rename(project_dir.parent / new_name)
        print(f"   - ✅ Markiert als: '{new_name}'")
        print("-" * 50)

if __name__ == "__main__":
    defaults_path = COMPONENTS_DIR / "_defaults.json"
    if not defaults_path.exists():
        defaults = {
            "identity": {"company_name": "Ihre Firma AG"},
            "design": {
                "logo": {"url": "", "favicon_url": "/favicon.ico"},
                "branding": {
                    "primary_color": "#FF5733",
                    "secondary_color": "#C70039",
                    "text_color": "#000000",
                    "font_family": "Arial, sans-serif",
                    "accent_color": "#900C3F",
                    "text_on_primary": "#FFFFFF",
                    "text_on_secondary": "#FFFFFF",
                    "benefits_gradient": {"css_value": "linear-gradient(to right, #FF5733, #C70039)"}
                }
            },
            "links": {"career_page_url": "#", "application_form_url": "#", "imprint_url": "#", "privacy_url": "#", "contact_url": "#"},
            "labels": {"career_button_text": "Offene Stellen", "application_button_text": "Initiativbewerbung", "imprint_text": "Impressum", "privacy_text": "Datenschutz", "contact_text": "Kontakt"},
            "project_config": {"canonical_url": "#"},
            "meta_data": {"page_title": "Karriere bei {{identity.company_name}}", "meta_description": "Entdecken Sie Karrieremöglichkeiten bei {{identity.company_name}}."},
            "integrations": {"meta_pixel_id": "1234567890", "tracking_script_url": ""},
            "hero_section": {"headline": "Gestalte die Zukunft mit uns!", "subheadline": "Werde Teil eines innovativen Teams.", "description": "Entdecke deine Karrierechancen.", "image_url": "", "image_alt_text": "Team in Aktion"},
            "culture_section": {"headline": "Unsere Kultur: Zusammen unschlagbar", "description": "Wir leben Teamarbeit und Innovation.", "image_url": "", "image_alt_text": "Kultur-Bild", "values_list": [{"title": "Zusammenhalt", "text": "Hand in Hand.", "icon": "🤝"}, {"title": "Innovation", "text": "Kreative Ideen.", "icon": "💡"}, {"title": "Respekt", "text": "Vielfalt schätzen.", "icon": "🙌"}]},
            "team_section": {"headline": "Unser Team", "description": "Lerne uns kennen.", "testimonial_quote": "Toll hier zu arbeiten!", "testimonial_author": "Anna Müller", "testimonial_role": "Entwicklerin", "image_url": "", "image_alt_text": "Team-Foto"},
            "diversity_section": {"headline": "Vielfalt & Inklusion", "description": "Wir feiern Unterschiede.", "image_url": "", "image_alt_text": "Vielfältiges Team"},
            "stolz_section": {"headline": "Worauf wir stolz sind", "description": "Unsere Erfolge.", "highlights_list": [{"title": "Projekt1", "text": "Erfolgreich umgesetzt."}, {"title": "Projekt2", "text": "Innovativ gelöst."}]},
            "story_telling_section": {"headline": "Unsere Geschichten", "description": "Alltags-Erlebnisse.", "image_url": "", "image_alt_text": "Geschichte-Bild"},
            "location_section": {"headline": "Unsere Standorte", "description": "Wo wir sind.", "map_url": "", "image_alt_text": "Standort-Karte"},
            "benefits_section": {"headline": "Deine Vorteile", "description": "Was wir bieten.", "benefits_list": [{"title": "Flexzeit", "text": "Flexible Stunden.", "icon": "⏰"}, {"title": "Weiterbildung", "text": "Lernchancen.", "icon": "📚"}, {"title": "Events", "text": "Team-Aktivitäten.", "icon": "🎉"}]},
            "career_cta_section": {"headline": "Starte jetzt!", "description": "Bewerbe dich.", "career_button_text": "Offene Stellen", "application_button_text": "Bewerbung", "career_page_url": "#", "application_form_url": "#"},
            "footer_section": {"copyright_text": "© 2025 {{identity.company_name}}"},
            "values_section": {"headline": "Unsere Werte", "values_list": [{"title": "Integrität", "text": "Ehrlichkeit zählt.", "icon": "🏅"}, {"title": "Innovation", "text": "Vorantreiben.", "icon": "🚀"}, {"title": "Teamgeist", "text": "Zusammen stark.", "icon": "👥"}]},
            "navigation_section": {"headline": "Navigation", "nav_items": [{"label": "Home", "url": "#"}, {"label": "Über uns", "url": "#"}]},
            "logo_header_section": {"url": "", "company_name": "{{identity.company_name}}"},
            # Füge Defaults für alle anderen Module hinzu, basierend auf JSON- und HTML-Platzhaltern
        }
        defaults_path.write_text(json.dumps(defaults, indent=2))
    main()
