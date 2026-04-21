import type {Transformer} from 'unified';
import type {Html, Root} from 'mdast';
import {visit} from 'unist-util-visit';

const OPEN_RE = /<style>\{`/g;
const CLOSE_RE = /`\}<\/style>/g;

/**
 * Laravel 원본 문서의 `<style>{\`...\`}</style>` 형식 인라인 스타일을
 * 표준 `<style>...</style>`로 정리하는 remark 플러그인.
 *
 * 배경:
 *   Laravel 공식 사이트는 MDX의 JSX 표현 안에서 tagged template literal을
 *   쓰기 위해 `<style>{\`...\`}</style>` 형태로 CSS를 포함한다. 하지만
 *   Docusaurus가 이 블록을 raw HTML 노드로 처리하면 브라우저는 실제 스타일
 *   문자열 앞에 남은 `{\`` 때문에 규칙을 파싱하지 못해 CSS가 전혀 적용되지 않는다.
 *
 * 동작:
 *   AST의 `html` 노드에서 여는 `<style>{\``와 닫는 `\`}</style>` 토큰을 제거해
 *   브라우저가 이해할 수 있는 평문 `<style>` 블록으로 바꾼다.
 */
export default function styleJsxCleanupPlugin(): Transformer<Root> {
  return (tree) => {
    visit(tree, 'html', (node: Html) => {
      if (!node.value.includes('<style>{`') && !node.value.includes('`}</style>')) {
        return;
      }
      node.value = node.value
        .replace(OPEN_RE, '<style>')
        .replace(CLOSE_RE, '</style>');
    });
  };
}
