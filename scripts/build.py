#!/usr/bin/env python3
"""Render the approved Markdown into buildless, GitHub Pages-ready HTML."""
from html import escape
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
DOMAIN = (ROOT / "CNAME").read_text().strip()


def inline(text):
    return re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", escape(text))


def head(title, description, path, prefix):
    url = f"https://{DOMAIN}/{path}"
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
  <meta property="og:image:alt" content="Official GlionIQ logo — Grow Your Mind. Enrich Your Life.">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="stylesheet" href="{prefix}assets/site.css">
</head>'''


def nav(prefix, current):
    return '<nav aria-label="Main navigation">' + ''.join(
        f'<a href="{prefix}{path}"' + (' aria-current="page"' if label == current else '')
        + f'>{label}</a>' for path, label in [('./', 'Home'), ('about-us/', 'About Us')]
    ) + '</nav>'


def story_html():
    blocks = (ROOT / 'content/about-us.md').read_text().strip().split('\n\n')
    result = []
    section_open = False
    cards_open = False
    for index, block in enumerate(blocks):
        if block.startswith('### '):
            if section_open:
                result.append('</section>')
            title = block[4:]
            section_id = re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')
            kind = 'principle' if title.startswith(('GLIA', 'NEURON', 'IQ')) else 'chapter'
            if title.startswith('Building Cognitive'):
                kind += ' reserve'
            result.append(f'<section class="{kind}" aria-labelledby="{section_id}"><h3 id="{section_id}">{escape(title)}</h3>')
            section_open = True
        elif block.startswith('# '):
            result.append(f'<h1>{escape(block[2:])}</h1>')
        elif block.startswith('## '):
            result.append(f'<h2>{escape(block[3:])}</h2>')
        elif block.startswith(('**Early Development**', '**Lifelong Learning**', '**Healthy Cognitive Aging**')):
            if not cards_open:
                result.append('<div class="life-stages">')
                cards_open = True
            result.append(f'<p>{inline(block)}</p>')
            if block.startswith('**Healthy Cognitive Aging**'):
                result.append('</div>')
                cards_open = False
        else:
            kind = ' class="opening"' if index == 2 else ''
            if block == '**Grow Your Mind. Enrich Your Life.**':
                kind = ' class="closing"'
            result.append(f'<p{kind}>{inline(block)}</p>')
    if section_open:
        result.append('</section>')
    return '\n'.join(result)


def build():
    home = head('GlionIQ — Coming Soon',
                'GlionIQ is preparing for launch. Discover the science behind our name and our vision for lifelong learning and cognitive engagement.', '', '')
    home += f'''
<body class="home-page">
  <a class="skip-link" href="#main">Skip to content</a>
  <header class="home-header">{nav('', 'Home')}</header>
  <main id="main" tabindex="-1" class="home-main">
    <h1 class="visually-hidden">GlionIQ — Coming Soon</h1>
    <figure class="launch-art">
      <img src="public/images/glioniq-coming-soon.PNG" width="1221" height="1288" fetchpriority="high" decoding="async"
           alt="GlionIQ. Where Neuroscience Meets Lifelong Learning. Coming soon: our new digital home is currently under development. Discover the vision and science behind GlionIQ while we prepare for launch.">
      <a class="art-link art-logo" href="./" aria-label="GlionIQ — Home"></a>
      <a class="art-link art-home" href="./" aria-label="Home" aria-current="page"></a>
      <a class="art-link art-about" href="about-us/" aria-label="About Us"></a>
      <a class="art-link art-contact" href="mailto:info@glioniq.tech" aria-label="Contact GlionIQ by email"></a>
      <a class="art-link art-story" href="about-us/" aria-label="Read Our Story"></a>
      <a class="art-link art-footer-logo" href="./" aria-label="GlionIQ — Home"></a>
      <a class="art-link art-email" href="mailto:info@glioniq.tech" aria-label="Email info@glioniq.tech"></a>
    </figure>
    <details class="launch-message">
      <summary>Read the launch message</summary>
      <p>Something Extraordinary Is Taking Shape.</p>
      <p>Our new digital home is currently under development. Discover the vision and science behind GlionIQ while we prepare for launch.</p>
      <a href="about-us/">Read Our Story <span aria-hidden="true">→</span></a>
    </details>
  </main>
</body>
</html>
'''
    about = head('About Us — The Science Behind GlionIQ',
                 'Explore the story of GlionIQ: glia, neurons, curiosity, and our vision for lifelong learning and cognitive engagement.', 'about-us/', '../')
    about += f'''
<body class="about-page">
  <a class="skip-link" href="#main">Skip to content</a>
  <header class="about-header">
    <a class="brand" href="../" aria-label="GlionIQ — Home">
      <img src="../public/images/glioniq-logo-official.PNG" width="1536" height="1024" fetchpriority="high" decoding="async"
           alt="GlionIQ — Grow Your Mind. Enrich Your Life.">
    </a>
    {nav('../', 'About Us')}
  </header>
  <main id="main" tabindex="-1">
    <article class="story">
{story_html()}
    </article>
  </main>
  <footer class="site-footer"><a href="../">Home</a><span>© 2026 GlionIQ. All Rights Reserved.</span></footer>
</body>
</html>
'''
    (ROOT / 'index.html').write_text(home)
    (ROOT / 'about-us').mkdir(exist_ok=True)
    (ROOT / 'about-us/index.html').write_text(about)
    print('Built index.html and about-us/index.html from the approved source.')


if __name__ == '__main__':
    build()
