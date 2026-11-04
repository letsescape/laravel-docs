import {test, expect, type Page} from '@playwright/test';
import versions from '../versions.json';

const stable = versions.find((version) => version !== 'master')!;

async function mockSearch(page: Page, totalPages = 1) {
  const filters: string[] = [];
  await page.route(/https:\/\/[^/]+\.algolia(?:\.net|net\.com)\//, async (route) => {
    const {requests} = route.request().postDataJSON();
    const results = requests.map((request: {params?: string; query?: string; facetFilters?: string[]; hitsPerPage?: number; page?: number}) => {
      const params = typeof request.params === 'string'
        ? Object.fromEntries(new URLSearchParams(request.params)) : request;
      const facets = JSON.stringify(params.facetFilters);
      if (Number(params.hitsPerPage) !== 0) filters.push(facets);
      const version = /docs-default-([\w.]+)/.exec(facets)?.[1] ?? stable;
      const prefix = facets.includes('language:ja') ? '/ja' : '';
      const hierarchy = {lvl0: 'Documentation', lvl1: 'Routing', lvl2: null, lvl3: null, lvl4: null, lvl5: null, lvl6: null};
      return {
        hits: Array.from({length: totalPages > 1 ? 15 : 1}, (_, index) => ({
          objectID: `${prefix}-${version}-routing-${params.page ?? 0}-${index}`,
          url: `https://laravel.chanhyung.kim${prefix}/docs/${version}/routing/`,
          type: 'lvl1',
          hierarchy,
          content: null,
          _highlightResult: {hierarchy: {lvl0: {value: 'Documentation'}, lvl1: {value: 'Routing'}}},
        })),
        nbHits: 100,
        nbPages: totalPages,
        page: Number(params.page ?? 0),
        hitsPerPage: 20,
        processingTimeMS: 1,
        query: params.query ?? 'routing',
        facets: {},
      };
    });
    await route.fulfill({json: {results}});
  });
  return filters;
}

for (const {locale, prefix} of [{locale: 'ko', prefix: ''}, {locale: 'ja', prefix: '/ja'}]) {
  test(`${locale} full search defaults to stable and applies every selected version`, async ({page}) => {
    const filters = await mockSearch(page);
    await page.goto(`${prefix}/q/?q=routing`);
    await expect(page.locator('select')).toHaveValue(stable);
    await expect(page.locator('select')).toHaveAccessibleName(
      locale === 'ko' ? `문서 버전: ${stable}` : `ドキュメントのバージョン: ${stable}`,
    );
    for (const version of versions) {
      filters.length = 0;
      await page.locator('select').selectOption(version);
      await expect.poll(() => filters.some((value) => value.includes(`docs-default-${version}`))).toBe(true);
      await expect(page.locator(`main article a[href="${prefix}/docs/${version}/routing/"]`).first()).toBeVisible();
      expect(filters.every((value) => value.includes(`language:${locale}`)), JSON.stringify(filters)).toBe(true);
    }
  });

  for (const version of ['11.x', 'master']) {
    test(`${locale} ${version} modal keeps its version in full search`, async ({page}) => {
      const filters = await mockSearch(page);
      await page.goto(`${prefix}/docs/${version}/routing/`);
      await expect(page.locator('html')).toHaveAttribute('data-has-hydrated', 'true');
      await page.locator('.DocSearch-Button').click();
      await page.locator('.DocSearch-Input').fill('routing');
      const fullSearch = page.locator('.DocSearch-Container a[href*="/q/?"]');
      await expect(fullSearch).toBeVisible();
      await fullSearch.click();
      await expect(page.locator('select')).toHaveValue(version);
      await expect(page.locator('.DocSearch-Container')).toHaveCount(0);
      await expect(page.locator(`main article a[href="${prefix}/docs/${version}/routing/"]`).first()).toBeVisible();
      expect(filters.every((value) => value.includes(`docs-default-${version}`)), JSON.stringify(filters)).toBe(true);
      await page.reload();
      await expect(page.locator('select')).toHaveValue(version);
    });
  }
}

for (const delayedPage of [0, 1]) {
  test(`full search discards an old version's delayed page ${delayedPage}`, async ({page}) => {
    await mockSearch(page, delayedPage + 1);
    let releaseResponse!: () => void;
    const responseGate = new Promise<void>((resolve) => { releaseResponse = resolve; });
    let delayedRequest = false;
    await page.route(/https:\/\/[^/]+\.algolia(?:\.net|net\.com)\//, async (route) => {
      const {requests} = route.request().postDataJSON();
      const request = requests[0];
      const params = typeof request.params === 'string'
        ? Object.fromEntries(new URLSearchParams(request.params)) : request;
      if (JSON.stringify(params.facetFilters).includes('docs-default-11.x') && Number(params.page ?? 0) === delayedPage) {
        delayedRequest = true;
        await responseGate;
      }
      await route.fallback();
    });

    await page.goto('/q/?q=routing');
    await expect(page.locator(`main article a[href="/docs/${stable}/routing/"]`).first()).toBeVisible();
    await page.locator('select').selectOption('11.x');
    if (delayedPage === 1) {
      await expect(page.locator('main article a[href="/docs/11.x/routing/"]').first()).toBeVisible();
      await page.waitForTimeout(100);
      await page.locator('[class*="loader_"]').evaluate((element) => element.scrollIntoView({block: 'center'}));
    }
    await expect.poll(() => delayedRequest).toBe(true);
    await page.locator('select').selectOption(stable);
    await expect(page.locator(`main article a[href="/docs/${stable}/routing/"]`).first()).toBeVisible();
    const delayedResponse = page.waitForResponse((response) =>
      response.request().postData()?.includes('docs-default-11.x') === true,
    );
    releaseResponse();
    await (await delayedResponse).finished();
    await page.waitForTimeout(200);
    await expect(page.locator('select')).toHaveValue(stable);
    await expect(page.locator('main article a[href="/docs/11.x/routing/"]')).toHaveCount(0);
    await expect(page.locator(`main article a[href="/docs/${stable}/routing/"]`).first()).toBeVisible();
  });
}

test('full search debounces typing and searches once when restoring a saved version', async ({page}) => {
  const filters = await mockSearch(page);
  await page.goto('/q/');
  await expect(page.locator('html')).toHaveAttribute('data-has-hydrated', 'true');
  await page.locator('input[name="q"]').pressSequentially('routing', {delay: 30});
  await expect(page.locator(`main article a[href="/docs/${stable}/routing/"]`)).toBeVisible();
  await page.waitForTimeout(400);
  expect(filters).toHaveLength(1);

  await page.locator('select').selectOption('11.x');
  await expect(page.locator('main article a[href="/docs/11.x/routing/"]')).toBeVisible();
  filters.length = 0;
  await page.reload();
  await expect(page.locator('select')).toHaveValue('11.x');
  await expect(page.locator('main article a[href="/docs/11.x/routing/"]')).toBeVisible();
  await page.waitForTimeout(400);
  expect(filters).toHaveLength(1);
});
