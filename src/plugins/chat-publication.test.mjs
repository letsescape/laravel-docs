import assert from 'node:assert/strict';
import {mkdtemp, mkdir, rm, writeFile} from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import test from 'node:test';
import chatPublication from './chat-publication.mjs';

const revision = 'a'.repeat(40);

async function fixture(t, chatName = 'laravel-chat') {
  const temporary = await mkdtemp(path.join(os.tmpdir(), 'docs-chat-publication-'));
  const previous = Object.fromEntries(['LARAVEL_CHAT_REPO', 'LARAVEL_CHAT_PUBLICATION_REVISION']
    .map((key) => [key, process.env[key]]));
  t.after(async () => {
    for (const [key, value] of Object.entries(previous)) {
      if (value === undefined) delete process.env[key];
      else process.env[key] = value;
    }
    await rm(temporary, {recursive: true, force: true});
  });
  delete process.env.LARAVEL_CHAT_REPO;
  process.env.LARAVEL_CHAT_PUBLICATION_REVISION = revision;
  const context = {siteDir: path.join(temporary, 'laravel-docs')};
  const repoDir = path.join(temporary, chatName);
  await mkdir(context.siteDir);
  await mkdir(path.join(repoDir, 'demo'), {recursive: true});
  await writeFile(path.join(repoDir, 'demo/publication-plugin.mjs'), `
export default function publicationPlugin(context, options) {
  return {
    name: 'fixture-publication',
    allContentLoaded(content) { return {context, options, content}; },
    postBuild(build) { return {context, options, build}; },
  };
}
`);
  return {context, repoDir, temporary};
}

test('loads the sibling plugin and preserves its publication lifecycle', async (t) => {
  const {context} = await fixture(t);
  const plugin = await chatPublication(context);
  const options = {sourceDir: context.siteDir, revision};
  const content = {allContent: {}};
  const build = {outDir: path.join(context.siteDir, 'build'), baseUrl: '/'};
  assert.equal(plugin.name, 'fixture-publication');
  assert.deepEqual(plugin.allContentLoaded(content), {context, options, content});
  assert.deepEqual(plugin.postBuild(build), {context, options, build});
});

test('uses an explicit repository path and forwards the exact pinned revision', async (t) => {
  const {context, repoDir} = await fixture(t, 'shared chat #fixture');
  process.env.LARAVEL_CHAT_REPO = repoDir;
  process.env.LARAVEL_CHAT_PUBLICATION_REVISION = 'b'.repeat(40);
  const plugin = await chatPublication(context);
  assert.deepEqual(plugin.postBuild({}).options, {
    sourceDir: context.siteDir,
    revision: 'b'.repeat(40),
  });
});

test('rejects missing or noncanonical revisions before importing the plugin', async (t) => {
  const {context, temporary} = await fixture(t);
  process.env.LARAVEL_CHAT_REPO = path.join(temporary, 'unavailable');
  for (const value of [undefined, '', 'HEAD', 'a'.repeat(39), 'a'.repeat(41), 'A'.repeat(40), `${revision}\n`]) {
    if (value === undefined) delete process.env.LARAVEL_CHAT_PUBLICATION_REVISION;
    else process.env.LARAVEL_CHAT_PUBLICATION_REVISION = value;
    await assert.rejects(chatPublication(context), /LARAVEL_CHAT_PUBLICATION_REVISION/);
  }
});

test('fails when the configured publication plugin cannot be imported', async (t) => {
  const {context, temporary} = await fixture(t);
  process.env.LARAVEL_CHAT_REPO = path.join(temporary, 'unavailable');
  await assert.rejects(chatPublication(context), {code: 'ERR_MODULE_NOT_FOUND'});
});
