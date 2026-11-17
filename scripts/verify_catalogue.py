#!/usr/bin/env python3
"""Read-only catalogue acceptance checks; run after scripts/build.py.

Uses only the standard library. Checks content and rendered evidence, not browser
interaction, clinical efficacy, live research URLs or owner visual approval.
The embedded baseline fingerprints were measured from f76dcfd and allow this
check to run in an exported checkout without Git history or app repositories.
"""
import ast
from collections import Counter
from hashlib import sha256
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import struct
import subprocess
import sys
from urllib.parse import unquote, urlsplit

sys.dont_write_bytecode = True
from catalogue import load_catalogue, research_ids

ROOT = Path(__file__).resolve().parents[1]
PLATFORMS = ('trampolina', 'dr-quiz', 'neuropath', 'neurobreath')
BASELINE = 'f76dcfd'
BASELINE_CSS_LENGTH = 35149
BASELINE_HASHES = {
    'hero': 'f5e39a337c2df0c99714cddf421cf9d7bab42df62fc77fe7a5346f6a409b54e7',
    'header': 'd932b685c11899cfa7986f5877cb8da39a654c92d833c25f6690c5c840137e3f',
    'footer': '0c6611bf99600c5012d056e241eddde38ae002bd73d5b1b937a3f0f586a2d82e',
    'css': 'cf18272cbe859ab7917d0377eae78dbdfa6e847d47e4325b80a2d0d0a2abaee0',
    'header_function': '713fa414c861f79e10679a549d7821debaf550a141c6c4ef00a918a766202097',
    'footer_function': '554f57b7f3dedd41f0059b9cad121e16b606148565fa858dfb6973ab66ec7bb3',
}
LEGACY_SUFFIXES = {
    'trampolina': ('', 'colors', 'numbers', 'shapes', 'letters', 'memory-perception',
        'thinking-logic', 'memory-perception/memory-game', 'memory-perception/picture-puzzle',
        'memory-perception/spot-differences', 'thinking-logic/continue-pattern',
        'thinking-logic/sorting-categories', 'thinking-logic/first-next', 'thinking-logic/odd-one-out'),
    'dr-quiz': ('', 'challenge-me', 'party-quiz', 'discover-learn'),
    'neuropath': ('', 'memory', 'attention', 'logic', 'flexibility',
        'memory/memory-activity', 'logic/neuroweave', 'logic/codequest'),
    'neurobreath': ('', 'square-focus', 'sleep-calm', 'neural-wave'),
}
NP_GAMES = {
    'memory-activity': 'memory', 'light-paths': 'memory', 'echoshift': 'memory',
    'target-hunt': 'attention', 'orbitmind': 'attention', 'neuroweave': 'logic',
    'codequest': 'logic', 'rule-shift': 'flexibility', 'synapse-forge': 'flexibility',
}
SIGNATURES = {'memory-activity', 'neuroweave', 'codequest'}
DR_CATEGORIES = set('countries geography history astronomy science physics chemistry biology nature animals plants oceans diving sailing wine food psychology philosophy law economics technology inventions art music movies literature sports mythology'.split())
DR_SUBCATEGORIES = set('wine.barolo wine.italy wine.piedmont astronomy.earth-moon astronomy.kuiper-belt astronomy.martian-moons physics.general-relativity physics.special-relativity biology.neuroscience biology.nervous-system biology.brain-cells biology.immune-system biology.brain-and-sleep biology.learning-and-memory science.scientific-myths sports.football sports.basketball sports.golf sports.tennis sports.american-football'.split())
RESEARCH_URLS = {
    'ramani2008': 'https://doi.org/10.1111/j.1467-8624.2007.01131.x',
    'fisher2013': 'https://doi.org/10.1111/cdev.12091',
    'james2012': 'https://doi.org/10.1016/j.tine.2012.08.001',
    'roediger2006': 'https://doi.org/10.1111/j.1467-9280.2006.01693.x',
    'diamond2013': 'https://doi.org/10.1146/annurev-psych-113011-143750',
    'simons2016': 'https://doi.org/10.1177/1529100616661983',
    'stern2020': 'https://doi.org/10.1016/j.jalz.2018.07.219',
    'balban2023': 'https://doi.org/10.1016/j.xcrm.2022.100895',
    'nhs-breathing': 'https://www.nhs.uk/mental-health/self-help/guides-tools-and-activities/breathing-exercises-for-stress/',
}
FAILURES = []


