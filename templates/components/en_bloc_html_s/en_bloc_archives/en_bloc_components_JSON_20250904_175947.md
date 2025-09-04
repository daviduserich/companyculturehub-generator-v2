# JSON-Komponenten-Zusammenzug (en bloc)

**Generiert am:** 2025-09-04 17:59:47

## Kontext
Dieses Dokument enthält alle JSON-Konfigurationsdateien der aktiven Webseiten-Module (Komponenten).
Diese JSON-Dateien enthalten die Datenstrukturen und Konfigurationen, die für die entsprechenden HTML-Module verwendet werden.

**Zweck dieses Dokuments:**
Einem Large Language Model (LLM) einen vollständigen Überblick über alle vorhandenen JSON-Datenstrukturen zu geben, um Analysen, Vorschläge oder Code-Generierungen durchzuführen.

**Anzahl der JSON-Module:** 13

**Hinweis:** Diese Datei enthält nur JSON-Dateien, für die auch entsprechende HTML-Module existieren.

---

## JSON-Modul: `benefits_section.json`

```json
{
  "headline": {
    "description": "Eine Überschrift, die die Vorteile klar als 'Gewinn' für den Mitarbeiter kommuniziert.",
    "example_value": "Alles, was Du für Deinen Erfolg brauchst.",
    "value": ""
  },
  "description": {
    "description": "Ein kurzer Text, der zusammenfasst, wie die Benefits den Mitarbeiter im Leben und bei der Arbeit unterstützen.",
    "example_value": "Dein Wohlbefinden und Deine Entwicklung sind uns wichtig. Deshalb bieten wir Dir mehr als nur ein gutes Gehalt.",
    "value": ""
  },
  "benefits_list": {
    "description": "Eine Liste von konkreten Vorteilen.",
    "icon": { "description": "Ein passendes Emoji oder Icon.", "example_value": "📚", "value": "" },
    "title": {
      "description": "Der Name des Benefits.",
      "example_value": "Individuelles Weiterbildungsbudget",
      "value": ""
    },
    "text": {
      "description": "Eine detaillierte Erklärung des Nutzens für den Mitarbeiter.",
      "example_value": "Du erhältst ein jährliches Budget, das Du frei für Konferenzen, Kurse oder Zertifizierungen nutzen kannst, um Deine Fähigkeiten gezielt zu erweitern.",
      "value": ""
    }
  }
}
```


## JSON-Modul: `career_cta_section.json`

```json
{
  "headline": {
    "description": "Die finale, aktivierende Überschrift, die Dich direkt anspricht.",
    "example_value": "Bereit, Deine Karriere zu starten?",
    "value": ""
  },
  "description": {
    "description": "Ein kurzer, motivierender Satz, der Dich zum nächsten Schritt ermutigt.",
    "example_value": "Wir sind immer auf der Suche nach talentierten Menschen wie Dir. Wir freuen uns darauf, von Dir zu hören.",
    "value": ""
  }
}
```


## JSON-Modul: `culture_section.json`

