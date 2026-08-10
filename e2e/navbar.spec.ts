import {test, expect, type Page, type Locator} from '@playwright/test';
import {docsPath} from './utils/docs-version';

// 로컬 사이트 대상 테스트(`playwright.config.ts`의 `baseURL` 사용)

// 헤더 컨트롤 정렬 검증의 허용 오차
const ORDER_TOLERANCE = 1; // 서브픽셀 반올림으로 인한 잘못된 순서 실패 판정 방지(px)
const VERTICAL_CENTER_TOLERANCE = 2; // 세로 중앙 정렬 허용 오차(px)

// 도우미: 모든 컨트롤의 표시 여부와 왼쪽→오른쪽 순서, 세로 중앙 정렬 검증
async function expectControlsAlignedLeftToRight(page: Page, controls: Locator[]) {
  for (const control of controls) {
    await expect(control).toBeVisible();
  }

  const boxes = await Promise.all(controls.map((control) => control.boundingBox()));
  const navbarBox = await page.locator('.navbar').boundingBox();
  expect(navbarBox).not.toBeNull();
  for (const box of boxes) {
    expect(box).not.toBeNull();
  }

  for (let index = 0; index < boxes.length - 1; index += 1) {
    expect(boxes[index]!.x + boxes[index]!.width).toBeLessThanOrEqual(boxes[index + 1]!.x + ORDER_TOLERANCE);
  }

  const navbarCenterY = navbarBox!.y + navbarBox!.height / 2;
  for (const box of boxes) {
    const controlCenterY = box!.y + box!.height / 2;
    expect(Math.abs(controlCenterY - navbarCenterY)).toBeLessThanOrEqual(VERTICAL_CENTER_TOLERANCE);
  }
}

// 도우미: `hover`와 `click` 간 간섭을 방지해 드롭다운 열기
async function openDropdown(page: Page, name: string) {
  const triggerId = `#trigger-${name}`;
  const contentId = `#content-${name}`;
  await page.locator(triggerId).click();
  // `hover` 간섭으로 닫혔을 수 있어 표시 상태 확인 후 재시도
  const visible = await page.locator(contentId).isVisible();
  if (!visible) {
    await page.locator(triggerId).click();
  }
  await expect(page.locator(contentId)).toBeVisible({timeout: 5000});
}

// 도우미: 모바일 오버레이에서 하위 메뉴를 열고 항목 검증
async function openMobileSubmenuAndVerify(page: Page, menuName: string, expectedItems: string[]) {
  await page.locator('.nav-mobile-hamburger').click();
  await page.locator('.nav-mobile-menu-item', {hasText: menuName}).first().click();
  await expect(page.locator('.nav-mobile-subitem', {hasText: expectedItems[0]}).first()).toBeVisible({timeout: 5000});
  for (const item of expectedItems) {
    await expect(page.locator('.nav-mobile-subitem', {hasText: item})).toBeVisible();
  }
}

// 도우미: 모바일 오버레이에서 직접 링크 검증
async function verifyMobileDirectLink(page: Page, linkText: string, expectedHref: string) {
  await page.locator('.nav-mobile-hamburger').click();
  const link = page.locator('a.nav-mobile-menu-item', {hasText: linkText});
  await expect(link).toBeVisible();
  await expect(link).toHaveAttribute('href', expectedHref);
}

async function expectTopRightMenuButton(page: Page, selector: string, viewportWidth: number) {
  const button = page.locator(selector).first();
  await expect(button).toBeVisible();

  const box = await button.boundingBox();
  const navbarBox = await page.locator('.navbar').boundingBox();
  expect(box).not.toBeNull();
  expect(navbarBox).not.toBeNull();
  expect(box!.x + box!.width).toBeGreaterThanOrEqual(viewportWidth - 48);
  expect(box!.x + box!.width).toBeGreaterThanOrEqual(navbarBox!.x + navbarBox!.width - 48);
  expect(box!.y).toBeGreaterThanOrEqual(navbarBox!.y);
  expect(box!.y + box!.height).toBeLessThanOrEqual(navbarBox!.y + navbarBox!.height);
}

