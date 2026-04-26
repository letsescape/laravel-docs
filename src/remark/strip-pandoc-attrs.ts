import type {Transformer} from 'unified';
import type {Heading, Root, Text} from 'mdast';
import {visit} from 'unist-util-visit';

const PANDOC_ATTR_RE = /\s*\{\.[^}]+\}\s*$/;

/**
 * Pandoc 속성 문법(`{.foo .bar}`)이 헤딩 끝에 평문으로 노출되는 현상을 제거.
 *
 * 라라벨 원본은 Jigsaw + Pandoc 기반이라 헤딩 뒤 `{.collection-method ...}` 가
 * CSS 클래스 지시자로 처리됐지만, Docusaurus(MDX/remark)는 이 문법을 모르므로
 * 그대로 화면에 평문으로 출력된다. 클래스 부여는 method-class 플러그인이 별도로
 * `<a name="method-X">` 앵커를 보고 처리하므로, 이 잔여 텍스트는 제거해도 안전.
 */
export default function stripPandocAttrsPlugin(): Transformer<Root> {
  return (tree) => {
    visit(tree, 'heading', (node: Heading) => {
      const last = node.children[node.children.length - 1];
      if (last?.type !== 'text') return;
      const textNode = last as Text;
      if (!PANDOC_ATTR_RE.test(textNode.value)) return;
      textNode.value = textNode.value.replace(PANDOC_ATTR_RE, '');
      if (!textNode.value) node.children.pop();
    });
  };
}
