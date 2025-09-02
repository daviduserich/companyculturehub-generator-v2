Vereinfachte Übersicht über Company Culture Hub Generator v2
Dieses Tool erstellt verschiedene Designvarianten (z. B. classic, stylish, classic_accents, hyper_stylish) für Arbeitgeber-Branding-Websites. Es verwendet modulare Konfigurationen für Farben, Stile und Layouts, um anpassbare HTML-Seiten zu generieren. Das System arbeitet in Schichten: Es verarbeitet Farben, Stile und Textfarben und fügt sie in eine Vorlage ein.
Verzeichnisstruktur

content/<project_name>/: Projektordner (z. B. content/florr99/). Hier liegen Eingabe- und Ausgabedateien.
Eingabedateien (im Ordner content/<project_name>/):

content_template_max.json: Basisstruktur und Inhalt des Projekts.
layout_extended_v2.csv: Definiert Reihenfolge, Komponenten und Standard-Styling.
color_definitions.json: Enthält Markenfarben (primär, sekundär, Akzent). Muss manuell hinzugefügt werden.
customer_style_config.json: Gibt an, welche Designvarianten erstellt werden.
layout_rules.json: Regeln für feste Layouts (kopiert aus content_template_new_project/).


Generierte Dateien (im Ordner content/<project_name>/):

interpreted_colors.json: Verarbeitete Farben, Farbverläufe und Stilvorschläge.
interpreted_styles_<variant>.json: Stile für jede Variante (z. B. interpreted_styles_classic.json).
interpreted_text_colors.json: Textfarben für Barrierefreiheit.
content_color_injected_<variant>.json: Finale Vorlagen mit eingefügten Stilen (z. B. content_color_injected_stylish.json).


content_template_new_project/: Template-Ordner mit Vorlagen, die bei der Projektinitialisierung kopiert werden:

content_template_max.json
layout_extended_v2.csv
customer_style_config.json
layout_rules.json (enthält background_color statt background).



Skripte und deren Reihenfolge
Um ein komplettes Projekt abzuwickeln, führe die folgenden Skripte in dieser Reihenfolge aus. Jedes Skript erzeugt bestimmte Dateien, die das nächste Skript benötigt. Wichtig: Verwende die angepasste Version Interpret_styles_v1.1.py (ohne die Generierung von layout_rules.json), wie in der vorherigen Antwort beschrieben.

init_new_project.py

Zweck: Erstellt einen neuen Projektordner mit den notwendigen Eingabedateien, indem es Dateien aus content_template_new_project/ kopiert.
Eingaben: Keine (verwendet content_template_new_project/ als Vorlage).
Ausgaben (im Ordner content/<project_name>/, z. B. content/florr99/):

content_template_max.json
layout_extended_v2.csv
customer_style_config.json
layout_rules.json (mit background_color, kopiert aus content_template_new_project/).


Ausführung:
bashpython /workspaces/companyculturehub-generator-v2/scripts/init_new_project.py

Hinweis: Füge nach der Erstellung color_definitions.json manuell in content/florr99/ hinzu (z. B. Pro_0299.Hiltbrandus99_20250901_07.54.56_Uhr_color_definitions.json). Bearbeite content_template_max.json, layout_extended_v2.csv und customer_style_config.json bei Bedarf für projektspezifische Anpassungen.


Interpret_colors_v1.0.py

Zweck: Verarbeitet color_definitions.json, um Farben, Farbverläufe und Stilvorschläge zu erstellen.
Eingaben:

content/<project_name>/color_definitions.json (z. B. content/florr99/Pro_0299.Hiltbrandus99_20250901_07.54.56_Uhr_color_definitions.json).


Ausgaben (im Ordner content/<project_name>/):

interpreted_colors.json


Ausführung:
bashpython /workspaces/companyculturehub-generator-v2/scripts/Interpret_colors_v1.0.py --project florr99

Hinweis: Falls color_definitions.json dynamische Namen hat, verwende eine angepasste Version des Skripts mit glob-Logik (wie in früheren Antworten beschrieben) oder gib den genauen Dateinamen mit --input-file an.


Interpret_styles_v1.1.py

Zweck: Generiert Stile und Textfarben für jede Designvariante basierend auf Eingabedateien.
Eingaben:

