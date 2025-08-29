PROJEKT-ZUSAMMENFASSUNG: "Echt-Header"-Integration

**Das Ziel:**
Das bestehende System zur Generierung von Employer-Branding-Seiten soll um ein optionales Feature erweitert werden, das es ermöglicht, den originalen Navigations-Header einer Firmen-Website zu extrahieren und in unsere generierte Seite zu integrieren. Dies soll die User Experience verbessern und eine nahtlose visuelle und funktionale Verbindung zwischen der Haupt-Website und unserer Seite schaffen.

**Der Workflow (Semi-Automatisch & Pragmatisch):**
1.  **Manueller Schritt (10 Sekunden):** Der Entwickler besucht die Firmen-Website, öffnet die Browser-Entwicklertools, identifiziert den Haupt-Navigations-Container (z.B. `<header>` oder `<nav>`) und kopiert dessen "Outer HTML" in die Zwischenablage.
2.  **Input-Erweiterung:** Dieses HTML-Snippet wird in die `start_inputs/projekt.json`-Datei des Farb-Extraktions-Repos in ein neues, optionales Feld namens `"header_html_snippet"` eingefügt.
3.  **Extraktions-Anpassung:** Das Farb-Extraktions-Skript wird so angepasst, dass es prüft, ob dieses Feld existiert.
    *   **Wenn ja:** Es nimmt das HTML-Snippet, "säubert" es (wandelt relative Links in absolute um, identifiziert/markiert den "Karriere"-Link) und gibt es in einem neuen `header_override`-Objekt in der finalen `color_definitions.json` aus.
    *   **Wenn nein:** Es überspringt den Schritt.
4.  **Template-Generator-Anpassung:**
    *   Eine neue Komponente `customer_header.html` wird erstellt, die das `header_override.html_content` und `header_override.css_content` (falls vorhanden) aus der `content.json` einfügt.
    *   Der Generator prüft, ob das `header_override`-Objekt in der geimpften `content.json` existiert.
    *   **Wenn ja:** Er verwendet die `customer_header.html`-Komponente anstelle des Standard-Headers.
    *   **Wenn nein:** Er verwendet den bisherigen Standard-Header.

**Kern-Vorteil dieser Methode:**
Wir umgehen die komplexe und fehleranfällige Aufgabe, den Header automatisch zu "erraten", und setzen stattdessen auf einen minimalen manuellen Schritt, der 100%ige Präzision und Zuverlässigkeit garantiert.


------------------------------------------
------------------------------------------

1. Deine Design-Idee für die Hero-Sektion (Für die Zukunft)
"...man könnte ja auch z.B hingehen und sagen einfach der unterste Drittel der Sektion wird von unten her aufgefüllt gegen oben verlaufen den transparent das ist dann irgendwie nach einem Drittel ist es dann quasi ausgelaufen das würde von mir aus gesehen relativ stylisch aussehen würde aber diese riesigen schwarzen Fläche ein wenig den Schrecken nehmen..."
Das ist eine absolut professionelle Design-Technik! Man nennt das oft einen "Farbverlauf zu Transparenz" (gradient to transparent). Es ist eine extrem elegante Methode, um einer Sektion Farbe zu geben, ohne sie komplett zu "erschlagen".
Konzeptionelle Notiz für die Zukunft (Pareto-Stein Nr. 4):
Wir könnten in unserer Theming Engine eine neue Option einführen: background_style: "fade-up".
CSS-Umsetzung: background: linear-gradient(to top, var(--color-primary) 0%, transparent 33%);
Effekt: Die Primärfarbe steigt vom unteren Rand der Sektion etwa ein Drittel hoch und läuft dann sanft aus. Der Rest der Sektion hätte die normale Hintergrundfarbe der Seite (z.B. Weiss).
Vorteil: Extrem modern, leicht, und perfekt für dunkle oder sehr dominante Markenfarben.
Das ist eine geniale Idee. Wir parken sie sicher in unserem "Zukunfts-Ideen"-Ordner.