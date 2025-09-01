### README: Vorlagen-Generierung im CompanyCultureHub-Generator

**Version: 1.0**  
**Datum: 31. August 2025**  
**Autor: Grok (basierend auf Diskussionen)**

Dieses Dokument beschreibt den Prozess der Vorlagen-Generierung im Repo 2 (`companyculturehub-generator-v2`). Es umfasst das Skript `Content_template_generator_nach_modulupdates_v07.py`, die verwendeten Hilfsdateien und wie das System skalierbar ist. Das Ziel ist, dass du bei Änderungen (z. B. neuen Modulen) schnell nachschlagen kannst, was zu tun ist. Der Prozess ist dynamisch: Neue Platzhalter werden automatisch in Hilfsdateien ergänzt, ohne dass du den Code anpassen musst.

#### 1. Überblick über den Prozess
- **Ziel**: Das Skript scannt die HTML-Module in `templates/components/`, extrahiert Platzhalter (`{{placeholder}}`) und generiert eine JSON-Vorlage (`content_template_YYYYMMDD_HHMMSS.json` in `content_template_nach_update_modules/`). Diese Vorlage dient als Basis für:
  - Inhalte-Erzeugung (z. B. via LLM oder manueller Edit).
  - Interpreter-Schicht (Injektion von Farben, Styling aus Repo 1).
  - HTML-Generator (z. B. `generator_v_fullpower.py`, der die JSON in eine komplette HTML-Seite umwandelt).
- **Schlüsselprinzipien**:
  - **Dynamik**: Globale Platzhalter (z. B. `{{hero_section.headline}}`) aus `global_variables.csv`, lokale Platzhalter (z. B. `{{headline}}`) aus `local_variables.csv`. Fehlende werden automatisch mit Defaults ("BITTE HIER WERT ERGÄNZEN" oder "Beispielwert für {key}") ergänzt.
  - **Skalierbarkeit**: Bei neuen Modulen oder Platzhaltern wird die CSV aktualisiert – kein Code-Change nötig.
  - **Integration**: Die Vorlage ist "leer" (mit Defaults), wird dann mit Inhalten/Farben "geimpft" und zu HTML generiert.
- **Abhängigkeiten**: Python 3.x, Bibliotheken: csv, json, re, pathlib, datetime, logging (alle standardmäßig verfügbar).

#### 2. Ordnerstruktur und Dateien
- **Eingaben**:
  - `content_template_new_project/layout_extended_v2.csv`: Definiert enabled Komponenten, Reihenfolge (`order`), Constraints (`min_count`, `max_count`), Styling (`styling_default`).
    - Beispiel: `order,component,data_source,enabled,...`
    - Ändern: Aktiviere neue Module mit `enabled=TRUE`.
  - `templates/components/global_variables.csv`: Globale Platzhalter (z. B. `key: hero_section.headline, value: BITTE HIER WERT ERGÄNZEN`).
    - Wird automatisch aktualisiert.
  - `templates/components/local_variables.csv`: Lokale Platzhalter pro Komponente (z. B. `component: hero_section, key: headline, value: Eine aussagekräftige Überschrift`).
    - Wird automatisch aktualisiert.
  - `templates/components/*.html`: Die Module (z. B. `hero_section.html`).
- **Ausgaben**:
  - `content_template_nach_update_modules/content_template_YYYYMMDD_HHMMSS.json`: Die generierte Vorlage.
  - `content_generator.log`: Log-Datei für Debugging.

#### 3. Wie das Skript funktioniert (Schritt-für-Schritt)
1. **Laden der Dateien**: Layout-CSV, globale/lokale Variablen-CSV.
2. **Verarbeiten jeder enabled Komponente** (aus Layout-CSV):
   - Lade HTML-Modul (z. B. `hero_section.html`).
   - Extrahiere Platzhalter mit Regex (`{{placeholder}}`).
   - Füge Styling aus CSV hinzu (z. B. `styling_default: "fade-up"`).
   - Verarbeite lokale Platzhalter aus `local_variables.csv` mit Defaults.
   - Verarbeite Listen (z. B. `BEGIN_LIST_ITEM:benefits_section.benefits_list`) als nested Arrays.
   - Sammle globale Platzhalter und aktualisiere `global_variables.csv` bei Fehlern.
   - Sammle neue lokale Platzhalter und aktualisiere `local_variables.csv` bei Fehlern.
   - Validierung: Prüfe, ob alle Platzhalter abgedeckt sind.
3. **Speichern**: JSON-Vorlage erzeugen.

#### 4. Wie neue Module hinzufügen
Siehe separate Sektion unten ("README: Aufbau von Modulen").

#### 5. Ausführung des Skripts
- **Voraussetzungen**: Stelle sicher, dass `layout_extended_v2.csv`, `global_variables.csv` und `local_variables.csv` existieren. Bei Fehlen werden sie erstellt.
- **Ausführen**: `python scripts/Content_template_generator_nach_modulupdates_v07.py`.
- **Output**: Neue JSON in `content_template_nach_update_modules/`.
- **Debugging**: Schau in `content_generator.log` (z. B. "Unabgedeckte Platzhalter: ..." bei Fehlern).

#### 6. Integration mit Interpreter-Schicht und Generator
- **Interpreter-Schicht**: Injiziert Farben/Styling aus Repo 1 (z. B. `design.branding.primary_color`) in `global_settings` der JSON (z. B. String-Replace oder JSON-Update).
- **Generator (z. B. `generator_v_fullpower.py`)**: Liest die "geimpfte" JSON, lädt Module in Order aus Layout-CSV, ersetzt Platzhalter, iteriert Listen und erzeugt HTML.
- **Vollständiger Workflow**: Modul-Änderung → Skript ausführen → Vorlage generieren → Inhalte erzeugen (z. B. LLM) → Interpreter injizieren → Generator zu HTML.

#### 7. Troubleshooting
- **Leere Arrays**: Wenn Platzhalter fehlen, prüfe `local_variables.csv` und füge manuell hinzu.
- **Fehlende CSV**: Das Skript erstellt sie automatisch.
- **Neue Platzhalter**: Wird automatisch in CSV geschrieben – editiere Defaults später.
- **Update**: Bei Änderungen: Skript ausführen, um Vorlage zu aktualisieren.

#### 8. Zukunftsideen
- Automatisiere Interpreter/Generator in einem Pipeline-Skript.
- Erweitere für Multi-Vorlagen (z. B. per Template-ID in CSV).