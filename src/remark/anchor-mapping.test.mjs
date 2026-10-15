import assert from 'node:assert/strict';
import test from 'node:test';

import headings from '@docusaurus/mdx-loader/lib/remark/headings/index.js';
import contentTitle from '@docusaurus/mdx-loader/lib/remark/contentTitle/index.js';
import toc from '@docusaurus/mdx-loader/lib/remark/toc/index.js';
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

for (const {name, markdown, ids} of [
  {
    name: 'keeps Docusaurus automatic heading numbering',
    markdown: '## Same\n\n## Same',
    ids: ['same', 'same-1'],
  },
  {
    name: 'separates a mapped heading from a later automatic heading',
    markdown: '<a name="same"></a>\n\n## Same\n\n## Same',
    ids: ['same', 'same-1'],
  },
  {
    name: 'reserves later explicit suffixes when mapped anchors repeat',
    markdown: '<a name="same"></a>\n\n## First\n\n' +
      '<a name="same"></a>\n\n## Second\n\n' +
      '<a name="same-1"></a>\n\n## Third',
    ids: ['same', 'same-2', 'same-1'],
  },
  {
    name: 'reserves later mapped anchors before assigning automatic IDs',
    markdown: '## Same\n\n<a name="same"></a>\n\n## Later',
    ids: ['same-1', 'same'],
  },
  {
    name: 'preserves a later alias instead of assigning its ID to an earlier heading',
    markdown: '## Legacy\n\n<a name="current"></a>\n<a name="legacy"></a>\n\n## Current',
    ids: ['legacy-1', 'legacy', 'current'],
  },
  {
    name: 'keeps the first target when an alias repeats its heading anchor',
    markdown: '<a name="same"></a>\n<a name="same"></a>\n\n## Title',
    ids: ['same-1', 'same'],
  },
  {
    name: 'separates raw HTML IDs while protecting a later explicit suffix',
    markdown: '<div id="software-list" markdown="1"></div>\n\n' +
      '<div id="software-list" markdown="1"></div>\n\n' +
      '<a id="software-list-1"></a>\n\n## Software List',
    ids: ['software-list', 'software-list-2', 'software-list-1', 'software-list-3'],
  },
  {
    name: 'keeps a mapped heading before a colliding raw HTML target',
    markdown: '<a name="same"></a>\n\n## Title\n\n<div id="same"></div>',
    ids: ['same', 'same-1'],
  },
  {
    name: 'keeps raw HTML before a colliding mapped heading',
    markdown: '<div id="same"></div>\n\n<a name="same"></a>\n\n## Title',
    ids: ['same', 'same-1'],
  },
  {
    name: 'ignores source annotation comments when reserving raw IDs',
    markdown: '<!-- <div id="same"></div> -->\n\n## Same',
    ids: ['same'],
  },
  {
    name: 'preserves punctuation in mapped IDs',
    markdown: '<a name="upgrade-8.0"></a>\n\n## Upgrade\n\n' +
      '<a name="upgrade-8.0"></a>\n\n## Another Upgrade',
    ids: ['upgrade-8.0', 'upgrade-8.0-1'],
  },
  {
    name: 'separates a mapped ID from a classic custom heading ID',
    markdown: '<a name="same"></a>\n\n## First\n\n## Second {#same}',
    ids: ['same', 'same-1'],
  },
  {
    name: 'separates a comment custom heading ID from a later mapped ID',
    markdown: '## First <!-- #same -->\n\n<a name="same"></a>\n\n## Second',
    ids: ['same', 'same-1'],
  },
]) {
  test(name, async () => {
    const elements = await renderElements(markdown);
    const renderedIds = elements.filter((node) => node.properties.id).map((node) => node.properties.id);
    assert.deepEqual(renderedIds, ids);
    assert.equal(new Set(renderedIds).size, renderedIds.length);
  });
}

test('keeps the document title unchanged before Docusaurus collects it', async () => {
  const processor = unified().use(remarkParse).use(anchorMappingPlugin).use(contentTitle.default);
  const file = {data: {}};
  await processor.run(processor.parse('# Document Title\n\n## Section'), file);
  assert.equal(file.data.contentTitle, 'Document Title');
});

test('keeps automatic heading numbering when the title matches an explicit ID', async () => {
  const elements = await renderElements('# Same\n\n<a name="same"></a>\n\n## Explicit\n\n## Same');
  assert.deepEqual(
    elements.filter((node) => node.tagName === 'h2').map((node) => node.properties.id),
    ['same', 'same-1'],
  );
});

test('uses the same distinct IDs for rendered headings and table of contents', async () => {
  const markdown = '<a name="stopping-on-first-validation-failure"></a>\n\n' +
    '#### Stopping on First Validation Failure\n\n' +
    '#### Stopping on First Validation Failure';
  const processor = unified()
    .use(remarkParse)
    .use(anchorMappingPlugin)
    .use(headings.default, {anchorsMaintainCase: false})
    .use(toc.default);
  const tree = await processor.run(processor.parse(markdown));
  const exportNode = tree.children.find((node) => node.type === 'mdxjsEsm');
  const tocItems = exportNode.data.estree.body[0].declaration.declarations[0].init.elements;
  const tocIds = tocItems.map((item) => item.properties.find((property) => property.key.value === 'id').value.value);
  const elements = await renderElements(markdown);
  const headingIds = elements.filter((node) => node.tagName === 'h4').map((node) => node.properties.id);

  assert.deepEqual(tocIds, ['stopping-on-first-validation-failure', 'stopping-on-first-validation-failure-1']);
  assert.deepEqual(headingIds, tocIds);
});
