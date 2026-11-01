import {expect, test} from '@playwright/test';
import {docsPath} from './utils/docs-version';

const readabilityPath = require.resolve('@mozilla/readability/Readability.js');

test('separates site navigation and version metadata from the document', async ({page}) => {
  await page.goto(docsPath('authorization'));
  await expect(page.locator('.navbar')).toHaveAttribute('role', 'navigation');
  await expect(page.locator('.theme-doc-version-badge')).toBeVisible();
  await expect(page.locator('article .theme-doc-version-badge')).toHaveCount(0);
  await expect(page.locator('article .theme-doc-breadcrumbs')).toHaveCount(0);
  await expect(page.locator('article h1')).toHaveText('Authorization');
});

for (const locale of ['ko', 'ja']) {
  for (const slug of ['authorization', 'collections', 'releases']) {
    test(`${locale} ${slug} excludes site navigation from reader extraction`, async ({page}) => {
      const prefix = locale === 'ko' ? '' : '/ja';
      await page.goto(`${prefix}${docsPath(slug)}`);
      await expect(page.locator('html')).toHaveAttribute('data-has-hydrated', 'true');
      const title = await page.locator('h1').innerText();
      const tables = await page.locator('.theme-doc-markdown table').evaluateAll(elements =>
        elements.map(table => Array.from(table.querySelectorAll('tr'), row =>
          Array.from(row.querySelectorAll('th, td'), cell => cell.textContent))));
      await page.addScriptTag({path: readabilityPath});
      const extracted = await page.evaluate(() => {
        const Reader = Reflect.get(window, 'Readability');
        const result = new Reader(document.cloneNode(true)).parse();
        const doc = new DOMParser().parseFromString(result.content, 'text/html');
        return {
          title: result.title,
          tables: Array.from(doc.querySelectorAll('table'), table => Array.from(table.querySelectorAll('tr'), row =>
            Array.from(row.querySelectorAll('th, td'), cell => cell.textContent))),
          navigation: doc.querySelectorAll('nav, [role="navigation"]').length,
          siteLogos: doc.querySelectorAll('img[alt="Laravel Logo"]').length,
          firstContentElement: doc.querySelector('h2, ul, ol, p')?.tagName,
        };
      });
      expect.soft(extracted.title).toBe(title);
      expect.soft(extracted.tables).toEqual(tables);
      expect(extracted.navigation).toBe(0);
      expect(extracted.siteLogos).toBe(0);
      expect(extracted.firstContentElement).toBe('H2');

      const toc = page.locator('.theme-doc-markdown > nav');
      await expect(toc).toHaveAttribute('role', 'navigation');
      await expect(toc).toHaveAttribute('aria-label', locale === 'ja' ? '目次' : '목차');
      await toc.locator('a').first().click();
      await expect(page).toHaveURL(/#introduction|#versioning-scheme/);
    });
  }
}
