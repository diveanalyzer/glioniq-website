#!/usr/bin/env python3
"""Extract approved source pixels; preserve every supplied file.

Optional authoring dependency: Pillow from branding-requirements.txt.
Normal site builds only read content/artwork-map.json and need no Pillow.
"""
from collections import deque
from hashlib import sha256
from pathlib import Path
import json
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
BASE = 'public/images/laboratories/'
OUTPUT = BASE + 'derived/'
SPECS = {}


def add(key, source, crop=None, **options):
    SPECS[key] = dict(source=BASE + source, crop=crop, **options)


trampolina = {
    'trampolina-brand': '526CFEED-567B-4C82-A7E9-21B7CDF1ACF2 3.png',
    'memory-perception': '78612329-716C-4B2E-A379-5969D6209669.png',
    'thinking-logic': '56D2556C-E502-49F1-90F3-A1D30C4F1621.png',
    'memory-game': '6F105743-02F3-479E-BDDB-7EC1908DC771 2.png',
    'picture-puzzle': '08471A48-DD4B-41BC-8A0D-5F843D58737B.png',
    'spot-differences': 'DFBEE128-E301-44F3-9316-092A7B7E2713.png',
    'continue-pattern': 'AAB54338-01FE-46AB-8BF5-3A39FD3F9786.png',
    'sorting-categories': 'A357F62F-4375-4B51-A261-5163FF7ADB06.png',
    'first-next': 'FEB9898E-F8C1-4B0E-837D-3C3A3814FF77.png',
    'odd-one-out': '1B2081EC-7484-4C5A-BF82-8B3721C02205.png',
}
for key, file in trampolina.items():
    add(key, 'trampolina/' + file, matte=key != 'trampolina-brand', embedded_text='en' if key == 'trampolina-brand' else 'he')
SPECS['memory-perception']['matte_seeds'] = [(750, 440)]
SPECS['thinking-logic']['matte_seeds'] = [(980, 455), (1085, 560), (900, 80), (955, 80)]
for key in ('colors', 'numbers', 'shapes', 'letters'):
    add(key, f'generated-review/trampolina-{key}-3d-review.png', status='owner-review-required')
add('dr-quiz-character', 'dr-quiz/C514A1B2-697F-4527-BF9E-E3BA8FBA2368.png')
add('challenge-me', 'dr-quiz/challenge-me.png', (80, 16, 579, 351))
add('discover-learn', 'dr-quiz/discover-and-learn.png', (32, 20, 545, 412))
add('party-quiz', 'dr-quiz/party-quiz.png', (70, 20, 625, 389))
selection = 'neuropath/06_games/game_selection.jpeg'
add('memory', selection, (58, 309, 352, 508), clear_rect=(260, 0, 294, 75))
add('attention', selection, (630, 305, 881, 511))
add('logic', selection, (632, 555, 866, 753))
add('flexibility', selection, (62, 556, 307, 754))
add('neuroweave', selection, (719, 884, 895, 1059), embedded_text='en')
add('codequest', selection, (923, 884, 1098, 1060), embedded_text='en')
add('memory-activity', 'neuropath/05_daily_training/training_duration.jpeg', (995, 654, 1125, 747))
add('neuropath-brand', 'neuropath/03_home/home.jpeg', (205, 70, 815, 508), clear_rect=(565, 0, 610, 18), embedded_text='en')
add('neurobreath', 'neurobreath/IMG_0020 3.JPG')


