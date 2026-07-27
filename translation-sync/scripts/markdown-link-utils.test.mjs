import assert from 'node:assert/strict';
import {join} from 'node:path';

import {extractMarkdownLinks} from './markdown-link-utils.mjs';
import {
  docsVersionFromUrl,
  relativeTargetPath,
  sourceUrl,
} from './anchor-routes.mjs';

assert.deepEqual(
  extractMarkdownLinks('<!-- [Hidden](/docs/13.x/mcp#client) -->\n[Visible](#ok)'),
  [{text: 'Visible', url: '#ok'}],
);

assert.deepEqual(
  extractMarkdownLinks('<!-- outer <!-- [Hidden](#bad) --> -->\n[Visible](#ok)'),
  [{text: 'Visible', url: '#ok'}],
);

const repo = '/repo';
assert.equal(
  sourceUrl(
    join(repo, 'versioned_docs', 'version-13.x', 'cache.md'),
    join(repo, 'versioned_docs'),
  ),
  '/docs/13.x/cache/',
);
assert.equal(
  sourceUrl(
    join(repo, 'i18n', 'ja', 'docs', 'version-13.x', 'installation.md'),
    join(repo, 'i18n', 'ja', 'docs'),
    '/ja',
  ),
  '/ja/docs/13.x/',
);
assert.equal(docsVersionFromUrl('/ja/docs/13.x/cache/'), '13.x');
assert.equal(
  relativeTargetPath('routing', '/ja/docs/13.x/cache/', '13.x'),
  '/ja/docs/13.x/routing',
);
assert.equal(
  relativeTargetPath('/docs/13.x/routing', '/ja/docs/13.x/cache/', '13.x'),
  '/ja/docs/13.x/routing',
);
assert.equal(
  relativeTargetPath('/ja/docs/13.x/routing', '/ja/docs/13.x/cache/', '13.x'),
  '/ja/docs/13.x/routing',
);

console.log('markdown-link-utils tests passed');
