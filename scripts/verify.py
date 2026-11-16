#!/usr/bin/env python3
"""Check the complete static site, approved story, artwork, icons and links."""
from hashlib import sha256
from html.parser import HTMLParser
from pathlib import Path
import json
import re
import struct
import zlib
from urllib.parse import parse_qs, urlsplit

ROOT = Path(__file__).resolve().parents[1]
provenance = json.loads((ROOT / 'public/images/branding-provenance.json').read_text())
icon_version = provenance['icon_cache_version']
assert icon_version, 'Missing icon cache version'
APPROVED = {
    'content/about-us.md': '0e7cabd04e9c2180bdfbb5e6cfd68246edecbcb10240f1ed8a0dfbfb4dfeb01d',
    'public/images/glioniq-coming-soon.PNG': '1bec352cca692d54d39e16f7ede7528f32eaa321c29f3fb277b51c3176c6dc3c',
    'public/images/glioniq-logo-official.PNG': '68b5f5375e51c588d45726377b1963aaa5403bbe523cde0350eb4b19449fe76f',
    'CNAME': '032cb9062e2ae84bdd721624565df97ae64ab2929e925b8e8241e94af8dfd45f',
    'public/images/neurobreath-logo-official.jpg': '6866c599f679a561dbe5aa78e7ed4dcaeb5fd19246c7f17790d7882ba065ac4b',
    'design/glioniq-homepage-approved.png': '6309d5952eb403822a4becfda6f357b6108f1e9b501336c059a135c17921b152',
}

ROUTES = ['/', '/about-us/', '/search/'] + [entry['route'] for filename in ('platforms.json','pages.json') for entry in json.loads((ROOT/'content'/filename).read_text())]
ROUTES += [item['url'] for item in json.loads((ROOT/'assets/search-index.json').read_text()) if item['url'] not in ROUTES]


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.refs, self.ids, self.blocks, self.stack = [], [], [], []
        self.article = False
        self.current = None
        self.text = []
        self.h1 = 0
        self.anchor = None
        self.brands = 0
        self.metadata = []
        self.scripts = []
        self.forms = []
        self.details = []
        self.detail_stack = []
        self.buttons = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'html':
            assert attrs.get('lang') == 'en'
        if tag == 'h1':
            self.h1 += 1
        if 'id' in attrs:
            self.ids.append(attrs['id'])
        if tag == 'a':
            self.anchor = attrs
        if tag == 'link':
            self.metadata.append(attrs)
        if tag == 'script':
            self.scripts.append(attrs)
        if tag == 'form':
            self.forms.append(attrs)
        if tag == 'details':
            self.detail_stack.append({'attrs': attrs, 'summaries': 0, 'summary_text': [], 'summary_links': 0, 'refs': []})
        if tag == 'summary' and self.detail_stack:
            self.detail_stack[-1]['summaries'] += 1
        if tag == 'a' and self.detail_stack:
            self.detail_stack[-1]['refs'].append(attrs.get('href', ''))
            if 'summary' in self.stack:
                self.detail_stack[-1]['summary_links'] += 1
        if tag == 'button':
            self.buttons.append(attrs)
        if tag == 'img':
            assert 'alt' in attrs and all(attrs.get(key) for key in ('width', 'height'))
            if self.anchor and self.anchor.get('aria-label') == 'GlionIQ — Home':
                assert self.anchor and self.anchor.get('href') == '/', 'Brand must link to /'
                self.brands += 1
        for key in ('href', 'src', 'action'):
            if key in attrs:
                self.refs.append(attrs[key])
        if tag == 'article':
            self.article = True
        if self.article and tag in ('h1', 'h2', 'h3', 'h4', 'p'):
            self.current, self.text = tag, []
        if tag not in ('meta', 'link', 'img', 'br', 'hr', 'input', 'source', 'wbr', 'area', 'col', 'embed', 'param', 'track', 'base'):
            self.stack.append(tag)

    def handle_data(self, data):
        if self.current:
            self.text.append(data)
        if self.detail_stack and 'summary' in self.stack:
            self.detail_stack[-1]['summary_text'].append(data)

    def handle_endtag(self, tag):
        assert self.stack and self.stack.pop() == tag, f'Unbalanced HTML: {tag}'
        if tag == self.current:
            self.blocks.append(''.join(self.text))
            self.current = None
        if tag == 'article':
            self.article = False
        if tag == 'a':
            self.anchor = None
        if tag == 'details':
            self.details.append(self.detail_stack.pop())


for filename, expected in APPROVED.items():
    assert sha256((ROOT / filename).read_bytes()).hexdigest() == expected, filename
print(f'PASS: approved original artwork, reference, Markdown, and CNAME bytes unchanged ({len(APPROVED)}/{len(APPROVED)}).')

