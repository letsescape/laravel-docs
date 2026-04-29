#!/usr/bin/env node
import {readFileSync, writeFileSync} from 'node:fs';
import {fileURLToPath} from 'node:url';
import {dirname, resolve} from 'node:path';

const repoRoot = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const versions = JSON.parse(
  readFileSync(resolve(repoRoot, 'versions.json'), 'utf-8'),
);
const latestStable = versions.find((v) => v !== 'master') ?? versions[0];

const sidebarVersions = [...new Set([latestStable, 'master'])];
const apiDocsHref = `https://api.laravel.com/docs/${latestStable}`;

const visit = (node, state) => {
  if (Array.isArray(node)) {
    node.forEach((item) => visit(item, state));
    return;
  }
  if (node && typeof node === 'object') {
    if (
      node.type === 'link' &&
      typeof node.href === 'string' &&
      node.href.startsWith('https://api.laravel.com/docs/')
    ) {
      if (node.href !== apiDocsHref) {
        node.href = apiDocsHref;
        state.changed = true;
      }
    }
    Object.values(node).forEach((item) => visit(item, state));
  }
};

for (const version of sidebarVersions) {
  const sidebarPath = resolve(
    repoRoot,
    `versioned_sidebars/version-${version}-sidebars.json`,
  );
  const original = readFileSync(sidebarPath, 'utf-8');
  const sidebar = JSON.parse(original);
  const state = {changed: false};

  visit(sidebar, state);

  if (state.changed) {
    const trailingNewline = original.endsWith('\n') ? '\n' : '';
    writeFileSync(
      sidebarPath,
      JSON.stringify(sidebar, null, 2) + trailingNewline,
    );
    console.log(
      `[sync-versioned-links] ${version} sidebar API link -> ${latestStable}`,
    );
  } else {
    console.log(
      `[sync-versioned-links] ${version} sidebar already in sync (${latestStable})`,
    );
  }
}