```json
{
  "headline": {
    "description": "Überschrift, die das Thema 'Unternehmenskultur' aus der Perspektive des Bewerbers beleuchtet. Was hat er davon?",
    "example_value": "Ein Umfeld, in dem Du wachsen kannst.",
    "value": ""
  },
  "description": {
    "description": "Ein kurzer Einleitungstext, der erklärt, wie die Kultur den Mitarbeiter im Alltag unterstützt und fördert.",
    "example_value": "Wir glauben, dass die besten Ideen in einem Umfeld entstehen, das auf Vertrauen, Freiheit und gegenseitiger Unterstützung basiert. So sieht Dein Arbeitsalltag bei uns aus:",
    "value": ""
  },
  "values_list": {
    "description": "Eine Liste von Kernwerten, die den Nutzen für den Mitarbeiter aufzeigen.",
    "icon": { "description": "Ein passendes Emoji oder Icon.", "example_value": "💡", "value": "" },
    "title": {
      "description": "Der Name des Kernwerts, formuliert als Vorteil.",
      "example_value": "Deine Ideen zählen",
      "value": ""
    },
    "text": {
      "description": "Eine konkrete Beschreibung, wie der Mitarbeiter diesen Wert im Alltag erlebt.",
      "example_value": "Bei uns hat jeder eine Stimme. Deine Vorschläge werden gehört, diskutiert und oft auch umgesetzt – egal, welche Position Du hast.",
      "value": ""
    }
  },
  "image_url": {
    "description": "URL zu einem Bild, das die Kultur in Aktion zeigt.",
    "example_value": "assets/images/placeholder_culture.jpg",
    "value": ""
  },
  "image_alt_text": {
    "description": "Alternativtext, der das Bild beschreibt.",
    "example_value": "Kollegen bei einem kreativen Brainstorming in unseren modernen Büroräumen.",
    "value": ""
  }
}
```


## JSON-Modul: `diversity_section.json`

```json
{
  "headline": {
    "description": "Eine Überschrift, die kommuniziert, dass hier jeder so sein kann, wie er ist, und willkommen ist.",
    "example_value": "Bring Deine ganze Persönlichkeit mit ein.",
    "value": ""
  },
  "description": {
    "description": "Ein Text, der erklärt, warum Vielfalt im Team zu besseren Ergebnissen führt und wie Du als Individuum davon profitierst.",
    "example_value": "Wir sind überzeugt: Die besten Ideen entstehen, wenn unterschiedliche Perspektiven und Erfahrungen aufeinandertreffen. Bei uns wirst Du für Deine einzigartige Sichtweise geschätzt und bist Teil eines Teams, in dem jeder vom anderen lernt.",
    "value": ""
  },
  "image_url": {
    "description": "URL zu einem Bild, das ein diverses Team in einer positiven, kollaborativen Umgebung zeigt.",
    "example_value": "assets/images/placeholder_diversity.jpg",
    "value": ""
  },
  "image_alt_text": {
    "description": "Ein Alternativtext, der die Vielfalt im Bild betont.",
    "example_value": "Ein diverses Team von Kollegen unterschiedlicher Herkunft und Geschlechter arbeitet lachend an einem Projekt.",
    "value": ""
  }
}
```


## JSON-Modul: `footer_section.json`

```json
{}
```


## JSON-Modul: `hero_section.json`

```json
{
  "headline": {
    "description": "Die emotionale Hauptüberschrift. Soll den Bewerber als Held positionieren und sein Potenzial ansprechen. Fokus: Wirkung, nicht Beschreibung.",
    "example_value": "Gestalte Deine Zukunft. Und die unserer Branche.",
    "value": ""
  },
  "subheadline": {
    "description": "Eine unterstützende Unterzeile, die das Versprechen der Headline konkretisiert und den Nutzen für den Bewerber hervorhebt.",
    "example_value": "Bei uns findest Du die Werkzeuge, das Team und die Freiheit, um wirklich etwas zu bewegen.",
    "value": ""
  },
  "description": {
    "description": "Ein kurzer, einladender Absatz, der den Bewerber direkt anspricht und ihm zeigt, was er auf dieser Seite für sich entdecken kann.",
    "example_value": "Bist Du bereit, Deine Ideen in die Tat umzusetzen? Entdecke hier, wie wir Dich dabei unterstützen, Deine beruflichen Ziele zu erreichen und über Dich hinauszuwachsen.",
    "value": ""
  },
  "image_url": {
    "description": "URL zu einem hochwertigen, authentischen Bild, das Kollaboration und Erfolg zeigt. Sollte Energie und eine positive Atmosphäre ausstrahlen.",
    "example_value": "assets/images/placeholder_hero.jpg",
    "value": ""
  },
  "image_alt_text": {
    "description": "Ein beschreibender Alternativtext, der den Bildinhalt aus der Perspektive von Teamarbeit und Erfolg beschreibt.",
    "example_value": "Ein Team von Experten arbeitet gemeinsam an einer innovativen Lösung.",
    "value": ""
  }
}
```


