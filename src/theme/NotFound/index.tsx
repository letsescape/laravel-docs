import React, {type ReactNode, useEffect} from 'react';
import {translate} from '@docusaurus/Translate';
import {PageMetadata} from '@docusaurus/theme-common';
import Layout from '@theme/Layout';
import NotFoundContent from '@theme/NotFound/Content';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';

export default function NotFound(): ReactNode {
  const title = translate({
    id: 'theme.NotFound.title',
    message: 'Page Not Found',
  });
  const {siteConfig, i18n} = useDocusaurusContext();
  const {currentLocale, defaultLocale} = i18n;

  const baseUrl = siteConfig.baseUrl.replace(/\/$/, '');
  const localePrefix =
    currentLocale === defaultLocale ? '' : `/${currentLocale}`;
  const target = `${baseUrl}${localePrefix}/`;

  useEffect(() => {
    const timeout = window.setTimeout(() => {
      window.location.replace(target);
    }, 3000);

    return () => window.clearTimeout(timeout);
  }, [target]);

  return (
    <>
      <PageMetadata title={title} />
      <Layout>
        <NotFoundContent />
        <div className="container margin-top--md margin-bottom--lg">
          <a href={target}>
            {translate({
              id: 'theme.NotFound.goHome',
              message: 'Go to main page →',
            })}
          </a>
        </div>
      </Layout>
    </>
  );
}
