import path from 'node:path';
import {pathToFileURL} from 'node:url';

export default async function chatPublication(context) {
  const revision = process.env.LARAVEL_CHAT_PUBLICATION_REVISION;
  if (revision?.length !== 40 || !/^[a-f0-9]{40}$/.test(revision)) {
    throw new Error('LARAVEL_CHAT_PUBLICATION_REVISION에는 40자리 원문 revision을 지정하세요.');
  }
  const repoDir = process.env.LARAVEL_CHAT_REPO ?? path.resolve(context.siteDir, '../laravel-chat');
  const pluginUrl = pathToFileURL(path.resolve(repoDir, 'demo/publication-plugin.mjs'));
  const {default: publicationPlugin} = await import(pluginUrl.href);
  return publicationPlugin(context, {sourceDir: context.siteDir, revision});
}
