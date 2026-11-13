#!/usr/bin/env python3
"""Check approved content, original artwork, HTML structure and local references."""
from hashlib import sha256
from html.parser import HTMLParser
from pathlib import Path
import re
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
APPROVED = {
    'content/about-us.md': '76ac31345bda9f4723afe161b757432c33549467f4a4529e6d3f22ccd7cd3ac7',
    'public/images/glioniq-coming-soon.PNG': '1bec352cca692d54d39e16f7ede7528f32eaa321c29f3fb277b51c3176c6dc3c',
    'public/images/glioniq-logo-official.PNG': '68b5f5375e51c588d45726377b1963aaa5403bbe523cde0350eb4b19449fe76f',
}


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.refs, self.ids, self.blocks, self.stack = [], [], [], []
        self.article = False
        self.current = None
        self.text = []
        self.h1 = 0

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'html':
            assert attrs.get('lang') == 'en'
        if tag == 'h1':
            self.h1 += 1
        if 'id' in attrs:
            self.ids.append(attrs['id'])
        if tag == 'img':
            assert all(attrs.get(key) for key in ('alt', 'width', 'height'))
        for key in ('href', 'src'):
            if key in attrs:
                self.refs.append(attrs[key])
        if tag == 'article':
            self.article = True
        if self.article and tag in ('h1', 'h2', 'h3', 'p'):
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


for filename, expected in APPROVED.items():
    assert sha256((ROOT / filename).read_bytes()).hexdigest() == expected, filename
print('PASS: original PNG bytes and approved Markdown checksum (3/3).')

source = (ROOT / 'content/about-us.md').read_text().strip().split('\n\n')
expected_blocks = [re.sub(r'^#{1,3} ', '', block).replace('**', '') for block in source]
reference_count = 0
for filename in ('index.html', 'about-us/index.html'):
    path = ROOT / filename
    page = Page()
    page.feed(path.read_text())
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
        assert not parsed.path.startswith('/'), f'Base-path-unsafe reference: {ref}'
        target = (path.parent / parsed.path).resolve() if parsed.path else path
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
print('PASS: relative URLs support both custom-domain root and GitHub project subpaths.')
