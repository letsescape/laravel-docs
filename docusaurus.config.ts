import {themes as prismThemes} from 'prism-react-renderer';
import type {Config} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';
import autoLanguagePlugin from './src/remark/auto-language-plugin';

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

const siteName = 'Laravel 한국어 문서';

const config: Config = {
  title: 'Laravel',
  tagline: '라라벨',
  favicon: 'img/favicon.png',

  headTags: [
    {
      tagName: 'script',
      attributes: {
        type: 'application/ld+json',
      },
      innerHTML: JSON.stringify({
        '@context': 'https://schema.org',
        '@type': 'WebSite',
        name: siteName,
        url: 'https://laravel.chanhyung.kim',
        potentialAction: {
          '@type': 'SearchAction',
          target: {
            '@type': 'EntryPoint',
            urlTemplate: 'https://laravel.chanhyung.kim/search?q={search_term_string}',
          },
          'query-input': 'required name=search_term_string',
        },
      }),
    },
  ],

  // Set the production url of your site here
  url: 'https://laravel.chanhyung.kim',
  // Set the /<baseUrl>/ pathname under which your site is served
  // For GitHub pages deployment, it is often '/<projectName>/'
  baseUrl: '/',

  // GitHub pages deployment config.
  // If you aren't using GitHub pages, you don't need these.
  organizationName: 'letsescape', // Usually your GitHub org/user name.
  projectName: 'laravel-docs-web', // Usually your repo name.

  onBrokenLinks: 'warn',
  onBrokenMarkdownLinks: 'warn',

  // MDX 파싱 오류를 무시하도록 설정
  markdown: {
    format: 'detect',
    mdx1Compat: {
      comments: false,
      admonitions: false,
      headingIds: false,
    },
  },

  // Even if you don't use internationalization, you can use this field to set
  // useful metadata like html lang. For example, if your site is Chinese, you
  // may want to replace "en" with "zh-Hans".
  i18n: {
    defaultLocale: 'ko',
    locales: ['en', 'ko', 'ja'],
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
        path: 'versioned_docs/version-12.x',
        routeBasePath: 'docs',
        sidebarPath: './versioned_sidebars/version-12.x-sidebars.json',
        // 버전 관리 설정
        includeCurrentVersion: false,
        lastVersion: '12.x',
        versions: {
          '12.x': {
            label: '12.x',
            path: '12.x',
          },
          '11.x': {
            label: '11.x',
            path: '11.x',
          },
          '10.x': {
            label: '10.x',
            path: '10.x',
          },
          '9.x': {
            label: '9.x',
            path: '9.x',
          },
          '8.x': {
            label: '8.x',
            path: '8.x',
          },
        },
        // 기타 설정
        editUrl: 'https://github.com/letsescape/laravel-docs-web/tree/main/',
        remarkPlugins: [autoLanguagePlugin],
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
          lastmod: 'date',
          changefreq: null,
          priority: null,
          filename: 'sitemap.xml',
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
    // OG 이미지 기본값 (문서 페이지에 적용)
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
      {property: 'og:site_name', content: siteName},
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
      title: null,
      logo: {
        alt: 'Laravel Logo',
        src: 'img/title_large.svg',
        srcDark: 'img/title_large.svg',
        className: 'navbar-logo',
      },
      items: [
        {
          to: '/docs/12.x',
          position: 'left',
          label: 'Docs',
        },
        {
          type: 'docsVersionDropdown',
          position: 'right',
          dropdownItemsAfter: [],
          dropdownActiveClassDisabled: true,
        },
        {
          type: 'localeDropdown',
          position: 'right',
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
              to: '/docs/12.x',
            },
            {
              label: 'Architecture Concepts',
              to: '/docs/12.x/container',
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
