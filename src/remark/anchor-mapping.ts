import type {Transformer} from 'unified';
import type {Heading, Html, Paragraph, Root} from 'mdast';
import {createSlugger, parseMarkdownHeadingId} from '@docusaurus/utils';
import {toString} from 'mdast-util-to-string';
import {visit} from 'unist-util-visit';

const ANCHOR_RE = /<a\s+name=["']([^"']+)["']\s*(?:\/?>|>\s*<\/a>)/;
const HTML_ID_RE = /<[a-z][^>]*?\sid=(["'])([^"']+)\1[^>]*>/gi;

function headingText(heading: Heading): string {
  const children = heading.children.filter(({type}) => type !== 'html');
  return toString(children.length > 0 ? children : heading);
}

/**
 * Laravel 원본 관행인 `<a name="xxx"></a>` 형태의 HTML 앵커를 다음 헤딩의 ID로 매핑하는 remark 플러그인
 *
 * 배경:
 * - Laravel 공식 문서는 각 섹션 헤딩 앞에 `<a name="xxx"></a>`로 앵커 선언
 * - Docusaurus는 기본적으로 헤딩 텍스트를 slug로 변환해 ID 생성
 * - 번역된 헤딩의 ID도 번역문 기반이 되어 `#xxx` 형식 링크가 모두 깨지는 문제 발생
 *
 * 파싱 참고:
 * - remark의 CommonMark 파서는 한 줄짜리 `<a name="..."></a>`를 HTML 블록이 아닌 `paragraph > html` 구조로 감싸는 경우가 많음
 * - 따라서 `paragraph`를 탐색하며 첫 자식이 일치하는 `html` 노드인지 검사
 *
 * 동작:
 * - 해당 `paragraph` 이후 다음 `heading` 노드에 Docusaurus heading ID 주석 주입
 * - TOC와 실제 HTML 헤딩 ID를 같은 값으로 설정
 * - 같은 `paragraph`의 추가 앵커는 별도 `id`로 보존
 * - 명시 ID를 먼저 예약하고 충돌하는 제목·HTML ID에만 접미사 부여
 */
export default function anchorMappingPlugin(): Transformer<Root> {
  return (tree) => {
    const mapped = new Map<Heading, {id: string; anchor: Html}>();
    visit(tree, 'paragraph', (para: Paragraph, index, parent) => {
      if (!parent || index == null) return;
      const first = para.children[0];
      if (first?.type !== 'html') return;

      const m = ANCHOR_RE.exec((first as Html).value);
      if (!m) return;
      const anchorId = m[1];

      // `parent.children`에서 현재 `paragraph` 다음의 `heading` 탐색
      const siblings = (parent as Root).children;
      for (let j = index + 1; j < siblings.length; j++) {
        const next = siblings[j];
        if (next.type === 'heading') {
          for (const child of para.children.slice(1)) {
            if (child.type === 'html' && ANCHOR_RE.test(child.value)) {
              child.value = child.value.replace('name=', 'id=');
            }
          }
          mapped.set(next, {id: anchorId, anchor: first});
          break;
        }
        // 다음 앵커가 먼저 나오면 현재 앵커에 헤딩 없음 — 중단
        if (
          next.type === 'paragraph' &&
          (next as Paragraph).children[0]?.type === 'html' &&
          ANCHOR_RE.test(((next as Paragraph).children[0] as Html).value)
        ) {
          break;
        }
      }
    });

    const targets: {id: string; offset: number; assign: (id: string) => void}[] = [];
    const automatic: Heading[] = [];
    visit(tree, 'heading', (heading: Heading) => {
      const mapping = mapped.get(heading);
      const last = heading.children.at(-1);
      const comment = last?.type === 'html'
        ? /^<!--\s*#([^\s]+)[\s\S]*-->$/.exec(last.value)?.[1]
        : undefined;
      const classic = parseMarkdownHeadingId(headingText(heading));
      const id = mapping?.id ?? comment ?? classic.id;
      if (!id) {
        automatic.push(heading);
        return;
      }
      targets.push({
        id,
        offset: (mapping?.anchor ?? heading).position?.start.offset ?? 0,
        assign: (finalId) => {
          if (mapping) {
            mapping.anchor.value = mapping.anchor.value.replace(
              /(name=["'])[^"']+/,
              (_, prefix) => prefix + finalId,
            );
            heading.children.push({type: 'html', value: `<!-- #${finalId} -->`});
          } else if (comment && last?.type === 'html') {
            last.value = `<!-- #${finalId} -->`;
          } else if (finalId !== id && last?.type === 'text') {
            last.value = `${parseMarkdownHeadingId(last.value).text} {#${finalId}}`;
          }
        },
      });
    });

    const htmlEdits = new Map<Html, {start: number; end: number; value: string}[]>();
    visit(tree, 'html', (node: Html) => {
      const content = node.value.replace(/<!--[\s\S]*?-->/g, (comment) => ' '.repeat(comment.length));
      for (const match of content.matchAll(HTML_ID_RE)) {
        targets.push({
          id: match[2],
          offset: (node.position?.start.offset ?? 0) + match.index,
          assign: (id) => {
            if (id === match[2]) return;
            const edits = htmlEdits.get(node) ?? [];
            edits.push({
              start: match.index,
              end: match.index + match[0].length,
              value: match[0].replace(/(\sid=["'])[^"']+/i, (_, prefix) => prefix + id),
            });
            htmlEdits.set(node, edits);
          },
        });
      }
    });

    const reserved = new Set(targets.map(({id}) => id));
    const used = new Set<string>();
    for (const target of targets.sort((a, b) => a.offset - b.offset)) {
      let id = target.id;
      for (let suffix = 1; used.has(id); suffix++) {
        id = `${target.id}-${suffix}`;
        while (reserved.has(id)) id = `${target.id}-${++suffix}`;
      }
      used.add(id);
      target.assign(id);
    }
    for (const [node, edits] of htmlEdits) {
      for (const edit of edits.sort((a, b) => b.start - a.start)) {
        node.value = node.value.slice(0, edit.start) + edit.value + node.value.slice(edit.end);
      }
    }

    const slugs = createSlugger();
    for (const heading of automatic) {
      const data = heading.data ?? (heading.data = {});
      const properties = data.hProperties ?? (data.hProperties = {});
      const text = properties.id ? String(properties.id) : headingText(heading);
      const options = {maintainCase: Boolean(properties.id)};
      let id = slugs.slug(text, options);
      // 테마가 H1의 ID를 제거하므로 기존 slug 순서만 소비하고 실제 ID는 예약하지 않는다.
      if (heading.depth !== 1) {
        while (used.has(id)) id = slugs.slug(text, options);
        used.add(id);
      }
      properties.id = id;
    }
  };
}
