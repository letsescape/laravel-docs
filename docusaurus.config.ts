import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {themes as prismThemes} from 'prism-react-renderer';
import type {Config} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';
import autoLanguagePlugin from './src/remark/auto-language-plugin';
import replacePlaceholdersPlugin from './src/remark/replace-placeholders';
import anchorMappingPlugin from './src/remark/anchor-mapping';
import githubAdmonitionPlugin from './src/remark/github-admonition';
import styleJsxCleanupPlugin from './src/remark/style-jsx-cleanup';
import methodClassPlugin from './src/remark/method-class';
import stripPandocAttrsPlugin from './src/remark/strip-pandoc-attrs';
import validateLocalAssetsPlugin, {
  assertFrontMatterImageAllowed,
} from './src/remark/validate-local-assets.mjs';
import safeHtmlPlugin from './src/rehype/safe-html.mjs';
import versions from './versions.json';

// This runs in Node.js.
// Do not use client-side code here (browser APIs, JSX, etc.).

// `versions.json`을 단일 출처로 사용
// 새 버전 출시 시 해당 파일만 갱신하면 footer, navbar, lastVersion, path, sidebarPath에 자동 반영
// master는 임시 버전이므로 안정 버전 후보에서 제외
// 첫 번째 안정 버전을 LATEST_STABLE로 사용하고 안정 버전이 없으면 첫 항목 사용
const LATEST_STABLE = versions.find((v) => v !== 'master') ?? versions[0];
const DEFAULT_LOCALE = 'ko';
const LOCALES = ['ko', 'ja'];
const LOCALIZED_ROUTE_PREFIXES = LOCALES.filter((locale) => locale !== DEFAULT_LOCALE);
const SITE_DIR = path.dirname(fileURLToPath(import.meta.url));
const STATIC_DIRS = [path.join(SITE_DIR, 'static')];
const MARKDOWN_SOURCE_ROOTS = [
  path.join(SITE_DIR, 'versioned_docs'),
  ...LOCALIZED_ROUTE_PREFIXES.map((locale) =>
    path.join(SITE_DIR, 'i18n', locale, 'docusaurus-plugin-content-docs'),
  ),
];
const MARKDOWN_ASSET_ROOTS = [...MARKDOWN_SOURCE_ROOTS, ...STATIC_DIRS];
const SITEMAP_LASTMOD = process.env.DOCUSAURUS_SITEMAP_LASTMOD === '0' ? null : 'date';
const DOCS_LATEST_REDIRECT_SCRIPT = `
(function () {
  var latest = ${JSON.stringify(LATEST_STABLE)};
  var versions = ${JSON.stringify(versions)};
  var locales = ${JSON.stringify(LOCALIZED_ROUTE_PREFIXES)};
  var parts = window.location.pathname.replace(/^\\/+|\\/+$/g, '').split('/').filter(Boolean);
  var locale = locales.indexOf(parts[0]) >= 0 ? parts.shift() : '';

  if (parts[0] !== 'docs') return;

  parts.shift();

  if (parts.length === 0) {
    window.location.replace('/' + (locale ? locale + '/' : '') + 'docs/' + latest + window.location.search + window.location.hash);
    return;
  }

  if (versions.indexOf(parts[0]) >= 0) return;

  window.location.replace('/' + (locale ? locale + '/' : '') + 'docs/' + latest + '/' + parts.join('/') + window.location.search + window.location.hash);
})();
`;

