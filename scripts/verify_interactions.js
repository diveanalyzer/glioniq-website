#!/usr/bin/env node
'use strict';

// Pure search behavior and its generated content contract. Browser interaction
// and responsive-layout acceptance are checked separately in Safari.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const { searchEntries } = require('../assets/site.js');
const root = path.resolve(__dirname, '..');
const entries = JSON.parse(fs.readFileSync(path.join(root, 'assets/search-index.json'), 'utf8'));
assert(Array.isArray(entries) && entries.length === 13);
assert.equal(new Set(entries.map(entry => entry.url)).size, entries.length, 'Duplicate search destinations');
for (const entry of entries) {
  assert(entry.url.startsWith('/') && entry.url.endsWith('/') && !entry.url.includes('..'));
  assert(fs.existsSync(path.join(root, entry.url, 'index.html')), `Missing search destination ${entry.url}`);
  for (const field of ['title', 'description', 'text']) assert.equal(typeof entry[field], 'string');
  assert(entry.title.trim());
}

const urls = query => searchEntries(entries, query).map(entry => entry.url);
const snapshot = JSON.stringify(entries);
assert.deepEqual(urls('MeMoRy'), urls('memory'), 'Search must ignore case');
assert.deepEqual(urls('   memory   lab  '), urls('memory lab'), 'Search must normalize whitespace');
assert(urls('memory lab').includes('/laboratories/neuropath/memory/'), 'Find the named Memory Lab');
assert(urls('NeuroWeave').includes('/laboratories/neuropath/logic/'), 'Find approved signature activity');
assert(urls('Trampolina').includes('/laboratories/trampolina/'), 'Find platform by name');
assert(urls('Dr. Quiz').includes('/laboratories/dr-quiz/'), 'Find punctuated product name');
assert.deepEqual(urls('zzzznonexistentquery8675309'), [], 'Unknown terms must not produce invented results');
assert.deepEqual(urls(''), [], 'Empty query must not claim a match');
assert.deepEqual(urls('    '), [], 'Whitespace-only query must stay empty');

const fixture = [
  { url: '/one/', title: 'Memory', description: 'Learning laboratory', text: 'Blue connections' },
  { url: '/two/', title: 'Memory', description: 'Learning laboratory', text: 'Gold patterns' },
];
assert.deepEqual(searchEntries(fixture, 'memory blue').map(item => item.url), ['/one/'],
  'Multiple terms must match across searchable fields');
assert.deepEqual(searchEntries(fixture, 'memory missing'), [], 'Do not return a partial term match');
assert.equal(JSON.stringify(entries), snapshot, 'Queries must not mutate the content index');
for (const query of ['memory', 'NeuroWeave', 'Trampolina', 'science', '<script>alert(1)</script>']) {
  assert(searchEntries(entries, query).every(item => entries.some(entry => entry.url === item.url)),
    'Search results must point only to indexed content');
}
console.log('PASS: 13 real search destinations; case/whitespace normalization, multi-term matching, signature activities, empty/no-result states and immutable index.');
