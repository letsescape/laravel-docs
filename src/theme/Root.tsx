import React from 'react';
import Head from '@docusaurus/Head';
import Translate, {translate} from '@docusaurus/Translate';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';

function Root({children}: Readonly<{children: React.ReactNode}>): React.ReactElement {
  const {i18n} = useDocusaurusContext();
  const {currentLocale, defaultLocale} = i18n;

  const keywords = translate({
    id: 'theme.keywords',
    message: '라라벨, Laravel, PHP 프레임워크, PHP artisan, PHP, 웹 개발, 한글 문서, 튜토리얼, 시작하기',
    description: 'The keywords meta tag for the site',
  });

  return (
    <>
      <Head>
        <meta name="keywords" content={keywords} />
      </Head>
      {currentLocale !== defaultLocale && (
        <div className="translation-banner">
          <Translate
            id="theme.translationBanner.message"
            description="The message for the translation banner shown on non-default locale pages"
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
