import path from 'node:path';
import {unified} from 'unified';
import remarkParse from 'remark-parse';

const parser = unified().use(remarkParse);

function plainText(node) {
  if (node.type === 'text' || node.type === 'inlineCode') return node.value;
  if (node.type === 'break') return ' ';
  if (node.type === 'html' || node.type === 'image' || node.type === 'imageReference') return '';
  return (node.children ?? []).map(plainText).join('');
}

const normalizeText = (node) => plainText(node).replace(/\s+/g, ' ').trim();

export function addDocumentSeo({filePath, siteDir, result}) {
  const relativePath = path.relative(siteDir, filePath).split(path.sep).join('/');
  const match = /^(?:versioned_docs|i18n\/(ko|ja)\/docusaurus-plugin-content-docs)\/version-([^/]+)\/(.+)\.md$/.exec(relativePath);
  if (!match || match[3].split('/').some((part) => part.startsWith('_') || part === 'origin') ||
      ['documentation', 'readme'].includes(match[3].split('/').at(-1))) return result;

  const {frontMatter, content} = result;
  if (frontMatter.title != null && frontMatter.description != null) return result;
  const locale = match[1] ?? 'ko';
  const isLicense = match[3] === 'license';
  const tree = parser.parse(content);
  const heading = tree.children.find((node) => node.type === 'heading');
  const title = heading?.depth === 1
    ? normalizeText(heading).replace(/\s*\{#[\w-]+\}\s*$/, '')
    : isLicense ? 'License' : undefined;
  const description = isLicense
    ? locale === 'ja'
      ? 'Laravel の MIT ライセンス。ソフトウェアの利用、複製、変更、配布に関する許諾条件と免責事項。'
      : 'Laravel의 MIT 라이선스입니다. 소프트웨어 사용, 복제, 수정, 배포의 허용 조건과 면책 조항을 안내합니다.'
    : tree.children.filter((node) => node.type === 'paragraph').map(normalizeText)
      .find((text) => text && !/^(?:영향 가능성|영향도|影響の可能性|Likelihood [Oo]f [Ii]mpact)\s*[:：]/.test(text));

  return {
    ...result,
    frontMatter: {
      ...frontMatter,
      ...(frontMatter.title == null && title ? {title} : {}),
      ...(frontMatter.description == null && description ? {description} : {}),
    },
  };
}