def check(condition, message):
    if not condition:
        FAILURES.append(message)
    return bool(condition)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(data):
    return sha256(data).hexdigest()


def read_json(path):
    return json.loads((ROOT / path).read_text())


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def local_file(value):
    require(nonempty(value), 'Empty asset path')
    decoded = unquote(urlsplit(value).path)
    require(not urlsplit(value).scheme and '..' not in Path(decoded).parts,
            f'Non-local or unsafe asset path: {value}')
    require(not re.search(r'(^|[/_.-])(private|profiles?|user[-_]data|user[-_]records)([/_.-]|$)', decoded, re.I),
            f'Private/profile asset referenced: {value}')
    path = (ROOT / decoded.lstrip('/')).resolve()
    require(path.is_relative_to(ROOT), f'Asset outside website: {value}')
    require(path.is_file(), f'Missing asset: {value}')
    return path


class Page(HTMLParser):
    def __init__(self, html):
        super().__init__(convert_charrefs=True)
        self.links, self.parent_links, self.breadcrumbs = [], [], []
        self.cards, self.images, self.statuses, self.ids = [], [], [], []
        self.text = []
        self.in_breadcrumb = False
        self.feed(html)

    def handle_starttag(self, tag, pairs):
        attrs = dict(pairs)
        if tag == 'nav' and 'catalogue-breadcrumbs' in attrs.get('class', '').split():
            self.in_breadcrumb = True
        if tag == 'a':
            href = attrs.get('href', '')
            self.links.append(href)
            if self.in_breadcrumb:
                self.breadcrumbs.append(href)
            if 'data-parent-link' in attrs:
                self.parent_links.append(href)
        if 'data-catalogue-card' in attrs:
            self.cards.append(attrs['data-catalogue-card'])
        if 'data-artwork-status' in attrs:
            self.statuses.append(attrs['data-artwork-status'])
        if 'id' in attrs:
            self.ids.append(attrs['id'])
        if tag == 'img':
            self.images.append(attrs)

    def handle_endtag(self, tag):
        if tag == 'nav':
            self.in_breadcrumb = False

    def handle_data(self, data):
        self.text.append(data)


