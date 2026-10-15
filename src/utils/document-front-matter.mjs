import {extname} from 'node:path';
import {DEFAULT_PARSE_FRONT_MATTER} from '@docusaurus/utils';

export const parseDocumentFrontMatter = async ({
  filePath,
  fileContent,
  defaultParseFrontMatter = DEFAULT_PARSE_FRONT_MATTER,
}) => {
  if (extname(filePath) !== '.md') {
    throw new Error(`Documents must use the .md extension: ${filePath}`);
  }

  const content = fileContent.replace(/^\uFEFF/, '');
  if (content.startsWith('---') && !content.startsWith('----')) {
    const language = content.slice(3).split(/\r?\n/, 1)[0].trim().toLowerCase();
    if (!['', 'yaml', 'yml', 'json'].includes(language)) {
      throw new Error(`Unsupported front matter language in ${filePath}`);
    }
  }

  const result = await defaultParseFrontMatter({filePath, fileContent});
  if (result.frontMatter.mdx?.format !== undefined) {
    throw new Error(`Document-controlled MDX format is not allowed: ${filePath}`);
  }
  return result;
};
