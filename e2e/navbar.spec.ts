import {test, expect, type Page, type Locator} from '@playwright/test';
import {docsPath, docsPathForVersion, latestDocsVersion} from './utils/docs-version';

// 로컬 사이트 대상 테스트(`playwright.config.ts`의 `baseURL` 사용)

// 헤더 컨트롤 정렬 검증의 허용 오차
const ORDER_TOLERANCE = 1; // 서브픽셀 반올림으로 인한 잘못된 순서 실패 판정 방지(px)
const VERTICAL_CENTER_TOLERANCE = 2; // 세로 중앙 정렬 허용 오차(px)

// 도우미: 컨트롤의 표시 여부, DOM 순서, 8px 간격과 같은 행 정렬 검증
async function expectControlsAlignedLeftToRight(page: Page, controls: Locator[]) {
  for (const control of controls) {
    await expect(control).toBeVisible();
  }

  const boxes = await Promise.all(controls.map((control) => control.boundingBox()));
  for (const box of boxes) {
    expect(box).not.toBeNull();
    expect(box!.x).toBeGreaterThanOrEqual(0);
    expect(box!.x + box!.width).toBeLessThanOrEqual(page.viewportSize()!.width + ORDER_TOLERANCE);
  }

  for (let index = 0; index < boxes.length - 1; index += 1) {
    const gap = boxes[index + 1]!.x - boxes[index]!.x - boxes[index]!.width;
    expect(Math.abs(gap - 8)).toBeLessThanOrEqual(ORDER_TOLERANCE);
    expect(await controls[index].evaluate(
      (element, next) => Boolean(next && (element.compareDocumentPosition(next) & Node.DOCUMENT_POSITION_FOLLOWING)),
      await controls[index + 1].elementHandle(),
    )).toBe(true);
  }

  const rowCenterY = boxes[0]!.y + boxes[0]!.height / 2;
  for (const box of boxes) {
    const controlCenterY = box!.y + box!.height / 2;
    expect(Math.abs(controlCenterY - rowCenterY)).toBeLessThanOrEqual(VERTICAL_CENTER_TOLERANCE);
  }
}

async function expectHeaderControlsUncovered(page: Page, selectors: string[]) {
  await expect.poll(() => page.evaluate((controlSelectors) => {
    const controls = controlSelectors.map((selector) =>
      [...document.querySelectorAll<HTMLElement>(selector)].find((element) => element.getBoundingClientRect().width > 0)!,
    );
    const boxes = controls.map((element) => element.getBoundingClientRect());
    const navbar = document.querySelector<HTMLElement>('.navbar')!;
    const navbarBox = navbar.getBoundingClientRect();
    const navbarFits = navbar.scrollWidth <= navbar.clientWidth &&
      navbarBox.left >= 0 && navbarBox.right <= window.innerWidth;
    return navbarFits && controls.every((element, index) => {
      const box = boxes[index];
      const target = element.closest('a, button') ?? element;
      const hit = document.elementFromPoint(box.x + box.width / 2, box.y + box.height / 2);
      const overlaps = boxes.some((other, otherIndex) => otherIndex !== index &&
        Math.min(box.right, other.right) - Math.max(box.left, other.left) > 1 &&
        Math.min(box.bottom, other.bottom) - Math.max(box.top, other.top) > 1,
      );
      return box.left >= 0 && box.right <= window.innerWidth && target.contains(hit) && !overlaps;
    });
  }, selectors)).toBe(true);
}

