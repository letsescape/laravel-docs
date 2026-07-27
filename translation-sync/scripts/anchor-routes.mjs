import {relative} from 'node:path';

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
