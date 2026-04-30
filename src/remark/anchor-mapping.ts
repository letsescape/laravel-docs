import type {Transformer} from 'unified';
import type {Html, Paragraph, Root} from 'mdast';
import {visit} from 'unist-util-visit';

const ANCHOR_RE = /<a\s+name=["']([^"']+)["']\s*(?:\/?>|>\s*<\/a>)/;

/**
 * Laravel 원본 관행인 `<a name="xxx"></a>` 형태의 HTML 앵커를
 * 다음 헤딩의 id로 매핑하는 remark 플러그인.
 *
 * 배경:
 *   Laravel 공식 문서는 각 섹션 헤딩 앞에 `<a name="xxx"></a>`로 앵커를 선언한다.
 *   Docusaurus 기본 동작은 헤딩 텍스트를 slug로 변환해 id를 생성하므로,
 *   한글로 번역된 헤딩은 id가 한글 기반이 되어 `#xxx` 형식 링크가 전부 깨진다.
 *
 * 파싱 참고:
 *   remark의 CommonMark 파서는 한 줄짜리 `<a name="..."></a>`를 block HTML이 아니라
 *   `paragraph > html` 구조로 감싸는 경우가 많다. 따라서 `paragraph`를 탐색하며
 *   첫 자식이 매칭되는 html 노드인지 검사한다.
 *
 * 동작:
 *   해당 paragraph 바로 다음의 heading 노드에 Docusaurus heading-id 주석을
 *   주입해 TOC와 실제 HTML heading id를 같은 값으로 맞춘다.
 */
export default function anchorMappingPlugin(): Transformer<Root> {
  return (tree) => {
    visit(tree, 'paragraph', (para: Paragraph, index, parent) => {
      if (!parent || index == null) return;
      const first = para.children[0];
      if (first?.type !== 'html') return;

      const m = ANCHOR_RE.exec((first as Html).value);
      if (!m) return;
      const anchorId = m[1];

      // parent.children에서 현재 paragraph 이후의 다음 heading 찾기
      const siblings = (parent as Root).children;
      for (let j = index + 1; j < siblings.length; j++) {
        const next = siblings[j];
        if (next.type === 'heading') {
          // Docusaurus heading 플러그인은 trailing `<!-- #id -->`를 명시 id로 사용하고
          // TOC 수집 전에 `data.id`와 `hProperties.id`를 함께 설정한다.
          next.children.push({type: 'html', value: `<!-- #${anchorId} -->`} as Html);
          break;
        }
        // 다음 앵커가 먼저 나오면 현재 앵커엔 헤딩이 없음 — 중단
        if (
          next.type === 'paragraph' &&
          (next as Paragraph).children[0]?.type === 'html' &&
          ANCHOR_RE.test(((next as Paragraph).children[0] as Html).value)
        ) {
          break;
        }
      }
    });
  };
}
