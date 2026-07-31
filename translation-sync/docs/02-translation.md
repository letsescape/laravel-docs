# 번역 단계 설계

## 1. 목적

전처리가 완료된 영어 원문의 변경분을 기존 한국어·일본어 locale 문서에 반영한다. 번역은 정규화된 effective delta가 선택한 완전한 번역 소유 블록 단위로 수행하며, 계획 밖의 기존 locale 블록은 수정하지 않는다.

---

## 2. 범위

번역 단계가 소유하는 책임은 다음으로 한정한다.

| 책임 | 설명 |
|------|------|
| normalized delta | 정규화된 이전·현재 작업 사본 사이에서 effective hunk를 계산한다 |
| PatchPlan | effective delta를 완전한 번역 소유 블록과 결합하여 적용 계획을 생성한다 |
| 소유 단위 | 각 블록 유형별 원자적 번역·적용 범위를 정의한다 |
| provider 계약 | provider adapter의 입력·출력 seam 및 호출 조건을 정의한다 |
| response contract | provider 응답의 구조 보존·언어·annotation 규칙을 검증한다 |
| retry | transient 오류에 대한 재시도 정책과 상한을 정의한다 |

문서 형식 정제, placeholder 복원, 최종 문서 정규화는 [후처리 단계](./03-postprocessing.md)의 책임이다. 입력 정규화와 placeholder 치환은 [전처리 단계](./01-preprocessing.md)의 책임이다.

---

## 3. 입력

| 입력 | 설명 |
|------|------|
| 정규화된 현재 원문 작업 사본 | 전처리 출력. provider에 전달하는 `new_source`의 기준 |
| 정규화된 이전 원문 작업 사본 | effective delta 계산의 비교 대상 |
| placeholder 매핑 | 전처리에서 생성한 base64 치환 정보 (번역 중 변경하지 않음) |
| 기존 locale 문서 | 위치 매칭·용어·문체 참고 |
| 설정 확인 완료 상태 | 선행 설정 검증에서 provider 설정 유효성이 확인된 상태 |

---

## 4. 출력

| 출력 | 설명 |
|------|------|
| PatchPlan | 소유 블록, 적용 위치, source/target 서명과 구조 주소를 포함한 변경 계획 |
| 검증된 locale 블록 집합 | PatchPlan의 각 provider 필요 소유 블록에 대응하며 response contract를 통과한 번역 결과 |
| 결정적 블록 집합 | provider 없이 원문 구조로 확정한 변경 결과 |

PatchPlan과 블록 집합은 [후처리 단계](./03-postprocessing.md)로 함께 전달한다. 기존 locale 문서에 대한 실제 적용과 전체 문서 정규화는 후처리 단계가 소유한다.

---

## 5. 불변조건

### 5.1 구조 보존

1. 코드 블록 내부의 코드와 주석은 원문 영어를 유지한다.
2. 인라인 코드는 원문과 동일하게 유지한다.
3. 링크 URL, 앵커, URL fragment는 변경하지 않는다.
4. Markdown heading 텍스트, 링크 label, front matter `title`은 번역하지 않고 최신 영어 원문으로 유지한다.
5. API 이름, 함수명, 클래스명, 파라미터명, 파일명, 경로, 명령어, 환경 변수, URL, 제품 고유명사는 번역하지 않는다.
6. source-authored HTML 주석은 순서·occurrence·구조적 위치를 보존한다.
7. front matter 구조 값은 YAML scalar 형식을 유지한다.
8. 표 열 수·정렬자는 원문과 동일하게 보존한다.
9. 명시적 hard break가 없는 prose 번역은 물리적 한 줄이어야 한다.
10. 영어 원문 annotation 안의 literal `-->`는 `--&gt;`로 escape한다.

### 5.2 annotation 규칙

1. 일반 prose와 heading은 `<!-- 최신 영어 원문 -->` + 번역문 형식을 유지한다. heading 주석에는 `#` marker를 포함한다.
2. blockquote 본문에는 새 annotation을 추가하지 않는다. 기존 exact quoted-source annotation은 호환용으로 허용한다.
3. 순수 inline-code 식별자 목록 항목은 annotation 대상이 아니다.
4. source에 없는 standalone 구조 주석을 provider가 추가하면 거부한다.

### 5.3 fail-closed 원칙

1. 위치가 유일하게 확정되지 않으면 provider를 호출하거나 문서를 수정하지 않고 실패한다.
2. annotation-backed 문서 상태가 source/target 어느 쪽과도 일치하지 않는 partial/mixed/제3 상태는 적용 전에 실패한다.
3. 동일 계획을 이미 적용한 target 문서에 다시 적용하면 no-op이어야 한다.

---

