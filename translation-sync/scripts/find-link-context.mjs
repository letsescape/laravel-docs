#!/usr/bin/env node
/**
 * 누락된 링크의 source 컨텍스트를 찾아 출력.
 * Usage: node scripts/find-link-context.mjs <source.md> <translated.md>
 */
import {readFileSync} from 'node:fs';
import {
  extractInternalMarkdownLinks,
  extractVersionFromPath,
  replaceVersionPlaceholders,
} from './markdown-link-utils.mjs';
import {safeMarkdownPath} from './safe-paths.mjs';

const [, , sourcePath, translatedPath] = process.argv;
if (!sourcePath || !translatedPath) {
  console.error('Usage: find-link-context.mjs <source.md> <translated.md>');
  process.exit(2);
}

const sourceFile = safeMarkdownPath(sourcePath, 'sourcePath');
const translatedFile = safeMarkdownPath(translatedPath, 'translatedPath');

const source = readFileSync(sourceFile, 'utf-8');
const translated = readFileSync(translatedFile, 'utf-8');

const version = extractVersionFromPath(sourceFile);

const srcLinks = extractInternalMarkdownLinks(source).map(l => ({
  ...l,
  url: replaceVersionPlaceholders(l.url, version),
}));
const trLinks = extractInternalMarkdownLinks(translated);

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
  const placeholderUrl = version ? m.url.replaceAll(version, '{{version}}') : m.url;
  const patterns = [m.url, placeholderUrl];
  let pos = -1;
  for (const p of patterns) {
    pos = source.indexOf(`](${p})`);
    if (pos >= 0) {
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
  console.log(`  source context: "...${context.replaceAll('\n', ' ').slice(0, 400)}..."`);
}
