# 후처리 단계 설계

## 1. 목적

번역이 완료된 locale 문서의 Markdown 형식을 정제하고, 전처리에서 치환한 placeholder를 원본으로 복원하며, 보존해야 할 markup을 복구하여 최종 문서 형식을 확정한다.

---

## 2. 범위

후처리 단계가 소유하는 책임은 다음 네 가지로 한정한다.

| 책임 | 설명 |
|------|------|
| 블록 형식 정제 | `<img>` self-closing 변환, 버전 placeholder 치환, alert 표준화, 제목 스타일 클래스 잔존 제거, trailing whitespace 정리 |
| placeholder 복원 | 예약 placeholder를 전처리에서 보관한 원본 값으로 복원 |
| 보존 markup 복구 | 번역 블록의 quote/list marker, heading, link, inline code, anchor, annotation을 유일하게 대응할 수 있을 때 복구 |
| 계획 적용·전체 정규화 | 정제된 블록을 PatchPlan에 따라 기존 locale 문서에 적용하고 전체 문서를 canonical form으로 정규화 |

번역 provider 호출, effective delta 계산, PatchPlan 생성과 response contract는 [번역 단계](./02-translation.md)의 책임이다. 입력 정규화와 placeholder 치환은 [전처리 단계](./01-preprocessing.md)의 책임이다.

---

## 3. 입력

| 입력 | 설명 |
|------|------|
| 기존 locale 문서 | 계획 적용 전의 번역 문서 |
| PatchPlan | 소유 블록, 적용 위치와 source/target 서명을 포함한 변경 계획 |
| 번역·결정적 블록 집합 | response contract를 통과했거나 원문 구조로 확정된 블록 |
| placeholder 매핑 | 전처리에서 생성한 예약 placeholder와 원본 값의 대응표 |
| 버전 문자열 | 문서에 적용할 대상 버전 |
| 최신 전체 영어 원문 | 적용 뒤 annotation 정규화와 최종 검증의 기준 |
| 알려진 stale 내부 링크 목록 | canonical 대상 보정용 |

---

## 4. 출력

| 출력 | 설명 |
|------|------|
| 최종 locale 문서 | 블록 정제, PatchPlan 적용과 전체 정규화가 완료된 Markdown |
| 검증 입력 | 최신 영어 기준본과 대조할 최종 문서 및 관련 version 정보 |

---

## 5. 불변조건

1. 번역문을 임의로 다시 쓰지 않는다.
2. 코드 블록 내부의 코드와 주석은 원문 영어를 유지한다.
3. 이미 보존된 인라인 코드와 링크를 원문 등장 순서에 맞추기 위해 재배치해서는 안 된다. 누락된 markup은 내용과 주변 문맥으로 유일하게 대응할 수 있을 때만 복구해야 한다.
4. 링크 URL과 앵커는 원문대로 유지한다. 알려진 stale 내부 링크는 탐지용 mask에서 위치만 찾고, label·title·구분자는 원본 span을 보존한 채 target만 canonical 값으로 보정해야 한다.
5. fenced code 밖의 파이프라인용 placeholder가 최종 문서에 남지 않아야 한다.
6. fenced code 내부 텍스트는 version/image/alert/title/HTML-comment 정제에서 제외한다.
7. 한 줄·여러 줄 inline code span 내부는 `<img>` self-closing 변환에서 제외한다.
8. fenced code의 `{{version}}`은 예시 코드의 literal placeholder로 보고 치환하지 않는다.
9. 본문의 명시적 Markdown hard break (trailing 공백 2개)는 보존한다.
10. `{#stable-id}`는 보존한다. `{.class #id}` 형태에서는 class만 제거하고 `{#id}`를 남긴다.

---

## 6. 처리 순서

후처리는 반드시 아래 순서를 따른다.

```text
1. 각 번역 블록 형식 정제
   a. fenced code 밖의 버전 placeholder 치환
   b. <img> self-closing 변환
   c. 지원 legacy note marker의 canonical alert 변환
   d. 제목 스타일 클래스 잔존 제거
   e. 원본 span을 보존한 stale 내부 링크 target 보정
2. alert 내부 fenced code의 blockquote 경계 보정
3. 각 블록의 base64 이미지 placeholder 복원
4. trailing whitespace 정리와 명시적 hard break 보존
5. 보존 markup 복구
   - 이미 보존된 inline code와 link는 재배치하지 않음
   - 누락된 markup은 내용과 주변 문맥으로 유일하게 대응될 때만 복구
   - 복수 후보 또는 대응 불가 상태는 실패
6. 정제된 블록 수와 PatchPlan 대상 수 일치 확인
7. source 상태 계획을 문서 아래쪽부터 역순 적용
   - target 상태는 no-op
   - 계획 밖의 locale 블록은 변경하지 않음
   - 적용 후 annotation-backed 서명이 목표 서명과 일치해야 함
8. 적용 완료 문서 전체 정규화
   - 최신 영어 기준본으로 annotation 정렬
   - 지원 legacy alert와 대응 annotation을 canonical form으로 정규화
   - 폐기 목록 label의 inline-code wrapper를 일반 label로 수렴
9. 최종 문서를 문서 검증 단계에 전달
```

base64 복원은 블록 형식 정제가 끝난 뒤 수행하여 복원된 data URI가 다른 정제 규칙에 의해 변경되지 않게 해야 한다. 전체 문서 정규화는 PatchPlan 적용 뒤 한 번 수행해야 한다.

---

## 7. 형식 정제 세부

### 7.1 `<img>` self-closing 변환

