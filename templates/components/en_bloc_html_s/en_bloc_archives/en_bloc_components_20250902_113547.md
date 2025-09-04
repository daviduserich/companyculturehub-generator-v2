# Komponenten-Zusammenzug (en bloc)

**Generiert am:** 2025-09-02 11:35:47

## Kontext
Dieses Dokument enthält den gesamten HTML-Quellcode aller aktiven Webseiten-Module (Komponenten).
Diese Module werden von einem Python-Skript verwendet, um dynamisch eine vollständige JSON-Content-Vorlage für eine Webseite zu generieren.

Jedes Modul ist eine eigenständige HTML-Datei, die Platzhalter im Format `{{ placeholder_name }}` enthält.

**Zweck dieses Dokuments:**
Einem Large Language Model (LLM) einen vollständigen Überblick über alle vorhandenen Module zu geben, um Analysen, Vorschläge oder Code-Generierungen durchzuführen.

---

## Modul: `benefits_section.html`

```html
<!-- Benefits Section -->
<section class="benefits">
    <div class="container">
        <div class="section-header">
            <h2>{{benefits_section.headline}}</h2>
            <p class="description">{{benefits_section.description}}</p>
        </div>
        
        <div class="benefits-grid">
            <!-- BEGIN_LIST_ITEM:benefits_section.benefits_list -->
            <div class="benefit-card">
                <div class="benefit-icon">{{icon}}</div>
                <h3>{{title}}</h3>
                <p>{{text}}</p>
            </div>
            <!-- END_LIST_ITEM:benefits_section.benefits_list -->
        </div>
    </div>
</section>

<style>
    /* --- Gemeinsame Basis-Stile für die Benefits-Sektion --- */
    .benefits {
        padding: var(--spacing-section-large) 0;
        color: white; /* Text ist in beiden Varianten weiss */
    }
    
    .benefits .section-header h2,
    .benefits .section-header .description {
        color: white;
    }
    
    .benefits-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
        gap: 40px;
    }

    .benefit-card {
        padding: 40px 30px;
        text-align: center;
        transition: transform 0.3s ease, background-color 0.3s ease;
    }
    
    .benefit-icon { font-size: 3.5rem; margin-bottom: 25px; opacity: 0.9; }
    .benefit-card h3 { font-size: 1.6rem; margin-bottom: 20px; font-weight: 600; }
    .benefit-card p { font-size: 1.1rem; line-height: 1.6; opacity: 0.9; }

    /* --- Stil-spezifische Anpassungen (Der Baukasten) --- */

    /* Hintergrund-Stile */
    .bg-solid .benefits {
        background: var(--color-primary); /* Klassisch: Einfarbiger Hintergrund */
    }
    .bg-gradient .benefits {
        background: var(--benefits-gradient); /* Stylisch: Der coole Verlauf */
    }

    /* Karten-Stile */
    .card-flat .benefit-card {
        background: transparent;
        border: 1px solid rgba(255,255,255,0.3);
        border-radius: 4px;
    }
    .card-shadow .benefit-card {
        background: rgba(0,0,0,0.15); /* Dunkelt den Hintergrund leicht ab */
        border-radius: var(--border-radius-card);
        border: 1px solid rgba(255,255,255,0.1);
    }
    .card-glass .benefit-card {
        background: rgba(255,255,255,0.1);
        backdrop-filter: blur(10px); /* Der "Glass"-Effekt */
        border-radius: 20px;
        border: 1px solid rgba(255,255,255,0.2);
    }

    /* Animations-Stile (betrifft den Hover-Effekt) */
    .anim-subtle .benefit-card:hover {
        background: rgba(0,0,0,0.25); /* Klassisch: Wird beim Hover einfach etwas dunkler */
    }
    .anim-playful .benefit-card:hover {
        transform: translateY(-10px); /* Stylisch: Die "Schwebe"-Animation */
        background: rgba(255,255,255,0.15);
    }

</style>
```


## Modul: `career_cta_section.html`

