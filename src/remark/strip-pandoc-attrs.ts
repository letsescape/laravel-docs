import type {Transformer} from 'unified';
import type {Heading, Root, Text} from 'mdast';
import {visit} from 'unist-util-visit';

function stripTrailingPandocAttrs(value: string): string {
  const trimmed = value.trimEnd();
  if (!trimmed.endsWith('}')) return value;

  const attrStart = trimmed.lastIndexOf('{.');
  if (attrStart < 0) return value;

  const attrBody = trimmed.slice(attrStart + 2, -1);
  if (!attrBody || attrBody.includes('{') || attrBody.includes('}') || attrBody.includes('\n')) {
    return value;
  }

  return trimmed.slice(0, attrStart).trimEnd();
}

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
      textNode.value = stripTrailingPandocAttrs(textNode.value);
      if (!textNode.value) node.children.pop();
    });
  };
}
