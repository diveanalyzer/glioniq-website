#!/usr/bin/env python3
"""Verify source integrity, artwork coverage and generated-art review status."""
from hashlib import sha256
from html.parser import HTMLParser
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
mapping = json.loads((ROOT / 'content/artwork-map.json').read_text())
for source in mapping['originals']:
    if source.get('backup_excluded') and not (ROOT / source['file']).exists():
        continue  # Personal reference stays on the owner's computer.
    assert sha256((ROOT / source['file']).read_bytes()).hexdigest() == source['sha256'], source['file']
assets = mapping['assets']
for key, asset in assets.items():
    for file_key, hash_key in [('source', 'source_sha256'), ('file', 'sha256'), ('web_file', 'web_sha256')]:
        assert sha256((ROOT / asset[file_key]).read_bytes()).hexdigest() == asset[hash_key], (key, file_key)
    assert asset['width'] * asset['web_height'] - asset['height'] * asset['web_width'] in range(-640, 641), key
expected = {e['route'] for e in json.loads((ROOT / 'content/platforms.json').read_text())}
assert set(mapping['routes']) == expected, 'Every existing laboratory/activity needs an explicit mapping'
assert {k for k, a in assets.items() if a['status'] == 'owner-review-required'} == {'colors', 'numbers', 'shapes', 'letters'}


class Images(HTMLParser):
    def __init__(self):
        super().__init__()
        self.images = []
    def handle_starttag(self, tag, attrs):
        if tag == 'img':
            self.images.append(dict(attrs))


for route, key in mapping['routes'].items():
    html = (ROOT / route.strip('/') / 'index.html').read_text()
    parser = Images()
    parser.feed(html)
    path = '/public/images/neurobreath-logo-official.jpg' if route == '/laboratories/neurobreath/' else '/' + assets[key]['web_file']
    assert any(i.get('src') == path for i in parser.images), (route, path)
    assert 'Category illustration' not in html, route
home = (ROOT / 'index.html').read_text()
for path in mapping['homepage_platforms'].values():
    assert f'src="/{path}"' in home, 'Master Design Reference platform artwork must remain'
assert '<span class="category-visual"><svg' not in home, 'No generic category SVG substitutes'
for k in ('colors', 'numbers', 'shapes', 'letters'):
    assert f'data-artwork="{k}" data-artwork-status="owner-review-required"' in home
print(f'PASS: {len(mapping["originals"])} supplied originals unchanged, {len(assets)} source/crop/web hashes valid, all {len(expected)} destinations mapped; 4 generated illustrations remain review-only.')
