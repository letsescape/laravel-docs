import {test, expect, type Page} from '@playwright/test';
import {latestDocsPathPattern} from './utils/docs-version';

// 로컬 사이트를 대상으로 테스트 (playwright.config.ts의 baseURL 사용)

// Helper: 가로 스크롤 없음 검증
async function expectNoHorizontalScroll(page: Page, maxWidth: number) {
  const scrollWidth = await page.evaluate(() => document.documentElement.scrollWidth);
  expect(scrollWidth).toBeLessThanOrEqual(maxWidth + 2);
}

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
    await expect(h1).toContainText('Artisan과 에이전트를 위한');
  });

  test('H-2: 서브 텍스트', async ({page}) => {
    await expect(page.getByText('놀라울 만큼 빠르게')).toBeVisible();
  });

  test('H-3: View framework docs 버튼', async ({page}) => {
    const link = page.locator('.hero-btn-secondary, .hero-btn-primary').first();
    await expect(link).toBeVisible();
  });

  test('H-4: 내부 문서 링크는 최신 안정 버전으로 연결', async ({page}) => {
    // dev 서버에서는 hydration 완료 전에 선택자가 비어 있을 수 있다.
    // footer 가 attached 될 때까지 기다린 뒤 링크를 수집한다.
    await page.locator('.hp-footer a[href^="/docs/"]').first().waitFor({state: 'attached'});
    const docsLinks = await page
      .locator('.homepage a[href^="/docs/"], .hp-footer a[href^="/docs/"], .nav-dropdowns-wrapper a[href^="/docs/"]')
      .evaluateAll((links) =>
        links
          .map((link) => link.getAttribute('href'))
          .filter((href): href is string => href !== null),
      );

    expect(docsLinks.length).toBeGreaterThan(0);
    for (const href of docsLinks) {
      expect(href).toMatch(latestDocsPathPattern);
    }
  });

  test('AF-1: AI Framework 섹션 헤딩', async ({page}) => {
    await expect(page.getByRole('heading', {level: 2, name: /웹 앱을 출시하세요/})).toBeVisible();
  });

  test('FD-1: 프레임워크 상세 헤딩', async ({page}) => {
    await expect(page.getByRole('heading', {level: 3, name: /에이전트를 위한 프레임워크/})).toBeVisible();
  });

  test('FD-4: 코드 카테고리 탭', async ({page}) => {
    for (const cat of ['Auth', 'AI SDK', 'ORM']) {
      await expect(page.getByRole('button', {name: cat, exact: true})).toBeAttached();
    }
  });

  test('CL-1: Laravel Cloud 섹션', async ({page}) => {
    await expect(page.getByRole('heading', {level: 3, name: /Laravel Cloud로 로컬에서 라이브까지/})).toBeVisible();
  });

  test('NW-1: Nightwatch 섹션', async ({page}) => {
    await expect(page.getByRole('heading', {level: 3, name: /Nightwatch로 이슈를 모니터링/})).toBeVisible();
  });

  test('FE-1: Frontend 섹션', async ({page}) => {
    await expect(page.getByRole('heading', {level: 3, name: /어떤 프런트엔드와도/})).toBeVisible();
  });

  test('CT-1: CTA 섹션', async ({page}) => {
    await expect(page.getByRole('heading', {level: 2, name: /한계 없이 만들어 보세요/})).toBeVisible();
  });

  test('E-1: Events 섹션', async ({page}) => {
    await expect(page.getByRole('heading', {level: 2, name: /이벤트.*만나요/})).toBeVisible();
  });

  test('FT-1: 푸터', async ({page}) => {
    await expect(page.locator('.hp-footer')).toBeVisible();
  });

  test('FT-2: 푸터 컬럼', async ({page}) => {
    for (const col of ['Products', 'Packages', 'Resources', 'Partners']) {
      await expect(page.locator('.hp-footer').getByText(col).first()).toBeAttached();
    }
  });

  test('FT-3: 푸터 내부 링크는 존재하는 로컬 경로만 사용', async ({page}) => {
    const hrefs = await page
      .locator('.hp-footer a[href^="/"]')
      .evaluateAll((links) =>
        [
          ...new Set(
            links
              .map((link) => link.getAttribute('href'))
              .filter((href): href is string => href !== null),
          ),
        ],
      );

    const failures: string[] = [];
    for (const href of hrefs) {
      const response = await page.request.get(href);
      if (!response.ok()) {
        failures.push(`${href} -> ${response.status()}`);
      }
    }

    expect(failures).toEqual([]);
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
    await expectNoHorizontalScroll(page, 768);
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
    await expectNoHorizontalScroll(page, 430);
  });
});
