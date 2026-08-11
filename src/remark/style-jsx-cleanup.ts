import type {Transformer} from 'unified';
import type {Html, Root} from 'mdast';
import {visit} from 'unist-util-visit';

const OPEN_RE = /<style>\{`/g;
const CLOSE_RE = /`\}<\/style>/g;

/**
 * Laravel 원본 문서의 `<style>{\`...\`}</style>` 형식 인라인 스타일을 표준 `<style>...</style>`로 정리하는 remark 플러그인
 *
 * 배경:
 * - Laravel 공식 사이트는 MDX의 JSX 표현 안에서 template literal을 사용하기 위해 `<style>{\`...\`}</style>` 형태로 CSS 포함
 * - Docusaurus가 이 블록을 raw HTML 노드로 처리하면 브라우저가 실제 스타일 문자열 앞에 남은 `{\`` 때문에 규칙을 파싱하지 못해 CSS 미적용
 *
 * 동작:
 * - AST의 `html` 노드에서 여는 `<style>{\``와 닫는 `\`}</style>` 토큰 제거
 * - 브라우저가 이해할 수 있는 평문 `<style>` 블록으로 변환
 */
export default function styleJsxCleanupPlugin(): Transformer<Root> {
  return (tree) => {
    visit(tree, 'html', (node: Html) => {
      if (!node.value.includes('<style>{`') && !node.value.includes('`}</style>')) {
        return;
      }
      node.value = node.value
        .replaceAll(OPEN_RE, '<style>')
        .replaceAll(CLOSE_RE, '</style>');
    });
  };
}
