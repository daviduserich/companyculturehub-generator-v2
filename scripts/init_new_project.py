#!/usr/bin/env python3
"""
Helfer-Skript zum Erstellen eines neuen Projekt-Ordners im 'content'-Verzeichnis.
"""
import shutil
from pathlib import Path

def main():
    """
    Kopiert den Vorlagen-Ordner nach 'content/' und benennt ihn um.
    """
    try:
        base_dir = Path(__file__).resolve().parent.parent
        
        # Pfade definieren
        template_dir = base_dir / "content_template_new_project"
        content_dir = base_dir / "content"
        new_project_name = "new-project-bitte_befuellen"
        destination_dir = content_dir / new_project_name

        print("🚀 Starte Initialisierung für ein neues Projekt...")
        print(f"   - Vorlage: '{template_dir.name}'")
        print(f"   - Ziel:    'content/{new_project_name}'")

        # Prüfen, ob die Vorlage existiert
        if not template_dir.is_dir():
            print(f"\n❌ FEHLER: Der Vorlagen-Ordner '{template_dir.name}' wurde nicht gefunden.")
            return

        # Prüfen, ob das Ziel bereits existiert, um Überschreiben zu verhindern
        if destination_dir.exists():
            print(f"\n⚠️ WARNUNG: Ein Ordner mit dem Namen '{new_project_name}' existiert bereits im 'content'-Verzeichnis.")
            print("   Prozess abgebrochen, um Datenverlust zu vermeiden.")
            return
            
        # Den gesamten Ordner-Baum kopieren
        shutil.copytree(template_dir, destination_dir)

        print(f"\n✅ Erfolgreich! Der Ordner '{new_project_name}' wurde im 'content'-Verzeichnis erstellt.")
        print("   Bitte benenne den Ordner um und passe die 'content.json' an.")

    except Exception as e:
        print(f"\n❌ Ein unerwarteter Fehler ist aufgetreten: {e}")

if __name__ == "__main__":
    main()
