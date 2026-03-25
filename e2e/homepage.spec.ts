import {test, expect} from '@playwright/test';

// 원본 Laravel.com을 대상으로 테스트
test.use({baseURL: 'https://laravel.com'});

// =============================================================================
// 데스크톱 (1280px)
// =============================================================================
test.describe('Homepage — Desktop (1280px)', () => {
  test.use({viewport: {width: 1280, height: 800}});

  test.beforeEach(async ({page}) => {
    await page.goto('/');
  });

  // ---------------------------------------------------------------------------
  // 히어로 섹션
  // ---------------------------------------------------------------------------
  test.describe('히어로 섹션', () => {
    // H-1
    test('H-1: 메인 헤드라인', async ({page}) => {
      const h1 = page.getByRole('heading', {level: 1});
      await expect(h1).toContainText('The clean stack for Artisans and agents.');
    });

    // H-2
    test('H-2: 서브 텍스트', async ({page}) => {
      await expect(page.getByText('Laravel is batteries-included so everyone can build and ship web apps at ridiculous speed.')).toBeVisible();
    });

    // H-3
    test('H-3: View framework docs 버튼', async ({page}) => {
      const link = page.getByRole('link', {name: 'View framework docs'}).first();
      await expect(link).toBeVisible();
      await expect(link).toHaveAttribute('href', '/docs');
    });

    // H-4
    test('H-4: 히어로 일러스트레이션 SVG 표시', async ({page}) => {
      const svg = page.locator('main .container svg.absolute.right-0.bottom-0');
      await expect(svg).toBeVisible();
      const box = await svg.boundingBox();
      expect(box!.width).toBeGreaterThan(0);
    });

    // H-5
    test('H-5: 일러스트레이션 940px 미만 숨김 클래스', async ({page}) => {
      const svg = page.locator('main .container svg.absolute.right-0.bottom-0');
      const cls = await svg.getAttribute('class');
      expect(cls).toContain('max-[940px]:hidden');
    });

    // H-6
    test('H-6: SVG 내 도메인 텍스트 (v13)', async ({page}) => {
      const text = page.locator('main .container svg.absolute.right-0.bottom-0 text', {hasText: 'v13.laravel.cloud'});
      await expect(text).toBeAttached();
    });

    // H-7
    test('H-7: SVG 내 도메인 텍스트 (skills)', async ({page}) => {
      const text = page.locator('main .container svg.absolute.right-0.bottom-0 text', {hasText: 'skills.laravel.cloud'});
      await expect(text).toBeAttached();
    });

    // H-8
    test('H-8: SVG 내 내장 이미지', async ({page}) => {
      const image = page.locator('main .container svg.absolute.right-0.bottom-0 image[href="/images/home/taylor-otwell.avif"]');
      await expect(image).toBeAttached();
    });

    // H-9
    test('H-9: 플로팅 아이콘 SVG', async ({page}) => {
      const count = await page.evaluate(() => {
        const overlay = document.querySelector('main .container')!.children[2];
        const allSvgs = overlay?.querySelectorAll('svg') ?? [];
        // 첫 번째는 메인 일러스트레이션, 나머지가 플로팅 아이콘
        return allSvgs.length - 1;
      });
      expect(count).toBe(19);
    });
  });

  // ---------------------------------------------------------------------------
  // AI Framework 섹션
  // ---------------------------------------------------------------------------
  test.describe('AI Framework 섹션', () => {
    // AF-1
    test('AF-1: 섹션 헤딩', async ({page}) => {
      const h2 = page.getByRole('heading', {level: 2, name: /Ship web apps with the.*framework/});
      await expect(h2).toBeVisible();
    });

    // AF-2
    test('AF-2: Toggle AI 버튼', async ({page}) => {
      const btn = page.getByRole('button', {name: 'Toggle AI', pressed: true});
      await expect(btn).toBeVisible();
    });

    // AF-3
    test('AF-3: 서브 텍스트', async ({page}) => {
      await expect(page.getByText(/We.re ready when you.re ready/)).toBeVisible();
    });
  });

  // ---------------------------------------------------------------------------
  // 프레임워크 상세 섹션
  // ---------------------------------------------------------------------------
  test.describe('프레임워크 상세 섹션', () => {
    // FD-1
    test('FD-1: 섹션 헤딩', async ({page}) => {
      await expect(page.getByRole('heading', {level: 3, name: 'A framework for developers and agents'})).toBeVisible();
    });

    // FD-2
    test('FD-2: 설명 텍스트', async ({page}) => {
      await expect(page.getByText('Laravel has opinions on everything')).toBeVisible();
    });

    // FD-3
    test('FD-3: 기능 목록 4개', async ({page}) => {
      const items = ['Starter kits', 'AI SDK', 'Database ORM', 'Open source ecosystem'];
      for (const item of items) {
        await expect(page.getByText(item).first()).toBeAttached();
      }
    });

    // FD-4
    test('FD-4: Explore 링크', async ({page}) => {
      const link = page.getByRole('link', {name: 'Explore the framework'});
      await expect(link).toBeVisible();
      await expect(link).toHaveAttribute('href', 'https://laravel.com/docs/');
    });

    // FD-5
    test('FD-5: 코드 카테고리 탭 8개', async ({page}) => {
      const categories = ['Auth', 'AI SDK', 'ORM', 'Migrations', 'Validation', 'Storage', 'Queues', 'Testing'];
      for (const cat of categories) {
        await expect(page.getByRole('button', {name: cat, exact: true})).toBeAttached();
      }
    });

    // FD-6
    test('FD-6: 기본 활성 카테고리', async ({page}) => {
      const authBtn = page.getByRole('button', {name: 'Auth', pressed: true});
      await expect(authBtn).toBeVisible();
    });

    // FD-7
    test('FD-7: 코드 파일 탭', async ({page}) => {
      const webTab = page.getByRole('tab', {name: 'web.php', selected: true});
      await expect(webTab).toBeVisible();
      const controllerTab = page.getByRole('tab', {name: 'UserController.php'});
      await expect(controllerTab).toBeVisible();
    });

    // FD-8
    test('FD-8: 코드 내용', async ({page}) => {
      const codePanel = page.getByRole('tabpanel', {name: 'web.php'});
      await expect(codePanel).toContainText("Route::get('/dashboard'");
    });

    // FD-9
    test('FD-9: 카테고리 탭 전환', async ({page}) => {
      const codePanel = page.getByRole('tabpanel').first();
      const initialText = await codePanel.textContent();
      await page.getByRole('button', {name: 'ORM', exact: true}).click();
      await expect(codePanel).not.toHaveText(initialText!);
    });

    // FD-10
    test('FD-10: 파일 탭 전환', async ({page}) => {
      const codeArea = page.getByRole('tabpanel').first();
      const initialText = await codeArea.textContent();
      await page.getByRole('tab', {name: 'UserController.php'}).click();
      await expect(codeArea).not.toHaveText(initialText!);
    });
  });

  // ---------------------------------------------------------------------------
  // Laravel Cloud 섹션
  // ---------------------------------------------------------------------------
  test.describe('Laravel Cloud 섹션', () => {
    // CL-1
    test('CL-1: 섹션 헤딩', async ({page}) => {
      await expect(page.getByRole('heading', {level: 3, name: 'Laravel Cloud takes you from local to live in seconds'})).toBeVisible();
    });

    // CL-2
    test('CL-2: 설명 텍스트', async ({page}) => {
      await expect(page.getByText('No more guessing how many servers you need')).toBeVisible();
    });

    // CL-3
    test('CL-3: 기능 목록 2개', async ({page}) => {
      await expect(page.getByText('Full control via dashboard or CLI')).toBeVisible();
      await expect(page.getByText('Instantly add databases')).toBeVisible();
    });

    // CL-4
    test('CL-4: CTA 링크', async ({page}) => {
      const link = page.getByRole('link', {name: 'Explore Laravel Cloud'});
      await expect(link).toBeVisible();
      await expect(link).toHaveAttribute('href', 'https://cloud.laravel.com');
    });

    // CL-5
    test('CL-5: 오토스케일 일러스트레이션 컨테이너', async ({page}) => {
      const container = page.locator('[aria-hidden="true"].overflow-hidden, .overflow-hidden:has([aria-hidden="true"])');
      // 섹션으로 스크롤하여 lazy load 트리거
      await page.getByRole('heading', {level: 3, name: 'Laravel Cloud takes you'}).scrollIntoViewIfNeeded();
      const illustContainer = page.locator('.overflow-hidden:has([aria-hidden="true"])').first();
      await expect(illustContainer).toBeVisible();
    });

    // CL-6
    test('CL-6: 오토스케일 SVG', async ({page}) => {
      await page.getByRole('heading', {level: 3, name: 'Laravel Cloud takes you'}).scrollIntoViewIfNeeded();
      const svg = page.locator('[aria-hidden="true"] svg[viewBox="0 0 748 274"]');
      await expect(svg).toBeAttached();
    });

    // CL-7
    test('CL-7: 상태 배지 텍스트', async ({page}) => {
      await page.getByRole('heading', {level: 3, name: 'Laravel Cloud takes you'}).scrollIntoViewIfNeeded();
      for (const label of ['Idling', 'Scaling up', 'Scaling down']) {
        await expect(page.locator('[aria-hidden="true"]').getByText(label, {exact: true})).toBeAttached();
      }
    });

    // CL-8
    test('CL-8: 활성 배지 1개 표시', async ({page}) => {
      await page.getByRole('heading', {level: 3, name: 'Laravel Cloud takes you'}).scrollIntoViewIfNeeded();
      // lazy load 대기: "Scaling up" 텍스트가 DOM에 나타날 때까지
      await page.locator('text=Scaling up').first().waitFor({state: 'attached', timeout: 10000});
      const count = await page.evaluate(() => {
        const allAria = document.querySelectorAll('[aria-hidden="true"]');
        let container = null;
        for (const el of allAria) {
          if (el.textContent?.includes('Idling') && el.textContent?.includes('Scaling')) {
            container = el;
            break;
          }
        }
        if (!container) return -1;
        const badges = ['Idling', 'Scaling up', 'Scaling down'];
        let visible = 0;
        container.querySelectorAll('div').forEach(d => {
          const text = d.textContent?.trim();
          if (badges.includes(text!) && d.children.length <= 2) {
            const opacity = parseFloat(getComputedStyle(d).opacity);
            if (opacity > 0.5) visible++;
          }
        });
        return visible;
      });
      expect(count).toBe(1);
    });
  });

  // ---------------------------------------------------------------------------
  // Preview Environments 섹션
  // ---------------------------------------------------------------------------
  test.describe('Preview Environments 섹션', () => {
    // PE-1
    test('PE-1: 섹션 헤딩', async ({page}) => {
      await expect(page.getByRole('heading', {level: 3, name: /Check pull requests from your team/})).toBeVisible();
    });

    // PE-2
    test('PE-2: 설명 텍스트', async ({page}) => {
      await expect(page.getByText(/Review every change in Cloud.s zero-risk/)).toBeVisible();
    });

    // PE-3
    test('PE-3: 기능 목록 2개', async ({page}) => {
      await expect(page.getByText('Integrates seamlessly with GitHub Actions')).toBeAttached();
      await expect(page.getByText('Test migrations and heavy changes safely')).toBeAttached();
    });

    // PE-4
    test('PE-4: CTA 링크', async ({page}) => {
      const link = page.getByRole('link', {name: 'Explore Preview Environments'});
      await expect(link).toBeVisible();
      await expect(link).toHaveAttribute('href', 'https://cloud.laravel.com/docs/preview-environments');
    });

    // PE-5
    test('PE-5: 파이프라인 일러스트레이션 SVG', async ({page}) => {
      const svg = page.locator('svg[viewBox="0 0 524 398"]');
      await expect(svg).toBeAttached();
      const box = await svg.boundingBox();
      expect(box!.width).toBeGreaterThan(0);
    });

    // PE-6
    test('PE-6: SVG 내 도메인 텍스트', async ({page}) => {
      const svg = page.locator('svg[viewBox="0 0 524 398"]');
      await expect(svg.locator('text', {hasText: 'laravel-ai.laravel.cloud'})).toBeAttached();
      await expect(svg.locator('text', {hasText: 'skills.laravel.cloud'})).toBeAttached();
    });
  });

  // ---------------------------------------------------------------------------
  // Nightwatch 섹션
  // ---------------------------------------------------------------------------
  test.describe('Nightwatch 섹션', () => {
    // NW-1
    test('NW-1: 섹션 헤딩', async ({page}) => {
      await expect(page.getByRole('heading', {level: 3, name: 'Monitor and fix issues with Nightwatch'})).toBeVisible();
    });

    // NW-2
    test('NW-2: 설명 텍스트', async ({page}) => {
      await expect(page.getByText('Laravel Nightwatch gives full observability')).toBeVisible();
    });

    // NW-3
    test('NW-3: 기능 목록 3개', async ({page}) => {
      await expect(page.getByText('Fix errors and performance with recommended solutions')).toBeVisible();
      await expect(page.getByText('Trace requests, jobs, logs, commands, cache, and more')).toBeVisible();
      await expect(page.getByText('Let agents fix your code using Nightwatch MCP')).toBeVisible();
    });

    // NW-4
    test('NW-4: CTA 링크', async ({page}) => {
      const link = page.getByRole('link', {name: 'Explore Nightwatch'});
      await expect(link).toBeVisible();
      await expect(link).toHaveAttribute('href', 'https://nightwatch.laravel.com');
    });

    // NW-5
    test('NW-5: 대시보드 이미지', async ({page}) => {
      const img = page.getByAltText('Nightwatch dashboard screenshot');
      await expect(img).toBeAttached();
    });
  });

  // ---------------------------------------------------------------------------
  // Frontend 섹션
  // ---------------------------------------------------------------------------
  test.describe('Frontend 섹션', () => {
    // FE-1
    test('FE-1: 섹션 헤딩', async ({page}) => {
      await expect(page.getByRole('heading', {level: 3, name: 'The best partner to any front-end'})).toBeVisible();
    });

    // FE-2
    test('FE-2: 설명 텍스트', async ({page}) => {
      await expect(page.getByText('Easily craft frontend experiences with React, Vue, or Svelte')).toBeVisible();
    });

    // FE-3
    test('FE-3: CTA 링크', async ({page}) => {
      const link = page.getByRole('link', {name: 'Explore front-ends'});
      await expect(link).toBeVisible();
      await expect(link).toHaveAttribute('href', 'https://laravel.com/docs/frontend');
    });

    // FE-4
    test('FE-4: 코드 탭', async ({page}) => {
      for (const tab of ['users.svelte', 'users.tsx', 'users.vue', 'users.blade.php']) {
        await expect(page.getByText(tab, {exact: true})).toBeAttached();
      }
    });
  });

  // ---------------------------------------------------------------------------
  // CTA 섹션
  // ---------------------------------------------------------------------------
  test.describe('CTA 섹션', () => {
    // CT-1
    test('CT-1: 섹션 헤딩', async ({page}) => {
      await expect(page.getByRole('heading', {level: 2, name: 'Create without limits. What will you ship?'})).toBeVisible();
    });

    // CT-2
    test('CT-2: Deploy on Cloud 버튼', async ({page}) => {
      const ctaSection = page.getByRole('heading', {level: 2, name: 'Create without limits'}).locator('..');
      const link = ctaSection.getByRole('link', {name: 'Deploy on Cloud'});
      await expect(link).toBeVisible();
      await expect(link).toHaveAttribute('href', 'https://cloud.laravel.com');
    });

    // CT-3
    test('CT-3: View framework docs 버튼', async ({page}) => {
      const ctaSection = page.getByRole('heading', {level: 2, name: 'Create without limits'}).locator('..');
      const link = ctaSection.getByRole('link', {name: 'View framework docs'});
      await expect(link).toBeVisible();
      await expect(link).toHaveAttribute('href', '/docs');
    });
  });

  // ---------------------------------------------------------------------------
  // Events 섹션
  // ---------------------------------------------------------------------------
  test.describe('Events 섹션', () => {
    // E-1
    test('E-1: 섹션 라벨', async ({page}) => {
      await expect(page.getByText('[', {exact: true}).first()).toBeAttached();
      await expect(page.getByText('Events').first()).toBeVisible();
    });

    // E-2
    test('E-2: 섹션 헤딩', async ({page}) => {
      const h2 = page.getByRole('heading', {level: 2, name: /We.ll see you in/});
      await expect(h2).toBeVisible();
    });

    // E-3
    test('E-3: 설명 텍스트', async ({page}) => {
      await expect(page.getByText('Laravel is best known for its amazing community')).toBeVisible();
    });

    // E-4
    test('E-4: Find nearby meetups 링크', async ({page}) => {
      const link = page.getByRole('link', {name: 'Find nearby meetups'});
      await expect(link).toBeVisible();
      await expect(link).toHaveAttribute('href', '/events');
    });

    // E-5
    test('E-5: 이벤트 카드 4개', async ({page}) => {
      const events = [
        {name: 'Laravel Live Japan', date: 'May 26-27', city: 'Tokyo', country: 'JP'},
        {name: 'Laravel Live UK', date: 'Jun 18-19', city: 'London', country: 'UK'},
        {name: 'Laracon US', date: 'Jul 28-29', city: 'Boston', country: 'US'},
        {name: 'Laravel Live Denmark', date: 'Aug 20-21', city: 'Copenhagen', country: 'DK'},
      ];
      for (const e of events) {
        await expect(page.getByAltText(e.name)).toBeAttached();
        await expect(page.getByText(e.date)).toBeAttached();
        await expect(page.getByText(e.city).first()).toBeAttached();
        await expect(page.getByText(e.country, {exact: true}).first()).toBeAttached();
      }
    });

    // E-6
    test('E-6: Claim your ticket 링크', async ({page}) => {
      const urls = ['https://laravellive.jp/en', 'https://laravellive.uk/', 'https://laracon.us', 'https://laravellive.dk/'];
      const tickets = page.getByRole('link', {name: 'Claim your ticket'});
      const count = await tickets.count();
      expect(count).toBe(4);
      for (let i = 0; i < count; i++) {
        const href = await tickets.nth(i).getAttribute('href');
        expect(urls).toContain(href);
      }
    });

    // E-7
    test('E-7: 이벤트 네비게이션', async ({page}) => {
      await expect(page.getByRole('button', {name: 'Previous event'})).toBeVisible();
      await expect(page.getByRole('button', {name: 'Next event'})).toBeVisible();
    });
  });

  // ---------------------------------------------------------------------------
  // 푸터
  // ---------------------------------------------------------------------------
  test.describe('푸터', () => {
    // FT-1
    test('FT-1: 푸터 표시', async ({page}) => {
      const footer = page.locator('main + div, footer').last();
      await expect(footer).toBeVisible();
    });

    // FT-2
    test('FT-2: 로고 및 태그라인', async ({page}) => {
      await expect(page.getByText('Laravel is the most productive way to build, deploy, and monitor software.')).toBeVisible();
    });

    // FT-3
    test('FT-3: 소셜 링크 4개', async ({page}) => {
      const socials = [
        {name: 'Laravel on GitHub', url: 'https://github.com/laravel'},
        {name: 'Laravel on X', url: 'https://x.com/laravelphp'},
        {name: 'Laravel on YouTube', url: 'https://www.youtube.com/@LaravelPHP'},
        {name: 'Laravel on Discord', url: /discord\.com/},
      ];
      for (const s of socials) {
        const link = page.getByRole('link', {name: s.name});
        await expect(link).toBeVisible();
        if (typeof s.url === 'string') {
          await expect(link).toHaveAttribute('href', s.url);
        } else {
          await expect(link).toHaveAttribute('href', s.url);
        }
      }
    });

    // FT-4
    test('FT-4: 저작권 및 하단 링크', async ({page}) => {
      await expect(page.getByText('© 2026 Laravel')).toBeVisible();
      const legal = page.getByRole('link', {name: 'Legal'});
      await expect(legal).toBeVisible();
      await expect(legal).toHaveAttribute('href', '/legal');
      const status = page.getByRole('link', {name: 'Status'});
      await expect(status).toBeVisible();
      await expect(status).toHaveAttribute('href', 'https://status.laravel.com/');
    });

    // FT-5
    test('FT-5: Products 컬럼', async ({page}) => {
      await expect(page.getByRole('heading', {level: 4, name: 'Products'})).toBeVisible();
      for (const name of ['Cloud', 'Forge', 'Nightwatch', 'Vapor', 'Nova']) {
        await expect(page.getByRole('link', {name, exact: true}).last()).toBeAttached();
      }
    });

    // FT-6
    test('FT-6: Packages 컬럼', async ({page}) => {
      await expect(page.getByRole('heading', {level: 4, name: 'Packages'})).toBeVisible();
      const packages = ['Cashier', 'Dusk', 'Horizon', 'Octane', 'Scout', 'Pennant', 'Pint', 'Sail', 'Sanctum', 'Socialite', 'Telescope', 'Pulse', 'Reverb', 'Echo'];
      for (const name of packages) {
        await expect(page.getByRole('link', {name, exact: true})).toBeAttached();
      }
    });

    // FT-7
    test('FT-7: Resources 컬럼', async ({page}) => {
      await expect(page.getByRole('heading', {level: 4, name: 'Resources'})).toBeVisible();
      const resources = ['Documentation', 'Starter Kits', 'Release Notes', 'Blog', 'News', 'Community', 'Larabelles', 'Learn', 'Jobs', 'Careers', 'Trust'];
      for (const name of resources) {
        await expect(page.getByRole('link', {name, exact: true})).toBeAttached();
      }
    });

    // FT-8
    test('FT-8: Partners 컬럼', async ({page}) => {
      await expect(page.getByRole('heading', {level: 4, name: 'Partners'})).toBeVisible();
      await expect(page.getByRole('link', {name: 'See All'})).toBeAttached();
    });

    // FT-9
    test('FT-9: 하단 Laravel 워드마크', async ({page}) => {
      const svg = page.locator('svg.text-laravel-red[viewBox="0 0 1280 308"], svg[viewBox="0 0 1280 308"].text-laravel-red');
      await expect(svg).toBeAttached();
    });
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

  // HR-1
  test('HR-1: 가로 스크롤 없음', async ({page}) => {
    const scrollWidth = await page.evaluate(() => document.documentElement.scrollWidth);
    expect(scrollWidth).toBeLessThanOrEqual(768);
  });

  // HR-2
  test('HR-2: 푸터 세로 스택', async ({page}) => {
    const columns = page.locator('h4:has-text("Products"), h4:has-text("Packages"), h4:has-text("Resources"), h4:has-text("Partners")');
    const count = await columns.count();
    expect(count).toBe(4);
    // 세로 스택이면 각 컬럼의 x 좌표가 동일하거나, y 좌표가 순차 증가
    const boxes = [];
    for (let i = 0; i < count; i++) {
      boxes.push(await columns.nth(i).boundingBox());
    }
    for (let i = 1; i < boxes.length; i++) {
      expect(boxes[i]!.y).toBeGreaterThanOrEqual(boxes[i - 1]!.y);
    }
  });

  // HR-3
  test('HR-3: 히어로 일러스트레이션 숨김', async ({page}) => {
    const svg = page.locator('main .container svg.absolute.right-0.bottom-0');
    await expect(svg).toBeHidden();
  });

  // HR-4
  test('HR-4: 가로 스크롤 없음 (하단)', async ({page}) => {
    await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
    const scrollWidth = await page.evaluate(() => document.documentElement.scrollWidth);
    expect(scrollWidth).toBeLessThanOrEqual(768);
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

  // HR-5
  test('HR-5: 히어로 텍스트 오버플로우 없음', async ({page}) => {
    const h1 = page.getByRole('heading', {level: 1});
    await expect(h1).toBeVisible();
    const box = await h1.boundingBox();
    expect(box!.x).toBeGreaterThanOrEqual(0);
    expect(box!.x + box!.width).toBeLessThanOrEqual(430);
  });

  // HR-6
  test('HR-6: CTA 버튼 표시', async ({page}) => {
    await expect(page.getByRole('link', {name: 'View framework docs'}).first()).toBeVisible();
  });

  // HR-7
  test('HR-7: 코드 카테고리 탭', async ({page}) => {
    const categories = ['Auth', 'AI SDK', 'ORM', 'Migrations', 'Validation', 'Storage', 'Queues', 'Testing'];
    for (const cat of categories) {
      await expect(page.getByRole('button', {name: cat, exact: true})).toBeAttached();
    }
  });

  // HR-8
  test('HR-8: 이벤트 카드 + 네비게이션', async ({page}) => {
    await expect(page.getByAltText('Laravel Live Japan')).toBeAttached();
    await expect(page.getByRole('button', {name: 'Previous event'})).toBeVisible();
    await expect(page.getByRole('button', {name: 'Next event'})).toBeVisible();
  });

  // HR-9
  test('HR-9: 푸터 세로 스택', async ({page}) => {
    const columns = page.locator('h4:has-text("Products"), h4:has-text("Packages"), h4:has-text("Resources"), h4:has-text("Partners")');
    const count = await columns.count();
    expect(count).toBe(4);
    const boxes = [];
    for (let i = 0; i < count; i++) {
      boxes.push(await columns.nth(i).boundingBox());
    }
    for (let i = 1; i < boxes.length; i++) {
      expect(boxes[i]!.y).toBeGreaterThanOrEqual(boxes[i - 1]!.y);
    }
  });

  // HR-10
  test('HR-10: 가로 스크롤 없음', async ({page}) => {
    const scrollWidth = await page.evaluate(() => document.documentElement.scrollWidth);
    expect(scrollWidth).toBeLessThanOrEqual(430);
  });
});
