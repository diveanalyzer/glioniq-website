#!/usr/bin/env python3
"""Generate static pages using approved originals and documented derivatives."""
from html import escape
from pathlib import Path
import json
import re
from hashlib import sha256
from laboratories import central_tree, explorer, neurobreath_art, breathing_methods, activity_cards, artwork_for, ARTWORK
from editorial import article_html, load_articles, listing_html

ROOT = Path(__file__).resolve().parents[1]
DOMAIN = (ROOT / 'CNAME').read_text().strip()
ICON_VERSION = json.loads((ROOT / 'public/images/branding-provenance.json').read_text())['icon_cache_version']


def head(title, description, path, prefix):
    asset_root = Path(__file__).resolve().parents[1]
    css_version = sha256((asset_root/'assets/site.css').read_bytes()).hexdigest()[:12]
    js_version = sha256((asset_root/'assets/site.js').read_bytes()).hexdigest()[:12]
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
  <link rel="icon" type="image/vnd.microsoft.icon" href="/favicon.ico?v={ICON_VERSION}" sizes="16x16 32x32 48x48">
  <link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png?v={ICON_VERSION}">
  <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png?v={ICON_VERSION}">
  <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png?v={ICON_VERSION}">
  <link rel="manifest" href="/site.webmanifest?v={ICON_VERSION}">
  <meta name="apple-mobile-web-app-title" content="GlionIQ">
  <link rel="stylesheet" href="{prefix}assets/site.css?v={css_version}">
  <script src="/assets/site.js?v={js_version}" defer></script>
</head>'''


def contact():
    return '''<section class="contact-section" id="contact" tabindex="-1" aria-labelledby="contact-heading">
      <h2 id="contact-heading">Contact</h2>
      <p>We look forward to connecting with you.</p>
      <p>Our contact details will be shared here when they are ready. In the meantime, discover the vision and science behind GlionIQ.</p>
      <a href="{story}">Read Our Story <span aria-hidden="true">→</span></a>
    </section>'''


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


def header(prefix, current):
    links = [('/', 'Home'), ('/#laboratories', 'Our Laboratories'), ('/about-us/', 'About Us'), ('/science/', 'Science & Research'), ('/blog/', 'Blog & Insights'), ('/contact/', 'Contact')]
    nav = ''.join(f'<a href="{path}"' + (' aria-current="page"' if label == current else '') + f'>{label}</a>' for path, label in links)
    return f'''<a class="skip-link" href="#main">Skip to content</a>
<header class="site-header"><a class="brand-link" href="/" aria-label="GlionIQ — Home"><img src="/public/images/development/header-brand.png" width="217" height="61" alt="GlionIQ"></a>
<details class="navigation" id="navigation" open><summary>Menu <span aria-hidden="true">☰</span></summary><nav aria-label="Main navigation">{nav}</nav></details>
<a class="search-link" href="/search/" aria-label="Search GlionIQ"><svg viewBox="0 0 24 24" width="25" height="25" aria-hidden="true"><circle cx="10" cy="10" r="7"></circle><path d="m15 15 6 6"></path></svg></a></header>'''


def footer(prefix=''):
    return '''<footer class="site-footer"><a class="footer-brand" href="/" aria-label="GlionIQ — Home"><img src="/public/images/glioniq-brain-transparent.png" width="768" height="768" alt="GlionIQ brain symbol" loading="lazy"></a>
