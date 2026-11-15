#!/usr/bin/env python3
"""Generate static pages using approved originals and documented derivatives."""
from html import escape
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
DOMAIN = (ROOT / 'CNAME').read_text().strip()
ICON_VERSION = json.loads((ROOT / 'public/images/branding-provenance.json').read_text())['icon_cache_version']


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
  <link rel="icon" type="image/vnd.microsoft.icon" href="/favicon.ico?v={ICON_VERSION}" sizes="16x16 32x32 48x48">
  <link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png?v={ICON_VERSION}">
  <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png?v={ICON_VERSION}">
  <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png?v={ICON_VERSION}">
  <link rel="manifest" href="/site.webmanifest?v={ICON_VERSION}">
  <meta name="apple-mobile-web-app-title" content="GlionIQ">
  <link rel="stylesheet" href="{prefix}assets/site.css">
  <script src="/assets/site.js" defer></script>
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
    cards = []
    platforms = [('trampolina','Trampolina', 'Children’s Learning &amp; Development Laboratories',''),('dr-quiz','Dr. Quiz','Knowledge &amp; Discovery Lab','Fascinating facts, quizzes and mind-expanding challenges.'),('neuropath','NeuroPath','Cognitive Engagement Laboratories','A suite of brain-training labs for memory, attention, logic and cognitive flexibility.')]
    for key,name,category,description in platforms:
        tree = f'<details class="lab-tree" id="neuro-labs" open><summary>NeuroPath laboratories <span aria-hidden="true">⌄</span></summary><div class="tree-links"><svg class="neural-branches" viewBox="0 0 100 24" preserveAspectRatio="none" aria-hidden="true"><path d="M60 0V6Q60 18 12.5 18M60 6Q60 18 37.5 18M60 6Q60 18 62.5 18M60 6Q60 18 87.5 18"/><circle cx="12.5" cy="18" r="1"/><circle cx="37.5" cy="18" r="1"/><circle cx="62.5" cy="18" r="1"/><circle cx="87.5" cy="18" r="1"/></svg>{lab_links()}</div></details>' if key=='neuropath' else ''
        cards.append(f'''<div class="platform-stack {key}"><article class="platform-card"><img class="product-art" src="/public/images/development/{key}.webp" width="364" height="230" alt="{name} approved artwork"><h3 class="visually-hidden">{name}</h3><h4>{category}</h4><p>{description}</p><a class="gold-button" href="/laboratories/{key}/">Explore {name} <span aria-hidden="true">›</span></a></article>{tree}</div>''')
    blocks = [('/science/','science','The Science Behind Our Work','Research, principles and methodology.'),('/about-us/','story','Our Story','The meaning and vision behind GlionIQ.'),('/blog/','blog','Blog &amp; Insights','Articles, ideas and updates from our labs.'),('/journey/','journey','Join Our Journey','Stay informed about new releases and features.')]
    lower = ''.join(f'<a href="{url}"><img class="portal-icon" src="/public/images/development/{icon}-symbol.png" width="66" height="54" alt=""><h3>{title}</h3><p>{text}</p></a>' for url,icon,title,text in blocks)
    return f'''<section class="corporate-hero"><a class="hero-art" href="/" aria-label="GlionIQ — Home"><img src="/public/images/glioniq-hero-transparent.png" width="450" height="270" fetchpriority="high" alt="GlionIQ luminous blue brain and silver and gold wordmark"></a><div class="hero-copy"><h1>Where <em>Neuroscience</em> Meets <em>Lifelong Learning</em></h1><p>Science-inspired digital laboratories for learning, discovery and cognitive engagement at every stage of life.</p></div></section>
<section class="laboratories" id="laboratories" aria-labelledby="labs-title"><h2 class="section-title" id="labs-title">Our Laboratories</h2><p class="section-intro">Three unified platforms. A lifelong journey of learning, knowledge and brain engagement.</p><div class="platform-grid">{''.join(cards)}</div></section>
<section class="portals" aria-label="Discover GlionIQ">{lower}</section><section class="earth-cta" aria-label="Explore our platforms"><a class="gold-button" href="#laboratories">Explore the GlionIQ World <span aria-hidden="true">›</span></a></section>'''


def information_html(entry):
    e = escape
    artwork = entry.get('artwork')
    image = f'<img class="detail-art" src="/public/images/development/{artwork}.webp" width="364" height="230" alt="{e(entry["name"])} approved artwork">' if artwork else ''
    info = ''.join(f'<div><dt>{label}</dt><dd>{e(entry[key])}</dd></div>' for key,label in [('audience','Intended audience'),('purpose','Purpose'),('status','Development status')] if entry.get(key))
    sections = ''
    for section in entry.get('sections',[]):
        paragraphs = ''.join(f'<p>{e(p)}</p>' for p in section.get('paragraphs',[]))
        items = '<ul>'+''.join(f'<li>{e(p)}</li>' for p in section['items'])+'</ul>' if section.get('items') else ''
        sections += f'<section><h2>{e(section["title"])}</h2>{paragraphs}{items}</section>'
    links = ''.join(f'<a class="gold-button" href="{e(link["href"])}">{e(link["label"])}</a>' for link in entry.get('links',[]))
    return f'''<div class="content-page"><a class="breadcrumb" href="/">← Home</a><div class="page-intro">{image}<div><p class="kicker">{e(entry.get('category',''))}</p><h1>{e(entry['name'])}</h1><p class="lead">{e(entry['introduction'])}</p></div></div><dl class="facts">{info}</dl><div class="editorial">{sections}</div><div class="related-links">{links}</div></div>'''


