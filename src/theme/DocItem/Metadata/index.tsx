import React, {type ReactNode} from 'react';
import {PageMetadata} from '@docusaurus/theme-common';
import {useDoc} from '@docusaurus/plugin-content-docs/client';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';

export default function DocItemMetadata(): ReactNode {
  const {metadata, frontMatter, assets} = useDoc();
  const {i18n: {currentLocale}} = useDocusaurusContext();
  const language = currentLocale === 'ja' ? '日本語ドキュメント' : '한국어 문서';
  const title = `${metadata.title} — Laravel ${metadata.version} ${language}`;

  return (
    <PageMetadata
      description={metadata.description}
      keywords={frontMatter.keywords}
      image={assets.image ?? frontMatter.image}
    >
      <title>{title}</title>
      <meta property="og:title" content={title} />
    </PageMetadata>
  );
}
