import {test, expect} from '@playwright/test';
import versions from '../versions.json';

const stable = versions.find((version) => version !== 'master')!;
const siteUrl = 'https://laravel.chanhyung.kim';

for (const {locale, prefix, language, heroTitle, docsLabel} of [
  {
    locale: 'ko', prefix: '', language: '한국어 문서',
    heroTitle: 'Artisan과 에이전트를 위한 군더더기 없는 스택.',
    docsLabel: '프레임워크 문서 보기',
  },
  {
    locale: 'ja', prefix: '/ja', language: '日本語ドキュメント',
    heroTitle: 'Artisanとエージェントのための 無駄のないスタック。',
    docsLabel: 'フレームワークのドキュメントを見る',
  },
]) {
  test(`${locale} home metadata describes the localized documentation and preserves the official Hero`, async ({page}) => {
    await page.goto(`${prefix}/`);
    await expect(page.locator('html')).toHaveAttribute('lang', locale);
    const title = `Laravel ${language}`;
    await expect(page.locator('head title')).toHaveCount(1);
    await expect(page).toHaveTitle(title);
    await expect(page.locator('h1')).toHaveText(heroTitle);
    const description = page.locator('meta[name="description"]');
    await expect(description).not.toHaveAttribute('content', /비공식|非公式/);
    const descriptionText = await description.getAttribute('content');
    expect(descriptionText).toContain(language);
    expect(descriptionText).not.toMatch(/\{(?:versionRange|versions)\}|\b(?:\d+\.x|master)\b/);
    for (const selector of ['meta[property="og:title"]', 'meta[name="twitter:title"]']) {
      await expect(page.locator(selector)).toHaveAttribute('content', title);
    }
    for (const selector of ['meta[property="og:description"]', 'meta[name="twitter:description"]']) {
      await expect(page.locator(selector)).toHaveAttribute('content', descriptionText!);
    }
    await expect(page.locator('link[rel="canonical"]')).toHaveAttribute('href', `${siteUrl}${prefix}${prefix ? '/' : ''}`);
    await expect(page.locator('meta[property="og:url"]')).toHaveAttribute('content', `${siteUrl}${prefix}${prefix ? '/' : ''}`);
    for (const selector of ['meta[property="og:image"]', 'meta[name="twitter:image"]']) {
      await expect(page.locator(selector)).toHaveAttribute('content', `${siteUrl}/img/laravel-home.png`);
    }
    const docsLink = page.locator('.hero-buttons a').first();
    await expect(docsLink).toHaveText(docsLabel);
    await expect(docsLink).toHaveAttribute('href', new RegExp(`^${prefix}/docs/${stable.replace('.', '\\.')}/?$`));
    await docsLink.click();
    await expect(page).toHaveURL(new RegExp(`${prefix}/docs/${stable.replace('.', '\\.')}/?$`));
    await expect(page.locator('article')).toBeVisible();
    await page.goBack();
    await expect(page.locator('head title')).toHaveCount(1);
    await expect(page).toHaveTitle(title);
    await expect(page.locator('meta[name="description"]')).toHaveAttribute('content', descriptionText!);
    await expect(page.locator('h1')).toHaveText(heroTitle);
  });
}