async function expectDocsResponsiveHeaderControls(page: Page, viewportWidth: number) {
  const rightItems = page.locator('.navbar__items--right');
  // 모바일/태블릿 문서에서 CSS로 버전/언어 드롭다운 숨김(데스크톱 문서에서는 유지)
  await expect(rightItems.locator('.navbar-version-dropdown')).toBeHidden();
  await expect(rightItems.locator('.navbar-locale-dropdown')).toBeHidden();

  const controls = [
    rightItems.locator('.navbar-color-mode-toggle'),
    rightItems.locator('[class*="navbarSearchContainer"]'),
    page.locator('.navbar__items--right > .navbar__toggle'),
  ];

  await expectTopRightMenuButton(page, '.navbar__items--right > .navbar__toggle', viewportWidth);
  await expectControlsAlignedLeftToRight(page, controls);
}

async function expectLocaleIconHidden(page: Page) {
  const localeDropdown = page.locator('.navbar__items--right .navbar-locale-dropdown');
  await expect(localeDropdown).toBeVisible();
  await expect(localeDropdown.locator('> svg')).toBeHidden();
}

async function expectHomepageResponsiveHeaderControls(page: Page) {
  const rightItems = page.locator('.navbar__items--right');
  // 표시 문자열(13.x, 언어명) 대신 안정적인 클래스 훅으로 버전/언어 컨트롤 선택
  const controls = [
    page.locator('.nav-mobile-mode-toggle'),
    rightItems.locator('.navbar-version-dropdown').first(),
    rightItems.locator('.navbar-locale-dropdown').first(),
    rightItems.locator('[class*="navbarSearchContainer"]'),
    page.locator('.nav-mobile-hamburger'),
  ];

  await expectControlsAlignedLeftToRight(page, controls);
  await expectLocaleIconHidden(page);
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
    // 로캘에 따라 /ja/ 등의 접두사가 붙을 수 있음
    await expect(logoLink).toHaveAttribute('href', /^\//);
  });

  test('N-3: Framework 드롭다운 열기', async ({page}) => {
    await openDropdown(page, 'framework');
  });

  test('N-3a: Framework > Explore Laravel', async ({page}) => {
    await openDropdown(page, 'framework');
    await expect(page.locator('#content-framework').getByRole('heading', {name: 'Explore Laravel'})).toBeVisible();
  });

  test('N-3b: Framework > Latest packages', async ({page}) => {
    await openDropdown(page, 'framework');
    await expect(page.locator('#content-framework').getByRole('heading', {name: 'Latest packages'})).toBeVisible();
  });

  test('N-3c: Framework > Documentation', async ({page}) => {
    await openDropdown(page, 'framework');
    const menu = page.locator('#content-framework');
    await expect(menu.getByRole('heading', {name: 'Documentation'})).toBeVisible();
    for (const item of ['Installation', 'Agent Setup', 'Eloquent ORM', 'Artisan Console', 'Routing']) {
      await expect(menu.getByRole('link', {name: item})).toBeVisible();
    }
    await expect(menu.getByRole('link', {name: 'Installation'})).toHaveAttribute('href', docsPath());
  });

  test('N-3d: Framework > Starter kits', async ({page}) => {
    await openDropdown(page, 'framework');
    await expect(page.locator('#content-framework').getByRole('link', {name: /Starter kits/i})).toBeVisible();
  });

  test('N-4: Products 드롭다운 열기', async ({page}) => {
    await openDropdown(page, 'products');
  });

  test('N-5: 비활성 메뉴 미노출', async ({page}) => {
    await expect(page.locator('#trigger-resources')).toHaveCount(0);
    await expect(page.locator('#trigger-events')).toHaveCount(0);
  });

  test('N-7: Docs 링크', async ({page}) => {
    const docsLink = page.locator('.nav-docs-link');
    await expect(docsLink).toBeVisible();
    await expect(docsLink).toHaveAttribute('href', docsPath());
  });

  test('N-12: 네비바 상단 고정', async ({page}) => {
    await page.evaluate(() => window.scrollBy(0, 500));
    await expect(page.locator('.navbar')).toBeVisible();
  });

  test('N-13: 언어 드롭다운 아이콘 미노출', async ({page}) => {
    await expectLocaleIconHidden(page);
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

  test('N-14: 햄버거 표시, 드롭다운 숨김', async ({page}) => {
    await expect(page.locator('.nav-mobile-hamburger')).toBeVisible();
    await expect(page.locator('.nav-dropdown-triggers')).toBeHidden();
  });

  test('N-14a: 헤더 버튼 순서와 높이 정렬', async ({page}) => {
    await expectHomepageResponsiveHeaderControls(page);
  });

  test('N-15: 오버레이 열기/닫기', async ({page}) => {
    await expect(page.locator('.nav-mobile-hamburger')).toBeVisible();
    await page.locator('.nav-mobile-hamburger').click();
    await expect(page.locator('.nav-mobile-fullscreen')).toBeVisible();
    await page.locator('.nav-mobile-close').first().click();
    await expect(page.locator('.nav-mobile-fullscreen')).toBeHidden();
  });

  test('N-16: 비활성 메뉴 미노출', async ({page}) => {
    await expect(page.locator('.nav-mobile-hamburger')).toBeVisible();
    await page.locator('.nav-mobile-hamburger').click();
    await expect(page.locator('.nav-mobile-menu-item', {hasText: 'Resources'})).toHaveCount(0);
    await expect(page.locator('.nav-mobile-menu-item', {hasText: 'Events'})).toHaveCount(0);
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

  test('N-17a: 헤더 버튼 순서와 높이 정렬', async ({page}) => {
    await expectHomepageResponsiveHeaderControls(page);
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

  test('N-21: 비활성 모바일 메뉴 미노출', async ({page}) => {
    await page.locator('.nav-mobile-hamburger').click();
    await expect(page.locator('.nav-mobile-menu-item', {hasText: 'Resources'})).toHaveCount(0);
    await expect(page.locator('.nav-mobile-menu-item', {hasText: 'Events'})).toHaveCount(0);
  });

  test('N-23: Docs 직접 링크', async ({page}) => {
    await verifyMobileDirectLink(page, 'Docs', docsPath());
  });

  test('N-24: 서브메뉴 뒤로가기', async ({page}) => {
    await page.locator('.nav-mobile-hamburger').click();
    await page.locator('.nav-mobile-menu-item', {hasText: 'Framework'}).first().click();
    await expect(page.locator('.nav-mobile-subitem').first()).toBeVisible({timeout: 5000});
    await page.locator('.nav-mobile-back').click();
    await expect(page.locator('.nav-mobile-menu-item', {hasText: 'Framework'}).first()).toBeVisible({timeout: 5000});
  });

  test('N-25: 다크모드 토글', async ({page}) => {
    await expect(page.locator('.nav-mobile-mode-toggle')).toBeVisible();
  });
});

// =============================================================================
// 문서 페이지 반응형 사이드바
// =============================================================================
test.describe('Navbar — Docs responsive menu', () => {
  test('N-26: 태블릿에서 우측 상단 햄버거 표시', async ({page}) => {
    await page.setViewportSize({width: 768, height: 1024});
    await page.goto(docsPath());
    await expectDocsResponsiveHeaderControls(page, 768);
  });

  test('N-27: 모바일에서 우측 상단 햄버거 표시', async ({page}) => {
    await page.setViewportSize({width: 430, height: 932});
    await page.goto(docsPath());
    await expectDocsResponsiveHeaderControls(page, 430);
  });

  test('N-28: 문서 햄버거 클릭 시 사이드바 열림', async ({page}) => {
    await page.setViewportSize({width: 430, height: 932});
    await page.goto(docsPath());
    await expectDocsResponsiveHeaderControls(page, 430);
    await page.locator('.navbar__items--right > .navbar__toggle').click();
    await expect(page.locator('.navbar-sidebar--show')).toBeVisible();
  });

  test('N-29: 좁은 모바일에서도 헤더 버튼 순서 유지', async ({page}) => {
    await page.setViewportSize({width: 390, height: 844});
    await page.goto(docsPath());
    await expectDocsResponsiveHeaderControls(page, 390);
  });

  test('N-30: 데스크톱 문서에서 버전/언어 컨트롤 노출', async ({page}) => {
    await page.setViewportSize({width: 1280, height: 800});
    await page.goto(docsPath());
    const rightItems = page.locator('.navbar__items--right');
    await expect(rightItems.locator('.navbar-version-dropdown')).toBeVisible();
    await expect(rightItems.locator('.navbar-locale-dropdown')).toBeVisible();
  });
});
