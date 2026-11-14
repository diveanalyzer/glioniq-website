#!/usr/bin/env python3
"""Deterministic source-pixel matting and icon export; never generate artwork.

Optional authoring dependencies: scripts/branding-requirements.txt.
Normal HTML builds and deployment do not need these dependencies.
"""
from hashlib import sha256
from pathlib import Path
import json

import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage as ndi
from scipy.interpolate import LinearNDInterpolator

ROOT = Path(__file__).resolve().parents[1]
IMAGES = ROOT / 'public/images'
ICON_VERSION = '20261114-2'
SOURCES = {
    'glioniq-logo-official.PNG': '68b5f5375e51c588d45726377b1963aaa5403bbe523cde0350eb4b19449fe76f',
    'glioniq-coming-soon.PNG': '1bec352cca692d54d39e16f7ede7528f32eaa321c29f3fb277b51c3176c6dc3c',
}
# Alpha-selection seeds inside the brain, to retain its dark interior details.
# These points are not drawing instructions and never replace source RGB pixels.
FULL_BRAIN = [(724,89),(786,85),(818,76),(852,79),(897,78),(927,75),(973,83),(1009,95),(1045,114),(1070,142),(1101,178),(1116,214),(1137,253),(1143,282),(1159,310),(1159,342),(1168,381),(1162,420),(1149,451),(1128,477),(1093,496),(1060,501),(1020,500),(1007,513),(1000,540),(970,520),(947,507),(924,482),(904,460),(886,437),(862,414),(834,414),(808,430),(780,443),(746,452),(712,458),(683,451),(660,435),(643,414),(621,405),(591,400),(565,394),(539,387),(520,375),(506,359),(498,339),(490,313),(492,290),(500,266),(511,248),(530,228),(548,204),(567,182),(588,160),(610,146),(642,126),(678,111),(705,98)]
HERO_BRAIN = [(98,90),(103,66),(122,43),(151,29),(173,28),(192,25),(206,28),(227,25),(248,29),(274,39),(292,53),(308,70),(316,91),(325,111),(327,130),(320,150),(306,164),(280,176),(271,188),(266,187),(252,171),(232,154),(214,153),(196,161),(180,160),(165,152),(150,142),(127,137),(113,128),(105,116)]


