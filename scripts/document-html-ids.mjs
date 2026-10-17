import {load} from 'cheerio';

export function collectDocumentHtmlIds(html) {
  const $ = load(html);
  const ids = new Set();
  const bodyIdCounts = new Map();
  $('[id]').each((_, element) => {
    ids.add(element.attribs.id);
  });
  $('.theme-doc-markdown [id]').each((_, element) => {
    const id = element.attribs.id;
    bodyIdCounts.set(id, (bodyIdCounts.get(id) ?? 0) + 1);
  });
  return {ids, bodyIdCounts};
}
