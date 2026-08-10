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

  // siteConfig.baseUrl은 로케일별 빌드에서 이미 로케일 접두사 포함
  // 예: ja 빌드 → "/ja/"
  // 별도의 로케일 접두사 추가 시 "/ja/ja/"와 같은 이중 접두사 발생
  // 따라서 baseUrl만 사용해 정규화
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
