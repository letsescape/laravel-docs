import versions from '@site/versions.json';

export const latestDocsVersion =
  versions.find((version) => version !== 'master') ?? versions[0];

export const docsVersions = versions;

export const docsPath = (slug = ''): string => {
  const normalizedSlug = slug.replace(/^\/+/, '').replace(/\/+$/, '');
  return normalizedSlug
    ? `/docs/${latestDocsVersion}/${normalizedSlug}`
    : `/docs/${latestDocsVersion}`;
};
