#!/usr/bin/env python3
"""Reproduce the wordmark by cropping approved source pixels, never redrawing."""
from pathlib import Path
from hashlib import sha256
import json
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
source = ROOT / 'public/images/laboratories/neurobreath/approved_neurobreath_branding.png'
original_orb = ROOT / 'public/images/laboratories/neurobreath/IMG_0020 3.JPG'
output = ROOT / 'public/images/laboratories/derived/neurobreath-approved-wordmark.png'
crop = (825, 704, 1364, 787)
Image.open(source).crop(crop).save(output)
metadata = {'reference': str(source.relative_to(ROOT)), 'reference_sha256': sha256(source.read_bytes()).hexdigest(),
            'original_orb': str(original_orb.relative_to(ROOT)), 'orb_sha256': sha256(original_orb.read_bytes()).hexdigest(),
            'wordmark': str(output.relative_to(ROOT)), 'wordmark_sha256': sha256(output.read_bytes()).hexdigest(),
            'crop': crop, 'method': 'Exact RGB crop of approved wordmark only; original orb is rendered separately without redrawing.'}
(source.parent / 'branding-provenance.json').write_text(json.dumps(metadata, indent=2) + '\n')
