import {
  existsSync,
  lstatSync,
  mkdirSync,
  readdirSync,
  readFileSync,
  writeFileSync,
} from 'node:fs';
import {basename, isAbsolute, relative, resolve, sep} from 'node:path';
import {fileURLToPath} from 'node:url';

import {DEFAULT_PARSE_FRONT_MATTER} from '@docusaurus/utils';

const repoRoot = fileURLToPath(new URL('..', import.meta.url));
const locales = ['', 'ja'];
const slugSegment = '[a-z0-9]+(?:-[a-z0-9]+)*';
const slugPattern = new RegExp(`^${slugSegment}(?:/${slugSegment})*$`);
const versionPattern = /^[a-z0-9]+(?:[.-][a-z0-9]+)*$/;
const localePattern = /^[a-z]{2}(?:-[a-z0-9]+)*$/;

const unsafeSlug = (sourceName, slug) =>
  new Error(`unsafe slug in ${sourceName}: ${JSON.stringify(slug)}`);

export const canonicalSlug = (slug, sourceName) => {
  if (slug === '/') {
    return '';
  }
  if (typeof slug !== 'string') {
    throw unsafeSlug(sourceName, slug);
  }
  const route = slug.startsWith('/') ? slug.slice(1) : slug;
  if (!slugPattern.test(route)) {
    throw unsafeSlug(sourceName, slug);
  }
  return route;
};

export const frontMatterSlug = async (content, sourceName) => {
  const {frontMatter} = await DEFAULT_PARSE_FRONT_MATTER({
    filePath: sourceName,
    fileContent: content,
  });
  return Object.hasOwn(frontMatter, 'slug')
    ? canonicalSlug(frontMatter.slug, sourceName)
    : null;
};

const escapeHtmlAttribute = (value) =>
  value.replace(
    /[&<>"']/g,
    (character) =>
      ({
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#39;',
      })[character],
  );

const scriptDataJson = (value) =>
  JSON.stringify(value).replace(
    /[<>&\u2028\u2029]/g,
    (character) =>
      `\\u${character.charCodeAt(0).toString(16).padStart(4, '0')}`,
  );

export const redirectHtml = (target) => {
  const attributeTarget = escapeHtmlAttribute(target);
  const scriptTarget = scriptDataJson(target);

  return `<!doctype html>
<html>
<head>
<meta charset="utf-8">
<meta name="robots" content="noindex">
<link rel="canonical" href="${attributeTarget}">
<meta http-equiv="refresh" content="0; url=${attributeTarget}">
<script>window.location.replace(${scriptTarget} + window.location.search + window.location.hash)</script>
</head>
<body>
<a href="${attributeTarget}">Redirecting...</a>
</body>
</html>
`;
};

const assertContained = (root, candidate) => {
  const child = relative(root, candidate);
  if (
    child === '..' ||
    child.startsWith(`..${sep}`) ||
    isAbsolute(child)
  ) {
    throw new Error(`redirect output escapes its root: ${candidate}`);
  }
};

const assertPhysicalBuildRoot = (root) => {
  if (!existsSync(root)) {
    return;
  }
  const stat = lstatSync(root);
  if (stat.isSymbolicLink() || !stat.isDirectory()) {
    throw new Error(`redirect root is not a physical directory: ${root}`);
  }
};

const collectSlugs = async (docsRoot) => {
  const slugs = new Map([['', '<implicit root>']]);

  for (const entry of readdirSync(docsRoot, {withFileTypes: true})) {
    if (
      !entry.isFile() ||
      !entry.name.endsWith('.md') ||
      entry.name.startsWith('_') ||
      ['documentation.md', 'readme.md'].includes(entry.name)
    ) {
      continue;
    }

    const filePath = resolve(docsRoot, entry.name);
    const content = readFileSync(filePath, 'utf8');
    const explicitSlug = await frontMatterSlug(content, entry.name);
    const slug =
      explicitSlug ?? canonicalSlug(basename(entry.name, '.md'), entry.name);
    const previousSource = slugs.get(slug);
    if (previousSource && slug !== '') {
      throw new Error(
        `duplicate redirect slug ${JSON.stringify(slug)} in ${previousSource} and ${entry.name}`,
      );
    }
    slugs.set(slug, entry.name);
  }

  return [...slugs.keys()];
};

export const planRedirects = async ({
  docsRoot,
  buildRoot,
  latestVersion,
  locales: requestedLocales = locales,
}) => {
  if (
    typeof latestVersion !== 'string' ||
    !versionPattern.test(latestVersion)
  ) {
    throw new Error(`unsafe documentation version: ${JSON.stringify(latestVersion)}`);
  }

  const absoluteBuildRoot = resolve(buildRoot);
  const slugs = await collectSlugs(resolve(docsRoot));
  const plan = [];

  for (const locale of requestedLocales) {
    if (locale !== '' && !localePattern.test(locale)) {
      throw new Error(`unsafe locale: ${JSON.stringify(locale)}`);
    }
    const localePrefix = locale ? `/${locale}` : '';
    const outputRoot = resolve(absoluteBuildRoot, locale, 'docs');
    assertContained(absoluteBuildRoot, outputRoot);

    for (const slug of slugs) {
      const outputDir = slug
        ? resolve(outputRoot, ...slug.split('/'))
        : outputRoot;
      const outputFile = resolve(outputDir, 'index.html');
      assertContained(outputRoot, outputDir);
      assertContained(outputRoot, outputFile);
      const target = slug
        ? `${localePrefix}/docs/${latestVersion}/${slug}/`
        : `${localePrefix}/docs/${latestVersion}/`;
      plan.push({outputDir, outputFile, target, html: redirectHtml(target)});
    }
  }

  return plan;
};

export const generateLatestDocRedirects = async (options) => {
  const plan = await planRedirects(options);
  assertPhysicalBuildRoot(resolve(options.buildRoot));
  for (const {outputDir, outputFile, html} of plan) {
    mkdirSync(outputDir, {recursive: true});
    writeFileSync(outputFile, html);
  }
  return plan.length;
};

const main = async () => {
  const versions = JSON.parse(
    readFileSync(resolve(repoRoot, 'versions.json'), 'utf8'),
  );
  const latestVersion =
    versions.find((version) => version !== 'master') ?? versions[0];
  const count = await generateLatestDocRedirects({
    docsRoot: resolve(repoRoot, 'versioned_docs', `version-${latestVersion}`),
    buildRoot: resolve(repoRoot, 'build'),
    latestVersion,
    locales,
  });
  console.log(
    `[create-latest-doc-redirects] ${count} redirects generated for ${latestVersion}`,
  );
};

if (process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  await main();
}
