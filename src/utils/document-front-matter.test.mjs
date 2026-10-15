import assert from 'node:assert/strict';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import test from 'node:test';

import {loadSiteConfig} from '@docusaurus/core/lib/server/config.js';
import {mdxLoader} from '@docusaurus/mdx-loader/lib/loader.js';
import {DEFAULT_PARSE_FRONT_MATTER} from '@docusaurus/utils';
import {visit} from 'unist-util-visit';

import {parseDocumentFrontMatter} from './document-front-matter.mjs';
import {frontMatterSlug} from '../../scripts/create-latest-doc-redirects.mjs';

const siteDir = fileURLToPath(new URL('../..', import.meta.url));
const filePath = path.join(siteDir, 'versioned_docs/version-13.x/security-fixture.md');
const {siteConfig} = await loadSiteConfig({siteDir});
const [, docsOptions] = siteConfig.plugins.find(
  (plugin) => Array.isArray(plugin) && plugin[0] === '@docusaurus/plugin-content-docs',
);
const parseHook = (fileContent, sourcePath = filePath, parser = DEFAULT_PARSE_FRONT_MATTER) =>
  siteConfig.markdown.parseFrontMatter({
    filePath: sourcePath,
    fileContent,
    defaultParseFrontMatter: parser,
  });
const entrypoints = [
  ['shared parser', (fileContent, filePath) => parseDocumentFrontMatter({filePath, fileContent})],
  ['site hook', parseHook],
  ['redirect parser', frontMatterSlug],
];
const loaderOptions = {
  ...docsOptions,
  siteDir,
  staticDirs: [path.join(siteDir, 'static')],
  markdownConfig: siteConfig.markdown,
};
const compileDocument = (fileContent, sourcePath = filePath, options = loaderOptions) =>
  new Promise((resolve, reject) => {
    mdxLoader.call({
      _compiler: {name: 'client'},
      resource: sourcePath,
      resourcePath: sourcePath,
      getOptions: () => options,
      async: () => (error, code) => error ? reject(error) : resolve(code),
    }, fileContent).catch(reject);
  });

test('shared parser and redirects preserve YAML, JSON, and documents without front matter', async () => {
  for (const [content, slug] of [
    ['# Title\n', null],
    ['----\nOrdinary Markdown\n', null],
    ['---\nslug: /\n---\n# Title\n', ''],
    ['\uFEFF---\r\nslug: /windows\r\n---\r\n# Title\r\n', 'windows'],
    ['--- YAML \ntitle: &title Laravel\ncopy: *title\ndefaults: &defaults\n  slug: /merged\n<<: *defaults\nlabel: !!str 123\n---\n', 'merged'],
    ['---yml\nslug: /yaml-alias\n---\n', 'yaml-alias'],
    ['---json\n{"slug":"/json","title":"JSON"}\n---\n# Title\n', 'json'],
    ['---\n{"slug":"/json-in-yaml"}\n---\n', 'json-in-yaml'],
  ]) {
    const actual = await parseDocumentFrontMatter({filePath, fileContent: content});
    assert.deepEqual(actual, await DEFAULT_PARSE_FRONT_MATTER({filePath, fileContent: content}));
    assert.equal(await frontMatterSlug(content, filePath), slug);
  }
});

for (const [name, parse] of entrypoints) {
  test(`${name} rejects JavaScript engines without evaluating their contents`, async (t) => {
    globalThis.__documentFrontMatterExecuted = false;
    t.after(() => delete globalThis.__documentFrontMatterExecuted);
    for (const bom of ['', '\uFEFF']) {
      for (const newline of ['\n', '\r\n']) {
        for (const language of ['js', 'javascript', ' JS ', '\tJaVaScRiPt\t']) {
          const content = `${bom}---${language}${newline}` +
            `(globalThis.__documentFrontMatterExecuted = true, {slug: '/safe'})${newline}` +
            `---${newline}# Title`;
          await assert.rejects(() => parse(content, filePath), /Unsupported front matter language/);
          assert.equal(globalThis.__documentFrontMatterExecuted, false);
        }
      }
    }
  });

  test(`${name} rejects document-controlled MDX formats and MDX files`, async () => {
    for (const content of [
      '---\nmdx:\n  format: mdx\n---\n{1 + 1}',
      '---\nmdx: {format: mdx}\n---\n{1 + 1}',
      '---\noptions: &options {format: mdx}\nmdx: *options\n---\n{1 + 1}',
      '---\noptions: &options {mdx: {format: mdx}}\n<<: *options\n---\n{1 + 1}',
      '---json\n{"mdx":{"format":"mdx"}}\n---\n{1 + 1}',
      '---\nmdx: {format: md}\n---\n# Title',
    ]) {
      await assert.rejects(() => parse(content, filePath), /Document-controlled MDX format/);
    }
    for (const extension of ['.mdx', '.MDX', '.MD', '.mD']) {
      await assert.rejects(
        () => parse('# Title\n', filePath.replace(/\.md$/, extension)),
        /Documents must use the \.md extension/,
      );
    }
  });
}

