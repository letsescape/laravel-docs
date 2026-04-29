#!/usr/bin/env node
import {readFileSync, readdirSync, existsSync} from 'node:fs';
import {join} from 'node:path';
import {fileURLToPath} from 'node:url';
import {
  extractInternalMarkdownLinks,
  replaceVersionPlaceholders,
  stripCode,
} from './markdown-link-utils.mjs';

const REPO_ROOT = fileURLToPath(new URL('..', import.meta.url));
const SOURCE_ROOT = join(REPO_ROOT, '.github/docs-updater/source');
const DOCS_ROOT = join(REPO_ROOT, 'versioned_docs');
const EXCLUDED = new Set(['license.md', 'readme.md', 'documentation.md']);

function extractAnchors(text) {
  const anchors = [];
  const stripped = stripCode(text);
  let index = 0;

  while (index < stripped.length) {
    const tagStart = stripped.indexOf('<a', index);
    if (tagStart < 0) break;

    const tagEnd = stripped.indexOf('>', tagStart + 2);
    if (tagEnd < 0) break;

    const tag = stripped.slice(tagStart, tagEnd + 1);
    const nameStart = tag.indexOf('name=');
    if (nameStart >= 0) {
      const quote = tag[nameStart + 'name='.length];
      if (quote === '"' || quote === "'") {
        const valueStart = nameStart + 'name='.length + 1;
        const valueEnd = tag.indexOf(quote, valueStart);
        if (valueEnd >= 0) {
          anchors.push(tag.slice(valueStart, valueEnd));
        }
      }
    }
    index = tagEnd + 1;
  }

  return anchors;
}

function extractHeadings(text) {
  const stripped = stripCode(text);
  const headings = [];

  for (const line of stripped.split('\n')) {
    let level = 0;
    while (level < line.length && line[level] === '#') {
      level++;
    }
    if (level < 1 || level > 6) continue;
    if (line[level] !== ' ' && line[level] !== '\t') continue;

    headings.push({
      level,
      text: line.slice(level + 1).trim(),
    });
  }

  return headings;
}

function extractInternalLinks(text, version) {
  const links = [];
  for (const link of extractInternalMarkdownLinks(text)) {
    const url = normalizeInternalLink(link.url, version);
    if (url === null) continue;
    links.push(url);
  }
  return links;
}

function normalizeInternalLink(url, version) {
  let normalized = replaceVersionPlaceholders(url, version);
  const laravelDocsPrefix = `https://laravel.com/docs/${version}`;
  if (
    normalized === laravelDocsPrefix ||
    normalized.startsWith(`${laravelDocsPrefix}/`) ||
    normalized.startsWith(`${laravelDocsPrefix}#`)
  ) {
    normalized = `/docs/${version}${normalized.slice(laravelDocsPrefix.length)}`;
  }

  // Official docs include a few stale anchors. The translated docs keep the
  // intended reference while pointing to anchors that are actually generated.
  normalized = normalized.replaceAll('#agents-integration', '#agent-integration');
  normalized = replaceSuffix(
    normalized,
    '#actions-handled-by-resource-controller',
    '#actions-handled-by-resource-controllers',
  );
  normalized = normalized.replaceAll(
    '/migrations#writing-migrations',
    '/migrations#creating-tables',
  );
  normalized = normalized.replaceAll(
    '#method-array-sort-recursive-desc',
    '#method-array-sort-recursive',
  );
  normalized = normalized.replaceAll('/errors#logging', '/logging');
  normalized = normalized.replaceAll(
    '/helpers#fluent-strings',
    '/strings#fluent-strings',
  );
  normalized = normalized.replaceAll('##date-casting', '#date-casting');
  normalized = normalized.replaceAll(
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

function replaceSuffix(value, search, replacement) {
  if (!value.endsWith(search)) return value;
  return `${value.slice(0, -search.length)}${replacement}`;
}

function compareStrings(a, b) {
  return a.localeCompare(b);
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

  const srcAnchors = extractAnchors(source).sort(compareStrings);
  const trAnchors = extractAnchors(translated).sort(compareStrings);
  if (JSON.stringify(srcAnchors) !== JSON.stringify(trAnchors)) {
    const missing = srcAnchors.filter(a => !trAnchors.includes(a));
    const extra = trAnchors.filter(a => !srcAnchors.includes(a));
    if (missing.length) issues.push({type: 'anchor-missing', detail: missing});
    if (extra.length) issues.push({type: 'anchor-extra', detail: extra});
  }

  const srcHeadings = extractHeadings(source);
  const trHeadings = extractHeadings(translated);
  if (srcHeadings.length === trHeadings.length) {
    for (let i = 0; i < srcHeadings.length; i++) {
      if (srcHeadings[i].level !== trHeadings[i].level) {
        issues.push({
          type: 'heading-level',
          detail: `#${i}: source=${srcHeadings[i].level} (${srcHeadings[i].text}) translated=${trHeadings[i].level} (${trHeadings[i].text})`,
        });
      }
    }
  } else {
    issues.push({
      type: 'heading-count',
      detail: `source=${srcHeadings.length} translated=${trHeadings.length}`,
    });
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

const versions = readdirSync(SOURCE_ROOT)
  .filter(d => d.startsWith('version-'))
  .sort(compareStrings);
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
  for (const [v, c] of Object.entries(byVersion).sort(([a], [b]) => compareStrings(a, b))) {
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
