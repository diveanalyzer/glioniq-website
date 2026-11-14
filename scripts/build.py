#!/usr/bin/env python3
"""Generate static pages using approved originals and documented derivatives."""
from html import escape
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
DOMAIN = (ROOT / 'CNAME').read_text().strip()


def head(title, description, path, prefix):
    url = f'https://{DOMAIN}/{path}'
    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="theme-color" content="#020d20">
  <title>{title}</title>
  <meta name="description" content="{description}">
  <link rel="canonical" href="{url}">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="GlionIQ">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{description}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="https://{DOMAIN}/public/images/glioniq-logo-official.PNG">
  <meta property="og:image:width" content="1536">
  <meta property="og:image:height" content="1024">
  <meta property="og:image:alt" content="GlionIQ — Grow Your Mind. Enrich Your Life.">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="icon" href="{prefix}favicon.ico" sizes="16x16 32x32 48x48">
  <link rel="icon" type="image/png" sizes="32x32" href="{prefix}favicon-32x32.png">
  <link rel="icon" type="image/png" sizes="16x16" href="{prefix}favicon-16x16.png">
  <link rel="apple-touch-icon" sizes="180x180" href="{prefix}apple-touch-icon.png">
  <link rel="manifest" href="{prefix}site.webmanifest">
  <meta name="apple-mobile-web-app-title" content="GlionIQ">
  <link rel="stylesheet" href="{prefix}assets/site.css">
</head>'''


def header(prefix, current):
    links = [('./', 'Home'), ('about-us/', 'About Us'), ('#contact', 'Contact')]
    nav = ''.join(f'<a href="{prefix + path if not path.startswith("#") else path}"'
                  + (' aria-current="page"' if label == current else '')
                  + f'>{label}</a>' for path, label in links)
    return f'''<a class="skip-link" href="#main">Skip to content</a>
  <header class="site-header">
    <a class="brand-link" href="/" aria-label="GlionIQ — Home">
      <img src="{prefix}public/images/glioniq-brain-transparent.png" width="768" height="768" decoding="async" alt="GlionIQ brain symbol">
    </a>
    <nav aria-label="Main navigation">{nav}</nav>
  </header>'''


def contact():
    return '''<section class="contact-section" id="contact" tabindex="-1" aria-labelledby="contact-heading">
      <h2 id="contact-heading">Contact</h2>
      <p>We look forward to connecting with you.</p>
      <p>Our contact details will be shared here when they are ready. In the meantime, discover the vision and science behind GlionIQ.</p>
      <a href="{story}">Read Our Story <span aria-hidden="true">→</span></a>
    </section>'''


def footer(prefix):
    return f'''<footer class="site-footer">
    <a class="footer-brand" href="/" aria-label="GlionIQ — Home">
      <img src="{prefix}public/images/glioniq-brain-transparent.png" width="768" height="768" loading="lazy" decoding="async" alt="GlionIQ brain symbol">
    </a>
    <p>© 2026 GlionIQ. All Rights Reserved.</p>
    <a href="#contact">Contact</a>
  </footer>'''


def story_html():
    blocks = (ROOT / 'content/about-us.md').read_text().strip().split('\n\n')
    result, section_open = [], False
    for block in blocks:
        match = re.match(r'^(#{1,4}) (.+)$', block)
        if match:
            level, title = len(match[1]), match[2]
            if level == 3:
                if section_open:
                    result.append('</section>')
                section_id = re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')
                result.append(f'<section class="chapter" aria-labelledby="{section_id}">')
                section_open = True
                result.append(f'<h3 id="{section_id}">{escape(title)}</h3>')
            else:
                result.append(f'<h{level}>{escape(title)}</h{level}>')
        else:
            kind = ' class="closing"' if block.startswith('GlionIQ — Where') else ''
            if block == 'Inspired by Research. Guided by Evidence. Continuously Evolving.':
                kind = ' class="statement"'
            result.append(f'<p{kind}>{escape(block)}</p>')
    if section_open:
        result.append('</section>')
    return '\n'.join(result)


def build():
    home = head('GlionIQ — Where Neuroscience Meets Lifelong Learning',
                'Exploring the science of the mind. Creating meaningful learning experiences for every generation. Discover the vision and science behind GlionIQ.', '', '')
    home += f'''
<body class="home-page">
  {header('', 'Home')}
  <main id="main" tabindex="-1">
    <section class="hero" aria-labelledby="hero-heading">
      <a class="hero-art" href="/" aria-label="GlionIQ — Home">
        <img src="public/images/glioniq-hero-transparent.png" width="450" height="270" fetchpriority="high" decoding="async" alt="GlionIQ: a luminous blue brain with gold neural connections above the silver and gold wordmark">
      </a>
      <h1 id="hero-heading">Where <em>Neuroscience</em> Meets <span>Lifelong Learning</span></h1>
      <p>Exploring the science of the mind. Creating meaningful learning experiences for every generation.</p>
    </section>
    <section class="coming-soon" aria-labelledby="coming-heading">
      <p class="eyebrow">COMING SOON</p>
      <h2 id="coming-heading">Something Extraordinary Is Taking Shape.</h2>
      <p>Our new digital home is currently under development. Discover the vision and science behind GlionIQ while we prepare for launch.</p>
    </section>
    <section class="about-preview" aria-labelledby="about-heading">
      <h2 class="section-title" id="about-heading">About Us</h2>
      <p class="section-subtitle">The Science Behind Our Name</p>
      <div class="science-cards">
        <article class="science-card"><span class="science-icon glia" aria-hidden="true"></span><div><h3>GLIA</h3><p>Supporting neural function, learning and memory.</p></div></article>
        <article class="science-card"><span class="science-icon neuron" aria-hidden="true"></span><div><h3>NEURON</h3><p>The extraordinary power of neural connections.</p></div></article>
        <article class="science-card"><span class="science-icon iq" aria-hidden="true"></span><div><h3>IQ</h3><p>Curiosity, intelligence and the pursuit of knowledge.</p></div></article>
      </div>
      <a class="story-link" href="about-us/">Read Our Story <span aria-hidden="true">⟶</span></a>
    </section>
    <section class="vision" aria-labelledby="vision-heading">
      <h2 class="section-title" id="vision-heading">Our Vision</h2>
      <p>We believe that curiosity belongs to every generation, learning should never stop, and technology inspired by science can enrich the way we think, discover, and grow.</p>
    </section>
    {contact().format(story='about-us/')}
  </main>
  {footer('')}
</body>
</html>
'''
    about = head('About Us — Our Story | GlionIQ',
                 'A Healthy Body. A Clear Mind. A Fuller Life. Our complete story, scientific commitment, and vision for learning and cognitive engagement at every age.', 'about-us/', '../')
    about += f'''
<body class="about-page">
  {header('../', 'About Us')}
  <main id="main" tabindex="-1">
    <article class="story">
{story_html()}
    </article>
    {contact().format(story='./')}
  </main>
  {footer('../')}
</body>
</html>
'''
    (ROOT / 'index.html').write_text(home)
    (ROOT / 'about-us/index.html').write_text(about)
    print('Built Home and About Us. CNAME:', DOMAIN)


if __name__ == '__main__':
    build()
