#!/usr/bin/env python3
"""Check approved content, original artwork, HTML structure and local references."""
from hashlib import sha256
from html.parser import HTMLParser
from pathlib import Path
import json
import re
import struct
import zlib
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
APPROVED = {
    'content/about-us.md': '0e7cabd04e9c2180bdfbb5e6cfd68246edecbcb10240f1ed8a0dfbfb4dfeb01d',
    'public/images/glioniq-coming-soon.PNG': '1bec352cca692d54d39e16f7ede7528f32eaa321c29f3fb277b51c3176c6dc3c',
    'public/images/glioniq-logo-official.PNG': '68b5f5375e51c588d45726377b1963aaa5403bbe523cde0350eb4b19449fe76f',
    'CNAME': '032cb9062e2ae84bdd721624565df97ae64ab2929e925b8e8241e94af8dfd45f',
}


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
        if tag == 'img':
            assert all(attrs.get(key) for key in ('alt', 'width', 'height'))
            if 'glioniq-' in attrs.get('src', ''):
                assert self.anchor and self.anchor.get('href') == '/', 'Brand must link to /'
                assert self.anchor.get('aria-label') == 'GlionIQ — Home'
                self.brands += 1
        for key in ('href', 'src'):
            if key in attrs:
                self.refs.append(attrs[key])
        if tag == 'article':
            self.article = True
        if self.article and tag in ('h1', 'h2', 'h3', 'h4', 'p'):
            self.current, self.text = tag, []
        if tag not in ('meta', 'link', 'img', 'br', 'hr', 'input'):
            self.stack.append(tag)

    def handle_data(self, data):
        if self.current:
            self.text.append(data)

    def handle_endtag(self, tag):
        assert self.stack and self.stack.pop() == tag, f'Unbalanced HTML: {tag}'
        if tag == self.current:
            self.blocks.append(''.join(self.text))
            self.current = None
        if tag == 'article':
            self.article = False
        if tag == 'a':
            self.anchor = None


for filename, expected in APPROVED.items():
    assert sha256((ROOT / filename).read_bytes()).hexdigest() == expected, filename
print('PASS: original PNGs, approved Markdown, and CNAME bytes unchanged (4/4).')

source = (ROOT / 'content/about-us.md').read_text().strip().split('\n\n')
expected_blocks = [re.sub(r'^#{1,4} ', '', block).replace('**', '') for block in source]
assert (ROOT / 'CNAME').read_text().strip() == 'glioniq.tech'
assert (ROOT / '.nojekyll').is_file()
reference_count = 0
for filename in ('index.html', 'about-us/index.html'):
    path = ROOT / filename
    page = Page()
    page.feed(path.read_text())
    assert 'mailto:' not in path.read_text(), 'Unverified contact address'
    assert 'info@glioniq.tech' not in path.read_text(), 'Unverified mailbox published'
    assert '<script' not in path.read_text(), 'Unexpected runtime JavaScript'
    assert 'id="contact"' in path.read_text(), 'Missing real contact section'
    assert f'https://glioniq.tech/' in path.read_text(), 'Incorrect canonical domain'
    assert 'Home</a>' in path.read_text() and 'About Us</a>' in path.read_text()
    assert 'Contact</a>' in path.read_text()
    assert page.brands == (2 if filename.startswith('about-us/') else 3)
    assert 'story-logo' not in path.read_text(), 'Redundant About Us logo'
    assert len([item for item in page.metadata if item.get('rel') == 'icon']) == 3
    assert any(item.get('rel') == 'apple-touch-icon' and item.get('sizes') == '180x180' for item in page.metadata)
    assert any(item.get('rel') == 'manifest' for item in page.metadata)
    assert not page.stack, filename
    assert page.h1 == 1, filename
    assert len(page.ids) == len(set(page.ids)), filename
    if filename.startswith('about-us/'):
        assert page.blocks == expected_blocks, 'Story wording, punctuation or paragraph order changed'
        print(f'PASS: all {len(page.blocks)} story blocks match, in order, including punctuation.')
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
            target_page = Page()
            target_page.feed(target.read_text())
            assert parsed.fragment in target_page.ids, ref
        reference_count += 1
print(f'PASS: 2 balanced English HTML pages, one H1 each, unique IDs, {reference_count} local references.')
print('PASS: every displayed brand links to /; favicon, touch-icon, and manifest metadata on both pages.')

css = ROOT / 'assets/site.css'
for ref in re.findall(r'url\([\'"]?([^\)\'\"]+)', css.read_text()):
    assert (css.parent / ref).resolve().is_file(), f'Missing CSS asset: {ref}'
print('PASS: CSS artwork reference, contact sections, domain, no unverified mailbox or runtime JS.')


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
assert {icon['sizes'] for icon in manifest['icons']} == {'192x192', '512x512'}
for icon in manifest['icons']:
    assert (ROOT / icon['src']).is_file()
provenance = json.loads((ROOT / 'public/images/branding-provenance.json').read_text())
for name, expected in provenance['derivatives'].items():
    assert sha256((ROOT / name).read_bytes()).hexdigest() == expected, name
print('PASS: PNG dimensions and real alpha, 3 ICO sizes, opaque navy app icons, manifest and derivative hashes.')