```html
<section class="career-cta">
    <div class="container">
        <div>
            <h2>{{career_cta_section.headline}}</h2>
            <p class="description">{{career_cta_section.description}}</p>
            <div class="cta-buttons">
                <a href="{{links.career_page_url}}" class="btn btn-primary">{{labels.career_button_text}}</a>
                <a href="{{links.application_form_url}}" class="btn btn-secondary">{{labels.application_button_text}}</a>
            </div>
        </div>
    </div>
</section>
<style>
    /* --- Gemeinsame Basis-Stile für die CTA-Sektion --- */
    .career-cta {
        padding: var(--spacing-section-large) 0;
        background: var(--color-secondary);
        color: var(--text-on-secondary);
        text-align: center;
    }
    
    .career-cta h2 { font-size: 3rem; margin-bottom: 25px; font-weight: 600; }
    .career-cta .description { font-size: 1.3rem; margin-bottom: 50px; opacity: 0.9; max-width: 600px; margin-left: auto; margin-right: auto; }
    .cta-buttons { display: flex; gap: 30px; justify-content: center; flex-wrap: wrap; }

    /* --- Gemeinsame Basis-Stile für ALLE Buttons --- */
    .btn {
        display: inline-block;
        padding: 18px 40px;
        text-decoration: none;
        font-weight: 600;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        border: 2px solid transparent;
        cursor: pointer;
    }

    /* --- Stil-spezifische Anpassungen (Der Baukasten) --- */

    /* Button-Formen */
    .btn-sharp .btn { border-radius: 4px; }
    .btn-rounded .btn { border-radius: 12px; }
    .btn-pill .btn { border-radius: 50px; }

    /* Primärer Button (Akzentfarbe) */
    .btn-primary {
        background: var(--color-accent, var(--color-primary));
        color: var(--text-on-primary);
    }

    /* Sekundärer Button (Outline-Stil) */
    .btn-secondary {
        background: transparent;
        color: var(--text-on-secondary);
        border-color: var(--text-on-secondary);
    }
    .btn-secondary:hover {
        background: var(--text-on-secondary);
        color: var(--color-secondary);
    }

    /* Animations-Stile (Hover-Effekte) */
    .anim-subtle .btn:hover {
        filter: brightness(110%); /* Klassisch: Wird nur heller */
    }
    .anim-playful .btn:hover {
        transform: translateY(-3px); /* Stylisch: "Schwebe"-Effekt */
        box-shadow: 0 10px 25px rgba(0,0,0,0.2);
    }

    /* Media Query für mobile Ansicht bleibt gleich */
    @media (max-width: 768px) {
        .cta-buttons { flex-direction: column; align-items: center; }
        .career-cta h2 { font-size: 2.2rem; }
    }
</style>
```


## Modul: `culture_section.html`

```html
<section class="culture">
    <div class="container">
        <div class="section-header">
            <h2>{{culture_section.headline}}</h2>
            <p class="description">{{culture_section.description}}</p>
        </div>
        <div class="values-grid">
            <!-- BEGIN_LIST_ITEM:culture_section.values_list -->


            <div class="value-card">
                <div class="value-icon">{{icon}}</div>
                <h3>{{title}}</h3>
                <p>{{text}}</p>
            </div>
            <!-- END_LIST_ITEM:culture_section.values_list -->
        </div>
        <div class="culture-image">
            <img src="{{culture_section.image_url}}" alt="{{culture_section.image_alt_text}}">
        </div>
    </div>
</section>
<style>
    .culture { padding: var(--spacing-section-large) 0; background: #f8f9fa; }
    .section-header { text-align: center; margin-bottom: var(--spacing-section-medium); }
    .section-header h2 { font-size: var(--font-size-h2); color: var(--color-secondary); margin-bottom: 20px; font-weight: 600; }
    .section-header .description { font-size: 1.2rem; color: #6c757d; max-width: 700px; margin: 0 auto; }
    .values-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 40px; margin-bottom: var(--spacing-section-medium); }
    .value-card { background: white; padding: 40px 30px; border-radius: var(--border-radius-card); text-align: center; box-shadow: 0 10px 30px rgba(0,0,0,0.1); transition: transform 0.3s ease, box-shadow 0.3s ease; }
    .value-card:hover { transform: translateY(-10px); box-shadow: 0 20px 40px rgba(0,0,0,0.15); }
    .value-icon { font-size: 3rem; margin-bottom: 20px; color: var(--color-primary); }
    .value-card h3 { font-size: 1.5rem; margin-bottom: 15px; color: var(--color-secondary); }
    .value-card p { color: #6c757d; line-height: 1.6; }
    .culture-image { text-align: center; margin-top: 40px; }
    .culture-image img { max-width: 100%; border-radius: var(--border-radius-card); box-shadow: 0 15px 35px rgba(0,0,0,0.1); }
</style>
```


## Modul: `diversity_section.html`

