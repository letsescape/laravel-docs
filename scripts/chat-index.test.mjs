import assert from 'node:assert/strict';
import {existsSync, mkdirSync, readFileSync, writeFileSync} from 'node:fs';
import {mkdtemp, rm} from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import test from 'node:test';
import {readPublicationRevision, runChatIndex} from './chat-index.mjs';

const revision = 'a'.repeat(40);

async function fixture(t) {
  const siteDir = await mkdtemp(path.join(os.tmpdir(), 'docs-chat-index-'));
  t.after(() => rm(siteDir, {recursive: true, force: true}));
  writeFileSync(path.join(siteDir, 'versions.json'), JSON.stringify(['master', '13.x', '12.x']));
  return siteDir;
}

function publications(directory, sha = revision) {
  for (const locale of ['ko', 'ja']) {
    const filename = path.join(directory, locale === 'ko' ? '' : locale, 'laravel-chat-manifest.json');
    mkdirSync(path.dirname(filename), {recursive: true});
    writeFileSync(filename, JSON.stringify({schema_version: 1, locale, docs_repo_sha: sha, pages: [{}]}));
  }
}

test('build pins one sanitized Git revision and prepares only the requested new directory', async (t) => {
  const siteDir = await fixture(t);
  const existing = path.join(siteDir, 'build', 'keep.txt');
  mkdirSync(path.dirname(existing));
  writeFileSync(existing, 'existing build');
  const output = path.join(siteDir, 'tmp', 'publication');
  const calls = [];
  const redirects = [];
  const env = {PATH: '/bin', GIT_DIR: '/wrong', GIT_CONFIG_COUNT: '1'};
  const result = await runChatIndex(['build', '--output', 'tmp/publication'], {siteDir, env,
    run(command, args, options) {
      calls.push({command, args, options});
      if (command === 'git') return `${revision}\n`;
      publications(output);
    }, redirects: (options) => redirects.push(options)});
  assert.equal(result, output);
  assert.equal(calls.length, 2);
  assert.deepEqual(calls[0].options.env, {PATH: '/bin'});
  assert.deepEqual(calls[0].args, ['--no-replace-objects', '-C', siteDir, 'rev-parse', 'HEAD^{commit}']);
  assert.deepEqual(calls[1].args.slice(-3), ['build', '--out-dir', output]);
  assert.equal(calls[1].options.env.LARAVEL_CHAT_PUBLICATION_REVISION, revision);
  assert.equal(calls[1].options.env.LARAVEL_CHAT_REPO, path.resolve(siteDir, '../laravel-chat'));
  assert.deepEqual(redirects, [{docsRoot: path.join(siteDir, 'versioned_docs/version-13.x'),
    buildRoot: output, latestVersion: '13.x', locales: ['', 'ja']}]);
  assert.equal(readFileSync(existing, 'utf8'), 'existing build');
});

test('build failure and an existing output never proceed to publication completion', async (t) => {
  const siteDir = await fixture(t);
  const output = path.join(siteDir, 'publication');
  let calls = 0;
  await assert.rejects(runChatIndex(['build', '--output', output], {siteDir,
    run: (command) => {calls += 1; if (command === 'git') return revision; throw new Error('build failed');},
    redirects: () => assert.fail('redirects must wait for a successful build'),
  }), /build failed/);
  assert.equal(calls, 2);
  mkdirSync(output);
  await assert.rejects(runChatIndex(['build', '--output', output], {siteDir,
    run: () => assert.fail('an existing output must be preserved'),
  }), /새 출력 경로/);
});

test('publication completion rejects missing, empty or inconsistent locale metadata', async (t) => {
  const siteDir = await fixture(t);
  assert.throws(() => readPublicationRevision(siteDir), /ENOENT/);
  publications(siteDir);
  assert.equal(readPublicationRevision(siteDir), revision);
  const filename = path.join(siteDir, 'ja/laravel-chat-manifest.json');
  const valid = JSON.parse(readFileSync(filename, 'utf8'));
  for (const change of [{pages: []}, {locale: 'en'}, {docs_repo_sha: `${revision}\n`},
    {docs_repo_sha: 'b'.repeat(40)}]) {
    writeFileSync(filename, JSON.stringify({...valid, ...change}));
    assert.throws(() => readPublicationRevision(siteDir), /게시 정보/);
  }
});

