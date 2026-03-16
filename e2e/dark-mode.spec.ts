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

  test('clicking toggle changes the theme', async ({page}) => {
    // Emulate dark mode as initial state for deterministic testing
    await page.emulateMedia({colorScheme: 'dark'});
    await page.goto('/');
    const html = page.locator('html');
    await expect(html).toHaveAttribute('data-theme', 'dark');

    const toggleButton = page.locator('button[class*="toggleButton"]');
    await toggleButton.click();

    // After clicking, the theme should switch to light
    await expect(html).toHaveAttribute('data-theme', 'light');
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
