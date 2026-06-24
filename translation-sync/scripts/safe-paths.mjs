import {existsSync, realpathSync, statSync} from 'node:fs';
import {dirname, extname, isAbsolute, relative, resolve, sep} from 'node:path';
import {fileURLToPath} from 'node:url';

const REPO_ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '../..');

function isInsideRepo(path) {
  const relativePath = relative(REPO_ROOT, path);
  return (
    relativePath === '' ||
    (!isAbsolute(relativePath) &&
      relativePath !== '..' &&
      !relativePath.startsWith(`..${sep}`))
  );
}

export function safeMarkdownPath(input, label) {
  if (typeof input !== 'string' || input.length === 0 || input.includes('\0')) {
    throw new Error(`${label} must be a non-empty path`);
  }

  const resolved = resolve(REPO_ROOT, input);
  if (!isInsideRepo(resolved)) {
    throw new Error(`${label} must stay inside the repository`);
  }

  const extension = extname(resolved).toLowerCase();
  if (extension !== '.md' && extension !== '.mdx') {
    throw new Error(`${label} must be a Markdown file`);
  }

  if (!existsSync(resolved) || !statSync(resolved).isFile()) {
    throw new Error(`${label} must be an existing file`);
  }

  const realPath = realpathSync(resolved);
  if (!isInsideRepo(realPath)) {
    throw new Error(`${label} must not resolve outside the repository`);
  }

  return realPath;
}
