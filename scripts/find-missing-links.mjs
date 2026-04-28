#!/usr/bin/env node
import {readFileSync} from 'node:fs';

const [, , sourcePath, translatedPath] = process.argv;
if (!sourcePath || !translatedPath) {
  console.error('Usage: find-missing-links.mjs <source.md> <translated.md>');
  process.exit(2);
}

function stripCode(src) {
  let out = '';
  let i = 0;
  while (i < src.length) {
    if (src.startsWith('```', i)) {
      const end = src.indexOf('```', i + 3);
      if (end < 0) return out;
      i = end + 3;
      continue;
    }
    if (src[i] === '`') {
      const end = src.indexOf('`', i + 1);
      const nl = src.indexOf('\n', i + 1);
      if (end < 0 || (nl >= 0 && nl < end)) {
        out += src[i++];
        continue;
      }
      i = end + 1;
      continue;
    }
    out += src[i++];
  }
  return out;
}

function extractLinks(text) {
  const stripped = stripCode(text);
  const links = [];
  for (const m of stripped.matchAll(/\[([^\]]+)\]\(([^)]+)\)/g)) {
    const url = m[2].split(/\s+/)[0];
    if (url.startsWith('/docs/') || url.startsWith('#') || url.startsWith('{{version}}')) {
      links.push({url, text: m[1]});
    }
  }
  return links;
}

const source = readFileSync(sourcePath, 'utf-8');
const translated = readFileSync(translatedPath, 'utf-8');

const versionMatch = sourcePath.match(/version-([^/]+)/);
const version = versionMatch ? versionMatch[1] : null;

const srcLinks = extractLinks(source).map(l => l.url.replaceAll('{{version}}', version));
const trLinks = extractLinks(translated).map(l => l.url);

console.log(`Source links: ${srcLinks.length}`);
console.log(`Translated links: ${trLinks.length}`);

// Multiset diff
const srcCount = new Map();
for (const u of srcLinks) srcCount.set(u, (srcCount.get(u) || 0) + 1);
const trCount = new Map();
for (const u of trLinks) trCount.set(u, (trCount.get(u) || 0) + 1);

const allUrls = new Set([...srcCount.keys(), ...trCount.keys()]);
const missing = [];
const extra = [];

for (const url of allUrls) {
  const s = srcCount.get(url) || 0;
  const t = trCount.get(url) || 0;
  if (s > t) missing.push({url, missing: s - t, source: s, translated: t});
  if (t > s) extra.push({url, extra: t - s, source: s, translated: t});
}

if (missing.length) {
  console.log('\nLinks missing in translation:');
  for (const m of missing) console.log(`  ${m.url} (source=${m.source}, translated=${m.translated})`);
}
if (extra.length) {
  console.log('\nLinks extra in translation:');
  for (const e of extra) console.log(`  ${e.url} (source=${e.source}, translated=${e.translated})`);
}
