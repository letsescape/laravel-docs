import {test, expect} from '@playwright/test';

test.describe('Navigation', () => {
  test('navbar is visible with logo', async ({page}) => {
    await page.goto('/');
    const navbar = page.locator('nav.navbar');
    await expect(navbar).toBeVisible();

    const logo = navbar.locator('.navbar__logo img');
    await expect(logo).toBeVisible();
  });

  test('navbar contains docs link', async ({page}) => {
    await page.goto('/');
    const docsLink = page.locator('nav.navbar a.navbar__item', {hasText: /문서|Docs/});
    await expect(docsLink).toBeVisible();
  });

  test('clicking CTA button navigates to docs', async ({page}) => {
    await page.goto('/');
    const ctaButton = page.locator('a.button--primary', {hasText: /시작하기/});
    await ctaButton.click();
    await expect(page).toHaveURL(/\/docs\/12\.x/);
  });

  test('docs page loads with sidebar', async ({page}) => {
    await page.goto('/docs/12.x');
    const sidebar = page.locator('aside nav.menu, nav.menu');
    await expect(sidebar.first()).toBeVisible();
  });

  test('footer is visible on homepage', async ({page}) => {
    await page.goto('/');
    const footer = page.locator('footer');
    await expect(footer).toBeVisible();
  });
});
