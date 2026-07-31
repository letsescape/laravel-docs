# 문서 검증 단계 설계

## 목적

번역 provider 응답 계약(response contract)을 통과한 locale 문서가 최신 영어 기준본의 구조를 정확히 보존하는지 최종 확인한다. 이 단계는 번역 의미·문체 평가가 아닌 자동 판정 가능한 구조 정합성만을 소유한다.

## 범위

- response contract 이후, 최종 문서 기록 직전의 전체 구조 검증을 수행한다.
- 코드, 링크, 앵커, 이미지, heading, admonition, placeholder 보존을 확인한다.
- 번역 의미 정확성, 용어 선택, 문체, 일반 HTML 렌더링은 이 단계의 자동 판정 범위가 아니다.

## 입력

| 항목 | 설명 |
|---|---|
| 최종 locale 문서 | 전처리·번역·후처리를 거친 검증 대상 |
| 최신 영어 기준본 | upstream raw source에 동일 전처리·후처리를 적용한 전체 문서 |
| 문서 version | 상대 링크와 절대 URL의 버전 동등 비교에 사용 |

## 출력

| 항목 | 설명 |
|---|---|
| issue label 목록 | 발견된 구조 위반의 분류 label 집합 |
| 빈 목록 | 검증 통과를 의미 |

## 불변조건

1. **구조 검증과 번역 의미 평가의 경계**: 자동 판정은 원문 대비 구조 보존만을 대상으로 하며, 번역 품질·의역·문체는 live provider 검토 영역이다.
2. **Fail-closed**: 판정 불가 상태는 통과가 아닌 실패로 처리한다. issue가 하나라도 존재하면 해당 locale target은 기록하지 않는다.
3. **저장소 오염 방지**: 검증 실패 시 기존 locale 파일을 덮어쓰지 않는다. 실패 응답은 최종 문서에 기록하지 않는다.
4. **기준본 단일성**: 비교 기준은 항상 최신 전체 영어 기준본이며, 과거 locale 문서의 형식 차이를 소급하지 않는다.

## 검증 순서

```text
1. 최종 locale 문서의 fenced code block 목록과 본문을 영어 기준본과 대조
2. inline 코드 multiset을 영어 기준본과 대조
3. Markdown inline link target·label pair를 정규화 후 영어 기준본과 대조
4. reference definition label·target·title·occurrence 순서를 영어 기준본과 대조
5. reference-style link·image의 해석 결과(image 여부·target·title) 순서를 대조
6. 명시적 <a name> 앵커 multiset을 영어 기준본과 대조
7. ATX heading 텍스트와 레벨 순서를 영어 기준본과 대조
8. HTML <img> src 순서를 영어 기준본과 대조
9. admonition marker 유형 순서를 영어 기준본과 대조
10. 순서 없는 목록 marker 수가 영어 기준본 이상인지 확인
11. 잔존 패턴 검사: base64 placeholder, {{version}}, legacy note marker, heading 스타일 클래스
12. 닫히지 않은 <img> 태그 검사
13. issue label 목록 반환
```

## 실패 정책

| 상태 | 처리 |
|---|---|
| issue label이 하나 이상 | 해당 locale target 실패, 문서 기록 차단 |
| 영어 기준본 부재 | 구조 대조가 불가능하므로 검증 실패 처리 |
| API 장애로 번역 미완료 | 검증 미진입, provider 단계에서 target 실패 처리 |

## 수용 기준

검증을 통과한 산출물은 다음을 모두 만족한다.

1. 최신 영어 기준본의 fenced code block 목록과 본문이 locale 문서에서 일치한다.
2. inline 코드 multiset이 영어 기준본과 일치한다.
3. 정규화된 inline link target·label pair가 영어 기준본과 일치한다.
4. reference definition과 reference-style link·image 해석 결과가 영어 기준본과 일치한다.
5. 명시적 `<a name>` 앵커 multiset이 영어 기준본과 일치한다.
6. ATX heading 텍스트와 레벨 순서가 영어 기준본과 일치한다.
7. HTML `<img>` 태그가 self-closing이며 `src` 순서가 영어 기준본과 일치한다.
8. admonition marker 유형 순서가 영어 기준본과 일치하고 중복·이탈이 없다.
9. fenced code 밖에 base64 placeholder, `{{version}}`, legacy note marker, heading 스타일 클래스가 잔존하지 않는다.
10. 닫히지 않은 `<img>` 태그가 없다.

## 오류 분류 경계

이 단계는 구조 issue를 반환할 뿐 진입점 종료 코드를 직접 결정하지 않는다. 구조 검증 실패의 오류 분류와 실행 중단·복구 정책은 [오류 처리 및 복구 설계](./08-error-cases.md)를 따른다.

## 부록: 링크 정규화 규칙

- 현재 검증 문서 버전과 같은 절대 docs URL prefix는 상대 경로와 동등하게 본다.
- 알려진 upstream stale 링크는 양쪽에 동일한 정규화를 적용하여 기존 보정본과의 위양성을 방지한다.
- `{{version}}` placeholder는 후처리에서 대상 버전으로 치환된 상태를 비교한다.

## 부록: 자동 판정 범위 밖 항목

Fail-closed 원칙은 이 문서가 요구하는 모든 구조 기준에 적용된다. 아래 항목은 구조 기준 밖이므로 issue 부재만으로 품질이 입증되지는 않으며, 각각 번역 응답 계약 또는 사이트 검증의 별도 기준을 따라야 한다. 범위 밖 항목 때문에 필수 구조 기준을 판정할 수 없다면 제외하지 않고 구조 issue로 처리해야 한다.

- 번역 의미의 정확성, 용어 선택과 문체
- admonition 유형의 문맥상 적합성
- 일반 HTML 태그의 렌더링 가능성
