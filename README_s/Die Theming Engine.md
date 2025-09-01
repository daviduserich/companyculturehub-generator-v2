Anleitung: Dynamische Theming Engine (v4.0)
Die Theming Engine ermöglicht granulare Kontrolle über das Design der generierten Seiten. Sie basiert auf einem Baukasten-System mit CSS-Klassen, gesteuert via content.json.
Konzept: Presets vs. Granulare Kontrolle

Presets: Einfacher Schalter in content.json ("presentation_style": "stylish" oder "classic"). Der Generator wählt ein Rezept (z. B. "stylish" = Gradient + Glass + Pill-Buttons).
Granulare Kontrolle: Füge "theme_options" hinzu – ignoriert Presets und erlaubt manuelle Einstellungen.

Beispiel in content.json:
"design": {
  "presentation_style": "stylish",  // Ignoriert, wenn theme_options existiert
  "theme_options": {
    "background_style": "gradient",
    "card_style": "glass",
    "button_style": "pill",
    "animation_intensity": "playful"
  }
}

Verfügbare Optionen

background_style: "solid" (einfarbig), "gradient" (Verlauf).
card_style: "flat" (einfach), "shadow" (Schatten), "glass" (Glas-Effekt).
button_style: "rect" (eckig), "pill" (rund).
animation_intensity: "subtle" (sanft), "playful" (dynamisch).

Der Generator fügt Klassen zu <body> hinzu (z. B. bg-gradient card-glass).
Integration mit Repo 1
Farben aus design.branding werden als CSS-Variablen gesetzt (z. B. --color-primary). Für bessere Harmonie: Erweitere den Generator, um Gradients dynamisch zu generieren (z. B. basierend auf Sättigung).