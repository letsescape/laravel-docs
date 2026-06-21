import assert from 'node:assert/strict';

import {extractMarkdownLinks} from './markdown-link-utils.mjs';

assert.deepEqual(
  extractMarkdownLinks('<!-- [Hidden](/docs/13.x/mcp#client) -->\n[Visible](#ok)'),
  [{text: 'Visible', url: '#ok'}],
);

console.log('markdown-link-utils tests passed');
