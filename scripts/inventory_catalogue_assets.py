#!/usr/bin/env python3
"""Inventory artwork without altering sources. Requires Pillow; --check is read-only."""
import argparse
from collections import Counter, defaultdict
from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
JSON_OUTPUT = ROOT / 'content/catalogue-assets-inventory.json'
DOC_OUTPUT = ROOT / 'docs/GLIONIQ_OFFICIAL_ASSET_MAPPING.md'
PLATFORMS = ('trampolina', 'dr-quiz', 'neuropath', 'neurobreath')
PRIVATE = 'public/images/laboratories/neuropath/04_profile/profile_setup_flow.jpeg'


def read(path):
    return json.loads((ROOT / path).read_text())


def norm(path):
    return path.lstrip('/')


def platform(path):
    return next((p for p in PLATFORMS if p in path), 'shared-branding')


def provisional(status):
    return 'provisional' in status or 'owner-review' in status


def inventory():
    old = read('content/artwork-map.json')
    branding = read('public/images/branding-provenance.json')
    home = read('public/images/development/provenance.json')
    breath = read('public/images/laboratories/neurobreath/branding-provenance.json')
    generation = read('content/artwork-generation.json')
    registry, expected, inputs = {}, defaultdict(list), {}
    errors = []

    def register(path, status, usage, evidence, digest=None, **extra):
        path = norm(path)
        registry.setdefault(path, {}).update({
            'approval_status': status, 'intended_use': usage,
            'mapping_confidence': 'high; explicit provenance or route mapping',
            'provenance': evidence, **extra,
        })
        if digest:
            expected[path].append({'source': evidence, 'sha256': digest})

    for entry in old['originals']:
        is_source = entry['role'] == 'artwork source'
        register(entry['file'], 'approved-supplied-artwork' if is_source else 'supplied-design-reference',
                 entry['role'], 'content/artwork-map.json:originals', entry['sha256'],
                 legacy_original=True, artwork_keys=entry['used_by'])
    for key, asset in old['assets'].items():
        group = 'trampolina-' + key if provisional(asset['status']) else None
        route = next(r for r, k in old['routes'].items() if k == key)
        for field, hash_field, use in [('source', 'source_sha256', 'Original source for ' + key),
                                      ('file', 'sha256', 'Preserved crop/full-resolution derivative for ' + key),
                                      ('web_file', 'web_sha256', 'Responsive website card/hero for ' + key)]:
            path = asset[field]
            # Do not overwrite source/reference identity with the derivative's status.
            if field == 'source' and path in registry:
                expected[path].append({'source': 'content/artwork-map.json:assets.' + key, 'sha256': asset[hash_field]})
                continue
            register(path, asset['status'], use, 'content/artwork-map.json:assets.' + key,
                     asset[hash_field], platform=route.split('/')[2], artwork_key=key,
                     source_file=asset['source'], review_group=group)
    for item in generation['prompts']:
        register(item['file'], generation['status'], 'Proposed Trampolina ' + item['key'] + ' illustration; not a logo',
                 'content/artwork-generation.json', platform='trampolina', review_group='trampolina-' + item['key'])
    for name, digest in branding['sources'].items():
        register('public/images/' + name, 'approved-branding-source', 'Preserved official GlionIQ branding source',
                 'public/images/branding-provenance.json:sources', digest)
    for path, digest in branding['derivatives'].items():
        register(path, 'approved-source-derivative', 'GlionIQ header/hero/icon; non-generative alpha matting or resizing',
                 'public/images/branding-provenance.json:derivatives', digest)
    register(home['source'], 'approved-master-design-reference', 'Authoritative homepage reference; retain approved visual identity',
             'public/images/development/provenance.json', home['sha256'])
    for path, digest in home['derivatives'].items():
        register(path, 'approved-reference-crop', 'Approved homepage artwork crop; reference resolution, not a new logo master',
                 'public/images/development/provenance.json:derivatives', digest)
    for field, hash_field, status, use in [
        ('reference', 'reference_sha256', 'approved-branding-reference', 'Approved NeuroBreath orb and wordmark design reference'),
        ('original_orb', 'orb_sha256', 'approved-supplied-artwork', 'Preserved original neural breathing orb'),
        ('wordmark', 'wordmark_sha256', 'approved-source-crop', 'Exact approved NeuroBreath wordmark crop, rendered separately from orb'),
    ]:
        register(breath[field], status, use, 'public/images/laboratories/neurobreath/branding-provenance.json',
                 breath[hash_field], platform='neurobreath')
    register('public/images/neurobreath-logo-official.jpg', 'approved-original-exact-copy',
             'Rendered living-orb artwork; byte-identical to supplied orb; not a redrawn logo',
             'public/images/laboratories/neurobreath/branding-provenance.json; scripts/laboratories.py:living_orb',
             breath['orb_sha256'], platform='neurobreath', source_file=breath['original_orb'])

    manifests = []
    for path in sorted((ROOT / 'content/catalogue').glob('*-assets.json')):
        relative = path.relative_to(ROOT).as_posix()
        manifest = read(relative)
        manifests.append(relative)
        for record in manifest.get('originals', []) + manifest.get('assets', []):
            status = record.get('approval_status', record.get('status', 'unverified'))
            use = record.get('intended_usage', record.get('usage', record.get('role', 'Reference source')))
            copied = {key: record[key] for key in ('source_file', 'source_repository', 'source_app_file', 'source_sha256',
                      'source', 'crop', 'transformation', 'review', 'activity', 'laboratory', 'id') if key in record}
            copied['platform'] = manifest['platform']
            if record.get('mapping_confidence'):
                copied['mapping_confidence'] = record['mapping_confidence']
            if provisional(status):
                copied['review_group'] = record.get('id', record.get('activity', 'dr-quiz-extra-category-atlas'))
            register(record['file'], status, use, relative, record.get('sha256'), **copied)

    register(PRIVATE, 'private-reference-excluded',
             'Private profile reference only; excluded from website catalogue, backups and publication; do not copy or embed',
             'content/artwork-map.json:originals.backup_excluded', excluded=True, legacy_original=True)
    paths = {p.relative_to(ROOT).as_posix() for p in (ROOT / 'public/images').rglob('*') if p.is_file()}
    paths.update(registry)
    assets, metadata = [], []
    image_ext = {'.png', '.jpg', '.jpeg', '.webp', '.gif', '.ico', '.avif'}
    for relative in sorted(paths):
        path = ROOT / relative
        meta = registry.get(relative, {})
        if path.suffix.lower() not in image_ext:
            metadata.append({'file': relative, 'format': 'JSON' if path.suffix == '.json' else 'OS metadata',
                             'intended_use': 'Provenance metadata' if path.suffix == '.json' else 'Not artwork; ignored OS metadata',
                             'excluded_from_artwork': True})
            continue
        record = {'file': relative, 'filename': path.name, 'platform': platform(relative), **meta,
                  'present': path.is_file(), 'catalogue_uses': []}
        if not path.is_file():
            if not record.get('excluded'):
                errors.append('Missing registered image: ' + relative)
            record.update(format=path.suffix.lstrip('.').upper(), width=None, height=None, sha256=None)
        else:
            digest = sha256(path.read_bytes()).hexdigest()
            try:
                with Image.open(path) as image:
                    record.update(format=image.format, width=image.width, height=image.height)
                    image.verify()
            except Exception as exc:
                errors.append('Unreadable image: ' + relative + ': ' + str(exc))
                record.update(format=path.suffix.lstrip('.').upper(), width=None, height=None)
            record.update(sha256=digest, bytes=path.stat().st_size)
            for check in expected[relative]:
                if check['sha256'] != digest:
                    errors.append('Hash mismatch: ' + relative + ' against ' + check['source'])
        record['hash_verification'] = 'PASS' if expected[relative] and record.get('present') and all(
            check['sha256'] == record['sha256'] for check in expected[relative]) else 'not pinned' if not expected[relative] else 'not present'
        record['expected_hashes'] = expected[relative]
        if not meta:
            record.update(approval_status='unclassified-owner-review', intended_use='No explicit provenance mapping found',
                          mapping_confidence='unverified')
            errors.append('Unclassified image: ' + relative)
        assets.append(record)
    by_file = {a['file']: a for a in assets}
    entries = []
    for path in sorted((ROOT / 'content/catalogue').glob('*.json')):
        relative = path.relative_to(ROOT).as_posix()
        doc = read(relative)
        if 'entries' in doc:
            entries.extend({**entry, 'content_file': relative} for entry in doc['entries'])
    by_route = {entry['route']: entry for entry in entries}

    def resolve(entry, hero=False):
        route = entry.get('hero_artwork_route') if hero else None
        route = route or entry.get('artwork_route') or entry['route']
        direct = entry.get('artwork_file') if not (hero and entry.get('hero_artwork_route')) else None
        if direct:
            return [norm(direct)], 'explicit artwork_file'
        if route.startswith('/laboratories/neurobreath/'):
            return ['public/images/neurobreath-logo-official.jpg', breath['wordmark']], 'approved orb plus separate wordmark renderer'
        if route in old['routes']:
            return [old['assets'][old['routes'][route]]['web_file']], 'explicit legacy ARTWORK route'
        errors.append('Unresolved artwork_route: ' + entry['id'] + ': ' + route)
        return [], 'unresolved'

    mappings, missing_art, missing_screenshots = [], [], []
    for entry in entries:
        primary, resolution = resolve(entry)
        hero, _ = resolve(entry, hero=True)
        parent = by_route.get(entry.get('parent'))
        parent_files = resolve(parent)[0] if parent else []
        reused = bool(primary and primary == parent_files)
        basis = 'reused parent illustration' if reused else 'dedicated mapped artwork'
        if entry['platform'] == 'neurobreath' and entry['kind'] != 'platform':
            basis = 'shared approved platform orb and wordmark'
        shots = [norm(s['file']) for s in entry.get('screenshots', [])]
        all_files = set(primary + hero + shots)
        for file in all_files:
            if file not in by_file or not by_file[file]['present']:
                errors.append('Broken catalogue asset: ' + entry['id'] + ': ' + file)
            elif by_file[file].get('excluded'):
                errors.append('Private asset referenced: ' + entry['id'])
            else:
                by_file[file]['catalogue_uses'].append(entry['id'])
        statuses = sorted({by_file[f]['approval_status'] for f in primary if f in by_file})
        mapping = {key: entry[key] for key in ('id', 'name', 'kind', 'platform', 'route', 'parent')}
        mapping.update(content_file=entry['content_file'], primary_files=primary, hero_files=hero,
                       screenshot_files=shots, mapping_type=basis, resolution=resolution,
                       mapping_confidence='high; file identity/route is explicit; reuse does not assert dedicated artwork',
                       approval_statuses=statuses, owner_review_required=any(provisional(s) for s in statuses),
                       declared_missing=entry.get('missing', []))
        mappings.append(mapping)
        if basis != 'dedicated mapped artwork' and entry['kind'] != 'platform':
            missing_art.append({'id': entry['id'], 'name': entry['name'], 'platform': entry['platform'],
                                'route': entry['route'], 'current_files': primary,
                                'reason': 'No standalone approved illustration for this entry; ' + basis + ' is intentional and labelled in this inventory.'})
        if not shots and (entry['kind'] in ('activity', 'category') or entry['platform'] == 'dr-quiz' and entry['kind'] == 'lab'):
            missing_screenshots.append({'id': entry['id'], 'name': entry['name'], 'platform': entry['platform'],
                                        'route': entry['route'], 'reason': 'No privacy-reviewed actual application screenshot supplied for this catalogue entry.'})
    for asset in assets:
        asset['catalogue_uses'].sort()
    input_paths = ['content/artwork-map.json', 'content/artwork-generation.json',
                   'public/images/branding-provenance.json', 'public/images/development/provenance.json',
                   'public/images/laboratories/neurobreath/branding-provenance.json'] + manifests
    input_paths += sorted({e['content_file'] for e in entries})
    for path in input_paths:
        inputs[path] = sha256((ROOT / path).read_bytes()).hexdigest()
    review = [a for a in assets if provisional(a['approval_status'])]
    return {'schema_version': 1, 'inspection_date': '2026-11-17', 'scope': 'Local website artwork inventory; no publication approval implied',
            'inputs': inputs, 'summary': {'catalogue_entries': len(mappings), 'image_files': len(assets),
            'legacy_originals': len(old['originals']), 'private_excluded': sum(bool(a.get('excluded')) for a in assets),
            'catalogue_counts': dict(Counter(e['platform'] for e in mappings)),
            'approval_status_counts': dict(sorted(Counter(a['approval_status'] for a in assets).items())),
            'provisional_files': len(review), 'actual_development_screenshots': sum(a['approval_status'] == 'development-ui-not-design-approval' for a in assets),
            'entries_reusing_artwork': len(missing_art), 'entries_without_actual_screenshots': len(missing_screenshots),
            'errors': len(errors)}, 'assets': assets, 'metadata_files': metadata, 'entries': mappings,
            'missing_dedicated_artwork': missing_art, 'missing_actual_screenshots': missing_screenshots,
            'errors': sorted(set(errors)),
            'notes': [
                'Approved-source status describes supplied artwork provenance, not approval of every crop, layout or application feature.',
                'The 27 legacy originals include a private profile reference that is intentionally excluded from the catalogue and publication. Metadata here does not authorize copying it.',
                'Development screenshots depict actual application UI with synthetic game state; they are neither new logos nor approved design references.',
                'Dr. Quiz category crops are small reference-resolution assets. Heroes deliberately retain the approved experience artwork.',
                'Reused parent artwork is explicitly mapped; it is not represented as a dedicated activity logo.',
                'No image pixels or original files are changed by this inventory script. No inferred approval, placeholder, generated logo or flattened website screenshot is introduced.',
            ]}