// 도우미: `hover`와 `click` 간 간섭을 방지해 드롭다운 열기
async function openDropdown(page: Page, name: string) {
  const triggerId = `#trigger-${name}`;
  const contentId = `#content-${name}`;
  await expect(page.locator('html')).toHaveAttribute('data-has-hydrated', 'true');
  await page.locator(triggerId).click();
  // `hover` 간섭으로 닫혔을 수 있어 표시 상태 확인 후 재시도
  const visible = await page.locator(contentId).isVisible();
  if (!visible) {
    await page.locator(triggerId).click();
  }
  await expect(page.locator(contentId)).toBeVisible({timeout: 5000});
  await page.locator(contentId).evaluate(async (element) => {
    await Promise.all(element.getAnimations({subtree: true}).map((animation) => animation.finished));
  });
  const panelBox = await page.locator(contentId).boundingBox();
  const triggerBox = await page.locator(triggerId).boundingBox();
  expect(panelBox!.y).toBeGreaterThanOrEqual(triggerBox!.y + triggerBox!.height - ORDER_TOLERANCE);
  expect(panelBox!.x).toBeGreaterThanOrEqual(-ORDER_TOLERANCE);
  expect(panelBox!.x + panelBox!.width).toBeLessThanOrEqual(page.viewportSize()!.width + ORDER_TOLERANCE);
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
  const controls = [
    rightItems.locator('.navbar-color-mode-toggle > button'),
    rightItems.locator('.navbar-version-dropdown'),
    rightItems.locator('.navbar-locale-dropdown'),
    rightItems.locator('.DocSearch-Button'),
    page.locator('.navbar__items--right > .navbar__toggle'),
  ];

  await expectTopRightMenuButton(page, '.navbar__items--right > .navbar__toggle', viewportWidth);
  await expectControlsAlignedLeftToRight(page, controls);
}

async function expectLocaleIconHidden(page: Page) {
  const localeDropdown = page.locator('.navbar__items--right .navbar-locale-dropdown');
  await expect(localeDropdown).toBeVisible();
  await expect(localeDropdown.locator('svg')).toBeHidden();
}

async function expectVersionLabel(control: Locator, version: string, compact: boolean, locale: string) {
  const versionName = version === 'master' ? `dev / master (${locale === 'ja' ? '開発版' : '개발 버전'})` : version;
  const accessibleName = `${locale === 'ja' ? 'ドキュメントのバージョン' : '문서 버전'}: ${versionName}`;
  await expect(control).toHaveAccessibleName(accessibleName);
  await expect(control).toHaveAttribute('title', accessibleName);
  const fullLabel = control.locator('.navbar-version-label');
  const compactLabel = control.locator('.navbar-version-code');
  if (compact) {
    await expect(compactLabel).toBeVisible();
    await expect(compactLabel).toHaveText(version === 'master' ? 'dev' : version.replace(/\.x$/, ''));
    await expect(fullLabel).toBeHidden();
  } else {
    await expect(fullLabel).toBeVisible();
    await expect(fullLabel).toHaveText(version);
    await expect(compactLabel).toBeHidden();
  }
}

