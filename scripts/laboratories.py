"""Shared laboratory presentation; original artwork remains byte-for-byte intact."""
from html import escape as e
from pathlib import Path
import json

ARTWORK = json.loads((Path(__file__).resolve().parents[1] / "content/artwork-map.json").read_text())


def neurobreath_art(detail=False):
    return '<div class="neurobreath-art'+(' detail-art' if detail else '')+'"><img class="orb-image" src="/public/images/neurobreath-logo-official.jpg" width="1206" height="640" alt="Official NeuroBreath blue and gold neural orb" loading="lazy"><img class="neurobreath-wordmark" src="/public/images/laboratories/derived/neurobreath-approved-wordmark.png" width="539" height="83" alt="NeuroBreath" loading="lazy"></div>'


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


def explorer(platforms):
    cards, trees = [], []
    for p in platforms:
        key = p['key']
        art = neurobreath_art() if key == 'neurobreath' else f'<img class="product-art" src="/public/images/development/{key}.webp" width="364" height="230" alt="{e(p["name"])} approved artwork" loading="lazy">'
        cards.append(f'''<article class="platform-card {key}" id="platform-{key}" data-platform="{key}">{art}<h3 class="visually-hidden">{e(p['name'])}</h3><h4>{e(p['subtitle'])}</h4><p class="platform-description">{e(p['description'])}</p><div class="platform-actions"><a class="gold-button" href="{p['route']}">Explore {e(p['name'])} <span aria-hidden="true">›</span></a><button class="laboratory-toggle" id="explore-{key}" type="button" aria-expanded="false" aria-controls="laboratory-panel" data-name="{e(p['name'])}" hidden><span class="toggle-label">Discover Laboratories</span> <span class="toggle-mark" aria-hidden="true">+</span><span class="visually-hidden"> — {e(p['name'])}</span></button></div></article>''')
        trees.append(f'<div class="laboratory-tree" id="branches-{key}" data-tree="{key}" hidden><div class="branch-links">'+''.join(branch_card(b) for b in p['branches'])+'</div></div>')
    panel='<section class="laboratory-panel" id="laboratory-panel" aria-labelledby="tree-title" hidden><header class="tree-header"><div><p class="kicker">Connected laboratories</p><h3 id="tree-title" tabindex="-1"></h3></div><button class="tree-close" type="button">Close Laboratories <span aria-hidden="true">×</span></button></header>'+''.join(trees)+'</section>'
    return '<p class="explorer-hint">Choose Discover Laboratories to reveal a platform’s connected experiences.</p><div class="laboratory-explorer"><svg class="neural-connector" aria-hidden="true" focusable="false"><path></path></svg><div class="platform-grid">'+''.join(cards)+'</div>'+panel+'<noscript><p>Explore each platform above to discover its laboratories.</p></noscript></div>'


METHODS = {
    'square-focus': ('Square Focus', '4–4–4–4', [('Inhale',4),('Hold',4),('Exhale',4),('Hold',4)], 'M45 160V40H165V160Z', 'Four sides of a square'),
    'sleep-calm': ('Sleep Calm', '4–2–6', [('Inhale',4),('Hold',2),('Exhale',6)], 'M45 160V40H165V160', 'A path shaped like the Hebrew letter ח'),
    'neural-wave': ('Neural Wave', '4–6', [('Inhale',4),('Exhale',6)], 'M10 110C45 10 70 10 105 110S165 210 200 110', 'A flowing wave'),
}


def breathing_methods(key=None):
    cards = []
    for slug, (name, cycle, phases, path, label) in METHODS.items():
        if key and slug != key:
            continue
        phase_text = ''.join(f'<li><strong>{phase}</strong> {duration} seconds</li>' for phase, duration in phases)
        cards.append(f'<section class="breathing-method"><h2>{name}</h2><p class="cycle">{cycle}</p><svg class="breathing-route" viewBox="0 0 210 210" role="img" aria-label="{label}"><path d="{path}"></path></svg><p>{label}</p><ol class="breathing-phases">{phase_text}</ol><p class="method-note">Illustrative route · Coming Soon</p></section>')
    return '<div class="breathing-methods">'+''.join(cards)+'</div>'
