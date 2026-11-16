"""Shared laboratory presentation; original artwork remains byte-for-byte intact."""
from html import escape as e


def neurobreath_art(detail=False):
    return '<div class="neurobreath-art'+(' detail-art' if detail else '')+'"><img src="/public/images/neurobreath-logo-official.jpg" width="1206" height="640" alt="Official NeuroBreath blue and gold neural orb" loading="lazy"><strong>NeuroBreath</strong></div>'


# Decorative category illustrations, never official product or game logos.
SYMBOLS = {
 'colors': '<circle cx="42" cy="41" r="20" fill="#ff7798"/><circle cx="65" cy="41" r="20" fill="#71d9ff"/><circle cx="54" cy="62" r="20" fill="#ffd36a"/>',
 'numbers': '<text x="24" y="52" fill="#ffce70" transform="rotate(-12 24 52)">1</text><text x="47" y="70" fill="#79d9ff">2</text><text x="72" y="47" fill="#bd9cff" transform="rotate(12 72 47)">3</text>',
 'shapes': '<circle cx="33" cy="32" r="14" fill="#ffbf71"/><path d="M58 44 75 16 92 44Z" fill="#88dbff"/><rect x="26" y="56" width="28" height="28" rx="5" fill="#c49cff"/><rect x="65" y="57" width="25" height="25" rx="4" fill="#7ae4ce" transform="rotate(15 78 70)"/>',
 'letters': '<text x="20" y="52" fill="#ffce70">A</text><text x="58" y="78" fill="#79d9ff">א</text><text x="65" y="35" fill="#c49cff" font-size="23">Б</text>',
 'memory-perception': '<rect x="19" y="23" width="34" height="51" rx="7" fill="#102d52" stroke="#72dcff" transform="rotate(-10 36 48)"/><rect x="57" y="29" width="34" height="51" rx="7" fill="#102d52" stroke="#ffdb7e" transform="rotate(10 74 54)"/><path d="m36 36 4 8 9 1-7 7 2 9-8-5-8 5 2-9-7-7 9-1Z" fill="#ffdb7e"/><circle cx="74" cy="54" r="10" fill="#72dcff"/>',
 'thinking-logic': '<circle cx="24" cy="30" r="10" fill="#ffce70"/><rect x="46" y="20" width="20" height="20" rx="4" fill="#7bddff"/><path d="m81 19 12 21H69Z" fill="#bf9aff"/><path d="M25 56H84M76 49l8 7-8 7" fill="none" stroke="#ffdb7e"/><circle cx="24" cy="79" r="7" fill="#ffce70"/><rect x="49" y="72" width="14" height="14" rx="3" fill="#7bddff"/><path d="m81 71 9 15H72Z" fill="#bf9aff"/>',
 'challenge-me': '<circle cx="55" cy="52" r="34" fill="none" stroke="#72d7ff"/><text x="42" y="67" fill="#ffe18a" font-size="48">?</text><path d="m84 16 3 7 8 2-8 3-3 7-3-7-7-3 7-2Z" fill="#ffe18a"/>',
 'party-quiz': '<path d="M37 21H73V43Q73 64 55 65 37 64 37 43ZM37 27H24V36Q24 49 39 49M73 27H86V36Q86 49 71 49M55 65V80M39 82H71" fill="none" stroke="#ffe18a"/><circle cx="23" cy="73" r="7" fill="#72d7ff"/><circle cx="87" cy="73" r="7" fill="#bb9cff"/>',
 'discover-learn': '<path d="M18 30Q35 24 55 35 75 24 92 30V76Q73 70 55 81 37 70 18 76ZM55 35V81" fill="#123253" stroke="#72d7ff"/><path d="m55 13 3 8 8 3-8 3-3 8-3-8-8-3 8-3Z" fill="#ffe18a"/><path d="m28 42 17 3m-17 9 17 3m20-12 17-3m-17 15 17-3" stroke="#ffe18a"/>',
 'square-focus': '<path d="M28 24H82V78H28Z" stroke="#72d7ff" fill="none"/><path d="M28 51V24H55" stroke="#ffe18a" fill="none"/><circle cx="28" cy="51" r="5" fill="#ffe18a"/>',
 'sleep-calm': '<path d="M28 80V24H82V80" stroke="#72d7ff" fill="none"/><path d="M28 51V24H55" stroke="#ffe18a" fill="none"/><circle cx="28" cy="51" r="5" fill="#ffe18a"/>',
 'neural-wave': '<path d="M10 54C25 10 42 10 55 54S85 98 100 54" stroke="#72d7ff" fill="none"/><path d="M10 54C20 25 31 16 40 25" stroke="#ffe18a" fill="none"/><circle cx="40" cy="25" r="5" fill="#ffe18a"/>',
 'neuroweave': '<path d="M23 20C83 24 23 79 87 82M87 20C23 24 87 79 23 82M24 35H86M34 52H76M24 69H86" stroke="#72d7ff" fill="none"/><circle cx="23" cy="20" r="5" fill="#ffe18a"/><circle cx="87" cy="82" r="5" fill="#ffe18a"/>',
 'codequest': '<path d="M20 22H90V82H20ZM20 42H90M20 62H90M43 22V82M67 22V82" fill="none" stroke="#72d7ff"/><path d="M31 72V51H55V31H79" fill="none" stroke="#ffe18a"/><circle cx="79" cy="31" r="5" fill="#ffe18a"/>',
 'picture-puzzle': '<path d="M20 22H50V35Q64 30 64 42T50 49V78H20ZM64 22H91V48H79Q84 62 71 62T64 48" fill="#102d52" stroke="#72d7ff"/><path d="M64 64V80H91V62" fill="none" stroke="#ffe18a"/>',
 'spot-differences': '<rect x="12" y="25" width="36" height="50" rx="6" fill="#102d52" stroke="#72d7ff"/><rect x="62" y="25" width="36" height="50" rx="6" fill="#102d52" stroke="#ffe18a"/><circle cx="30" cy="44" r="8" fill="#72d7ff"/><path d="m80 35 9 17H71Z" fill="#ffe18a"/><path d="M23 64H37M73 64H87" stroke="#9cceec"/>',
 'continue-pattern': '<circle cx="19" cy="51" r="10" fill="#ffce70"/><rect x="38" y="41" width="20" height="20" rx="4" fill="#7bddff"/><circle cx="76" cy="51" r="10" fill="#ffce70"/><path d="M94 42H106V60H94Z" stroke="#7bddff" stroke-dasharray="3 3" fill="none"/>',
 'sorting-categories': '<rect x="14" y="50" width="34" height="33" rx="6" fill="#102d52" stroke="#ffe18a"/><rect x="62" y="50" width="34" height="33" rx="6" fill="#102d52" stroke="#72d7ff"/><circle cx="31" cy="28" r="10" fill="#ffe18a"/><path d="m79 17 12 21H67Z" fill="#72d7ff"/><path d="M31 40V61M79 40V61" stroke="#9cceec"/>',
 'first-next': '<circle cx="29" cy="51" r="19" fill="#102d52" stroke="#72d7ff"/><circle cx="83" cy="51" r="19" fill="#102d52" stroke="#ffe18a"/><path d="M49 51H62M57 46l5 5-5 5" stroke="#ffe18a" fill="none"/><text x="22" y="59" fill="#72d7ff" font-size="22">1</text><text x="76" y="59" fill="#ffe18a" font-size="22">2</text>',
 'odd-one-out': '<circle cx="31" cy="29" r="13" fill="#72d7ff"/><circle cx="79" cy="29" r="13" fill="#72d7ff"/><circle cx="31" cy="75" r="13" fill="#72d7ff"/><path d="m79 61 15 27H64Z" fill="#ffe18a"/>',
 'memory-activity': '<rect x="21" y="23" width="29" height="53" rx="5" fill="#102d52" stroke="#72d7ff"/><rect x="61" y="23" width="29" height="53" rx="5" fill="#102d52" stroke="#ffe18a"/><circle cx="35" cy="49" r="9" fill="#ffe18a"/><circle cx="75" cy="49" r="9" fill="#72d7ff"/>',
}


