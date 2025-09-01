Praxis-Tipps für CompanyCultureHub Generator
Edge Cases

Dunkle Farben: Nutze fade-up (zukünftig) oder manuell in CSS anpassen.
Fehlende Daten: Stelle sicher, dass color_definitions.json vorhanden ist; sonst Fallback zu Defaults.

Testen

Generiere mit Beispiel-JSON: python scripts/generator_v_fullpower.py.
Überprüfe HTML in Browser für Kontraste.

Optimierung

In generator_v_fullpower.py Farben interpretieren: HSV-Anpassung für bessere Lesbarkeit.
