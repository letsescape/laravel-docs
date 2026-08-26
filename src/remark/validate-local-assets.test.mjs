import assert from 'node:assert/strict';
import {mkdir, mkdtemp, rm, symlink, writeFile} from 'node:fs/promises';
import {tmpdir} from 'node:os';
import path from 'node:path';
import test from 'node:test';

import {unified} from 'unified';
import remarkParse from 'remark-parse';

import validateLocalAssetsPlugin, {
  assertFrontMatterImageAllowed,
  assertPathAllowed,
  resolveMarkdownAssetCandidates,
} from './validate-local-assets.mjs';

const withFixture = async (t) => {
  const siteDir = await mkdtemp(path.join(tmpdir(), 'markdown-assets-'));
  t.after(() => rm(siteDir, {recursive: true, force: true}));
  const docsRoot = path.join(siteDir, 'versioned_docs', 'version-13.x');
  const staticDir = path.join(siteDir, 'static');
  const outsideDir = path.join(siteDir, '..', `${path.basename(siteDir)}-outside`);
  await mkdir(docsRoot, {recursive: true});
  await mkdir(staticDir, {recursive: true});
  await mkdir(outsideDir, {recursive: true});
  t.after(() => rm(outsideDir, {recursive: true, force: true}));
  const filePath = path.join(docsRoot, 'guide.md');
  await writeFile(filePath, '# Guide\n');
  await writeFile(path.join(docsRoot, 'guide.pdf'), 'pdf');
  await writeFile(path.join(staticDir, 'logo.png'), 'png');
  await writeFile(path.join(outsideDir, 'secret.json'), '{}');
  await writeFile(path.join(outsideDir, 'secret.MD'), '# secret\n');
  return {
    siteDir,
    docsRoot,
    staticDir,
    outsideDir,
    filePath,
    sourceRoots: [path.dirname(docsRoot)],
    allowedRoots: [path.dirname(docsRoot), staticDir],
  };
};

const candidatesFor = (fixture, kind, url) =>
  resolveMarkdownAssetCandidates({
    kind,
    url,
    filePath: fixture.filePath,
    siteDir: fixture.siteDir,
    staticDirs: [fixture.staticDir],
    allowedRoots: fixture.allowedRoots,
  });

const assertCandidates = async (fixture, kind, url) => {
  for (const {candidate, roots} of candidatesFor(fixture, kind, url)) {
    await assertPathAllowed({
      candidate,
      allowedRoots: roots,
      url,
      filePath: fixture.filePath,
    });
  }
};

test('allows remote, route, and contained asset references', async (t) => {
  const fixture = await withFixture(t);
  assert.deepEqual(candidatesFor(fixture, 'image', 'https://example.com/a.png'), []);
  assert.deepEqual(candidatesFor(fixture, 'link', '../routing'), []);
  await assertCandidates(fixture, 'link', './guide.pdf?download=1#page');
  await assertCandidates(fixture, 'image', '/logo.png');
  await assertCandidates(fixture, 'image', '@site/static/logo.png');
});

test('rejects lexical, encoded, Windows, and loader-delimiter escapes', async (t) => {
  const fixture = await withFixture(t);
  for (const url of [
    '@site/../secret.json',
    '@site/%2e%2e/secret.json',
    '@site/%2e%2e%2fsecret.json',
    '/../../secret.json',
    '../../../secret.json',
    '@site/%5c..%5csecret.json',
    '@site/static/logo.png!loader',
    '@site/static/logo%21.png',
    '@site/static/logo.png?loader%21payload',
  ]) {
    await assert.rejects(
      () => assertCandidates(fixture, url.endsWith('.json') ? 'link' : 'image', url),
      /unsafe local Markdown asset/,
      url,
    );
  }
  await assert.rejects(
    () => assertCandidates(fixture, 'link', '../../../secret.MD'),
    /unsafe local Markdown asset/,
  );
});

test('rejects an existing symlink that resolves outside approved roots', async (t) => {
  const fixture = await withFixture(t);
  const link = path.join(fixture.docsRoot, 'linked.json');
  await symlink(path.join(fixture.outsideDir, 'secret.json'), link);

  await assert.rejects(
    () => assertCandidates(fixture, 'link', './linked.json'),
    /unsafe local Markdown asset/,
  );
});

test('front matter image validation follows the same containment boundary', async (t) => {
  const fixture = await withFixture(t);
  await assertFrontMatterImageAllowed({
    filePath: fixture.filePath,
    image: './guide.pdf?raw=1',
    sourceRoots: fixture.sourceRoots,
    allowedRoots: fixture.allowedRoots,
  });
  for (const image of ['./../../../secret.json', './guide.pdf!loader']) {
    await assert.rejects(
      () =>
        assertFrontMatterImageAllowed({
          filePath: fixture.filePath,
          image,
          sourceRoots: fixture.sourceRoots,
          allowedRoots: fixture.allowedRoots,
        }),
      /unsafe local Markdown asset/,
    );
  }
});

test('remark integration catches CommonMark-normalized traversal', async (t) => {
  const fixture = await withFixture(t);
  const processor = unified().use(remarkParse).use(validateLocalAssetsPlugin, {
    siteDir: fixture.siteDir,
    staticDirs: [fixture.staticDir],
    allowedRoots: fixture.allowedRoots,
  });

  for (const markdown of [
    '[secret](@site/&#x2e;&#x2e;/secret.json)',
    '[secret](@site/\\..\\/secret.json)',
  ]) {
    const tree = processor.parse(markdown);
    await assert.rejects(
      () => processor.run(tree, {path: fixture.filePath, value: markdown}),
      /unsafe local Markdown asset/,
      markdown,
    );
  }
});