<nav aria-label="Footer navigation"><a href="/#laboratories">Our Laboratories</a><a href="/about-us/">About Us</a><a href="/science/">Science & Research</a><a href="/blog/">Blog & Insights</a><a href="/contact/">Contact</a></nav><p>© 2026 GlionIQ. All Rights Reserved.</p></footer>'''


def lab_links():
    return ''.join(f'<a href="/laboratories/neuropath/{key}/"><img src="/public/images/development/{key}-symbol.png" width="60" height="54" alt="">{label} Lab</a>' for key, label in zip(['memory','attention','logic','flexibility'],['Memory','Attention','Logic','Flexibility']))


def home_html():
    platforms = json.loads((ROOT/'content/laboratories.json').read_text())
    blocks = [('/science/','science','The Science Behind Our Work','Research, principles and methodology.'),('/about-us/','story','Our Story','The meaning and vision behind GlionIQ.'),('/blog/','blog','Blog &amp; Insights','Articles, ideas and updates from our labs.'),('/journey/','journey','Join Our Journey','Stay informed about new releases and features.')]
    lower = ''.join(f'<a href="{url}"><img class="portal-icon" src="/public/images/development/{icon}-symbol.png" width="66" height="54" alt=""><h3>{title}</h3><p>{text}</p></a>' for url,icon,title,text in blocks)
    return f'''<section class="corporate-hero"><a class="hero-art" href="/" aria-label="GlionIQ — Home"><img src="/public/images/glioniq-hero-transparent.png" width="450" height="270" fetchpriority="high" alt="GlionIQ luminous blue brain and silver and gold wordmark"></a><div class="hero-copy"><h1>Where <em>Neuroscience</em> Meets <em>Lifelong Learning</em></h1><p>Science-inspired digital laboratories for learning, discovery and cognitive engagement at every stage of life.</p></div></section>
