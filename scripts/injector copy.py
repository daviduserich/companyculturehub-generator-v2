#!/usr/bin/env python3
"""
Color & Style Injector v1.1
Merges color and style definitions from a source JSON into a target
content.json, creating a new, "injected" file.
"""
import json
import glob
from pathlib import Path
import argparse

def find_color_definitions_file(project_dir: Path) -> Path | None:
    """Finds a file containing 'color_definitions.json' in its name."""
    # Sucht nach jeder JSON-Datei, deren Name 'color_definitions' enthält
    search_pattern = f"{project_dir}/*color_definitions.json"
    files = glob.glob(search_pattern)
    if not files:
        return None
    # Nimm die erste gefundene Datei
    return Path(files[0])

def inject_data(project_name: str, base_dir: Path):
    """Injects colors and styles for a specific project."""
    print(f"💉 Starting injection for project: {project_name}")
    
    content_dir = base_dir / "content"
    project_dir = content_dir / project_name

    # 1. Finde die beiden benötigten Dateien
    content_file = project_dir / "content.json"
    color_file = find_color_definitions_file(project_dir)

    if not content_file.exists():
        print(f"   - ❌ ERROR: 'content.json' not found. Skipping.")
        return
    
    if not color_file:
        print(f"   - 🟡 SKIPPING: No '*color_definitions.json' file found in '{project_dir}'.")
        return

    # 2. Lade die Inhalte
    try:
        with content_file.open('r', encoding='utf-8') as f:
            content_data = json.load(f)
        
        with color_file.open('r', encoding='utf-8') as f:
            # Wir laden die gesamte 'design'-Sektion aus der Quelldatei
            injection_data = json.load(f)
            if 'design' not in injection_data:
                 raise ValueError("Source file must contain a 'design' object.")
            new_design_data = injection_data['design']

    except Exception as e:
        print(f"   - ❌ ERROR: Could not read or parse JSON files. {e}")
        return

    # 3. Führe die "Impfung" durch
    # Wir stellen sicher, dass die global_settings und design Objekte existieren
    if 'global_settings' not in content_data:
        content_data['global_settings'] = {}
    
    # Wir ersetzen den gesamten 'design'-Block. Das ist sauberer,
    # da unser Farb-Repo jetzt die komplette Wahrheit über das Design kennt.
    content_data['global_settings']['design'] = new_design_data
    print("   - ✅ 'design' block successfully replaced with new data.")

    # 4. Speichere die neue, geimpfte Datei
    output_filename = "content_color_injected.json"
    output_path = project_dir / output_filename
    try:
        with output_path.open('w', encoding='utf-8') as f:
            json.dump(content_data, f, indent=2, ensure_ascii=False)
        print(f"   - ✅ Successfully created injected file: {output_filename}")
    except Exception as e:
        print(f"   - ❌ ERROR: Could not write injected file. {e}")

def main():
    """Main function to run the injector."""
    # Annahme: Das Skript liegt in einem 'scripts' Ordner
    base_dir = Path(__file__).resolve().parent.parent
    content_dir = base_dir / "content"
    
    parser = argparse.ArgumentParser(description='Color & Style Injector for CompanyCultureHub')
    parser.add_argument('--project', type=str, help='Inject a specific project (folder name).')
    parser.add_argument('--all', action='store_true', help='Inject all projects in the content folder.')
    args = parser.parse_args()

    if args.project:
        inject_data(args.project, base_dir)
    elif args.all:
        print("--- STARTING INJECTION FOR ALL PROJECTS ---")
        for project_dir in content_dir.iterdir():
            if project_dir.is_dir():
                inject_data(project_dir.name, base_dir)
        print("-" * 40)
    else:
        print("Please specify a project with --project <name> or use --all to process all projects.")

if __name__ == "__main__":
    main()
