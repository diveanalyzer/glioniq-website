"""Shared laboratory presentation; original artwork remains byte-for-byte intact."""
from html import escape as e
from pathlib import Path
import json

ARTWORK = json.loads((Path(__file__).resolve().parents[1] / "content/artwork-map.json").read_text())


def living_orb():
    source = '/public/images/neurobreath-logo-official.jpg'
    image = f'<img src="{source}" width="1206" height="640" alt="" loading="lazy" decoding="async">'
    return f'<div class="living-orb" role="img" aria-label="Original NeuroBreath neural orb"><div class="orb-body">{image}</div><div class="orb-arms arms-left" aria-hidden="true">{image}</div><div class="orb-arms arms-right" aria-hidden="true">{image}</div></div>'


def neurobreath_art(detail=False):
    return '<div class="neurobreath-art'+(' detail-art' if detail else '')+'">'+living_orb()+'<img class="neurobreath-wordmark" src="/public/images/laboratories/derived/neurobreath-approved-wordmark.png" width="539" height="83" alt="NeuroBreath" loading="lazy"></div>'


def artwork_for(route, detail=False):
    key = ARTWORK['routes'][route]
    asset = ARTWORK['assets'][key]
    css = 'detail-art artwork-detail' if detail else 'category-visual'
    status = asset['status']
    image = f'<img src="/{e(asset["web_file"])}" width="{asset["web_width"]}" height="{asset["web_height"]}" alt="" loading="lazy" decoding="async">'
    return f'<span class="{css}" data-artwork="{e(key)}" data-artwork-status="{e(status)}">{image}</span>'


def branch_card(branch, activity=False):
    signature = activity and branch['route'].startswith('/laboratories/neuropath/')
    asset = ARTWORK['assets'][ARTWORK['routes'][branch['route']]]
    title_class = 'visually-hidden' if asset.get('embedded_text') == 'en' else 'activity-title'
    return f'<a class="activity-card'+(' signature-card' if signature else '')+f'" href="{e(branch["route"])}">{artwork_for(branch["route"])}<strong class="{title_class}">{e(branch["name"])}</strong><span class="activity-description">{e(branch["description"])}</span>'+ (f'<span class="activity-status">{e(branch["laboratory"])} · In development</span>' if activity else '')+'<span class="activity-action">'+('View activity' if activity else 'Explore laboratory')+' <span aria-hidden="true">→</span></span></a>'


def activity_cards(activities):
    return '<div class="activity-grid">'+''.join(branch_card(a, True) for a in activities)+'</div>'


def platform_art(platform):
    key = platform['key']
    return neurobreath_art() if key == 'neurobreath' else f'<img class="product-art" src="/public/images/development/{key}.webp" width="364" height="230" alt="{e(platform["name"])} approved artwork" loading="lazy">'


def explorer(platforms):
    cards = []
    for p in platforms:
        key = p['key']
        cards.append(f'''<article class="platform-card {key}" id="platform-{key}" data-platform="{key}">{platform_art(p)}<h3 class="visually-hidden">{e(p['name'])}</h3><h4>{e(p['subtitle'])}</h4><p class="platform-description">{e(p['description'])}</p><div class="platform-actions"><a class="gold-button" href="{p['route']}">Explore {e(p['name'])} <span aria-hidden="true">›</span></a><a class="laboratory-toggle" href="{p['route']}explore/">Discover Laboratories <span aria-hidden="true">→</span><span class="visually-hidden"> — {e(p['name'])}</span></a></div></article>''')
    return '<p class="explorer-hint">Choose Discover Laboratories to explore a platform’s connected experiences.</p><div class="laboratory-explorer"><div class="platform-grid">'+''.join(cards)+'</div></div>'


def central_tree(platform, entries):
    nodes = []
    for branch in platform['branches']:
        entry = next(item for item in entries if item['route'] == branch['route'])
        children = entry.get('activities', [])
        nested = '<ul class="tree-activities">'+''.join('<li>'+branch_card(a, True)+'</li>' for a in children)+'</ul>' if children else ''
        if platform['key'] == 'neurobreath':
            name, cycle, phases, _, _ = METHODS[branch['key']]
            summary = ' · '.join(f'{phase} {seconds}s' for phase, seconds in phases)
            node = f'<a class="activity-card breathing-node" href="{branch["route"]}">{artwork_for(branch["route"])}<strong class="activity-title">{e(name)}</strong><span class="cycle">{cycle}</span><span class="activity-description">{e(branch["description"])}</span><span class="phase-summary">{summary}</span><span class="activity-action">Open activity <span aria-hidden="true">→</span></span></a>'
        else:
            node = branch_card(branch) + '<p class="tree-status">In development · Explore information</p>'
        nodes.append('<li class="tree-branch">'+node+nested+'</li>')
    key = platform['key']
    return f'''<section class="central-exploration content-page" data-central-tree="{key}"><a class="breadcrumb" href="/#platform-{key}">← Back to Home</a><header class="tree-root">{platform_art(platform)}<h1>{e(platform['name'])} Laboratories</h1><p>{e(platform['description'])}</p><p class="kicker">Choose a connected experience</p></header><nav class="neural-tree" aria-label="{e(platform['name'])} laboratory tree"><ul class="tree-branches">{''.join(nodes)}</ul></nav><a class="breadcrumb" href="/#platform-{key}">← Back to Home</a></section>'''


METHODS = {
    'square-focus': ('Square Focus', '4–4–4–4', [('Inhale',4),('Hold',4),('Exhale',4),('Hold',4)], 'M45 160V40H165V160Z', 'Four sides of a square'),
    'sleep-calm': ('Sleep Calm', '4–2–6', [('Inhale',4),('Hold',2),('Exhale',6)], 'M45 160V40H165V160', 'A path shaped like the Hebrew letter ח'),
    'neural-wave': ('Neural Wave', '4–6', [('Inhale',4),('Exhale',6)], 'M10 110C45 10 70 10 105 110S165 210 200 110', 'A flowing wave'),
}


def breathing_scene(key):
    _, _, _, path, label = METHODS[key]
    return f'<div class="breathing-scene" data-shape="{key}">{living_orb()}<svg class="breathing-frame" viewBox="0 0 210 210" aria-hidden="true"><path class="frame-base" d="{path}"></path><path class="frame-trace" d="{path}" pathLength="1"></path></svg></div>'


def breathing_methods(key=None):
    cards = []
    for slug, (name, cycle, phases, path, label) in METHODS.items():
        if key and slug != key:
            continue
        phase_text = ''.join(f'<li><strong>{phase}</strong> {duration} seconds</li>' for phase, duration in phases)
        cards.append(f'<section class="breathing-method"><h2>{name}</h2><p class="cycle">{cycle}</p>{breathing_scene(slug)}<p>{label}</p><ol class="breathing-phases">{phase_text}</ol><p class="method-note">Illustrative route · Coming Soon</p></section>')
    return '<div class="breathing-methods">'+''.join(cards)+'</div>'
