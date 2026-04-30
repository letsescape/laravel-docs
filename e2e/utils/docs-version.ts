import versions from '../../versions.json';

export const latestDocsVersion =
  versions.find((version) => version !== 'master') ?? versions[0];

export const stableDocsVersions = versions.filter(
  (version) => version !== 'master',
);

export const docsPathForVersion = (version: string, slug = ''): string => {
  const normalizedSlug = slug.replace(/^\/+/, '').replace(/\/+$/, '');
  return normalizedSlug ? `/docs/${version}/${normalizedSlug}` : `/docs/${version}`;
};

export const docsPath = (slug = ''): string =>
  docsPathForVersion(latestDocsVersion, slug);

export const latestDocsPathPattern = new RegExp(
  `^${docsPath().replaceAll('.', '\\.')}(/|$)`,
);