def matte(image, polygon=None, spacing=24, dilation=30):
    """Estimate the smooth navy matte from measured clean-background samples.

    Bright surfaces and seeded brain interiors retain exact source RGB. Only
    edge/glow colors are unmatted. The output has real per-pixel PNG alpha.
    """
    rgb = np.asarray(image.convert('RGB')).astype(float)
    value = np.maximum(rgb[:, :, 0], rgb[:, :, 1] * 1.15)
    seed = Image.new('L', image.size)
    if polygon:
        ImageDraw.Draw(seed).polygon(polygon, fill=255)
    core = np.asarray(seed) > 0
    exclude = ndi.binary_dilation((value > 60) | core, iterations=dilation)
    yy, xx = np.mgrid[:image.height, :image.width]
    samples = (yy % spacing == 0) & (xx % spacing == 0) & ~exclude
    samples[0, :] = samples[-1, :] = True
    samples[:, 0] = samples[:, -1] = True
    coords = np.column_stack([yy[samples], xx[samples]])
    step = max(1, spacing // 3)
    gy, gx = np.mgrid[0:image.height:step, 0:image.width:step]
    background = LinearNDInterpolator(coords, rgb[samples])(gy, gx)
    background = np.nan_to_num(background, nan=0)
    background = np.stack([
        np.asarray(Image.fromarray(background[:, :, c].astype('float32'), 'F')
                   .resize(image.size, Image.Resampling.BICUBIC)) for c in range(3)
    ], axis=2)
    residual = np.maximum(rgb - background, 0)
    alpha = np.max(residual / np.maximum(255 - background, 1), axis=2)
    solid = np.clip((value - 90) / 60, 0, 1)
    solid = solid * solid * (3 - 2 * solid)
    if polygon:
        solid[ndi.binary_erosion(core, iterations=max(1, dilation // 8))] = 1
    else:
        # The small, unobscured reference symbol has a closed luminous outline.
        enclosed = ndi.binary_fill_holes(ndi.binary_closing(value > 65, iterations=1))
        solid[ndi.binary_erosion(enclosed, iterations=1)] = 1
    alpha = np.maximum(np.maximum(alpha, solid) - .012, 0) / .988
    alpha[solid == 1] = 1
    alpha = np.clip(alpha, 0, 1)
    foreground = np.where(alpha[:, :, None] > 0,
                          (rgb - (1 - alpha[:, :, None]) * background)
                          / np.maximum(alpha[:, :, None], 1e-6), 0)
    foreground[solid == 1] = rgb[solid == 1]
    output = np.dstack([np.clip(foreground, 0, 255), alpha * 255]).astype('uint8')
    output[output[:, :, 3] == 0, :3] = 0
    return Image.fromarray(output, 'RGBA')


def square(symbol, size, padding, background=(0, 0, 0, 0)):
    mark = symbol.crop(symbol.getchannel('A').getbbox())
    inner = round(size * (1 - padding * 2))
    ratio = min(inner / mark.width, inner / mark.height)
    mark = mark.resize((round(mark.width * ratio), round(mark.height * ratio)), Image.Resampling.LANCZOS)
    canvas = Image.new('RGBA', (size, size), background)
    canvas.alpha_composite(mark, ((size - mark.width) // 2, (size - mark.height) // 2))
    return canvas


def build():
    for name, expected in SOURCES.items():
        assert sha256((IMAGES / name).read_bytes()).hexdigest() == expected, name
    official = Image.open(IMAGES / 'glioniq-logo-official.PNG').convert('RGB')
    reference = Image.open(IMAGES / 'glioniq-coming-soon.PNG').convert('RGB')
    outputs = []

    def save(image, path):
        image.save(ROOT / path, optimize=True)
        outputs.append(path)

    save(matte(official, FULL_BRAIN), 'public/images/glioniq-logo-transparent.png')
    # Exactly the existing hero region, preserving its 450 x 270 layout and art.
    hero = reference.crop((390, 8, 840, 278))
    save(matte(hero, HERO_BRAIN, spacing=8, dilation=8), 'public/images/glioniq-hero-transparent.png')
    # Use the fully visible approved header symbol. The larger brains overlap
    # lettering; reconstructing hidden parts would violate the no-redraw brief.
    symbol = matte(reference.crop((60, 1, 134, 61)), spacing=3, dilation=3)
    save(square(symbol, 768, .06), 'public/images/glioniq-brain-transparent.png')
    for size in (16, 32):
        save(square(symbol, size, .03), f'favicon-{size}x{size}.png')
    square(symbol, 48, .03).save(ROOT / 'favicon.ico', sizes=[(16,16), (32,32), (48,48)])
    outputs.append('favicon.ico')
    for size, name in [(180, 'apple-touch-icon.png'), (192, 'icon-192.png'), (512, 'icon-512.png')]:
        save(square(symbol, size, .12, (2,13,32,255)).convert('RGB'), name)
    manifest = {
        'id': '/', 'name': 'GlionIQ', 'short_name': 'GlionIQ', 'lang': 'en',
        'start_url': '/', 'scope': '/', 'display': 'standalone',
        'theme_color': '#020d20', 'background_color': '#020d20',
        'description': 'Where Neuroscience Meets Lifelong Learning',
        'icons': [{'src': f'/icon-{n}.png?v={ICON_VERSION}', 'sizes': f'{n}x{n}', 'type': 'image/png', 'purpose': 'any'} for n in (192, 512)],
    }
    (ROOT / 'site.webmanifest').write_text(json.dumps(manifest, indent=2) + '\n')
    provenance = {
        'icon_cache_version': ICON_VERSION,
        'method': 'Non-generative measured-background alpha matting; original bright surfaces retained; Lanczos icon resizing.',
        'sources': SOURCES,
        'hero_source_box': [390, 8, 840, 278],
        'brain_source_box': [60, 1, 134, 61],
        'brain_source_limit': 'The fully visible approved symbol is a 74x60 reference crop. Large icon exports are resampled, not new high-resolution artwork. Larger brains overlap lettering and are not reconstructed.',
        'derivatives': {path: sha256((ROOT / path).read_bytes()).hexdigest() for path in outputs},
    }
    (IMAGES / 'branding-provenance.json').write_text(json.dumps(provenance, indent=2) + '\n')
    print(f'Created {len(outputs)} image assets and site.webmanifest; original sources unchanged.')


if __name__ == '__main__':
    build()
