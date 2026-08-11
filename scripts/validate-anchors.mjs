#!/usr/bin/env node
/**
 * 소스 기반 앵커 검사기
 *
 * 배경:
 *
 * - Docusaurus 내장 앵커 오류 검증과 별도로 Laravel 원본 문서의 `<a name="xxx">` 앵커가 실제 빌드 HTML의 `id`로 렌더링되는지 확인
 * - 실제 빌드 산출물(HTML)을 기준으로 원본 Markdown의 앵커 링크가 HTML `id`와 일치하는지 검증
 * - stale-link 레지스트리의 교체·폐기 규칙을 적용한 최종 대상 검증
 *
 * 전제:
 *
 * - `npm run build`를 먼저 실행해 `build/` 디렉터리가 존재해야 함
 * - 빌드 실패 시 이 스크립트는 의미 없음
 *
 * 사용:
 *
 * node scripts/validate-anchors.mjs
 *
 * 종료 코드:
 *
 * - 0 — 검증 실패 없음
 * - 1 — 검증 실패 1건 이상(`id` 또는 대상 HTML 누락), 상세 목록 출력
 * - 2 — `build/` 디렉터리 없음(선행 빌드 필요)
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

// Windows에서 `new URL(...).pathname`은 `/C:/...` 형식으로 나타나거나 공백을 `%20`으로 인코딩
// `fs` API가 해석하지 못하므로 `fileURLToPath`로 플랫폼 독립 경로 획득
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
      if (entry.name === 'documentation.md') continue; // 빌드 제외
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
      if (!href.includes('#')) continue; // 앵커 참조 아님
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
