import {expect, test} from '@playwright/test';

test.describe('Docs rendering', () => {
  test('version root renders the installation document, not README', async ({page}) => {
    const response = await page.goto('/docs/12.x');
    expect(response?.ok()).toBe(true);

    await expect(page.getByRole('heading', {level: 1})).toContainText('설치');
    await expect(page.getByText('Laravel 문서의 온라인 버전')).toHaveCount(0);

    const slashResponse = await page.goto('/docs/12.x/');
    expect(slashResponse?.ok()).toBe(true);
    await expect(page.getByRole('heading', {level: 1})).toContainText('설치');
  });

  test('collections page renders Laravel-specific HTML, anchors, and admonitions', async ({page}) => {
    await page.goto('/docs/12.x/collections');

    await expect(page.getByRole('heading', {level: 1})).toContainText('컬렉션');
    await expect(page.locator('#introduction')).toBeVisible();
    await expect(page.locator('#method-listing.collection-method.first-collection-method')).toBeVisible();
    await expect(page.locator('#method-map.collection-method')).toBeVisible();
    await expect(page.locator('body')).not.toContainText('{.collection-method');
    await expect(page.locator('blockquote.admonition-info')).not.toHaveCount(0);
    await expect(page.locator('blockquote.admonition-warning')).not.toHaveCount(0);
    await expect(page.getByText('[!NOTE]')).toHaveCount(0);
    await expect(page.getByText('[!WARNING]')).toHaveCount(0);

    const bodyText = await page.locator('body').textContent();
    expect(bodyText).not.toContain('{{version}}');
  });

  test('blade fences render through a supported Prism language alias', async ({page}) => {
    await page.goto('/docs/12.x/collections');

    await expect(page.locator('.language-markup')).not.toHaveCount(0);
    await expect(page.locator('.language-blade')).toHaveCount(0);
  });

  test('hash navigation lands on mapped Laravel anchor ids', async ({page}) => {
    await page.goto('/docs/12.x/database#configuration');

    const heading = page.locator('#configuration');
    await expect(heading).toBeVisible();

    const box = await heading.boundingBox();
    expect(box).not.toBeNull();
    expect(box!.y).toBeGreaterThanOrEqual(0);
    expect(box!.y).toBeLessThan(220);
  });

  for (const version of ['12.x', '11.x', '10.x', '9.x', '8.x']) {
    test(`collections document renders for ${version}`, async ({page}) => {
      await page.goto(`/docs/${version}/collections`);

      await expect(page.getByRole('heading', {level: 1})).toContainText('컬렉션');
      await expect(page.locator('#introduction')).toBeVisible();
      await expect(page.locator('body')).not.toContainText('{{version}}');
    });
  }
});
