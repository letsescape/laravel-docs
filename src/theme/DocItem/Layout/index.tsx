import React from 'react';
import Layout from '@theme-original/DocItem/Layout';
import type LayoutType from '@theme/DocItem/Layout';
import Head from '@docusaurus/Head';
import {useDoc} from '@docusaurus/plugin-content-docs/client';

type Props = React.ComponentProps<typeof LayoutType>;

export default function LayoutWrapper(props: Props): React.JSX.Element {
  const {metadata} = useDoc();
  const {title, description, permalink} = metadata;

  const structuredData = {
    '@context': 'https://schema.org',
    '@type': 'TechArticle',
    headline: title,
    description,
    url: `https://laravel.chanhyung.kim${permalink}`,
    inLanguage: 'ko',
    publisher: {
      '@type': 'Organization',
      name: 'Laravel 한국어 문서',
      url: 'https://laravel.chanhyung.kim',
    },
    about: {
      '@type': 'SoftwareApplication',
      name: 'Laravel',
      applicationCategory: 'Web Framework',
    },
  };

  return (
    <>
      <Head>
        <script type="application/ld+json">
          {JSON.stringify(structuredData)}
        </script>
      </Head>
      <Layout {...props} />
    </>
  );
}
