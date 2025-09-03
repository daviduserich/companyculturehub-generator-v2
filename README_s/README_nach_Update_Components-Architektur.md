
### Zusammenfassung des Workflows: Von der Idee zur fertigen HTML-Seite

Hier ist der gesamte Prozess in logischer Reihenfolge, aufgeteilt in die einzelnen Phasen und Artefakte.

#### Phase 1: Die Vorbereitung (Einmalige Einrichtung & Modul-Entwicklung)

1.  **Die Bausteine (Input):**
    *   `templates/components/*.html`: Die **HTML-Modul-Templates**. Sie definieren die Grundstruktur und die Platzhalter (`{{...}}`) für jede Sektion.
    *   `templates/components/*.json`: Die **JSON-Definitionsdateien**. Jede Datei ist eine "Anleitung" für das zugehörige HTML-Modul und beschreibt den Zweck jedes einzelnen Feldes (z.B. was eine `headline` bezwecken soll).

2.  **Das Gehirn (Unser Skript):**
    *   `content_generator.py`: Das **Python-Skript**, das wir gerade finalisiert haben. Seine Aufgabe ist es, aus den Bausteinen und einer Konfigurationsdatei eine Blaupause zu erstellen.

#### Phase 2: Die Projekt-Konfiguration (Projektspezifische Anpassung)

*   **Der Bauplan (Input):**
    *   `{projekt_ordner}/layout_extended_v2.csv`: Die **projektspezifische Layout-Datei**. Dies ist die zentrale Steuerungsdatei für ein konkretes Projekt. Sie wird aus einer Master-Vorlage kopiert und angepasst.
    *   **Was sie steuert:**
        *   Welche Module werden verwendet? (`enabled: TRUE/FALSE`)
        *   Wie oft kommt jedes Modul vor? (`max_count`)
        *   Wie viele Listenelemente hat ein Modul? (`max_list_items`)

#### Phase 3: Die Template-Generierung (Unser aktueller Fokus)

*   **Der Prozess:**
    1.  Sie rufen das Skript `content_generator.py` auf und übergeben ihm den Pfad zum `{projekt_ordner}`.
    2.  Das Skript liest die projektspezifische `layout_extended_v2.csv`.
    3.  Es baut, basierend auf den Regeln in der CSV, eine JSON-Struktur auf.
    4.  Für jedes Feld in der Struktur holt es sich die Zweck-Beschreibung aus den `templates/components/*.json`-Dateien.

*   **Das Ergebnis (Output):**
    *   `{projekt_ordner}/output/generated_content_template_... .json`: Das **maßgeschneiderte Anleitungs-JSON**. Dies ist die "leere", aber perfekt strukturierte und mit Anweisungen versehene Blaupause, die exakt den Anforderungen des Projekts entspricht.

#### Phase 4: Die Content-Erstellung (Ihr großes Framework)

*   **Der Prozess:**
    1.  Ihr großes **Copyrighting-Framework** wird aktiv.
    2.  Es nimmt das **Anleitungs-JSON** aus Phase 3 als Input.
    3.  Es nutzt die darin enthaltenen Beschreibungen (`description`) und sein Wissen über die Firma, um die `value`-Felder mit hochwertigen, kontextbezogenen Texten und Bildvorschlägen zu befüllen.

*   **Das Ergebnis (Output):**
    *   Ein **vollständig befülltes JSON**. Die Blaupause ist jetzt mit Leben (Inhalten) gefüllt.

#### Phase 5: Die finale HTML-Generierung (Der nächste Schritt)

*   **Der Prozess:**
    1.  Ein **neuer HTML-Generator** (das nächste Skript, das wir konzipieren werden) wird gestartet.
    2.  Er nimmt zwei Dinge als Input:
        *   Die **projektspezifische `layout_extended_v2.csv`**, um die Reihenfolge und Anzahl der Module zu kennen.
        *   Das **vollständig befüllte JSON** aus Phase 4, um die Inhalte zu bekommen.
    3.  Er lädt zusätzlich die projektspezifischen **Styling- und Farb-Dateien** (z.B. `interpreted_styles_classic.json`).
    4.  Er durchläuft die CSV Zeile für Zeile, nimmt das entsprechende HTML-Modul, füllt es mit den Inhalten aus dem befüllten JSON und den passenden Style-Klassen und fügt alles zu einer finalen HTML-Datei zusammen. Dieser Schritt wird für jede der vier Styling-Varianten wiederholt.

*   **Das Ergebnis (Output):**
    *   Vier fertige `index_{style}.html`-Dateien.

---

