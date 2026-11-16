"""Shared laboratory presentation. Artwork is never synthesized."""
from html import escape as e


def placeholder():
    return '<div class="art-placeholder"><span class="placeholder-mark" aria-hidden="true">◌</span><strong>NeuroBreath</strong><small>Development placeholder<br>Approved artwork pending</small></div>'


def explorer(platforms):
    cards = []
    for p in platforms:
        key = p['key']
        art = placeholder() if key == 'neurobreath' else f'<img class="product-art" src="/public/images/development/{key}.webp" width="364" height="230" alt="{e(p["name"])} approved artwork" loading="lazy">'
        branches = ''.join(f'<a href="{b["route"]}"><span class="branch-node" aria-hidden="true"></span><strong>{e(b["name"])}</strong><span>{e(b["description"])}</span></a>' for b in p['branches'])
        cards.append(f'''<article class="platform-card {key}" data-platform="{key}">{art}<h3 class="visually-hidden">{e(p['name'])}</h3><h4>{e(p['subtitle'])}</h4><p class="platform-description">{e(p['description'])}</p><div class="platform-actions"><a class="gold-button" href="{p['route']}">Explore {e(p['name'])} <span aria-hidden="true">›</span></a></div><details class="platform-disclosure" name="laboratory" id="explore-{key}"><summary aria-controls="branches-{key}"><span>Discover laboratories</span> <span aria-hidden="true">＋</span><span class="visually-hidden"> in {e(p['name'])}</span></summary><div class="laboratory-tree" id="branches-{key}" aria-label="{e(p['name'])} laboratories"><p class="tree-heading">Inside {e(p['name'])}</p><div class="branch-links">{branches}</div><button class="tree-close" type="button">Close laboratories <span aria-hidden="true">×</span></button></div></details></article>''')
    return '<p class="explorer-hint">Choose a platform to discover its laboratories, or explore its story.</p><div class="laboratory-explorer"><div class="platform-grid">'+''.join(cards)+'</div></div>'


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