content/<project_name>/layout_extended_v2.csv
content/<project_name>/interpreted_colors.json
content/<project_name>/layout_rules.json (kopiert aus content_template_new_project/, mit background_color)
templates/components/style_modulator.json
content/<project_name>/customer_style_config.json


Ausgaben (im Ordner content/<project_name>/):

interpreted_styles_<variant>.json (z. B. interpreted_styles_classic.json, interpreted_styles_stylish.json)
interpreted_text_colors.json


Ausführung:
bashpython /workspaces/companyculturehub-generator-v2/scripts/Interpret_styles_v1.1.py --project florr99

Hinweis: Verwende die angepasste Version Interpret_styles_v1.1.py, in der die Funktion create_default_layout_rules und ihr Aufruf entfernt wurden (siehe vorherige Antwort). Stelle sicher, dass layout_rules.json in content/florr99/ den Schlüssel background_color enthält.


Inject_styles_v1.0.py

Zweck: Fügt Farben, Stile und Textfarben in content_template_max.json ein, um variantenspezifische Vorlagen zu erstellen.
Eingaben:

content/<project_name>/content_template_max.json
content/<project_name>/interpreted_colors.json
content/<project_name>/interpreted_styles_<variant>.json
content/<project_name>/interpreted_text_colors.json
content/<project_name>/customer_style_config.json


Ausgaben (im Ordner content/<project_name>/):

content_color_injected_<variant>.json (z. B. content_color_injected_classic.json)


Ausführung:
bashpython /workspaces/companyculturehub-generator-v2/scripts/Inject_styles_v1.0.py --project florr99




Kompletter Workflow

Initialisiere das Projekt:
bashpython /workspaces/companyculturehub-generator-v2/scripts/init_new_project.py

Erstellt content/florr99/ mit:

content_template_max.json
layout_extended_v2.csv
customer_style_config.json
layout_rules.json (mit background_color)


Füge color_definitions.json manuell hinzu und bearbeite bei Bedarf die anderen Dateien.


Verarbeite Farben:
bashpython /workspaces/companyculturehub-generator-v2/scripts/Interpret_colors_v1.0.py --project florr99

Erzeugt content/florr99/interpreted_colors.json.


Verarbeite Stile:
bashpython /workspaces/companyculturehub-generator-v2/scripts/Interpret_styles_v1.1.py --project florr99

Erzeugt content/florr99/interpreted_styles_<variant>.json und content/florr99/interpreted_text_colors.json.


Injiziere Stile:
bashpython /workspaces/companyculturehub-generator-v2/scripts/Inject_styles_v1.0.py --project florr99

Erzeugt content/florr99/content_color_injected_<variant>.json für jede Variante.



Wichtige Hinweise

Reihenfolge: Führe die Skripte in der angegebenen Reihenfolge aus, da jedes Skript die Ausgaben des vorherigen benötigt.
Template-Datei: Stelle sicher, dass layout_rules.json in content_template_new_project/ den Schlüssel background_color verwendet (siehe vorherige Antwort). Dies wird automatisch in content/florr99/ kopiert.
Prüfe Eingabedateien: Überprüfe, ob alle Eingabedateien vorhanden sind:
bashls -l /workspaces/companyculturehub-generator-v2/content/florr99/
ls -l /workspaces/companyculturehub-generator-v2/templates/components/

Dynamische Dateinamen: Falls customer_style_config.json oder color_definitions.json dynamische Namen haben (z. B. Pro_0299.Hiltbrandus99_20250901_07.54.56_Uhr_customer_style_config.json), passe die Skripte mit glob-Logik an (siehe frühere Antworten) oder gib die Dateinamen explizit an.

Zusammenfassung der generierten Dateien

Nach init_new_project.py (in content/florr99/):

content_template_max.json
layout_extended_v2.csv
customer_style_config.json
layout_rules.json


Nach Interpret_colors_v1.0.py (in content/florr99/):

interpreted_colors.json


Nach Interpret_styles_v1.1.py (in content/florr99/):

interpreted_styles_classic.json, interpreted_styles_stylish.json, etc.
interpreted_text_colors.json


Nach Inject_styles_v1.0.py (in content/florr99/):

content_color_injected_classic.json, content_color_injected_stylish.json, etc.



Falls du eine Anpassung für dynamische Dateinamen oder weitere Vereinfachungen brauchst, lass es mich wissen! Ich bleibe klar und fokussiert.