## JSON-Modul: `location_section.json`

```json
{
  "headline": {
    "description": "Eine Überschrift, die Dein zukünftiges Arbeitsumfeld vorstellt.",
    "example_value": "Dein neuer Arbeitsplatz im Herzen der Stadt.",
    "value": ""
  },
  "description": {
    "description": "Ein Text, der die Vorteile des Standorts und der Büroräumlichkeiten für Dich beschreibt (z.B. gute Anbindung, moderne Ausstattung).",
    "example_value": "Genieße eine perfekte Anbindung an öffentliche Verkehrsmittel und eine Mittagspause in den besten Cafés der Stadt. Unsere modernen, ergonomisch ausgestatteten Büros bieten Dir alles, was Du für einen produktiven und angenehmen Arbeitstag brauchst.",
    "value": ""
  },
  "map_url": {
    "description": "URL zu einem Bild, das eine Karte des Standorts oder ein ansprechendes Foto der Büroräumlichkeiten zeigt.",
    "example_value": "assets/images/placeholder_location.jpg",
    "value": ""
  },
  "image_alt_text": {
    "description": "Ein beschreibender Alternativtext.",
    "example_value": "Die hellen und modernen Büroräume mit Blick über die Stadt.",
    "value": ""
  }
}
```


## JSON-Modul: `logo_header_section.json`

```json
{}
```


## JSON-Modul: `navigation_section.json`

```json
{
  "nav_items": {
    "description": "Eine Liste von Navigationselementen, die Dir helfen, schnell zu finden, was Du suchst.",
    "url": {
      "description": "Die vollständige URL, zu der das Navigationselement verlinken soll.",
      "example_value": "https://example.com/ueber-uns",
      "value": ""
    },
    "label": {
      "description": "Der sichtbare Text des Links. Kurz und eindeutig.",
      "example_value": "Über uns",
      "value": ""
    }
  }
}
```


## JSON-Modul: `stolz_section.json`

```json
{
  "headline": {
    "description": "Eine selbstbewusste Überschrift, die zeigt, an welchen beeindruckenden Projekten Du mitarbeiten kannst.",
    "example_value": "Projekte, die Deine Handschrift tragen werden.",
    "value": ""
  },
  "description": {
    "description": "Ein kurzer Text, der den Kontext für die Highlights gibt und zeigt, dass hier Arbeit mit echtem 'Impact' geleistet wird.",
    "example_value": "Wir setzen Maßstäbe in unserer Branche. Hier sind einige der Projekte, bei denen Du Deine Fähigkeiten einsetzen und stolz auf Deine Arbeit sein kannst:",
    "value": ""
  },
  "highlights_list": {
    "description": "Eine Liste von konkreten Erfolgen, die für einen neuen Mitarbeiter attraktiv sind.",
    "title": {
      "description": "Der Titel des Highlights, der den Erfolg auf den Punkt bringt.",
      "example_value": "Open-Source-Tool mit 10.000+ Nutzern",
      "value": ""
    },
    "text": {
      "description": "Eine kurze Beschreibung, die den Beitrag des Teams und die Relevanz des Erfolgs hervorhebt.",
      "example_value": "Unser Team hat ein Tool entwickelt, das heute von Entwicklern weltweit genutzt wird. Du hast die Chance, an solchen Projekten mitzuwirken.",
      "value": ""
    }
  }
}
```


## JSON-Modul: `story_telling_section.json`

