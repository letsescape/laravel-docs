import assert from 'node:assert/strict';
import {spawnSync} from 'node:child_process';
import {cpSync, mkdirSync, symlinkSync, writeFileSync} from 'node:fs';
import {mkdtemp, rm} from 'node:fs/promises';
import {tmpdir} from 'node:os';
import {dirname, join} from 'node:path';
import {fileURLToPath} from 'node:url';
import test from 'node:test';

async function validateFixture(t, files) {
  const root = await mkdtemp(join(tmpdir(), 'validate-anchors-'));
  t.after(() => rm(root, {recursive: true, force: true}));
  cpSync(new URL('./', import.meta.url), join(root, 'scripts'), {recursive: true});
  mkdirSync(join(root, 'translation-sync'));
  cpSync(
    new URL('../translation-sync/stale-links.json', import.meta.url),
    join(root, 'translation-sync/stale-links.json'),
  );
  symlinkSync(
    fileURLToPath(new URL('../node_modules', import.meta.url)),
    join(root, 'node_modules'),
    'junction',
  );
  for (const [path, content] of Object.entries(files)) {
    const target = join(root, path);
    mkdirSync(dirname(target), {recursive: true});
    writeFileSync(target, content);
  }
  return spawnSync(process.execPath, [join(root, 'scripts/validate-anchors.mjs')], {
    encoding: 'utf8',
  });
}

test('rejects duplicate IDs in document bodies without inbound links', async (t) => {
  const result = await validateFixture(t, {
    'versioned_docs/version-13.x/fixture.md': '# Fixture\n',
    'build/docs/13.x/fixture/index.html':
      '<main class="theme-doc-markdown"><h2 id="a&amp;b">Heading</h2>' +
      "<div id='a&#38;b'>Duplicate</div></main>",
  });
  assert.equal(result.status, 1, result.stdout + result.stderr);
  assert.match(result.stdout, /duplicate ID.*docs\/13\.x\/fixture\/index\.html.*a&b.*2/);
});

test('preserves aliases and ignores duplicate IDs outside document bodies', async (t) => {
  const result = await validateFixture(t, {
    'versioned_docs/version-13.x/fixture.md':
      '[Original](#one) [Alias](#two) [Encoded](#a%26b)\n',
    'versioned_docs/version-13.x/other.md': '# Other\n',
    'build/docs/13.x/fixture/index.html':
      '<svg><path id="icon"></path><path id="icon"></path></svg>' +
      '<main class="theme-doc-markdown"><a name="one"></a><a id="two"></a>' +
      '<h2 id="one">Heading</h2><div id="a&amp;b"></div>' +
      '<!-- <div id="one"></div> -->' +
      '<script>const example = \'<div id="one"></div>\';</script></main>',
    'build/docs/13.x/other/index.html':
      '<main class="theme-doc-markdown"><h2 id="one">Other</h2></main>',
    'build/index.html': '<div id="outside"></div><div id="outside"></div>',
  });
  assert.equal(result.status, 0, result.stdout + result.stderr);
  assert.match(result.stdout, /OK \(id in HTML\):\s+3/);
});

test('continues rejecting missing anchors and target documents', async (t) => {
  const result = await validateFixture(t, {
    'versioned_docs/version-13.x/fixture.md':
      '[Missing ID](#missing) [Missing document](absent#target)\n',
    'build/docs/13.x/fixture/index.html':
      '<main class="theme-doc-markdown"><h2 id="present">Heading</h2></main>',
  });
  assert.equal(result.status, 1, result.stdout + result.stderr);
  assert.match(result.stdout, /Target HTML gone:\s+1/);
  assert.match(result.stdout, /id not found:\s+1/);
});
