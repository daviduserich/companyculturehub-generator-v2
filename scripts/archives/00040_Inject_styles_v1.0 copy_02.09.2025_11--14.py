import json
import os
import argparse

def inject_styles(project_name):
    """Inject styles into content_template_max.json and generate content_color_injected_<variant>.json."""
    project_dir = f"content/{project_name}"
    template_file = f"{project_dir}/content_template_max.json"
    colors_file = f"{project_dir}/interpreted_colors.json"
    text_colors_file = f"{project_dir}/interpreted_text_colors.json"
    config_file = f"{project_dir}/customer_style_config.json"

    # Read inputs
    try:
        with open(template_file, 'r') as f:
            template = json.load(f)
        with open(colors_file, 'r') as f:
            colors = json.load(f)["colors"]
        with open(text_colors_file, 'r') as f:
            text_colors = json.load(f)["text_colors"]
        with open(config_file, 'r') as f:
            config = json.load(f)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Error: {e.filename} not found.")

    # Get preferred variants
    preferred_variants = config.get("preferred_variants", ["classic", "stylish", "classic_accents", "hyper_stylish"])

    # Process each variant
    for variant in preferred_variants:
        styles_file = f"{project_dir}/interpreted_styles_{variant}.json"
        try:
            with open(styles_file, 'r') as f:
                styles = json.load(f)["styles"]
        except FileNotFoundError:
            continue

        # Create output template
        output = template.copy()
        output["global_settings"] = output.get("global_settings", {})
        output["global_settings"]["design"] = output["global_settings"].get("design", {})
        output["global_settings"]["design"]["branding"] = {
            "primary_color": colors["primary_color"],
            "secondary_color": colors["secondary_color"],
            "accent_color": colors["accent_color"],
            "gradient_type": colors["gradient_type"]
        }
        output["global_settings"]["text_colors"] = text_colors

        # Inject styles into page_content
        for component, style in styles.items():
            if component not in output["page_content"]:
                output["page_content"][component] = []
            style_entries = []
            if "class" in style:
                style_entries.append({"name": "styling_default", "value": style["class"]})
            if "background_color" in style:
                style_entries.append({"name": "background_color", "value": style["background_color"]})
            if "card_style" in style:
                style_entries.append({"name": "card_style", "value": style["card_style"]})
            if "image_frame" in style:
                style_entries.append({"name": "image_frame", "value": style["image_frame"]})
            if "button_style" in style:
                style_entries.append({"name": "button_style", "value": style["button_style"]})
            output["page_content"][component].extend(style_entries)

        # Write output
        output_file = f"{project_dir}/content_color_injected_{variant}.json"
        with open(output_file, 'w') as f:
            json.dump(output, f, indent=2)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Inject styles into template for a project.")
    parser.add_argument("--project", required=True, help="Project name (e.g., content_template_new_project)")
    args = parser.parse_args()
    inject_styles(args.project)