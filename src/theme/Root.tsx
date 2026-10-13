import React from 'react';
import Head from '@docusaurus/Head';
import Translate, {translate} from '@docusaurus/Translate';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';

const TRANSLATION_IN_PROGRESS_LOCALES = new Set(['en']);

function Root({children}: Readonly<{children: React.ReactNode}>): React.ReactElement {
  const {siteConfig, i18n} = useDocusaurusContext();
  const {currentLocale} = i18n;
  const showTranslationBanner = TRANSLATION_IN_PROGRESS_LOCALES.has(currentLocale);

  const siteName = translate({
    id: 'theme.siteName',
    message: 'Laravel 한국어 문서',
    description: 'The localized Open Graph site name',
  });

  const jsonLd = JSON.stringify({
    '@context': 'https://schema.org',
    '@type': 'WebSite',
    name: 'Laravel Docs',
    url: new URL('/', siteConfig.url).href,
  });

  return (
    <>
      <Head>
        <meta property="og:site_name" content={siteName} />
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