def inspect_content():
    documents = {platform: read_json(f'content/catalogue/{platform}.json') for platform in PLATFORMS}
    raw = []
    for platform, doc in documents.items():
        require(doc.get('platform') == platform and doc.get('entries'), f'Invalid platform document: {platform}')
        require(all(doc.get('source', {}).get(k) for k in ('repository', 'revision', 'inspection')),
                f'Missing repository inspection evidence: {platform}')
        for entry in doc['entries']:
            require(entry.get('platform') == platform, f'Wrong platform on {entry.get("id")}')
        raw.extend(doc['entries'])
    for key in ('id', 'route'):
        values = [entry.get(key) for entry in raw]
        require(all(nonempty(value) for value in values) and len(values) == len(set(values)), f'Missing or duplicate {key}')
    entries = load_catalogue()  # Includes explicit inheritance; no build or file writes.
    for route, entry in entries.items():
        require(re.fullmatch(r'/laboratories/[a-z0-9-]+/(?:[a-z0-9-]+/)*', route), f'Invalid route: {route}')
        require(route.startswith('/laboratories/' + entry['platform'] + '/'), f'Cross-platform route: {route}')
        require(entry['kind'] in ('platform', 'lab', 'category', 'activity'), f'Invalid kind: {route}')
        for key in ('name', 'introduction', 'purpose', 'audience', 'age_guidance', 'difficulty', 'status'):
            require(nonempty(entry.get(key)), f'Empty {key}: {route}')
        for key in ('languages', 'objectives', 'offers'):
            value = entry.get(key)
            require(nonempty(value) or isinstance(value, list) and value and all(nonempty(x) for x in value), f'Empty {key}: {route}')
        require(isinstance(entry.get('signature'), bool), f'Missing signature boolean: {route}')
        require(entry.get('tutorial') and all(nonempty(step.get('title')) and nonempty(step.get('text')) for step in entry['tutorial']), f'Missing tutorial: {route}')
        require(all(nonempty(entry.get('interaction', {}).get(key)) for key in ('see', 'hear', 'do', 'feedback', 'progression', 'help')), f'Incomplete interaction: {route}')
        require(entry.get('sources') and all(all(nonempty(str(source.get(key, ''))) for key in ('file', 'lines', 'supports')) for source in entry['sources']), f'Missing source evidence: {route}')
        for evidence in entry['sources']:
            require(not Path(evidence['file']).is_absolute() and '..' not in Path(evidence['file']).parts,
                    f'Non-portable source citation: {route}')
        parent = entry.get('parent')
        require(parent == '/#laboratories' if entry['kind'] == 'platform' else parent in entries, f'Missing explicit parent: {route}')
        seen = {route}
        while parent in entries:
            require(parent not in seen, f'Cyclic parents: {route}')
            require(entries[parent]['platform'] == entry['platform'], f'Cross-platform parent: {route}')
            seen.add(parent)
            parent = entries[parent]['parent']
        require(parent == '/#laboratories', f'Unrooted hierarchy: {route}')
        related = entry.get('related', [])
        require(isinstance(related, list) and len(related) == len(set(related)) and all(r in entries and r != route for r in related), f'Invalid related destination: {route}')
    legacy = {'/laboratories/' + platform + '/' + (suffix + '/' if suffix else '') for platform, suffixes in LEGACY_SUFFIXES.items() for suffix in suffixes}
    require(len(legacy) == 30 and legacy <= entries.keys(), f'Legacy routes missing: {legacy - entries.keys()}')
    require({e['platform'] for e in entries.values() if e['kind'] == 'platform'} == set(PLATFORMS), 'Four platform roots required')
    np = [entry for entry in entries.values() if entry['platform'] == 'neuropath' and entry['kind'] == 'activity']
    require({e['route'].strip('/').split('/')[-1] for e in np} == set(NP_GAMES), 'NeuroPath nine-game inventory changed')
    for entry in np:
        game = entry['route'].strip('/').split('/')[-1]
        require(entry['parent'] == '/laboratories/neuropath/' + NP_GAMES[game] + '/', f'Incorrect NeuroPath placement: {game}')
        require(entry['signature'] == (game in SIGNATURES), f'Incorrect signature marker: {game}')
    require(sum(e['signature'] for e in entries.values()) == 3, 'Exactly three signature games required')
    dr = [e for e in entries.values() if e['platform'] == 'dr-quiz']
    categories = [e for e in dr if e.get('source_category_id') and not e.get('source_subcategory_id')]
    subcategories = [e for e in dr if e.get('source_subcategory_id')]
    require(len(categories) == 28 and {e['source_category_id'] for e in categories} == DR_CATEGORIES, 'Dr. Quiz 28 active categories incomplete')
    require(len(subcategories) == 20 and {e['source_subcategory_id'] for e in subcategories} == DR_SUBCATEGORIES, 'Dr. Quiz 20 active subcategories incomplete')
    require(not any('sailing-practice' in e['route'] or re.search(r'sailing\s+practice', e['name'], re.I) for e in entries.values()), 'Inactive Sailing Practice exposed')
    counts = Counter(entry['platform'] for entry in entries.values())
    return entries, counts


