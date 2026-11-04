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

  test('preview serves document HEAD requests and static assets', async ({request}) => {
    const document = await request.head(`${docsPath()}/`);
    expect(document.status()).toBe(200);
    expect(document.headers()['content-type']).toContain('text/html');
    expect(await document.body()).toHaveLength(0);

    const asset = await request.get('/img/favicon.png');
    expect(asset.status()).toBe(200);
    expect(asset.headers()['content-type']).toContain('image/png');
    expect((await asset.body()).length).toBeGreaterThan(0);
  });

  test('preview returns the built 404 page for a missing path', async ({request}) => {
    const response = await request.get('/preview-test-missing-page/');
    expect(response.status()).toBe(404);
    expect(response.headers()['content-type']).toContain('text/html');
    expect(await response.text()).toContain('Laravel');
  });

  for (const {locale, prefix, title, homeLabel} of [
    {locale: 'ko', prefix: '', title: '페이지를 찾을 수 없습니다.', homeLabel: '메인 페이지로 이동 →'},
    {locale: 'ja', prefix: '/ja', title: 'ページが見つかりません', homeLabel: 'メインページへ移動 →'},
  ]) {
    test(`${locale} missing page keeps its locale and returns to its homepage`, async ({page}) => {
      const path = `${prefix}/verification-missing-page/?check=1#section`;
      const response = await page.goto(path);
      expect(response?.status()).toBe(404);
      await expect(page.locator('html')).toHaveAttribute('lang', locale);
      await expect(page.getByRole('heading', {level: 1})).toHaveText(title);
      await expect(page.getByRole('link', {name: homeLabel})).toHaveAttribute('href', `${prefix}/`);
      await expect(page).toHaveURL((url) => `${url.pathname}${url.search}${url.hash}` === path);
      await page.waitForURL((url) => url.pathname === `${prefix}/`);
      await expect(page.locator('html')).toHaveAttribute('lang', locale);
    });

    test(`${locale} missing versioned document preserves its address and 404 page`, async ({page}) => {
      const path = `${prefix}/docs/11.x/verification-missing-page/?check=1#section`;
      const response = await page.goto(path);
      expect(response?.status()).toBe(404);
      await expect(page.locator('html')).toHaveAttribute('lang', locale);
      await expect(page.getByRole('heading', {level: 1})).toHaveText(title);
      await page.waitForTimeout(3500);
      const original = new URL(page.url());
      expect(`${original.pathname}${original.search}${original.hash}`).toBe(path);
      await expect(page.getByRole('heading', {level: 1})).toHaveText(title);
    });
  }

  test('Japanese missing unversioned document keeps its query and fragment', async ({page}) => {
    await page.goto('/ja/docs/verification-missing-page/?check=1#section');
    await expect(page.locator('html')).toHaveAttribute('lang', 'ja');
    await expect(page.getByRole('heading', {level: 1})).toHaveText('ページが見つかりません');
    await page.waitForTimeout(3500);
    const original = new URL(page.url());
    expect(normalizePathname(original.pathname)).toBe(`/ja${docsPath('verification-missing-page')}`);
    expect(original.search).toBe('?check=1');
    expect(original.hash).toBe('#section');
  });

  test('404 return paths cannot leave the locale or use malformed URLs', async ({page}) => {
    const errors: string[] = [];
    page.on('pageerror', (error) => errors.push(error.message));
    for (const [path, target] of [
      ['/404.html?from=%2F%2Fexample.com%2F', '/'],
      ['/404.html?from=%2F%2F%5B', '/'],
      ['/ja/404.html?from=%2Fja%2F..%2Fdocs%2F11.x%2Fmissing%2F', '/ja/'],
    ]) {
      await page.goto(path);
      const origin = new URL(page.url()).origin;
      await page.waitForURL((url) => url.pathname === target);
      expect(new URL(page.url()).origin).toBe(origin);
    }
    expect(errors).toEqual([]);
  });

  test('preview survives malformed request paths and Host headers', async ({request}) => {
    const malformedPath = await request.get('/%E0%A4%A');
    expect(malformedPath.status()).toBe(400);
    const malformedHost = await request.get('/', {headers: {host: '['}});
    expect(malformedHost.status()).toBe(400);
    expect((await request.get('/')).status()).toBe(200);
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

  for (const locale of ['', '/ja']) {
    for (const [slug, text] of [
      ['broadcasting', 'Illuminate\\Broadcasting\\InteractsWithSockets'],
      ['eloquent-mutators', 'Illuminate\\Contracts\\Support\\Arrayable'],
      ['filesystem', 'League\\Flysystem\\WhitespacePathNormalizer::normalizePath'],
    ]) {
      test(`${locale || 'ko'} ${slug} admonition scrolls without overflowing the page`, async ({page}) => {
        await page.setViewportSize({width: 390, height: 844});
        await page.goto(`${locale}${docsPath(slug)}`);
        await expect(page.locator('html')).toHaveAttribute('data-has-hydrated', 'true');
        await page.evaluate(() => document.fonts.ready);

        const admonition = page.locator('blockquote.admonition').filter({hasText: text});
        await expect(admonition).toHaveCount(1);
        expect(await page.evaluate(() => document.documentElement.scrollWidth)).toBeLessThanOrEqual(390);
        expect(await admonition.evaluate((element) => element.scrollWidth > element.clientWidth)).toBe(true);

        await admonition.hover();
        await page.mouse.wheel(250, 0);
        await expect.poll(() => admonition.evaluate((element) => element.scrollLeft)).toBeGreaterThan(0);
        expect(await page.evaluate(() => window.scrollX)).toBe(0);

        await page.setViewportSize({width: 1440, height: 1000});
        expect(await page.evaluate(() => document.documentElement.scrollWidth)).toBeLessThanOrEqual(1440);
        expect(await admonition.evaluate((element) => element.scrollWidth <= element.clientWidth)).toBe(true);
      });
    }
  }

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

  for (const locale of ['', '/ja']) {
    test(`${locale || 'ko'} repeated validation headings have distinct working permalinks`, async ({page}) => {
      await page.goto(`${locale}${docsPath('validation')}`);
      await expect(page.locator('html')).toHaveAttribute('data-has-hydrated', 'true');
      await page.evaluate(() => document.fonts.ready);

      const headings = page.getByRole('heading', {
        level: 4,
        name: 'Stopping on First Validation Failure',
      });
      await expect(headings).toHaveCount(2);
      const ids = await headings.evaluateAll((elements) => elements.map((element) => element.id));
      expect(ids[0]).toBe('stopping-on-first-validation-failure');
      expect(ids[1]).not.toBe('');
      expect(ids[1]).not.toBe(ids[0]);
      for (const id of ids) {
        await expect(page.locator(`[id="${id}"]`)).toHaveCount(1);
      }

      const secondHeading = headings.nth(1);
      await secondHeading.locator('.hash-link').click();
      await expect(page).toHaveURL((url) => url.hash === `#${ids[1]}`);
      await expect.poll(() => secondHeading.evaluate((element) => element.getBoundingClientRect().top))
        .toBeLessThan(220);
      expect((await secondHeading.boundingBox())!.y).toBeGreaterThanOrEqual(0);
      expect((await headings.first().boundingBox())!.y).toBeLessThan(0);
    });
  }

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
    // `en` 로캘은 주석과 검증에만 사용하는 원문 참조용이며 공개 사이트가 아님
    // 방문 시 문서 페이지를 제공하지 않아야 함
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
