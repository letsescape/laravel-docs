import {
  lstatSync,
  mkdirSync,
  writeFileSync,
} from 'node:fs';
import {dirname, join, resolve} from 'node:path';

const slugSegment = '[a-z0-9]+(?:-[a-z0-9]+)*';
const slugPattern = new RegExp(`^${slugSegment}(?:/${slugSegment})*$`);
const versionPattern = /^[a-z0-9]+(?:[.-][a-z0-9]+)*$/;

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

export default function latestDocRedirects(_context, {latestVersion}) {
  if (
    typeof latestVersion !== 'string' ||
    !versionPattern.test(latestVersion)
  ) {
    throw new Error(`unsafe documentation version: ${JSON.stringify(latestVersion)}`);
  }

  return {
    name: 'latest-doc-redirects',
    postBuild({outDir, routesPaths, siteConfig: {baseUrl}}) {
      const root = resolve(outDir);
      const prefix = `${baseUrl}docs/${latestVersion}/`;
      const occupiedRoutes = new Set(routesPaths.map((route) => route.replace(/\/$/, '')));
      const plan = [];

      for (const target of routesPaths.filter((route) => route.startsWith(prefix))) {
        const slug = target.slice(prefix.length).replace(/\/$/, '');
        if (target !== prefix && !slugPattern.test(slug)) {
          throw new Error(`unsafe redirect slug: ${JSON.stringify(slug)}`);
        }
        const alias = `${baseUrl}docs${slug ? `/${slug}` : ''}`;
        if (occupiedRoutes.has(alias)) {
          throw new Error(`redirect conflicts with an existing route: ${alias}`);
        }
        occupiedRoutes.add(alias);
        const outputFile = join(root, 'docs', slug, 'index.html');
        if (lstatSync(outputFile, {throwIfNoEntry: false})) {
          throw new Error(`redirect output already exists: ${outputFile}`);
        }
        for (let directory = dirname(outputFile);; directory = dirname(directory)) {
          const stat = lstatSync(directory, {throwIfNoEntry: false});
          if (stat && (stat.isSymbolicLink() || !stat.isDirectory())) {
            throw new Error(`redirect output is not a physical directory: ${directory}`);
          }
          if (directory === root) break;
        }
        plan.push({outputFile, html: redirectHtml(target)});
      }

      for (const {outputFile, html} of plan) {
        mkdirSync(dirname(outputFile), {recursive: true});
        writeFileSync(outputFile, html);
      }
      console.log(`[latest-doc-redirects] ${plan.length} redirects generated for ${baseUrl}`);
    },
  };
}
