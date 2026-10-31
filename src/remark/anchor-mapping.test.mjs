import assert from 'node:assert/strict';
import test from 'node:test';

import headings from '@docusaurus/mdx-loader/lib/remark/headings/index.js';
import rehypeRaw from 'rehype-raw';
import remarkParse from 'remark-parse';
import remarkRehype from 'remark-rehype';
import {unified} from 'unified';
import {visit} from 'unist-util-visit';

import safeHtmlPlugin from '../rehype/safe-html.mjs';
import anchorMappingPlugin from './anchor-mapping.ts';

const renderElements = async (markdown) => {
  const processor = unified()
    .use(remarkParse)
    .use(anchorMappingPlugin)
    .use(headings.default, {anchorsMaintainCase: false})
    .use(remarkRehype, {allowDangerousHtml: true})
    .use(rehypeRaw)
    .use(safeHtmlPlugin);
  const tree = await processor.run(processor.parse(markdown));
  const elements = [];
  visit(tree, 'element', (node) => {
    elements.push(node);
  });
  return elements;
};

for (const [original, alias, title] of [
  ['streaming-using-the-vercel-ai-sdk-protocol', 'stream-protocols', 'Stream Protocols'],
  ['chat-requests', 'frontend-integration', 'Frontend Integration'],
]) {
  test(`renders both consecutive anchors for ${title}`, async () => {
    const elements = await renderElements(
      `<a name="${original}"></a>\n` +
        `<a name="${alias}"></a>\n` +
        `<!-- #### ${title} -->\n#### ${title}`,
    );
    for (const id of [original, alias]) {
      assert.equal(elements.filter((node) => node.properties.id === id).length, 1);
    }
    assert.equal(elements.find((node) => node.tagName === 'h4').properties.id, original);
  });
}

test('preserves multiple aliases while keeping single-anchor headings unchanged', async () => {
  const elements = await renderElements(
    '<a name="original"></a>\n' +
      '<a name="alias-one"></a>\n' +
      "<a name='alias-two'></a>\n\n## 제목\n\n" +
      '<a name="next-section"></a>\n\n## 次の節',
  );
  assert.deepEqual(
    elements.filter((node) => node.properties.id).map((node) => node.properties.id),
    ['alias-one', 'alias-two', 'original', 'next-section'],
  );
});

for (const mappedFirst of [true, false]) {
  test(`keeps the mapped anchor when its heading appears ${mappedFirst ? 'first' : 'last'}`, async () => {
    const mapped = '<a name="stopping-on-first-validation-failure"></a>\n\n' +
      '#### Stopping on First Validation Failure';
    const automatic = '#### Stopping on First Validation Failure';
    const elements = await renderElements(
      (mappedFirst ? [mapped, automatic] : [automatic, mapped]).join('\n\n'),
    );
    const ids = elements.filter((node) => node.tagName === 'h4').map((node) => node.properties.id);
    assert.deepEqual(ids, mappedFirst
      ? ['stopping-on-first-validation-failure', 'stopping-on-first-validation-failure-1']
      : ['stopping-on-first-validation-failure-1', 'stopping-on-first-validation-failure']);
  });
}

test('reserves aliases and HTML IDs before assigning automatic heading IDs', async () => {
  const elements = await renderElements(
    '## Alias\n\n## Existing\n\n' +
      '<a name="original"></a>\n<a name="alias"></a>\n\n## 제목\n\n' +
      '<div id="existing"></div>',
  );
  const ids = elements.filter((node) => node.properties.id).map((node) => node.properties.id);
  assert.equal(new Set(ids).size, ids.length);
  assert.deepEqual(
    elements.filter((node) => node.tagName === 'h2').map((node) => node.properties.id),
    ['alias-1', 'existing-1', 'original'],
  );
});

test('preserves authored IDs and skips reserved suffixes', async () => {
  const elements = await renderElements(
    '## Reserved\n\n## Reserved\n\n' +
      '## Custom {#reserved}\n\n## Other <!-- #reserved-1 -->\n\n' +
      '<a name="upgrade-13.0"></a>\n\n## Upgrade\n\n' +
      '<span id="reserved-2"></span>',
  );
  const headings = elements.filter((node) => node.tagName === 'h2');
  assert.deepEqual(headings.map((node) => node.properties.id), [
    'reserved-3', 'reserved-4', 'reserved', 'reserved-1', 'upgrade-13.0',
  ]);
  assert.equal(headings[2].children[0].value, 'Custom');
  assert.equal(headings[3].children[0].value, 'Other');
});

test('keeps existing duplicate declarations while avoiding them for automatic headings', async () => {
  const elements = await renderElements(
    '<a name="section"></a>\n\n## First\n\n' +
      '<a name="section"></a>\n\n## Second\n\n## Section',
  );
  assert.deepEqual(
    elements.filter((node) => node.tagName === 'h2').map((node) => node.properties.id),
    ['section', 'section', 'section-1'],
  );
});

test('keeps native slugs for formatted and localized headings', async () => {
  const elements = await renderElements(
    '## [Client](https://example.com) `fake()`\n\n' +
      '## **문서** 제목\n\n## 문서 제목\n\n' +
      '## 見出し 例\n\n## 見出し 例',
  );
  assert.deepEqual(
    elements.filter((node) => node.tagName === 'h2').map((node) => node.properties.id),
    ['client-fake', '문서-제목', '문서-제목-1', '見出し-例', '見出し-例-1'],
  );
});

test('reserves standalone names and decoded HTML IDs but ignores commented examples', async () => {
  const elements = await renderElements(
    '## Existing\n\n## A & B\n\n## Example\n\n' +
      '<a name="existing"></a>\n\n' +
      '<div id="&#97;--b"></div>\n\n<!-- <div id="example"></div> -->',
  );
  assert.deepEqual(
    elements.filter((node) => node.tagName === 'h2').map((node) => node.properties.id),
    ['existing-1', 'a--b-1', 'example'],
  );
});

test('keeps the native H1 slug sequence without reserving its hidden DOM ID', async () => {
  const elements = await renderElements(
    '# Reserved\n\n## Reserved\n\n' +
      '# Custom {#other}\n\n## Other\n\n<div id="reserved-1"></div>',
  );
  assert.deepEqual(
    elements.filter((node) => node.tagName === 'h2').map((node) => node.properties.id),
    ['reserved-2', 'other'],
  );
});
