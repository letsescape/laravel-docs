import React, {useEffect, type ReactNode} from 'react';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import {translate} from '@docusaurus/Translate';
import Layout from '@theme/Layout';
import Head from '@docusaurus/Head';

import HeroSection from '@site/src/components/Homepage/HeroSection';
import {AIFrameworkSection} from '@site/src/components/Homepage/FrameworkSection';
import FrameworkSection from '@site/src/components/Homepage/FrameworkSection';
import CloudSection from '@site/src/components/Homepage/CloudSection';
import NightwatchSection from '@site/src/components/Homepage/NightwatchSection';
import FrontendSection from '@site/src/components/Homepage/FrontendSection';
import CTASection from '@site/src/components/Homepage/CTASection';
import EventsSection from '@site/src/components/Homepage/EventsSection';

import '@site/src/components/Homepage/homepage.css';

export default function Home(): ReactNode {
  const {siteConfig, i18n} = useDocusaurusContext();
  const {url} = siteConfig;
  const {currentLocale, defaultLocale} = i18n;
  const pageUrl = currentLocale === defaultLocale ? url : `${url}/${currentLocale}/`;

  const title = translate({
    id: 'homepage.title',
    message: 'Laravel 한국어 문서',
    description: 'The title for the homepage',
  });
  const description = translate({
    id: 'homepage.description',
    message: 'Laravel 한국어 문서. 설치, 라우팅, 인증, Eloquent ORM 등 주요 기능 안내.',
    description: 'The description for the homepage',
  });
  const imageAlt = translate({
    id: 'homepage.imageAlt',
    message: 'Laravel 한국어 문서',
    description: 'The image alt text for the homepage',
  });

  useEffect(() => {
    document.body.classList.add('homepage-layout');
    return () => {
      document.body.classList.remove('homepage-layout');
    };
  }, []);

  return (
    <Layout description={description}>
      <Head>
        <title>{title}</title>
        <link rel="canonical" href={pageUrl} />
        <meta property="og:title" content={title} />
        <meta property="og:description" content={description} />
        <meta property="og:url" content={pageUrl} />
        <meta property="og:image" content={`${url}/img/laravel-home.png`} />
        <meta property="og:image:alt" content={imageAlt} />
        <meta property="og:image:width" content="2400" />
        <meta property="og:image:height" content="1260" />
        <meta name="twitter:title" content={title} />
        <meta name="twitter:description" content={description} />
        <meta name="twitter:image" content={`${url}/img/laravel-home.png`} />
      </Head>
      <main className="homepage">
        <HeroSection />
        <div className="hp-bordered-wrapper">
          <AIFrameworkSection />
          <FrameworkSection />
          <CloudSection />
          <div className="nw-fe-row">
            <NightwatchSection />
            <FrontendSection />
          </div>
          <CTASection />
          <EventsSection />
        </div>
      </main>
    </Layout>
  );
}
