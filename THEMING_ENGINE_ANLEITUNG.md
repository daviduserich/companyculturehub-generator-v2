THEMING_ENGINE_ANLEITUNG.md
Markdown
# Anleitung: Die Dynamische Theming Engine (v4.0)

Dieses Dokument erklärt, wie man die volle, granulare Kontrolle über das Design der generierten Webseiten übernimmt. Das System ist so aufgebaut, dass es nicht nur zwei feste Stile ("Klassisch", "Stylisch") kennt, sondern durch ein modulares Baukasten-System gesteuert wird.

## 1. Das Konzept: Vom "Preset" zum "Cockpit"

Standardmässig steuerst du das Design über einen einzigen Schalter in der `content.json`:

```json
"design": {
  "presentation_style": "stylish" // oder "classic"
}
Dieser Schalter wählt ein Preset (ein vordefiniertes "Rezept") im Python-Generator aus. Das ist einfach und schnell.
Um die volle Kontrolle zu erhalten, kannst du dieses Preset-System umgehen und die Design-Entscheidungen direkt in der content.json treffen.
2. Das Design-Cockpit: Dein Steuerpult in der content.json
Um vom Preset-Modus in den manuellen Modus zu wechseln, fügst du in der content.json ein neues Objekt namens theme_options in den design-Block ein.
Wichtig: Sobald das theme_options-Objekt existiert, wird der presentation_style-Schalter ignoriert.
Dein design-Block in der content.json würde dann so aussehen:
JSON
"design": {
  "branding": { ... },
  "logo": { ... },
  // "presentation_style": "stylish", // Diese Zeile wird jetzt ignoriert

  "theme_options": {
    "background_style": "gradient",
    "card_style": "glass",
    "button_style": "pill",
    "animation_intensity": "playful"
  }
}
Dieses theme_options-Objekt ist dein Cockpit. Du kannst hier die einzelnen "Regler" bedienen, um das Design fein abzustimmen.
3. Die verfügbaren "Regler" und ihre Optionen
Hier ist eine Übersicht aller verfügbaren Design-Entscheidungen und ihrer möglichen Werte.
a) Hintergrund-Stil (background_style)
Steuert den Hintergrund der Haupt-Farbsektionen (hero, benefits).
"solid": Verwendet eine einfarbige Fläche (meist --color-primary).
Ergebnis: Ruhig, klassisch, fokussiert.
"gradient": Verwendet die dynamisch generierten Farbverläufe.
Ergebnis: Modern, dynamisch, auffällig.
b) Karten-Stil (card_style)
Steuert das Aussehen der "Karten" (z.B. in der benefits-Sektion).
"shadow": Karten heben sich durch einen dezenten Schatten vom Hintergrund ab.
Ergebnis: Professionell, sauber, gute Tiefenwirkung.
"glass": Wendet den "Glasmorphismus"-Effekt an (halb-transparent mit unscharfem Hintergrund).
Ergebnis: Sehr modern, elegant, "High-Tech".
"flat": Karten haben fast keinen eigenen Stil, nur einen dünnen Rahmen.
Ergebnis: Minimalistisch, puristisch.
c) Button-Stil (button_style)
Steuert die Form der Haupt-Buttons.
"sharp": Fast eckige Buttons mit minimal abgerundeten Ecken.
Ergebnis: Seriös, technisch, formal.
"rounded": Deutlich abgerundete Ecken.
Ergebnis: Freundlich, modern, der "Standard" im Webdesign.
"pill": Komplett abgerundete Seiten, die eine "Pillen"-Form ergeben.
Ergebnis: Verspielt, stylisch, sehr modern.
d) Animations-Intensität (animation_intensity)
Steuert kleine Effekte wie Hover-Animationen oder Text-Schatten.
"subtle": Minimale Interaktion. Elemente werden beim Hovern z.B. nur leicht heller.
Ergebnis: Dezent, professionell, lenkt nicht ab.
"playful": Aktiviert zusätzliche Effekte wie "Schweben" beim Hovern (transform), Text-Schatten oder Overlay-Effekte für mehr Tiefe.
Ergebnis: Lebendig, interaktiv, fesselnd.
4. Anwendungsbeispiele: Eigene Stile kreieren
Mit diesem Cockpit kannst du nun jeden beliebigen Stil zusammenstellen, ohne eine Zeile Code zu ändern.
Beispiel 1: "Ultra-Klassisch & Seriös"
JSON
"theme_options": {
  "background_style": "solid",
  "card_style": "flat",
  "button_style": "sharp",
  "animation_intensity": "subtle"
}
Beispiel 2: "Modern, aber nicht zu verspielt"
JSON
"theme_options": {
  "background_style": "gradient",
  "card_style": "shadow",
  "button_style": "rounded",
  "animation_intensity": "subtle"
}
Beispiel 3: "Einzigartiger Mix"
JSON
"theme_options": {
  "background_style": "solid",      // Ruhiger Hintergrund...
  "card_style": "glass",        // ...aber mit modernen Glaskarten.
  "button_style": "pill",         // Sehr moderne Buttons...
  "animation_intensity": "subtle"   // ...aber mit dezenten Animationen.
}
5. Wie es technisch funktioniert (Kurzfassung)
Der Python-Generator prüft, ob das theme_options-Objekt in der content.json existiert.
Wenn ja, ignoriert er den presentation_style-Schalter.
Er liest die Werte aus dem theme_options-Cockpit.
Er baut daraus einen String von CSS-Klassen (z.B. "bg-solid card-glass btn-pill anim-subtle").
Dieser String wird als Klasse an den <body>-Tag der finalen Webseite gehängt.
Die CSS-Regeln in den Komponenten-Templates sind so geschrieben, dass sie auf diese spezifischen Klassen reagieren und das Design entsprechend anpassen.
Diese Anleitung gibt dir die volle Macht über das Design-System, das wir gebaut haben. Du kannst mit den Presets starten und bei Bedarf jederzeit in den manuellen Modus wechseln, um pixelgenaue, individuelle Designs für deine Kunden zu erstellen.


-------------------------Präzisierungsfragen--------------------
Also ich muss jetzt noch nachfragen das heisst also wir haben einen presentation Style Schalter David klassisch oder stylisch unterschieden.
Und es kann sein dass es in dem Content Jason das ist dort ein sieben optionsobjekt gibt.
Wenn ein solches vorhanden ist wird alles was dort definiert ist umgesetzt.
Wenn keines vorhanden ist wird eben diese Präsentation Style Schalter berücksichtigt.
>>>>>>>>>>>>>>>>>> Antwort:
---------------------------------------------------------------
a. Du hast es exakt und perfekt auf den Punkt gebracht. Das ist die 100% korrekte Zusammenfassung der Logik, die wir implementiert haben.
Genau so funktioniert es:
Der Generator schaut zuerst nach dem "Cockpit":
Er prüft: "Gibt es in der content.json ein Objekt namens theme_options?"
Fall A: Das "Cockpit" existiert (theme_options ist vorhanden):
Der Generator sagt: "Ah, der Nutzer will die volle manuelle Kontrolle!"
Er ignoriert den presentation_style-Schalter komplett.
Er liest die einzelnen Werte aus dem theme_options-Objekt (background_style, card_style etc.) und baut daraus die spezifischen CSS-Klassen für den <body>-Tag.
Ergebnis: Ein massgeschneidertes Design, das exakt deinen manuellen Einstellungen entspricht.
Fall B: Das "Cockpit" existiert NICHT (theme_options ist nicht vorhanden):
Der Generator sagt: "Okay, kein manueller Eingriff. Ich schalte auf den einfachen Preset-Modus um."
Er schaut sich jetzt den presentation_style-Schalter an.
Er liest den Wert (z.B. "stylish") und wählt das passende, vordefinierte "Rezept" (Preset) aus seinem internen Speicher.
Er leitet aus diesem Rezept die CSS-Klassen für den <body>-Tag ab.
Ergebnis: Ein konsistentes Design, das entweder dem "Klassisch"- oder dem "Stylisch"-Preset entspricht.
Du hast die Hierarchie und die Fallback-Logik absolut richtig verstanden. Das gibt dir die maximale Flexibilität: Du kannst schnell und einfach mit den Presets arbeiten, hast aber jederzeit die Möglichkeit, durch Hinzufügen des theme_options-Objekts in den "Experten-Modus" zu wechseln und jedes Detail von Hand zu steuern, ohne eine einzige Zeile am Generator-Code ändern zu müssen.
Das System ist bereit für deine Tests.

----------------------------------------------------------------