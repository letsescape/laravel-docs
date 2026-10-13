import assert from 'node:assert/strict';
import {test} from 'node:test';
import {addDocumentSeo} from './document-seo.mjs';

const siteDir = '/fixture';
const filePath = `${siteDir}/versioned_docs/version-13.x/routing.md`;
const enrich = (content, frontMatter = {}, file = filePath) =>
  addDocumentSeo({siteDir, filePath: file, result: {content, frontMatter}});

test('uses the real heading and localized paragraph after source comments and TOC', () => {
  const content = '<!-- # Wrong title -->\n# Routing\n\n- [Introduction](#introduction)\n\n<a name="introduction"></a>\n<!-- ## Introduction -->\n## Introduction\n\n<!-- English paragraph. -->\n한국어 **라우팅**과 [링크](/docs/13.x/routing), `Route`를 설명합니다.\n이어지는 문장입니다.\n';
  const result = enrich(content);
  assert.equal(result.content, content);
  assert.deepEqual(result.frontMatter, {
    title: 'Routing',
    description: '한국어 라우팅과 링크, Route를 설명합니다. 이어지는 문장입니다.',
  });
});

test('skips code, lists, blockquotes, images and HTML when choosing the description', () => {
  const result = enrich('# `Routing` {#routing}\n\n```md\nWrong\n```\n\n> Note\n\n1. Entry\n\n![image](image.png)\n\n<div>HTML block</div>\n\n本文の<span>説明</span>です。');
  assert.equal(result.frontMatter.title, 'Routing');
  assert.equal(result.frontMatter.description, '本文の説明です。');
});

test('keeps explicit metadata, other front matter and the parsed content unchanged', () => {
  const frontMatter = {title: 'Explicit', description: 'Explicit description', slug: '/', image: '/img/test.png'};
  const result = {frontMatter, content: '# Heading\n\nBody'};
  assert.equal(addDocumentSeo({siteDir, filePath, result}), result);
  assert.deepEqual(enrich(result.content, {title: 'Explicit', slug: '/'}).frontMatter,
    {title: 'Explicit', slug: '/', description: 'Body'});
  assert.deepEqual(frontMatter, result.frontMatter);
});

test('does not add metadata to pages, partials, source caches or excluded documents', () => {
  for (const file of ['src/pages/example.md', 'i18n/en/docusaurus-plugin-content-docs/version-13.x/routing.md',
    'versioned_docs/version-13.x/_partial.md', 'versioned_docs/version-13.x/_parts/example.md',
    'versioned_docs/version-13.x/origin/routing.md', 'versioned_docs/version-13.x/documentation.md',
    'versioned_docs/version-13.x/readme.md', 'versioned_docs/version-13.x/nested/readme.md',
    'versioned_docs/version-13.x/nested/documentation.md', 'versioned_docs/version-13.x/component.mdx',
    '../versioned_docs/version-13.x/routing.md']) {
    const result = {frontMatter: {}, content: '# Heading\n\nBody'};
    assert.equal(addDocumentSeo({siteDir, filePath: `${siteDir}/${file}`, result}), result, file);
  }
});

test('provides localized license metadata without changing the legal text', () => {
  for (const [file, pattern] of [
    [`${siteDir}/versioned_docs/version-8.x/license.md`, /MIT 라이선스/],
    [`${siteDir}/i18n/ja/docusaurus-plugin-content-docs/version-master/license.md`, /MIT ライセンス/],
  ]) {
    const content = 'The MIT License (MIT)\n\nCopyright (c) Taylor Otwell';
    const result = enrich(content, {}, file);
    assert.equal(result.frontMatter.title, 'License');
    assert.match(result.frontMatter.description, pattern);
    assert.equal(result.content, content);
  }
});

test('handles setext headings and is idempotent', () => {
  const result = enrich('<!-- Source -->\nRouting\n=======\n\n説明です。');
  assert.deepEqual(result.frontMatter, {title: 'Routing', description: '説明です。'});
  assert.equal(addDocumentSeo({siteDir, filePath, result}), result);
});

test('uses upgrade instructions instead of the preceding impact label', () => {
  for (const label of ['영향 가능성: 높음', '영향도: 높음', '影響の可能性: 高', 'Likelihood Of Impact: High']) {
    const result = enrich(`# Upgrade Guide\n\n**${label}**\n\n의존성을 업데이트해야 합니다.`);
    assert.equal(result.frontMatter.description, '의존성을 업데이트해야 합니다.');
  }
});
