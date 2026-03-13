import React, {type ReactNode} from 'react';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import {translate} from '@docusaurus/Translate';
import Layout from '@theme/Layout';
import Head from '@docusaurus/Head';

import Hero from '@site/src/components/Hero';
import Features from '@site/src/components/Features';
import CodeExamples from '@site/src/components/CodeExamples';

export default function Home(): ReactNode {
  const {siteConfig, i18n} = useDocusaurusContext();
  const {url} = siteConfig;
  const {currentLocale, defaultLocale} = i18n;
  const pageUrl = currentLocale === defaultLocale ? url : `${url}/${currentLocale}`;

  const title = translate({
    id: 'homepage.title',
    message: '라라벨 - 웹 장인을 위한 PHP 프레임워크',
    description: 'The title for the homepage',
  });
  const description = translate({
    id: 'homepage.description',
    message: '라라벨은 표현력이 풍부하고 우아한 문법을 갖춘 PHP 웹 애플리케이션 프레임워크입니다. 사소한 부분에 얽매이지 않고 창작에만 집중할 수 있습니다.',
    description: 'The description for the homepage',
  });
  const imageAlt = translate({
    id: 'homepage.imageAlt',
    message: '라라벨 - 웹 장인을 위한 PHP 프레임워크',
    description: 'The image alt text for the homepage',
  });

  return (
    <Layout title={title} description={description}>
      <Head>
        <link rel="canonical" href={pageUrl} />

        <meta property="og:title" content={title} />
        <meta property="og:description" content={description} />
        <meta property="og:url" content={pageUrl} />
        <meta property="og:site_name" content={siteConfig.title} />
        {/* 메인 페이지 전용 OG 이미지 (laravel-home.png: 2400x1260, 문서 페이지 기본값: 1200x630) */}
        <meta property="og:image" content={`${url}/img/laravel-home.png`} />
        <meta property="og:image:alt" content={imageAlt} />
        <meta property="og:image:width" content="2400" />
        <meta property="og:image:height" content="1260" />

        <meta name="twitter:title" content={title} />
        <meta name="twitter:description" content={description} />
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
