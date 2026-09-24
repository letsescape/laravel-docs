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