## 6. 처리 순서

```text
1. effective delta 계산
   - 정규화된 이전·현재 작업 사본을 비교하여 effective hunk 추출
   - style-only 변경은 정규화에 의해 자동 제거됨

2. PatchPlan 생성
   - 각 effective hunk를 소유 블록 경계에 맞춰 결합
   - old_source / new_source (완전한 블록)와 old_lines / new_lines (effective delta) 분리
   - 이전·다음 anchor 및 동일 블록 occurrence 기록
   - annotation source/target 서명 생성

3. locale 문서 상태 판정
   - annotatable 주석 순서를 old/new 서명과 비교
   - source 상태에서만 계획 적용, target 상태는 no-op
   - partial/mixed 상태는 실패

4. 블록별 위치 확정
   - 기존 원문 주석, anchor, occurrence로 기존 locale 문서의 대응 블록 탐색
   - 유일하게 확정되지 않으면 실패

5. provider 호출 또는 결정적 처리
   - 소유 단위에 따라 provider 필요 여부 판정
   - provider 필요 블록: new_source 전체를 전달하고 응답 수신
   - provider 불필요 블록: 결정적으로 생성

6. response contract 검증
   - 구조 보존·annotation·언어 규칙 검증
   - 위반 시 feedback 포함 재요청 (완료 응답 최대 2회)

7. 후처리 인계
   - PatchPlan의 모든 번역 대상에 대응하는 검증된 블록이 있는지 확인
   - provider 불필요 블록을 포함한 출력 수와 계획 대상 수의 일치 확인
   - PatchPlan, 블록 집합, placeholder 매핑을 후처리 단계에 전달
```

---

## 7. 소유 단위 정의

| 소유 단위 | provider | 적용 범위 |
|-----------|----------|-----------|
| 일반 문단·목록·heading | 필요 | annotation이 대응하는 완전한 블록 또는 연속 블록 범위 |
| 독립 fenced-code-only 변경 | 불필요 | 원문 전체 code block을 그대로 교체 |
| bare 내부 링크 목록 | 불필요 | 원문 구조 블록을 그대로 반영 |
| inline-code 식별자 목록 | 불필요 | 원문 구조 블록을 그대로 반영 |
| 표 (지원 조건 내) | 필요 | 변경 전후 각 한 행, 열 수 동일, separator가 아닌 기존 행 |
| admonition 본문 | 필요 | marker는 구조 context로 유지, 연속 변경 본문 segment |
| admonition marker 유형 변경 | 필요 | marker + 연속 quote 본문 전체 |
| named `<a name="...">` 한 줄 추가·삭제·rename | 불필요 | source occurrence와 target count로 정확한 한 줄 선택 |
| section 순서 변경 (내용 동일) | 불필요 | named anchor 기준 section 전체를 목표 순서로 이동 |

prose와 fence가 한 연속 변경 범위에 함께 있으면 전체를 provider 필요 블록으로 취급한다.

---

## 8. provider 계약

### 8.1 공통 인터페이스

provider adapter는 `TranslationRequest`를 받아 번역 Markdown 문자열만 반환하는 seam이다. 설명, 위치 지시, wrapper 문구를 출력하지 않는다.

### 8.2 adapter별 요구사항

| adapter | 요청 구조 | 완료 판정 |
|---------|-----------|-----------|
| OpenAI | `instructions` / `input` 분리, Responses API, `store=false` | `status=completed`일 때 `output_text` |
| Azure OpenAI | system / user 메시지 분리, Chat Completions | `finish_reason=stop`일 때 첫 assistant message content |
| CLI | 임시 디렉터리에서 실행, 사용자 설정·execpolicy·AGENTS.md 제외 | `--output-last-message` 파일 내용 |

### 8.3 CLI adapter 보안 경계

- browser, computer, image generation, plugin, shell, app, subagent, web search, hook을 끈다.
- child process에는 인증·runtime·proxy/CA allowlist 환경 변수만 전달한다.
- model이 실행하는 subprocess에는 환경 변수를 상속하지 않는다.

### 8.4 요청 템플릿

```text
# Translation Sync Input

## English Diff
{정규화된 effective delta — 값이 있을 때만 포함}

## English Source
{완전한 최신 source 블록}

## Existing Translation Context
{기존 locale 문맥 또는 (none)}

## Previous Output Verification Failure
{이전 완료 응답의 검증 issue — 값이 있을 때만 포함}

## Output
Return only the translated Markdown block(s) for the English Source.
```

번역 규칙과 annotation 형식은 user payload가 아닌 locale prompt와 공통 system instructions로 전달한다.

---

## 9. response contract

provider 응답은 적용 전에 다음을 모두 통과해야 한다.