async function expectHomepageResponsiveHeaderControls(page: Page) {
  const rightItems = page.locator('.navbar__items--right');
  // 표시 문자열(13.x, 언어명) 대신 안정적인 클래스 훅으로 버전/언어 컨트롤 선택
  const controls = [
    rightItems.locator('.navbar-color-mode-toggle > button'),
    rightItems.locator('.navbar-version-dropdown').first(),
    rightItems.locator('.navbar-locale-dropdown').first(),
    rightItems.locator('.DocSearch-Button'),
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
    await expect(menu.getByRole('link', {name: 'Installation'})).toHaveAttribute('href', `${docsPath()}/`);
  });

  test('N-3d: Framework > Starter kits', async ({page}) => {
    await openDropdown(page, 'framework');
    await expect(page.locator('#content-framework').getByRole('link', {name: /Starter kits/i})).toBeVisible();
  });

  test('N-4: Products 드롭다운 열기', async ({page}) => {
    await page.setViewportSize({width: 1024, height: 800});
    await openDropdown(page, 'products');
  });

  test('N-5: 비활성 메뉴 미노출', async ({page}) => {
    await expect(page.locator('#trigger-resources')).toHaveCount(0);
    await expect(page.locator('#trigger-events')).toHaveCount(0);
  });

  test('N-7: Docs 링크', async ({page}) => {
    const docsLink = page.locator('.nav-docs-link');
    await expect(docsLink).toBeVisible();
    await expect(docsLink).toHaveAttribute('href', `${docsPath()}/`);
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
    await verifyMobileDirectLink(page, 'Docs', `${docsPath()}/`);
  });

  test('N-24: 서브메뉴 뒤로가기', async ({page}) => {
    await page.locator('.nav-mobile-hamburger').click();
    await page.locator('.nav-mobile-menu-item', {hasText: 'Framework'}).first().click();
    await expect(page.locator('.nav-mobile-subitem').first()).toBeVisible({timeout: 5000});
    await page.locator('.nav-mobile-back').click();
    await expect(page.locator('.nav-mobile-menu-item', {hasText: 'Framework'}).first()).toBeVisible({timeout: 5000});
  });

  test('N-25: 다크모드 토글', async ({page}) => {
    await expect(page.locator('.navbar-color-mode-toggle > button')).toBeVisible();
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
    await expect(page.locator('.navbar-sidebar--show .navbar-sidebar')).toBeVisible();
  });

  test('N-29: 좁은 모바일에서도 헤더 버튼 순서 유지', async ({page}) => {
    await page.setViewportSize({width: 390, height: 844});
    await page.goto(docsPath());
    await expectDocsResponsiveHeaderControls(page, 390);
  });

  for (const width of [997, 1024, 1279, 1280]) {
    test(`N-30: ${width}px 문서에서 버전/언어 컨트롤 노출`, async ({page}) => {
      await page.setViewportSize({width, height: 800});
      await page.goto(docsPath());
      await expect(page.locator('html')).toHaveAttribute('data-has-hydrated', 'true');
      const rightItems = page.locator('.navbar__items--right');
      await expect(rightItems.locator('.navbar-version-dropdown')).toBeVisible();
      await expect(rightItems.locator('.navbar-locale-dropdown')).toBeVisible();
      await expect(rightItems.locator('.navbar__toggle')).toBeHidden();
    });
  }

  test('N-31: 996px 메뉴를 연 뒤 화면을 확대해도 닫고 다시 열 수 있음', async ({page}) => {
    await page.setViewportSize({width: 996, height: 800});
    await page.goto(docsPath());
    await expect(page.locator('html')).toHaveAttribute('data-has-hydrated', 'true');
    const toggle = page.locator('.navbar__items--right > .navbar__toggle');
    await toggle.click();
    await expect(page.locator('.navbar-sidebar--show .navbar-sidebar')).toBeVisible();

    await page.setViewportSize({width: 997, height: 800});
    await expect(page.locator('.navbar-sidebar--show')).toHaveCount(0);
    await expect(toggle).toBeHidden();
    await expect(page.locator('body')).not.toHaveCSS('overflow', 'hidden');

    await page.setViewportSize({width: 996, height: 800});
    await toggle.click();
    await expect(page.locator('.navbar-sidebar--show .navbar-sidebar')).toBeVisible();
    await page.locator('.navbar-sidebar__close').click();
    await expect(page.locator('.navbar-sidebar--show')).toHaveCount(0);
  });
});

test.describe('Navbar — Narrow homepage', () => {
  for (const width of [320, 360, 390]) {
    for (const version of [latestDocsVersion, 'master']) {
      test(`N-32: ${width}px 홈 ${version}에서 로고와 컨트롤이 겹치지 않음`, async ({page}) => {
        await page.goto('/');
        await expect(page.locator('html')).toHaveAttribute('data-has-hydrated', 'true');
        const versionControl = page.locator('.navbar__items--right .navbar-version-dropdown');
        if (version !== latestDocsVersion) {
          await versionControl.click();
          await page.locator('.navbar__items--right').getByRole('link', {name: 'master (개발 버전)', exact: true}).click();
          await page.locator('.navbar__brand').first().click();
        }
        await page.setViewportSize({width, height: 844});
        await page.evaluate(() => document.fonts.ready);
        await expectVersionLabel(versionControl, version, true, 'ko');
        await expectHomepageResponsiveHeaderControls(page);

        const logo = page.locator('.navbar__brand').first().locator('img:visible');
        await expectHeaderControlsUncovered(page, [
          '.navbar__brand img', '.navbar-color-mode-toggle > button', '.navbar-version-dropdown',
          '.navbar-locale-dropdown', '.DocSearch-Button', '.nav-mobile-hamburger',
        ]);
        const logoUncovered = await logo.evaluate((element) => {
          const box = element.getBoundingClientRect();
          return [0.1, 0.5, 0.9].every((position) =>
            element.closest('a')?.contains(document.elementFromPoint(box.x + box.width * position, box.y + box.height / 2)),
          );
        });
        expect(logoUncovered).toBe(true);
      });
    }
  }
});

