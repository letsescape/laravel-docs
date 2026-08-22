import React from 'react';
import Head from '@docusaurus/Head';
import Translate, {translate} from '@docusaurus/Translate';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';

const TRANSLATION_IN_PROGRESS_LOCALES = new Set(['en']);

function Root({children}: Readonly<{children: React.ReactNode}>): React.ReactElement {
  const {siteConfig, i18n} = useDocusaurusContext();
  const {currentLocale, defaultLocale} = i18n;
  const siteUrl = siteConfig.url;
  const localePath = currentLocale === defaultLocale ? '' : `/${currentLocale}`;
  const baseUrl = `${siteUrl}${localePath}`;
  const showTranslationBanner = TRANSLATION_IN_PROGRESS_LOCALES.has(currentLocale);

  const keywords = translate({
    id: 'theme.keywords',
    message: '라라벨, Laravel, PHP 프레임워크, PHP artisan, PHP, 웹 개발, 한글 문서, 튜토리얼, 시작하기',
    description: 'The keywords meta tag for the site',
  });

  const siteName = translate({
    id: 'theme.siteName',
    message: 'Laravel 한국어 문서',
    description: 'The site name for JSON-LD structured data',
  });

  const jsonLd = JSON.stringify({
    '@context': 'https://schema.org',
    '@type': 'WebSite',
    name: siteName,
    url: baseUrl,
    potentialAction: {
      '@type': 'SearchAction',
      target: {
        '@type': 'EntryPoint',
        urlTemplate: `${baseUrl}/q?q={search_term_string}`,
      },
      'query-input': 'required name=search_term_string',
    },
  });

  return (
    <>
      <Head>
        <meta property="og:site_name" content={siteName} />
        <meta name="keywords" content={keywords} />
        <script type="application/ld+json">{jsonLd}</script>
      </Head>
      {showTranslationBanner && (
        <div className="translation-banner" role="status">
          <Translate
            id="theme.translationBanner.message"
            description="The message for the translation banner shown on locales that are still being translated"
          >
            This documentation is currently being translated. Some pages may appear in Korean.
          </Translate>
        </div>
      )}
      {children}
    </>
  );
}

export default Root;