- 닫는 태그가 없는 HTML `<img>` 태그를 self-closing 형식으로 변환한다.
- tag end는 따옴표 속성과 balanced JSX `{...}` 안의 `>`를 건너뛴 뒤 찾는다.
- 마지막 속성 값이 따옴표 없는 형식이면 값과 closing slash 사이에 공백을 넣는다.
- 이미 self-closing인 태그는 변경하지 않는다.
- malformed 또는 닫히지 않은 expression/tag는 복구하지 않는다.

### 7.2 GitHub Markdown alert 표준화

지원하는 legacy marker를 canonical form으로 변환한다.

| 원문 표현 | canonical form |
|-----------|----------------|
| `{note}`, `Note`, `Note:`, `**Note**`, `**Note:**`, `참고`, `注意`, `注` | `[!NOTE]` |
| `{tip}`, `Tip`, `Tip:`, `**Tip**`, `**Tip:**` | `[!TIP]` |
| `{warning}`, `Warning`, `Warning:`, `**Warning**`, `**Warning:**` | `[!WARNING]` |
| `{caution}`, `Caution`, `Caution:`, `**Caution**`, `**Caution:**` | `[!CAUTION]` |
| `{important}`, `Important`, `Important:`, `**Important**`, `**Important:**` | `[!IMPORTANT]` |

- 후처리는 marker만 바꾸고 본문을 번역하지 않는다.
- 지원 범위 밖의 임의 표현을 `[!NOTE]`로 추정 변환하지 않는다.
- 1~3칸 들여쓴 blockquote marker는 변환 대상이 아니다.

### 7.3 `{{version}}` 치환

- fenced code 밖의 모든 `{{version}}`을 대상 버전 문자열로 치환한다.
- 영어 주석, 링크 URL 안의 `{{version}}`도 치환한다.
- fenced code 안의 `{{version}}`은 literal placeholder로 보고 유지한다.

### 7.4 제목 스타일 클래스 제거

- Markdown heading 줄의 `{.class-name}` 패턴을 제거한다.
- `{#stable-id}`는 보존한다.
- 본문 내 의미 있는 중괄호 표현은 유지한다.

### 7.5 stale 내부 링크 보정

- 알려진 stale 내부 링크만 canonical 대상으로 보정한다.
- fenced code, inline code, HTML 주석 안은 건드리지 않는다.
- 대응 대상이 폐기된 fragment 링크: standalone 목록 항목이면 목록 label의 일반 텍스트로, bare link이면 표시 label의 inline code로 남긴다.

---

## 8. placeholder 복원 세부

- 전처리에서 생성한 매핑을 사용하여 `__BASE64_IMAGE_<N>__`을 원본 data URI로 치환한다.
- 매핑이 없으면 임의로 데이터를 생성하지 않는다.
- fenced code 밖에 미복원 placeholder가 남은 결과는 [문서 검증 단계](./04-verification.md)에서 실패해야 하며 locale 파일로 기록해서는 안 된다.

---

## 9. 보존 markup 복구 세부

부분 번역 블록은 일반 후처리 뒤, 검증 전에 다음을 복구한다.

| 복구 대상 | 조건 |
|-----------|------|
| blockquote `>` marker | 원문 블록 전체가 blockquote일 때 |
| 목록 marker (`-`, `*`, `+`) | 원문 블록 전체가 순수 순서 없는 목록이고 항목 일대일 대응 가능할 때 |
| heading | 원문 기준으로 복구 |
| link label / target / title | URL, separator, 따옴표 형태(작은따옴표·큰따옴표·괄호) 포함 보존 |
| inline code | 원문 기준으로 복구 |
| named anchor | 원문 기준으로 복구 |
| annotation | 정렬 또는 추가 |

- 이미 올바르게 보존된 inline code, link와 anchor의 순서를 원문 순서에 맞추기 위해 변경해서는 안 된다.
- 누락된 markup은 내용과 주변 문맥으로 source 항목 하나에 유일하게 대응할 때만 복구해야 한다.
- 동일한 후보가 여러 개이거나 locale 어순 변경 때문에 대응을 증명할 수 없으면 임의 복구하지 않고 실패해야 한다.
- 복구 뒤에도 남은 구조 불일치는 문서 검증 단계에서 실패 처리해야 한다.

---

## 10. 실패 정책

후처리는 **fail-closed** 원칙을 따른다.

| 실패 유형 | 처리 |
|-----------|------|
| 번역 단계에서 실패한 블록 | 후처리 입력으로 전달하지 않음 |
| placeholder 원본 매핑 부재 | 해당 target 실패, 계획 적용 금지 |
| 보존 markup 대응이 모호하거나 복구 불가 | 해당 target 실패, 계획 적용 금지 |
| PatchPlan 대상 수와 정제 블록 수 불일치 | 해당 target 실패, 계획 적용 금지 |
| 적용 뒤 목표 서명 불일치 | 최종 문서 폐기, 기존 locale 문서 보존 |

후처리는 provider 호출 실패를 복구하지 않는다. 후처리 결과는 직접 기록하지 않고 [문서 검증 단계](./04-verification.md)에 전달해야 한다.

---

## 11. 수용 기준

후처리 출력이 다음 조건을 모두 만족해야 [문서 검증 단계](./04-verification.md)로 전달한다.

1. fenced code 밖에 `__BASE64_IMAGE_<N>__` placeholder가 남아 있지 않다.
2. fenced code 밖에 `{{version}}` placeholder가 남아 있지 않다.
3. 지원 legacy note marker가 canonical GitHub Markdown alert form으로 변환되었다.
4. heading 줄에 `{.class-name}` 패턴이 남아 있지 않다 (`{#id}`는 허용).
5. 모든 `<img>` 태그가 self-closing 형식이다 (fenced code·inline code 내부 제외).
6. 최신 전체 영어 기준본 대비 annotation 순서·구조가 정규화되었다.
7. 계획 밖의 locale 블록과 source-authored 구조가 변경되지 않았다.