test.describe('Navbar — Consistent control spacing', () => {
  for (const {locale, prefix, label, code} of [
    {locale: 'ko', prefix: '', label: '한국어', code: 'KO'},
    {locale: 'ja', prefix: '/ja', label: '日本語', code: 'JA'},
  ]) {
    for (const route of ['home', 'docs']) {
      test(`${locale} ${route} controls keep their order, spacing, and compact labels`, async ({page}) => {
        await page.goto(route === 'home' ? `${prefix}/` : `${prefix}${docsPath()}/`);
        await expect(page.locator('html')).toHaveAttribute('data-has-hydrated', 'true');
        const rightItems = page.locator('.navbar__items--right');
        const colorMode = rightItems.locator('.navbar-color-mode-toggle > button');
        const version = rightItems.locator('.navbar-version-dropdown');
        const language = rightItems.locator('.navbar-locale-dropdown');
        const search = rightItems.locator('.DocSearch-Button');
        const menu = rightItems.locator(route === 'home' ? '.nav-mobile-hamburger' : '.navbar__toggle');

        for (const width of [320, 390, 768, 997, 1023, 1024, 1280]) {
          await test.step(`${width}px`, async () => {
            await page.setViewportSize({width, height: 900});
            await page.evaluate(() => document.fonts.ready);
            const compact = width < 1024;
            const showMenu = route === 'home' ? compact : width <= 996;
            const controls = [colorMode, version, language, search, ...(showMenu ? [menu] : [])];
            await expectControlsAlignedLeftToRight(page, controls);
            await expectVersionLabel(version, latestDocsVersion, compact, locale);

            const navbar = page.locator('.navbar');
            await expect(navbar).toHaveCSS('padding-left', '18px');
            await expect(navbar).toHaveCSS('padding-right', '18px');
            await expect(page.locator('.navbar__inner')).toHaveCSS('padding-left', '0px');
            await expect(page.locator('.navbar__inner')).toHaveCSS('padding-right', '0px');
            await expect(page.locator('.navbar__inner')).toHaveCSS('max-width', '1280px');
            await expect(page.locator('.navbar__brand').first().locator('img:visible')).toHaveCSS('height', '20px');
            if (width >= 390) {
              await expect(navbar).toHaveCSS('height', '64px');
            }

            if (showMenu) {
              await expect(menu).toBeVisible();
              const buttonBox = (await menu.boundingBox())!;
              const iconBox = (await menu.locator('svg').boundingBox())!;
              expect(Math.abs(buttonBox.x + buttonBox.width / 2 - iconBox.x - iconBox.width / 2)).toBeLessThanOrEqual(1);
              expect(Math.abs(buttonBox.y + buttonBox.height / 2 - iconBox.y - iconBox.height / 2)).toBeLessThanOrEqual(1);
            } else {
              await expect(menu).toBeHidden();
            }
            if (route === 'home') {
              if (compact) {
                await expect(page.locator('.nav-dropdown-triggers')).toBeHidden();
              } else {
                await expect(page.locator('.nav-dropdown-triggers')).toBeVisible();
              }
            }

            if (compact) {
              await expect(search.locator('.DocSearch-Button-Placeholder')).toBeHidden();
              await expect(search.locator('.DocSearch-Button-Keys')).toBeHidden();
              expect((await search.boundingBox())!.width).toBeLessThanOrEqual(32 + ORDER_TOLERANCE);
            } else {
              await expect(search.locator('.DocSearch-Button-Placeholder')).toBeVisible();
              expect((await search.boundingBox())!.width).toBeGreaterThan(32);
            }

            await expect(language).toHaveAccessibleName(label);
            if (compact) {
              await expect(language.locator('.navbar-locale-code')).toBeVisible();
              await expect(language.locator('.navbar-locale-code')).toHaveText(code);
              await expect(language.locator('.navbar-locale-label')).toBeHidden();
            } else {
              await expect(language.locator('.navbar-locale-label')).toBeVisible();
              await expect(language.locator('.navbar-locale-label')).toHaveText(label);
              await expect(language.locator('.navbar-locale-code')).toBeHidden();
            }

            if (width === 1023) {
              await language.click();
              const dropdown = language.locator('..');
              await expect(dropdown.getByRole('link', {name: '한국어', exact: true})).toBeVisible();
              await expect(dropdown.getByRole('link', {name: '日本語', exact: true})).toBeVisible();
              await page.mouse.move(0, 0);
              await language.press('Escape');
            }
          });
        }

        await version.click();
        const versionDropdown = version.locator('..');
        await expect(versionDropdown.getByRole('link', {name: latestDocsVersion, exact: true})).toBeVisible();
        const master = versionDropdown.getByRole('link', {
          name: locale === 'ja' ? 'master (開発版)' : 'master (개발 버전)',
          exact: true,
        });
        await expect(master).toHaveAttribute('href', `${prefix}${docsPathForVersion('master')}/`);
        await master.click();
        await expect(page).toHaveURL(new RegExp(`${prefix}${docsPathForVersion('master')}/?$`));
        if (route === 'home') {
          await page.locator('.navbar__brand').first().click();
          await expect(page).toHaveURL((url) => url.pathname === `${prefix}/`);
        }

        for (const width of [320, 390, 1023, 1024]) {
          await test.step(`master ${width}px`, async () => {
            await page.setViewportSize({width, height: 900});
            const compact = width < 1024;
            const showMenu = route === 'home' ? compact : width <= 996;
            await expectVersionLabel(version, 'master', compact, locale);
            await expectControlsAlignedLeftToRight(page, [colorMode, version, language, search, ...(showMenu ? [menu] : [])]);
          });
        }

        await version.click();
        await versionDropdown.getByRole('link', {name: latestDocsVersion, exact: true}).click();
        await expect(page).toHaveURL(new RegExp(`${prefix}${docsPath().replaceAll('.', '\\.')}/?$`));
        if (route === 'home') {
          await page.locator('.navbar__brand').first().click();
          await expect(page).toHaveURL((url) => url.pathname === `${prefix}/`);
        }
        await expectVersionLabel(version, latestDocsVersion, false, locale);
      });
    }

    test(`${locale} docs sidebar keeps its logo and close button without a duplicate theme toggle`, async ({page}) => {
      await page.setViewportSize({width: 390, height: 844});
      await page.goto(`${prefix}${docsPath()}/`);
      await expect(page.locator('html')).toHaveAttribute('data-has-hydrated', 'true');
      const themeButton = page.locator('.navbar__items--right .navbar-color-mode-toggle > button');
      const themeLabel = await themeButton.getAttribute('aria-label');
      expect(themeLabel).toBeTruthy();
      await page.locator('.navbar__items--right > .navbar__toggle').click();
      const sidebar = page.locator('.navbar-sidebar--show .navbar-sidebar');
      await expect(sidebar).toBeVisible();
      await expect(sidebar.locator('.navbar-sidebar__brand .navbar__brand')).toBeVisible();
      await expect(sidebar.getByRole('button', {name: themeLabel!, exact: true})).toHaveCount(0);
      await sidebar.locator('.navbar-sidebar__close').click();
      await expect(page.locator('.navbar-sidebar--show')).toHaveCount(0);
      await expect(themeButton).toBeVisible();
    });
  }
});

