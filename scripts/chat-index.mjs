import {execFileSync} from 'node:child_process';
import {lstatSync, mkdirSync, readFileSync} from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {parseArgs} from 'node:util';
import {generateLatestDocRedirects} from './create-latest-doc-redirects.mjs';

const repoRoot = fileURLToPath(new URL('..', import.meta.url));
const publicationFiles = {ko: 'laravel-chat-manifest.json', ja: 'ja/laravel-chat-manifest.json'};
const commandOptions = {
  build: [],
  sqlite: ['published-dir', 'curation'],
  browser: ['manifest', 'device'],
  openai: ['manifest', 'resume', 'expires-days'],
};

function requireNewPath(filename) {
  try {
    lstatSync(filename);
  } catch (error) {
    if (error.code === 'ENOENT') return;
    throw error;
  }
  throw new Error(`새 출력 경로를 지정하세요: ${filename}`);
}

export function readPublicationRevision(directory) {
  const manifests = Object.entries(publicationFiles).map(([locale, filename]) => {
    const manifest = JSON.parse(readFileSync(path.join(directory, filename), 'utf8'));
    if (manifest.schema_version !== 1 || manifest.locale !== locale
      || typeof manifest.docs_repo_sha !== 'string' || manifest.docs_repo_sha.length !== 40
      || !/^[a-f0-9]{40}$/.test(manifest.docs_repo_sha ?? '')
      || !Array.isArray(manifest.pages) || !manifest.pages.length) {
      throw new Error('한국어·일본어 게시 정보를 확인하세요.');
    }
    return manifest;
  });
  if (manifests[0].docs_repo_sha !== manifests[1].docs_repo_sha) {
    throw new Error('게시 정보의 문서 revision이 일치하지 않습니다.');
  }
  return manifests[0].docs_repo_sha;
}

export async function runChatIndex(args, {
  siteDir = repoRoot, env = process.env, run = execFileSync, redirects = generateLatestDocRedirects,
} = {}) {
  const {values, positionals} = parseArgs({args, allowPositionals: true, options: {
    'chat-dir': {type: 'string'}, output: {type: 'string'}, 'published-dir': {type: 'string'},
    curation: {type: 'string'}, manifest: {type: 'string'}, 'expires-days': {type: 'string'},
    resume: {type: 'boolean'}, device: {type: 'string'},
  }});
  const command = positionals[0];
  if (positionals.length !== 1 || !Object.hasOwn(commandOptions, command) || !values.output) {
    throw new Error('build, sqlite, browser, openai 중 하나와 --output을 지정하세요.');
  }
  for (const key of Object.keys(values)) {
    if (!['chat-dir', 'output', ...commandOptions[command]].includes(key)) {
      throw new Error(`${command} 명령은 --${key} 옵션을 사용하지 않습니다.`);
    }
  }
  const chatDir = path.resolve(siteDir, values['chat-dir'] ?? env.LARAVEL_CHAT_REPO ?? '../laravel-chat');
  const output = path.resolve(siteDir, values.output);
  const python = (...args) => run('uv', ['run', '--locked', 'python', ...args],
    {cwd: chatDir, env, stdio: 'inherit'});

  if (command === 'build') {
    requireNewPath(output);
    const gitEnv = Object.fromEntries(Object.entries(env).filter(([key]) => !key.startsWith('GIT_')));
    const revision = run('git', ['--no-replace-objects', '-C', siteDir, 'rev-parse', 'HEAD^{commit}'],
      {env: gitEnv, encoding: 'utf8'}).trim();
    if (!/^[a-f0-9]{40}$/.test(revision)) throw new Error('문서 Git revision을 확인하세요.');
    run(process.execPath, [path.join(siteDir, 'node_modules/@docusaurus/core/bin/docusaurus.mjs'),
      'build', '--out-dir', output], {cwd: siteDir, stdio: 'inherit',
      env: {...env, LARAVEL_CHAT_REPO: chatDir, LARAVEL_CHAT_PUBLICATION_REVISION: revision}});
    const versions = JSON.parse(readFileSync(path.join(siteDir, 'versions.json'), 'utf8'));
    const latestVersion = versions.find((version) => version !== 'master') ?? versions[0];
    await redirects({docsRoot: path.join(siteDir, 'versioned_docs', `version-${latestVersion}`),
      buildRoot: output, latestVersion, locales: ['', 'ja']});
    if (readPublicationRevision(output) !== revision) {
      throw new Error('게시 빌드가 시작 시 고정한 문서 revision과 다릅니다.');
    }
    return output;
  }

  if (command === 'sqlite') {
    if (!values['published-dir']) throw new Error('--published-dir을 지정하세요.');
    const publishedDir = path.resolve(siteDir, values['published-dir']);
    const revision = readPublicationRevision(publishedDir);
    python('-m', 'demo.index', '--repo', siteDir, '--revision', revision,
      '--published-dir', publishedDir, '--output', output,
      ...(values.curation ? ['--curation', path.resolve(siteDir, values.curation)] : []));
    return;
  }

  if (!values.manifest) throw new Error('--manifest를 지정하세요.');
  const manifest = path.resolve(siteDir, values.manifest);
  if (command === 'browser') {
    if (values.device !== undefined && !['cpu', 'webgpu'].includes(values.device)) {
      throw new Error('--device에는 cpu 또는 webgpu를 지정하세요.');
    }
    requireNewPath(output);
    const input = `${output}.jsonl`;
    requireNewPath(input);
    mkdirSync(path.dirname(output), {recursive: true});
    python('-m', 'demo.retrieval_index', 'export-browser', '--manifest', manifest, '--output', input);
    run(process.execPath, [path.join(chatDir, 'demo/index-browser.mjs'), '--input', input, '--output', output,
      ...(values.device ? ['--device', values.device] : [])],
      {cwd: chatDir, env, stdio: 'inherit'});
  } else {
    python('-m', 'demo.retrieval_index', 'openai', '--manifest', manifest, '--output', output,
      ...(values.resume ? ['--resume'] : []),
      ...(values['expires-days'] ? ['--expires-days', values['expires-days']] : []));
  }
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  const output = await runChatIndex(process.argv.slice(2));
  if (output) console.log(output);
}
