import {expect, test} from '@playwright/test';
import {docsPath, docsPathForVersion, latestDocsVersion, stableDocsVersions} from './utils/docs-version';

const normalizePathname = (path: string): string =>
  path.length > 1 ? path.replace(/\/$/, '') : path;

test.describe('Docs rendering', () => {
  test('version root renders the installation document, not README', async ({page}) => {
    const response = await page.goto(docsPath());
    expect(response?.ok()).toBe(true);
    expect(response?.request().redirectedFrom()).toBeNull();

    await expect(page.getByRole('heading', {level: 1})).toContainText('Installation');
    await expect(page.locator('article')).toContainText('Laravel은');
    await expect(page.getByText('Laravel 문서의 온라인 버전')).toHaveCount(0);

    const slashResponse = await page.goto(`${docsPath()}/`);
    expect(slashResponse?.ok()).toBe(true);
    await expect(page.getByRole('heading', {level: 1})).toContainText('Installation');
  });

  test('collections page renders Laravel-specific HTML, anchors, and admonitions', async ({page}) => {
    await page.goto(docsPath('collections'));

    await expect(page.getByRole('heading', {level: 1})).toContainText('Collections');
    await expect(page.locator('article')).toContainText('컬렉션');
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

  test('sidebar labels stay in English while body text is localized', async ({page}) => {
    await page.goto(docsPath('collections'));

    const sidebar = page.locator('.theme-doc-sidebar-container');
    await expect(sidebar).toContainText('Getting Started');
    await expect(sidebar).toContainText('Collections');
    await expect(sidebar).not.toContainText(/[가-힣ぁ-んァ-ン一-龯]/);
    await expect(page.locator('article')).toContainText('컬렉션');
  });

  test('paginator keeps doc title when sidebar permalink has duplicate labels', async ({page}) => {
    await page.goto(docsPath('cashier-paddle'));

    const nextLink = page.locator('.pagination-nav__link--next');
    await expect(nextLink).toContainText('Dusk');
    await expect(nextLink).not.toContainText('Browser Tests');
  });

  test('blade fences render through a supported Prism language alias', async ({page}) => {
    await page.goto(docsPath('collections'));

    await expect(page.locator('.language-markup')).not.toHaveCount(0);
    await expect(page.locator('.language-blade')).toHaveCount(0);
  });

  test('hash navigation lands on mapped Laravel anchor ids', async ({page}) => {
    await page.goto(`${docsPath('database')}#configuration`);

    const heading = page.locator('#configuration');
    await expect(heading).toBeVisible();

    const box = await heading.boundingBox();
    expect(box).not.toBeNull();
    expect(box!.y).toBeGreaterThanOrEqual(0);
    expect(box!.y).toBeLessThan(220);
  });

  test('table of contents links point to rendered heading ids', async ({page}) => {
    await page.goto(docsPath());

    const brokenTocLinks = await page
      .locator('.table-of-contents a[href^="#"]')
      .evaluateAll((links) =>
        links
          .map((link) => link.getAttribute('href'))
          .filter((href): href is string => href !== null)
          .filter((href) => !document.getElementById(decodeURIComponent(href.slice(1)))),
      );

    expect(brokenTocLinks).toEqual([]);
  });

  test('upgrade guide preserves Laravel dot anchor ids', async ({page}) => {
    const latestMajor = latestDocsVersion.replace(/\.x$/, '.0');
    const upgradeAnchor = `upgrade-${latestMajor}`;

    await page.goto(`${docsPath('upgrade')}#${upgradeAnchor}`);

    await expect(page.locator(`[id="${upgradeAnchor}"]`)).toBeVisible();
    const brokenTocLinks = await page
      .locator('.table-of-contents a[href^="#"]')
      .evaluateAll((links) =>
        links
          .map((link) => link.getAttribute('href'))
          .filter((href): href is string => href !== null)
          .filter((href) => !document.getElementById(decodeURIComponent(href.slice(1)))),
      );

    expect(brokenTocLinks).toEqual([]);
  });

  test('unversioned docs paths redirect to the latest stable version', async ({page}) => {
    await page.goto('/docs/pulse');
    await page.waitForURL(
      (url) => normalizePathname(url.pathname) === docsPath('pulse'),
    );

    await expect(page.getByRole('heading', {level: 1})).toContainText('Pulse');

    const samplePath = 'sample';
    await page.goto(`/docs/${samplePath}`);
    await page.waitForURL(
      (url) => normalizePathname(url.pathname) === docsPath(samplePath),
    );
    await page.waitForTimeout(3500);

    expect(normalizePathname(new URL(page.url()).pathname)).toBe(
      docsPath(samplePath),
    );
  });

  test('Japanese docs do not show the translation-in-progress banner', async ({page}) => {
    await page.goto('/ja/docs/13.x');

    await expect(page.locator('.translation-banner')).toHaveCount(0);
    await expect(page.getByRole('heading', {level: 1})).toContainText('Installation');
    await expect(page.locator('article')).toContainText('Laravel');
  });

  test('English locale is excluded from the build', async ({page}) => {
    // en is a source-reference locale only (annotation/verification); it is not a
    // published site. Visiting it must not serve a docs page.
    const response = await page.goto('/en/docs/13.x');

    expect(response?.status()).toBe(404);
    await expect(page.locator('.translation-banner')).toHaveCount(0);
  });

  for (const version of stableDocsVersions) {
    test(`collections document renders for ${version}`, async ({page}) => {
      await page.goto(docsPathForVersion(version, 'collections'));

      await expect(page.getByRole('heading', {level: 1})).toContainText('Collections');
      await expect(page.locator('article')).toContainText('컬렉션');
      await expect(page.locator('#introduction')).toBeVisible();
      await expect(page.locator('body')).not.toContainText('{{version}}');
    });
  }
});
