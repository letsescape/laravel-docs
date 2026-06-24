#!/usr/bin/env node
import {readFileSync} from 'node:fs';
import {
  extractInternalMarkdownLinks,
  extractVersionFromPath,
  replaceVersionPlaceholders,
} from './markdown-link-utils.mjs';
import {safeMarkdownPath} from './safe-paths.mjs';

const [, , sourcePath, translatedPath] = process.argv;
if (!sourcePath || !translatedPath) {
  console.error('Usage: find-missing-links.mjs <source.md> <translated.md>');
  process.exit(2);
}

const sourceFile = safeMarkdownPath(sourcePath, 'sourcePath');
const translatedFile = safeMarkdownPath(translatedPath, 'translatedPath');

const source = readFileSync(sourceFile, 'utf-8');
const translated = readFileSync(translatedFile, 'utf-8');

const version = extractVersionFromPath(sourceFile);

const srcLinks = extractInternalMarkdownLinks(source).map(l =>
  replaceVersionPlaceholders(l.url, version),
);
const trLinks = extractInternalMarkdownLinks(translated).map(l => l.url);

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