def inspect_research(entries):
    registry = read_json('content/catalogue-research.json')
    require(set(registry) == set(RESEARCH_URLS), 'Research registry differs from reviewed source identities')
    for key, ref in registry.items():
        require(ref.get('url') == RESEARCH_URLS[key], f'Research URL/identifier mismatch: {key}')
        require(all(nonempty(ref.get(k)) for k in ('title', 'authors', 'publication', 'summary', 'relevance', 'type')), f'Incomplete research citation: {key}')
        require(isinstance(ref.get('year'), int) and 1900 <= ref['year'] <= 2100, f'Invalid research year: {key}')
        for field in ('url', 'verified_url'):
            url = urlsplit(ref.get(field, ''))
            require(url.scheme == 'https' and url.hostname and not url.username, f'Invalid research HTTPS URL: {key}/{field}')
        require(re.fullmatch(r'\d{4}-\d{2}-\d{2}', ref.get('verified_on', '')), f'Missing research review date: {key}')
    for entry in entries.values():
        ids = research_ids(entry)
        require(ids and len(ids) == len(set(ids)) and all(key in registry for key in ids), f'Unknown research reference: {entry["route"]}')
    return registry


def inspect_assets(entries):
    manifest = {}
    for filename in sorted((ROOT / 'content/catalogue').glob('*-assets.json')):
        doc = json.loads(filename.read_text())
        for item in doc.get('originals', []) + doc.get('assets', []):
            path = local_file(item['file'])
            require(re.fullmatch(r'[a-f0-9]{64}', item.get('sha256', '')) and digest(path.read_bytes()) == item['sha256'], f'Asset hash mismatch: {item["file"]}')
            require(item['file'] not in manifest, f'Duplicate manifest file: {item["file"]}')
            manifest[item['file']] = item
            data = path.read_bytes()
            if data.startswith(b'\x89PNG\r\n\x1a\n'):
                dimensions = struct.unpack('>II', data[16:24])
                expected = tuple(item.get('dimensions', [item.get('width'), item.get('height')]))
                require(dimensions == expected, f'Incorrect PNG dimensions: {item["file"]}')
            if item.get('source', '').startswith('public/'):
                source = local_file(item['source'])
                require(digest(source.read_bytes()) == item.get('source_sha256'), f'Original source hash mismatch: {item["file"]}')
            if item.get('transformation', '').startswith('None'):
                require(item['sha256'] == item.get('source_sha256'), f'Unchanged copy differs from source: {item["file"]}')
            for key in ('source_file', 'source_app_file'):
                require(not re.search(r'(^|[/_.-])(private|profiles?|user[-_]data)([/_.-]|$)', item.get(key, ''), re.I), f'Private source referenced: {item["file"]}')
            status = item.get('approval_status', item.get('status', ''))
            if 'provisional' in item['file'] or item.get('owner_review_required'):
                require('provisional' in status or 'review' in status, f'Provisional art promoted without review: {item["file"]}')
            if item.get('role') == 'application screenshot':
                require(status == 'development-ui-not-design-approval', f'Screenshot incorrectly approved: {item["file"]}')
    mapping = read_json('content/artwork-map.json')
    for route, entry in entries.items():
        direct = entry.get('artwork_file')
        if direct:
            local_file(direct)
            manifest_key = direct.lstrip('/')
            require(manifest_key in manifest, f'Untracked catalogue derivative: {direct}')
            expected = manifest[manifest_key].get('approval_status', manifest[manifest_key].get('status'))
            require(entry.get('artwork_status') == expected, f'Artwork approval mismatch: {route}')
        for key in ('artwork_route', 'hero_artwork_route'):
            if entry.get(key):
                require(entry[key] in mapping['routes'], f'Unknown artwork route: {route}/{key}')
                asset = mapping['assets'][mapping['routes'][entry[key]]]
                local_file(asset['web_file'])
                require(digest(local_file(asset['web_file']).read_bytes()) == asset['web_sha256'], f'Existing artwork hash mismatch: {route}')
                if key == 'artwork_route' and not direct and entry.get('artwork_status'):
                    require(entry['artwork_status'] == asset['status'], f'Existing artwork review status changed: {route}')
        require(direct or entry.get('artwork_route'), f'No explicit artwork mapping: {route}')
        for shot in entry.get('screenshots', []):
            local_file(shot['file'])
            manifest_key = shot['file'].lstrip('/')
            require(manifest_key in manifest, f'Untracked screenshot: {route}')
            require(shot.get('status') == manifest[manifest_key].get('approval_status') == 'development-ui-not-design-approval', f'Screenshot status mismatch: {route}')
            require(nonempty(shot.get('alt')) and nonempty(shot.get('caption')), f'Missing screenshot explanation: {route}')
    return manifest