def search_html():
    return '''<section class="content-page search-page"><a class="breadcrumb" href="/">← Home</a><h1>Search GlionIQ</h1><p>Explore our platforms, laboratories, story and science-informed approach.</p><form action="/search/" method="get" role="search" id="site-search"><label for="query">Search website content</label><div class="search-fields"><input id="query" name="q" type="search" maxlength="120" autocomplete="off" placeholder="Try memory or Trampolina"><button class="gold-button" type="submit">Search</button></div></form><p id="search-status" role="status" aria-live="polite">Enter a topic to search.</p><div id="search-results"></div><noscript><p>Search needs JavaScript. Browse <a href="/#laboratories">Our Laboratories</a>, <a href="/about-us/">About Us</a>, <a href="/science/">Science &amp; Research</a>, <a href="/blog/">Blog &amp; Insights</a>, or <a href="/contact/">Contact</a>.</p></noscript></section>'''


def build():
    entries = json.loads((ROOT/'content/platforms.json').read_text()) + json.loads((ROOT/'content/pages.json').read_text())
    pages = [('/', 'GlionIQ — Where Neuroscience Meets Lifelong Learning', 'Science-inspired digital laboratories for learning, discovery and cognitive engagement at every stage of life.', home_html(), 'home-page', 'Home'),('/about-us/', 'About Us — Our Story', 'Our complete approved story, scientific commitment and vision.', '<article class="story">'+story_html()+'</article>'+contact().format(story='/about-us/'), 'about-page', 'About Us')]
    for entry in entries:
        pages.append((entry['route'],entry['name'],entry['introduction'],information_html(entry),'information-page',entry['name']))
    pages.append(('/search/','Search GlionIQ','Search available GlionIQ website content.',search_html(),'information-page','Search'))
    # Approved future articles are authored in content/articles.json. Empty means no invented publications.
    articles = json.loads((ROOT/'content/articles.json').read_text())['approved_articles']
    for article in articles:
        assert all(article.get(k) for k in ('slug','title','category','publication_date','body')), 'Incomplete approved article'
        assert re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', article['slug']), 'Unsafe article slug'
        from datetime import date
        date.fromisoformat(article['publication_date'])
        body = ''
        for section in article['body']:
            body += '<section><h2>'+escape(section['title'])+'</h2>'
            body += ''.join('<p>'+escape(p)+'</p>' for p in section.get('paragraphs', []))
            if section.get('items'): body += '<ul>'+''.join('<li>'+escape(i)+'</li>' for i in section['items'])+'</ul>'
            body += '</section>'
        assert all(s['url'].startswith(('https://','http://')) for s in article.get('sources',[])), 'Invalid article source URL'
        sources = ''.join(f'<li><a href="{escape(s["url"])}">{escape(s["title"])}</a></li>' for s in article.get('sources',[]))
        byline = ' · '+escape(article['author']) if article.get('author') else ''
        html=f'<article class="content-page editorial"><a href="/blog/">← Blog &amp; Insights</a><p class="kicker">{escape(article["category"])}</p><h1>{escape(article["title"])}</h1><p><time datetime="{escape(article["publication_date"])}">{escape(article["publication_date"])}</time>{byline}</p>{body}<ul>{sources}</ul></article>'
        pages.append((f'/blog/{article["slug"]}/',article['title'],article['title'],html,'information-page','Blog & Insights'))
    if articles:
        listing = '<div class="content-page"><h1>Blog &amp; Insights</h1><p>Articles, ideas and updates from our labs.</p>'
        for article in articles:
            listing += '<article class="search-result"><p class="kicker">'+escape(article['category'])+'</p><h2><a href="/blog/'+escape(article['slug'])+'/">'+escape(article['title'])+'</a></h2><p>'+escape(article['publication_date'])+'</p><p>'+escape(article.get('summary',''))+'</p></article>'
        listing += '</div>'
        pages = [(r,t,'Articles, ideas and updates from our labs.' if r=='/blog/' else d,listing if r=='/blog/' else b,c,n) for r,t,d,b,c,n in pages]
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
    (ROOT/'assets/search-index.json').write_text(json.dumps(search,ensure_ascii=False,indent=2)+'\n')
    print(f'Built {len(pages)} local pages; indexed {len(search)} content pages. No publication performed.')


if __name__ == '__main__':
    build()
