import {realpath} from 'node:fs/promises';
import path from 'node:path';

import {parseLocalURLPath} from '@docusaurus/utils';
import {visit} from 'unist-util-visit';

export const isPathInside = (root, candidate) => {
  const child = path.relative(path.resolve(root), path.resolve(candidate));
  return (
    child === '' ||
    (child !== '..' &&
      !child.startsWith(`..${path.sep}`) &&
      !path.isAbsolute(child))
  );
};

const unsafeAsset = (url, filePath) =>
  new Error(`unsafe local Markdown asset ${JSON.stringify(url)} in ${filePath}`);

const realpathIfPresent = async (candidate) => {
  try {
    return await realpath(candidate);
  } catch (error) {
    if (error?.code === 'ENOENT' || error?.code === 'ENOTDIR') {
      return null;
    }
    throw error;
  }
};

export const assertPathAllowed = async ({
  candidate,
  allowedRoots,
  url,
  filePath,
}) => {
  const lexicalRoots = allowedRoots.filter((root) => isPathInside(root, candidate));
  if (lexicalRoots.length === 0) {
    throw unsafeAsset(url, filePath);
  }

  const realCandidate = await realpathIfPresent(candidate);
  if (realCandidate === null) {
    return;
  }
  const realRoots = (
    await Promise.all(lexicalRoots.map((root) => realpathIfPresent(root)))
  ).filter(Boolean);
  if (!realRoots.some((root) => isPathInside(root, realCandidate))) {
    throw unsafeAsset(url, filePath);
  }
};

const isLoaderCandidate = (kind, pathname) => {
  if (kind === 'image' || pathname.startsWith('@site/')) {
    return true;
  }
  const extension = path.extname(pathname);
  return Boolean(extension) && !/\.(?:mdx?|html)$/.test(pathname);
};

export const resolveMarkdownAssetCandidates = ({
  kind,
  url,
  filePath,
  siteDir,
  staticDirs,
  allowedRoots,
}) => {
  const localUrl = parseLocalURLPath(url);
  if (!localUrl || !isLoaderCandidate(kind, localUrl.pathname)) {
    return [];
  }
  if (
    localUrl.pathname.includes('!') ||
    (localUrl.search ?? '').includes('!')
  ) {
    throw unsafeAsset(url, filePath);
  }

  let pathname;
  try {
    pathname = decodeURIComponent(localUrl.pathname);
  } catch {
    throw unsafeAsset(url, filePath);
  }
  let search;
  try {
    search = decodeURIComponent(localUrl.search ?? '');
  } catch {
    throw unsafeAsset(url, filePath);
  }
  if (/[!\\\0]/.test(pathname) || /[!\\\0]/.test(search)) {
    throw unsafeAsset(url, filePath);
  }

  if (pathname.startsWith('@site/')) {
    return [
      {
        candidate: path.join(siteDir, pathname.slice('@site/'.length)),
        roots: allowedRoots,
      },
    ];
  }
  if (path.isAbsolute(pathname)) {
    return staticDirs.map((staticDir) => ({
      candidate: path.join(staticDir, pathname),
      roots: [staticDir],
    }));
  }
  return [
    {
      candidate: path.join(path.dirname(filePath), pathname),
      roots: allowedRoots,
    },
  ];
};

export const assertFrontMatterImageAllowed = async ({
  filePath,
  image,
  sourceRoots,
  allowedRoots,
}) => {
  if (
    !sourceRoots.some((root) => isPathInside(root, filePath)) ||
    typeof image !== 'string' ||
    !image.startsWith('./')
  ) {
    return;
  }
  if (/[!\\\0]/.test(image)) {
    throw unsafeAsset(image, filePath);
  }
  const resourcePath = image.split(/[?#]/, 1)[0];
  await assertPathAllowed({
    candidate: path.resolve(path.dirname(filePath), resourcePath),
    allowedRoots,
    url: image,
    filePath,
  });
};

export default function validateLocalAssetsPlugin(options) {
  return async (tree, file) => {
    const nodes = [];
    visit(tree, ['link', 'image'], (node) => {
      nodes.push(node);
    });

    const filePath = String(file.path);
    for (const node of nodes) {
      const candidates = resolveMarkdownAssetCandidates({
        kind: node.type,
        url: node.url,
        filePath,
        ...options,
      });
      for (const {candidate, roots} of candidates) {
        await assertPathAllowed({
          candidate,
          allowedRoots: roots,
          url: node.url,
          filePath,
        });
      }
    }
  };
}
