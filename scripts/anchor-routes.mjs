import {relative} from 'node:path';

const EXTERNAL_HREF = /^(?:[a-z][a-z\d+.-]*:|\/\/)/i;

export function sourceUrl(mdAbsPath, docsRoot, localePrefix = '') {
  const parts = relative(docsRoot, mdAbsPath).split(/[\\/]/);
  const version = parts[0].replace('version-', '');
  const tail = parts.slice(1).join('/').replace(/\.md$/, '');
  const docsPrefix = `${localePrefix}/docs`;
  if (tail === 'installation') return `${docsPrefix}/${version}/`;
  return `${docsPrefix}/${version}/${tail}/`;
}

export function docsVersionFromUrl(url) {
  const match = url.match(/^\/(?:[^/]+\/)?docs\/([^/]+)(?:\/|$)/);
  return match ? match[1] : null;
}

export function relativeTargetPath(path, srcUrl, version) {
  const localeMatch = srcUrl.match(/^\/(?:([^/]+)\/)?docs\//);
  const localePrefix = localeMatch?.[1] ? `/${localeMatch[1]}` : '';
  if (path.startsWith('/')) {
    return localePrefix && path.startsWith('/docs/') ? `${localePrefix}${path}` : path;
  }
  return `${localePrefix}/docs/${version}/${path}`;
}

export function fragmentTarget(href, srcUrl, version) {
  const hashIndex = href.indexOf('#');
  if (hashIndex < 0) return null;

  let path = href.slice(0, hashIndex);
  if (EXTERNAL_HREF.test(path)) return null;

  const queryIndex = path.indexOf('?');
  if (queryIndex >= 0) path = path.slice(0, queryIndex);
  let targetUrl = srcUrl;
  if (path) {
    path = relativeTargetPath(path, srcUrl, version);
    targetUrl = new URL(path, 'https://laravel-docs.invalid/').pathname;
    const installationSuffix = '/installation';
    if (targetUrl.endsWith(installationSuffix)) {
      targetUrl = `${targetUrl.slice(0, -installationSuffix.length)}/`;
    }
    if (!targetUrl.endsWith('/')) targetUrl += '/';
  }

  const rawAnchor = href.slice(hashIndex + 1);
  let anchor;
  try {
    anchor = decodeURIComponent(rawAnchor);
  } catch {
    return {targetUrl, anchor: rawAnchor, error: 'invalid fragment encoding'};
  }

  return {targetUrl, anchor};
}
