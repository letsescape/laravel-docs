import {test, expect} from '@playwright/test';

test.describe('Homepage', () => {
  test.beforeEach(async ({page}) => {
    await page.goto('/');
  });

  test('page loads with correct title', async ({page}) => {
    await expect(page).toHaveTitle(/Laravel/);
  });

  test('hero section is visible', async ({page}) => {
    const hero = page.locator('main section').first();
    await expect(hero).toBeVisible();
  });

  test('hero section contains Laravel SVG logo', async ({page}) => {
    const svgLogo = page.locator('.hero-svg-logo svg');
    await expect(svgLogo).toBeVisible();
  });

  test('hero section contains call-to-action button', async ({page}) => {
    const ctaButton = page.locator('a.button--primary', {hasText: /시작하기/});
    await expect(ctaButton).toBeVisible();
    await expect(ctaButton).toHaveAttribute('href', /\/docs\/12\.x/);
  });

  test('hero section displays code snippet', async ({page}) => {
    const codeBlock = page.locator('pre code').first();
    await expect(codeBlock).toBeVisible();
    await expect(codeBlock).toContainText('composer global require laravel/installer');
    await expect(codeBlock).toContainText('laravel new example-app');
  });

  test('features/ecosystem section is visible', async ({page}) => {
    const ecosystemTitle = page.getByRole('heading', {name: '생태계', exact: true});
    await expect(ecosystemTitle).toBeVisible();
  });

  test('features section displays packages', async ({page}) => {
    const scoutPackage = page.getByText('Scout');
    await expect(scoutPackage).toBeVisible();

    const octanePackage = page.getByText('Octane');
    await expect(octanePackage).toBeVisible();
  });

  test('features section displays starter kits', async ({page}) => {
    const reactKit = page.getByText('React 스타터 킷');
    await expect(reactKit).toBeVisible();

    const vueKit = page.getByText('Vue 스타터 킷');
    await expect(vueKit).toBeVisible();

    const livewireKit = page.getByText('Livewire 스타터 킷');
    await expect(livewireKit).toBeVisible();
  });

  test('code examples section is visible', async ({page}) => {
    const codeExamples = page.locator('main section').nth(2);
    await expect(codeExamples).toBeVisible();
  });
});