def cell(value):
    if isinstance(value, list):
        value = '; '.join(str(v) for v in value) or '—'
    return str(value).replace('|', '\\|').replace('\n', ' ')


def table(lines, headings, rows):
    lines.extend(['', '| ' + ' | '.join(headings) + ' |', '| ' + ' | '.join('---' for _ in headings) + ' |'])
    lines.extend('| ' + ' | '.join(cell(v) for v in row) + ' |' for row in rows)


def markdown(data):
    s = data['summary']
    lines = ['# GlionIQ official asset mapping', '',
             'Generated from local source files on ' + data['inspection_date'] + '. This is a provenance and mapping report, not permission to publish.', '',
             f"Coverage: **{s['catalogue_entries']} catalogue entries**, **{s['image_files']} image files**, **27 legacy supplied originals**, shared branding/icons and the approved homepage reference. **{s['actual_development_screenshots']} real NeuroPath development screenshots** are distinct from design references. Current integrity/reference errors: **{s['errors']}**.", '',
             'All image hashes, byte counts, input hashes, source provenance and complete entry references are recorded in `content/catalogue-assets-inventory.json`. Dimensions below are measured from each file with Pillow, not inferred from filenames.', '',
             '## Preservation and approval boundaries', '']
    lines.extend('- ' + note for note in data['notes'])
    lines.extend(['', 'The approved homepage reference is `design/glioniq-homepage-approved.png`. NeuroBreath uses the byte-identical original orb alias `public/images/neurobreath-logo-official.jpg` and a separately cropped approved wordmark; the legacy orb WebP remains inventoried but is not the current catalogue renderer.', '',
                  '**Private exclusion:** `public/images/laboratories/neuropath/04_profile/profile_setup_flow.jpeg` is retained only as local private reference. It is not linked, embedded, used by any catalogue entry, or authorized for backup/publication. OS `.DS_Store` files are metadata, not artwork.', '',
                  '## Original source inventory — all 27 legacy files'])
    originals = [a for a in data['assets'] if a.get('legacy_original')]
    table(lines, ['File', 'Format / dimensions', 'Platform', 'Approval / role', 'Source mapping', 'Integrity'],
          [[a['file'], f"{a['format']} {a['width']}×{a['height']}", a['platform'], a['approval_status'],
            a.get('artwork_keys', []) or a['intended_use'], a['hash_verification']] for a in originals])
    lines.extend(['', '## All remaining image assets', '', 'Includes shared branding, homepage crops, browser icons, approved reference files, source derivatives, copied atlases, provisional illustrations and real development UI. The full relative filename is intentionally retained.'])
    table(lines, ['File', 'Format / dimensions', 'Platform', 'Approval status', 'Intended use / lab or activity', 'Mapping confidence'],
          [[a['file'], f"{a['format']} {a['width']}×{a['height']}", a['platform'], a['approval_status'],
            a.get('activity', a.get('laboratory', '')) + ('; ' if a.get('activity') or a.get('laboratory') else '') + a['intended_use'],
            a['mapping_confidence']] for a in data['assets'] if not a.get('legacy_original')])
    lines.extend(['', '## Per-entry artwork mapping', '', '“Dedicated” means the mapping is specifically assigned to that catalogue entry. It does not upgrade a provisional illustration to an approved logo. Hero assets may intentionally differ from compact card assets.'])
    for platform_name in PLATFORMS:
        lines.extend(['', '### ' + platform_name])
        table(lines, ['Entry / route', 'Card artwork', 'Hero artwork', 'Mapping / confidence', 'Approval', 'Actual screenshot'],
              [[e['name'] + ' — ' + e['route'], e['primary_files'], e['hero_files'],
                e['mapping_type'] + '; high (explicit file/route)', e['approval_statuses'], e['screenshot_files'] or 'Not supplied']
               for e in data['entries'] if e['platform'] == platform_name])
    lines.extend(['', '## Owner review list', '',
                  '13 illustration concepts remain provisional: four existing Trampolina category proposals, six existing NeuroPath game proposals, and three Dr. Quiz extra-category proposals. Their source atlases and derivatives retain the same review restriction. No new artwork was generated for this catalogue inventory.'])
    table(lines, ['File', 'Concept / activity', 'Status', 'Source / provenance'],
          [[a['file'], a.get('review_group', a.get('activity', 'See provenance')), a['approval_status'], a['provenance']]
           for a in data['assets'] if provisional(a['approval_status'])])
    lines.extend(['', '## Dedicated artwork gaps', '',
                  'The following entries intentionally reuse a parent/category illustration or the approved NeuroBreath orb. Their current files resolve correctly. No distinct approved activity artwork is claimed.'])
    table(lines, ['Entry', 'Route', 'Current fallback', 'Required correction or review'],
          [[e['name'], e['route'], e['current_files'], e['reason']] for e in data['missing_dedicated_artwork']])
    lines.extend(['', '## Actual application screenshot gaps', '',
                  'These entries have no separately supplied, privacy-reviewed actual application screenshot in the website catalogue. This is an evidence gap, not a claim that the corresponding application feature is missing. Approved illustration/reference screenshots are not substituted as real development captures.'])
    table(lines, ['Platform', 'Entry', 'Route'],
          [[e['platform'], e['name'], e['route']] for e in data['missing_actual_screenshots']])
    lines.extend(['', 'The nine NeuroPath captures are explicitly labelled `development-ui-not-design-approval`. Light Paths uses the current native 2.0 tutorial capture; the legacy V1 host screenshot and the clipped debug capture are excluded. See `content/catalogue/neuropath-assets.json` for privacy review notes and exact original-copy hashes.', '',
                  '## Non-artwork files found recursively'])
    table(lines, ['File', 'Format', 'Treatment'], [[m['file'], m['format'], m['intended_use']] for m in data['metadata_files']])
    lines.extend(['', '## Reproduction and validation', '',
                  'Run with a Python environment containing Pillow:', '',
                  '```sh', 'python3 scripts/inventory_catalogue_assets.py', 'python3 scripts/inventory_catalogue_assets.py --check', '```', '',
                  'The first command writes only this report and `content/catalogue-assets-inventory.json`; `--check` verifies that they match the current source files without writing. Source image integrity, decode validity, explicit catalogue image references and private-image exclusion are checked. No app, website build, browser, Git or deployment command is invoked.', '',
                  'Validation errors: ' + ('none.' if not data['errors'] else '')])
    lines.extend('- ' + error for error in data['errors'])
    return '\n'.join(lines) + '\n'