```json
{
  "headline": {
    "description": "Die Überschrift einer narrativen Geschichte, die den Bewerber inspiriert.",
    "example_value": "Vom Nebenprojekt zur Erfolgsgeschichte.",
    "value": ""
  },
  "text": {
    "description": "Eine Geschichte, die zeigt, wie Mitarbeiter bei uns wachsen und ihre Ideen verwirklichen können.",
    "example_value": "Alles begann mit einer kleinen Idee in einer Kaffeepause. Markus, einer unserer Entwickler, wollte einen internen Prozess optimieren. Er bekam nicht nur die Zeit, daran zu arbeiten, sondern auch ein kleines Team. Heute wird dieses Tool von tausenden Kunden genutzt. Das ist nur eine von vielen Geschichten, die zeigen: Bei uns kannst Du wirklich etwas erschaffen.",
    "value": ""
  },
  "image_url": {
    "description": "URL zu einem Bild, das die Geschichte visuell unterstützt.",
    "example_value": "assets/images/placeholder_story.jpg",
    "value": ""
  },
  "image_alt_text": {
    "description": "Ein Alternativtext, der die Szene der Geschichte beschreibt.",
    "example_value": "Markus präsentiert stolz den Prototyp seiner Idee vor dem gesamten Team.",
    "value": ""
  }
}
```


## JSON-Modul: `team_section.json`

```json
{
  "headline": {
    "description": "Überschrift, die ein authentisches Testimonial ankündigt.",
    "example_value": "Was Deine zukünftigen Kollegen sagen.",
    "value": ""
  },
  "description": {
    "description": "Ein kurzer einleitender Satz, der den Kontext für das folgende Zitat gibt.",
    "example_value": "Niemand kann besser beschreiben, wie es ist, bei uns zu arbeiten, als das Team selbst:",
    "value": ""
  },
  "testimonial_quote": {
    "description": "Ein authentisches Zitat, das einen spezifischen Vorteil für den Mitarbeiter hervorhebt.",
    "example_value": "Ich kam mit einer Idee und dachte, sie sei zu verrückt. Heute ist sie ein Kernprodukt. Diese Art von Vertrauen und Freiheit habe ich noch nirgends sonst erlebt.",
    "value": ""
  },
  "testimonial_author_name": {
    "description": "Der vollständige Name des Mitarbeiters.",
    "example_value": "Maria Schmidt",
    "value": ""
  },
  "testimonial_author_title": {
    "description": "Die Berufsbezeichnung des Mitarbeiters.",
    "example_value": "Senior Software Engineer",
    "value": ""
  },
  "image_url": {
    "description": "URL zu einem professionellen Foto des zitierten Mitarbeiters oder einem Team-Bild.",
    "example_value": "assets/images/placeholder_testimonial.jpg",
    "value": ""
  },
  "image_alt_text": {
    "description": "Alternativtext für das Bild.",
    "example_value": "Porträt von Maria Schmidt, einer erfahrenen Software-Entwicklerin in unserem Team.",
    "value": ""
  }
}
```


## JSON-Modul: `values_section.json`

```json
{
  "headline": {
    "description": "Eine klare Überschrift, die zeigt, nach welchen Prinzipien hier gearbeitet wird, damit Du erfolgreich sein kannst.",
    "example_value": "Unsere Leitlinien für Deinen Erfolg.",
    "value": ""
  },
  "values_list": {
    "description": "Eine Liste von Kernwerten, die das Fundament der Zusammenarbeit bilden und Deinen Arbeitsalltag positiv prägen.",
    "icon": {
      "description": "Ein passendes Emoji oder Icon, das den Wert visuell repräsentiert.",
      "example_value": "🚀",
      "value": ""
    },
    "title": {
      "description": "Der Name des Kernwerts, formuliert als ein Versprechen an Dich.",
      "example_value": "Mut zur Lücke",
      "value": ""
    },
    "text": {
      "description": "Eine konkrete Beschreibung, wie Du diesen Wert im Arbeitsalltag erlebst und davon profitierst.",
      "example_value": "Wir erwarten nicht, dass Du auf alles eine Antwort hast. Bei uns darfst Du experimentieren, Fragen stellen und aus Fehlern lernen, um zu wachsen.",
      "value": ""
    }
  }
}
```