| 검증 항목 | 규칙 |
|-----------|------|
| annotation 순서·occurrence | source와 정확히 대응 |
| Markdown block 수·순서 | source와 일치 |
| 목록 들여쓰기·checkbox 상태 | source와 일치 |
| 인용 깊이·canonical admonition 유형 | source 경고 수준 보존 |
| 표 열·정렬자 | source와 일치 |
| front matter 구조 값 | YAML 문자열 scalar, collection/bool/null/숫자/날짜 불허 |
| 보존 HTML/JSX 속성 | identifier·operator 구조 보존 |
| emphasis delimiter | 단일·이중 구분 source와 일치 |
| inline-link label·target·pair·title | source와 일치 |
| reference definition | 정규화 label과 raw target·title의 ordered occurrence 일치 |
| prose 줄 수 | 명시적 hard break 없으면 물리 한 줄 |
| 목표 언어 충분성 | 충분히 긴 영어 본문을 그대로 반환하면 거부 |
| source 밖 주석 | 추가 시 거부 |
| 표 prose cell | 목표 언어 요구, data cell(코드·링크·식별자·타입·설정 값·버전·날짜)은 원문 허용 |

### 9.1 verification feedback

주석만 남고 본문이 없거나, source 밖 prose·구조 주석이 추가되거나, 영어 본문을 그대로 반환하거나, 목표 문자 범위가 부족한 경우 feedback을 포함해 완료 응답을 블록당 최대 2회 요청한다 (자동 재요청 1회). 계속 실패하면 해당 locale target을 기록하지 않는다.

---

## 10. retry 정책

### 10.1 transient 재시도

| 대상 오류 | 처리 |
|-----------|------|
| 요청 timeout | 재시도 |
| 네트워크 연결 실패 | 재시도 |
| 응답 본문 미수신 | 재시도 |
| HTTP 429 / 5xx | 재시도 |
| CLI timeout | 재시도 |

| 비재시도 대상 | 처리 |
|---------------|------|
| CLI 실행 파일 누락·권한·option/model/auth 오류 | 즉시 실패 |
| HTTP 4xx (429 제외) | 즉시 실패 |
| 부분 응답 (OpenAI status ≠ completed, Azure finish_reason ≠ stop) | 저장하지 않고 실패 |

### 10.2 재시도 상한

- 한 논리 요청당 물리 provider 호출: 초기 요청 포함 최대 **3회**
- 재시도 간 대기: **5분**
- SDK 내부 재시도: 사용하지 않음
- verification feedback 포함 재요청: 완료 응답 최대 **2회** (블록당)
- 최악 물리 호출 상한: 블록당 최대 **6회** (3회 × 2 논리 요청)

### 10.3 최종 실패

최대 재시도 후에도 유효 응답이 없으면 해당 locale target을 기록하지 않고, 기존 locale 파일을 변경하지 않는다.

---

## 11. 실패 정책

| 실패 유형 | 처리 |
|-----------|------|
| effective delta가 비어 있음 (정규화로 모든 raw delta 제거) | 해당 문서를 번역 대상에서 제외 |
| 위치 확정 불가 (anchor 모호, 대상 없음) | 문서 미수정, locale target 실패 |
| annotation 상태가 partial/mixed | 문서 미수정, locale target 실패 |
| 표 구조 조건 불충족 (열 수 불일치, 복수 행, separator) | 해당 블록 실패 |
| admonition marker가 old/new 외 제3 유형 | 해당 블록 실패 |
| front matter 변경 또는 standalone source HTML comment 추가·삭제·수정 | provider 호출 전 실패 |
| response contract 위반 후 재요청도 실패 | locale target 미기록 |
| transient 오류 최대 재시도 초과 | locale target 미기록 |

모든 실패는 fail-closed로 처리한다. 기존 locale 문서를 부분적으로 수정한 상태로 남기지 않는다.

---

## 12. 수용 기준

번역 단계 출력이 다음 조건을 모두 만족해야 [후처리 단계](./03-postprocessing.md)로 전달한다.

1. PatchPlan의 모든 번역 대상 블록에 대해 provider 응답 또는 결정적 생성 결과가 존재한다.
2. 모든 provider 응답이 response contract를 통과했다.
3. 블록 출력 수와 PatchPlan 대상 수가 정확히 일치한다.
4. locale 문서 상태가 source, target 또는 명시적으로 허용된 unguarded 상태 중 하나로 판정되었다.
5. source 상태의 각 계획에 대해 적용 위치가 유일하게 확정되었다.
6. placeholder 매핑이 번역 중 변경되지 않았다.
7. 기존 locale 문서는 후처리 단계에 인계하기 전까지 변경되지 않았다.
