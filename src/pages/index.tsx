import React, {type ReactNode} from 'react';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import Head from '@docusaurus/Head';

import Hero from '@site/src/components/Hero';
import Features from '@site/src/components/Features';
import CodeExamples from '@site/src/components/CodeExamples';

const homePageMeta: Record<string, {title: string; description: string; imageAlt: string}> = {
  ko: {
    title: '라라벨 - 웹 장인을 위한 PHP 프레임워크',
    description: '라라벨은 표현력이 풍부하고 우아한 문법을 갖춘 PHP 웹 애플리케이션 프레임워크입니다. 사소한 부분에 얽매이지 않고 창작에만 집중할 수 있습니다.',
    imageAlt: '라라벨 - 웹 장인을 위한 PHP 프레임워크',
  },
  en: {
    title: 'Laravel - The PHP Framework for Web Artisans',
    description: 'Laravel is a PHP web application framework with expressive, elegant syntax. Focus on creating without sweating the small things.',
    imageAlt: 'Laravel - The PHP Framework for Web Artisans',
  },
  ja: {
    title: 'Laravel - ウェブ職人のためのPHPフレームワーク',
    description: 'Laravelは表現力豊かでエレガントな構文を持つPHPウェブアプリケーションフレームワークです。細かいことに悩まず、創作に集中できます。',
    imageAlt: 'Laravel - ウェブ職人のためのPHPフレームワーク',
  },
};

export default function Home(): ReactNode {
  const {siteConfig, i18n} = useDocusaurusContext();
  const {url} = siteConfig;
  const currentLocale = i18n.currentLocale;
  const defaultLocale = i18n.defaultLocale;
  const meta = homePageMeta[currentLocale] ?? homePageMeta[defaultLocale];
  const pageUrl = currentLocale === defaultLocale ? url : `${url}/${currentLocale}`;

  return (
    <Layout title={meta.title} description={meta.description}>
      <Head>
        <link rel="canonical" href={pageUrl} />

        <meta property="og:type" content="website" />
        <meta property="og:title" content={meta.title} />
        <meta property="og:description" content={meta.description} />
        <meta property="og:url" content={pageUrl} />
        <meta property="og:site_name" content={siteConfig.title} />
        <meta property="og:image" content={`${url}/img/laravel-home.png`} />
        <meta property="og:image:alt" content={meta.imageAlt} />

        <meta name="twitter:card" content="summary_large_image" />
        <meta name="twitter:title" content={meta.title} />
        <meta name="twitter:description" content={meta.description} />
        <meta name="twitter:image" content={`${url}/img/laravel-home.png`} />
      </Head>
      <main>
        <Hero />
        <Features />
        <CodeExamples />
      </main>
    </Layout>
  );
}
