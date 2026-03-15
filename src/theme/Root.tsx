import React, {lazy, Suspense} from 'react';
import Head from '@docusaurus/Head';
import Translate, {translate} from '@docusaurus/Translate';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import ChatBotErrorBoundary from '@site/src/components/ChatBot/ChatBotErrorBoundary';

const ChatBot = lazy(() => import('@site/src/components/ChatBot'));

function Root({children}: Readonly<{children: React.ReactNode}>): React.ReactElement {
  const {siteConfig, i18n} = useDocusaurusContext();
  const {currentLocale, defaultLocale} = i18n;
  const siteUrl = siteConfig.url;
  const localePath = currentLocale === defaultLocale ? '' : `/${currentLocale}`;
  const baseUrl = `${siteUrl}${localePath}`;

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
        urlTemplate: `${baseUrl}/search?q={search_term_string}`,
      },
      'query-input': 'required name=search_term_string',
    },
  });

  return (
    <>
      <Head>
        <meta name="keywords" content={keywords} />
        <script type="application/ld+json">{jsonLd}</script>
      </Head>
      {currentLocale !== defaultLocale && (
        <div className="translation-banner" role="status">
          <Translate
            id="theme.translationBanner.message"
            description="The message for the translation banner shown on non-default locale pages"
          >
            This documentation is currently being translated. Some pages may appear in Korean.
          </Translate>
        </div>
      )}
      {children}
      <ChatBotErrorBoundary>
        <Suspense fallback={null}>
          <ChatBot />
        </Suspense>
      </ChatBotErrorBoundary>
    </>
  );
}

export default Root;
