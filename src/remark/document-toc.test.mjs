import assert from 'node:assert/strict';
import test from 'node:test';
import remarkParse from 'remark-parse';
import remarkRehype from 'remark-rehype';
import {unified} from 'unified';
import {visit} from 'unist-util-visit';
import safeHtmlPlugin from '../rehype/safe-html.mjs';
import documentTocPlugin from './document-toc.ts';

async function render(markdown, path = '/repo/versioned_docs/version-13.x/example.md') {
  const processor = unified().use(remarkParse).use(documentTocPlugin)
    .use(remarkRehype).use(safeHtmlPlugin);
  return processor.run(processor.parse(markdown), {path});
}

for (const [path, label] of [
  ['/repo/versioned_docs/version-13.x/example.md', '목차'],
  ['i18n/ja/docusaurus-plugin-content-docs/version-13.x/example.md', '目次'],
]) {
  test(`marks the leading nested fragment list as ${label}`, async () => {
    const tree = await render('<!-- # Original -->\n# Title\n\n- [Introduction](#introduction)\n  - [`Code`](#code)\n\n## Introduction\n\nBody.', path);
    const nav = tree.children.find(node => node.tagName === 'nav');
    assert.equal(nav.properties.role, 'navigation');
    assert.equal(nav.properties['aria-label'], label);
    assert.equal(nav.children.filter(node => node.type === 'element')[0].tagName, 'ul');
    const links = [];
    visit(nav, {type: 'element', tagName: 'a'}, node => { links.push(node.properties.href); });
    assert.deepEqual(links, ['#introduction', '#code']);
    assert.ok(tree.children.some(node => node.tagName === 'h2'));
  });
}

for (const markdown of [
  '# Title\n\n- Install dependencies\n- [Continue](#continue)',
  '# Title\n\n- [External](https://laravel.com)\n- [Internal](#internal)',
  '# Title\n\n- [Introduction](#introduction)\n  - Read the example',
  '# Title\n\nBody paragraph.\n\n- [Introduction](#introduction)',
  '## Section\n\n- [Introduction](#introduction)',
  '# Title\n\nNo contents list.',
]) {
  test(`does not mark a body list as navigation: ${markdown}`, async () => {
    const tree = await render(markdown);
    assert.equal(tree.children.some(node => node.tagName === 'nav'), false);
  });
}
