import json
import os
import argparse
import colorsys

def hex_to_rgb(hex_color):
    """Convert hex color to RGB tuple."""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hsv(r, g, b):
    """Convert RGB to HSV."""
    r, g, b = r / 255.0, g / 255.0, b / 255.0
    return colorsys.rgb_to_hsv(r, g, b)

def interpret_colors(project_name):
    """Interpret colors from color_definitions.json and generate interpreted_colors.json."""
    project_dir = f"content/{project_name}"
    input_file = f"{project_dir}/color_definitions.json"
    output_file = f"{project_dir}/interpreted_colors.json"

    # Read input
    try:
        with open(input_file, 'r') as f:
            color_data = json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Error: {input_file} not found.")

    # Extract colors
    branding = color_data.get("design", {}).get("branding", {})
    primary_color = branding.get("primary_color", "#FF5733")
    secondary_color = branding.get("secondary_color", "#C70039")
    accent_color = branding.get("accent_color", "#900C3F")

    # Calculate HSV for primary_color
    rgb = hex_to_rgb(primary_color)
    h, s, v = rgb_to_hsv(*rgb)
    gradient_type = "vertical" if v < 0.3 else "horizontal"
    style_recommendation = "stylish" if s > 0.5 else "classic"

    # Generate image frame gradient
    image_frame_gradient = f"linear-gradient(to top, {accent_color}, transparent)"

    # Output
    output = {
        "colors": {
            "primary_color": primary_color,
            "secondary_color": secondary_color,
            "accent_color": accent_color,
            "gradient_type": gradient_type,
            "style_recommendation": style_recommendation,
            "image_frame_gradient": image_frame_gradient,
            "accent_color_rgb": list(rgb)
        }
    }

    # Ensure project directory exists
    os.makedirs(project_dir, exist_ok=True)

    # Write output
    with open(output_file, 'w') as f:
        json.dump(output, f, indent=2)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Interpret colors for a project.")
    parser.add_argument("--project", required=True, help="Project name (e.g., content_template_new_project)")
    args = parser.parse_args()
    interpret_colors(args.project)