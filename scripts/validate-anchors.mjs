#!/usr/bin/env node
/**
 * Source-based anchor validator.
 *
 * 배경:
 *   Docusaurus 내장 broken-anchor 검증과 별개로, Laravel 원본 문서의
 *   `<a name="xxx">` 앵커가 실제 빌드 HTML id로 렌더링되는지 확인한다.
 *
 *   이 스크립트는 "실제 빌드 산출물(HTML)"을 진실의 기준으로 삼아
 *   source markdown의 앵커 링크가 실제로 HTML id와 매칭되는지 검증한다.
 *
 * 전제:
 *   - `npm run build`가 선행되어 `build/` 디렉토리가 존재해야 함.
 *   - 빌드가 실패했으면 이 스크립트는 의미 없음.
 *
 * 사용:
 *   node scripts/validate-anchors.mjs
 *
 * 종료 코드:
 *   0 — 검증 실패 0건
 *   1 — 검증 실패 1건 이상 (id 누락 또는 타겟 HTML 누락). 상세 리스트 출력.
 *   2 — build/ 디렉토리 없음 (선행 빌드 필요).
 */
import {readFileSync, existsSync, readdirSync} from 'node:fs';
import {isAbsolute, join, relative, resolve, sep} from 'node:path';
import {fileURLToPath} from 'node:url';
import {
  extractMarkdownLinks,
  replaceVersionPlaceholders,
  stripCode,
} from './markdown-link-utils.mjs';
import {
  docsVersionFromUrl,
  fragmentTarget,
  sourceUrl,
} from './anchor-routes.mjs';
import {staleLinkResolution} from './stale-links.mjs';

// `new URL(...).pathname`은 Windows에서 `/C:/...` 형태이거나 공백이 `%20`으로
// 인코딩되어 fs API가 해석하지 못한다. fileURLToPath로 플랫폼 중립 경로를 얻는다.
const REPO_ROOT = fileURLToPath(new URL('..', import.meta.url));
const BUILD_ROOT = join(REPO_ROOT, 'build');
const DOCS_ROOTS = [
  {path: join(REPO_ROOT, 'versioned_docs'), localePrefix: ''},
  {
    path: join(
      REPO_ROOT,
      'i18n',
      'ja',
      'docusaurus-plugin-content-docs',
    ),
    localePrefix: '/ja',
  },
];

function walkMd(dir, acc = []) {
  for (const entry of readdirSync(dir, {withFileTypes: true})) {
    const full = join(dir, entry.name);
    if (entry.isDirectory()) {
      if (entry.name === 'origin') continue;
      walkMd(full, acc);
    } else if (entry.isFile() && entry.name.endsWith('.md')) {
      if (entry.name === 'documentation.md') continue; // excluded from build
      acc.push(full);
    }
  }
  return acc;
}

function htmlPathFor(url) {
  const path = resolve(BUILD_ROOT, `.${url}`, 'index.html');
  const relativePath = relative(BUILD_ROOT, path);
  if (
    isAbsolute(relativePath) ||
    relativePath === '..' ||
    relativePath.startsWith(`..${sep}`)
  ) {
    return null;
  }
  return path;
}

if (!existsSync(BUILD_ROOT)) {
  console.error('[validate-anchors] build/ not found. Run `npm run build` first.');
  process.exit(2);
}

const htmlCache = new Map();
function readHtml(path) {
  let cached = htmlCache.get(path);
  if (cached === undefined) {
    cached = readFileSync(path, 'utf-8');
    htmlCache.set(path, cached);
  }
  return cached;
}

let total = 0;
let ok = 0;
let missingHtml = 0;
let idNotFound = 0;
const broken = [];

for (const docsRoot of DOCS_ROOTS) {
  if (!existsSync(docsRoot.path)) continue;
  for (const md of walkMd(docsRoot.path)) {
    const src = stripCode(readFileSync(md, 'utf-8'));
    const srcUrl = sourceUrl(md, docsRoot.path, docsRoot.localePrefix);
    const srcVersion = docsVersionFromUrl(srcUrl);

    for (const {url: href} of extractMarkdownLinks(src)) {
      if (!href.includes('#')) continue; // not an anchor reference
      const normalizedHref = srcVersion
        ? replaceVersionPlaceholders(href, srcVersion)
        : href;
      const staleResolution = staleLinkResolution(normalizedHref, srcVersion);
      if (staleResolution?.target === null) continue;
      const effectiveHref = staleResolution?.target ?? normalizedHref;
      const target = fragmentTarget(effectiveHref, srcUrl, srcVersion);
      if (target === null) continue;

      total++;
      const {targetUrl, anchor, error} = target;
      if (error) {
        idNotFound++;
        broken.push({
          md: relative(REPO_ROOT, md),
          src: srcUrl,
          target: targetUrl,
          anchor,
          reason: error,
        });
        continue;
      }

      const hp = htmlPathFor(targetUrl);
      if (hp === null) {
        missingHtml++;
        broken.push({
          md: relative(REPO_ROOT, md),
          src: srcUrl,
          target: targetUrl,
          anchor,
          reason: 'target path outside build',
        });
        continue;
      }
      if (!existsSync(hp)) {
        missingHtml++;
        broken.push({md: relative(REPO_ROOT, md), src: srcUrl, target: targetUrl, anchor, reason: 'target HTML missing'});
        continue;
      }
      const html = readHtml(hp);
      if (html.includes(`id="${anchor}"`)) {
        ok++;
      } else {
        idNotFound++;
        broken.push({md: relative(REPO_ROOT, md), src: srcUrl, target: targetUrl, anchor, reason: 'id not found in HTML'});
      }
    }
  }
}

console.log(`Total anchor links:  ${total}`);
console.log(`  OK (id in HTML):   ${ok}`);
console.log(`  Target HTML gone:  ${missingHtml}`);
console.log(`  id not found:      ${idNotFound}`);

if (broken.length) {
  console.log('\nBroken details:');
  for (const b of broken) {
    console.log(`  [${b.reason}] ${b.md} on ${b.src} -> ${b.target}#${b.anchor}`);
  }
  process.exit(1);
}