def external_matte(image, seeds=()):
    """Remove only border-connected neutral white/checker pixels.

    Source RGB is never repainted. Opaque interior colors and lettering stay
    byte-identical; ambiguous enclosed checker areas remain for owner review.
    """
    image = image.convert('RGBA')
    w, h = image.size
    pixels = image.load()
    visited = bytearray(w * h)
    queue = deque(list(seeds) + [(x, 0) for x in range(w)] + [(x, h-1) for x in range(w)] +
                  [(0, y) for y in range(h)] + [(w-1, y) for y in range(h)])
    while queue:
        x, y = queue.popleft()
        pos = y * w + x
        if visited[pos]:
            continue
        visited[pos] = 1
        r, g, b, a = pixels[x, y]
        if min(r, g, b) < 190 or max(r, g, b) - min(r, g, b) > 13:
            continue
        pixels[x, y] = (r, g, b, 0)
        for nx, ny in ((x-1, y), (x+1, y), (x, y-1), (x, y+1)):
            if 0 <= nx < w and 0 <= ny < h and not visited[ny*w+nx]:
                queue.append((nx, ny))
    return image


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def prepare():
    (ROOT / OUTPUT).mkdir(exist_ok=True)
    previous_path = ROOT / 'content/artwork-map.json'
    previous = json.loads(previous_path.read_text()).get('assets', {}) if previous_path.exists() else {}
    assets = {}
    for key, spec in SPECS.items():
        source = ROOT / spec['source']
        original = Image.open(source)
        destination = OUTPUT + key + '-source-art.png'
        old = previous.get(key, {})
        unchanged = all(old.get(k) == json.loads(json.dumps(v)) for k, v in spec.items())
        if unchanged and old.get('source_sha256') == digest(source) and (ROOT / destination).exists():
            image = Image.open(ROOT / destination)
        else:
            image = original.crop(spec['crop']) if spec['crop'] else original.copy()
            if spec.get('matte'):
                image = external_matte(image, spec.get('matte_seeds', ()))
            if spec.get('clear_rect'):
                image = image.convert('RGBA')
                alpha = image.getchannel('A')
                alpha.paste(0, spec['clear_rect'])
                image.putalpha(alpha)
            image.save(ROOT / destination)
        web = image.copy()
        web.thumbnail((640, 640), Image.Resampling.LANCZOS)
        web_file = OUTPUT + key + '-card.webp'
        web.save(ROOT / web_file, lossless=True, method=4)
        assets[key] = {**spec, 'file': destination, 'width': image.width, 'height': image.height,
                       'web_file': web_file, 'web_width': web.width, 'web_height': web.height,
                       'web_sha256': digest(ROOT / web_file),
                       'source_sha256': digest(source), 'sha256': digest(ROOT / destination),
                       'status': spec.get('status', 'approved-source-derivative')}
    routes = {}
    for entry in json.loads((ROOT / 'content/platforms.json').read_text()):
        parts = entry['route'].strip('/').split('/')
        platform, slug = parts[1], parts[-1]
        if len(parts) == 2:
            key = {'trampolina': 'trampolina-brand', 'dr-quiz': 'dr-quiz-character',
                   'neuropath': 'neuropath-brand', 'neurobreath': 'neurobreath'}[platform]
        elif platform == 'neurobreath':
            key = 'neurobreath'  # Approved shared orb; no invented method logos.
        else:
            key = slug
        assert key in assets, entry['route']
        routes[entry['route']] = key
    originals = []
    for path in sorted((ROOT / BASE).rglob('*')):
        if not path.is_file() or path.name == '.DS_Store' or any(p in path.parts for p in ('derived', 'generated-review')):
            continue
        image = Image.open(path)
        used = [k for k, s in SPECS.items() if ROOT / s['source'] == path]
        originals.append({'file': path.relative_to(ROOT).as_posix(), 'sha256': digest(path),
                          'width': image.width, 'height': image.height, 'used_by': used,
                          'backup_excluded': path.name == 'profile_setup_flow.jpeg',
                          'role': 'artwork source' if used else 'reference only; no UI or additional games imported'})
    output = {'version': 1, 'originals': originals, 'assets': assets, 'routes': routes,
              'homepage_platforms': {k: f'public/images/development/{k}.webp' for k in ('trampolina', 'dr-quiz', 'neuropath')},
              'notes': ['Homepage platform logos retain the authoritative Master Design Reference.',
                        'Hebrew labels stay unchanged; English card headings provide the site-language translation.',
                        'NeuroBreath methods share the approved orb; route diagrams remain explanatory content.',
                        'Generated illustrations are proposals, never officially approved logos.',
                        'Other games visible in screenshots are inventory references only, not new site content.']}
    (ROOT / 'content/artwork-map.json').write_text(json.dumps(output, ensure_ascii=False, indent=2) + '\n')
    print(f'Prepared {len(assets)} assets; mapped {len(routes)} destinations; inventoried {len(originals)} supplied images.')


if __name__ == '__main__':
    prepare()
