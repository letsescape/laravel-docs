import type {Transformer} from 'unified';
import type {Link, Root, Text} from 'mdast';
import type {VFile} from 'vfile';
import {visit} from 'unist-util-visit';

/**
 * 파일 경로에서 버전 세그먼트를 추출.
 * 예: ".../versioned_docs/version-11.x/mcp.md" → "11.x"
 */
const VERSION_RE = /versioned_docs[/\\]version-([^/\\]+)[/\\]/;

function extractVersion(filePath: string | undefined): string | null {
  if (!filePath) return null;
  const m = VERSION_RE.exec(filePath);
  return m ? m[1] : null;
}

/**
 * Laravel 공식 문서의 서버사이드 템플릿/관례적 링크 패턴을
 * Docusaurus 라우팅에 맞게 자동 치환하는 remark 플러그인.
 *
 * 치환 규칙:
 *   1) `{{version}}` → 현재 파일이 속한 버전 (예: `11.x`)
 *   2) `/docs/<version>/installation[#anchor]` → `/docs/<version>/[#anchor]`
 *      (번역본의 `installation.md`가 `slug: /`로 루트 페이지이므로 경로 보정)
 *
 * 코드 블록(`code`, `inlineCode`)은 의도적으로 건드리지 않음 —
 * 사용자가 Laravel 코드 예제를 그대로 복사할 수 있도록 원형 보존.
 */
export default function replacePlaceholdersPlugin(): Transformer<Root> {
  return (tree, file: VFile) => {
    const version = extractVersion(file.path);
    if (!version) return;

    const applyText = (input: string): string =>
      input.includes('{{version}}')
        ? input.replaceAll('{{version}}', version)
        : input;

    // 링크 URL 보정: {{version}} 치환 + /installation 경로 → 루트
    const applyUrl = (input: string): string => {
      let out = applyText(input);
      // /docs/<ver>/installation(#anchor)? → /docs/<ver>/(#anchor)?
      out = out.replace(
        /^(\/docs\/[^/]+\/)installation(#.*)?$/,
        (_m, base: string, anchor = '') => `${base}${anchor}`,
      );
      return out;
    };

    visit(tree, 'text', (node: Text) => {
      node.value = applyText(node.value);
    });

    visit(tree, 'link', (node: Link) => {
      if (node.url) node.url = applyUrl(node.url);
    });
  };
}
