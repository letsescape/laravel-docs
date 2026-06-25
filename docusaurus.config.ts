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
import versions from './versions.json';

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

// `versions.json`을 단일 출처로 사용해 새 버전 출시 시 한 곳만 갱신하면 footer/navbar/
// lastVersion/path/sidebarPath가 자동으로 따라가도록 한다. master는 임시 버전이므로
// 안정 버전 후보에서 제외하고, 첫 번째 항목을 LATEST_STABLE로 사용한다.
const LATEST_STABLE = versions.find((v) => v !== 'master') ?? versions[0];
const DEFAULT_LOCALE = 'ko';
const LOCALES = ['ko', 'ja'];
const LOCALIZED_ROUTE_PREFIXES = LOCALES.filter((locale) => locale !== DEFAULT_LOCALE);
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

  // Set the production url of your site here
  url: 'https://laravel.chanhyung.kim',
  // Set the /<baseUrl>/ pathname under which your site is served
  // For GitHub pages deployment, it is often '/<projectName>/'
  baseUrl: '/',
  trailingSlash: true,
  headTags: [
    {
      tagName: 'script',
      attributes: {},
      innerHTML: DOCS_LATEST_REDIRECT_SCRIPT,
    },
  ],

  // GitHub pages deployment config.
  // If you aren't using GitHub pages, you don't need these.
  organizationName: 'letsescape', // Usually your GitHub org/user name.
  projectName: 'laravel-docs', // Usually your repo name.

  onBrokenLinks: 'warn',
  // 실제 브라우저 앵커 동작은 별도 검증 스크립트와 e2e에서 확인한다.
  onBrokenAnchors: 'ignore',

  // Docusaurus 확장 문법({#id}, admonitions 등)과 CommonMark 자동 감지를 위해 detect 유지.
  // Blade/Livewire 특수문자는 Prism 코드 블록 내에서 토큰화되므로 실제 렌더링에 영향 없음.
  markdown: {
    format: 'detect',
    hooks: {
      onBrokenMarkdownLinks: 'warn',
    },
    mdx1Compat: {
      // 영어 원문 병기 주석(<!-- ... -->)은 빌드 산출물에 노출하지 않는 소스 전용
      // 메타데이터다. comments:true면 remark 단계에서 주석을 제거해, 주석 본문의
      // `*/`(예: addSelect(DB::raw(/* ... */)))가 MDX(JSX {/* */})를 깨지 않게 한다.
      // verify.py는 raw 소스를 읽으므로 병기 검증에는 영향이 없다.
      comments: true,
      admonitions: false,
      headingIds: false,
    },
  },

  // Even if you don't use internationalization, you can use this field to set
  // useful metadata like html lang. For example, if your site is Chinese, you
  // may want to replace "en" with "zh-Hans".
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
        // origin/ 하위는 Laravel 원본 보관용. `{{version}}` 등 서버사이드 템플릿이
        // 남아있어 문서로 렌더링하면 링크가 깨지므로 사이트에서 제외.
        // documentation.md는 사이드바 시드이며 문서 페이지로 노출할 필요가 없다.
        // readme.md는 installation.md의 `slug: /`와 같은 버전 루트 경로를 만들어
        // `/docs/<version>/` 중복 라우트 경고를 내므로 사이트에서 제외.
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
          ignorePatterns: ['/search', '/search/', '/**/search', '/**/search/'],
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
    // OG 이미지 사이트 기본값 (메인 페이지에서는 별도 이미지로 오버라이드)
    image: 'img/laravel-docs.png',

    // 다크 모드 설정
    colorMode: {
      defaultMode: 'dark',     // 기본 모드를 다크로 설정
      disableSwitch: false,    // 테마 전환 스위치 활성화
      respectPrefersColorScheme: true,  // 사용자 시스템 설정 존중
    },

    // SEO 메타데이터 (언어 중립 항목만, 로케일별 메타데이터는 src/theme/Root.tsx에서 처리)
    // og:image/twitter:image는 themeConfig.image가 기본값으로 제공하며, 페이지별로 Head에서 오버라이드
    metadata: [
      {property: 'og:type', content: 'website'},
      {name: 'twitter:card', content: 'summary_large_image'},
    ],

    // Algolia DocSearch 설정
    algolia: {
      // The application ID provided by Algolia
      appId: 'I09J6O9PPB',
      // Public API key: it is safe to commit it
      apiKey: '9490c4a274419bf3d76145ab91c89b14',
      indexName: 'laravel-chanhyung',
      // 로케일 및 버전별 검색 필터링
      contextualSearch: true,
      // 검색 결과 페이지 경로 설정
      searchPagePath: 'search',
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
