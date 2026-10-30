import {expect, test} from '@playwright/test';
import {docsPath, docsPathForVersion, latestDocsVersion} from './utils/docs-version';

test.describe('Document printing', () => {
  for (const colorScheme of ['light', 'dark'] as const) {
    test(`${colorScheme}: prints the document without site controls`, async ({page, context}) => {
      await page.emulateMedia({colorScheme});
      await page.goto(docsPath());
      await expect(page.locator('.docs-print-qr path')).toHaveCount(2);
      await expect(page.locator('.docs-print-header')).toBeHidden();
      await expect(page.locator('.navbar')).toBeVisible();
      await expect(page.locator('.hp-footer')).toBeVisible();

      await context.setOffline(true);
      await page.emulateMedia({media: 'print'});

      await expect(page.locator('.docs-print-header')).toBeVisible();
      await expect(page.locator('.docs-print-qr')).toBeVisible();
      await expect(page.locator('h1')).toContainText('Installation');
      await expect(page.locator('html')).toHaveCSS('background-color', 'rgb(255, 255, 255)');
      await expect(page.locator('body')).toHaveCSS('color', 'rgb(17, 17, 17)');
      await expect(page.locator('.docs-print-qr path').first()).toHaveCSS('fill', 'rgb(255, 255, 255)');
      await expect(page.locator('.docs-print-qr path').last()).toHaveCSS('fill', 'rgb(0, 0, 0)');
      const code = page.locator('.theme-code-block pre').first();
      await expect(code).toHaveCSS('background-color', 'rgba(0, 0, 0, 0)');
      await expect(code.locator('span[style]').first()).toHaveCSS('color', 'rgb(17, 17, 17)');

      for (const selector of [
        '.navbar', '.theme-announcement-bar', '.hp-footer',
        '.theme-doc-sidebar-container', '.theme-doc-toc-desktop',
        '.theme-doc-toc-mobile', '.theme-doc-breadcrumbs',
        '.theme-doc-footer', '.pagination-nav', '.theme-back-to-top-button',
        'main > .container > .row > .col--3',
      ]) {
        await expect(page.locator(selector)).toBeHidden();
      }
      for (const button of await page.locator('.theme-code-block button').all()) {
        await expect(button).toBeHidden();
      }

      const article = await page.locator('article').boundingBox();
      expect(article!.x).toBeLessThanOrEqual(1);
      expect(article!.y).toBeLessThanOrEqual(1);
      expect(article!.width).toBeGreaterThanOrEqual(page.viewportSize()!.width - 2);

      await page.emulateMedia({media: 'screen'});
      await expect(page.locator('.docs-print-header')).toBeHidden();
      await expect(page.locator('.navbar')).toBeVisible();
      await expect(page.locator('.hp-footer')).toBeVisible();
      await expect(page.locator('html')).toHaveAttribute('data-theme', colorScheme);
    });
  }

  for (const [route, source] of [
    [docsPath(), `${latestDocsVersion}/installation`],
    [`/ja${docsPath('collections')}`, `${latestDocsVersion}/collections`],
    [docsPathForVersion('8.x', 'routing'), '8.x/routing'],
    [docsPathForVersion('master', 'configuration'), 'master/configuration'],
  ]) {
    test(`links ${route} to its original Laravel document`, async ({page}) => {
      await page.goto(route);
      await expect(page.locator('.docs-print-header a')).toHaveAttribute('href', `https://laravel.com/docs/${source}`);
      await expect(page.locator('.docs-print-qr title')).toHaveText(`https://laravel.com/docs/${source}`);
      await page.emulateMedia({media: 'print'});
      await expect(page.locator('.docs-print-header')).toBeVisible();
      await expect(page.locator('.docs-print-header')).toContainText(route.startsWith('/ja') ? '日本語ドキュメント' : '한국어 문서');
    });
  }

  test('prints code, tables, and method names without horizontal clipping', async ({page}) => {
    const viewportWidth = 680;
    await page.setViewportSize({width: viewportWidth, height: 900});
    await page.goto(docsPath('collections'));
    await expect(page.locator('html')).toHaveAttribute('data-has-hydrated', 'true');
    await page.emulateMedia({media: 'print', colorScheme: 'dark'});

    const content = page.locator('.theme-doc-markdown');
    const clipped = await content.locator('pre, code, table, blockquote.admonition, .collection-method-list a').evaluateAll(elements =>
      elements.filter(element => element.clientWidth > 0 && element.scrollWidth > element.clientWidth + 1)
        .map(element => element.textContent?.slice(0, 80)),
    );
    expect(clipped).toEqual([]);
    expect(await page.locator('html').evaluate(element => element.scrollWidth)).toBeLessThanOrEqual(viewportWidth + 1);
    expect(await content.evaluate(element => element.scrollWidth)).toBeLessThanOrEqual(viewportWidth + 1);
    await expect(content.locator('blockquote.admonition-warning').first()).toBeVisible();
    await expect(content.locator('pre code').first()).toHaveCSS('float', 'none');

    await page.goto(docsPath('releases'));
    await expect(page.locator('.theme-doc-markdown table').first()).toBeVisible();
    expect(await page.locator('.theme-doc-markdown table').evaluateAll(tables =>
      tables.every(table => table.scrollWidth <= table.clientWidth + 1),
    )).toBe(true);
    expect(await page.locator('html').evaluate(element => element.scrollWidth)).toBeLessThanOrEqual(viewportWidth + 1);
    expect(await content.evaluate(element => element.scrollWidth)).toBeLessThanOrEqual(viewportWidth + 1);
  });

  test('updates the QR source on client navigation and leaves the homepage unchanged', async ({page}) => {
    await page.goto(docsPath('configuration'));
    const firstQr = await page.locator('.docs-print-qr path').last().getAttribute('d');
    await page.locator('.pagination-nav__link--next').click();
    await expect(page.locator('.docs-print-qr path').last()).not.toHaveAttribute('d', firstQr!);
    await expect(page.locator('.docs-print-header a')).not.toHaveAttribute('href', `https://laravel.com/docs/${latestDocsVersion}/configuration`);

    await page.locator('.navbar__brand').click();
    await expect(page.locator('.homepage')).toBeVisible();
    await expect(page.locator('.docs-print-header')).toHaveCount(0);
    const background = await page.locator('html').evaluate(element => getComputedStyle(element).backgroundColor);
    await page.emulateMedia({media: 'print'});
    await expect(page.locator('html')).not.toHaveClass(/docs-doc-page/);
    await expect(page.locator('html')).toHaveCSS('background-color', background);
    await expect(page.locator('.hp-footer')).toBeVisible();
  });

  test('prints the full document even with mobile search open', async ({page}) => {
    await page.setViewportSize({width: 390, height: 844});
    await page.goto(docsPath());
    await page.locator('.DocSearch-Button').click();
    await expect(page.locator('.DocSearch-Container')).toBeVisible();
    await page.emulateMedia({media: 'print'});
    await expect(page.locator('.DocSearch-Container')).toBeHidden();
    await expect(page.locator('body')).toHaveCSS('position', 'static');
    await expect(page.locator('body')).toHaveCSS('overflow', 'visible');
    await expect(page.locator('.theme-doc-markdown')).toBeVisible();
    const body = await page.locator('body').boundingBox();
    const article = await page.locator('article').boundingBox();
    expect(body!.height).toBeGreaterThanOrEqual(article!.height);
  });
});
