import React from 'react';
import Head from '@docusaurus/Head';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';

const keywordsByLocale: Record<string, string> = {
  ko: '라라벨, Laravel, PHP 프레임워크, PHP artisan, PHP, 웹 개발, 한글 문서, 튜토리얼, 시작하기',
  en: 'Laravel, PHP framework, PHP artisan, PHP, web development, documentation, tutorial, getting started',
  ja: 'Laravel, PHPフレームワーク, PHP artisan, PHP, ウェブ開発, ドキュメント, チュートリアル, はじめに',
};

const bannerMessages: Record<string, string> = {
  en: 'This documentation is currently being translated. Some pages may appear in Korean.',
  ja: 'このドキュメントは現在翻訳中です。一部のページが韓国語で表示される場合があります。',
};

function Root({children}: Readonly<{children: React.ReactNode}>): React.ReactElement {
  const {i18n} = useDocusaurusContext();
  const currentLocale = i18n.currentLocale;
  const keywords = keywordsByLocale[currentLocale] ?? keywordsByLocale.ko;
  const bannerMessage = bannerMessages[currentLocale];

  return (
    <>
      <Head>
        <meta name="keywords" content={keywords} />
      </Head>
      {bannerMessage && <div className="translation-banner">{bannerMessage}</div>}
      {children}
    </>
  );
}

export default Root;
