#!/usr/bin/env node
import {readFileSync, readdirSync, existsSync} from 'node:fs';
import {join, relative} from 'node:path';
import {fileURLToPath} from 'node:url';

const REPO_ROOT = fileURLToPath(new URL('..', import.meta.url));
const SOURCE_ROOT = join(REPO_ROOT, '.github/docs-updater/source');
const DOCS_ROOT = join(REPO_ROOT, 'versioned_docs');
const EXCLUDED = new Set(['license.md', 'readme.md', 'documentation.md']);

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

function extractAnchors(text) {
  return [...stripCode(text).matchAll(/<a\s+name=["']([^"']+)["']\s*\/?>/g)].map(m => m[1]);
}

function extractHeadings(text) {
  const stripped = stripCode(text);
  return [...stripped.matchAll(/^(#{1,6})\s+(.+)$/gm)].map(m => ({
    level: m[1].length,
    text: m[2].trim(),
  }));
}

function extractInternalLinks(text, version) {
  const stripped = stripCode(text);
  const links = [];
  for (const m of stripped.matchAll(/\[([^\]]+)\]\(([^)]+)\)/g)) {
    const url = normalizeInternalLink(m[2].split(/\s+/)[0], version);
    if (url === null) continue;
    if (url.startsWith('/docs/') || url.startsWith('#') || url.startsWith('{{version}}')) {
      links.push(url);
    }
  }
  return links;
}

function normalizeInternalLink(url, version) {
  let normalized = url.replace(/\{\{\s*version\s*\}\}/g, version);
  normalized = normalized.replace(
    new RegExp(`^https://laravel\\.com/docs/${version}(?=/|#|$)`),
    `/docs/${version}`,
  );

  // Official docs include a few stale anchors. The translated docs keep the
  // intended reference while pointing to anchors that are actually generated.
  normalized = normalized.replace('#agents-integration', '#agent-integration');
  normalized = normalized.replace(
    /#actions-handled-by-resource-controller$/,
    '#actions-handled-by-resource-controllers',
  );
  normalized = normalized.replace(
    '/migrations#writing-migrations',
    '/migrations#creating-tables',
  );
  normalized = normalized.replace(
    '#method-array-sort-recursive-desc',
    '#method-array-sort-recursive',
  );
  normalized = normalized.replace('/errors#logging', '/logging');
  normalized = normalized.replace(
    '/helpers#fluent-strings',
    '/strings#fluent-strings',
  );
  normalized = normalized.replace('##date-casting', '#date-casting');
  normalized = normalized.replace(
    '/database-testing#writing-factories',
    '/database-testing#defining-model-factories',
  );

  if (
    normalized === '#assert-similar-json' ||
    normalized === '#formatting-shortcode-notifications'
  ) {
    return null;
  }

  return normalized;
}

function countValues(values) {
  const counts = new Map();
  for (const value of values) counts.set(value, (counts.get(value) || 0) + 1);
  return counts;
}

function compareLinkTargets(source, translated, version) {
  const srcLinks = countValues(extractInternalLinks(source, version));
  const trLinks = countValues(extractInternalLinks(translated, version));
  const allLinks = new Set([...srcLinks.keys(), ...trLinks.keys()]);
  const diffs = [];

  for (const link of allLinks) {
    const sourceCount = srcLinks.get(link) || 0;
    const translatedCount = trLinks.get(link) || 0;
    if (sourceCount !== translatedCount) {
      diffs.push({link, source: sourceCount, translated: translatedCount});
    }
  }

  return diffs;
}

function compare(source, translated, version) {
  const issues = [];

  const srcAnchors = extractAnchors(source).sort();
  const trAnchors = extractAnchors(translated).sort();
  if (JSON.stringify(srcAnchors) !== JSON.stringify(trAnchors)) {
    const missing = srcAnchors.filter(a => !trAnchors.includes(a));
    const extra = trAnchors.filter(a => !srcAnchors.includes(a));
    if (missing.length) issues.push({type: 'anchor-missing', detail: missing});
    if (extra.length) issues.push({type: 'anchor-extra', detail: extra});
  }

  const srcHeadings = extractHeadings(source);
  const trHeadings = extractHeadings(translated);
  if (srcHeadings.length !== trHeadings.length) {
    issues.push({
      type: 'heading-count',
      detail: `source=${srcHeadings.length} translated=${trHeadings.length}`,
    });
  } else {
    for (let i = 0; i < srcHeadings.length; i++) {
      if (srcHeadings[i].level !== trHeadings[i].level) {
        issues.push({
          type: 'heading-level',
          detail: `#${i}: source=${srcHeadings[i].level} (${srcHeadings[i].text}) translated=${trHeadings[i].level} (${trHeadings[i].text})`,
        });
      }
    }
  }

  const linkDiffs = compareLinkTargets(source, translated, version);
  if (linkDiffs.length) {
    issues.push({
      type: 'internal-link-target',
      detail: linkDiffs,
    });
  }

  return issues;
}

const versions = readdirSync(SOURCE_ROOT).filter(d => d.startsWith('version-')).sort();
let total = 0;
let withIssues = 0;
const allIssues = [];

for (const versionDir of versions) {
  const sourceDir = join(SOURCE_ROOT, versionDir);
  const docsDir = join(DOCS_ROOT, versionDir);
  if (!existsSync(docsDir)) continue;

  for (const entry of readdirSync(sourceDir)) {
    if (!entry.endsWith('.md')) continue;
    if (EXCLUDED.has(entry.toLowerCase())) continue;
    const sourcePath = join(sourceDir, entry);
    const docsPath = join(docsDir, entry);
    if (!existsSync(docsPath)) {
      allIssues.push({version: versionDir, file: entry, issues: [{type: 'translation-missing'}]});
      withIssues++;
      total++;
      continue;
    }
    const source = readFileSync(sourcePath, 'utf-8');
    const translated = readFileSync(docsPath, 'utf-8');
    total++;
    const version = versionDir.replace(/^version-/, '');
    const issues = compare(source, translated, version);
    if (issues.length) {
      withIssues++;
      allIssues.push({version: versionDir, file: entry, issues});
    }
  }
}

console.log(`Total: ${total} files`);
console.log(`Files with structural issues: ${withIssues}`);

if (allIssues.length) {
  console.log('\n--- Issues by version ---');
  const byVersion = {};
  for (const f of allIssues) {
    byVersion[f.version] = (byVersion[f.version] || 0) + 1;
  }
  for (const [v, c] of Object.entries(byVersion).sort()) {
    console.log(`  ${v}: ${c}`);
  }

  console.log('\n--- Issues by type ---');
  const byType = {};
  for (const f of allIssues) {
    for (const i of f.issues) {
      byType[i.type] = (byType[i.type] || 0) + 1;
    }
  }
  for (const [t, c] of Object.entries(byType).sort((a, b) => b[1] - a[1])) {
    console.log(`  ${t}: ${c}`);
  }

  console.log('\n--- Detailed issues ---');
  for (const f of allIssues) {
    console.log(`\n[${f.version}/${f.file}]`);
    for (const i of f.issues) {
      console.log(`  ${i.type}: ${JSON.stringify(i.detail)}`);
    }
  }
  process.exit(1);
}
