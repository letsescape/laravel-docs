import {test, expect, type Page} from '@playwright/test';
import versions from '../versions.json';

const stable = versions.find((version) => version !== 'master')!;

async function mockSearch(page: Page) {
  const filters: string[] = [];
  await page.route(/https:\/\/[^/]+\.algolia(?:\.net|net\.com)\//, async (route) => {
    const {requests} = route.request().postDataJSON();
    const results = requests.map((request: {params?: string; query?: string; facetFilters?: string[]; hitsPerPage?: number}) => {
      const params = typeof request.params === 'string'
        ? Object.fromEntries(new URLSearchParams(request.params)) : request;
      const facets = JSON.stringify(params.facetFilters);
      if (Number(params.hitsPerPage) !== 0) filters.push(facets);
      const version = /docs-default-([\w.]+)/.exec(facets)?.[1] ?? stable;
      const prefix = facets.includes('language:ja') ? '/ja' : '';
      const hierarchy = {lvl0: 'Documentation', lvl1: 'Routing', lvl2: null, lvl3: null, lvl4: null, lvl5: null, lvl6: null};
      return {
        hits: [{
          objectID: `${prefix}-${version}-routing`,
          url: `https://laravel.chanhyung.kim${prefix}/docs/${version}/routing/`,
          type: 'lvl1',
          hierarchy,
          content: null,
          _highlightResult: {hierarchy: {lvl0: {value: 'Documentation'}, lvl1: {value: 'Routing'}}},
        }],
        nbHits: 100,
        nbPages: 1,
        page: 0,
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
