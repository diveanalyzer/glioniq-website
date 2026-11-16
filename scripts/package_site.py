#!/usr/bin/env python3
"""Prepare an allowlisted static artifact locally. Never upload or deploy."""
import argparse
import json
import re
import shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def package(output):
    output=Path(output).resolve()
    if output==ROOT or output.is_relative_to(ROOT): raise ValueError('Use a new output folder outside the source repository.')
    if output.exists(): raise ValueError('Output must not exist; existing artifacts are never overwritten.')
    output.mkdir(parents=True)
    files=['.nojekyll','CNAME','site.webmanifest','favicon.ico','favicon-16x16.png','favicon-32x32.png','apple-touch-icon.png','icon-192.png','icon-512.png']
    routes=json.loads((ROOT/'assets/generated-routes.json').read_text())
    for route in routes:
        if route!='/' and not re.fullmatch(r'/(?:about-us|blog|science|search|contact|journey|laboratories)(?:/[a-z0-9]+(?:-[a-z0-9]+)*)*/',route): raise ValueError('Unsafe generated route.')
    files += ['index.html' if route=='/' else route.strip('/')+'/index.html' for route in routes]
    files += ['assets/site.css','assets/site.js','assets/search-index.json']
    files += [str(path.relative_to(ROOT)) for folder in ('public/images','public/editorial') for path in (ROOT/folder).rglob('*') if path.is_file() and path.suffix.lower() in ('.png','.webp','.jpg','.jpeg','.pdf')]
    for name in files:
        source=ROOT/name
        if not source.resolve().is_relative_to(ROOT): raise ValueError('Unsafe source path.')
        target=output/name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source,target)
    print(f'Packaged {len(files)} static files locally at {output}. No publication performed.')
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',required=True);package(parser.parse_args().output)