```html
<!-- Diversity Section -->
<section class="diversity">
    <div class="container">
        <h2>{{diversity_section.headline}}</h2>
        <p>{{diversity_section.description}}</p>
        <img src="{{image_url}}" alt="{{image_alt_text}}">
    </div>
</section>

<style>
    .diversity { padding: var(--spacing-section-large) 0; text-align: center; }
    .diversity img { max-width: 100%; border-radius: 10px; }

    /* Varianten */
    .bg-solid .diversity { background: var(--color-accent); color: var(--text-on-accent); }
    .anim-playful .diversity:hover img { transform: scale(1.05); transition: 0.3s; }
</style>
```


## Modul: `footer_section.html`

```html
<footer class="footer">
    <div class="container">
        <div class="footer-links">
            <a href="{{links.imprint_url}}">{{labels.imprint_text}}</a>
            <a href="{{links.privacy_url}}">{{labels.privacy_text}}</a>
            <a href="{{links.contact_url}}">{{labels.contact_text}}</a>
        </div>
        <p>{{footer_section.copyright_text}}</p>
    </div>
</footer>
</body>
</html>
<style>
    .footer { background: #1a1a1a; color: #ccc; padding: 40px 0; text-align: center; }
    .footer-links { display: flex; justify-content: center; gap: 40px; margin-bottom: 20px; flex-wrap: wrap; }
    .footer-links a { color: #ccc; text-decoration: none; transition: color 0.3s ease; }
    .footer-links a:hover { color: var(--color-primary); }
    .footer p { font-size: 0.9rem; opacity: 0.7; }
</style>
```


## Modul: `hero_section.html`

```html
<section class="hero">
    <div class="container">
        <div class="hero-content">
            <h1>{{hero_section.headline}}</h1>
            <p class="subtitle">{{hero_section.subheadline}}</p>
            <p class="description">{{hero_section.description}}</p>
            <div class="hero-image">
                <img src="{{hero_section.image_url}}" alt="{{hero_section.image_alt_text}}">
            </div>
        </div>
    </div>
</section>
<style>
    /* --- Gemeinsame Basis-Stile für die Hero-Sektion --- */
    .hero {
        color: var(--text-on-primary); /* Dynamische Textfarbe für beide Stile */
        padding: var(--spacing-section-large) 0;
        text-align: center;
        position: relative;
        overflow: hidden;
        transition: background 0.5s ease; /* Sanfter Übergang, falls sich Stile ändern */
    }
    
    .hero-content { position: relative; z-index: 2; }
    .hero h1 { font-size: var(--font-size-h1); font-weight: 700; margin-bottom: 20px; }
    .hero .subtitle { font-size: 1.4rem; margin-bottom: 15px; opacity: 0.9; }
    .hero .description { font-size: 1.1rem; margin-bottom: 40px; max-width: 600px; margin-left: auto; margin-right: auto; opacity: 0.8; }
    .hero-image { margin-top: 40px; max-width: 800px; margin-left: auto; margin-right: auto; }
    .hero-image img { width: 100%; height: auto; display: block; }

    /* --- Stil-spezifische Anpassungen (Der Baukasten) --- */

    /* Hintergrund-Stile */
    .bg-solid .hero {
        background: var(--color-primary);
    }
    .bg-gradient .hero {
        background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-secondary) 100%);
    }

    /* Karten-Stile (betrifft das Bild in der Hero-Sektion) */
    .card-shadow .hero-image {
        border-radius: var(--border-radius-card);
        overflow: hidden;
        box-shadow: 0 15px 30px rgba(0,0,0,0.2);
    }
    .card-glass .hero-image {
        border-radius: var(--border-radius-card);
        overflow: hidden;
        box-shadow: 0 20px 40px rgba(0,0,0,0.3);
    }
    .card-flat .hero-image {
        border-radius: 4px; /* Etwas eckiger für einen flachen Stil */
        box-shadow: none;
    }

    /* Animations-Stile (subtile Effekte für den Text) */
    .anim-subtle .hero h1, .anim-subtle .hero p {
        /* Keine Animation für den klassischen Stil */
    }
    .anim-playful .hero h1 {
        /* Beispiel: Leichter Schatten für mehr Tiefe im stylischen Modus */
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    .anim-playful .hero::before {
        /* Der abdunkelnde Overlay-Effekt nur im stylischen Modus */
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0; bottom: 0;
        background: rgba(0,0,0,0.3);
        z-index: 1;
    }

</style>
```


## Modul: `location_section.html`