def portable_comparison(data, stored):
    """Retain recorded local-only metadata when a clean export omits those files.

    Required images, mappings, expected hashes and validation errors are never
    normalized. A present private reference still receives the normal hash check.
    Only the explicitly excluded profile's filesystem observations and absent
    .DS_Store records may come from the existing report.
    """
    result = deepcopy(data)
    tolerated = []
    saved_assets = {item['file']: item for item in stored.get('assets', [])}
    for item in result['assets']:
        saved = saved_assets.get(item['file'], {})
        if (item['file'] == PRIVATE and item.get('excluded') and not item['present']
                and saved.get('excluded')):
            pinned = {check['sha256'] for check in item['expected_hashes']}
            if saved.get('sha256') is not None and saved['sha256'] not in pinned:
                continue  # A changed recorded private-source hash is not tolerated.
            for field in ('present', 'bytes', 'width', 'height', 'sha256', 'hash_verification'):
                if field in saved:
                    item[field] = saved[field]
                else:
                    item.pop(field, None)
            tolerated.append(item['file'])
    actual_metadata = {item['file'] for item in result['metadata_files']}
    for item in stored.get('metadata_files', []):
        path = Path(item['file'])
        if (path.name == '.DS_Store' and path.parts[:2] == ('public', 'images')
                and item['file'] not in actual_metadata and not (ROOT / path).exists()):
            canonical = {'file': item['file'], 'format': 'OS metadata',
                         'intended_use': 'Not artwork; ignored OS metadata', 'excluded_from_artwork': True}
            result['metadata_files'].append(canonical)
            tolerated.append(item['file'])
    result['metadata_files'].sort(key=lambda item: item['file'])
    return result, tolerated


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Read-only: fail if generated reports are stale or references invalid')
    args = parser.parse_args()
    data = inventory()
    comparison, tolerated = data, []
    if args.check and JSON_OUTPUT.is_file():
        comparison, tolerated = portable_comparison(data, json.loads(JSON_OUTPUT.read_text()))
    output = {JSON_OUTPUT: json.dumps(comparison, indent=2, ensure_ascii=False) + '\n', DOC_OUTPUT: markdown(comparison)}
    stale = []
    for path, text in output.items():
        if args.check:
            matches = path.is_file() and (json.loads(path.read_text()) == comparison
                                          if path == JSON_OUTPUT else path.read_text() == text)
            if not matches:
                stale.append(path.relative_to(ROOT).as_posix())
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text)
    print(json.dumps({'mode': 'check' if args.check else 'generate', **data['summary'],
                      'stale': stale, 'absent_local_only_files_tolerated': tolerated}, indent=2))
    if data['errors'] or stale:
        for error in data['errors']:
            print(error)
        raise SystemExit(1)


if __name__ == '__main__':
    main()
