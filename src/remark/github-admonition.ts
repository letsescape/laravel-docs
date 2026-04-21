import type {Transformer} from 'unified';
import type {Blockquote, Paragraph, Root, Text} from 'mdast';
import {visit} from 'unist-util-visit';

const MARKER_RE = /^\[!(NOTE|TIP|WARNING|IMPORTANT|CAUTION)\](?:\n|\s)?/;

// Laravel 공식 사이트는 GFM 5종을 2계열(info/warning)로 통합해 렌더링한다.
// 동일 시각 경험을 재현하기 위해 동일하게 매핑한다.
const TYPE_MAP: Record<string, string> = {
  NOTE: 'info',
  TIP: 'info',
  IMPORTANT: 'info',
  WARNING: 'warning',
  CAUTION: 'warning',
};

/**
 * GitHub Flavored Markdown의 alert 문법 `> [!NOTE]` 계열을
 * Docusaurus admonition 스타일로 매핑하는 remark 플러그인.
 *
 * 배경:
 *   Laravel 원본 문서는 GitHub 표기법인 `> [!NOTE]`, `> [!WARNING]` 등을
 *   사용한다(번역본도 이 형식 유지). Docusaurus는 `:::note ... :::` 문법만
 *   admonition으로 인식하므로, 변환 없이는 단순 blockquote로만 렌더링되어
 *   admonition UI가 적용되지 않는다.
 *
 * 동작:
 *   blockquote 노드의 첫 paragraph > text가 `[!TYPE]`로 시작하면
 *   마커를 제거하고 blockquote에 admonition 관련 className과 data-type을
 *   주입한다. 실제 스타일은 `src/css/custom.css`에서 해당 클래스에 부여.
 */
export default function githubAdmonitionPlugin(): Transformer<Root> {
  return (tree) => {
    visit(tree, 'blockquote', (node: Blockquote) => {
      const firstChild = node.children[0];
      if (firstChild?.type !== 'paragraph') return;
      const para = firstChild as Paragraph;
      const firstInline = para.children[0];
      if (firstInline?.type !== 'text') return;
      const textNode = firstInline as Text;

      const m = MARKER_RE.exec(textNode.value);
      if (!m) return;

      const type = TYPE_MAP[m[1]];
      textNode.value = textNode.value.slice(m[0].length);
      // 마커만 있던 경우 빈 text 노드 제거
      if (textNode.value === '' && para.children.length > 1) {
        para.children.shift();
      }

      const data = (node.data ?? {}) as Record<string, unknown>;
      const hProps = (data.hProperties ?? {}) as Record<string, unknown>;
      const existingClass = hProps.className;
      const added = ['admonition', `admonition-${type}`];
      node.data = {
        ...data,
        hProperties: {
          ...hProps,
          className: Array.isArray(existingClass)
            ? [...(existingClass as unknown[]), ...added]
            : added,
          'data-admonition-type': type,
        },
      };
    });
  };
}