def symbol(key):
    if key in ('memory','attention','logic','flexibility'):
        return f'<span class="category-visual"><img src="/public/images/development/{key}-symbol.png" width="65" height="55" alt="" loading="lazy"></span>'
    return f'<span class="category-visual"><svg viewBox="0 0 110 104" aria-hidden="true" focusable="false">{SYMBOLS[key]}</svg><small>Category illustration</small></span>'


def branch_card(branch, activity=False):
    signature = activity and branch['route'].startswith('/laboratories/neuropath/')
    return f'<a class="activity-card'+(' signature-card' if signature else '')+f'" href="{e(branch["route"])}">{symbol(branch["key"])}<strong>{e(branch["name"])}</strong><span class="activity-description">{e(branch["description"])}</span>'+ (f'<span class="activity-status">{e(branch["laboratory"])} · In development</span>' if activity else '')+'<span class="activity-action">'+('View activity' if activity else 'Explore laboratory')+' <span aria-hidden="true">→</span></span></a>'


def activity_cards(activities):
    return '<div class="activity-grid">'+''.join(branch_card(a, True) for a in activities)+'</div>'


def explorer(platforms):
    cards, trees = [], []
    for p in platforms:
        key = p['key']
        art = neurobreath_art() if key == 'neurobreath' else f'<img class="product-art" src="/public/images/development/{key}.webp" width="364" height="230" alt="{e(p["name"])} approved artwork" loading="lazy">'
        cards.append(f'''<article class="platform-card {key}" data-platform="{key}">{art}<h3 class="visually-hidden">{e(p['name'])}</h3><h4>{e(p['subtitle'])}</h4><p class="platform-description">{e(p['description'])}</p><div class="platform-actions"><a class="gold-button" href="{p['route']}">Explore {e(p['name'])} <span aria-hidden="true">›</span></a><button class="laboratory-toggle" id="explore-{key}" type="button" aria-expanded="false" aria-controls="laboratory-panel" data-name="{e(p['name'])}" hidden><span class="toggle-label">Discover Laboratories</span> <span class="toggle-mark" aria-hidden="true">+</span><span class="visually-hidden"> — {e(p['name'])}</span></button></div></article>''')
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
