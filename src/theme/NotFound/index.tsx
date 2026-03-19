import React, {type ReactNode, useEffect} from 'react';
import {translate} from '@docusaurus/Translate';
import {PageMetadata} from '@docusaurus/theme-common';
import Layout from '@theme/Layout';
import NotFoundContent from '@theme/NotFound/Content';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';

export default function Index(): ReactNode {
  const title = translate({
    id: 'theme.NotFound.title',
    message: 'Page Not Found',
  });
  const {siteConfig, i18n} = useDocusaurusContext();
  const {currentLocale, defaultLocale} = i18n;

  useEffect(() => {
    const baseUrl = siteConfig.baseUrl.replace(/\/$/, '');
    const localePrefix = currentLocale === defaultLocale ? '' : `/${currentLocale}`;
    const target = `${baseUrl}${localePrefix}/`;

    const timeout = window.setTimeout(() => {
      window.location.replace(target);
    }, 3000);

    return () => window.clearTimeout(timeout);
  }, [currentLocale, defaultLocale, siteConfig.baseUrl]);

  return (
    <>
      <PageMetadata title={title} />
      <Layout>
        <NotFoundContent />
      </Layout>
    </>
  );
}
