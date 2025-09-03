import json
import os
import argparse
from datetime import datetime
import copy
from pathlib import Path

def find_newest_file(directory, pattern):
    """Findet die neueste Datei in einem Ordner, die einem Muster entspricht."""
    files = list(directory.glob(pattern))
    if not files:
        return None
    return max(files, key=lambda f: f.stat().st_mtime)

def inject_styles(project_name):
    """
    Liest das neueste 'Stufe01'-Template, injiziert die vier Style-Varianten
    und erzeugt für jede Variante eine 'Stufe02'-Datei.
    """
    print(f"--- STARTING INJECTOR V2.0 für Projekt: {project_name} ---")
    
    # Pfade mit pathlib definieren für Robustheit
    base_dir = Path(__file__).resolve().parent.parent
    project_dir = base_dir / "content" / project_name

    # Finde die neueste Stufe01-Template-Datei
    template_file = find_newest_file(project_dir, "project_template_Stufe01_Anleitung_*.json")
    if not template_file:
        raise FileNotFoundError(f"Error: Keine 'project_template_Stufe01_...' Datei in {project_dir} gefunden.")
    
    print(f"   - ℹ️ Verarbeite Template: {template_file.name}")

    # Lese die Basis-Dateien dynamisch
    colors_file = find_newest_file(project_dir, "interpreted_colors*.json")
    text_colors_file = find_newest_file(project_dir, "interpreted_text_colors*.json")

    # Prüfe, ob alle notwendigen Dateien gefunden wurden
    if not all([template_file, colors_file, text_colors_file]):
        missing = [name for name, var in [("Stufe01_Template", template_file), ("interpreted_colors", colors_file), ("interpreted_text_colors", text_colors_file)] if not var]
        print(f"   - ❌ FEHLER: Folgende Input-Dateien konnten nicht gefunden werden: {', '.join(missing)}")
        return

    try:
        with template_file.open('r', encoding='utf-8') as f:
            base_template = json.load(f)
    except json.JSONDecodeError as e:
        print(f"   - ❌ FEHLER beim Parsen von {template_file.name}: {e}")
        return


    # Verarbeite jede der vier Styling-Varianten
    variants = ["classic", "classic_accents", "stylish", "hyper_stylish"]
    for variant in variants:
        print(f"   - 💉 Injiziere Style-Variante: '{variant}'")
        
        styles_file = find_newest_file(project_dir, f"interpreted_styles_{variant}*.json")
        if not styles_file:
            print(f"   - ⚠️ WARNUNG: Style-Datei für '{variant}' nicht gefunden. Überspringe.")
            continue

        try:
            with styles_file.open('r', encoding='utf-8') as f:
                # Annahme: Die relevanten Daten sind unter einem Top-Level-Key, z.B. "styles"
                styles_data = json.load(f).get("styles", {})
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"   - ❌ FEHLER beim Laden der Style-Datei {styles_file.name}: {e}")
            continue

        # Erstelle eine tiefe Kopie für jede Variante, um Seiteneffekte zu vermeiden
        output_template = copy.deepcopy(base_template)

        # Füge die Style-Informationen in jede Instanz jeder Komponente ein
        if "page_content" in output_template:
            for component_name, instances in output_template["page_content"].items():
                if component_name in styles_data:
                    component_style = styles_data[component_name]
                    
                    # Iteriere durch jede Instanz der Komponente
                    for instance in instances:
                        # Füge die Style-Werte direkt in das Instanz-Objekt ein
                        if "class" in component_style:
                            instance["styling_default"] = {"description": "CSS-Klasse für das Haupt-Styling.", "value": component_style["class"]}
                        if "background_color" in component_style:
                            instance["background_color"] = {"description": "Hintergrundfarbe der Sektion.", "value": component_style["background_color"]}
                        if "card_style" in component_style:
                            instance["card_style"] = {"description": "Styling-Typ für Karten innerhalb der Sektion.", "value": component_style["card_style"]}
                        if "image_frame" in component_style:
                            instance["image_frame"] = {"description": "Rahmen-Stil für Bilder.", "value": component_style["image_frame"]}
                        if "button_style" in component_style:
                            instance["button_style"] = {"description": "Styling für Buttons.", "value": component_style["button_style"]}
        
        # Update der Metadaten
        output_template["metadata"]["generator_version"] = "v2.0-structured-injector"
        output_template["metadata"]["injected_style"] = variant

        # Schreibe die neue Stufe-02-Datei
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_filename = f"project_template_Stufe02_Styled_{variant}_{timestamp}.json"
        output_path = project_dir / output_filename
        
        with output_path.open('w', encoding='utf-8') as f:
            json.dump(output_template, f, indent=2, ensure_ascii=False)
        
        print(f"   - ✅ '{variant}' erfolgreich injiziert. Output: {output_path.name}")

    print("\n--- INJECTOR V2.0 erfolgreich abgeschlossen. ---")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Inject styles into a project's content template.")
    # Das Argument ist jetzt der Projekt-Ordnername, nicht der ganze Pfad
    parser.add_argument("--project", required=True, help="Project name (e.g., DEF_88)")
    args = parser.parse_args()
    try:
        inject_styles(args.project)
    except Exception as e:
        print(f"\nEin unerwarteter Fehler ist aufgetreten: {e}")
