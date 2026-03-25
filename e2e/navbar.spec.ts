import {test, expect} from '@playwright/test';

// 원본 Laravel.com을 대상으로 테스트
test.use({baseURL: 'https://laravel.com'});

// =============================================================================
// 데스크톱 (1280px)
// =============================================================================
test.describe('Navbar — Desktop (1280px)', () => {
  test.use({viewport: {width: 1280, height: 800}});

  test.beforeEach(async ({page}) => {
    await page.goto('/');
  });

  // N-1
  test('N-1: 네비바 표시', async ({page}) => {
    const nav = page.getByRole('navigation', {name: 'Main'});
    await expect(nav).toBeVisible();
  });

  // N-2
  test('N-2: 로고 표시 및 링크', async ({page}) => {
    const logoLink = page.getByRole('navigation', {name: 'Main'}).getByRole('link', {name: 'Laravel'});
    await expect(logoLink).toBeVisible();
    await expect(logoLink).toHaveAttribute('href', '/');
    await expect(logoLink.getByRole('img', {name: 'Laravel'})).toBeVisible();
  });

  // N-3
  test('N-3: Framework 드롭다운 열기', async ({page}) => {
    await page.getByRole('button', {name: 'Framework'}).click();
    await expect(page.getByRole('heading', {name: 'Explore Laravel'})).toBeVisible();
  });

  // N-3a
  test('N-3a: Framework > Explore Laravel', async ({page}) => {
    await page.getByRole('button', {name: 'Framework'}).click();
    const menu = page.locator('[id$="content-framework"]');
    await expect(menu.getByRole('heading', {name: 'Explore Laravel'})).toBeVisible();

    const items = [
      {name: /Overview/, href: '/'},
      {name: /Changelog/, href: '/docs/changelog'},
      {name: /Laravel Learn/, href: '/learn'},
    ];
    for (const item of items) {
      const link = menu.getByRole('link', {name: item.name}).first();
      await expect(link).toBeVisible();
      await expect(link).toHaveAttribute('href', item.href);
    }
  });

  // N-3b
  test('N-3b: Framework > Latest packages', async ({page}) => {
    await page.getByRole('button', {name: 'Framework'}).click();
    await expect(page.getByRole('heading', {name: 'Latest packages'})).toBeVisible();

    const items = [
      {name: 'AI SDK', href: '/ai'},
      {name: 'Boost', href: '/ai/boost'},
      {name: 'Wayfinder', href: /github\.com\/laravel\/wayfinder/},
    ];
    for (const item of items) {
      const link = page.getByRole('link', {name: item.name});
      await expect(link).toBeVisible();
      await expect(link).toHaveAttribute('href', item.href);
    }
  });

  // N-3c
  test('N-3c: Framework > Documentation', async ({page}) => {
    await page.getByRole('button', {name: 'Framework'}).click();
    await expect(page.getByRole('heading', {name: 'Documentation'})).toBeVisible();

    const docItems = ['Installation', 'Agent Setup', 'Eloquent ORM', 'Artisan Console', 'Routing'];
    for (const item of docItems) {
      await expect(page.getByRole('link', {name: item})).toBeVisible();
    }
    const viewAll = page.getByRole('link', {name: 'View all'});
    await expect(viewAll).toBeVisible();
    await expect(viewAll).toHaveAttribute('href', '/docs');
  });

  // N-3d
  test('N-3d: Framework > Starter kits', async ({page}) => {
    await page.getByRole('button', {name: 'Framework'}).click();
    const menu = page.locator('[id$="content-framework"]');
    const starterLink = menu.getByRole('link', {name: /Starter kits/i});
    await expect(starterLink).toBeVisible();
    await expect(starterLink).toHaveAttribute('href', '/starter-kits');

    for (const file of ['users.svelte', 'users.tsx', 'users.vue', 'users.blade.php']) {
      await expect(menu.getByText(file, {exact: true})).toBeVisible();
    }
  });

  // N-4
  test('N-4: Products 드롭다운 열기', async ({page}) => {
    await page.getByRole('button', {name: 'Products'}).click();
    await expect(page.getByText('Deploy now')).toBeVisible();
  });

  // N-4a
  test('N-4a: Products > Cloud', async ({page}) => {
    await page.getByRole('button', {name: 'Products'}).click();
    const cloudLink = page.getByRole('link', {name: /Cloud/}).first();
    await expect(cloudLink).toBeVisible();
    await expect(page.getByText('The fastest way to deploy and scale Laravel applications')).toBeVisible();
    await expect(page.getByText('Deploy now')).toBeVisible();
  });

  // N-4b
  test('N-4b: Products > Forge', async ({page}) => {
    await page.getByRole('button', {name: 'Products'}).click();
    const menu = page.locator('[id$="content-products"]');
    await expect(menu.getByRole('link', {name: /Forge/})).toBeVisible();
    await expect(menu.getByText('Next-level server management with unparalleled control')).toBeVisible();
    await expect(menu.getByText('Manage your servers')).toBeVisible();
  });

  // N-4c
  test('N-4c: Products > Nightwatch', async ({page}) => {
    await page.getByRole('button', {name: 'Products'}).click();
    await expect(page.getByRole('link', {name: /Nightwatch/}).first()).toBeVisible();
    await expect(page.getByText('Full observability and monitoring for Laravel apps')).toBeVisible();
    await expect(page.getByText('Free plans available')).toBeVisible();
  });

  // N-5
  test('N-5: Resources 드롭다운 열기', async ({page}) => {
    await page.getByRole('button', {name: 'Resources'}).click();
    await expect(page.getByRole('heading', {name: 'Company'})).toBeVisible();
  });

  // N-5a
  test('N-5a: Resources > Company', async ({page}) => {
    await page.getByRole('button', {name: 'Resources'}).click();
    await expect(page.getByRole('heading', {name: 'Company'})).toBeVisible();

    const items = [
      {name: 'Blog', href: '/blog'},
      {name: 'Careers', href: '/careers'},
      {name: 'Trust', href: /trust\.laravel\.com/},
      {name: 'Legal', href: '/legal'},
      {name: 'Status', href: /status\.laravel\.com/},
    ];
    for (const item of items) {
      const link = page.getByRole('link', {name: item.name, exact: true}).first();
      await expect(link).toBeVisible();
      await expect(link).toHaveAttribute('href', item.href);
    }
  });

  // N-5b
  test('N-5b: Resources > Social 링크', async ({page}) => {
    await page.getByRole('button', {name: 'Resources'}).click();
    const socials = ['GitHub', 'YouTube', 'X', 'LinkedIn', 'Discord'];
    for (const name of socials) {
      await expect(page.getByRole('link', {name, exact: true}).first()).toBeVisible();
    }
  });

  // N-5c
  test('N-5c: Resources > Partners', async ({page}) => {
    await page.getByRole('button', {name: 'Resources'}).click();
    const menu = page.locator('[id$="content-resources"]');
    await expect(menu.getByRole('heading', {name: 'Partners'})).toBeVisible();

    // 파트너 목록이 6개 이상 표시되는지 (랜덤 순서)
    const partnerLinks = menu.locator('a[href*="/partners/"]');
    await expect(partnerLinks.first()).toBeVisible();
    const count = await partnerLinks.count();
    expect(count).toBeGreaterThanOrEqual(6);

    const viewAll = menu.getByRole('link', {name: 'View all'}).first();
    await expect(viewAll).toBeVisible();
    await expect(viewAll).toHaveAttribute('href', '/partners');
  });

  // N-5d
  test('N-5d: Resources > Featured article', async ({page}) => {
    await page.getByRole('button', {name: 'Resources'}).click();
    await expect(page.getByRole('heading', {name: 'Featured article'})).toBeVisible();
    await expect(page.getByRole('link', {name: 'Read more'})).toBeVisible();
  });

  // N-6
  test('N-6: Events 드롭다운 열기', async ({page}) => {
    await page.getByRole('button', {name: 'Events'}).click();
    await expect(page.getByRole('heading', {name: 'Upcoming events'})).toBeVisible();
  });

  // N-6a
  test('N-6a: Events > Upcoming events', async ({page}) => {
    await page.getByRole('button', {name: 'Events'}).click();
    await expect(page.getByRole('heading', {name: 'Upcoming events'})).toBeVisible();
    const viewAll = page.getByRole('link', {name: 'View all'});
    await expect(viewAll).toBeVisible();
    await expect(viewAll).toHaveAttribute('href', '/community');
  });

  // N-6b
  test('N-6b: Events > Featured events', async ({page}) => {
    await page.getByRole('button', {name: 'Events'}).click();
    // 컨퍼런스 카드가 하나 이상 표시되는지
    const eventCards = page.getByRole('link', {name: /Laravel Live|Laracon/});
    await expect(eventCards.first()).toBeVisible();
  });

  // N-7
  test('N-7: Docs 링크', async ({page}) => {
    const docsLink = page.getByRole('navigation', {name: 'Main'}).getByRole('link', {name: 'Docs'});
    await expect(docsLink).toBeVisible();
    await expect(docsLink).toHaveAttribute('href', '/docs');
  });

  // N-10
  test('N-10: 검색 버튼', async ({page}) => {
    const searchBtn = page.getByRole('button', {name: /Search docs/});
    await expect(searchBtn).toBeVisible();
    await expect(page.getByText('⌘K')).toBeVisible();
  });

  // N-11
  test('N-11: 검색 키보드 단축키', async ({page}) => {
    await page.keyboard.press('Control+k');
    // 검색 모달/다이얼로그가 열리는지
    await expect(page.locator('.DocSearch-Modal, [role="dialog"], [class*="search"]').first()).toBeVisible({timeout: 5000});
  });

  // N-12
  test('N-12: 네비바 상단 고정', async ({page}) => {
    const nav = page.getByRole('navigation', {name: 'Main'});
    // 스크롤 전 위치 확인
    await expect(nav).toBeVisible();
    // 페이지 스크롤
    await page.evaluate(() => window.scrollBy(0, 500));
    // 스크롤 후에도 여전히 보이는지
    await expect(nav).toBeVisible();
    const box = await nav.boundingBox();
    expect(box!.y).toBeLessThanOrEqual(0);
  });

  // N-13
  test('N-13: 네비바 전체 요소 확인', async ({page}) => {
    const nav = page.getByRole('navigation', {name: 'Main'});
    // 로고
    await expect(nav.getByRole('link', {name: 'Laravel'})).toBeVisible();
    // 드롭다운 버튼 4개 + Docs 링크
    for (const name of ['Framework', 'Products', 'Resources', 'Events']) {
      await expect(nav.getByRole('button', {name})).toBeVisible();
    }
    await expect(nav.getByRole('link', {name: 'Docs'})).toBeVisible();
    // Search docs
    await expect(nav.getByRole('button', {name: /Search docs/})).toBeVisible();
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

  // N-14
  test('N-14: 네비바 좌측', async ({page}) => {
    const nav = page.getByRole('navigation', {name: 'Main'});
    await expect(nav.getByRole('link', {name: 'Laravel'})).toBeVisible();
    for (const name of ['Framework', 'Products', 'Resources', 'Events']) {
      await expect(nav.getByRole('button', {name})).toBeVisible();
    }
    await expect(nav.getByRole('link', {name: 'Docs'})).toBeVisible();
  });

  // N-15
  test('N-15: 네비바 우측 요소 숨김', async ({page}) => {
    const searchBtn = page.getByRole('button', {name: /Search docs/});
    await expect(searchBtn).toBeHidden();
  });

  // N-16
  test('N-16: 햄버거 메뉴 없음', async ({page}) => {
    const hamburger = page.getByRole('button', {name: /Open navigation menu/i});
    await expect(hamburger).toBeHidden();
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

  // N-17
  test('N-17: 햄버거 메뉴 표시', async ({page}) => {
    const nav = page.getByRole('navigation', {name: 'Main'});
    // 로고 표시
    await expect(nav.getByRole('link', {name: 'Laravel'})).toBeVisible();
    // 햄버거 버튼 표시
    await expect(page.getByRole('button', {name: /Open navigation menu/i})).toBeVisible();
    // 드롭다운 숨김
    for (const name of ['Framework', 'Products', 'Resources', 'Events']) {
      await expect(nav.getByRole('button', {name})).toBeHidden();
    }
    // Search 숨김
    await expect(page.getByRole('button', {name: /Search docs/})).toBeHidden();
  });

  // N-18
  test('N-18: 햄버거 메뉴 열기/닫기', async ({page}) => {
    // 열기
    await page.getByRole('button', {name: /Open navigation menu/i}).click();
    const drawer = page.getByRole('link', {name: 'Docs', exact: true}).last();
    await expect(drawer).toBeVisible();

    // 닫기
    const closeBtn = page.getByRole('button', {name: /Close/i});
    await expect(closeBtn).toBeVisible();
    await closeBtn.click();
    // 드로어가 닫히는지 확인 (Docs 링크가 드로어 안에 있으므로)
    await expect(page.getByRole('button', {name: /Open navigation menu/i})).toBeVisible();
  });

  // N-19
  test('N-19: 드로어 > Framework 아코디언', async ({page}) => {
    await page.getByRole('button', {name: /Open navigation menu/i}).click();
    // Framework 아코디언 열기
    await page.getByRole('button', {name: 'Framework'}).click();

    const items = ['Overview', 'Starter Kits', 'Release Notes', 'Documentation', 'Laravel Learn'];
    for (const item of items) {
      await expect(page.getByRole('link', {name: item, exact: true}).first()).toBeVisible();
    }
  });

  // N-20
  test('N-20: 드로어 > Products 아코디언', async ({page}) => {
    await page.getByRole('button', {name: /Open navigation menu/i}).click();
    await page.getByRole('button', {name: 'Products'}).click();

    const items = ['Laravel Cloud', 'Forge', 'Nightwatch', 'Nova'];
    for (const item of items) {
      await expect(page.getByRole('link', {name: item, exact: true}).first()).toBeVisible();
    }
  });

  // N-21
  test('N-21: 드로어 > Resources 아코디언', async ({page}) => {
    await page.getByRole('button', {name: /Open navigation menu/i}).click();
    await page.getByRole('button', {name: 'Resources'}).click();

    const items = ['Blog', 'Partners', 'Careers', 'Trust', 'Legal', 'Status'];
    for (const item of items) {
      await expect(page.getByRole('link', {name: item, exact: true}).first()).toBeVisible();
    }
  });

  // N-22
  test('N-22: 드로어 > Events 직접 링크', async ({page}) => {
    await page.getByRole('button', {name: /Open navigation menu/i}).click();
    const eventsLink = page.getByRole('link', {name: 'Events', exact: true});
    await expect(eventsLink).toBeVisible();
    await expect(eventsLink).toHaveAttribute('href', '/community');
  });

  // N-23
  test('N-23: 드로어 > Docs 직접 링크', async ({page}) => {
    await page.getByRole('button', {name: /Open navigation menu/i}).click();
    const docsLink = page.getByRole('link', {name: 'Docs', exact: true}).last();
    await expect(docsLink).toBeVisible();
    await expect(docsLink).toHaveAttribute('href', '/docs');
  });
});
