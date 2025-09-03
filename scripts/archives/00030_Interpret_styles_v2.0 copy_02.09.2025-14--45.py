import json
import csv
import os
import argparse

def read_csv(file_path):
    """Read CSV file and return list of rows."""
    with open(file_path, 'r') as f:
        reader = csv.DictReader(f)
        return list(reader)


def calculate_contrast(bg_color, text_color):
    """Calculate WCAG contrast ratio (simplified)."""
    def luminance(color):
        r, g, b = [int(color.lstrip('#')[i:i+2], 16) / 255.0 for i in (0, 2, 4)]
        return 0.299 * r + 0.587 * g + 0.114 * b
    bg_lum = luminance(bg_color)
    text_lum = luminance(text_color)
    contrast = (max(bg_lum, text_lum) + 0.05) / (min(bg_lum, text_lum) + 0.05)
    return contrast

def interpret_styles(project_name):
    """Interpret styles and generate interpreted_styles_<variant>.json and interpreted_text_colors.json."""
    project_dir = f"content/{project_name}"
    colors_file = f"{project_dir}/interpreted_colors.json"
    layout_file = f"{project_dir}/layout_extended_v2.csv"
    style_modulator_file = "templates/components/style_modulator.json"
    config_file = f"{project_dir}/customer_style_config.json"

    # Read inputs
    try:
        with open(colors_file, 'r') as f:
            colors = json.load(f)["colors"]
        layout_data = read_csv(layout_file)
        with open(style_modulator_file, 'r') as f:
            style_modulator = json.load(f)
        with open(config_file, 'r') as f:
            config = json.load(f)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Error: {e.filename} not found.")


    # Read layout_rules.json
    with open(f"{project_dir}/layout_rules.json", 'r') as f:
        layout_rules = json.load(f)

    # Get preferred variants
    preferred_variants = config.get("preferred_variants", ["classic", "stylish", "classic_accents", "hyper_stylish"])

    # Process styles for each variant
    styles_output = {}
    text_colors = {}
    fixed_layouts = layout_rules.get("fixed_layouts", {})
    footer_bg = colors["primary_color"]  # Assume footer uses primary_color

    for variant in preferred_variants:
        styles = {}
        variant_styles = style_modulator["variants"].get(variant, {})
        alt_backgrounds = variant_styles.get("alternating_backgrounds", ["#FFFFFF", "#F5F5F5"])
        element_styles = variant_styles.get("element_styles", {})

        for row in layout_data:
            component = row["component"]
            order = int(row["order"])
            enabled = row["enabled"].lower() == "true"

            if not enabled:
                continue

            # Apply fixed layout if exists
            if component in fixed_layouts:
                style = fixed_layouts[component].copy()
                for key, value in style.items():
                    style[key] = value.replace("{{colors.gradient_type}}", colors["gradient_type"]).replace("{{colors.primary_color}}", colors["primary_color"]).replace("{{colors.secondary_color}}", colors["secondary_color"])
            else:
                # Alternating layouts
                is_last_before_footer = (order == max(int(r["order"]) for r in layout_data if r["enabled"].lower() == "true") and component != "footer")
                bg_index = 0 if order % 2 == 0 else 1
                bg_color = alt_backgrounds[bg_index]
                if is_last_before_footer and len([r for r in layout_data if r["enabled"].lower() == "true"]) % 2 == 1:
                    # Ungerade Anzahl: last module before footer
                    footer_lum = sum(hex_to_rgb(footer_bg)) / 3 / 255
                    if footer_lum > 0.5:  # Light footer
                        bg_color = "#FFFFFF" if variant in ["classic", "classic_accents"] else bg_color.replace("{{colors.accent_color_rgb}}", ",".join(map(str, colors["accent_color_rgb"])))

                style = {
                    "gradient_type": "none",
                    "background_color": bg_color,
                    "class": row["styling_default"],
                    "image_frame": element_styles.get("image_frame", {}).get("style", "none"),
                    "card_style": element_styles.get("card", {}).get("style", "none"),
                    "button_style": element_styles.get("button", {}).get("style", "none")
                }

            styles[component] = style

            # Calculate text colors
            bg_color = style["background_color"].replace("rgba({{colors.accent_color_rgb}}, 0.2)", f"#{colors['accent_color'][:7]}").replace("rgba({{colors.accent_color_rgb}}, 0.3)", f"#{colors['accent_color'][:7]}")
            default_color = "#000000" if calculate_contrast(bg_color, "#000000") > 4.5 else "#FFFFFF"
            heading_color = default_color
            if variant == "stylish" or variant == "hyper_stylish":
                if bg_color in ["#FFFFFF", "#F5F5F5"]:  # White or gray modules
                    heading_color = colors["accent_color"]
            elif variant == "classic_accents":
                heading_color = colors["accent_color"]

            text_colors[component] = {"default": default_color, "heading": heading_color}

        styles_output[variant] = {"styles": styles}

    # Write outputs
    os.makedirs(project_dir, exist_ok=True)
    for variant, data in styles_output.items():
        with open(f"{project_dir}/interpreted_styles_{variant}.json", 'w') as f:
            json.dump(data, f, indent=2)
    with open(f"{project_dir}/interpreted_text_colors.json", 'w') as f:
        json.dump({"text_colors": text_colors}, f, indent=2)

def hex_to_rgb(hex_color):
    """Convert hex color to RGB tuple."""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Interpret styles for a project.")
    parser.add_argument("--project", required=True, help="Project name (e.g., content_template_new_project)")
    args = parser.parse_args()
    interpret_styles(args.project)