import {test, expect} from '@playwright/test';

// 로컬 사이트를 대상으로 테스트 (playwright.config.ts의 baseURL 사용)

// Helper: 드롭다운을 확실하게 열기 (hover+click 간섭 방지)
async function openDropdown(page: any, name: string) {
  const triggerId = `#trigger-${name}`;
  const contentId = `#content-${name}`;
  await page.locator(triggerId).click();
  // hover 간섭으로 닫혔을 수 있으므로 확인 후 재시도
  const visible = await page.locator(contentId).isVisible().catch(() => false);
  if (!visible) {
    await page.locator(triggerId).click();
  }
  await expect(page.locator(contentId)).toBeVisible({timeout: 5000});
}

// Helper: 모바일 오버레이에서 서브메뉴 열고 항목 검증
async function openMobileSubmenuAndVerify(page: any, menuName: string, expectedItems: string[]) {
  await page.locator('.nav-mobile-hamburger').click();
  await page.locator('.nav-mobile-menu-item', {hasText: menuName}).first().click();
  await page.waitForTimeout(400);
  for (const item of expectedItems) {
    await expect(page.locator('.nav-mobile-subitem', {hasText: item})).toBeVisible();
  }
}

// Helper: 모바일 오버레이에서 직접 링크 검증
async function verifyMobileDirectLink(page: any, linkText: string, expectedHref: string) {
  await page.locator('.nav-mobile-hamburger').click();
  const link = page.locator('a.nav-mobile-menu-item', {hasText: linkText});
  await expect(link).toBeVisible();
  await expect(link).toHaveAttribute('href', expectedHref);
}

