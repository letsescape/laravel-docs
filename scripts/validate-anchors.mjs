#!/usr/bin/env node
/**
 * Source-based anchor validator.
 *
 * 배경:
 *   Docusaurus 내장 broken-anchor 검증기는 heading 텍스트 기반 slug만 수집하므로
 *   `src/remark/anchor-mapping.ts` 플러그인이 주입한 `<a name="xxx">` → `id="xxx"`
 *   매핑을 인식하지 못해 대량의 false positive 경고를 낸다.
 *   (그래서 docusaurus.config.ts 에서 `onBrokenAnchors: 'ignore'`로 설정.)
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
 *   0 — true broken 0건
 *   1 — true broken 1건 이상 발견 (상세 리스트 출력)
 */
import {readFileSync, existsSync, readdirSync, statSync} from 'node:fs';
import {join, relative} from 'node:path';

const REPO_ROOT = new URL('..', import.meta.url).pathname;
const DOCS_ROOT = join(REPO_ROOT, 'versioned_docs');
const BUILD_ROOT = join(REPO_ROOT, 'build');
const SLUG_ROOT_FILE = 'installation.md'; // `slug: /` 매핑 파일 (링크 치환 반영)

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

function toUrlPath(mdAbsPath) {
  const rel = relative(DOCS_ROOT, mdAbsPath);
  const parts = rel.split('/');
  const versionDir = parts[0]; // version-12.x
  const version = versionDir.replace('version-', '');
  const tail = parts.slice(1).join('/').replace(/\.md$/, '');
  if (tail === 'installation') return `/docs/${version}/`;
  return `/docs/${version}/${tail}/`;
}

function htmlPathFor(url) {
  return join(BUILD_ROOT, url, 'index.html');
}

const LINK_RE = /\[[^\]]*\]\(((?:#[^)]+)|(?:\/docs\/[^)]+#[^)]+))\)/g;

if (!existsSync(BUILD_ROOT)) {
  console.error('[validate-anchors] build/ not found. Run `npm run build` first.');
  process.exit(2);
}

let total = 0;
let ok = 0;
let missingHtml = 0;
const broken = [];

for (const md of walkMd(DOCS_ROOT)) {
  const src = readFileSync(md, 'utf-8');
  const srcUrl = toUrlPath(md);
  for (const match of src.matchAll(LINK_RE)) {
    const href = match[1];
    let targetUrl;
    let anchor;
    if (href.startsWith('#')) {
      targetUrl = srcUrl;
      anchor = href.slice(1);
    } else {
      const hashIdx = href.indexOf('#');
      let path = href.slice(0, hashIdx);
      anchor = href.slice(hashIdx + 1);
      // `{{version}}` 치환 (remark 플러그인과 동일)
      const srcVersionMatch = srcUrl.match(/^\/docs\/([^/]+)\//);
      if (srcVersionMatch) {
        path = path.replaceAll('{{version}}', srcVersionMatch[1]);
      }
      // `/docs/<ver>/installation` → `/docs/<ver>/` (remark 플러그인과 동일)
      path = path.replace(/^(\/docs\/[^/]+\/)installation$/, '$1');
      if (!path.endsWith('/')) path += '/';
      targetUrl = path;
    }
    total++;
    const hp = htmlPathFor(targetUrl);
    if (!existsSync(hp)) {
      missingHtml++;
      broken.push({md: relative(REPO_ROOT, md), src: srcUrl, target: targetUrl, anchor, reason: 'target HTML missing'});
      continue;
    }
    const html = readFileSync(hp, 'utf-8');
    if (html.includes(`id="${anchor}"`)) {
      ok++;
    } else {
      broken.push({md: relative(REPO_ROOT, md), src: srcUrl, target: targetUrl, anchor, reason: 'id not found in HTML'});
    }
  }
}

const trueBroken = broken.length - missingHtml;
console.log(`Total anchor links:  ${total}`);
console.log(`  OK (id in HTML):   ${ok}`);
console.log(`  Target HTML gone:  ${missingHtml}`);
console.log(`  True broken:       ${trueBroken}`);

if (broken.length) {
  console.log('\nBroken details:');
  for (const b of broken) {
    console.log(`  [${b.reason}] ${b.md} on ${b.src} -> ${b.target}#${b.anchor}`);
  }
  process.exit(1);
}
