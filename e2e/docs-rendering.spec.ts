import {expect, test} from '@playwright/test';
import {docsPath, docsPathForVersion, latestDocsVersion, stableDocsVersions} from './utils/docs-version';

test.describe('Docs rendering', () => {
  test('version root renders the installation document, not README', async ({page}) => {
    const response = await page.goto(docsPath());
    expect(response?.ok()).toBe(true);
    expect(response?.request().redirectedFrom()).toBeNull();

    await expect(page.getByRole('heading', {level: 1})).toContainText('설치');
    await expect(page.getByText('Laravel 문서의 온라인 버전')).toHaveCount(0);

    const slashResponse = await page.goto(`${docsPath()}/`);
    expect(slashResponse?.ok()).toBe(true);
    await expect(page.getByRole('heading', {level: 1})).toContainText('설치');
  });

  test('collections page renders Laravel-specific HTML, anchors, and admonitions', async ({page}) => {
    await page.goto(docsPath('collections'));

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
    await page.goto(docsPath('collections'));

    await expect(page.locator('.language-markup')).not.toHaveCount(0);
    await expect(page.locator('.language-blade')).toHaveCount(0);
  });

  test('mapped Laravel anchor ids land on rendered headings', async ({page}) => {
    // anchor-mapping 플러그인이 라라벨 원본의 `<a name="configuration">` 을
    // 다음 헤딩의 HTML id 로 매핑하는지를 검증한다. 실제 hash 자동 스크롤은
    // Docusaurus prod 빌드의 inline script 책임이라 dev 서버에서는 검증할 수
    // 없고 GitHub Pages 운영에서 동작한다.
    await page.goto(`${docsPath('database')}#configuration`);

    const heading = page.locator('#configuration');
    await expect(heading).toBeVisible();
    await expect(heading).toContainText(/설정|Configuration/);
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
    await page.waitForURL(`**${docsPath('pulse')}`);

    await expect(page.getByRole('heading', {level: 1})).toContainText('Pulse');

    const samplePath = 'sample';
    await page.goto(`/docs/${samplePath}`);
    await page.waitForURL(`**${docsPath(samplePath)}`);
    await page.waitForTimeout(3500);

    expect(new URL(page.url()).pathname).toBe(docsPath(samplePath));
  });

  for (const version of stableDocsVersions) {
    test(`collections document renders for ${version}`, async ({page}) => {
      await page.goto(docsPathForVersion(version, 'collections'));

      await expect(page.getByRole('heading', {level: 1})).toContainText('컬렉션');
      await expect(page.locator('#introduction')).toBeVisible();
      await expect(page.locator('body')).not.toContainText('{{version}}');
    });
  }
});
