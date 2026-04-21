import {themes as prismThemes} from 'prism-react-renderer';
import type {Config} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';
import autoLanguagePlugin from './src/remark/auto-language-plugin';
import replacePlaceholdersPlugin from './src/remark/replace-placeholders';
import anchorMappingPlugin from './src/remark/anchor-mapping';
import githubAdmonitionPlugin from './src/remark/github-admonition';
import styleJsxCleanupPlugin from './src/remark/style-jsx-cleanup';

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

const config: Config = {
  title: 'Laravel',
  tagline: '라라벨',
  favicon: 'img/favicon.png',

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
  // Docusaurus의 broken-anchor 검증기는 heading 텍스트 기반 slug만 수집하고
  // `data.hProperties.id`(anchor-mapping 플러그인이 주입한 실제 HTML id)를 인식하지 못해
  // 대량의 false positive 경고를 낸다. 실제 브라우저 앵커 동작은 HTML id 기반이라 정상.
  // 진짜 broken anchor는 별도 검증 스크립트(scripts/validate-anchors.mjs)로 잡는다.
  onBrokenAnchors: 'ignore',

  // Docusaurus 확장 문법({#id}, admonitions 등)과 CommonMark 자동 감지를 위해 detect 유지.
  // Blade/Livewire 특수문자는 Prism 코드 블록 내에서 토큰화되므로 실제 렌더링에 영향 없음.
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
        remarkPlugins: [
          styleJsxCleanupPlugin,
          githubAdmonitionPlugin,
          anchorMappingPlugin,
          replacePlaceholdersPlugin,
          autoLanguagePlugin,
        ],
        // origin/ 하위는 Laravel 원본 보관용. `{{version}}` 등 서버사이드 템플릿이
        // 남아있어 문서로 렌더링하면 링크가 깨지므로 사이트에서 제외.
        // documentation.md는 사이드바 시드(generate-sidebars.ts가 origin/documentation.md를 읽음)
        // 이며 문서 페이지로 노출할 필요가 없고, 미번역 버전이 링크 깨짐의 원인이 되므로 제외.
        exclude: [
          '**/origin/**',
          '**/documentation.md',
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
