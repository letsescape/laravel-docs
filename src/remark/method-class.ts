import type {Transformer} from 'unified';
import type {Html, Paragraph, Root} from 'mdast';
import {visit} from 'unist-util-visit';

const METHOD_ANCHOR_RE = /<a\s+name=["']method-[^"']+["']\s*(?:\/?>|>\s*<\/a>)/;

function mergeClassNames(existing: unknown, added: string[]): string[] {
  const current = Array.isArray(existing)
    ? existing.filter((value): value is string | number => typeof value === 'string' || typeof value === 'number')
    : typeof existing === 'string' || typeof existing === 'number'
      ? [existing]
      : [];

  return [...current.map(String), ...added];
}

/**
 * Laravel 공식 문서의 "메서드 목록" 페이지에서 각 메서드 섹션 헤딩에 `.collection-method` 클래스를 자동 부여하는 remark 플러그인
 *
 * 배경:
 * - laravel.com/docs의 정적 사이트 생성기는 `<a name="method-xxx"></a>` 다음 heading에 `collection-method` 클래스 자동 주입
 * - 첫 메서드에는 `first-collection-method` 클래스도 추가
 * - 관련 CSS(코드 폰트 크기, 섹션 여백 등)가 `<style>` 블록에 포함되어 있으나 Docusaurus 빌드에는 해당 wrapping 단계가 없어 스타일 미적용
 *
 * 동작:
 * - `<a name="method-*"></a>`로 시작하는 paragraph 이후 다음 heading 노드에 `collection-method`를 className으로 추가
 * - 파일에서 처음 발견된 메서드에는 `first-collection-method`도 함께 부여
 */
export default function methodClassPlugin(): Transformer<Root> {
  return (tree) => {
    let isFirstInFile = true;

    visit(tree, 'paragraph', (para: Paragraph, index, parent) => {
      if (!parent || index == null) return;
      const first = para.children[0];
      if (first?.type !== 'html') return;
      if (!METHOD_ANCHOR_RE.test((first as Html).value)) return;

      const siblings = (parent as Root).children;
      for (let j = index + 1; j < siblings.length; j++) {
        const next = siblings[j];
        if (next.type !== 'heading') {
          if (
            next.type === 'paragraph' &&
            (next as Paragraph).children[0]?.type === 'html' &&
            METHOD_ANCHOR_RE.test(((next as Paragraph).children[0] as Html).value)
          ) {
            // 다음 메서드 앵커가 먼저 나오면 대상 없음
            break;
          }
          continue;
        }

        const data = (next.data ?? {}) as Record<string, unknown>;
        const hProps = (data.hProperties ?? {}) as Record<string, unknown>;
        const existing = hProps.className;
        const added = ['collection-method'];
        if (isFirstInFile) {
          added.push('first-collection-method');
          isFirstInFile = false;
        }
        next.data = {
          ...data,
          hProperties: {
            ...hProps,
            className: mergeClassNames(existing, added),
          },
        };
        break;
      }
    });
  };
}