test.describe('Navbar — Minimum viewport width', () => {
  for (const {locale, prefix} of [{locale: 'ko', prefix: ''}, {locale: 'ja', prefix: '/ja'}]) {
    for (const route of ['home', 'docs']) {
      test(`${locale} ${route} preserves the 320px header below the minimum width`, async ({page}) => {
        await page.setViewportSize({width: 320, height: 844});
        await page.goto(route === 'home' ? `${prefix}/` : `${prefix}${docsPath()}/`);
        await expect(page.locator('html')).toHaveAttribute('data-has-hydrated', 'true');
        await page.evaluate(() => document.fonts.ready);
        const navbar = page.locator('.navbar');
        const controls = page.locator('.navbar__items--right').locator(
          '.navbar-color-mode-toggle > button, .navbar-version-dropdown, .navbar-locale-dropdown, .DocSearch-Button, .nav-mobile-hamburger, .navbar__toggle',
        );
        const readControlPositions = () => controls.evaluateAll((elements) => {
          const navbarBox = document.querySelector('.navbar')!.getBoundingClientRect();
          return elements.map((element) => element.getBoundingClientRect())
            .filter((box) => box.width > 0)
            .map((box) => ({x: box.x - navbarBox.x, y: box.y - navbarBox.y, width: box.width, height: box.height}));
        });
        const baselineNavbar = await navbar.boundingBox();
        const baselineControls = await readControlPositions();

        for (const width of [214, 280]) {
          await test.step(`${width}px`, async () => {
            await page.setViewportSize({width, height: 844});
            await page.evaluate(() => window.scrollTo({left: 0, top: 0}));
            await expect(page.locator('body')).toHaveCSS('width', '320px');
            const box = await navbar.boundingBox();
            expect(box!.width).toBe(320);
            expect(box!.height).toBe(baselineNavbar!.height);
            expect(await readControlPositions()).toEqual(baselineControls);
            await page.evaluate(() => window.scrollTo({left: document.documentElement.scrollWidth, top: 0}));
            await expect.poll(() => page.evaluate(() => window.scrollX)).toBeGreaterThan(0);
          });
        }
      });
    }
  }
});

