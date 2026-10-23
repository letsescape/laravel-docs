import {test, expect} from '@playwright/test';
import {existsSync, readdirSync, readFileSync} from 'node:fs';
import {join, relative, resolve, sep} from 'node:path';
import {parseDocumentFrontMatter} from '../src/utils/document-front-matter.mjs';
import {load} from 'cheerio';
import versions from '../versions.json';
import {announcement} from '../src/theme/AnnouncementBar/config';
import {DISMISSAL_STORAGE_KEY} from '../src/theme/AnnouncementBar/constants';

const siteDir = resolve(__dirname, '..');
const buildDir = join(siteDir, 'build');
const origin = 'https://laravel.chanhyung.kim';
const locales = [
  {locale: 'ko', prefix: '', label: '한국어 문서'},
  {locale: 'ja', prefix: '/ja', label: '日本語ドキュメント'},
];
const normalizedText = (text: string) => text.replace(/\s+/g, ' ').trim();
const documents = new Map<string, Map<string, string | undefined>>();
const pages = new Set(locales.flatMap(({prefix}) => [`${prefix}/`, `${prefix}/q/`]));

test.beforeAll(async () => {
  expect(versions.length).toBeGreaterThan(0);
  expect(new Set(versions).size).toBe(versions.length);
  for (const {locale, prefix} of locales) {
    for (const version of versions) {
      const sourceDir = join(siteDir, locale === 'ko'
        ? 'versioned_docs' : 'i18n/ja/docusaurus-plugin-content-docs', `version-${version}`);
      const root = `${prefix}/docs/${version}/`;
      const routes = new Map<string, string | undefined>([[root, undefined]]);
      for (const entry of readdirSync(sourceDir, {withFileTypes: true})) {
        if (!entry.isFile() || !entry.name.endsWith('.md') || entry.name.startsWith('_') ||
          ['documentation.md', 'readme.md'].includes(entry.name)) continue;
        const filePath = join(sourceDir, entry.name);
        const {frontMatter} = await parseDocumentFrontMatter({filePath, fileContent: readFileSync(filePath, 'utf8')});
        const rawSlug = Object.hasOwn(frontMatter, 'slug') ? frontMatter.slug : entry.name.slice(0, -3);
        expect(typeof rawSlug, filePath).toBe('string');
        const slug = String(rawSlug).replace(/^\//, '');
        if (rawSlug !== '/') expect(slug, filePath).toMatch(/^[a-z0-9]+(?:-[a-z0-9]+)*(?:\/[a-z0-9]+(?:-[a-z0-9]+)*)*$/);
        const route = `${root}${slug ? `${slug}/` : ''}`;
        if (slug) expect(routes.has(route), `duplicate source route: ${route}`).toBe(false);
        routes.set(route, frontMatter.title == null ? undefined : String(frontMatter.title));
      }
      documents.set(`${locale}/${version}`, routes);
      for (const route of routes.keys()) pages.add(route);
    }
  }
});

test('build contains its homepage and static assets', () => {
  expect(existsSync(join(buildDir, 'index.html'))).toBe(true);
  expect(existsSync(join(buildDir, 'img')) || existsSync(join(buildDir, 'assets'))).toBe(true);
});

for (const {locale, prefix, label} of locales) {
  test(`${locale} build respects notice visibility`, () => {
    for (const route of [`${prefix}/`, `${prefix}/docs/${versions[0]}/`]) {
      const html = readFileSync(join(buildDir, route, 'index.html'), 'utf8');
      const $ = load(html);
      const notice = $(`aside[aria-label="${announcement.locales[locale].label}"]`);
      expect(notice).toHaveLength(announcement.enabled ? 1 : 0);
      if (!announcement.enabled) expect(html).not.toContain(DISMISSAL_STORAGE_KEY);
    }
  });

  for (const version of ['', ...versions]) {
    test(`${locale}/${version || 'home and query'} build metadata and alternate links`, async () => {
      const sourceRoutes = documents.get(`${locale}/${version}`);
      const routes = version ? [...sourceRoutes!.keys()] : [`${prefix}/`, `${prefix}/q/`];
      if (version) {
        const directory = join(buildDir, prefix, 'docs', version);
        const actual = readdirSync(directory, {recursive: true, withFileTypes: true})
          .filter((entry) => entry.isFile() && entry.name === 'index.html')
          .map((entry) => `/${relative(buildDir, join(entry.parentPath, entry.name)).split(sep).join('/').replace(/index\.html$/, '')}`);
        expect(actual.length).toBeGreaterThan(0);
        expect(actual.sort()).toEqual([...routes].sort());
      } else {
        expect(existsSync(join(buildDir, prefix, 'search/index.html'))).toBe(false);
      }
      for (const route of routes) {
        await test.step(route, async () => {
          const $ = load(readFileSync(join(buildDir, route, 'index.html'), 'utf8'));
          const value = (selector: string, attribute: string | null = 'content') => {
            const nodes = $(selector);
            expect(nodes, selector).toHaveLength(1);
            const text = normalizedText((attribute ? nodes.attr(attribute) : nodes.text()) ?? '');
            expect(text, selector).not.toBe('');
            return text;
          };
          expect(value('html', 'lang')).toBe(locale);
          const title = value('head title', null);
          const ogTitle = value('head meta[property="og:title"]');
          expect(title === ogTitle || (!version && title === `${ogTitle} | Laravel`)).toBe(true);
          expect(new URL(value('head link[rel="canonical"]', 'href')).href).toBe(`${origin}${route}`);
          expect(value('head meta[property="og:site_name"]')).toBe(`Laravel ${label}`);
          const query = route === `${prefix}/q/`;
          if (!query) {
            const description = value('head meta[name="description"]');
            expect(description).not.toMatch(/^(?:[-*+]\s|\d+[.)]\s)/);
            expect(value('head meta[property="og:description"]')).toBe(description);
          }
          if (version) {
            const heading = $('h1').clone();
            heading.find('.hash-link').remove();
            expect(heading).toHaveLength(1);
            const name = normalizedText(heading.text());
            expect(name).not.toBe('');
            expect(title).toBe(normalizedText(`${sourceRoutes!.get(route) ?? name} — Laravel ${version} ${label}`));
          }
          const robots = $('head meta[name="robots"]').toArray()
            .flatMap((node) => ($(node).attr('content') ?? '').toLowerCase().split(/[\s,]+/));
          if (query) expect(robots).toContain('noindex');
          expect(robots.filter((token) => (query ? ['index', 'all'] : ['noindex', 'none']).includes(token))).toEqual([]);
          const websites = $('head script[type="application/ld+json"]').toArray()
            .map((node) => JSON.parse($(node).text())).filter((data) => data['@type'] === 'WebSite');
          expect(websites).toHaveLength(1);
          expect(websites[0]).toMatchObject({name: 'Laravel Docs', url: `${origin}/`});
          expect($('head link[rel="alternate"][hreflang]')).toHaveLength(3);
          for (const alternate of [...locales, {locale: 'x-default', prefix: ''}]) {
            const target = `${alternate.prefix}${route.slice(prefix.length)}`;
            expect(value(`head link[rel="alternate"][hreflang="${alternate.locale}"]`, 'href')).toBe(`${origin}${target}`);
            expect(pages.has(target), `missing alternate source: ${target}`).toBe(true);
            expect(existsSync(join(buildDir, target, 'index.html')), target).toBe(true);
          }
        });
      }
    });
  }

  test(`${locale} sitemap contains exactly its homepage and source documents`, () => {
    const $ = load(readFileSync(join(buildDir, prefix, 'sitemap.xml'), 'utf8'), {xmlMode: true});
    expect($.root().children()).toHaveLength(1);
    expect($('urlset').attr('xmlns')).toBe('http://www.sitemaps.org/schemas/sitemap/0.9');
    const actual = $('urlset > url').toArray().map((node) => {
      const loc = $(node).children('loc');
      expect(loc).toHaveLength(1);
      expect(loc.text().trim()).not.toBe('');
      return loc.text().trim();
    });
    const expected = [...pages].filter((route) => route === `${prefix}/` || route.startsWith(`${prefix}/docs/`));
    expect(new Set(actual).size).toBe(actual.length);
    expect(actual.sort()).toEqual(expected.map((route) => `${origin}${route}`).sort());
  });
}

test('robots.txt declares both locale sitemaps exactly once', () => {
  const robots = readFileSync(join(buildDir, 'robots.txt'), 'utf8');
  const actual = [...robots.matchAll(/^\s*Sitemap:\s*(\S+)\s*$/gim)].map((match) => match[1]);
  expect(new Set(actual).size).toBe(actual.length);
  expect(actual.sort()).toEqual(locales.map(({prefix}) => `${origin}${prefix}/sitemap.xml`).sort());
});