def fragment(html, name):
    tag, css = {'hero': ('section', 'corporate-hero'), 'header': ('header', 'site-header'), 'footer': ('footer', 'site-footer')}[name]
    matches = re.findall(r'<' + tag + r' class="' + css + r'">.*?</' + tag + '>', html, re.S)
    require(len(matches) == 1, f'Expected one {name} fragment')
    return matches[0]


def inspect_baseline():
    home = (ROOT / 'index.html').read_text()
    for name in ('hero', 'header', 'footer'):
        require(digest(fragment(home, name).encode()) == BASELINE_HASHES[name], f'Approved homepage {name} changed')
    css = (ROOT / 'assets/site.css').read_bytes()
    require(digest(css[:BASELINE_CSS_LENGTH]) == BASELINE_HASHES['css'], 'Approved CSS prefix changed')
    source = (ROOT / 'scripts/build.py').read_text()
    functions = {n.name: ast.get_source_segment(source, n) for n in ast.parse(source).body if isinstance(n, ast.FunctionDef)}
    for name in ('header', 'footer'):
        require(digest(functions.get(name, '').encode()) == BASELINE_HASHES[name + '_function'], f'Shared {name} generator changed')
    # Git is an extra independent baseline check; fingerprints above always run.
    try:
        baseline_css = subprocess.run(['git', 'show', BASELINE + ':assets/site.css'], cwd=ROOT, capture_output=True, timeout=10)
    except (OSError, subprocess.TimeoutExpired):
        baseline_css = None
    if baseline_css and baseline_css.returncode == 0:
        require(len(baseline_css.stdout) == BASELINE_CSS_LENGTH and digest(baseline_css.stdout) == BASELINE_HASHES['css'], 'Pinned baseline differs from Git revision')
        require(css.startswith(baseline_css.stdout), 'CSS no longer preserves Git baseline prefix')
        mode = 'Git revision and embedded fingerprints'
    else:
        mode = 'embedded fingerprints; Git baseline unavailable'
    return home, mode


