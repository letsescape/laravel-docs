import React, {type ReactNode, useEffect} from 'react';
import {translate} from '@docusaurus/Translate';
import {PageMetadata} from '@docusaurus/theme-common';
import Layout from '@theme/Layout';
import NotFoundContent from '@theme/NotFound/Content';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import {docsPath, docsVersions} from '@site/src/utils/docs';

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
  const localizedDocsPath = (slug = '') =>
    `${baseUrl}${localePrefix}${docsPath(slug)}`.replace(/\/{2,}/g, '/');

  useEffect(() => {
    const {pathname, search, hash} = window.location;
    const normalizedPath = pathname.replace(/\/+$/, '');
    const docsPrefix = `${baseUrl}${localePrefix}/docs`.replace(/\/{2,}/g, '/');
    const docsPrefixWithSlash = `${docsPrefix}/`;

    if (normalizedPath === docsPrefix) {
      window.location.replace(`${localizedDocsPath()}${search}${hash}`);
      return undefined;
    }

    if (normalizedPath.startsWith(docsPrefixWithSlash)) {
      const rest = normalizedPath.slice(docsPrefixWithSlash.length);
      const [maybeVersion] = rest.split('/');

      if (!docsVersions.includes(maybeVersion)) {
        window.location.replace(`${localizedDocsPath(rest)}${search}${hash}`);
        return undefined;
      }

      return undefined;
    }

    const timeout = window.setTimeout(() => {
      window.location.replace(target);
    }, 3000);

    return () => window.clearTimeout(timeout);
  }, [baseUrl, localePrefix, target]);

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