test.describe('Navbar — Localized homepage links', () => {
  for (const {locale, prefix} of [{locale: 'ko', prefix: ''}, {locale: 'ja', prefix: '/ja'}]) {
    test(`${locale} 1024px 데스크톱 Overview 선택 후 메뉴 닫힘`, async ({page}) => {
      await page.setViewportSize({width: 1024, height: 900});
      await page.goto(`${prefix}/`);
      await expect(page.locator('html')).toHaveAttribute('data-has-hydrated', 'true');
      await openDropdown(page, 'framework');
      await page.locator('#content-framework').getByRole('link', {name: /^Overview/}).click();
      await expect(page).toHaveURL(new RegExp(`${prefix}/$`));
      await expect(page.locator('html')).toHaveAttribute('lang', locale);
      await expect(page.locator('#trigger-framework')).toHaveAttribute('aria-expanded', 'false');
      await expect(page.locator('#content-framework')).toHaveCount(0);
    });

    for (const key of ['Enter', 'Space']) {
      test(`${locale} 모바일 ${key}로 하위 메뉴를 열고 문서 이동`, async ({page}) => {
        await page.setViewportSize({width: 390, height: 844});
        await page.goto(`${prefix}/`);
        await expect(page.locator('html')).toHaveAttribute('data-has-hydrated', 'true');
        await page.locator('.nav-mobile-hamburger').click();
        await page.locator('button.nav-mobile-menu-item', {hasText: 'Framework'}).press(key);
        const documentation = page.locator('.nav-mobile-submenu').getByRole('link', {name: 'Documentation', exact: true});
        await expect(documentation).toBeVisible();
        await documentation.press('Enter');
        await expect(page).toHaveURL(new RegExp(`${prefix}/docs/${latestDocsVersion.replace('.', '\\.')}/?$`));
        await expect(page.locator('html')).toHaveAttribute('lang', locale);
        await expect(page.locator('article')).toBeVisible();
        await expect(page.locator('.nav-mobile-overlay')).toHaveCount(0);
        await page.goBack();
        await expect(page.locator('.nav-mobile-hamburger')).toBeVisible();
        await expect(page.locator('.nav-mobile-overlay')).toHaveCount(0);
      });
    }

    test(`${locale} 모바일 Docs 키보드 이동`, async ({page}) => {
      await page.setViewportSize({width: 390, height: 844});
      await page.goto(`${prefix}/`);
      await expect(page.locator('html')).toHaveAttribute('data-has-hydrated', 'true');
      await page.locator('.nav-mobile-hamburger').click();
      await page.locator('a.nav-mobile-menu-item', {hasText: 'Docs'}).press('Enter');
      await expect(page).toHaveURL(new RegExp(`${prefix}/docs/${latestDocsVersion.replace('.', '\\.')}/?$`));
      await expect(page.locator('html')).toHaveAttribute('lang', locale);
      await expect(page.locator('article')).toBeVisible();
      await expect(page.locator('.nav-mobile-overlay')).toHaveCount(0);
    });

    test(`${locale} 모바일 메뉴 포커스가 활성 패널 안에서 순환`, async ({page}) => {
      await page.setViewportSize({width: 390, height: 844});
      await page.goto(`${prefix}/`);
      await expect(page.locator('html')).toHaveAttribute('data-has-hydrated', 'true');
      await page.locator('.nav-mobile-hamburger').click();
      const docsLink = page.locator('a.nav-mobile-menu-item', {hasText: 'Docs'});
      await docsLink.focus();
      await page.keyboard.press('Tab');
      await expect(page.locator('.nav-mobile-logo')).toBeFocused();
      await page.keyboard.press('Shift+Tab');
      await expect(docsLink).toBeFocused();

      await page.locator('button.nav-mobile-menu-item', {hasText: 'Framework'}).press('Enter');
      const back = page.locator('.nav-mobile-back');
      await expect(back).toBeFocused();
      const lastLink = page.locator('.nav-mobile-submenu').getByRole('link', {name: 'Laravel Learn', exact: true});
      await lastLink.focus();
      await page.keyboard.press('Tab');
      await expect(back).toBeFocused();
      await page.keyboard.press('Shift+Tab');
      await expect(lastLink).toBeFocused();
      await back.press('Enter');
      await expect(page.locator('.nav-mobile-close').first()).toBeFocused();
      await expect(page.locator('.nav-mobile-overlay')).toBeVisible();
    });

    test(`${locale} 모바일 Escape와 닫기 버튼으로 닫으면 포커스 복귀`, async ({page}) => {
      await page.setViewportSize({width: 390, height: 844});
      await page.goto(`${prefix}/`);
      await expect(page.locator('html')).toHaveAttribute('data-has-hydrated', 'true');
      const hamburger = page.locator('.nav-mobile-hamburger');
      await hamburger.press('Enter');
      await page.locator('a.nav-mobile-menu-item', {hasText: 'Docs'}).focus();
      await page.keyboard.press('Escape');
      await expect(page.locator('.nav-mobile-overlay')).toHaveCount(0);
      await expect(hamburger).toBeFocused();
      await hamburger.press('Enter');
      await page.locator('button.nav-mobile-menu-item', {hasText: 'Framework'}).press('Enter');
      await page.locator('.nav-mobile-subpanel .nav-mobile-close').press('Enter');
      await expect(page.locator('.nav-mobile-overlay')).toHaveCount(0);
      await expect(hamburger).toBeFocused();
    });

    for (const width of [1280, 390]) {
      test(`${locale} ${width}px 홈 메뉴에서 문서 언어 유지`, async ({page}) => {
        const mobile = width < 1024;
        const localizedDocs = `${prefix}${docsPath()}/`;
        await page.setViewportSize({width, height: 900});
        await page.goto(`${prefix}/`);
        await expect(page.locator('html')).toHaveAttribute('data-has-hydrated', 'true');
        if (mobile) {
          await page.locator('.nav-mobile-hamburger').click();
        }
        const docsLink = page.locator(mobile ? 'a.nav-mobile-menu-item' : '.nav-docs-link', {hasText: 'Docs'});
        await expect(docsLink).toHaveAttribute('href', localizedDocs);

        if (mobile) {
          await page.locator('button.nav-mobile-menu-item', {hasText: 'Framework'}).click();
        } else {
          await openDropdown(page, 'framework');
        }
        const links = page.locator(`${mobile ? '.nav-mobile-submenu' : '#content-framework'} a[href^="/"]`);
        const slugs = mobile
          ? ['starter-kits', 'releases', '']
          : ['releases', '', 'ai', 'eloquent', 'artisan', 'routing', '', 'starter-kits'];
        await expect(links).toHaveCount(slugs.length + 1);
        expect(await links.evaluateAll((elements) => elements.map((element) => element.getAttribute('href'))))
          .toEqual([`${prefix}/`, ...slugs.map((slug) => `${prefix}${docsPath(slug)}/`)]);
        if (mobile) {
          await page.locator('.nav-mobile-back').click();
        }

        await docsLink.click();
        await expect(page).toHaveURL(new RegExp(`${prefix}/docs/${latestDocsVersion.replace('.', '\\.')}/?$`));
        await expect(page.locator('html')).toHaveAttribute('lang', locale);
        await expect(page.locator('article')).toBeVisible();
      });
    }
  }
});

