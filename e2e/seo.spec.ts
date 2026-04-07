import {test, expect} from '@playwright/test';

test.describe('SEO', () => {
  test.beforeEach(async ({page}) => {
    await page.goto('/');
  });

  test('page has meta description', async ({page}) => {
    const metaDescription = page.locator('meta[name="description"]');
    await expect(metaDescription).toHaveAttribute('content', /.+/);
  });

  test('page has og:title meta tag', async ({page}) => {
    const ogTitle = page.locator('meta[property="og:title"]');
    await expect(ogTitle).toHaveAttribute('content', /.+/);
  });

  test('page has og:description meta tag', async ({page}) => {
    const ogDescription = page.locator('meta[property="og:description"]');
    await expect(ogDescription).toHaveAttribute('content', /.+/);
  });

  test('page has og:image meta tag', async ({page}) => {
    const ogImage = page.locator('meta[property="og:image"]');
    await expect(ogImage).toHaveAttribute('content', /laravel-home\.png/);
  });

  test('page has canonical link', async ({page}) => {
    const canonical = page.locator('link[rel="canonical"]');
    await expect(canonical).toHaveAttribute('href', /.+/);
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
    const twitterTitle = page.locator('meta[name="twitter:title"]');
    await expect(twitterTitle).toHaveAttribute('content', /.+/);

    const twitterDescription = page.locator('meta[name="twitter:description"]');
    await expect(twitterDescription).toHaveAttribute('content', /.+/);
  });

  test('page has og:site_name meta tag', async ({page}) => {
    const ogSiteName = page.locator('meta[property="og:site_name"]');
    await expect(ogSiteName).toHaveAttribute('content', /.+/);
  });

  test('page has keywords meta tag', async ({page}) => {
    const keywords = page.locator('meta[name="keywords"]');
    await expect(keywords).toHaveAttribute('content', /Laravel/i);
  });
});
