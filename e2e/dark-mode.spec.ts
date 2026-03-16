import {test, expect} from '@playwright/test';

test.describe('Dark mode', () => {
  test('page loads with a color theme attribute', async ({page}) => {
    await page.goto('/');
    const html = page.locator('html');
    const theme = await html.getAttribute('data-theme');
    expect(['dark', 'light']).toContain(theme);
  });

  test('color mode toggle button exists', async ({page}) => {
    await page.goto('/');
    const toggleButton = page.locator('button[class*="toggleButton"]');
    await expect(toggleButton).toBeVisible();
  });

  test('clicking toggle cycles through themes', async ({page}) => {
    await page.goto('/');
    const html = page.locator('html');
    const toggleButton = page.locator('button[class*="toggleButton"]');

    // Click and check we can reach dark mode
    await toggleButton.click();
    await page.waitForTimeout(300);
    const themeAfterFirstClick = await html.getAttribute('data-theme');

    await toggleButton.click();
    await page.waitForTimeout(300);
    const themeAfterSecondClick = await html.getAttribute('data-theme');

    // Verify both themes are valid and at least one transition produces a different theme
    expect(['dark', 'light']).toContain(themeAfterFirstClick);
    expect(['dark', 'light']).toContain(themeAfterSecondClick);
    expect(themeAfterFirstClick).not.toBe(themeAfterSecondClick);
  });

  test('dark mode can be activated via color scheme emulation', async ({page}) => {
    await page.emulateMedia({colorScheme: 'dark'});
    await page.goto('/');
    const html = page.locator('html');
    await expect(html).toHaveAttribute('data-theme', 'dark');
  });

  test('light mode can be activated via color scheme emulation', async ({page}) => {
    await page.emulateMedia({colorScheme: 'light'});
    await page.goto('/');
    const html = page.locator('html');
    await expect(html).toHaveAttribute('data-theme', 'light');
  });
});