test.describe('Navbar — Enlarged homepage text', () => {
  for (const prefix of ['', '/ja']) {
    for (const width of [320, 390, 431]) {
      test(`${prefix || 'ko'} ${width}px enlarged controls remain separate and clickable`, async ({page}) => {
        await page.setViewportSize({width, height: 844});
        await page.goto(`${prefix}/`);
        await expect(page.locator('html')).toHaveAttribute('data-has-hydrated', 'true');
        await page.evaluate(async () => {
          document.documentElement.style.fontSize = '32px';
          await document.fonts.ready;
          await Promise.all(document.querySelector('.navbar')!.getAnimations({subtree: true}).map((animation) => animation.finished));
        });

        await expectHeaderControlsUncovered(page, [
          '.navbar__brand img', '.navbar-color-mode-toggle > button', '.navbar-version-dropdown',
          '.navbar-locale-dropdown', '.DocSearch-Button', '.nav-mobile-hamburger',
        ]);

        const before = await page.locator('html').getAttribute('data-theme-choice');
        await page.locator('.navbar-color-mode-toggle > button').click();
        await expect(page.locator('html')).not.toHaveAttribute('data-theme-choice', before!);
        await page.locator('.nav-mobile-hamburger').click();
        await expect(page.locator('.nav-mobile-overlay')).toBeVisible();
        await page.locator('.nav-mobile-close').first().click();
        await expect(page.locator('.nav-mobile-overlay')).toHaveCount(0);
      });
    }
  }
});