```html
<!-- Location Section -->
<section class="location">
    <div class="container">
        <h2>{{location_section.headline}}</h2>
        <p>{{location_section.description}}</p>
        <img src="{{map_url}}" alt="{{image_alt_text}}">
    </div>
</section>

<style>
    .location { padding: var(--spacing-section-medium) 0; text-align: center; }
    .location img { max-width: 80%; }

    /* Varianten */
    .bg-gradient .location { background: var(--location-gradient); }
    .card-flat .location { border: 1px solid var(--color-accent); border-radius: 10px; }
</style>
```


## Modul: `logo_header_section.html`

```html
<header class="logo-header-section">
    <div class="container">
        <div class="logo">
            <a href="{{project_config.canonical_url}}">
                <img src="{{design.logo.url}}" alt="{{identity.company_name}} Logo">
            </a>
        </div>
    </div>
</header>
<style>
    .logo-header-section {
        padding: 20px 0;
        background-color: #fff;
        border-bottom: 1px solid #eee;
        position: sticky;
        top: 0;
        z-index: 1000;
        transition: padding 0.3s ease;
    }
    .logo-header-section .logo img {
        height: 50px; /* Standardhöhe */
        width: auto;
        transition: height 0.3s ease;
    }
    body.scrolled .logo-header-section {
        padding: 10px 0;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    body.scrolled .logo-header-section .logo img {
        height: 40px; /* Kleinere Höhe beim Scrollen */
    }
</style>
<script>
    document.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            document.body.classList.add('scrolled');
        } else {
            document.body.classList.remove('scrolled');
        }
    });
</script>
```


## Modul: `navigation_section.html`

```html
<!-- Navigation Section -->
<nav class="navigation">
    <ul class="nav-list">
        <!-- BEGIN_LIST_ITEM:navigation.nav_items -->
        <li><a href="{{url}}">{{label}}</a></li>
        <!-- END_LIST_ITEM:navigation.nav_items -->
    </ul>
</nav>

<style>
    .navigation { background: var(--color-secondary); padding: 10px 0; }
    .nav-list { display: flex; list-style: none; justify-content: center; gap: 20px; }
    .nav-list a { color: var(--text-on-secondary); text-decoration: none; }

    /* Varianten */
    .bg-solid .navigation { background: var(--color-primary); }
    .bg-gradient .navigation { background: var(--nav-gradient); }
</style>
```


## Modul: `stolz_section.html`

```html
<!-- Stolz Section -->
<section class="stolz">
    <div class="container">
        <h2>{{stolz_section.headline}}</h2>
        <p>{{stolz_section.description}}</p>
        <div class="highlights-grid">
            <!-- BEGIN_LIST_ITEM:stolz_section.highlights_list -->
            <div class="highlight-item">
                <h3>{{title}}</h3>
                <p>{{text}}</p>
            </div>
            <!-- END_LIST_ITEM:stolz_section.highlights_list -->
        </div>
    </div>
</section>

<style>
    .stolz { padding: var(--spacing-section-medium) 0; background: var(--color-primary); color: white; }
    .highlights-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 25px; }
    .highlight-item { padding: 20px; border: 1px solid rgba(255,255,255,0.2); border-radius: 8px; }

    /* Varianten */
    .card-shadow .highlight-item { box-shadow: 0 4px 8px rgba(0,0,0,0.2); }
    .bg-gradient .stolz { background: var(--stolz-gradient); }
</style>
```


## Modul: `story_telling_section.html`

```html
<!-- Story Telling Section -->
<section class="story-telling">
    <div class="container">
        <h2>{{story_telling_section.headline}}</h2>
        <p>{{story_telling_section.text}}</p>
        <img src="{{image_url}}" alt="{{image_alt_text}}">
    </div>
</section>

<style>
    .story-telling { padding: var(--spacing-section-large) 0; }
    .story-telling img { max-width: 100%; }

    /* Varianten (für Multi-Instanzen: Styles per Instance anpassen) */
    .bg-solid .story-telling { background: var(--color-secondary); }
    .anim-subtle .story-telling:hover { opacity: 0.9; transition: 0.3s; }
</style>
```


## Modul: `team_section.html`

