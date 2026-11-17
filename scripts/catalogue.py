"""Source-backed catalogue, shared hierarchy and escaped presentation templates."""
from copy import deepcopy
from html import escape as e
from pathlib import Path
import json
import struct

from laboratories import ARTWORK, artwork_for, neurobreath_art, living_orb, breathing_activity, METHODS

ROOT = Path(__file__).resolve().parents[1]
PLATFORMS = ('trampolina', 'dr-quiz', 'neuropath', 'neurobreath')
PLATFORM_NAMES = dict(zip(PLATFORMS, ('Trampolina', 'Dr. Quiz', 'NeuroPath', 'NeuroBreath')))


def load_catalogue():
    entries = {}
    for platform in PLATFORMS:
        path = ROOT / 'content/catalogue' / (platform + '.json')
        if not path.exists():
            continue
        document = json.loads(path.read_text())
        for entry in document['entries']:
            assert entry['route'] not in entries, 'Duplicate catalogue route'
            entries[entry['route']] = dict(entry, platform=platform)
    resolved = {}
    def resolve(route, visiting=()):
        assert route not in visiting, 'Cyclic content inheritance'
        if route in resolved:
            return resolved[route]
        entry = deepcopy(entries[route])
        if entry.get('inherits'):
            inherited = resolve(entry['inherits'], (*visiting, route))
            for key in ('audience', 'difficulty', 'languages', 'status', 'interaction', 'tutorial', 'parent_tips'):
                if not entry.get(key) and inherited.get(key):
                    entry[key] = deepcopy(inherited[key])
        resolved[route] = entry
        return entry
    for route in entries:
        resolve(route)
    return resolved


def words(value):
    return ', '.join(str(x) for x in value) if isinstance(value, list) else str(value or '')


def image_dimensions(path):
    """PNG dimensions for separately copied catalogue media; no build dependency."""
    data = (ROOT / path.lstrip('/')).read_bytes()
    if data[:8] == b'\x89PNG\r\n\x1a\n':
        return struct.unpack('>II', data[16:24])
    # Existing non-PNG art is rendered from its exact inventory dimensions.
    return (1200, 800)


def image(entry, hero=False):
    route = entry.get('hero_artwork_route') if hero else None
    route = route or entry.get('artwork_route') or entry['route']
    direct = entry.get('artwork_file') if not (hero and entry.get('hero_artwork_route')) else None
    if direct:
        width, height = image_dimensions(direct)
        status = entry.get('artwork_status', 'provisional')
        small = ' compact-art' if entry.get('artwork_compact') or width <= 256 else ''
        return f'<span class="catalogue-art{small}" data-artwork-status="{e(status)}"><img src="/{e(direct.lstrip("/"))}" width="{width}" height="{height}" alt="{e(entry.get("artwork_alt", entry["name"] + " illustration"))}" loading="lazy" decoding="async"></span>'
    if route.startswith('/laboratories/neurobreath/'):
        return neurobreath_art(detail=hero) if entry['kind']=='platform' else '<div class="neurobreath-art">'+living_orb()+'</div>'
    if route in ARTWORK['routes']:
        return artwork_for(route, detail=hero)
    return artwork_for('/laboratories/' + entry['platform'] + '/', detail=hero)


def ancestors(entry, entries):
    chain, seen = [], {entry['route']}
    parent = entry['parent']
    while parent in entries:
        assert parent not in seen, 'Cyclic catalogue parent'
        seen.add(parent)
        chain.append(entries[parent])
        parent = entries[parent]['parent']
    return list(reversed(chain))


def breadcrumbs(entry, entries):
    links = [('/', 'Home'), ('/#laboratories', 'Our Laboratories')]
    links += [(p['route'], p['name']) for p in ancestors(entry, entries)]
    items = ''.join(f'<li><a href="{e(route)}">{e(name)}</a></li>' for route, name in links)
    parent = entries.get(entry['parent'])
    label = parent['name'] if parent else 'Our Laboratories'
    return f'<nav class="catalogue-breadcrumbs" aria-label="Breadcrumb"><ol>{items}<li aria-current="page">{e(entry["name"])}</li></ol></nav><a class="catalogue-back" data-parent-link href="{e(entry["parent"])}">← Back to {e(label)}</a>'


def paragraphs(values):
    return ''.join('<p>' + e(words(v)) + '</p>' for v in values)


def interaction(entry, heading='How it works'):
    labels = [('see', 'What appears on screen'), ('hear', 'Sound and spoken guidance'), ('do', 'Your actions'), ('feedback', 'Feedback'), ('progression', 'Progression'), ('help', 'Help, replay and leaving the activity')]
    rows = ''.join(f'<div><dt>{label}</dt><dd>{e(words(entry.get("interaction", {}).get(key)))}</dd></div>' for key, label in labels if entry.get('interaction', {}).get(key))
    return f'<details class="catalogue-disclosure"><summary>{e(heading)}</summary><dl class="interaction-facts">{rows}</dl></details>' if rows else ''