test('site hook rejects unsupported engines before delegating to the default parser', async () => {
  let parserCalls = 0;
  const parser = async () => {
    parserCalls += 1;
    return {frontMatter: {}, content: ''};
  };
  for (const language of ['javascript', 'js', 'toml', 'python']) {
    await assert.rejects(
      () => parseHook(`---${language}\n{}\n---\n`, filePath, parser),
      /Unsupported front matter language/,
    );
  }
  assert.equal(parserCalls, 0);
});

test('installed loader rejects execution-selecting documents before compilation', async () => {
  let compiled = false;
  const options = {
    ...loaderOptions,
    beforeDefaultRemarkPlugins: [() => () => { compiled = true; }],
  };
  for (const [content, sourcePath, error] of [
    ['---js\n({slug: "/safe"})\n---\n', filePath, /Unsupported front matter language/],
    ['---\nmdx: {format: mdx}\n---\n{1 + 1}', filePath, /Document-controlled MDX format/],
    ...['.mdx', '.MDX', '.MD'].map((extension) => [
      '{1 + 1}', filePath.replace(/\.md$/, extension), /Documents must use the \.md extension/,
    ]),
  ]) {
    await assert.rejects(() => compileDocument(content, sourcePath, options), error);
  }
  assert.equal(compiled, false);
});

test('installed loader preserves Markdown data and plugin-generated JSX', async () => {
  const sourceMdx = [];
  const generatedMdx = [];
  const capture = (nodes) => () => (tree) => {
    visit(tree, (node) => {
      if (node.type.startsWith('mdx')) nodes.push({type: node.type, name: node.name});
    });
  };
  const options = {
    ...loaderOptions,
    beforeDefaultRemarkPlugins: [capture(sourceMdx), ...docsOptions.beforeDefaultRemarkPlugins],
    remarkPlugins: [...docsOptions.remarkPlugins, capture(generatedMdx)],
  };
  const code = await compileDocument([
    '# Example',
    'Literal {1 + 1}',
    'export const documentValue = 42;',
    'import documentValue from "./untrusted.js";',
    '<span>{2 + 2}</span>',
    '[Website](https://example.com)',
    '[Download](@site/static/img/laravel-docs.png)',
    '![Logo](@site/static/img/laravel-docs.png)',
    '```blade\n{{ $name }}\n<x-alert />\n```',
    '```mdx\n{3 + 3}\nexport const example = 1;\n```',
  ].join('\n\n'), filePath, options);

  assert.deepEqual(sourceMdx, []);
  assert.ok(generatedMdx.some(({name}) => name === 'img'));
  assert.ok(generatedMdx.some(({name}) => name === 'a'));
  assert.ok(generatedMdx.some(({type}) => type === 'mdxjsEsm'));
  assert.match(code, /children: "Literal \{1 \+ 1\}"/);
  assert.match(code, /children: "export const documentValue = 42;"/);
  assert.match(code, /children: "import documentValue from \\"\.\/untrusted\.js\\";"/);
  assert.match(code, /children: "\{2 \+ 2\}"/);
  assert.match(code, /className: "language-markup"/);
  assert.match(code, /\{\{ \$name \}\}/);
  assert.match(code, /className: "language-mdx"/);
  assert.match(code, /href: "https:\/\/example\.com"/);
  assert.match(code, /src: require\(/);
  assert.match(code, /href: require\(/);
});


test('site hook applies the document boundary to source and every locale override', async () => {
  for (const root of [
    'versioned_docs',
    'i18n/ko/docusaurus-plugin-content-docs',
    'i18n/ja/docusaurus-plugin-content-docs',
  ]) {
    const sourcePath = path.join(siteDir, root, 'version-13.x/fixture.md');
    await assert.rejects(
      () => parseHook('---js\n({title: "Unsafe"})\n---\n', sourcePath),
      /Unsupported front matter language/,
    );
    await assert.rejects(
      () => parseHook('---\nmdx: {format: mdx}\n---\n', sourcePath),
      /Document-controlled MDX format/,
    );
    await assert.rejects(
      () => parseHook('# Title', sourcePath.replace(/\.md$/, '.mdx')),
      /Documents must use the \.md extension/,
    );
  }
});

test('site hook preserves SEO and local image validation', async () => {
  const result = await parseHook('# Title\n\nDescription.');
  assert.equal(result.frontMatter.title, 'Title');
  assert.equal(result.frontMatter.description, 'Description.');
  const explicit = await parseHook('---\ntitle: Custom\ndescription: Explicit\n---\n# Title\n\nDescription.');
  assert.equal(explicit.frontMatter.title, 'Custom');
  assert.equal(explicit.frontMatter.description, 'Explicit');
  await assert.rejects(
    () => parseHook('---\nimage: ./../../package.json\n---\n# Title'),
    /unsafe local Markdown asset/,
  );
});

test('site hook preserves parsing outside the document roots', async () => {
  const fileContent = '---\nmdx: {format: mdx}\n---\n# Trusted page\n\n{1 + 1}';
  for (const sourcePath of [
    path.join(siteDir, 'src/pages/fixture.mdx'),
    path.join(siteDir, 'versioned_docs-other/fixture.mdx'),
  ]) {
    assert.deepEqual(
      await parseHook(fileContent, sourcePath),
      await DEFAULT_PARSE_FRONT_MATTER({filePath: sourcePath, fileContent}),
    );
  }
});
