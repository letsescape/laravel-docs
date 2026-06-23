import {mkdirSync, readdirSync, readFileSync, writeFileSync} from 'node:fs';
import {basename, join} from 'node:path';
import {fileURLToPath} from 'node:url';

const repoRoot = fileURLToPath(new URL('../..', import.meta.url));
const versions = JSON.parse(readFileSync(join(repoRoot, 'versions.json'), 'utf8'));
const latestVersion = versions.find((version) => version !== 'master') ?? versions[0];
const docsRoot = join(repoRoot, 'versioned_docs', `version-${latestVersion}`);
const buildRoot = join(repoRoot, 'build');
const locales = ['', 'ja'];

const frontMatterSlug = (content) => {
  if (!content.startsWith('---\n')) {
    return null;
  }

  const end = content.indexOf('\n---', 4);
  if (end < 0) {
    return null;
  }

  const frontMatter = content.slice(4, end);
  const match = frontMatter.match(/^slug:\s*['"]?([^'"\n]+)['"]?\s*$/m);

  return match ? match[1].replace(/^\/+|\/+$/g, '') : null;
};

const redirectHtml = (target) => `<!doctype html>
<html>
<head>
<meta charset="utf-8">
<meta name="robots" content="noindex">
<link rel="canonical" href="${target}">
<meta http-equiv="refresh" content="0; url=${target}">
<script>window.location.replace(${JSON.stringify(target)} + window.location.search + window.location.hash)</script>
</head>
<body>
<a href="${target}">Redirecting...</a>
</body>
</html>
`;

const writeRedirect = (locale, slug) => {
  const localePrefix = locale ? `/${locale}` : '';
  const outputDir = join(buildRoot, locale, 'docs', slug);
  const target = slug
    ? `${localePrefix}/docs/${latestVersion}/${slug}/`
    : `${localePrefix}/docs/${latestVersion}/`;

  mkdirSync(outputDir, {recursive: true});
  writeFileSync(join(outputDir, 'index.html'), redirectHtml(target));
};

const slugs = new Set(['']);

for (const entry of readdirSync(docsRoot, {withFileTypes: true})) {
  if (!entry.isFile() || !entry.name.endsWith('.md')) {
    continue;
  }

  if (['documentation.md', 'readme.md'].includes(entry.name)) {
    continue;
  }

  const filePath = join(docsRoot, entry.name);
  const content = readFileSync(filePath, 'utf8');
  const slug = frontMatterSlug(content) ?? basename(entry.name, '.md');
  slugs.add(slug);
}

for (const locale of locales) {
  for (const slug of slugs) {
    writeRedirect(locale, slug);
  }
}

console.log(`[create-latest-doc-redirects] ${slugs.size} redirects generated for ${latestVersion}`);
