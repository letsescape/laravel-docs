import {expect, test} from '@playwright/test';
import {docsPath} from './utils/docs-version';

const dismissalKey = 'laravel-docs.security-notice.php-critical-vulnerability-response-updates.dismissed';
const noticeSelector = 'aside[aria-label="중요 보안 공지"]';

for (const [locale, label] of [['', '중요 보안 공지'], ['/ja', '重要なセキュリティのお知らせ']]) {
  test(`security notice is visible without JavaScript in ${locale || 'ko'}`, async ({browser, baseURL}) => {
    const context = await browser.newContext({baseURL, javaScriptEnabled: false});
    try {
      const page = await context.newPage();
      await page.goto(`${locale}${docsPath()}`);
      await expect(page.getByRole('complementary', {name: label})).toBeVisible();
    } finally {
      await context.close();
    }
  });
}

for (const dismissed of [false, true]) {
  test(`security notice keeps its initial layout through hydration when dismissed=${dismissed}`, async ({page}) => {
    if (dismissed) {
      await page.addInitScript((key) => localStorage.setItem(key, 'true'), dismissalKey);
    }

    let releaseScripts!: () => void;
    const scriptGate = new Promise<void>((resolve) => { releaseScripts = resolve; });
    await page.route('**/assets/js/**', async (route) => {
      await scriptGate;
      await route.continue();
    });

    try {
      await page.goto(docsPath(), {waitUntil: 'commit'});
      const notice = page.locator(noticeSelector);
      await expect(notice).toHaveCount(1);
      await expect(notice).toHaveCSS('position', 'relative');
      await expect(page.locator('html')).toHaveAttribute('data-has-hydrated', 'false');
      if (dismissed) {
        await expect(notice).toBeHidden();
      } else {
        await expect(notice).toBeVisible();
      }
      await page.evaluate(() => document.fonts.ready);
      const before = await page.locator('.navbar').boundingBox();
      const sidebarMargin = await page.locator('.theme-doc-sidebar-container .menu').evaluate(
        (element) => getComputedStyle(element).marginBottom,
      );
      const positions = page.evaluate(() => new Promise<number[]>((resolve) => {
        const samples: number[] = [];
        let hydratedFrames = 0;
        function sample() {
          samples.push(document.querySelector('.navbar')!.getBoundingClientRect().top);
          if (document.documentElement.dataset.hasHydrated === 'true') hydratedFrames += 1;
          if (hydratedFrames >= 3) resolve(samples);
          else requestAnimationFrame(sample);
        }
        requestAnimationFrame(sample);
      }));
      releaseScripts();
      expect((await positions).every((top) => Math.abs(top - before!.y) < 1)).toBe(true);
      await expect(page.locator('.theme-doc-sidebar-container .menu')).toHaveCSS('margin-bottom', sidebarMargin);
      if (dismissed) await expect(notice).toHaveCount(0);
      else await expect(notice).toBeVisible();
    } finally {
      releaseScripts();
    }
  });
}

test('security notice dismissal persists across tabs, reloads and locales', async ({page, context}) => {
  await page.goto(docsPath());
  await expect(page.locator('html')).toHaveAttribute('data-has-hydrated', 'true');
  const otherPage = await context.newPage();
  await otherPage.goto('/');
  await expect(otherPage.locator('html')).toHaveAttribute('data-has-hydrated', 'true');
  await page.getByRole('button', {name: '보안 공지 닫기'}).click();
  await expect(otherPage.locator(noticeSelector)).toHaveCount(0);
  await page.reload();
  await expect(page.locator('html')).toHaveAttribute('data-has-hydrated', 'true');
  await expect(page.locator(noticeSelector)).toHaveCount(0);
  await page.goto(`/ja${docsPath()}`);
  await expect(page.locator('html')).toHaveAttribute('data-has-hydrated', 'true');
  await expect(page.getByRole('complementary', {name: '重要なセキュリティのお知らせ'})).toHaveCount(0);
});

test('security notice still displays and closes when localStorage is unavailable', async ({page}) => {
  await page.addInitScript(() => {
    Object.defineProperty(window, 'localStorage', {
      get() { throw new DOMException('Storage unavailable', 'SecurityError'); },
    });
  });
  await page.goto(docsPath());
  await expect(page.locator('html')).toHaveAttribute('data-has-hydrated', 'true');
  await expect(page.locator(noticeSelector)).toBeVisible();
  await page.getByRole('button', {name: '보안 공지 닫기'}).click();
  await expect(page.locator(noticeSelector)).toHaveCount(0);
});