const config: Config = {
  title: 'Laravel',
  tagline: '라라벨',
  favicon: 'img/favicon.png',

  // Set the production URL of your site here.
  url: 'https://laravel.chanhyung.kim',
  // Set the /<baseUrl>/ pathname under which your site is served.
  // For GitHub Pages deployment, it is often '/<projectName>/'.
  baseUrl: '/',
  trailingSlash: true,
  headTags: [
    {
      tagName: 'script',
      attributes: {},
      innerHTML: DOCS_LATEST_REDIRECT_SCRIPT,
    },
  ],

  // GitHub Pages deployment config.
  // If you are not using GitHub Pages, you do not need these.
  organizationName: 'letsescape', // Usually your GitHub org/user name.
  projectName: 'laravel-docs', // Usually your repo name.

  onBrokenLinks: 'warn',
  // 실제 브라우저 앵커 동작은 별도 검증 스크립트와 E2E에서 확인
  onBrokenAnchors: 'ignore',

  // Docusaurus 확장 문법({#id}, admonitions 등)과 CommonMark 자동 감지를 위해 detect 유지
  // Blade/Livewire 특수문자는 Prism 코드 블록 내에서 토큰화되므로 실제 렌더링에 영향 없음
  markdown: {
    format: 'detect',
    parseFrontMatter: async ({filePath, fileContent, defaultParseFrontMatter}) => {
      const result = await defaultParseFrontMatter({filePath, fileContent});
      await assertFrontMatterImageAllowed({
        filePath,
        image: result.frontMatter.image,
        sourceRoots: MARKDOWN_SOURCE_ROOTS,
        allowedRoots: MARKDOWN_ASSET_ROOTS,
      });
      return result;
    },
    hooks: {
      onBrokenMarkdownLinks: 'warn',
    },
    mdx1Compat: {
      // 영어 원문 병기 주석(<!-- ... -->)은 빌드 산출물에 노출하지 않는 소스 전용 메타데이터
      // `comments: true`이면 remark 단계에서 주석 제거
      // 주석 본문의 `*/`(예: addSelect(DB::raw(/* ... */)))로 인한 MDX(JSX {/* */}) 파싱 오류 방지
      // verify.py는 원시 소스를 읽으므로 병기 검증에는 영향 없음
      comments: true,
      admonitions: false,
      headingIds: false,
    },
  },

  // Even without internationalization, you can use this field to set useful metadata such as the HTML language.
  // For example, if your site is Chinese, you may want to replace "en" with "zh-Hans".
  i18n: {
    defaultLocale: DEFAULT_LOCALE,
    locales: LOCALES,
    localeConfigs: {
      en: {
        htmlLang: 'en',
        label: 'English',
      },
      ko: {
        htmlLang: 'ko',
        label: '한국어',
      },
      ja: {
        htmlLang: 'ja',
        label: '日本語',
      },
    },
  },

  // 테마 설정
  themes: [],

  plugins: [
    [
      '@docusaurus/plugin-content-docs',
      {
        id: 'default',
        path: `versioned_docs/version-${LATEST_STABLE}`,
        routeBasePath: 'docs',
        sidebarPath: `./versioned_sidebars/version-${LATEST_STABLE}-sidebars.json`,
        // 버전 관리 설정
        includeCurrentVersion: false,
        lastVersion: LATEST_STABLE,
        versions: Object.fromEntries(
          versions.map((v) => [v, {label: v, path: v}]),
        ),
        // 기타 설정
        editUrl: 'https://github.com/letsescape/laravel-docs/tree/main/',
        beforeDefaultRemarkPlugins: [
          [
            validateLocalAssetsPlugin,
            {
              siteDir: SITE_DIR,
              staticDirs: STATIC_DIRS,
              allowedRoots: MARKDOWN_ASSET_ROOTS,
            },
          ],
          anchorMappingPlugin,
        ],
        remarkPlugins: [
          styleJsxCleanupPlugin,
          githubAdmonitionPlugin,
          methodClassPlugin,
          stripPandocAttrsPlugin,
          replacePlaceholdersPlugin,
          autoLanguagePlugin,
        ],
        rehypePlugins: [safeHtmlPlugin],
        // origin/ 하위는 Laravel 원본 보관용
        // `{{version}}` 등의 서버 측 템플릿이 남아 있어 문서로 렌더링하면 링크가 깨지므로 사이트에서 제외
        // documentation.md는 사이드바 시드이므로 문서 페이지에서 제외
        // readme.md는 installation.md의 `slug: /`와 동일한 버전 루트 경로 생성
        // `/docs/<version>/` 중복 라우트 경고를 방지하기 위해 사이트에서 제외
        exclude: [
          '**/origin/**',
          '**/documentation.md',
          '**/readme.md',
          // Docusaurus 기본 exclude 유지
          '**/_*.{js,jsx,ts,tsx,md,mdx}',
          '**/_*/**',
          '**/*.test.{js,jsx,ts,tsx}',
          '**/__tests__/**',
        ],
      },
    ],
  ],

  presets: [
    [
      'classic',
      {
        docs: false, // 플러그인으로 대체
        blog: false,
        sitemap: {
          lastmod: SITEMAP_LASTMOD,
          changefreq: null,
          priority: null,
          filename: 'sitemap.xml',
          ignorePatterns: ['/q/', '/**/q/'],
        },
        gtag: {
          trackingID: 'G-P3YFWCWEBP',
          anonymizeIP: true,
        },
        googleTagManager: {
          containerId: 'GTM-MDN4L5LV',
        },
        theme: {
          customCss: './src/css/custom.css',
        },
      } satisfies Preset.Options,
    ],
  ],

  themeConfig: {
    // 사이트의 기본 OG 이미지(메인 페이지에서는 별도 이미지로 재정의)
    image: 'img/laravel-docs.png',

    // 다크 모드 설정
    colorMode: {
      defaultMode: 'dark',     // 기본 모드는 다크 모드
      disableSwitch: false,    // 테마 전환 스위치 활성화
      respectPrefersColorScheme: true,  // 사용자 시스템 설정 반영
    },

    // SEO 메타데이터(언어 중립 항목만 사용하고 로케일별 메타데이터는 src/theme/Root.tsx에서 처리)
    // og:image와 twitter:image의 기본값은 themeConfig.image이며 페이지별 Head에서 재정의
    metadata: [
      {property: 'og:type', content: 'website'},
      {name: 'twitter:card', content: 'summary_large_image'},
    ],

    // Algolia DocSearch 설정
    algolia: {
      // Algolia provides this application ID.
      appId: 'I09J6O9PPB',
      // The public API key is safe to commit.
      apiKey: '9490c4a274419bf3d76145ab91c89b14',
      indexName: 'laravel-chanhyung',
      // 로케일 및 버전별 검색 필터링
      contextualSearch: true,
      // 검색 결과 페이지 경로 설정
      searchPagePath: 'q',
      // 사용자 검색 분석 기능 활성화
      insights: true,
    },

    navbar: {
      logo: {
        alt: 'Laravel Logo',
        src: 'img/title_large.svg',
        srcDark: 'img/title_large.svg',
        className: 'navbar-logo',
      },
      items: [
        {
          to: `/docs/${LATEST_STABLE}`,
          position: 'left',
          label: 'Docs',
        },
        {
          type: 'docsVersionDropdown',
          position: 'right',
          className: 'navbar-version-dropdown',
          dropdownItemsAfter: [],
          dropdownActiveClassDisabled: true,
        },
        {
          type: 'localeDropdown',
          position: 'right',
          className: 'navbar-locale-dropdown',
        },

      ],
    },
    footer: {
      style: 'dark',
      logo: {
        alt: 'Laravel Logo',
        src: 'img/title_large.svg',
        href: '/',
        className: 'footer-logo',
      },
      links: [
        {
          title: 'Docs',
          items: [
            {
              label: 'Getting Started',
              to: `/docs/${LATEST_STABLE}`,
            },
            {
              label: 'Architecture Concepts',
              to: `/docs/${LATEST_STABLE}/container`,
            },
          ],
        },
        {
          title: 'Community',
          items: [
            {
              label: 'Laravel Korea',
              href: 'https://laravel.kr',
            },
          ],
        },
      ],
      copyright: `Copyright © 2025 kimchanhyung98. Built with Docusaurus.`,
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
      additionalLanguages: [
        'php',
        'bash',
        'ini',
        'nginx',
        'docker',
        'apacheconf',
        'json',
        'yaml',
        'sql',
        'markup',
      ],
    },
  } satisfies Preset.ThemeConfig,
};

export default config;