source = (ROOT / 'content/about-us.md').read_text().strip().split('\n\n')
expected_blocks = [re.sub(r'^#{1,4} ', '', block).replace('**', '') for block in source]
assert (ROOT / 'CNAME').read_text().strip() == 'glioniq.tech'
assert (ROOT / '.nojekyll').is_file()
reference_count = 0
pages = {}
for route in ROUTES:
    filename = route.lstrip('/') + 'index.html'
    path = ROOT / filename
    assert path.is_file(), f'Missing required route: {route}'
    html = path.read_text()
    page = Page()
    page.feed(html)
    pages[path.resolve()] = page
    assert 'mailto:' not in html and 'info@glioniq.tech' not in html, 'Unverified contact address'
    assert all(urlsplit(script.get('src','')).path == '/assets/site.js' and 'defer' in script for script in page.scripts), 'Unexpected or blocking runtime JavaScript'
    assert len(page.scripts) == 1, f'Missing shared interaction script: {route}'
    assert f'https://glioniq.tech{route}' in html, 'Incorrect canonical domain'
    for destination in ('/', '/about-us/', '/science/', '/blog/', '/contact/', '/search/'):
        assert destination in page.refs, f'Missing shared navigation {destination} on {route}'
    assert page.brands == (3 if route == '/' else 2), f'Brand count on {route}: {page.brands}'
    assert 'story-logo' not in html, 'Redundant About Us logo'
    assert len([item for item in page.metadata if item.get('rel') == 'icon']) == 3
    assert any(item.get('rel') == 'apple-touch-icon' and item.get('sizes') == '180x180' for item in page.metadata)
    assert any(item.get('rel') == 'manifest' for item in page.metadata)
    icon_links = [item for item in page.metadata if item.get('rel') in ('icon', 'apple-touch-icon', 'manifest')]
    for item in icon_links:
        url = urlsplit(item['href'])
        assert url.path.startswith('/') and parse_qs(url.query) == {'v': [icon_version]}, 'Unversioned or inconsistent icon reference'
    assert {urlsplit(item['href']).path for item in icon_links} == {
        '/favicon.ico', '/favicon-16x16.png', '/favicon-32x32.png',
        '/apple-touch-icon.png', '/site.webmanifest'}, 'Incorrect icon paths'
    assert not page.stack, filename
    assert page.h1 == 1, filename
    assert len(page.ids) == len(set(page.ids)), filename
    if route == '/about-us/':
        assert page.blocks == expected_blocks, 'Story wording, punctuation or paragraph order changed'
        print(f'PASS: all {len(page.blocks)} story blocks match, in order, including punctuation.')
    for form in page.forms:
        assert form.get('method', 'get').lower() == 'get' and form.get('action') == '/search/', 'Unexpected data-collecting form'
    for detail in page.details:
        assert detail['summaries'] == 1 and ''.join(detail['summary_text']).strip(), 'Disclosure needs one named summary'
        assert detail['summary_links'] == 0, 'Keep navigation separate from the disclosure control'

home = pages[(ROOT / 'index.html').resolve()]
for platform in json.loads((ROOT/'content/laboratories.json').read_text()):
    route = platform['route']+'explore/'
    assert route in home.refs, 'Discover must open its dedicated tree'
    assert platform['route'] in home.refs, 'Explore must keep its original destination'
    tree = pages[(ROOT/route.strip('/')/'index.html').resolve()]
    assert {b['route'] for b in platform['branches']} <= set(tree.refs), platform['name']
    assert '/#platform-'+platform['key'] in tree.refs
    assert not any(b['route'] in home.refs for b in platform['branches']), 'No branches appended to home'
assert 'laboratory-panel' not in home.ids
assert len(home.details) == 1
assert '/public/images/neurobreath-logo-official.jpg' in home.refs
search_html=(ROOT/'search/index.html').read_text()
assert 'Search GlionIQ laboratories, platforms and research…' in search_html
assert 'Discover our platforms, laboratories and scientific insights.' in search_html
assert 'Try memory or Trampolina' not in search_html and 'Enter a topic to search.' not in search_html
runtime=(ROOT/'assets/site.js').read_text()
assert not any(word in runtime for word in ['pointerenter','pointermove','pointerleave','mouseenter','mouseleave','setTimeout']), 'No timed or pointer-driven expansion'
print('PASS: four dedicated exploration routes, no appended panel, official NeuroBreath image and corrected search source output.')

for path, page in pages.items():
    for ref in page.refs:
        parsed = urlsplit(ref)
        if parsed.scheme or parsed.netloc:
            continue
        target = ((ROOT / parsed.path.lstrip('/')) if parsed.path.startswith('/')
                  else (path.parent / parsed.path)).resolve() if parsed.path else path
        assert target.is_relative_to(ROOT), ref
        if target.is_dir():
            target /= 'index.html'
        assert target.is_file(), f'Missing target: {ref}'
        if parsed.fragment:
            assert target in pages, f'Anchor targets a non-page: {ref}'
            target_page = pages[target]
            assert parsed.fragment in target_page.ids, ref
        reference_count += 1
