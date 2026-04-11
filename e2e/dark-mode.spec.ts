import {test, expect, type Page} from '@playwright/test';

// Helper: color scheme을 설정하고 페이지 로드 후 테마 검증
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
});
