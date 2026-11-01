import {test, expect} from '@playwright/test';
import versions from '../versions.json';

const host = 'https://laravel.chanhyung.kim';
const stable = versions.find((version) => version !== 'master')!;

for (const {locale, prefix, siteName, language} of [
  {locale: 'ko', prefix: '', siteName: 'Laravel 한국어 문서', language: '한국어 문서'},
  {locale: 'ja', prefix: '/ja', siteName: 'Laravel 日本語ドキュメント', language: '日本語ドキュメント'},
]) {
  test(`${locale} home uses localized site metadata`, async ({page}) => {
    await page.goto(`${prefix}/`);
    await expect(page.locator('html')).toHaveAttribute('lang', locale);
    await expect(page.locator('meta[property="og:site_name"]')).toHaveAttribute('content', siteName);
    await expect(page.locator('meta[property="og:image"]')).toHaveAttribute('content', `${host}/img/laravel-home.png`);
    await expect(page.locator('link[rel="canonical"]')).toHaveAttribute('href', new RegExp(`^${host}${prefix}/?$`));
    const structured = await page.locator('script[type="application/ld+json"]').evaluateAll((nodes) =>
      nodes.map((node) => JSON.parse(node.textContent ?? '{}')));
    expect(structured.find((data) => data['@type'] === 'WebSite')).toMatchObject({name: 'Laravel Docs', url: `${host}/`});
    const docsLink = page.locator('.hero-buttons a').first();
    await expect(docsLink).toHaveAttribute('href', new RegExp(`^${prefix}/docs/${stable.replace('.', '\\.')}/?$`));
  });

  for (const version of [...new Set([stable, versions.at(-1)!, 'master'])]) {
    test(`${locale} ${version} document metadata survives client navigation`, async ({page}) => {
      await page.goto(`${prefix}/docs/${version}/routing/`);
      const title = `Routing — Laravel ${version} ${language}`;
      await expect(page).toHaveTitle(title);
      await expect(page.locator('h1')).toHaveCount(1);
      await expect(page.locator('h1')).toHaveText('Routing');
      await expect(page.locator('meta[property="og:title"]')).toHaveAttribute('content', 'Routing');
      const description = await page.locator('meta[name="description"]').getAttribute('content');
      expect(description).toMatch(locale === 'ko' ? /[가-힣]/ : /[ぁ-んァ-ン一-龠]/);
      expect(description).not.toMatch(/^[-*]|Introduction/);
      await expect(page.locator('meta[property="og:description"]')).toHaveAttribute('content', description!);
      await expect(page.locator('meta[property="og:site_name"]')).toHaveAttribute('content', siteName);
      await expect(page.locator('link[rel="canonical"]')).toHaveAttribute('href', `${host}${prefix}/docs/${version}/routing/`);
      await expect(page.locator('html')).toHaveAttribute('data-has-hydrated', 'true');
      await page.evaluate(() => Reflect.set(window, '__seoNavigationMarker', true));
      await page.locator(`.theme-doc-markdown a[href^="${prefix}/docs/${version}/eloquent"][href$="#soft-deleting"]`).first().click();
      const destinationTitle = `Eloquent: Getting Started — Laravel ${version} ${language}`;
      await expect(page).toHaveTitle(destinationTitle);
      expect(await page.evaluate(() => Reflect.get(window, '__seoNavigationMarker'))).toBe(true);
      await expect(page.locator('h1')).toHaveCount(1);
      await expect(page.locator('h1')).toHaveText('Eloquent: Getting Started');
      await expect(page.locator('meta[property="og:title"]')).toHaveAttribute('content', 'Eloquent: Getting Started');
      await expect(page.locator('link[rel="canonical"]')).toHaveAttribute('href', `${host}${prefix}/docs/${version}/eloquent/`);
      await expect(page.locator('meta[name="description"]')).not.toHaveAttribute('content', description!);
      const destinationDescription = await page.locator('meta[name="description"]').getAttribute('content');
      expect(destinationDescription).toContain('Eloquent');
      expect(destinationDescription).toMatch(locale === 'ko' ? /[가-힣]/ : /[ぁ-んァ-ン一-龠]/);
      await expect(page.locator('meta[property="og:description"]')).toHaveAttribute('content', destinationDescription!);
      await expect(page.locator('meta[property="og:site_name"]')).toHaveAttribute('content', siteName);
    });
  }

  test(`${locale} query page is noindex while search documentation remains indexable`, async ({page}) => {
    await page.goto(`${prefix}/q/?q=routing`);
    await expect(page.locator('meta[name="robots"]')).toHaveAttribute('content', 'noindex, follow');
    await page.goto(`${prefix}/docs/${stable}/search/`);
    await expect(page.locator('meta[name="robots"][content*="noindex"]')).toHaveCount(0);
    await expect(page.locator('h1')).toHaveCount(1);
  });
}
