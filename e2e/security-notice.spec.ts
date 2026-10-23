import {expect, test} from '@playwright/test';
import {docsPath} from './utils/docs-version';
import {announcement} from '../src/theme/AnnouncementBar/config';
import {DISMISSAL_ATTRIBUTE, DISMISSAL_STORAGE_KEY as dismissalKey} from '../src/theme/AnnouncementBar/constants';

const noticeSelector = `aside[aria-label="${announcement.locales.ko.label}"]`;
const locales = [['', announcement.locales.ko], ['/ja', announcement.locales.ja]] as const;

test.describe('disabled notice', () => {
  test.skip(announcement.enabled, 'Run with enabled: false');

  for (const [locale, text] of locales) {
    for (const path of ['/', docsPath()]) {
      for (const javaScriptEnabled of [false, true]) {
        test(`no banner or reserved space at ${locale}${path}, JavaScript=${javaScriptEnabled}`, async ({browser, baseURL}) => {
          const context = await browser.newContext({baseURL, javaScriptEnabled});
          try {
            await context.addInitScript((key) => localStorage.setItem(key, 'true'), dismissalKey);
            const page = await context.newPage();
            await page.goto(`${locale}${path}`);
            if (javaScriptEnabled) await expect(page.locator('html')).toHaveAttribute('data-has-hydrated', 'true');
            await expect(page.getByRole('complementary', {name: text.label})).toHaveCount(0);
            await expect(page.locator('html')).not.toHaveAttribute(DISMISSAL_ATTRIBUTE);
            expect((await page.locator('.navbar').boundingBox())!.y).toBe(0);
          } finally {
            await context.close();
          }
        });
      }
    }
  }
});

test.describe('enabled notice', () => {
  test.skip(!announcement.enabled, 'Run with enabled: true');

  for (const [locale, text] of locales) {
    for (const path of ['/', docsPath()]) {
      test(`security notice is visible without JavaScript at ${locale}${path}`, async ({browser, baseURL}) => {
        const context = await browser.newContext({baseURL, javaScriptEnabled: false});
        try {
          const page = await context.newPage();
          await page.goto(`${locale}${path}`);
          await expect(page.getByRole('complementary', {name: text.label})).toBeVisible();
        } finally {
          await context.close();
        }
      });
    }
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
    await expect(otherPage.locator(noticeSelector)).toBeVisible();
    await page.getByRole('button', {name: announcement.locales.ko.dismissLabel}).click();
    await expect(otherPage.locator(noticeSelector)).toHaveCount(0);
    await page.reload();
    await expect(page.locator('html')).toHaveAttribute('data-has-hydrated', 'true');
    await expect(page.locator(noticeSelector)).toHaveCount(0);
    await page.goto(`/ja${docsPath()}`);
    await expect(page.locator('html')).toHaveAttribute('data-has-hydrated', 'true');
    await expect(page.getByRole('complementary', {name: announcement.locales.ja.label})).toHaveCount(0);
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
    await page.getByRole('button', {name: announcement.locales.ko.dismissLabel}).click();
    await expect(page.locator(noticeSelector)).toHaveCount(0);
  });

  for (const [locale, text] of locales) {
    test(`notice uses configured content and optional links at ${locale || '/'}`, async ({page}) => {
      await page.goto(`${locale}/`);
      const notice = page.getByRole('complementary', {name: text.label});
      await expect(notice).toHaveAttribute('data-variant', announcement.variant);
      await expect(notice).toContainText(text.message);
      if (announcement.href) {
        await expect(notice.getByRole('link').filter({hasText: text.message})).toHaveAttribute('href', announcement.href);
        if (text.linkText) await expect(notice.getByRole('link', {name: text.linkText, exact: true})).toHaveAttribute('href', announcement.href);
      } else {
        await expect(notice.getByRole('link').filter({hasText: text.message})).toHaveCount(0);
      }
      if (announcement.github) {
        await expect(notice.getByRole('link', {name: announcement.github.label})).toHaveAttribute('href', announcement.github.href);
      } else {
        await expect(notice.locator('svg')).toHaveCount(0);
      }
    });
  }

  test('closing a previous notice does not hide a different notice', async ({page}) => {
    await page.addInitScript(() => localStorage.setItem('laravel-docs.security-notice.previous-notice.dismissed', 'true'));
    await page.goto('/');
    await expect(page.locator('html')).toHaveAttribute('data-has-hydrated', 'true');
    await expect(page.locator(noticeSelector)).toBeVisible();
  });
});
