import React from 'react';
import Head from '@docusaurus/Head';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';

const seoByLocale: Record<string, {keywords: string; description: string; title: string}> = {
  ko: {
    keywords: '라라벨, Laravel, PHP 프레임워크, 웹 개발, 한글 문서, 튜토리얼, 시작하기',
    description: '라라벨 프레임워크의 설치 방법, 기본 사용법, 주요 기능들을 한글로 쉽게 배우고 시작하세요.',
    title: '라라벨 한국어 문서 - PHP 웹 프레임워크',
  },
  en: {
    keywords: 'Laravel, PHP framework, web development, documentation, tutorial, getting started',
    description: 'Learn how to install, configure, and use the Laravel PHP framework with comprehensive documentation.',
    title: 'Laravel Documentation - PHP Web Framework',
  },
  ja: {
    keywords: 'Laravel, PHPフレームワーク, ウェブ開発, ドキュメント, チュートリアル, はじめに',
    description: 'LaravelのPHPフレームワークのインストール方法、基本的な使い方、主な機能を日本語で学びましょう。',
    title: 'Laravel日本語ドキュメント - PHPウェブフレームワーク',
  },
};

const bannerStyle: React.CSSProperties = {
  background: '#fef3cd',
  color: '#856404',
  padding: '8px 16px',
  textAlign: 'center',
  fontSize: '14px',
  borderBottom: '1px solid #ffc107',
};

const bannerMessages: Record<string, string> = {
  en: 'This documentation is currently being translated. Some pages may appear in Korean.',
  ja: 'このドキュメントは現在翻訳中です。一部のページが韓国語で表示される場合があります。',
};

function Root({children}: {children: React.ReactNode}): React.ReactElement {
  const {i18n} = useDocusaurusContext();
  const currentLocale = i18n.currentLocale;
  const seo = seoByLocale[currentLocale] ?? seoByLocale.ko;
  const bannerMessage = bannerMessages[currentLocale];

  return (
    <>
      <Head>
        <meta name="keywords" content={seo.keywords} />
        <meta name="description" content={seo.description} />
        <meta property="og:title" content={seo.title} />
        <meta property="og:description" content={seo.description} />
        <meta name="twitter:title" content={seo.title} />
        <meta name="twitter:description" content={seo.description} />
      </Head>
      {bannerMessage && <div style={bannerStyle}>{bannerMessage}</div>}
      {children}
    </>
  );
}

export default Root;