```html
<section class="team">
    <div class="container">
        <div class="section-header">
            <h2>{{team_section.headline}}</h2>
            <p class="description">{{team_section.description}}</p>
        </div>
        <div class="testimonial">
            <p class="testimonial-quote">{{team_section.testimonial_quote}}</p>
            <div class="testimonial-author">
                <div class="author-info">
                    <h4>{{team_section.testimonial_author_name}}</h4>
                    <p>{{team_section.testimonial_author_title}}</p>
                </div>
            </div>
        </div>
        <div class="team-image">
            <img src="{{team_section.image_url}}" alt="{{team_section.image_alt_text}}">
        </div>
    </div>
</section>
<style>
    .team { padding: var(--spacing-section-large) 0; background: white; }
    .testimonial { background: #f8f9fa; padding: 60px 40px; border-radius: 20px; text-align: center; margin-bottom: var(--spacing-section-medium); position: relative; }
    .testimonial::before { content: '"'; font-size: 6rem; color: var(--color-primary); position: absolute; top: 10px; left: 40px; font-family: serif; opacity: 0.3; }
    .testimonial-quote { font-size: 1.4rem; font-style: italic; color: var(--color-secondary); margin-bottom: 30px; position: relative; z-index: 1; }
    .testimonial-author { display: flex; align-items: center; justify-content: center; gap: 20px; }
    .author-info h4 { font-size: 1.2rem; color: var(--color-secondary); margin-bottom: 5px; }
    .author-info p { color: #6c757d; font-size: 1rem; }
    .team-image { text-align: center; }
    .team-image img { max-width: 100%; border-radius: var(--border-radius-card); box-shadow: 0 15px 35px rgba(0,0,0,0.1); }
    @media (max-width: 768px) {
        .testimonial { padding: 40px 20px; }
        .testimonial::before { font-size: 4rem; top: 5px; left: 20px; }
    }
</style>
```


## Modul: `technik_header.html`

```html
<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{meta_data.page_title}}</title>
    <meta name="description" content="{{meta_data.meta_description}}">
    <link rel="canonical" href="{{project_config.canonical_url}}" />
    <link rel="icon" href="{{design.logo.favicon_url}}">
    <script>
        !function(f,b,e,v,n,t,s){if(f.fbq)return;n=f.fbq=function(){n.callMethod?
        n.callMethod.apply(n,arguments):n.queue.push(arguments)};if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
        n.queue=[];t=b.createElement(e);t.async=!0;t.src=v;s=b.getElementsByTagName(e)[0];
        s.parentNode.insertBefore(t,s)}(window, document,'script','https://connect.facebook.net/en_US/fbevents.js'  );
        fbq('init', '{{integrations.meta_pixel_id}}');
        fbq('track', 'PageView');
    </script>
    <noscript><img height="1" width="1" style="display:none" src="https://www.facebook.com/tr?id={{integrations.meta_pixel_id}}&ev=PageView&noscript=1"/></noscript>
    <script src="{{integrations.tracking_script_url}}"></script>
    <style>
        :root {
            --color-primary: {{design.branding.primary_color}};
            --color-secondary: {{design.branding.secondary_color}};
            --color-text: {{design.branding.text_color}};
            --font-family-base: {{design.branding.font_family}};
            --color-accent: {{design.branding.accent_color}};
            --text-on-primary: {{design.branding.text_on_primary}};
            --text-on-secondary: {{design.branding.text_on_secondary}};
            --benefits-gradient: {{design.branding.benefits_gradient.css_value}};
            --spacing-section-large: 100px;
            --spacing-section-medium: 60px;
            --border-radius-card: 15px;
            --font-size-h1: 3.5rem;
            --font-size-h2: 2.8rem;
            --font-size-body: 1rem;
        }
        @media (max-width: 768px  ) {
            :root { --font-size-h1: 2.5rem; --font-size-h2: 2.2rem; --spacing-section-large: 60px; }
        }
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: var(--font-family-base); line-height: 1.6; color: var(--color-text); }
        .container { max-width: 1200px; margin: 0 auto; padding: 0 20px; }
    </style>
</head>
<!-- KORREKTUR: Der Body-Tag wird dynamisch mit den Stil-Klassen befüllt -->
<body class="{{theme_classes}}">
```


## Modul: `values_section.html`

```html
<!-- Values Section -->
<section class="values">
    <div class="container">
        <h2>{{values_section.headline}}</h2>
        <div class="values-grid">
            <!-- BEGIN_LIST_ITEM:values_section.values_list -->
            <div class="value-item">
                <div class="value-icon">{{icon}}</div>
                <h3>{{title}}</h3>
                <p>{{text}}</p>
            </div>
            <!-- END_LIST_ITEM:values_section.values_list -->
        </div>
    </div>
</section>

<style>
    .values { padding: var(--spacing-section-medium) 0; background: var(--color-background); }
    .values-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 30px; }
    .value-item { text-align: center; }

    /* Varianten */
    .bg-gradient .values { background: var(--values-gradient); }
    .card-glass .value-item { background: rgba(255,255,255,0.1); backdrop-filter: blur(10px); border-radius: 15px; }
</style>
```
