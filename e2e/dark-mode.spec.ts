import {test, expect, type Page} from '@playwright/test';

// 도우미: 색 구성표 설정 후 페이지를 불러와 테마 검증
async function emulateAndVerifyTheme(page: Page, colorScheme: 'dark' | 'light') {
  await page.emulateMedia({colorScheme});
  await page.goto('/');
  await expect(page.locator('html')).toHaveAttribute('data-theme', colorScheme);
}

test.describe('Dark mode', () => {
  test('page loads with a color theme attribute', async ({page}) => {
    await page.goto('/');
    const theme = await page.locator('html').getAttribute('data-theme');
    expect(['dark', 'light']).toContain(theme);
  });

  test('color mode toggle button exists', async ({page}) => {
    await page.goto('/');
    await expect(page.locator('button[class*="toggleButton"]')).toBeVisible();
  });

  test('clicking toggle changes the theme', async ({page}) => {
    await emulateAndVerifyTheme(page, 'dark');
    const toggleButton = page.locator('button[class*="toggleButton"]');
    await toggleButton.click();
    await expect(page.locator('html')).toHaveAttribute('data-theme', 'light');
  });

  test('dark mode can be activated via color scheme emulation', async ({page}) => {
    await emulateAndVerifyTheme(page, 'dark');
  });

  test('light mode can be activated via color scheme emulation', async ({page}) => {
    await emulateAndVerifyTheme(page, 'light');
  });

  test('does not render the bright hero fallback image while the hero SVG is still loading', async ({page}) => {
    await page.emulateMedia({colorScheme: 'dark'});

    let releaseSvgRequest!: () => void;
    let resolveSvgRequestStarted!: () => void;
    const holdSvgRequest = new Promise<void>(resolve => {
      releaseSvgRequest = resolve;
    });
    const svgRequestStarted = new Promise<void>(resolve => {
      resolveSvgRequestStarted = resolve;
    });
    const svgResponse = page.waitForResponse(response =>
      response.url().includes('/images/home/hero-illustration.svg'),
    );

    await page.route('**/images/home/hero-illustration.svg', async route => {
      resolveSvgRequestStarted();
      await holdSvgRequest;
      await route.continue();
    });

    await page.goto('/', {waitUntil: 'domcontentloaded'});
    await expect(page.locator('html')).toHaveAttribute('data-theme', 'dark');
    await expect(page.locator('.hero-text-section')).toBeVisible();
    await svgRequestStarted;

    const fallbackImage = page.locator('img.hero-illustration-svg[src*="hero-illustration.png"]');
    await expect(fallbackImage).toHaveCount(0);

    releaseSvgRequest();
    await svgResponse;
  });
});
