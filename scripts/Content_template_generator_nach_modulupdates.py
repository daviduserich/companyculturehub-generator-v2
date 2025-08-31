import csv
import json
import re
from pathlib import Path
from datetime import datetime


def generate_content_template(csv_path, templates_dir, output_path):
    # Lade CSV
    with open(csv_path, 'r', encoding='utf-8') as f:
        layout = list(csv.DictReader(f))
    
    # Basis-Struktur
    content = {
        "metadata": {
            "generated_at": datetime.now().isoformat(),
            "generator_version": "v2.0",
            "csv_source": str(csv_path)
        },
        "global_settings": {
            "project_config": {"project_id": "example_project_v1", "primary_domain": "example.culture.localhost", "canonical_url": "https://example.culture.localhost/employer-branding"},
            "identity": {"company_name": "Example AG", "company_slogan": "Innovation trifft Teamgeist"},
            "links": {"imprint_url": "https://example.com/impressum", "privacy_url": "https://example.com/datenschutz", "contact_url": "https://example.com/kontakt", "career_page_url": "https://example.com/karriere", "application_form_url": "mailto:karriere@example.com"},
            "design": {"branding": {"primary_color": "#4A5568", "secondary_color": "#2c3e50", "text_color": "#333333", "accent_color": "#3182CE", "text_on_primary": "#FFFFFF", "text_on_secondary": "#FFFFFF", "benefits_gradient": {"type": "dynamic_fallback", "css_value": "linear-gradient(135deg, #4A5568, #3182CE)"}, "font_family": "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif"}, "logo": {"url": "assets/images/example_logo.svg", "favicon_url": "assets/images/example_favicon.png"}},
            "labels": {"imprint_text": "Impressum", "privacy_text": "Datenschutz", "contact_text": "Kontakt", "career_button_text": "Aktuelle Stellen", "application_button_text": "Initiativbewerbung"},
            "integrations": {"meta_pixel_id": "YOUR_META_PIXEL_ID_HERE", "tracking_script_url": ""}
        },
        "page_content": {}
    }
    
    # Regex für Platzhalter: {{...}}
    placeholder_pattern = re.compile(r'\{\{([^}]+)\}\}')
    
    for row in layout:
        component = row['component']
        if not component:
            continue
        
        # Standard-Werte aus CSV
        max_count = int(row['max_count']) if row['max_count'] else 1
        
        # HTML-Template scannen
        html_path = templates_dir / f"{component}.html"
        section_content = []
        
        if html_path.exists():
            html_content = html_path.read_text(encoding='utf-8')
            is_list = 'BEGIN_LIST_ITEM' in html_content
            
            placeholders = set(placeholder_pattern.findall(html_content))
            placeholders = [p.strip() for p in placeholders if not p.startswith(('BEGIN_LIST_ITEM', 'END_LIST_ITEM'))]
            
            # Entferne Pfad-Prefixe (z. B. "benefits_section." aus {{benefits_section.headline}})
            clean_placeholders = []
            for p in placeholders:
                parts = p.split('.')
                clean_placeholders.append(parts[-1] if len(parts) > 1 else p)
            
            # Initialize list_name
            list_name = None
            
            # Handle List-Items
            if is_list:
                list_name = next((p.split('.')[-1] for p in placeholders if '.list' in p.lower()), None)
                if list_name:
                    section_content.append({
                        "id": f"EB-{component.capitalize()}-C2",
                        "name": list_name,
                        "type": "list",
                        "value": [
                            {"id": "item1", "elements": [
                                {"name": "icon", "value": "🌟" if component in ['values_section', 'culture_section', 'benefits_section'] else ""},
                                {"name": "title", "value": f"Beispiel-Titel 1 für {component}"},
                                {"name": "text", "value": f"Beispiel-Text 1 für {component}"}
                            ]},
                            {"id": "item2", "elements": [
                                {"name": "icon", "value": "🚀" if component in ['values_section', 'culture_section', 'benefits_section'] else ""},
                                {"name": "title", "value": f"Beispiel-Titel 2 für {component}"},
                                {"name": "text", "value": f"Beispiel-Text 2 für {component}"}
                            ]}
                        ]
                    })
            
            # Handle Einzel-Elemente
            for p in clean_placeholders:
                if p not in ['icon', 'title', 'text'] and p != list_name:
                    value = f"Beispiel-{p} für {component}"
                    if p in ['image_url', 'map_url']:
                        value = f"assets/images/{component}_{p}.png"
                    elif p == 'image_alt_text':
                        value = f"Bild für {component}"
                    elif p == 'testimonial_author_name':
                        value = "Hans Muster"
                    elif p == 'testimonial_author_title':
                        value = "Beispiel-Position"
                    section_content.append({"id": f"EB-{component.capitalize()}-C1-{p}", "name": p, "value": value})
        
        else:
            # Default, falls kein HTML-Template
            section_content = [{"id": f"EB-{component.capitalize()}-C1-E1", "name": "placeholder", "value": f"Content for {component}"}]
        
        # Handle Multi-Instanzen (z. B. story_telling_section)
        if max_count > 1 and component == 'story_telling_section':
            section_content = [
                {"instance": i+1, "id": f"EB-{component.capitalize()}-{i+1}-C1-E1", "name": p, "value": f"Beispiel-{p} Instanz {i+1} für {component}"}
                for i in range(min(max_count, 2)) for p in clean_placeholders
            ]
        
        content["page_content"][component] = section_content
    
    # Speichere JSON
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(content, f, indent=2, ensure_ascii=False)
    print(f"Generated {output_path}")

# Usage
generate_content_template(
    csv_path='content_template_new_project/layout_extended_v2.csv',
    templates_dir=Path('templates/components'),
    output_path=f'content_template_nach_update_modules/content_template_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
)