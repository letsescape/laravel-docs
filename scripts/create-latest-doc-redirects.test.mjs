import assert from 'node:assert/strict';
import {
  existsSync,
  mkdirSync,
  readFileSync,
  symlinkSync,
  writeFileSync,
} from 'node:fs';
import {tmpdir} from 'node:os';
import {join} from 'node:path';
import {mkdtemp, rm} from 'node:fs/promises';
import test from 'node:test';

import {
  canonicalSlug,
  frontMatterSlug,
  generateLatestDocRedirects,
  planRedirects,
  redirectHtml,
} from './create-latest-doc-redirects.mjs';

test('canonicalSlug accepts the supported route grammar', () => {
  assert.equal(canonicalSlug('/', 'fixture.md'), '');
  assert.equal(canonicalSlug('cache', 'fixture.md'), 'cache');
  assert.equal(canonicalSlug('/cache', 'fixture.md'), 'cache');
  assert.equal(canonicalSlug('foo-bar/v2', 'fixture.md'), 'foo-bar/v2');
});

test('canonicalSlug rejects path and markup differentials', () => {
  for (const slug of [
    '',
    '.',
    '..',
    '../q',
    'a/../../q',
    'a//b',
    '//cache',
    'cache/',
    'a\\b',
    'C:\\tmp',
    '%2e%2e',
    '%252e%252e',
    'a?b',
    'a#b',
    'x</script><script>alert(1)</script>',
    'fullwidth．dot',
  ]) {
    assert.throws(() => canonicalSlug(slug, 'fixture.md'), /unsafe slug/);
  }
});

test('frontMatterSlug uses the same YAML semantics as Docusaurus', async () => {
  assert.equal(await frontMatterSlug('# Title\n', 'fixture.md'), null);
  assert.equal(
    await frontMatterSlug('---\ntitle: Cache\n---\n', 'fixture.md'),
    null,
  );
  assert.equal(await frontMatterSlug('---\nslug: /\n---\n', 'fixture.md'), '');
  assert.equal(
    await frontMatterSlug("---\nslug: '/custom'\n---\n", 'fixture.md'),
    'custom',
  );
  assert.equal(
    await frontMatterSlug('---\r\nslug: /windows\r\n---\r\n', 'fixture.md'),
    'windows',
  );
  assert.equal(
    await frontMatterSlug(
      '---\ndefaults: &defaults\n  slug: /merged\n<<: *defaults\n---\n',
      'fixture.md',
    ),
    'merged',
  );
  assert.equal(
    await frontMatterSlug('---\nslug: !!str /tagged\n---\n', 'fixture.md'),
    'tagged',
  );
  assert.equal(
    await frontMatterSlug('---\n"slug": /quoted-key\n---\n', 'fixture.md'),
    'quoted-key',
  );
  assert.equal(
    await frontMatterSlug(
      '---\nslug: safe # an inert YAML comment\n---\n',
      'fixture.md',
    ),
    'safe',
  );

  for (const content of [
    '---\nslug: cache\nslug: queues\n---\n',
    '---\nslug: |\n  cache\n---\n',
    '---\nslug: *route\n---\n',
  ]) {
    await assert.rejects(
      () => frontMatterSlug(content, 'fixture.md'),
      /slug|duplicated mapping key|unidentified alias/,
    );
  }
});

test('redirectHtml encodes HTML attributes and script data separately', () => {
  const target = '/docs/13.x/x</script><script>alert(1)</script>&"';
  const html = redirectHtml(target);

  assert.ok(html.includes('x&lt;/script&gt;&lt;script&gt;alert(1)&lt;/script&gt;&amp;&quot;'));
  assert.ok(html.includes('x\\u003c/script\\u003e\\u003cscript\\u003ealert(1)'));
  assert.equal((html.match(/<script>/g) ?? []).length, 1);
  assert.equal((html.match(/<\/script>/g) ?? []).length, 1);
});

test('planRedirects excludes Docusaurus-private documents', async (t) => {
  const root = await mkdtemp(join(tmpdir(), 'redirect-plan-'));
  t.after(() => rm(root, {recursive: true, force: true}));
  const docsRoot = join(root, 'docs');
  const buildRoot = join(root, 'build');
  mkdirSync(docsRoot);
  writeFileSync(join(docsRoot, 'cache.md'), '# Cache\n');
  writeFileSync(join(docsRoot, 'installation.md'), '---\nslug: /\n---\n');
  writeFileSync(
    join(docsRoot, '_private.md'),
    '---\nslug: ../q</script><script>alert(1)</script>\n---\n',
  );

  const plan = await planRedirects({
    docsRoot,
    buildRoot,
    latestVersion: '13.x',
    locales: ['', 'ja'],
  });

  assert.equal(plan.length, 4);
  assert.deepEqual(
    plan.map(({target}) => target).sort(),
    [
      '/docs/13.x/',
      '/docs/13.x/cache/',
      '/ja/docs/13.x/',
      '/ja/docs/13.x/cache/',
    ],
  );
});

test('generation validates the complete plan before its first write', async (t) => {
  const root = await mkdtemp(join(tmpdir(), 'redirect-generate-'));
  t.after(() => rm(root, {recursive: true, force: true}));
  const docsRoot = join(root, 'docs');
  const buildRoot = join(root, 'build');
  mkdirSync(docsRoot);
  writeFileSync(join(docsRoot, 'cache.md'), '# Cache\n');
  writeFileSync(join(docsRoot, 'z-bad.md'), '---\nslug: ../q\n---\n');

  await assert.rejects(
    () =>
      generateLatestDocRedirects({
        docsRoot,
        buildRoot,
        latestVersion: '13.x',
        locales: [''],
      }),
    /unsafe slug/,
  );
  assert.equal(existsSync(buildRoot), false);
});

test('generation writes only contained locale redirects', async (t) => {
  const root = await mkdtemp(join(tmpdir(), 'redirect-write-'));
  t.after(() => rm(root, {recursive: true, force: true}));
  const docsRoot = join(root, 'docs');
  const buildRoot = join(root, 'build');
  mkdirSync(docsRoot);
  writeFileSync(join(docsRoot, 'cache.md'), '# Cache\n');

  const count = await generateLatestDocRedirects({
    docsRoot,
    buildRoot,
    latestVersion: '13.x',
    locales: ['', 'ja'],
  });

  assert.equal(count, 4);
  for (const relative of [
    'docs/index.html',
    'docs/cache/index.html',
    'ja/docs/index.html',
    'ja/docs/cache/index.html',
  ]) {
    const html = readFileSync(join(buildRoot, relative), 'utf8');
    assert.match(html, /window\.location\.replace/);
  }
});

test('generation rejects a symlinked build root before writing', async (t) => {
  const root = await mkdtemp(join(tmpdir(), 'redirect-symlink-'));
  t.after(() => rm(root, {recursive: true, force: true}));
  const docsRoot = join(root, 'docs');
  const outsideRoot = join(root, 'outside');
  const buildRoot = join(root, 'build');
  mkdirSync(docsRoot);
  mkdirSync(outsideRoot);
  writeFileSync(join(docsRoot, 'cache.md'), '# Cache\n');
  symlinkSync(outsideRoot, buildRoot);

  await assert.rejects(
    () =>
      generateLatestDocRedirects({
        docsRoot,
        buildRoot,
        latestVersion: '13.x',
        locales: [''],
      }),
    /physical directory/,
  );
  assert.equal(existsSync(join(outsideRoot, 'docs', 'index.html')), false);
});
