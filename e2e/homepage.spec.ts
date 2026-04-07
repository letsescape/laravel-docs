import {test, expect} from '@playwright/test';

// 로컬 사이트를 대상으로 테스트 (playwright.config.ts의 baseURL 사용)

// =============================================================================
// 데스크톱 (1280px)
// =============================================================================
test.describe('Homepage — Desktop (1280px)', () => {
  test.use({viewport: {width: 1280, height: 800}});

  test.beforeEach(async ({page}) => {
    await page.goto('/');
  });

  test('H-1: 메인 헤드라인', async ({page}) => {
    const h1 = page.getByRole('heading', {level: 1});
    await expect(h1).toContainText('Artisans and agents');
  });

  test('H-2: 서브 텍스트', async ({page}) => {
    await expect(page.getByText('batteries-included')).toBeVisible();
  });

  test('H-3: View framework docs 버튼', async ({page}) => {
    const link = page.locator('.hero-btn-secondary, .hero-btn-primary').first();
    await expect(link).toBeVisible();
  });

  test('AF-1: AI Framework 섹션 헤딩', async ({page}) => {
    await expect(page.getByRole('heading', {level: 2, name: /Ship web apps with the/})).toBeVisible();
  });

  test('FD-1: 프레임워크 상세 헤딩', async ({page}) => {
    await expect(page.getByRole('heading', {level: 3, name: /framework for developers and agents/})).toBeVisible();
  });

  test('FD-4: 코드 카테고리 탭', async ({page}) => {
    for (const cat of ['Auth', 'AI SDK', 'ORM']) {
      await expect(page.getByRole('button', {name: cat, exact: true})).toBeAttached();
    }
  });

  test('CL-1: Laravel Cloud 섹션', async ({page}) => {
    await expect(page.getByRole('heading', {level: 3, name: /Laravel Cloud takes you from local to live/})).toBeVisible();
  });

  test('NW-1: Nightwatch 섹션', async ({page}) => {
    await expect(page.getByRole('heading', {level: 3, name: /Monitor and fix issues with Nightwatch/})).toBeVisible();
  });

  test('FE-1: Frontend 섹션', async ({page}) => {
    await expect(page.getByRole('heading', {level: 3, name: /The best partner to any front-end/})).toBeVisible();
  });

  test('CT-1: CTA 섹션', async ({page}) => {
    await expect(page.getByRole('heading', {level: 2, name: /Create without limits/})).toBeVisible();
  });

  test('E-1: Events 섹션', async ({page}) => {
    await expect(page.getByRole('heading', {level: 2, name: /We.ll see you in/})).toBeVisible();
  });

  test('FT-1: 푸터', async ({page}) => {
    await expect(page.locator('.hp-footer')).toBeVisible();
  });

  test('FT-2: 푸터 컬럼', async ({page}) => {
    for (const col of ['Products', 'Packages', 'Resources', 'Partners']) {
      await expect(page.locator('.hp-footer').getByText(col).first()).toBeAttached();
    }
  });
});

// =============================================================================
// 태블릿 (768px)
// =============================================================================
test.describe('Homepage — Tablet (768px)', () => {
  test.use({viewport: {width: 768, height: 1024}});

  test.beforeEach(async ({page}) => {
    await page.goto('/');
  });

  test('HR-1: 가로 스크롤 없음', async ({page}) => {
    const scrollWidth = await page.evaluate(() => document.documentElement.scrollWidth);
    expect(scrollWidth).toBeLessThanOrEqual(768);
  });

  test('HR-2: 히어로 텍스트 표시', async ({page}) => {
    await expect(page.getByRole('heading', {level: 1})).toBeVisible();
  });
});

// =============================================================================
// 모바일 (430px)
// =============================================================================
test.describe('Homepage — Mobile (430px)', () => {
  test.use({viewport: {width: 430, height: 932}});

  test.beforeEach(async ({page}) => {
    await page.goto('/');
  });

  test('HR-3: 히어로 텍스트 오버플로우 없음', async ({page}) => {
    const h1 = page.getByRole('heading', {level: 1});
    await expect(h1).toBeVisible();
    const box = await h1.boundingBox();
    expect(box!.x).toBeGreaterThanOrEqual(0);
    expect(box!.x + box!.width).toBeLessThanOrEqual(430);
  });

  test('HR-4: CTA 버튼 표시', async ({page}) => {
    await expect(page.locator('.hero-btn-secondary, .hero-btn-primary').first()).toBeVisible();
  });

  test('HR-5: 가로 스크롤 없음', async ({page}) => {
    const scrollWidth = await page.evaluate(() => document.documentElement.scrollWidth);
    expect(scrollWidth).toBeLessThanOrEqual(430);
  });
});