test('sqlite uses the publication revision and forwards optional reviewed curation without narrowing languages', async (t) => {
  const siteDir = await fixture(t);
  publications(path.join(siteDir, 'published'));
  const calls = [];
  await runChatIndex(['sqlite', '--published-dir', 'published', '--output', 'releases',
    '--curation', 'reviewed.json', '--chat-dir', '../custom chat'], {siteDir,
    run: (...args) => calls.push(args)});
  assert.equal(calls.length, 1);
  assert.equal(calls[0][0], 'uv');
  assert.deepEqual(calls[0][1], ['run', '--locked', 'python', '-m', 'demo.index',
    '--repo', siteDir, '--revision', revision, '--published-dir', path.join(siteDir, 'published'),
    '--output', path.join(siteDir, 'releases'), '--curation', path.join(siteDir, 'reviewed.json')]);
  assert.equal(calls[0][2].cwd, path.resolve(siteDir, '../custom chat'));
});

test('browser exports first and invokes the shared model builder only after success', async (t) => {
  const siteDir = await fixture(t);
  const calls = [];
  const args = ['browser', '--manifest', 'release/manifest.json', '--output', 'browser'];
  await runChatIndex(args, {siteDir, run: (...call) => calls.push(call)});
  assert.equal(calls.length, 2);
  assert.deepEqual(calls[0][1].slice(3), ['-m', 'demo.retrieval_index', 'export-browser',
    '--manifest', path.join(siteDir, 'release/manifest.json'), '--output', path.join(siteDir, 'browser.jsonl')]);
  assert.deepEqual(calls[1][1], [path.resolve(siteDir, '../laravel-chat/demo/index-browser.mjs'),
    '--input', path.join(siteDir, 'browser.jsonl'), '--output', path.join(siteDir, 'browser')]);
  let failures = 0;
  await assert.rejects(runChatIndex(args, {siteDir,
    run: () => {failures += 1; throw new Error('export failed');},
  }), /export failed/);
  assert.equal(failures, 1);
  writeFileSync(path.join(siteDir, 'browser.jsonl'), 'previous export');
  await assert.rejects(runChatIndex(args, {siteDir,
    run: () => assert.fail('existing export must be preserved'),
  }), /새 출력 경로/);
});

test('browser forwards an explicit device and rejects unsupported devices before export', async (t) => {
  const siteDir = await fixture(t);
  for (const device of ['cpu', 'webgpu']) {
    const calls = [];
    await runChatIndex(['browser', '--manifest', 'release/manifest.json', '--output', 'browser',
      '--device', device], {siteDir, run: (...call) => calls.push(call)});
    assert.deepEqual(calls[1][1].slice(-2), ['--device', device]);
    assert.equal(calls[0][1].includes('--device'), false);
  }
  await assert.rejects(runChatIndex(['browser', '--manifest', 'release/manifest.json', '--output', 'browser',
    '--device', 'cuda'], {siteDir, run: () => assert.fail('invalid device must not export')}), /cpu 또는 webgpu/);
});

test('OpenAI upload is an explicit command and retains resume and expiry settings', async (t) => {
  const siteDir = await fixture(t);
  const calls = [];
  await runChatIndex(['openai', '--manifest', 'release/manifest.json', '--output', 'openai',
    '--resume', '--expires-days', '7'], {siteDir, run: (...call) => calls.push(call)});
  assert.equal(calls.length, 1);
  assert.deepEqual(calls[0][1].slice(3), ['-m', 'demo.retrieval_index', 'openai',
    '--manifest', path.join(siteDir, 'release/manifest.json'), '--output', path.join(siteDir, 'openai'),
    '--resume', '--expires-days', '7']);
  assert.equal(existsSync(path.join(siteDir, 'openai')), false);
});

test('incomplete or mixed command options fail before any external process', async (t) => {
  const siteDir = await fixture(t);
  for (const args of [[], ['upload', '--output', 'new'], ['browser', '--output', 'new'],
    ['sqlite', '--output', 'new'], ['build', '--output', 'new', '--resume'],
    ['sqlite', '--output', 'new', '--manifest', 'wrong']]) {
    await assert.rejects(runChatIndex(args, {siteDir,
      run: () => assert.fail('invalid arguments must not run any process'),
    }));
  }
});
