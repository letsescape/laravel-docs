import {test, expect} from '@playwright/test';

// Helper: meta 태그의 attribute 존재 검증
async function expectMetaAttribute(page: any, selector: string, attr: string, pattern: RegExp) {
  await expect(page.locator(selector)).toHaveAttribute(attr, pattern);
}

test.describe('SEO', () => {
  test.beforeEach(async ({page}) => {
    await page.goto('/');
  });

  for (const {name, selector, pattern} of [
    {name: 'meta description', selector: 'meta[name="description"]', pattern: /.+/},
    {name: 'og:title', selector: 'meta[property="og:title"]', pattern: /.+/},
    {name: 'og:description', selector: 'meta[property="og:description"]', pattern: /.+/},
    {name: 'og:image', selector: 'meta[property="og:image"]', pattern: /laravel-home\.png/},
    {name: 'og:site_name', selector: 'meta[property="og:site_name"]', pattern: /.+/},
    {name: 'keywords', selector: 'meta[name="keywords"]', pattern: /Laravel/i},
  ]) {
    test(`page has ${name} meta tag`, async ({page}) => {
      await expectMetaAttribute(page, selector, 'content', pattern);
    });
  }

  test('page has canonical link', async ({page}) => {
    await expectMetaAttribute(page, 'link[rel="canonical"]', 'href', /.+/);
  });

  test('page has JSON-LD structured data', async ({page}) => {
    const jsonLd = page.locator('script[type="application/ld+json"]').first();
    await expect(jsonLd).toBeAttached();

    const content = await jsonLd.textContent();
    expect(content).not.toBeNull();
    const data = JSON.parse(content!);
    expect(data['@type']).toBe('WebSite');
    expect(data).toHaveProperty('potentialAction');
  });

  test('page has twitter meta tags', async ({page}) => {
    await expectMetaAttribute(page, 'meta[name="twitter:title"]', 'content', /.+/);
    await expectMetaAttribute(page, 'meta[name="twitter:description"]', 'content', /.+/);
  });
});
