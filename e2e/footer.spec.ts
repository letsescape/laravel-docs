import {test, expect, type Page, type Locator} from '@playwright/test';
import {docsPath} from './utils/docs-version';

// 메인 페이지와 문서 페이지에 서로 다른 푸터 변형 사용
// - 메인 페이지: 브랜드 + 링크 컬럼 4개(Products/Packages/Resources/Partners)
// - 문서 페이지: 브랜드 + Community 섹션(제품군 컬럼 제거)
// 중간 해상도(800~1000px)의 레이아웃 깨짐 재발과 메인/문서 푸터 변형 혼용 방지

const HOME_COLUMNS = ['Products', 'Packages', 'Resources', 'Partners'];

// h4 제목을 기준으로 푸터 컬럼을 정확히 선택
function footerColumn(page: Page, title: string): Locator {
  return page.locator('.hp-footer .footer-column').filter({
    has: page.getByRole('heading', {level: 4, name: title, exact: true}),
  });
}

// 푸터 오른쪽 컬럼 그룹이 뷰포트 밖으로 넘치지 않는지 확인
async function expectFooterWithinViewport(
  page: Page,
  viewportWidth: number,
  columns: string[],
) {
  await expect(page.locator('.hp-footer')).toBeVisible();
  // 첫 번째 컬럼이 렌더링될 때까지 대기(레이스 방지)
  await expect(footerColumn(page, columns[0])).toBeVisible();

  // 가로 스크롤(오버플로) 없음
  const scrollWidth = await page.evaluate(
    () => document.documentElement.scrollWidth,
  );
  expect(scrollWidth, '가로 스크롤(오버플로)이 없어야 함').toBeLessThanOrEqual(
    viewportWidth + 2,
  );

  // 오른쪽 컬럼 그룹의 끝이 뷰포트 안에 있어야 함
  const colsRight = await page
    .locator('.footer-columns-right')
    .evaluate((el) => el.getBoundingClientRect().right);
  expect(colsRight, '링크 컬럼이 뷰포트 안에 보여야 함').toBeLessThanOrEqual(
    viewportWidth + 2,
  );

  // 모든 예상 컬럼이 화면 안(왼쪽 0 이상, 오른쪽 뷰포트 이하)에 위치
  for (const col of columns) {
    const box = await footerColumn(page, col).first().boundingBox();
    expect(box, `${col} 컬럼 box`).not.toBeNull();
    expect(box!.x, `${col} 좌측`).toBeGreaterThanOrEqual(-2);
    expect(box!.x + box!.width, `${col} 우측`).toBeLessThanOrEqual(
      viewportWidth + 2,
    );
  }
}

// =============================================================================
// 메인 페이지 푸터 — 중간 해상도(800~1000px) 레이아웃
// =============================================================================
test.describe('Homepage footer — mid widths (800–1000px)', () => {
  for (const width of [800, 900, 996, 1000]) {
    test(`FT-W-${width}: ${width}px에서 푸터 오버플로 없음`, async ({page}) => {
      await page.setViewportSize({width, height: 1000});
      await page.goto('/');
      await expectFooterWithinViewport(page, width, HOME_COLUMNS);
    });
  }
});

// =============================================================================
// 메인 페이지 푸터 변형 — 제품군 컬럼 유지, Community 없음
// =============================================================================
test.describe('Homepage footer variant', () => {
  test.use({viewport: {width: 1280, height: 800}});

  test('FT-H-1: 메인 푸터는 docs 변형이 아님', async ({page}) => {
    await page.goto('/');
    await expect(page.locator('.hp-footer')).toBeVisible();
    await expect(page.locator('.hp-footer.hp-footer--docs')).toHaveCount(0);
  });

  test('FT-H-2: 메인 푸터는 4개 제품군 컬럼을 가진다', async ({page}) => {
    await page.goto('/');
    for (const col of HOME_COLUMNS) {
      await expect(footerColumn(page, col)).toBeVisible();
    }
  });

  test('FT-H-3: 메인 푸터에는 Community 섹션이 없다', async ({page}) => {
    await page.goto('/');
    // 제품군 컬럼이 렌더링될 때까지 기다린 뒤 Community 컬럼 부재 검증
    await expect(footerColumn(page, 'Products')).toBeVisible();
    await expect(footerColumn(page, 'Community')).toHaveCount(0);
  });
});

// =============================================================================
// 문서 페이지 푸터 변형 — 제품군 컬럼 제거 + Community 섹션 추가
// =============================================================================
test.describe('Docs footer variant', () => {
  test.use({viewport: {width: 1280, height: 800}});

  test('FT-D-1: 문서 페이지가 커스텀 푸터(docs 변형)를 렌더', async ({page}) => {
    await page.goto(docsPath());
    await expect(page.locator('.hp-footer.hp-footer--docs')).toBeVisible();
  });

  test('FT-D-2: 문서 푸터에는 제품군 컬럼이 없다', async ({page}) => {
    await page.goto(docsPath());
    // 문서 변형이 렌더링될 때까지 기다린 뒤 제품군 컬럼 부재 검증
    await expect(page.locator('.hp-footer.hp-footer--docs')).toBeVisible();
    for (const col of HOME_COLUMNS) {
      await expect(footerColumn(page, col)).toHaveCount(0);
    }
  });

  test('FT-D-3: Community 섹션에 지정된 커뮤니티 링크가 있다', async ({page}) => {
    await page.goto(docsPath());
    const community = footerColumn(page, 'Community');
    await expect(community).toBeVisible();
    for (const href of [
      'https://laravel.kr',
      'https://php64.net',
      'https://open.kakao.com/o/g3dWlf0',
      'https://discord.gg/WUMhVr85cv',
    ]) {
      await expect(community.locator(`a[href="${href}"]`)).toBeVisible();
    }
    // 링크는 정확히 4개(안내 문구는 링크가 아님)
    await expect(community.locator('a')).toHaveCount(4);
  });

  test('FT-D-6: Community 섹션에 링크 없는 안내문구가 있다', async ({page}) => {
    await page.goto(docsPath());
    const note = footerColumn(page, 'Community').locator('.footer-note');
    await expect(note).toBeVisible();
    await expect(note).not.toBeEmpty();
    await expect(note.locator('a')).toHaveCount(0);
  });

  test('FT-D-4: 문서 페이지에서 기본 Docusaurus 푸터(.footer__links)는 없음', async ({page}) => {
    await page.goto(docsPath());
    await expect(page.locator('.hp-footer.hp-footer--docs')).toBeVisible();
    await expect(page.locator('.footer__links')).toHaveCount(0);
  });

  test('FT-D-5: 문서 페이지 푸터도 800–1000px에서 오버플로 없음', async ({page}) => {
    await page.setViewportSize({width: 900, height: 1000});
    await page.goto(docsPath());
    await expectFooterWithinViewport(page, 900, ['Community']);
  });
});
