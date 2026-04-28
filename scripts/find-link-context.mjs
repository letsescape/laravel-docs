#!/usr/bin/env node
/**
 * 누락된 링크의 source 컨텍스트를 찾아 출력.
 * Usage: node scripts/find-link-context.mjs <source.md> <translated.md>
 */
import {readFileSync} from 'node:fs';

const [, , sourcePath, translatedPath] = process.argv;
if (!sourcePath || !translatedPath) {
  console.error('Usage: find-link-context.mjs <source.md> <translated.md>');
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

const srcLinks = extractLinks(source).map(l => ({...l, url: l.url.replaceAll('{{version}}', version)}));
const trLinks = extractLinks(translated);

// Find which links are missing
const trCount = new Map();
for (const l of trLinks) trCount.set(l.url, (trCount.get(l.url) || 0) + 1);

const missing = [];
const seenSrc = new Map();
for (const l of srcLinks) {
  seenSrc.set(l.url, (seenSrc.get(l.url) || 0) + 1);
  const found = trCount.get(l.url) || 0;
  if (seenSrc.get(l.url) > found) {
    missing.push(l);
  }
}

console.log(`Missing links count: ${missing.length}`);
for (const m of missing) {
  // Find context in source
  // Replace version placeholder for finding
  const placeholderUrl = m.url.replace(version, '{{version}}');
  const patterns = [m.url, placeholderUrl];
  let pos = -1;
  let pattern = '';
  for (const p of patterns) {
    pos = source.indexOf(`](${p})`);
    if (pos >= 0) {
      pattern = p;
      break;
    }
  }
  if (pos < 0) {
    console.log(`\n  [${m.url}] (text: "${m.text}") — context not found`);
    continue;
  }
  // Get surrounding context: 200 chars before, 200 after
  const start = Math.max(0, pos - 200);
  const end = Math.min(source.length, pos + 200);
  const context = source.slice(start, end);
  console.log(`\n  [${m.url}] (text: "${m.text}")`);
  console.log(`  source context: "...${context.replace(/\n/g, ' ').slice(0, 400)}..."`);
}