// =============================================================================
// 데스크톱 (1280px)
// =============================================================================
test.describe('Navbar — Desktop (1280px)', () => {
  test.use({viewport: {width: 1280, height: 800}});

  test.beforeEach(async ({page}) => {
    await page.goto('/');
  });

  test('N-1: 네비바 표시', async ({page}) => {
    await expect(page.locator('.navbar')).toBeVisible();
  });

  test('N-2: 로고 표시 및 링크', async ({page}) => {
    const logoLink = page.locator('.navbar__brand').first();
    await expect(logoLink).toBeVisible();
    // 로캘에 따라 /ja/ 등 prefix가 붙을 수 있음
    await expect(logoLink).toHaveAttribute('href', /^\//);
  });

  test('N-3: Framework 드롭다운 열기', async ({page}) => {
    await openDropdown(page, 'framework');
  });

  test('N-3a: Framework > Explore Laravel', async ({page}) => {
    await openDropdown(page, 'framework');
    const menu = page.locator('#content-framework');
    await expect(menu.getByRole('heading', {name: 'Explore Laravel'})).toBeVisible();
  });

  test('N-3b: Framework > Latest packages', async ({page}) => {
    await openDropdown(page, 'framework');
    const menu = page.locator('#content-framework');
    await expect(menu.getByRole('heading', {name: 'Latest packages'})).toBeVisible();
  });

  test('N-3c: Framework > Documentation', async ({page}) => {
    await openDropdown(page, 'framework');
    const menu = page.locator('#content-framework');
    await expect(menu.getByRole('heading', {name: 'Documentation'})).toBeVisible();
    for (const item of ['Installation', 'Agent Setup', 'Eloquent ORM', 'Artisan Console', 'Routing']) {
      await expect(menu.getByRole('link', {name: item})).toBeVisible();
    }
  });

  test('N-3d: Framework > Starter kits', async ({page}) => {
    await openDropdown(page, 'framework');
    const menu = page.locator('#content-framework');
    await expect(menu.getByRole('link', {name: /Starter kits/i})).toBeVisible();
  });

  test('N-4: Products 드롭다운 열기', async ({page}) => {
    await openDropdown(page, 'products');
  });

  test('N-5: Resources 드롭다운 열기', async ({page}) => {
    await openDropdown(page, 'resources');
  });

  test('N-6: Events 드롭다운 열기', async ({page}) => {
    await openDropdown(page, 'events');
  });

  test('N-7: Docs 링크', async ({page}) => {
    const docsLink = page.locator('.nav-docs-link');
    await expect(docsLink).toBeVisible();
    await expect(docsLink).toHaveAttribute('href', '/docs');
  });

  test('N-12: 네비바 상단 고정', async ({page}) => {
    await page.evaluate(() => window.scrollBy(0, 500));
    await expect(page.locator('.navbar')).toBeVisible();
  });
});

// =============================================================================
// 태블릿 (768px)
// =============================================================================
test.describe('Navbar — Tablet (768px)', () => {
  test.use({viewport: {width: 768, height: 1024}});

  test.beforeEach(async ({page}) => {
    await page.goto('/');
  });

  test('N-14: 메뉴 항목 표시', async ({page}) => {
    for (const name of ['framework', 'products', 'resources', 'events']) {
      await expect(page.locator(`#trigger-${name}`)).toBeVisible();
    }
  });

  test('N-15: 햄버거 숨김', async ({page}) => {
    await expect(page.locator('.nav-mobile-hamburger')).toBeHidden();
  });

  test('N-16: 드롭다운 열기', async ({page}) => {
    await openDropdown(page, 'framework');
  });
});

// =============================================================================
// 모바일 (430px)
// =============================================================================
test.describe('Navbar — Mobile (430px)', () => {
  test.use({viewport: {width: 430, height: 932}});

  test.beforeEach(async ({page}) => {
    await page.goto('/');
  });

  test('N-17: 햄버거 표시, 드롭다운 숨김', async ({page}) => {
    await expect(page.locator('.navbar__brand').first()).toBeVisible();
    await expect(page.locator('.nav-mobile-hamburger')).toBeVisible();
    await expect(page.locator('.nav-dropdown-triggers')).toBeHidden();
  });

  test('N-18: 오버레이 열기/닫기', async ({page}) => {
    await page.locator('.nav-mobile-hamburger').click();
    await expect(page.locator('.nav-mobile-fullscreen')).toBeVisible();
    await page.locator('.nav-mobile-close').first().click();
    await expect(page.locator('.nav-mobile-fullscreen')).toBeHidden();
  });

  test('N-19: Framework 서브메뉴', async ({page}) => {
    await openMobileSubmenuAndVerify(page, 'Framework', ['Overview', 'Starter Kits', 'Release Notes', 'Documentation', 'Laravel Learn']);
  });

  test('N-20: Products 서브메뉴', async ({page}) => {
    await openMobileSubmenuAndVerify(page, 'Products', ['Laravel Cloud', 'Forge', 'Nightwatch', 'Nova']);
  });

  test('N-21: Resources 서브메뉴', async ({page}) => {
    await openMobileSubmenuAndVerify(page, 'Resources', ['Blog', 'Partners', 'Careers', 'Trust', 'Legal', 'Status']);
  });

  test('N-22: Events 직접 링크', async ({page}) => {
    await verifyMobileDirectLink(page, 'Events', '/community');
  });

  test('N-23: Docs 직접 링크', async ({page}) => {
    await verifyMobileDirectLink(page, 'Docs', '/docs');
  });

  test('N-24: 서브메뉴 뒤로가기', async ({page}) => {
    await page.locator('.nav-mobile-hamburger').click();
    await page.locator('.nav-mobile-menu-item', {hasText: 'Framework'}).first().click();
    await page.waitForTimeout(400);
    await page.locator('.nav-mobile-back').click();
    await page.waitForTimeout(400);
    await expect(page.locator('.nav-mobile-menu-item', {hasText: 'Framework'}).first()).toBeVisible();
  });

  test('N-25: 다크모드 토글', async ({page}) => {
    await expect(page.locator('.nav-mobile-mode-toggle')).toBeVisible();
  });
});
