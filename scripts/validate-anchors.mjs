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
 *   0 — 검증 실패 0건
 *   1 — 검증 실패 1건 이상 (id 누락 또는 타겟 HTML 누락). 상세 리스트 출력.
 *   2 — build/ 디렉토리 없음 (선행 빌드 필요).
 */
import {readFileSync, existsSync, readdirSync} from 'node:fs';
import {join, relative} from 'node:path';
import {fileURLToPath} from 'node:url';

// `new URL(...).pathname`은 Windows에서 `/C:/...` 형태이거나 공백이 `%20`으로
// 인코딩되어 fs API가 해석하지 못한다. fileURLToPath로 플랫폼 중립 경로를 얻는다.
const REPO_ROOT = fileURLToPath(new URL('..', import.meta.url));
const DOCS_ROOT = join(REPO_ROOT, 'versioned_docs');
const BUILD_ROOT = join(REPO_ROOT, 'build');

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
  const rel = relative(DOCS_ROOT, mdAbsPath).split(/[\\/]/);
  const version = rel[0].replace('version-', '');
  const tail = rel.slice(1).join('/').replace(/\.md$/, '');
  if (tail === 'installation') return `/docs/${version}/`;
  return `/docs/${version}/${tail}/`;
}

function htmlPathFor(url) {
  // url은 항상 `/`로 시작. leading slash를 제거해 join이 항상 BUILD_ROOT 내부에
  // 머무르게 한다(POSIX의 path.join도 안전하지만 명시적으로 처리).
  return join(BUILD_ROOT, url.replace(/^\//, ''), 'index.html');
}

// fenced code block과 inline code를 제거해 코드 샘플 안의 link-like 텍스트가
// 실제 링크로 오검출되는 것을 막는다. indexOf 기반 단순 스캔으로 정규식을
// 쓰지 않아 ReDoS 위험이 원천 차단된다.
function stripCode(src) {
  let out = '';
  let i = 0;
  while (i < src.length) {
    if (src[i] === '`' && src[i + 1] === '`' && src[i + 2] === '`') {
      const end = src.indexOf('```', i + 3);
      if (end < 0) return out;
      i = end + 3;
      continue;
    }
    if (src[i] === '`') {
      const end = src.indexOf('`', i + 1);
      const nl = src.indexOf('\n', i + 1);
      // inline code는 개행을 넘지 않는다 (CommonMark)
      if (end < 0 || (nl >= 0 && nl < end)) {
        out += src[i++];
        continue;
      }
      i = end + 1;
      continue;
    }
    out += src[i++];
  }
  return out;
}

// `[text](url)` 또는 `[text](url "title")` 패턴을 추출한다.
// 정규식 백트래킹(예: SonarQube S5852)에 의한 슈퍼리니어 런타임 가능성을
// 제거하기 위해 순수 indexOf 탐색만 사용한다.
function extractLinkHrefs(src) {
  const hrefs = [];
  let i = 0;
  while (i < src.length) {
    const lb = src.indexOf('[', i);
    if (lb < 0) break;
    const rb = src.indexOf(']', lb + 1);
    if (rb < 0) break;
    if (src[rb + 1] !== '(') {
      i = rb + 1;
      continue;
    }
    const rp = src.indexOf(')', rb + 2);
    if (rp < 0) break;
    let raw = src.slice(rb + 2, rp);
    // title suffix 제거: 첫 공백/탭/개행 이후는 href가 아님
    for (let j = 0; j < raw.length; j++) {
      const c = raw.charCodeAt(j);
      if (c === 32 || c === 9 || c === 10 || c === 13) {
        raw = raw.slice(0, j);
        break;
      }
    }
    if (raw.length > 0) hrefs.push(raw);
    i = rp + 1;
  }
  return hrefs;
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

for (const md of walkMd(DOCS_ROOT)) {
  const src = stripCode(readFileSync(md, 'utf-8'));
  const srcUrl = toUrlPath(md);
  const versionMatch = srcUrl.match(/^\/docs\/([^/]+)\//);
  const srcVersion = versionMatch ? versionMatch[1] : null;

  for (const href of extractLinkHrefs(src)) {
    if (!href.includes('#')) continue; // not an anchor reference
    const lower = href.toLowerCase();
    if (
      lower.startsWith('http://') ||
      lower.startsWith('https://') ||
      lower.startsWith('mailto:')
    ) {
      continue; // external
    }

    let targetUrl;
    let anchor;
    if (href.startsWith('#')) {
      targetUrl = srcUrl;
      anchor = href.slice(1);
    } else {
      const hashIdx = href.indexOf('#');
      let path = href.slice(0, hashIdx);
      anchor = href.slice(hashIdx + 1);
      if (srcVersion) path = path.replaceAll('{{version}}', srcVersion);
      // 상대 경로는 현재 파일의 버전 루트 기준으로 해석
      if (!path.startsWith('/') && srcVersion) {
        path = `/docs/${srcVersion}/${path}`;
      }
      // remark 플러그인과 동일한 `/installation` → `/` 재작성
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
    const html = readHtml(hp);
    if (html.includes(`id="${anchor}"`)) {
      ok++;
    } else {
      idNotFound++;
      broken.push({md: relative(REPO_ROOT, md), src: srcUrl, target: targetUrl, anchor, reason: 'id not found in HTML'});
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