def card(entry):
    signature = bool(entry.get('signature'))
    badge = '<span class="signature-label"><span class="signature-diamond" aria-hidden="true"></span>GlionIQ Signature Game</span>' if signature else ''
    details = ''.join(f'<div><dt>{label}</dt><dd>{e(words(entry.get(key)))}</dd></div>' for key, label in [('purpose', 'Objective'), ('audience', 'Audience'), ('difficulty', 'Difficulty / progression')] if entry.get(key))
    status = 'Interactive local breathing guide' if entry['platform'] == 'neurobreath' and entry['kind'] == 'activity' else 'In development · Explore information'
    return f'<article class="catalogue-card'+(' signature-card' if signature else '')+f'" data-catalogue-card="{e(entry["id"])}"><div class="catalogue-card-art">{image(entry)}</div><div class="catalogue-card-copy">{badge}<h3><a href="{e(entry["route"])}">{e(entry["name"])}</a></h3><p>{e(entry["introduction"])}</p><dl class="card-facts">{details}</dl><p class="catalogue-status">{status}</p><a class="gold-button" href="{e(entry["route"])}">Explore {e(entry["name"])} <span aria-hidden="true">›</span></a>{interaction(entry, "Activity details")}</div></article>'


def research_ids(entry):
    if entry.get('research'):
        return entry['research']
    platform, route = entry['platform'], entry['route']
    if platform == 'neurobreath':
        return ['balban2023', 'nhs-breathing']
    if platform == 'dr-quiz':
        return ['roediger2006']
    if platform == 'neuropath':
        return ['diamond2013', 'simons2016', 'stern2020']
    if '/numbers/' in route:
        return ['ramani2008']
    if '/shapes/' in route:
        return ['fisher2013']
    if '/letters/' in route:
        return ['james2012']
    return ['diamond2013', 'fisher2013']


def research_section(entry):
    registry = json.loads((ROOT / 'content/catalogue-research.json').read_text())
    items = []
    for key in research_ids(entry):
        ref = registry[key]
        items.append(f'<li><h3><a href="{e(ref["url"])}">{e(ref["title"])}</a></h3><p class="reference-citation">{e(ref["authors"])} · {e(str(ref["year"]))} · {e(ref["publication"])}</p><p>{e(ref["summary"])}</p><p><strong>Relevance and limits:</strong> {e(ref["relevance"])}</p></li>')
    return '<section class="catalogue-section research-context" id="research"><p class="kicker">Research in context</p><h2>Scientific and educational background</h2><p>These sources explain general ideas behind the experience. They do not establish that a GlionIQ product improves health, prevents illness or produces a guaranteed learning outcome. Product-specific effectiveness has not been established in the evidence reviewed for this catalogue.</p><ol class="catalogue-references">'+''.join(items)+'</ol></section>'


def tutorial(entry):
    steps = entry.get('tutorial', [])
    if not steps:
        return ''
    items = ''.join(f'<li><h3>{e(step["title"])}</h3><p>{e(step["text"])}</p></li>' for step in steps)
    return '<section class="catalogue-section" id="tutorial"><p class="kicker">A guided introduction</p><h2>Step by step</h2><ol class="tutorial-steps">'+items+'</ol></section>'


def gallery(entry):
    figures = []
    for shot in entry.get('screenshots', []):
        width, height = image_dimensions(shot['file'])
        path = '/' + shot['file'].lstrip('/')
        figures.append(f'<figure><a href="{e(path)}" aria-label="Open full screenshot: {e(shot["alt"])}"><img src="{e(path)}" width="{width}" height="{height}" alt="{e(shot["alt"])}" loading="lazy" decoding="async"></a><figcaption>{e(shot["caption"])}</figcaption></figure>')
    return '<section class="catalogue-section"><h2>Inside the activity</h2><div class="tutorial-gallery">'+''.join(figures)+'</div></section>' if figures else ''


def related_section(entry, entries):
    routes = [r for r in entry.get('related', []) if r in entries and r != entry['route']]
    if not routes:
        routes = [r for r, item in entries.items() if item['parent'] == entry['parent'] and r != entry['route']][:3]
    if not routes:
        return ''
    return '<section class="catalogue-section"><h2>Continue exploring</h2><div class="related-catalogue">'+''.join(f'<a href="{e(r)}">{e(entries[r]["name"])} <span aria-hidden="true">→</span></a>' for r in dict.fromkeys(routes))+'</div></section>'


def detail_sections(entry, entries):
    objectives = '<ul class="catalogue-objectives">'+''.join('<li>'+e(words(x))+'</li>' for x in entry.get('objectives', []))+'</ul>' if entry.get('objectives') else ''
    offers = '<section class="catalogue-section"><h2>What this '+('platform' if entry['kind']=='platform' else 'laboratory' if entry['kind']=='lab' else 'experience')+' offers</h2>'+paragraphs(entry.get('offers', [entry['purpose']]))+objectives+'</section>'
    children = [item for item in entries.values() if item['parent'] == entry['route']]
    child_title = 'Laboratories and experiences' if entry['kind']=='platform' else 'Topics to discover' if all(c['kind']=='category' for c in children) else 'Games and activities'
    child_section = '<section class="catalogue-section" id="activities"><h2>'+child_title+'</h2><div class="catalogue-cards">'+''.join(card(child) for child in children)+'</div></section>' if children else ''
    tips = '<section class="catalogue-section parent-guidance"><h2>For parents and shared learning</h2>'+paragraphs(entry.get('parent_tips', []))+'</section>' if entry.get('parent_tips') else ''
    return offers+child_section+interaction(entry)+tutorial(entry)+gallery(entry)+tips+research_section(entry)+related_section(entry, entries)


