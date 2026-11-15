#!/usr/bin/env python3
"""Check the running local preview's page, asset and icon responses."""
from concurrent.futures import ThreadPoolExecutor
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit
from urllib.request import urlopen
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
BASE = sys.argv[1] if len(sys.argv) > 1 else 'http://127.0.0.1:8787'
assert urlsplit(BASE).hostname in ('127.0.0.1', 'localhost'), 'Local preview checks only'


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.urls = []

    def handle_starttag(self, tag, attrs):
        for key, value in attrs:
            if key in ('href', 'src') and value and value.startswith('/'):
                self.urls.append(value)


paths = {'/assets/search-index.json'}
for page in ROOT.rglob('index.html'):
    if '.git' in page.parts:
        continue
    relative = page.parent.relative_to(ROOT).as_posix().strip('.')
    paths.add('/' + relative + '/' if relative else '/')
    parser = Links()
    parser.feed(page.read_text())
    paths.update(parser.urls)
paths.update(re.findall(r"url\(['\"]?(/[^)'\"]+)", (ROOT / 'assets/site.css').read_text()))
paths.update(icon['src'] for icon in json.loads((ROOT / 'site.webmanifest').read_text())['icons'])
paths = {path.split('#', 1)[0] for path in paths}


def check(path):
    with urlopen(BASE.rstrip('/') + path, timeout=15) as response:
        data = response.read()
        assert response.status == 200 and data, path
        local_path = ROOT / urlsplit(path).path.lstrip('/')
        if local_path.is_dir():
            local_path /= 'index.html'
        assert data == local_path.read_bytes(), f'Response differs from local file: {path}'
    return path


with ThreadPoolExecutor(max_workers=4) as pool:
    results = list(pool.map(check, sorted(paths)))
print(f'PASS: {len(results)} unique local page/asset URLs returned HTTP 200 and matched repository bytes.')
