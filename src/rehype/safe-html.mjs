import {visit} from 'unist-util-visit';

const safeElements = new Set([
  'a',
  'abbr',
  'b',
  'bdi',
  'bdo',
  'blockquote',
  'br',
  'caption',
  'cite',
  'code',
  'col',
  'colgroup',
  'data',
  'dd',
  'del',
  'details',
  'dfn',
  'div',
  'dl',
  'dt',
  'em',
  'figcaption',
  'figure',
  'h1',
  'h2',
  'h3',
  'h4',
  'h5',
  'h6',
  'hr',
  'i',
  'img',
  'input',
  'ins',
  'kbd',
  'li',
  'mark',
  'ol',
  'p',
  'pre',
  'q',
  'rp',
  'rt',
  'ruby',
  's',
  'samp',
  'section',
  'small',
  'span',
  'strong',
  'sub',
  'summary',
  'sup',
  'table',
  'tbody',
  'td',
  'tfoot',
  'th',
  'thead',
  'time',
  'tr',
  'u',
  'ul',
  'var',
  'wbr',
]);

const globalProperties = new Set([
  'className',
  'dir',
  'hidden',
  'id',
  'lang',
  'role',
  'tabIndex',
  'title',
]);

const elementProperties = new Map([
  ['a', new Set(['href', 'name', 'rel', 'target'])],
  ['blockquote', new Set(['cite'])],
  ['code', new Set(['metastring'])],
  ['col', new Set(['span'])],
  ['colgroup', new Set(['span'])],
  ['data', new Set(['value'])],
  ['del', new Set(['cite', 'dateTime'])],
  ['details', new Set(['open'])],
  ['div', new Set(['markdown'])],
  ['img', new Set(['alt', 'decoding', 'height', 'loading', 'src', 'width'])],
  ['input', new Set(['checked', 'disabled', 'type'])],
  ['ins', new Set(['cite', 'dateTime'])],
  ['li', new Set(['value'])],
  ['ol', new Set(['reversed', 'start', 'type'])],
  ['p', new Set(['align'])],
  ['q', new Set(['cite'])],
  ['td', new Set(['align', 'colSpan', 'headers', 'rowSpan'])],
  ['th', new Set(['align', 'colSpan', 'headers', 'rowSpan', 'scope'])],
  ['time', new Set(['dateTime'])],
]);

const isCustomDataProperty = (property) =>
  /^(?:aria|data)(?:[A-Z][A-Za-z0-9]*|-[a-z][a-z0-9_.:-]*)$/.test(property);

const safeUrl = (value, {image = false} = {}) => {
  if (typeof value !== 'string' || /[\u0000-\u001f\u007f\\]/.test(value)) {
    return false;
  }
  const normalized = value.trim();
  if (normalized.startsWith('//')) {
    return false;
  }
  const scheme = normalized.match(/^([a-z][a-z0-9+.-]*):/i)?.[1]?.toLowerCase();
  if (!scheme) {
    return true;
  }
  if (image && scheme === 'data') {
    return /^data:image\/(?:gif|jpe?g|png|webp);base64,[a-z0-9+/=\r\n]+$/i.test(
      normalized,
    );
  }
  return image
    ? ['http', 'https'].includes(scheme)
    : ['http', 'https', 'mailto', 'tel'].includes(scheme);
};

const unsafeHtml = (node, filePath, detail) => {
  const line = node.position?.start?.line;
  const location = line ? `${filePath}:${line}` : filePath;
  return new Error(`unsafe raw HTML in ${location}: ${detail}`);
};

export const assertSafeHtmlElement = (node, filePath = '<Markdown>') => {
  if (!safeElements.has(node.tagName)) {
    throw unsafeHtml(node, filePath, `<${node.tagName}> is not allowed`);
  }

  for (const [property, value] of Object.entries(node.properties ?? {})) {
    const allowed =
      globalProperties.has(property) ||
      isCustomDataProperty(property) ||
      elementProperties.get(node.tagName)?.has(property);
    if (!allowed) {
      throw unsafeHtml(
        node,
        filePath,
        `${property} is not allowed on <${node.tagName}>`,
      );
    }
    if (
      ['href', 'cite'].includes(property) &&
      !safeUrl(value)
    ) {
      throw unsafeHtml(node, filePath, `${property} has an unsafe URL`);
    }
    if (property === 'src' && !safeUrl(value, {image: true})) {
      throw unsafeHtml(node, filePath, 'src has an unsafe URL');
    }
  }

  if (
    node.tagName === 'input' &&
    (node.properties?.type !== 'checkbox' || node.properties?.disabled !== true)
  ) {
    throw unsafeHtml(node, filePath, 'only disabled checkbox inputs are allowed');
  }
};

export default function safeHtmlPlugin() {
  return (tree, file) => {
    const filePath = String(file.path || '<Markdown>');
    visit(tree, 'element', (node) => {
      assertSafeHtmlElement(node, filePath);
    });
  };
}