test.describe('Navbar — Enlarged docs text', () => {
  for (const prefix of ['', '/ja']) {
    for (const theme of ['light', 'dark'] as const) {
      for (const {width, fontSize} of [{width: 320, fontSize: 16}, {width: 320, fontSize: 32}, {width: 390, fontSize: 32}]) {
        test(`${prefix || 'ko'} ${width}px ${fontSize}px ${theme} docs controls remain separate and clickable`, async ({page}) => {
          await page.emulateMedia({colorScheme: theme});
          await page.setViewportSize({width, height: 844});
          await page.goto(`${prefix}${docsPath()}/`);
          await expect(page.locator('html')).toHaveAttribute('data-has-hydrated', 'true');
          await expect(page.locator('html')).toHaveAttribute('data-theme', theme);
          await page.evaluate(async (size) => {
            document.documentElement.style.fontSize = `${size}px`;
            await document.fonts.ready;
            await Promise.all(document.querySelector('.navbar')!.getAnimations({subtree: true}).map((animation) => animation.finished));
          }, fontSize);

          await expectHeaderControlsUncovered(page, [
            '.navbar__brand img', '.navbar__items--right .navbar-color-mode-toggle > button',
            '.navbar-version-dropdown', '.navbar-locale-dropdown', '.DocSearch-Button',
            '.navbar__items--right > .navbar__toggle',
          ]);
          const before = await page.locator('html').getAttribute('data-theme-choice');
          await page.locator('.navbar__items--right .navbar-color-mode-toggle > button').click();
          await expect(page.locator('html')).not.toHaveAttribute('data-theme-choice', before!);
          await page.locator('.DocSearch-Button').click();
          await expect(page.locator('.DocSearch-Modal')).toBeVisible();
          await page.keyboard.press('Escape');
          await expect(page.locator('.DocSearch-Modal')).toHaveCount(0);
          await page.locator('.navbar__items--right > .navbar__toggle').click();
          await expect(page.locator('.navbar-sidebar--show .navbar-sidebar')).toBeVisible();
          await page.locator('.navbar-sidebar__close').click();
          await expect(page.locator('.navbar-sidebar--show')).toHaveCount(0);

          if (fontSize === 32) {
            const heading = page.locator('article h2[id]').nth(1);
            const headingId = await heading.getAttribute('id');
            const toc = page.locator('.theme-doc-toc-mobile');
            await toc.getByRole('button').click();
            await toc.locator(`a[href="#${headingId}"]`).click();
            await expect.poll(async () => {
              const headingBox = await heading.boundingBox();
              const navbarBox = await page.locator('.navbar').boundingBox();
              return headingBox!.y - navbarBox!.y - navbarBox!.height;
            }).toBeGreaterThanOrEqual(-ORDER_TOLERANCE);
          }
        });
      }
    }
  }
});
