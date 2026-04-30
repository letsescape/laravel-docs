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
  const {siteConfig} = useDocusaurusContext();

  // siteConfig.baseUrl은 i18n 로케일별 빌드에서 이미 locale prefix를 포함한다
  // (예: en 빌드 → "/en/"). 별도 localePrefix를 추가로 붙이면 "/en/en/" 같은
  // 이중 prefix가 발생하므로 baseUrl만 신뢰해 normalize한다.
  const baseUrl = siteConfig.baseUrl.endsWith('/')
    ? siteConfig.baseUrl
    : `${siteConfig.baseUrl}/`;
  const target = baseUrl;
  const localizedDocsPath = (slug = '') =>
    `${baseUrl.replace(/\/$/, '')}${docsPath(slug)}`.replace(/\/{2,}/g, '/');

  useEffect(() => {
    const {pathname, search, hash} = window.location;
    const normalizedPath = pathname.replace(/\/+$/, '');
    const docsPrefix = `${baseUrl}docs`.replace(/\/{2,}/g, '/');
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
  }, [baseUrl, target]);

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