def inspect_rendered(entries, registry, home):
    generated = read_json('assets/generated-routes.json')
    require(len(generated) == len(set(generated)) and set(entries) <= set(generated), 'Rendered route manifest incomplete or duplicated')
    search = read_json('assets/search-index.json')
    search_routes = [item['url'] for item in search]
    require(len(search_routes) == len(set(search_routes)) and set(entries) <= set(search_routes), 'Catalogue search coverage incomplete or duplicated')
    baseline_header = fragment(home, 'header').replace(' aria-current="page"', '')
    baseline_footer = fragment(home, 'footer')
    for route, entry in entries.items():
        target = ROOT / route.strip('/') / 'index.html'
        require(target.is_file(), f'Missing rendered page: {route}; run scripts/build.py')
        html = target.read_text()
        page = Page(html)
        rendered_text = re.sub(r'\s+', ' ', ' '.join(page.text))
        expected_text = [entry['introduction']]
        expected_text += [entry[key] for key in ('purpose', 'audience', 'age_guidance', 'difficulty', 'status')]
        expected_text += [step[key] for step in entry['tutorial'] for key in ('title', 'text')]
        expected_text += list(entry['interaction'].values())
        expected_text += [shot['caption'] for shot in entry.get('screenshots', [])]
        require(all(re.sub(r'\s+', ' ', text).strip() in rendered_text for text in expected_text), f'Stale or missing rendered detail/tutorial/interaction text: {route}')
        require(page.parent_links == [entry['parent']], f'Expected exactly one explicit parent link: {route}')
        ancestors, parent = [], entry['parent']
        while parent in entries:
            ancestors.append(parent)
            parent = entries[parent]['parent']
        require(page.breadcrumbs == ['/', '/#laboratories'] + list(reversed(ancestors)), f'Incorrect explicit breadcrumb ancestry: {route}')
        children = [e for e in entries.values() if e['parent'] == route]
        require(Counter(page.cards) == Counter(e['id'] for e in children), f'Missing/duplicate rendered child cards: {route}')
        require(all(child['route'] in page.links for child in children), f'Unreachable rendered child: {route}')
        require(all(related in page.links for related in entry.get('related', [])), f'Related link missing in HTML: {route}')
        require('tutorial' in page.ids and 'research' in page.ids, f'Missing tutorial/research section: {route}')
        for key in research_ids(entry):
            require(registry[key]['url'] in page.links, f'Research link missing: {route}/{key}')
        for img in page.images:
            local_file(img.get('src', ''))
        for shot in entry.get('screenshots', []):
            require('/' + shot['file'].lstrip('/') in [img.get('src') for img in page.images], f'Screenshot absent from page: {route}')
        if entry.get('artwork_file'):
            # Small topic crops belong to the parent card; their own large hero
            # deliberately uses the approved experience artwork instead.
            if entry.get('hero_artwork_route'):
                parent_html = (ROOT / entry['parent'].strip('/') / 'index.html').read_text()
                own_card = re.search(r'<article\b[^>]*data-catalogue-card="' + re.escape(entry['id']) + r'"[^>]*>.*?</article>', parent_html, re.S)
                require(own_card, f'Missing parent artwork card: {route}')
                artwork_page = Page(own_card.group())
            else:
                artwork_page = page
            require(entry['artwork_status'] in artwork_page.statuses and '/' + entry['artwork_file'].lstrip('/') in [img.get('src') for img in artwork_page.images], f'Artwork or review status absent from HTML: {route}')
        if entry['platform'] == 'neuropath' and entry['kind'] == 'activity':
            hero = re.search(r'<header class="catalogue-hero">.*?</header>', html, re.S)
            require(hero and ('GlionIQ Signature Game' in hero.group()) == entry['signature'], f'Rendered signature mismatch: {route}')
        require(fragment(html, 'header').replace(' aria-current="page"', '') == baseline_header and fragment(html, 'footer') == baseline_footer, f'Shared navigation/footer differs: {route}')
        require(not re.search(r'href="[^"]*sailing-practice', html, re.I), f'Inactive practice link rendered: {route}')
    return len(generated), len(search_routes)


def main():
    try:
        entries, counts = inspect_content()
        print('PASS: ' + str(len(entries)) + ' catalogue entries (' + ', '.join(f'{key}: {counts[key]}' for key in PLATFORMS) + '); unique IDs/routes, rooted parents, related links, complete content and 30 preserved routes.')
        print('PASS: NeuroPath nine game placements/three signature markers; Dr. Quiz 28 categories/20 subcategories; inactive Sailing Practice excluded.')
    except (ValueError, AssertionError, KeyError, TypeError, OSError) as exc:
        print('FAIL: catalogue source: ' + str(exc))
        return 1
    results = {}
    for label, operation in [('research', lambda: inspect_research(entries)), ('assets', lambda: inspect_assets(entries)), ('baseline', inspect_baseline)]:
        try:
            results[label] = operation()
            print('PASS: ' + {'research': 'Reviewed research IDs, HTTPS URLs and complete citations (offline registry check).', 'assets': 'Artwork/screenshot existence, provenance hashes, PNG dimensions and approval status.', 'baseline': 'Approved Hero, shared header/footer and CSS prefix unchanged.'}[label])
        except (ValueError, AssertionError, KeyError, TypeError, OSError) as exc:
            check(False, label + ': ' + str(exc))
    if 'research' in results and 'baseline' in results:
        try:
            generated, search = inspect_rendered(entries, results['research'], results['baseline'][0])
            print(f'PASS: {len(entries)} rendered catalogue pages; explicit breadcrumbs/parent links, children, search, research and media; {generated} generated pages/{search} search entries.')
            print('PASS: baseline verification via ' + results['baseline'][1] + '.')
        except (ValueError, AssertionError, KeyError, TypeError, OSError) as exc:
            check(False, 'rendered catalogue: ' + str(exc))
    for failure in FAILURES:
        print('FAIL: ' + failure)
    if FAILURES:
        return 1
    print('NOT VERIFIED by this script: browser behavior, visual acceptance, app runtime, live URL responses or product-specific scientific efficacy.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
