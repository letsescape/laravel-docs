import React, {type ReactNode, useEffect} from 'react';
import {translate} from '@docusaurus/Translate';
import {useHistory} from '@docusaurus/router';
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
  const history = useHistory();

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
    let {pathname, search, hash} = window.location;

    if (pathname === `${baseUrl}404.html`) {
      const from = new URLSearchParams(search).get('from');
      if (from?.startsWith(baseUrl)) {
        try {
          const original = new URL(from, window.location.origin);
          if (original.origin === window.location.origin && original.pathname.startsWith(baseUrl)) {
            ({pathname, search, hash} = original);
            history.replace(`${pathname}${search}${hash}`);
          }
        } catch {
          // 잘못된 복귀 주소는 무시하고 현재 로케일의 404 안내를 유지한다.
        }
      }
    }

    // GitHub Pages는 모든 누락 경로에 기본 로케일의 404.html을 제공한다.
    const locale = i18n.locales.find((candidate) => candidate !== i18n.defaultLocale &&
      pathname.startsWith(i18n.localeConfigs[candidate].baseUrl)) ?? i18n.defaultLocale;
    if (locale !== i18n.currentLocale) {
      const localized404 = `${i18n.localeConfigs[locale].baseUrl}404.html`;
      window.location.replace(`${localized404}?from=${encodeURIComponent(`${pathname}${search}${hash}`)}`);
      return undefined;
    }

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
  }, [baseUrl, target, history, i18n]);

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
