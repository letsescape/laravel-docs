import assert from 'node:assert/strict';
import test from 'node:test';

import rehypeRaw from 'rehype-raw';
import remarkParse from 'remark-parse';
import remarkRehype from 'remark-rehype';
import {unified} from 'unified';

import safeHtmlPlugin from './safe-html.mjs';

const parse = async (markdown) => {
  const processor = unified()
    .use(remarkParse)
    .use(remarkRehype, {allowDangerousHtml: true})
    .use(rehypeRaw)
    .use(safeHtmlPlugin);
  const tree = processor.parse(markdown);
  return processor.run(tree, {path: 'fixture.md', value: markdown});
};

test('allows the repository raw HTML subset and ordinary Markdown output', async () => {
  await parse(
    '# Heading\n\n' +
      '<a name="legacy"></a>\n\n' +
      '<a id="alias" data-translation-alias="old" href="mailto:test@example.com">Mail</a>\n\n' +
      '<div class="content" markdown="1"><strong>Safe</strong></div>\n\n' +
      '<blockquote data-admonition-type="note"><p>Safe note</p></blockquote>\n\n' +
      '<pre><code class="language-php" metastring="tab=Example">echo 1;</code></pre>\n\n' +
      '<img src="https://laravel.com/example.png" alt="Example" width="320">\n\n' +
      '<table><tbody><tr><td align="center">Cell</td></tr></tbody></table>',
  );
});

test('rejects active and embedding elements after HTML parsing', async () => {
  for (const markdown of [
    '<script src="https://example.com/payload.js"></script>',
    '<iframe srcdoc="<script>alert(1)</script>"></iframe>',
    '<style>body{display:none}</style>',
    '<object data="https://example.com/payload"></object>',
    '<svg><script>alert(1)</script></svg>',
    '<meta http-equiv="refresh" content="0;url=https://example.com">',
  ]) {
    await assert.rejects(() => parse(markdown), /unsafe raw HTML/, markdown);
  }
});

test('rejects event, style, document injection, and unsafe URL attributes', async () => {
  for (const markdown of [
    '<img src="https://example.com/a.png" onerror="alert(1)">',
    '<div style="background:url(https://example.com)">x</div>',
    '<a href="javascript:alert(1)">x</a>',
    '<a href="JaVaScRiPt:alert(1)">x</a>',
    '<a href="java&#x0a;script:alert(1)">x</a>',
    '<img src="data:image/svg+xml,<svg></svg>">',
    '<input type="text" disabled>',
    '<input type="checkbox">',
  ]) {
    await assert.rejects(() => parse(markdown), /unsafe raw HTML/, markdown);
  }
});

test('allows generated disabled checkboxes and raster data images', async () => {
  await parse('<input type="checkbox" disabled checked>');
  await parse('![pixel](data:image/png;base64,iVBORw0KGgo=)');
});
