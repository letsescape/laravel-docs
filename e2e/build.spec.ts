import {test, expect} from '@playwright/test';
import {existsSync, readFileSync} from 'fs';
import {resolve} from 'path';

function sitemapLocations(path: string): Set<string> {
  const xml = readFileSync(path, 'utf8');
  return new Set(
    [...xml.matchAll(/<loc>([^<]+)<\/loc>/g)].map((match) => match[1]),
  );
}

test.describe('Build verification', () => {
  test('build output directory exists', () => {
    const buildDir = resolve(__dirname, '../build');
    expect(existsSync(buildDir)).toBe(true);
  });

  test('build output contains index.html', () => {
    const indexFile = resolve(__dirname, '../build/index.html');
    expect(existsSync(indexFile)).toBe(true);
  });

  test('build output contains static assets', () => {
    const imgDir = resolve(__dirname, '../build/img');
    const assetsDir = resolve(__dirname, '../build/assets');
    expect(existsSync(imgDir) || existsSync(assetsDir)).toBe(true);
  });

  test('build keeps query pages separate from search documentation', () => {
    const buildDir = resolve(__dirname, '../build');
    const sitemap = sitemapLocations(resolve(buildDir, 'sitemap.xml'));
    const jaSitemap = sitemapLocations(resolve(buildDir, 'ja/sitemap.xml'));

    for (const version of ['master', '13.x', '12.x']) {
      expect(
        sitemap.has(`https://laravel.chanhyung.kim/docs/${version}/search/`),
      ).toBe(true);
      expect(
        jaSitemap.has(`https://laravel.chanhyung.kim/ja/docs/${version}/search/`),
      ).toBe(true);
    }

    expect(sitemap.has('https://laravel.chanhyung.kim/q/')).toBe(false);
    expect(jaSitemap.has('https://laravel.chanhyung.kim/ja/q/')).toBe(false);
    expect(existsSync(resolve(buildDir, 'q/index.html'))).toBe(true);
    expect(existsSync(resolve(buildDir, 'ja/q/index.html'))).toBe(true);
    expect(existsSync(resolve(buildDir, 'search/index.html'))).toBe(false);
    expect(existsSync(resolve(buildDir, 'ja/search/index.html'))).toBe(false);
  });
});
