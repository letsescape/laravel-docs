import assert from 'node:assert/strict';
import test from 'node:test';

import {unified} from 'unified';
import remarkParse from 'remark-parse';
import remarkGfm from 'remark-gfm';
import remarkRehype from 'remark-rehype';
import rehypeRaw from 'rehype-raw';
import {visit} from 'unist-util-visit';

import replacePlaceholdersPlugin from './replace-placeholders.ts';
import {staleLinkResolution} from '../utils/stale-links.mjs';

assert.deepEqual(
  staleLinkResolution(
    '/docs/10.x/migrations#writing-migrations',
    '10.x',
  ),
  {
    target: '/docs/10.x/migrations#generating-migrations',
    retireMode: null,
  },
);
assert.deepEqual(staleLinkResolution('#assert-similar-json', '8.x'), {
  target: null,
  retireMode: 'bare-inline-code',
});
assert.equal(staleLinkResolution('#unknown', '10.x'), null);
assert.equal(
  staleLinkResolution('https://example.com/docs#writing-migrations', '10.x'),
  null,
);
assert.equal(
  staleLinkResolution('//example.com/docs/migrations#writing-migrations', '10.x'),
  null,
);
assert.equal(
  staleLinkResolution('mailto:migrations#writing-migrations', '10.x'),
  null,
);
assert.deepEqual(
  staleLinkResolution(
    'https://laravel.com/docs/10.x/migrations#writing-migrations',
    '10.x',
  ),
  {
    target: 'https://laravel.com/docs/10.x/migrations#generating-migrations',
    retireMode: null,
  },
);

const processor = unified().use(remarkParse).use(replacePlaceholdersPlugin);
test('contribution email renders one visible link and preserves ordinary links', async () => {
  const markdown = '<a href="mailto:security@laravel.com">security@laravel.com</a> ' +
    'taylor@laravel.com [문서](https://laravel.com/docs)';
  const renderer = unified().use(remarkParse).use(remarkGfm)
    .use(replacePlaceholdersPlugin).use(remarkRehype, {allowDangerousHtml: true}).use(rehypeRaw);
  const tree = await renderer.run(renderer.parse(markdown), {path: '/repo/versioned_docs/version-13.x/contributions.md'});
  const links = [];
  visit(tree, 'element', (node) => { if (node.tagName === 'a') links.push(node); });
  assert.deepEqual(links.map((node) => node.properties.href), [
    'mailto:security@laravel.com', 'mailto:taylor@laravel.com', 'https://laravel.com/docs',
  ]);
  assert.equal(links[0].children[0].value, 'security@laravel.com');
});

test('renderer replaces version, installation, and stale links while preserving code examples', async () => {
  const markdown = [
    'Version {{version}}',
    '[Installation](/docs/{{version}}/installation#installation)',
    '[Migrations](/docs/{{version}}/migrations#writing-migrations)',
    '[External](https://example.com/docs/migrations#writing-migrations)',
    '`{{version}}`',
    '```text\n{{version}}\n[Example](#writing-migrations)\n```',
  ].join('\n\n');
  for (const root of ['versioned_docs', 'i18n/ja/docusaurus-plugin-content-docs']) {
    const tree = await processor.run(processor.parse(markdown), {
      path: `/repo/${root}/version-10.x/migrations.md`,
    });
    const links = [];
    const code = [];
    visit(tree, 'link', (node) => links.push(node.url));
    visit(tree, (node) => {
      if (node.type === 'code' || node.type === 'inlineCode') code.push(node.value);
    });
    assert.equal(tree.children[0].children[0].value, 'Version 10.x');
    assert.deepEqual(links, [
      '/docs/10.x/#installation',
      '/docs/10.x/migrations#generating-migrations',
      'https://example.com/docs/migrations#writing-migrations',
    ]);
    assert.deepEqual(code, ['{{version}}', '{{version}}\n[Example](#writing-migrations)']);
  }
});

test('renderer retires a removed API link without losing its label', async () => {
  const tree = await processor.run(processor.parse('[`assertSimilarJson`](#assert-similar-json)'), {
    path: '/repo/versioned_docs/version-8.x/http-tests.md',
  });
  assert.deepEqual(tree.children[0].children, [{type: 'inlineCode', value: 'assertSimilarJson'}]);
});

test('renderer repairs the AI SDK schema link without changing the MCP schema link', async () => {
  const markdown = [
    '[JSON Schema](/docs/{{version}}/ai-sdk#tool-input-schemas)',
    '[Laravel MCP](/docs/{{version}}/mcp#tool-input-schemas)',
  ].join('\n\n');
  for (const root of ['versioned_docs', 'i18n/ja/docusaurus-plugin-content-docs']) {
    const tree = await processor.run(processor.parse(markdown), {
      path: `/repo/${root}/version-13.x/validation.md`,
    });
    const links = [];
    visit(tree, 'link', (node) => links.push(node.url));
    assert.deepEqual(links, [
      '/docs/13.x/ai-sdk#tools',
      '/docs/13.x/mcp#tool-input-schemas',
    ]);
  }
});

for (const version of ['13.x', 'master', '12.x']) {
  for (const label of ['Core Development Discussion', '코어 개발 논의', 'コア開発の議論']) {
    const link = `[${label}](#core-development-discussion)`;
    const markdown = [
      `- ${link}`,
      link,
      `- See ${link}`,
      `\`${link}\``,
      `<!-- ${link} -->`,
      `\`\`\`md\n- ${link}\n\`\`\`\n`,
      `<a name="core-development-discussion"></a>\n## ${label}`,
    ].join('\n\n');
    const original = processor.parse(markdown);
    const tree = await processor.run(processor.parse(markdown), {
      path: `/repo/versioned_docs/version-${version}/contributions.md`,
    });
    assert.deepEqual(tree, original);
  }
}
