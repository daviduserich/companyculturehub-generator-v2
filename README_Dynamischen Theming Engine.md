PROJEKT-START: Implementierung der "Dynamischen Theming Engine"

**Das Ziel:**
Wir rüsten den bestehenden Seiten-Generator von einer starren Struktur zu einer flexiblen "Dynamischen Theming Engine" auf. Anstatt nur zwei fester Stile ("Klassisch", "Stylisch"), schaffen wir ein modulares Baukasten-System, das durch einfache Parameter in der `content.json` gesteuert wird. Wir implementieren dies jedoch so, dass wir als ersten Schritt zwei "Presets" ("Klassisch" und "Stylisch") definieren, um den Prozess einfach und pragmatisch zu halten.

**Der Plan (Hybrid-Ansatz: Presets + Baukasten):**

1.  **Technische Grundlage (Der Baukasten):**
    *   Wir passen die HTML-Komponenten so an, dass sie auf spezifische CSS-Klassen reagieren (z.B. `.bg-gradient`, `.card-glass`, `.btn-pill`).
    *   Diese Klassen steuern einzelne Design-Aspekte wie Hintergrund-Stile (Verlauf/einfarbig), Karten-Effekte (Schatten/Glas-Effekt) und Button-Formen (eckig/rund).

2.  **Abstraktionsebene (Die Presets):**
    *   Wir führen in der `content.json` einen einzigen, einfachen Schalter ein: `"presentation_style": "stylish"` (oder `"classic"`).
    *   Der Python-Generator (`generator.v2.py`) wird so angepasst, dass er diesen einen Schalter liest.
    *   Basierend auf dem Wert (`stylish` oder `classic`) wählt der Generator ein vordefiniertes "Rezept" (Preset) aus.
    *   Ein Rezept ist eine festgelegte Kombination der Baukasten-Optionen (z.B. "Stylisch" = Verlauf + Glas-Effekt + runde Buttons).
    *   Der Generator fügt dann die entsprechenden CSS-Klassen (`bg-gradient card-glass btn-pill`) automatisch dem `<body>`-Tag der finalen Webseite hinzu.

**Vorteile dieses Ansatzes:**
*   **Einfache Steuerung:** Wir müssen nur einen einzigen Wert in der `content.json` ändern, um das gesamte Erscheinungsbild zu wechseln.
*   **Maximale Flexibilität:** Die darunterliegende Baukasten-Architektur erlaubt uns in Zukunft, durch manuelle Anpassung der `content.json` auch individuelle Mischformen zu erstellen.
*   **Klarer Projektabschluss:** Das Projekt ist abgeschlossen, sobald die zwei Presets "Klassisch" und "Stylisch" erfolgreich implementiert sind.

**Nächster Schritt:**
Wir beginnen mit der Anpassung der `header.html`-Komponente, um den `<body>`-Tag dynamisch mit den Klassen des gewählten Presets zu befüllen.