def page(entry, entries):
    crumb = breadcrumbs(entry, entries)
    facts = ''.join(f'<div><dt>{label}</dt><dd>{e(words(entry.get(key)))}</dd></div>' for key, label in [('purpose','Purpose'),('audience','Intended audience'),('age_guidance','Age guidance'),('difficulty','Difficulty and progression'),('languages','Languages'),('status','Availability')] if entry.get(key))
    if entry['platform']=='neurobreath' and entry['route'].strip('/').split('/')[-1] in METHODS:
        body = breathing_activity(entry)
        start = body.index('<a class="breadcrumb"')
        end = body.index('</a>', start)+4
        body = body[:start]+crumb+body[end:]
        return body[:-len('</section>')]+f'<dl class="facts catalogue-facts">{facts}</dl>'+detail_sections(entry, entries)+'</section>'
    label = {'platform':'Platform', 'lab':'Laboratory', 'category':'Knowledge topic', 'activity':'Activity guide'}[entry['kind']]
    signature = '<span class="signature-label"><span class="signature-diamond" aria-hidden="true"></span>GlionIQ Signature Game</span>' if entry.get('signature') else ''
    jump = '<nav class="catalogue-jump" aria-label="On this page">'+('<a href="#activities">Explore the catalogue</a>' if any(x['parent']==entry['route'] for x in entries.values()) else '')+('<a href="#tutorial">Step-by-step guide</a>' if entry.get('tutorial') else '')+'<a href="#research">Research context</a></nav>'
    return f'<article class="content-page catalogue-page" data-catalogue-id="{e(entry["id"])}">{crumb}<header class="catalogue-hero"><div class="catalogue-hero-art">{image(entry, True)}</div><div><p class="kicker">{e(label)} · {e(PLATFORM_NAMES[entry["platform"]])}</p>{signature}<h1>{e(entry["name"])}</h1><p class="lead">{e(entry["introduction"])}</p>{jump}</div></header><dl class="facts catalogue-facts">{facts}</dl>{detail_sections(entry,entries)}<a class="catalogue-back" href="{e(entry["parent"])}">← Back to {e(entries.get(entry["parent"], {}).get("name", "Our Laboratories"))}</a></article>'


def tree_card(entry):
    signature = ' signature-card' if entry.get('signature') else ''
    badge = '<span class="signature-label"><span class="signature-diamond" aria-hidden="true"></span>Signature Game</span>' if signature else ''
    timing = ''
    if entry.get('timing'):
        cycle = '–'.join(str(p['seconds']) for p in entry['timing'])
        phases = ' · '.join(p['phase']+' '+str(p['seconds'])+'s' for p in entry['timing'])
        timing = f'<span class="catalogue-timing">{cycle}</span><span class="phase-summary">{e(phases)}</span>'
    action = 'Open activity' if entry.get('timing') else 'Explore information'
    return f'<a class="activity-card{signature}" href="{e(entry["route"])}">{image(entry)}{badge}<strong class="activity-title">{e(entry["name"])}</strong>{timing}<span class="activity-description">{e(entry["introduction"])}</span><span class="activity-action">{action} <span aria-hidden="true">→</span></span></a>'


def exploration(platform, entries):
    root = entries[platform['route']]
    nodes = []
    for branch in platform['branches']:
        item = entries[branch['route']]
        # Keep the overview legible: categories and all deeper levels are reached
        # through their explicit parent pages; only games appear on this tree.
        children = [x for x in entries.values() if x['parent']==item['route'] and x['kind']=='activity']
        nested = '<ul class="tree-activities">'+''.join('<li>'+tree_card(x)+'</li>' for x in children)+'</ul>' if children else ''
        nodes.append('<li class="tree-branch">'+tree_card(item)+nested+'</li>')
    close = f'<a class="tree-close" data-close-explorer href="/#platform-{e(platform["key"])}">Close Laboratories <span aria-hidden="true">×</span></a>'
    return f'<section class="central-exploration content-page" data-central-tree="{e(platform["key"])}"><div class="explorer-controls">{close}<a href="{e(root["route"])}">About {e(root["name"])}</a></div><header class="tree-root">{image(root,True)}<h1 tabindex="-1">{e(root["name"])} Laboratories</h1><p>{e(root["introduction"])}</p><p class="kicker">Choose a connected experience</p></header><nav class="neural-tree" aria-label="{e(root["name"])} laboratory tree"><svg class="tree-wires" aria-hidden="true" focusable="false"></svg><ul class="tree-branches">'+''.join(nodes)+f'</ul></nav><div class="explorer-controls">{close}</div></section>'
