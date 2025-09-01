### README: Aufbau von Modulen

**Version: 1.0**  
**Datum: 31. August 2025**  
**Autor: Grok (basierend auf Diskussionen)**

Dieses Dokument beschreibt den exakten Aufbau eines Moduls (HTML-Komponente in `templates/components/`). Das Ziel ist, dass du bei Hinzufügen eines neuen Moduls (z. B. `new_section.html`) genau weißt, wie es strukturiert werden muss, um mit dem Vorlagen-Generierungs-Skript, Interpreter-Schicht und Generator kompatibel zu sein. Modul sind eigenständig, modular und skalierbar – neue Platzhalter werden automatisch in `global_variables.csv` oder `local_variables.csv` ergänzt.

#### 1. Grundstruktur eines Moduls
- **Dateiname**: `component_name_section.html` oder `component_name.html` (z. B. `hero_section.html`). Das Skript sucht beides.
- **Inhalt**: HTML + CSS in `<section>`-Tag, mit Platzhaltern für Inhalte.
- **Platzhalter-Format**: `{{placeholder_name}}` für lokale (einfach) und `{{group.key}}` für globale.
- **Beispiel-Grundstruktur** (für ein einfaches Modul):
  ```html
  <!-- Modul-Name: Beschreibung -->
  <section class="modul-name">
      <div class="container">
          <h2>{{modul_name.headline}}</h2>  <!-- Globaler Platzhalter -->
          <p>{{description}}</p>  <!-- Lokaler Platzhalter -->
          <!-- BEGIN_LIST_ITEM:modul_name.list_name -->  <!-- Für Listen (optional) -->
          <div class="item">
              <div>{{icon}}</div>  <!-- Sub-Platzhalter -->
              <h3>{{title}}</h3>
              <p>{{text}}</p>
          </div>
          <!-- END_LIST_ITEM:modul_name.list_name -->
      </div>
  </section>

  <style>
      .modul-name { /* Basis-Stile */ }
      /* Varianten für Styling (z. B. aus Interpreter) */
      .bg-gradient .modul-name { background: var(--modul-gradient); }
      .card-glass .item { backdrop-filter: blur(10px); }
  </style>
  ```
- **Pflicht-Elemente**:
  - `<section class="component-name">`: Für CSS-Targeting.
  - Kommentar am Anfang: `<!-- Modul-Name: Beschreibung -->` (für Dokumentation).
- **Optionale Elemente**:
  - Listen: Mit `BEGIN_LIST_ITEM:group.list_name` und `END_LIST_ITEM`.
  - CSS: Basis + Varianten (z. B. `.bg-gradient`, `.card-glass`), mit Variablen für Interpreter (z. B. `--color-primary`).

#### 2. Platzhalter-Regeln
- **Lokale Platzhalter**: Einfach, ohne '.', z. B. `{{headline}}`, `{{description}}`. Für Listen: Sub-Platzhalter wie `{{icon}}` in `BEGIN_LIST_ITEM`.
  - Das Skript extrahiert sie automatisch und fügt zu `local_variables.csv` hinzu, wenn fehlend (mit "Beispielwert für {key}").
- **Globale Platzhalter**: Mit '.', z. B. `{{modul_name.headline}}`, `{{identity.company_name}}`. Werden in `global_variables.csv` ergänzt.
- **Defaults**: In CSV-Dateien definiert – editiere sie für benutzerdefinierte Defaults.
- **Styling**: Verwende CSS-Variablen (z. B. `--benefits-gradient`), die von Interpreter injiziert werden. Styling-Klassen (z. B. "fade-up") aus Layout-CSV.

#### 3. Hinzufügen eines neuen Moduls (Schritt-für-Schritt)
1. **Modul erstellen**: Schreibe `new_section.html` in `templates/components/`, mit obiger Struktur (Platzhalter, CSS).
2. **Layout aktualisieren**: Füge in `layout_extended_v2.csv` hinzu, z. B.:
   ```
   order,component,data_source,enabled,Must or Possibility,min_count,max_count,recommended_count,description,styling_default,position_constraints,integration_status
   70,new_section,new_section,TRUE,P,0,1,1,Neue Sektion.,glass,after:60 before:100,core
   ```
3. **Skript ausführen**: `python scripts/Content_template_generator_nach_modulupdates_v07.py`.
   - Das Skript extrahiert neue Platzhalter und aktualisiert `local_variables.csv` oder `global_variables.csv` (z. B. `new_section.headline, BITTE HIER WERT ERGÄNZEN`).
4. **Prüfen**: Schaue in die JSON – sie enthält `page_content["new_section"]` mit Defaults.
5. **Interpreter/Generator**: Die Vorlage ist bereit – Interpreter injiziert Farben, Generator baut HTML.

#### 4. Best Practices für Module
- **Konsistenz**: Verwende standardisierte Namen (z. B. `headline`, `description`, `image_url`).
- **Listen**: Immer mit `BEGIN_LIST_ITEM:group.list_name` (z. B. `new_section.items_list`).
- **CSS**: Basis-Stile + Varianten (z. B. `.bg-gradient`, `.card-shadow`) für Interpreter-Flexibilität.
- **Responsive**: Füge Media Queries hinzu (z. B. `@media (max-width: 768px)`).
- **Edge Cases**: Vermeide Duplikate; teste mit Generator, ob Platzhalter ersetzt werden.

#### 5. Troubleshooting
- **Fehlende Platzhalter**: Prüfe CSV-Dateien – editiere Defaults.
- **Inkonsistenz**: Stelle sicher, dass Platzhalter-Namen in Modulen mit CSV übereinstimmen.
- **Neues Modul nicht erkannt**: Überprüfe `enabled=TRUE` in Layout-CSV.
