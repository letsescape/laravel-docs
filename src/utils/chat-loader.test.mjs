import assert from 'node:assert/strict';
import test from 'node:test';
import {createChatLoader} from './chat-loader.mjs';

const container = {path: '/docs/13.x/container/', version: '13.x', docKey: 'container', language: 'ko'};
const routing = {...container, path: '/docs/13.x/routing/', docKey: 'routing'};

function fixture(options = {}) {
  const calls = [];
  const sdk = {
    initChat: (options) => {
      calls.push(['init', options]);
      return Object.fromEntries(['updatePage', 'setVisible', 'resetContext', 'destroy'].map((method) =>
        [method, (...args) => calls.push([method, ...args])],
      ));
    },
  };
  const loader = createChatLoader({
    sdkUrl: 'https://sdk.example.test/index.js',
    endpoint: 'https://api.example.test/v1/chat',
    loadSDK: async () => sdk,
    ...options,
  });
  return {calls, sdk, loader};
}

test('initializes only on documents and keeps the API URL independent of the SDK URL', async () => {
  const {loader, calls} = fixture();
  await loader.update(null);
  assert.deepEqual(calls, []);
  await loader.update(container);
  await loader.update(container);
  assert.deepEqual(calls, [['init', {endpoint: 'https://api.example.test/v1/chat', page: container}]]);
});

test('enables browser AI only when a manifest URL is configured', async () => {
  const enabled = fixture({browserManifestUrl: '/__chat/__browser/manifest.json'});
  await enabled.loader.update(container);
  assert.deepEqual(enabled.calls, [['init', {
    endpoint: 'https://api.example.test/v1/chat',
    page: container,
    browserAI: {manifestURL: '/__chat/__browser/manifest.json'},
  }]]);
  const disabled = fixture({browserManifestUrl: ''});
  await disabled.loader.update(container);
  assert.deepEqual(disabled.calls, [['init', {endpoint: 'https://api.example.test/v1/chat', page: container}]]);
});

test('passes document, version and language changes to the same SDK instance', async () => {
  const {loader, calls} = fixture({browserManifestUrl: '/__chat/__browser/manifest.json'});
  await loader.update(container);
  const japanese = {path: '/ja/docs/12.x/', version: '12.x', docKey: 'installation', language: 'ja'};
  await loader.update(japanese);
  assert.deepEqual(calls.slice(1), [['updatePage', japanese], ['setVisible', true]]);
  assert.equal(calls.filter(([method]) => method === 'init').length, 1);
});

test('leaving documents hides and resets once, then restores the existing widget', async () => {
  const {loader, calls} = fixture();
  await loader.update(container);
  await loader.update(null);
  await loader.update(null);
  await loader.update(routing);
  assert.deepEqual(calls.slice(1), [
    ['setVisible', false], ['resetContext'], ['updatePage', routing], ['setVisible', true],
  ]);
});

test('slow SDK loading uses the latest page and creates only one instance', async () => {
  let resolve;
  const loaded = new Promise((done) => { resolve = done; });
  const {loader, calls, sdk} = fixture({loadSDK: () => loaded});
  const first = loader.update(container);
  const second = loader.update(routing);
  resolve(sdk);
  await Promise.all([first, second]);
  assert.deepEqual(calls, [['init', {endpoint: 'https://api.example.test/v1/chat', page: routing}]]);
});

test('leaving documents or unmounting during import cannot create a late widget', async () => {
  for (const destroy of [false, true]) {
    let resolve;
    const loaded = new Promise((done) => { resolve = done; });
    const {loader, calls, sdk} = fixture({loadSDK: () => loaded});
    const pending = loader.update(container);
    if (destroy) loader.destroy();
    else await loader.update(null);
    resolve(sdk);
    await pending;
    assert.deepEqual(calls, []);
    await loader.update(routing);
    assert.equal(calls.length, destroy ? 0 : 1);
  }
});

test('failed loading can be retried on navigation without touching the document', async () => {
  let attempts = 0;
  const fixtureValue = fixture({loadSDK: async () => {
    if (++attempts === 1) throw new Error('SDK unavailable');
    return fixtureValue.sdk;
  }});
  await assert.rejects(fixtureValue.loader.update(container), /SDK unavailable/);
  assert.deepEqual(fixtureValue.calls, []);
  await fixtureValue.loader.update(routing);
  assert.equal(fixtureValue.calls[0][1].page, routing);
});

test('destroy is idempotent and missing settings never load the SDK', async () => {
  const {loader, calls} = fixture();
  await loader.update(container);
  loader.destroy();
  loader.destroy();
  await loader.update(routing);
  assert.deepEqual(calls.slice(1), [['destroy']]);
  for (const options of [{sdkUrl: ''}, {endpoint: ''}, {endpoint: '', browserManifestUrl: '/__chat/__browser/manifest.json'}]) {
    const disabled = fixture({...options, loadSDK: () => assert.fail('SDK must not load')});
    await disabled.loader.update(container);
  }
});