print(f'PASS: {len(pages)} balanced English HTML pages, one H1 each, unique IDs, {reference_count} local references.')
print('PASS: shared navigation, Home-linked branding, deferred local JavaScript, and versioned icon metadata on every page.')

css = ROOT / 'assets/site.css'
for ref in re.findall(r'url\([\'"]?([^\)\'\"]+)', css.read_text()):
    parsed = urlsplit(ref)
    assert not parsed.scheme and not parsed.netloc, f'Unexpected external CSS asset: {ref}'
    target = (ROOT / parsed.path.lstrip('/')) if parsed.path.startswith('/') else css.parent / parsed.path
    assert target.resolve().is_relative_to(ROOT) and target.is_file(), f'Missing CSS asset: {ref}'
print('PASS: CSS artwork references, canonical domain, and no unverified mailbox or data-collecting forms.')


def png(path):
    """Read our RGB/RGBA PNGs without optional image-authoring dependencies."""
    data = path.read_bytes()
    assert data[:8] == b'\x89PNG\r\n\x1a\n', path
    width, height, depth, kind, _, _, interlace = struct.unpack('>IIBBBBB', data[16:29])
    assert depth == 8 and kind in (2, 6) and interlace == 0, path
    channels = 4 if kind == 6 else 3
    compressed = b''
    offset = 8
    while offset < len(data):
        length = struct.unpack('>I', data[offset:offset + 4])[0]
        if data[offset + 4:offset + 8] == b'IDAT':
            compressed += data[offset + 8:offset + 8 + length]
        offset += length + 12
    raw = zlib.decompress(compressed)
    stride = width * channels
    previous = bytearray(stride)
    rows = []
    for y in range(height):
        start = y * (stride + 1)
        method = raw[start]
        row = bytearray(raw[start + 1:start + stride + 1])
        for x in range(stride):
            left = row[x - channels] if x >= channels else 0
            above = previous[x]
            corner = previous[x - channels] if x >= channels else 0
            if method == 1:
                predictor = left
            elif method == 2:
                predictor = above
            elif method == 3:
                predictor = (left + above) // 2
            elif method == 4:
                p = left + above - corner
                distances = (abs(p - left), abs(p - above), abs(p - corner))
                predictor = (left, above, corner)[distances.index(min(distances))]
            else:
                assert method == 0
                predictor = 0
            row[x] = (row[x] + predictor) & 255
        rows.append(row)
        previous = row
    return width, height, channels, rows


assets = {
    'favicon-16x16.png': (16, 16, True),
    'favicon-32x32.png': (32, 32, True),
    'apple-touch-icon.png': (180, 180, False),
    'icon-192.png': (192, 192, False),
    'icon-512.png': (512, 512, False),
    'public/images/glioniq-hero-transparent.png': (450, 270, True),
    'public/images/glioniq-brain-transparent.png': (768, 768, True),
    'public/images/glioniq-logo-transparent.png': (1536, 1024, True),
}
for name, (expected_width, expected_height, transparent) in assets.items():
    width, height, channels, rows = png(ROOT / name)
    assert (width, height) == (expected_width, expected_height), name
    if transparent:
        assert channels == 4, name
        alpha = [a for row in rows for a in row[3::4]]
        assert min(alpha) == 0 and max(alpha) > 200, name
        assert any(0 < a < 255 for a in alpha), 'Missing antialiased alpha'
        assert all(row[x] == 0 for row in (rows[0], rows[-1]) for x in (3, len(row)-1)), name
    else:
        assert channels == 3, name
        assert tuple(rows[0][:3]) == (2, 13, 32), 'Home-screen icon background'
ico = (ROOT / 'favicon.ico').read_bytes()
assert struct.unpack('<HHH', ico[:6]) == (0, 1, 3)
assert {(ico[6+i*16], ico[7+i*16]) for i in range(3)} == {(16,16), (32,32), (48,48)}
manifest = json.loads((ROOT / 'site.webmanifest').read_text())
assert manifest['start_url'] == '/' and manifest['scope'] == '/'
assert manifest['name'] == manifest['short_name'] == 'GlionIQ'
assert manifest['theme_color'] == manifest['background_color'] == '#020d20'
assert {icon['sizes'] for icon in manifest['icons']} == {'192x192', '512x512'}
for icon in manifest['icons']:
    url = urlsplit(icon['src'])
    size = icon['sizes'].split('x')[0]
    assert url.path == f'/icon-{size}.png' and icon['type'] == 'image/png'
    assert parse_qs(url.query) == {'v': [icon_version]}
    assert (ROOT / url.path.lstrip('/')).is_file()
for name, expected in provenance['derivatives'].items():
    assert sha256((ROOT / name).read_bytes()).hexdigest() == expected, name
print('PASS: PNG dimensions and real alpha, 3 ICO sizes, opaque navy app icons, manifest and derivative hashes.')
