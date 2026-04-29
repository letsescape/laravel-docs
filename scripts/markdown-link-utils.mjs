function fenceAt(src, index) {
  if (src.startsWith('```', index)) return '```';
  if (src.startsWith('~~~', index)) return '~~~';
  return null;
}

function findInlineCodeEnd(src, index) {
  const end = src.indexOf('`', index + 1);
  if (end < 0) return -1;

  const newline = src.indexOf('\n', index + 1);
  if (newline >= 0 && newline < end) return -1;

  return end;
}

function versionReplacement(version) {
  if (version === null) return '';
  return version;
}

export function stripCode(src) {
  let out = '';
  let i = 0;
  while (i < src.length) {
    const fence = fenceAt(src, i);
    if (fence) {
      const end = src.indexOf(fence, i + fence.length);
      if (end < 0) return out;
      i = end + fence.length;
      continue;
    }
    if (src[i] === '`') {
      const end = findInlineCodeEnd(src, i);
      if (end < 0) {
        out += src[i++];
        continue;
      }
      i = end + 1;
      continue;
    }
    out += src[i++];
  }
  return out;
}

function stripTitleSuffix(raw) {
  let inPlaceholder = false;

  for (let i = 0; i < raw.length; i++) {
    if (!inPlaceholder && raw.startsWith('{{', i)) {
      inPlaceholder = true;
      i++;
      continue;
    }
    if (inPlaceholder && raw.startsWith('}}', i)) {
      inPlaceholder = false;
      i++;
      continue;
    }

    const char = raw[i];
    if (
      !inPlaceholder &&
      (char === ' ' || char === '\t' || char === '\n' || char === '\r')
    ) {
      return raw.slice(0, i);
    }
  }
  return raw;
}

export function extractMarkdownLinks(text) {
  const stripped = stripCode(text);
  const links = [];
  let i = 0;

  while (i < stripped.length) {
    const labelStart = stripped.indexOf('[', i);
    if (labelStart < 0) break;

    const labelEnd = stripped.indexOf(']', labelStart + 1);
    if (labelEnd < 0) break;
    if (stripped[labelEnd + 1] !== '(') {
      i = labelEnd + 1;
      continue;
    }

    const urlEnd = stripped.indexOf(')', labelEnd + 2);
    if (urlEnd < 0) break;

    const url = stripTitleSuffix(stripped.slice(labelEnd + 2, urlEnd));
    if (url) {
      links.push({
        text: stripped.slice(labelStart + 1, labelEnd),
        url,
      });
    }
    i = urlEnd + 1;
  }

  return links;
}

export function isInternalDocsLink(url) {
  return (
    url.startsWith('/docs/') ||
    url.startsWith('#') ||
    url.startsWith('{{version}}') ||
    url.startsWith('{{ version }}')
  );
}

export function extractInternalMarkdownLinks(text) {
  return extractMarkdownLinks(text).filter((link) => isInternalDocsLink(link.url));
}

export function extractVersionFromPath(path) {
  const parts = String(path).split('/');
  const versionDir = parts.find((part) => part.startsWith('version-'));
  return versionDir ? versionDir.slice('version-'.length) : null;
}

export function replaceVersionPlaceholders(value, version = '') {
  const replacement = versionReplacement(version);
  let output = '';
  let index = 0;

  while (index < value.length) {
    if (!value.startsWith('{{', index)) {
      output += value[index++];
      continue;
    }

    const end = value.indexOf('}}', index + 2);
    if (end < 0) {
      output += value.slice(index);
      break;
    }

    const token = value.slice(index + 2, end).trim();
    if (token === 'version') {
      output += replacement;
    } else {
      output += value.slice(index, end + 2);
    }
    index = end + 2;
  }

  return output;
}
