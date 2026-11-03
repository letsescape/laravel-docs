import assert from 'node:assert/strict';
import {existsSync, mkdirSync, readFileSync, symlinkSync, writeFileSync} from 'node:fs';
import {mkdtemp, rm} from 'node:fs/promises';
import {tmpdir} from 'node:os';
import {join} from 'node:path';
import test from 'node:test';
import {runInNewContext} from 'node:vm';
import {load} from 'cheerio';

import latestDocRedirects, {redirectHtml} from './latest-doc-redirects.mjs';

const fixture = async (t) => {
  const root = await mkdtemp(join(tmpdir(), 'latest-doc-redirects-'));
  t.after(() => rm(root, {recursive: true, force: true}));
  return root;
};

const build = (outDir, routesPaths, baseUrl = '/') =>
  latestDocRedirects({}, {latestVersion: '13.x'}).postBuild({
    outDir, routesPaths, siteConfig: {baseUrl},
  });

test('postBuild uses emitted routes and the locale output directory', async (t) => {
  const root = await fixture(t);
  for (const [baseUrl, locale] of [['/project/', 'ko'], ['/project/ja/', 'ja']]) {
    const outDir = join(root, locale);
    build(outDir, [
      baseUrl,
      `${baseUrl}docs/13.x/`,
      `${baseUrl}docs/13.x/custom/nested/`,
      `${baseUrl}docs/12.x/old-only/`,
      `${baseUrl}docs/master/future-only/`,
      `${baseUrl}q/`,
    ], baseUrl);

    for (const slug of ['', 'custom/nested/']) {
      const html = readFileSync(join(outDir, 'docs', slug, 'index.html'), 'utf8');
      const $ = load(html);
      assert.equal($('link[rel=canonical]').attr('href'), `${baseUrl}docs/13.x/${slug}`);
      let location;
      runInNewContext($('script').text(), {window: {location: {
        search: '?source=nav', hash: '#example', replace: (url) => { location = url; },
      }}});
      assert.equal(location, `${baseUrl}docs/13.x/${slug}?source=nav#example`);
    }
    for (const absent of ['project', 'ja', 'docs/old-only', 'docs/future-only', 'docs/installation']) {
      assert.equal(existsSync(join(outDir, absent)), false);
    }
  }
});

test('postBuild does not invent a root redirect when no root route was emitted', async (t) => {
  const outDir = await fixture(t);
  build(outDir, ['/docs/13.x/cache/']);
  assert.equal(existsSync(join(outDir, 'docs/index.html')), false);
  assert.equal(existsSync(join(outDir, 'docs/cache/index.html')), true);
});

test('postBuild validates every route before writing', async (t) => {
  const root = await fixture(t);
  for (const slug of [
    '../q', 'a/../../q', 'a//b', '/', 'a\\b', '%2e%2e', '%252e%252e',
    'a?b', 'a#b', 'x</script><script>alert(1)</script>', 'fullwidth．dot',
  ]) {
    const outDir = join(root, 'build');
    assert.throws(() => build(outDir, ['/docs/13.x/cache/', `/docs/13.x/${slug}/`]), /unsafe redirect slug/);
    assert.equal(existsSync(outDir), false);
  }
});

test('postBuild rejects collisions with emitted routes and duplicate aliases', async (t) => {
  const outDir = await fixture(t);
  for (const routes of [
    ['/docs/13.x/cache/', '/docs/cache/'],
    ['/docs/13.x/cache/', '/docs/cache'],
    ['/docs/13.x/cache/', '/docs/13.x/cache/'],
  ]) {
    assert.throws(() => build(outDir, ['/docs/13.x/', ...routes]), /conflicts with an existing route/);
    assert.equal(existsSync(join(outDir, 'docs')), false);
  }
});

test('postBuild preserves existing output files', async (t) => {
  const outDir = await fixture(t);
  mkdirSync(join(outDir, 'docs/cache'), {recursive: true});
  writeFileSync(join(outDir, 'docs/cache/index.html'), 'existing page');
  assert.throws(() => build(outDir, ['/docs/13.x/', '/docs/13.x/cache/']), /already exists/);
  assert.equal(existsSync(join(outDir, 'docs/index.html')), false);
  assert.equal(readFileSync(join(outDir, 'docs/cache/index.html'), 'utf8'), 'existing page');
});

test('postBuild rejects symlinks in the output path', async (t) => {
  const root = await fixture(t);
  const outside = join(root, 'outside');
  mkdirSync(outside);
  for (const relative of ['', 'docs', 'docs/cache']) {
    const outDir = join(root, `build-${relative.length}`);
    const link = join(outDir, relative);
    mkdirSync(join(link, '..'), {recursive: true});
    symlinkSync(outside, link);
    assert.throws(() => build(outDir, ['/docs/13.x/cache/']), /physical directory/);
    assert.equal(existsSync(join(outside, 'index.html')), false);
    assert.equal(existsSync(join(outside, 'docs')), false);
  }
});

test('plugin rejects unsafe version segments', () => {
  for (const latestVersion of ['', '../13.x', '/13.x', '13.x?query', null]) {
    assert.throws(() => latestDocRedirects({}, {latestVersion}), /unsafe documentation version/);
  }
});

test('redirectHtml encodes HTML attributes and script data separately', () => {
  for (const target of [
    '/docs/13.x/x</script><script>alert(1)</script>&"',
    '/docs/13.x/x</ScRiPt ><ScRiPt data-test="x">alert(1)</ScRiPt>&"',
  ]) {
    const $ = load(redirectHtml(target));
    assert.equal($('script').length, 1);
    assert.equal($('a').attr('href'), target);
    let location;
    runInNewContext($('script').text(), {window: {location: {
      search: '', hash: '', replace: (url) => { location = url; },
    }}});
    assert.equal(location, target);
  }
});