<section class="laboratories" id="laboratories" aria-labelledby="labs-title"><h2 class="section-title" id="labs-title">Our Laboratories</h2><p class="section-intro">Four unified platforms. A lifelong journey of learning, discovery, cognitive engagement and mindful well-being.</p>{explorer(platforms)}</section>
<section class="portals" aria-label="Discover GlionIQ">{lower}</section><section class="earth-cta" aria-label="Explore our platforms"><a class="gold-button" href="#laboratories">Explore the GlionIQ World <span aria-hidden="true">›</span></a></section>'''


def information_html(entry):
    e = escape
    artwork = entry.get('artwork')
    image = f'<img class="detail-art" src="/public/images/development/{artwork}.webp" width="364" height="230" alt="{e(entry["name"])} approved artwork">' if artwork else ''
    if entry['route'] in ARTWORK['routes']: image = artwork_for(entry['route'], detail=True)
    if entry['route'] == '/laboratories/neurobreath/': image = neurobreath_art(detail=True)
    methods = breathing_methods(entry['route'].strip('/').split('/')[-1] if entry.get('kind') == 'lab' else None) if entry['route'].startswith('/laboratories/neurobreath/') else ''
    info = ''.join(f'<div><dt>{label}</dt><dd>{e(entry[key])}</dd></div>' for key,label in [('audience','Intended audience'),('purpose','Purpose'),('status','Development status')] if entry.get(key))
    sections = ''
    for section in entry.get('sections',[]):
        paragraphs = ''.join(f'<p>{e(p)}</p>' for p in section.get('paragraphs',[]))
        items = '<ul>'+''.join(f'<li>{e(p)}</li>' for p in section['items'])+'</ul>' if section.get('items') else ''
        cards = activity_cards(entry['activities']) if section.get('activity_cards') else ''
        sections += f'<section><h2>{e(section["title"])}</h2>{paragraphs}{items}{cards}</section>'
    links = ''.join(f'<a class="gold-button" href="{e(link["href"])}">{e(link["label"])}</a>' for link in entry.get('links',[]))
    return f'''<div class="content-page"><a class="breadcrumb" href="/">← Home</a><div class="page-intro">{image}<div><p class="kicker">{e(entry.get('category',''))}</p><h1>{e(entry['name'])}</h1><p class="lead">{e(entry['introduction'])}</p></div></div><dl class="facts">{info}</dl>{methods}<div class="editorial">{sections}</div><div class="related-links">{links}</div></div>'''


def search_html():
    return '''<section class="content-page search-page"><a class="breadcrumb" href="/">← Home</a><h1>Search GlionIQ</h1><p>Explore our platforms, laboratories, story and science-informed approach.</p><form action="/search/" method="get" role="search" id="site-search"><label for="query">Search website content</label><div class="search-fields"><input id="query" name="q" type="search" maxlength="120" autocomplete="off" placeholder="Search GlionIQ laboratories, platforms and research…"><button class="gold-button" type="submit">Search</button></div></form><p id="search-status" role="status" aria-live="polite">Discover our platforms, laboratories and scientific insights.</p><div id="search-results"></div><noscript><p>Search needs JavaScript. Browse <a href="/#laboratories">Our Laboratories</a>, <a href="/about-us/">About Us</a>, <a href="/science/">Science &amp; Research</a>, <a href="/blog/">Blog &amp; Insights</a>, or <a href="/contact/">Contact</a>.</p></noscript></section>'''


def build():
    entries = json.loads((ROOT/'content/platforms.json').read_text()) + json.loads((ROOT/'content/pages.json').read_text())
    pages = [('/', 'GlionIQ — Where Neuroscience Meets Lifelong Learning', 'Science-inspired digital laboratories for learning, discovery and cognitive engagement at every stage of life.', home_html(), 'home-page', 'Home'),('/about-us/', 'About Us — Our Story', 'Our complete approved story, scientific commitment and vision.', '<article class="story">'+story_html()+'</article>'+contact().format(story='/about-us/'), 'about-page', 'About Us')]
    for entry in entries:
        pages.append((entry['route'],entry['name'],entry['introduction'],information_html(entry),'information-page',entry['name']))
    for platform in json.loads((ROOT/'content/laboratories.json').read_text()):
        pages.append((platform['route']+'explore/', platform['name']+' Laboratories', platform['description'], central_tree(platform, entries), 'information-page', platform['name']))
    pages.append(('/search/','Search GlionIQ','Search available GlionIQ website content.',search_html(),'information-page','Search'))
    articles = load_articles(ROOT / 'content/editorial')
    for article in articles:
        route = f'/{article["destination"]}/{article["slug"]}/'
        pages.append((route, article.get('seo_title') or article['title'], article.get('seo_description') or article['summary'], article_html(article), 'information-page', 'Blog & Insights' if article['destination']=='blog' else 'Science & Research'))
    for destination in ('blog', 'science'):
        selected = [a for a in articles if a['destination']==destination]
        if selected:
            pages = [(r,t,d,listing_html(selected,destination) if r==f'/{destination}/' else b,c,n) for r,t,d,b,c,n in pages]
    search = []
    for route,title,description,body,css,current in pages:
        target = ROOT / route.strip('/') / 'index.html' if route!='/' else ROOT/'index.html'
        target.parent.mkdir(parents=True,exist_ok=True)
        document = head(escape(title),escape(description),route.lstrip('/'),'/') + f'\n<body class="{css}">{header("/",current)}<main id="main" tabindex="-1">{body}</main>{footer()}</body></html>\n'
        target.write_text(document)
        if route!='/search/':
            from html import unescape
            plain = re.sub(r'\s+',' ',unescape(re.sub('<[^>]+>',' ',body))).strip()
            search.append({'url':route,'title':title,'description':description,'text':plain})
    current_routes = [page[0] for page in pages]
    manifest_path = ROOT/'assets/generated-routes.json'
    previous_routes = json.loads(manifest_path.read_text()) if manifest_path.exists() else []
    for old_route in set(previous_routes)-set(current_routes):
        # Only retired generated editorial pages may be removed; never site pages.
        if re.fullmatch(r'/(blog|science)/[a-z0-9]+(?:-[a-z0-9]+)*/', old_route):
            target = ROOT/old_route.strip('/')/'index.html'
            if target.is_file(): target.unlink()
    manifest_path.write_text(json.dumps(current_routes,indent=2)+'\n')
    (ROOT/'assets/search-index.json').write_text(json.dumps(search,ensure_ascii=False,indent=2)+'\n')
    print(f'Built {len(pages)} local pages; indexed {len(search)} content pages. No publication performed.')


if __name__ == '__main__':
    build()
