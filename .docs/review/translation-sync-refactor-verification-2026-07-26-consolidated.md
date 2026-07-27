# Translation Sync 통합 재검증 보고서

검증일: 2026-07-26 KST

기준 커밋: `645a2d4a374c5d7eb8a1a1d4d8678e7effce4b0a`

검증 지시서: 프로젝트 루트 `prompt.md` (`SHA-256 d43aee151ee23d7584c53c86c4441d5c3cd753737e82e53d3f1e91dbdb5d2e95`)

최신 동결본: `.review/latest-gate-abbd78d4/frozen/`

최신 gate/재현 log: `.review/latest-gate-abbd78d4/logs/`

live/A.6 사본: `.review/verify-fixes-20260726-104813/`

이 문서는 기존 보고서를 수정하거나 대체하지 않는다. 다음 다섯 문서를 처음부터 끝까지 읽고, 각 보고서가 다룬 스냅샷과 현재 로컬 변경을 분리해 재검증했다.

- `translation-sync-refactor-review-2026-07-15.md`
- `translation-sync-refactor-verification-2026-07-26.md`
- `translation-sync-refactor-verification-2026-07-26-independent.md`
- `translation-sync-refactor-verification-2026-07-26-supplement.md`
- `translation-sync-fixes-verification-2026-07-26.md`

## 1. 결론

**판정: merge 불가. 부록 A.7의 완료 조건을 충족하지 못했다.**

1. 현재 동결본에서 N-02/N-16/N-17/N-26/N-27/N-28의 P1 silent-accept 또는 정상 sync 차단이 재현된다. N-18은 provider gate가 보강됐지만 final-only non-`img` 경로가 남은 부분 해결이고, N-24의 직접 type-drift fixture는 해결됐다.
2. live는 mini A.5 0/3, Luna A.5 0/3이며 artifact 0/6, 사람 판정 0/6, A.6 no-op 0/6이다.
3. A.2/A.3 exact 절차와 2.3이 실패한 뒤 호환 runner를 사용했고 production 변경도 남아 있어 A.7은 검증 미완료다.

## 2. 검증 스냅샷

### 2.1 서로 다른 세 범위

움직이는 worktree의 결과를 한 판정으로 합치지 않았다.

| 범위 | 고정 값 | 사용 목적 |
|---|---|---|
| clean commit | `645a2d4`, `main..HEAD` 1 commit, 74 files +13,232/-1,288 | clean smoke와 선행 주장 비교 |
| live 고정본 | 38 tracked, +1,907/-215, diff SHA-256 `644c9bb75cef0f1bf9d4613e213ddbdafca78cfeb6aed30633f9080426cc9444` | 두 모델 × 3회 provider/live/no-op |
| 최신 로컬본 | 78 tracked, +11,294/-1,270, diff SHA-256 `abbd78d475084e903b407547a012cbd93b72d5b75b332a081cd33d9c12b216d7` | 최종 코드·회귀·Docker gate |

최신본에는 untracked production 파일 세 개가 있다. `translation-sync/sync/common/files.py` SHA-256은 `13a0baeff5a20fcd321e1d3ea8db8651b692ff475455a3dda2e02c6932e78a03`, `versions.py`는 `9dce87540dc707711b028182bef6b61a7615df5ad7dc680375a3a1a7fe35f6fb`, `tests/test_files.py`는 `61cefdec9649e62e02b2e456f766f3359d6279c0887c7f525c357391105d8503`다. 세 파일을 동결 사본에 별도로 복사했다. `17:11:25~17:12:57 KST` 90초 이상 active diff가 동일함을 확인한 뒤 동결했고, 78 tracked overlay와 세 untracked production 파일을 합친 81-file frozen mismatch는 0이다. 동결 직전 active diff hash도 `abbd78d4…`로 동일했다.

live 6회는 동일한 38-file 고정본과 다음 입력을 사용했다.

- upstream ref: `b0b1c3e17c715880e0c380cd30061da6ca952c9d`
- manifest SHA-256: `971bd608d3117cf70596f9c5c76b033d6b793ffde39c1f54fe8a4d3ad415ac39`
- 고정 문서: `version-13.x/ai-sdk.md`

### 2.2 실행 환경과 credential 취급

| 항목 | 실제 값 |
|---|---|
| Python | 3.14.6 |
| uv(host / Docker pin) | 0.11.31 / 0.11.32 |
| Node / `.nvmrc` | 26.5.0 / 26 |
| npm | 11.17.0 |
| act | 0.2.89 |
| Docker / Compose | 29.1.3 / 5.0.1 |
| live provider | OpenAI 경로 |
| reasoning effort | medium |

`dot_env`는 일반 파일, 현재 사용자 소유, 권한 `0600`임을 값 출력 없이 확인했다. 값을 사람이 읽거나 log에 출력하지 않았고 clone, Docker image, build context에 복사하지 않았다. root `.env`는 접근하지 않았다.

부록 A.2의 awk는 macOS awk에서 변수명 `index`가 builtin과 충돌해 exit 2였다. 변수명만 `i`로 바꾼 동등한 무출력 검사는 통과했다. 부록 A.3 exact runner는 `dot_env`의 세 번째 줄을 `unquoted whitespace`로 거부했다. live에는 secret key의 strict whitespace 규칙을 유지하고 비밀이 아닌 설정 key의 trailing comment만 제거하는 호환 runner를 썼다. 따라서 live는 provider 진단 증거지만 exact A.3 통과 증거는 아니다.

A.2는 `prompt.md:479-502`의 awk program을 byte-for-byte 실행했고 secret stdout은 `/dev/null`로 보냈다. 정제하지 않은 실제 stderr/exit는 다음과 같다.

```text
awk: syntax error at source line 11
 context is
        for >>>  (index= <<< 1; index<=4; index++) {
awk: illegal statement at source line 11
awk: illegal statement at source line 11
A2_EXACT_EXIT=2
```

A.3 exact runner의 안전한 사전 재현 명령과 실제 출력은 다음과 같다. runner가 하위 `make`를 시작하기 전에 실패했으므로 credential 값은 출력되지 않았다.

```sh
python3 .review/translation-sync-local-validation-20260726-104656/credential_runner.py \
  "$PWD/dot_env" "$PWD" gpt-5.4-mini make -n translation-test
```

```text
unquoted whitespace at line 3
A3_EXACT_EXIT=1
```

### 2.3 변경·commit 상태

검증 전후 HEAD는 `645a2d4`로 동일하다. commit, merge, rebase, tag, push를 실행하지 않았다. 검증 담당자가 만든 변경은 `.review`와 이 새 보고서뿐이다. 다만 전체 worktree에는 병행 작업의 production 변경 78개와 untracked `files.py`, `versions.py`, `test_files.py`가 있으므로 A.7의 “전체 변경이 `.review`와 보고서뿐”이라는 조건은 worktree 전체 기준으로 미충족이다.

### 2.4 F-01(P0) 종료 근거

F-01은 닫혔다. `translation-sync/sync/__init__.py:3-5,15,20-40`은 flat import 호환 alias와 canonical package import를 분리하고, 하위 모듈 namespace를 보존해야 하는 `sync.sidebar`만 `sys.modules` flat alias 등록에서 제외한다고 명시한다. `tests/test_sidebar.py:13-18`의 `SidebarSyncTests.test_sync_sidebar_attribute_is_the_sidebar_package`가 package/generator object identity를 고정한다.

fresh process의 flat/canonical/interleaved/sidebar/provider/main-first 6개 순서 probe는 `identities=12/12`, `sidebar=package`, `duplicate_origins=0`, `partially_initialized=0`, `static_cycles=[]`, `result=PASS`였다. 관련 frozen 명령도 15/15 통과했다.

```sh
docker run --rm --network none \
  laravel-docs-translation-local-validation:1dee6ee0-overlay \
  uv run --locked --offline python -m unittest -v \
  tests.test_provider_check \
  tests.test_sidebar.SidebarSyncTests.test_sync_sidebar_attribute_is_the_sidebar_package
```

```text
Ran 15 tests in 0.043s
OK
```

`translation-sync/docs`의 숫자 문서는 정확히 00~08이고 `07-local-replay.md`, `08-error-cases.md`가 존재한다. legacy `07-error-cases.md` 파일·참조는 0, `00-workflow-summary.md`의 01~08 참조와 실제 내부 Markdown link 19개는 broken 0이었다. 전체 probe와 출력은 `.review/f01-import-evidence-1dee6ee0/evidence.md`에 있다.

## 3. gate 결과표

명령 성공, 대체 검증, prompt의 정식 절차 통과를 구분했다.

| # | gate | 실제 결과 | 판정 |
|---|---|---|---|
| 2.1 | Python 단위 테스트 | clean Docker 419/419 PASS; 최신 mount-free offline overlay 696/696, 1 skip | clean PASS / 최신 대체 regression PASS, fresh build 미실행 |
| 2.2 | replay 계약 | 실제 679-doc replay는 commit 생성 때문에 금지; mount-free `tests.test_replay` 34/34, 1 skip | 대체 확인 |
| 2.3 | workflow | `act -l`은 `sync` 1 job 파싱; online은 action ref fetch 실패, offline은 SHA cache 부재 | FAIL |
| 2.4 | artifact smoke | clean base `0 file(s)`는 PASS; live checkout 6/6은 직접 validator FAIL | FAIL(live) |
| 2.5 | Markdown link | clean PASS; 최신 mount-free site overlay 1/1 | clean/최신 대체 PASS |
| 2.6 | typecheck/build/anchor | 최신 typecheck·KO/JA build PASS, 46,626/46,626, missing 0 | 최신 대체 PASS, fresh build는 network FAIL |
| 2.7 | diff check | clean·live 6회·최신 tracked diff 모두 무출력 | PASS |
| 2.8 | provider check | mini/Luna의 KO/JA는 호환 runner에서 PASS; 선행 2.3과 exact A.3이 실패 | 비정식 진단 PASS / prompt gate FAIL |
| 2.9 | live 번역 | mini raw 2/3, Luna raw 1/3; 정식 A.5는 각 0/3 | FAIL |
| 2.10 | 후속 gate/사람 검토 | raw host site 6/6, diff 6/6, artifact 0/6, 일관된 사람 판정 0/6 | FAIL |
| 2.11 | F-01 종료 | import seam과 docs 번호 체계 확인 | PASS |
| A.6 | no-op | 유효 raw 성공 checkout 3건 중 0/3; 요구 coverage는 0/6 | FAIL |

### 3.1 최신 deterministic 명령

최신 image는 `laravel-docs-translation-local-validation:1dee6ee0-overlay`, image ID는 `sha256:6a9b426bd1f8a982ba1f6380a0df69b74d9b92e974c162c82942c1bd2baa006b`다. 원 `Dockerfile.translate` fresh build는 이전 `a6b6d3e4` gate에서 dependency CDN의 `httpx` download timeout으로 완료되지 않았고, 1dee gate에서는 반복하지 않았다. `pyproject.toml`과 `uv.lock`이 a6 image와 byte-identical함을 확인한 뒤 정확한 1dee frozen source/workflow/docs를 COPY하고 `uv sync --locked --offline`한 대체 image를 썼다.

```sh
docker run --rm --network none \
  laravel-docs-translation-local-validation:1dee6ee0-overlay \
  env PYTHONPATH=. \
  uv run --locked --offline --python 3.14 \
  python -m unittest discover -s tests
```

실제 재실행 출력:

```text
Ran 696 tests in 3.855s
OK (skipped=1)
```

image에는 workflow fixture와 두 untracked helper가 있고 `dot_env`와 `.env`는 없다. 2,275개 tracked 파일, 78개 overlay, 두 helper 및 image 포함 범위 2,129개 mismatch가 모두 0이고 `git diff --check`도 통과했다. 이 결과는 host mount와 network가 없는 regression gate지만 원 Dockerfile fresh-build PASS로 승격하지 않는다.

replay 계약의 focused 명령과 끝부분 출력은 다음과 같다. 실제 full replay는 내부 임시 commit을 만들므로 실행하지 않았다.

```sh
docker run --rm --network none \
  laravel-docs-translation-local-validation:1dee6ee0-overlay \
  env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. \
  uv run --locked --offline --python 3.14 \
  python -m unittest tests.test_replay
```

```text
Ran 34 tests in 2.279s
OK (skipped=1)
```

site input과 package-lock도 바뀌어 기존 결과를 상속하지 않았으며, 최신 1dee frozen input에서 네 npm 단계를 별도로 다시 실행했다. 원 Dockerfile build는 project-local buildx state를 쓴 재시도에서도 `npm ci` network timeout으로 실패했다. 대신 package/package-lock SHA-256이 최신 frozen과 정확히 같은 a6 fresh-`npm ci` image(`sha256:4cb4e1e1c8bc…`) 위에 1dee frozen source를 COPY한 `laravel-docs-site-local-validation:1dee6ee0-overlay`를 썼다. 최신 site image ID는 `sha256:1be18bd1793cb34ef9db90700d093ed2701faa6f9fd1a85d637191f5f2746622`다.

site image와 frozen source의 2,220-entry manifest diff는 0이고 전체 manifest SHA-256은 `0fed2eee2f7c5abd02f1dd4fd7d0723dd35c5e389e4accab5d4f4570d4af09ea`다.

```sh
docker run --rm --network none \
  laravel-docs-site-local-validation:1dee6ee0-overlay sh -lc '
    npm run test:markdown-links &&
    npm run typecheck -- --pretty false &&
    npm run build &&
    npm run validate-anchors
  '
```

```text
tests 1
pass 1
fail 0
[ko] Generated static files in "build".
[ja] Generated static files in "build/ja".
Total anchor links:  46626
  OK (id in HTML):   46626
  Target HTML gone:  0
  id not found:      0
[gate] PASS
```

### 3.2 실패 log

live harness는 `.review/verify-fixes-20260726-104813/run-a7.sh:27-44`에 있다.

```sh
bash .review/verify-fixes-20260726-104813/run-a7.sh
```

| 증거 | 원문 log와 실제 출력 |
|---|---|
| mini 1 | `logs/gpt-5.4-mini-run-1.log:1-7`: `provider inline code mismatch` |
| Luna 1 | `logs/gpt-5.6-luna-run-1.log:1-6`: `provider untranslated source text, provider target language mismatch` |
| Luna 3 | `logs/gpt-5.6-luna-run-3.log:1-6`: 위와 동일 |
| artifact | `logs/*-artifact.log`: `unpaired translation document` 및 허용되지 않은 생성 경로, exit 1 |
| act online | `.review/translation-sync-local-validation-20260726-104656/logs/act-dryrun-final.log`: setup-node ref fetch 후 job failure |
| act offline | 같은 경로 `act-dryrun-offline.log`: 지정 SHA local cache 부재 |

2.3의 실패 재현 명령은 다음과 같다.

```sh
act workflow_dispatch \
  --dryrun \
  -W .github/workflows/sync-translation.yml \
  --input version=13.x \
  --input doc=ai-sdk.md
```

원문 log가 18줄이므로 앞뒤 20줄을 줄이는 대신 전체를 인용한다.

```text
time="2026-07-26T12:16:53+09:00" level=info msg="Using docker host 'unix:///var/run/docker.sock', and daemon socket 'unix:///var/run/docker.sock'"
level=warning msg= ⚠ You are using Apple M-series chip and you have not specified container architecture, you might encounter issues while running act. If so, try running it with '--container-architecture linux/amd64'. ⚠

*DRYRUN* [Sync Documentation Translation/Sync translations] ⭐ Run Set up job
*DRYRUN* [Sync Documentation Translation/Sync translations] 🚀  Start image=node:26-alpine
*DRYRUN* [Sync Documentation Translation/Sync translations]   🐳  docker pull image=node:26-alpine platform= username= forcePull=false
*DRYRUN* [Sync Documentation Translation/Sync translations]   🐳  docker create image=node:26-alpine platform= entrypoint=["tail" "-f" "/dev/null"] cmd=[] network="host"
*DRYRUN* [Sync Documentation Translation/Sync translations]   🐳  docker run image=node:26-alpine platform= entrypoint=["tail" "-f" "/dev/null"] cmd=[] network="host"
*DRYRUN* [Sync Documentation Translation/Sync translations]   ✅  Success - Set up job
*DRYRUN* [Sync Documentation Translation/Sync translations]   ☁  git clone 'https://github.com/astral-sh/setup-uv' # ref=fac544c07dec837d0ccb6301d7b5580bf5edae39
*DRYRUN* [Sync Documentation Translation/Sync translations]   ☁  git clone 'https://github.com/actions/setup-node' # ref=249970729cb0ef3589644e2896645e5dc5ba9c38
*DRYRUN* [Sync Documentation Translation/Sync translations] Unable to resolve 249970729cb0ef3589644e2896645e5dc5ba9c38: reference not found
*DRYRUN* [Sync Documentation Translation/Sync translations] Unable to resolve 249970729cb0ef3589644e2896645e5dc5ba9c38: reference not found
*DRYRUN* [Sync Documentation Translation/Sync translations] reference not found
*DRYRUN* [Sync Documentation Translation/Sync translations] ⭐ Run Complete job
*DRYRUN* [Sync Documentation Translation/Sync translations]   ✅  Success - Complete job
*DRYRUN* [Sync Documentation Translation/Sync translations] 🏁  Job failed
Error: reference not found
```

최신 site 원 Dockerfile build 실패의 exact 명령은 다음과 같다.

```sh
set -o pipefail
BUILDX_CONFIG="$PWD/.review/latest-gate-1dee6ee0/buildx" docker build --progress=plain \
  -t laravel-docs-site-local-validation:1dee6ee0 \
  .review/latest-gate-1dee6ee0/frozen \
  2>&1 | tee .review/latest-gate-1dee6ee0/logs/site-image-build-retry1.log
```

실패 지점과 뒤 출력은 다음과 같고 exit는 1이다.

```text
#9 [ 5/13] RUN npm ci
#9 366.3 npm error code ECONNRESET
#9 366.3 npm error network aborted
#9 366.3 npm error network This is a problem related to network connectivity.
#9 366.3 npm error network In most cases you are behind a proxy or have bad network settings.
#9 366.3 npm error network
#9 366.3 npm error network If you are behind a proxy, please make sure that the 'proxy' config is set properly.
#9 366.3 npm error A complete log of this run can be found in: /root/.npm/_logs/2026-07-26T06_49_24_672Z-debug-0.log
#9 ERROR: process "/bin/sh -c npm ci" did not complete successfully: exit code: 1
------
Dockerfile:11
--------------------
   9 |
  10 |     COPY package.json package-lock.json ./
  11 | >>> RUN npm ci
  12 |
  13 |     COPY docusaurus.config.ts sidebars.ts tsconfig.json versions.json ./
--------------------
ERROR: failed to build: failed to solve: process "/bin/sh -c npm ci" did not complete successfully: exit code: 1
```

mini 1의 7줄짜리 원문 log 전체는 다음과 같다.

```text
translating: ko i18n/en/docusaurus-plugin-content-docs/version-13.x/ai-sdk.md
translating: ja i18n/en/docusaurus-plugin-content-docs/version-13.x/ai-sdk.md
verify failed: ja i18n/en/docusaurus-plugin-content-docs/version-13.x/ai-sdk.md: ['partial translation failed: provider response contract failed: provider inline code mismatch']
stopping after first verification failure
version-13.x: 1 files
total: 1 files
upstream manifest: /app/.git/translation-upstream-refs.json
```

Luna 1과 Luna 3은 동일한 6줄을 남겼다.

```text
translating: ko i18n/en/docusaurus-plugin-content-docs/version-13.x/ai-sdk.md
verify failed: ko i18n/en/docusaurus-plugin-content-docs/version-13.x/ai-sdk.md: ['partial translation failed: provider response contract failed: provider untranslated source text, provider target language mismatch']
stopping after first verification failure
version-13.x: 1 files
total: 1 files
upstream manifest: /app/.git/translation-upstream-refs.json
```

artifact 대표 실패인 mini 2 log의 실패 시작점과 뒤 39줄 전체는 다음과 같다. 다른 5개 run도 같은 baseline 경로군과 `unpaired translation document` 사유로 exit 1이었다.

```sh
(
  cd .review/verify-fixes-20260726-104813/runs/gpt-5.4-mini/run-2/translation-sync
  python3 validate_generated_changes.py
)
```

```text
unexpected translation sync changes:
- .dockerignore
- .github/workflows/deploy.yml
- .github/workflows/sync-translation.yml
- .gitignore
- README.md
- translation-sync/main.py
- translation-sync/replay.py
- translation-sync/scripts/anchor-routes.mjs
- translation-sync/scripts/markdown-link-utils.test.mjs
- translation-sync/sync/__init__.py
- translation-sync/sync/common/markdown.py
- translation-sync/sync/postprocessing/postprocess.py
- translation-sync/sync/sidebar/generator.py
- translation-sync/sync/source/upstream.py
- translation-sync/sync/translation/patch.py
- translation-sync/sync/translation/translate.py
- translation-sync/sync/verification/response_contract.py
- translation-sync/sync/verification/verify.py
- translation-sync/tests/test_generated_changes.py
- translation-sync/tests/test_main.py
- translation-sync/tests/test_patch.py
- translation-sync/tests/test_postprocess.py
- translation-sync/tests/test_provider_check.py
- translation-sync/tests/test_replay.py
- translation-sync/tests/test_sidebar.py
- translation-sync/tests/test_translate.py
- translation-sync/tests/test_upstream.py
- translation-sync/tests/test_verify.py
- translation-sync/validate_generated_changes.py
invalid translation sync changes:
- unpaired translation document: version-10.x/errors.md
- unpaired translation document: version-10.x/helpers.md
- unpaired translation document: version-10.x/migrations.md
- unpaired translation document: version-8.x/database-testing.md
- unpaired translation document: version-8.x/eloquent-mutators.md
- unpaired translation document: version-8.x/errors.md
- unpaired translation document: version-8.x/migrations.md
- unpaired translation document: version-9.x/errors.md
- unpaired translation document: version-9.x/migrations.md
```

유효 no-op 원문은 `.review/translation-sync-local-validation-20260726-104656/logs/{gpt-5.4-mini-run-2,gpt-5.4-mini-run-3,gpt-5.6-luna-run-2}-noop.log`다. mini 두 건은 exit 0과 `translated 1 doc(s) into ko, ja`, Luna 한 건은 exit 1과 provider untranslated/target-language failure를 남겼다. 모두 첫 줄부터 `translating:`이며 `no source changes`는 없다. 세 diff hash는 재실행 전후 동일했지만 A.6의 명시 조건은 충족하지 못했다.

## 4. Track A 결과

| 항목 | 판정 | A-1 / A-2 / A-3 |
|---|---|---|
| F-02 | 부분적 | **A-1** `response_contract.py:1959-2231`; 본문 누락·exact echo·duplicate occurrence·extra block·문단→list의 독립 negative test가 있다. **A-2** 각 검사를 제거하면 대응 label 단언이 실패한다. **A-3** near-English(N-02)와 같은 물리 줄에 붙인 임의 추가 문장(N-26)은 provider/final 모두 `[]`다 |
| F-03 | 확인됨 | **A-1** `main.py:234-248,303,348-350`, `provider_check.py:115-125`; `test_rejects_paragraph_indented_as_a_code_block`, `test_rejects_modified_fenced_code`. **A-2** 어느 verifier 호출을 제거해도 label 단언이 실패한다. **A-3** 공유 호출 경로 자체를 우회하는 별도 완화 경로는 없다 |
| F-04 | 부분적 | **A-1** `verify.py:287-318,867-930`; internal/reference wrong-version test가 있다. **A-2** 버전까지 정규화하면 test가 실패한다. **A-3** `> <div>` container 뒤 definition은 `markdown.py:775-874`가 숨겨 13.x→12.x/title drift를 양 gate가 승인한다(N-06) |
| F-05 | 부분적 | **A-1** `patch.py:3535-3739`; named-anchor move, crossed ownership, TOC permutation test가 있다. **A-2** reorder/separator/ownership guard 제거 시 실패한다. **A-3** 유효한 `+ [Alpha](#alpha)` TOC swap은 `[-*]`만 받는 parser 때문에 `PatchError`로 막힌다 |
| F-06 | 부분적 | **A-1** `sync/runtime/config.py:46-87`, `main.py:823-828`; numeric option/config exit test가 있다. **A-2** validator/예외 변환 제거 시 실패한다. **A-3** Azure endpoint `not a url`, API version `yesterday`, model `not-a-model`은 non-empty라 config를 통과한다 |
| F-07 | 확인됨 | **A-1** `translate.py:27-82,410-483`; final-message와 `.env` 선검사 test가 env/cwd/flag를 고정한다. **A-2** allowlist, 임시 cwd, hook/tool disable 중 하나를 되돌리면 exact 인자/env 단언이 실패한다. **A-3** 신뢰된 CLI executable/PATH 전제 안의 구체적 우회는 찾지 못했다 |
| F-08 | 미확인 | **A-1** KO `translation-sync/prompt.md:9-18,45-70,176-188`, JA `translation-sync/prompt_jp.md:15-22,308-339`에 규칙은 있으나 `tests/test_prompt.py`는 파일 로딩만 검사한다. **A-2** 누락 금지를 되돌려도 test가 실패하지 않는다. **A-3** migration 절을 생략한 번역을 양 gate가 승인한다 |
| F-10 | 확인됨 | **A-1** `Dockerfile:2`, `package.json:40-42`와 1dee mount-free Node 26 site log. **A-2/A-3** 동일 frozen artifact의 markdown 1/1, typecheck, KO/JA build, anchor 46,626/46,626 실제 gate가 통과했다 |
| F-13 | 부분적 | **A-1** `preprocess.py:154-250,387-418`, `postprocess.py:165-207`, `markdown.py:1324-1394`; note/heading-ID/sentinel/style/list 전용 test가 있다. **A-2** 각 fix 제거 시 대응 test가 실패한다. **A-3** canonical opener-only와 escaped closer는 통과하지만 raw provider closer 및 comment/code-span 교차 경계가 남는다(N-16/N-22) |
| F-16 | 확인됨 | **A-1** `sidebar/generator.py:38-49,83-128,328-347`, `common/versions.py:8-42`; future-version/순서·중복 test가 있다. **A-2** 8.x~13.x 하드코딩 복원 시 14.x test가 실패한다. **A-3** production Python grep에서 해당 고정 목록이나 우회 fixture를 찾지 못했다 |

### Track B·생성물·CI·문서 정면 검토

| 범위 | 실제 판정과 근거 |
|---|---|
| patch 후보/tie·경계 | `main.py:379-398`은 raw/repaired/annotated 후보의 issue 수가 동률이면 첫 raw를 고른다. `patch.py:1177-1185,2821-2827,2938-2964`에는 unique substring/최단거리 best-estimate가 있고 `_apply_code_block()`은 후보가 1개가 아니면 원문을 돌려준다(`:2755-2765`). public 경로는 `:737-796` state guard와 `main.py:498-509` final gate로 대체로 fail-closed지만 N-09/N-20과 의미 tie-break 부재가 남는다 |
| contract 휴리스틱·retry | 누락/구조는 `response_contract.py:1971-2122`의 signature/Counter가 중심이고, 영어 echo·protected term·목표언어는 `:1475-1521,1704-1756,1835-1868` 임계값이다. 별도 block/물리 줄의 extra prose는 잡지만 같은 줄에 붙인 임의 지시는 놓친다(N-26). contract 위반은 한 번 재요청한 뒤 기록을 막아 false positive도 pipeline을 중단하며 N-25가 실제 예다 |
| Markdown parser 범위 | arbitrary-width/multiline code span, multiline reference, ≤3칸/blockquote fence 지원은 `markdown.py:52-91,600-1078,1249-1297`에 있다. raw-HTML container와 comment/code 경계는 N-06/N-16/N-22에서 실패한다. `docs/04-verification.md:143-151,211,393`도 전체 CommonMark parser가 아님을 명시한다 |
| provider 경계 | API/CLI 모두 `translate.py:323-332,404-407` 뒤 `main.py:234-248`의 같은 contract를 쓴다. timeout/network/429/5xx·빈 응답만 재시도하고 4xx/CLI usage는 즉시 중단한다(`translate.py:335-401`). OpenAI는 live 진단했지만 Azure adapter는 설정 부재로 미검증이다 |
| replay | active repo 내부 sandbox parent를 거부하고 local clone+overlay를 강제한다(`replay.py:188-197,290-332`). HEAD/tree/status/staged/untracked-byte fingerprint(`:89-133,681-746`)와 1차 commit 뒤 2차 fingerprint equality(`:620-647`)가 no-op 기준이다. 이는 구조·멱등성이지 번역 의미 검증이 아니다 |
| test 품질 | 최신 전체 suite와 replay 34개가 통과했다. patch 위치/멱등성, issue label, retry count, 실제 temp Git test는 독립 계약 표본이지만 `test_main.py:269-281`은 같은 verifier 결과를 기대값으로 쓰고 일부 patch negative는 사유 없이 `assertRaises`만 해 잘못된 거부 이유도 통과할 수 있다 |
| 생성 산출물 | boost table annotation 재배치는 KO/JA 12/13/master 6파일에서 같은 형태이고 JA 13 `ai-sdk.md` 정리도 인접 버전 패턴과 정합한다. 그러나 current code로 전체 committed 산출물 no-op은 live A.6 실패 때문에 미증명이다. `_ALLOWED_PATHS`는 지원 버전 top-level `[^/]+\.md` 전체를 허용하지만 fullmatch로 code/workflow/prompt/nested path는 차단한다(`validate_generated_changes.py:15-28,57-110`) |
| workflow·배포 | `sync-translation.yml:31-44` branch guard/credential persistence off, `:67-84` preflight status+manifest 보존, `:86-156` provider→sync→site→artifact→commit→push→deploy 순서다. push 직전에만 `gh auth setup-git`을 쓴다. Node는 `.nvmrc`, package, Dockerfile, 두 workflow, Makefile에서 모두 26이다. setup-node SHA 해석과 실제 push/dispatch는 act 실패로 미증명이다 |
| docs 00~08 | 00/05/07의 단계·rollback·credential·identity fingerprint 설명과 single-writer/TOCTOU 한계는 구현과 맞고 04는 parser 한계를 기록한다. N-24의 직접 type-drift fixture도 문서 주장대로 닫혔다. 다만 F-09의 여러 파일 publish는 run-level transaction이 아니고, F-14의 provider-free admonition patch 우회(N-27/N-28)와 parser 경계가 남아 전체 정합은 부분적이다 |

## 5. 신규 Finding 요약표

“Resolved”는 최신 `abbd78d4`에서 선행 재현이 닫혔다는 뜻이며, 과거 보고서가 틀렸다는 뜻은 아니다.

| ID | 심각도 | 요약 | 최신 상태 |
|---|---:|---|---|
| N-01 | P1 | 재정렬된 동일형 표의 다른 행을 덮어씀 | Resolved |
| N-02 | P1 | 마침표가 있는 짧은 near-English를 승인 | **Open** |
| N-03 | P1 | multiline inline-code의 `<style>` 삭제 | Resolved |
| N-04 | P2 | image alt-target 의미 association 검증 부족 | **Partial** |
| N-05 | P2 | EN-only `M` artifact 승인 | **Open** |
| N-06 | P3 | multiline reference title integrity gap | **Partial** |
| N-07 | P2 | locale-root symlink write 경계 | Resolved |
| N-08 | P2 | all-cell 변경 table row를 찾지 못함 | Resolved |
| N-09 | P2 | 정상 순서의 두 번째 localized admonition marker 변경 거부 | **Open** |
| N-10 | P2 | 일반 timeout을 transient retry에서 누락 | Resolved |
| N-11 | P3 | `013.x` semantic duplicate 허용 | Resolved |
| N-12 | P3 | root `--frozen`과 product `--locked` 불일치 | **Open** |
| N-13 | P2 | translation image의 workflow fixture 누락 | Resolved |
| N-14 | P1 | 긴 ALL-CAPS 영문 prose echo 승인 | Resolved |
| N-15 | P1 | legacy table 영문 prose echo 승인 | Resolved |
| N-16 | P1 | raw closer 및 comment/code-span 교차 경계 처리 실패 | **Partial / Open** |
| N-17 | P1 | permuted fenced insertion을 TARGET으로 오판정 | **Open** |
| N-18 | P1(잔여 P2) | 동적 JSX display expression 변경 승인 | **Partial** |
| N-19 | P2 | non-img display attribute의 provider/final 불일치 | **Open** |
| N-20 | P2 | 동일-shape 표의 wrong-owner annotation 승인 | **Open** |
| N-21 | P2 | blockquoted fence 뒤 quote ordinal 불일치 | **Open** |
| N-22 | P2 | Markdown literal 문맥의 `<!--` 오탐 | **Open** |
| N-23 | P2 | 빈 quote가 source annotation을 소유한 것으로 final 승인 | **Open** |
| N-24 | P1 | Warning/Caution을 NOTE로 하향해도 양 gate 통과 | Resolved |
| N-25 | P2 | legacy table의 자연스러운 단어 번역을 과보호 | **Open** |
| N-26 | P1 | 같은 문단 줄에 붙인 임의 추가 지시를 양 gate가 승인 | **Open** |
| N-27 | P1 | 단일 blockquote admonition의 본문 대응 검증 우회 | **Open** |
| N-28 | P1 | legacy admonition의 제3 type을 provider-free patch가 덮어씀 | **Open** |
| N-29 | P2 | admonition marker 교체 시 list 들여쓰기 유실 | **Open** |

## 6. 상세 Finding

N-01~N-25 Open/Partial 항목의 공통 exact fixture는 다음 고정 log에서 frozen production 함수를 직접 호출한다. N-16, N-26, N-27~N-29는 해당 상세 절의 별도 frozen probe를 쓴다.

```sh
PYTHONDONTWRITEBYTECODE=1 \
  python3 .review/latest-gate-21b6a340/logs/probe-open-findings.py
```

실제 전체 stdout은 `.review/latest-gate-21b6a340/logs/probe-open-findings.stdout.log`에 ID별 `[N-xx]` block으로 보존했다. 독립 재실행 세 번이 모두 고정 log와 `diff -u` exit 0이었고, script/log SHA-256은 각각 `a1d09501e034e0fb2762d22ead97c804b81f5cefca2edddc812ec7f21b6b314f`, `e4517afe06e42e47870af4a20c1402387401a9dc06d142794e1cf9fc537673a0`다. `abbd78d4`가 이 probe 대상 production 파일을 21b 이후 바꾸지 않았음을 byte 비교했으며, 최신 delta 별도 probe도 같은 판정을 확인했다. 따라서 아래 Open/Partial 항목의 입력과 “실제 반환”은 같은 ID block의 재현 명령·출력이다.

Resolved 항목은 §3.1의 최신 mount-free full-suite 명령과 각 항목에 적은 named regression test로 다시 확인했다. 아래 결과는 `abbd78d4…` 동결본 기준이며, 21b에 보존한 fixture는 최신본과 관련 production SHA가 동일한 경우에만 인용했다.

| Resolved ID | 최신 full-suite run에 포함된 정확한 회귀 test |
|---|---|
| `N-01` | `test_reordered_same_shape_tables_fail_closed_before_replacement` |
| `N-03` | `test_keeps_style_blocks_inside_multiline_code_spans` |
| `N-07` | `test_rejects_symlinked_locale_root_before_write`, `...root_parent`, `...version_root_with_internal_target`, `...document_with_internal_target` |
| `N-08` | `test_unique_all_cell_translated_row_uses_its_structural_address`, `test_all_cell_translated_row_with_two_tables_fails_closed` |
| `N-10` | `test_retries_cli_transport_failures`, `test_retries_http_429_and_5xx_errors`, `test_retries_cli_http_status_messages` |
| `N-11` | `test_sync_version_rejects_leading_zero_version_before_write`, `test_load_versions_rejects_duplicates_and_misordered_stable_versions` |
| `N-13` | `tests.test_replay` import/collection을 포함한 full suite와 §3.1의 별도 34-test run |
| `N-14` | `test_detects_all_caps_prose_echoes`, `test_rejects_all_caps_prose_echoes` |
| `N-15` | `test_detects_untranslated_prose_in_a_legacy_pipe_table`, `test_rejects_untranslated_prose_in_a_legacy_pipe_table`, 두 `...accepts_translated_prose...` |
| `N-24` | `test_rejects_changed_final_admonition_type`, `test_rejects_localized_legacy_admonition_type_downgrade`, `test_rejects_changed_final_admonition_type_in_markdown_containers`, `test_rejects_changed_provider_admonition_type_in_markdown_containers` |

### N-01. 재정렬된 동일형 표의 silent overwrite — P1

#### 근거

`sync/translation/patch.py:3200-3248`은 구조 주소와 ambiguity를 확인한다. 기존 fixture에서 실제 반환은 `PatchError: missing existing translation block for: | \`foo\` | Alpha old |`였다. `tests/test_patch.py:2259-2271`이 회귀를 고정한다.

#### 재현 조건

source와 locale에 동일 shape·동일 key 표 두 개를 반대 순서로 둔다.

#### 영향

과거에는 다른 표를 덮었지만 최신본은 fail-closed 한다.

#### 권고

현재 ordinal/cardinality/후보 모호성 guard를 유지한다.

#### 완료 조건

기존 fixture가 올바른 표만 수정하거나 명시적으로 거부되어야 한다. 최신본에서 충족했다.

### N-02. 짧은 near-English 승인 — P1

#### 근거

`response_contract.py:1511-1521`의 exact substring과 `:1835-1868,2214-2231`의 문자 비율을 다음 입력이 우회한다. final의 영어 잔존 판정은 `verify.py:461-469,983-984`다.

```text
source   = This Works.
target   = <!-- This Works. -->
           This Works예요.
provider = []
final    = []
```

마침표 없는 기존 test는 거부되지만 이 exact 문장부호 변형은 통과한다.

#### 재현 조건

source 문장부호를 visible body에서 제거하고 target 문자 몇 개만 붙인다.

#### 영향

사실상 미번역인 문장이 자동 기록될 수 있다.

#### 권고

문장부호·공백 정규화 후 token overlap/edit distance와 target-language 비율을 함께 본다.

#### 완료 조건

위 fixture와 같은 길이 영단어 치환 fixture를 거부하고 정상 identifier/product name은 통과한다.

### N-03. multiline inline-code style 삭제 — P1

#### 근거

`preprocess.py:201-258,387-415`가 multiline code span을 먼저 보호한다. `<style>` fixture에서 `preprocess(source) == source`가 `True`였고 `tests/test_preprocess.py:137-150`이 고정한다.

#### 재현 조건

multiline backtick span 안에 `<style>...</style>`을 둔다.

#### 영향

과거 원문 삭제 경로는 최신본에서 재현되지 않는다.

#### 권고

공통 inline scanner를 유지한다.

#### 완료 조건

span 내부는 byte-identical, 외부 page style만 제거되어야 한다. 최신본에서 충족했다.

### N-04. image alt-target association — P2

#### 근거

`repair.py:415-432`는 raw reorder를 `RepairError: translated Markdown image targets are reordered`로 막는다. 그러나 이미 alt를 서로 바꾼 두 image fixture는 `verify.py:247-258,875-893`의 target/title/order 비교를 통과해 `final=[]`였다.

#### 재현 조건

target 순서는 유지하면서 두 image의 번역 alt만 서로 교환한다.

#### 영향

접근성 문구가 실제 image 의미와 어긋날 수 있다.

#### 권고

target occurrence와 alt를 pair signature로 비교한다.

#### 완료 조건

repair reorder와 crafted swapped-alt를 모두 독립 사유로 거부해야 한다.

### N-05. EN-only `M` artifact 승인 — P2

#### 근거

`validate_generated_changes.py:94-101`은 EN status가 `{"M"}`이면 존재하는 locale만 검사하고 `continue`한다.

```text
validate_changes({"i18n/en/.../version-13.x/cache.md": {"M"}}, {"13.x"})
=> []
```

`tests/test_generated_changes.py:125-133`도 EN+JA, KO 누락을 승인한다.

#### 재현 조건

EN cache 문서만 `M`이고 대응 KO/JA status를 입력하지 않는다.

#### 영향

원문만 갱신된 반쪽 sync를 정상 no-change locale과 구분하지 못한다.

#### 권고

EN `M`에는 locale status 또는 byte-identical target임을 증명하는 manifest를 요구한다.

#### 완료 조건

EN-only 자동 산출은 거부하고 증명된 locale no-change만 통과시킨다.

### N-06. multiline reference title integrity — P3

#### 근거

`common/markdown.py:600-774,908-1064`의 multiline reference parser는 일반 continuation title drift를 provider/final의 `link title mismatch`로 검출한다. 그러나 `:775-874`의 raw-HTML range가 blockquote container 경계를 잃어 다음 definition까지 마스킹한다.

```markdown
> <div>
# Heading
[ref]: /docs/13.x/cache "Cache docs"
```

target에서 source annotation을 둔 뒤 target을 `/docs/12.x/cache "Changed docs"`로 바꿔도 `[N-06-container-boundary]`의 실제 출력은 `source_definitions=()`, `translated_definitions=()`, provider `[]`, final `[]`였다.

#### 재현 조건

blockquote에서 raw-HTML opener를 시작하고 다음 root heading 뒤 reference target/title을 바꾼다.

#### 영향

잘못된 version link와 title이 양 gate를 통과한다. 일반 multiline reference는 해결됐지만 container 경계 때문에 parser coverage가 완전하지 않다.

#### 권고

CommonMark block parser와 동일하게 raw-HTML block의 container/blank termination을 계산하거나, 모호한 경계 뒤 definition을 fail-closed 한다.

#### 완료 조건

root/blockquote/list 안의 raw HTML type별 fixture 뒤 reference target/title drift가 모두 명시적 사유로 거부된다.

### N-07. locale-root symlink write 경계 — P2

#### 근거

`annotate_cli.py:25-65`는 exact locale root, parent component, root/version/leaf symlink를 검사한다. root symlink fixture는 `ValueError: invalid locale root`였고 `tests/test_annotate.py:80-171`이 네 경계를 고정한다.

#### 재현 조건

locale root 또는 하위 component를 repo 내부 다른 tree로 향하는 symlink로 둔다.

#### 영향

의도하지 않은 내부 tree write는 최신본에서 차단된다.

#### 권고

lexical/canonical root equality 검사를 유지한다.

#### 완료 조건

네 symlink fixture가 write 전에 거부되어야 한다. 최신본에서 충족했다.

### N-08. 모든 cell이 바뀐 row 식별 — P2

#### 근거

`patch.py:3168-3248`은 유일한 table/row 구조 주소를 사용하고 다중 후보는 거부한다. 실제 출력은 유일 fixture `updated=True, old-removed=True`, 다중 fixture `PatchError`였다. `tests/test_patch.py:2273-2310`이 고정한다.

#### 재현 조건

한 row의 모든 source cell을 바꾸고 locale은 old/new English와 일치하지 않게 한다.

#### 영향

정상 upstream 표 변경 차단은 유일 후보에서 해결됐다.

#### 권고

모호한 후보의 fail-closed 정책을 유지한다.

#### 완료 조건

유일 row는 적용하고 다중 후보는 거부한다. 최신본에서 충족했다.

### N-09. 정상 순서의 두 번째 admonition marker 변경 거부 — P2

#### 근거

`patch.py:1772-1843`은 ordinal로 block을 고른 뒤에도 번역 body를 English `after_context` 또는 English comment와 비교한다.

```text
정상 순서 localized admonition 2개, 둘째 NOTE→WARNING
=> PatchError: could not verify existing admonition body: > Second body.
```

`tests/test_patch.py:2498-2519`는 reordered negative만 고정한다.

#### 재현 조건

정상 순서의 번역된 admonition 두 개에서 두 번째 source marker만 바꾼다.

#### 영향

명확한 경고 강도 변경이 자동 sync를 차단한다.

#### 권고

ordinal, source comment, 주변 stable anchor를 결합하고 후보가 모호할 때만 거부한다.

#### 완료 조건

첫째·둘째 marker flip은 올바른 block에 적용되고 reordered ambiguity만 거부된다.

### N-10. timeout retry corpus — P2

#### 근거

`translate.py:95-123,335-357`의 직접 probe는 `context deadline exceeded`, `read timeout`, `request timeout`, `timed out waiting`, `operation timed out`을 모두 `True`, auth/model 오류를 `False`로 분류했다. 관련 선택 test 19/19가 통과했다.

#### 재현 조건

CLI가 일반 timeout 문구와 non-zero exit를 반환한다.

#### 영향

선행 일시 장애 조기 종료 문제는 해결됐다.

#### 권고

transient/permanent corpus test를 유지한다.

#### 완료 조건

일반 timeout/429/5xx는 retry, auth/model/usage는 즉시 중단한다. 최신본에서 충족했다.

### N-11. leading-zero version — P3

#### 근거

현재 동결본에 포함한 untracked `common/versions.py:8-13`의 canonical regex가 `013.x`를 `ValueError: invalid version: 013.x`로 거부한다. upstream/sidebar 관련 test 2/2가 통과했다. 로컬 동작은 해결됐지만 전달 스냅샷 위험은 F-18에서 별도로 판정한다.

#### 재현 조건

versions 목록에 `13.x`와 `013.x`를 둔다.

#### 영향

semantic duplicate path 생성은 loader 단계에서 차단된다.

#### 권고

canonical token 검사를 유지한다.

#### 완료 조건

leading-zero token을 쓰기 전에 거부한다. 최신본에서 충족했다.

### N-12. `--frozen`/`--locked` 절차 불일치 — P3

#### 근거

root `prompt.md:74,652,684,729,818`은 `uv run --frozen`을 요구한다. `Makefile:15-53`, `Dockerfile.translate:17-28`, workflow `:52-54`는 모두 `--locked`다.

```sh
rg -n -- '--frozen|--locked' \
  prompt.md Makefile Dockerfile.translate .github/workflows/sync-translation.yml
```

```text
Dockerfile.translate:19:RUN uv sync --locked
Dockerfile.translate:28:CMD ["uv", "run", "--locked", "python", "main.py"]
prompt.md:74:- Python: `uv run --frozen --python 3.14` ...
prompt.md:652:  env PYTHONPATH=. uv run --frozen --python 3.14 \
prompt.md:684:        uv run --frozen --python 3.14 python provider_check.py \
prompt.md:729:          uv run --frozen --python 3.14 \
prompt.md:818:          uv run --frozen --python 3.14 \
Makefile:20,24,33,43,49,53: uv run --locked ...
.github/workflows/sync-translation.yml:54: run: uv sync --locked
```

#### 재현 조건

Appendix 명령을 문자 그대로 product gate와 비교한다.

#### 영향

검증 담당자마다 lock freshness 조건과 “exact 준수” 판정이 달라진다.

#### 권고

root prompt를 현재 product contract와 동기화한다.

#### 완료 조건

prompt, Makefile, workflow, Dockerfile, docs가 동일 option 의미를 사용한다.

### N-13. Docker workflow fixture 누락 — P2

#### 근거

`Dockerfile.translate:21-26`은 `.github/workflows/sync-translation.yml`을 image에 복사한다. mount 없는 최신 실제 명령이 `Ran 696 tests ... OK (skipped=1)`였고 image 안 workflow 존재도 확인했다.

#### 재현 조건

추가 mount 없이 image 전체 test를 실행한다.

#### 영향

과거 `FileNotFoundError`는 재현되지 않는다.

#### 권고

fixture COPY와 mount-free test를 유지한다.

#### 완료 조건

image 단독 전체 suite가 통과해야 한다. 최신본에서 충족했다.

### N-14. 긴 ALL-CAPS prose echo — P1

#### 근거

`response_contract.py:1490-1508`은 5단어 초과 ALL-CAPS prose를 보호 문구에서 제외한다.

```text
API ERROR HANDLING AND RETRY GUIDE
provider = [provider untranslated source text,
            provider target language mismatch]
final    = [untranslated source text]
```

관련 provider/final test 2/2가 통과했다.

#### 재현 조건

대문자 기술 단어만으로 긴 문장을 만들고 visible body를 그대로 둔다.

#### 영향

기존 silent approval은 해결됐다.

#### 권고

환경변수·identifier positive와 prose negative를 함께 유지한다.

#### 완료 조건

긴 prose는 거부하고 실제 literal만 허용한다. 최신본에서 충족했다.

### N-15. legacy table 영문 prose echo — P1

#### 근거

`response_contract.py:1310-1472`는 prose role과 target language를 검사한다. 전체 영어 `Feature | Description / Lock | Prevent writes`는 provider에서 untranslated/target mismatch, final에서 untranslated였다. `Lock | 쓰기 방지`는 양쪽 `[]`였다.

#### 재현 조건

legacy pipe table의 자연어 header/설명을 전부 영어로 둔다.

#### 영향

기존 영어 table 전체 승인 문제는 해결됐다.

#### 권고

prose/literal positive·negative test를 유지하되 N-25 과보호를 별도로 고친다.

#### 완료 조건

영문 prose echo는 거부하고 identifier를 보존한 정상 번역은 통과한다. 최신본에서 충족했다.

### N-16. raw closer 및 comment/code-span 교차 경계 처리 실패 — P1

#### 근거

canonical opener-only annotation은 최신본에서 통과하고, `annotation/annotate.py:194-200`이 생성한 escaped closer/paired form도 provider/final 모두 `[]`다. 그러나 provider prompt는 literal `-->`를 `--&gt;`로 바꾸라고 요구하지 않으며 raw contract는 postprocess 전에 실행된다. 모델이 실제로 낼 수 있는 raw closer/paired form은 다음처럼 거부된다.

```text
N-16-raw-closer:
provider = [provider malformed HTML comment, provider original comment mismatch,
            provider paragraph layout mismatch, provider inline code mismatch,
            provider annotation ownership mismatch]
final    = [malformed HTML comment, inline code mismatch,
            source comment mismatch, missing original comment]

N-16-escaped-closer:
provider = []
final    = []
```

반대 방향의 false negative도 있다. `<!-- begin \` --> <!-- unclosed \`\n`은 실제 comment 경계 밖의 dangling opener가 있는데 `has_malformed_html_comment_delimiters()`가 `False`, final verifier가 `[]`를 반환한다. `common/markdown.py:1516-1525`가 parsed comment와 **교차**하는 code span을 포함 관계처럼 취급해 뒤 opener까지 마스킹하기 때문이다.

고정 probe/log는 `.review/latest-gate-21b6a340/logs/probe-comment-delimiter-boundaries.{py,stdout.log}`이고 SHA-256은 각각 `e23355d6ca9548eb9c971222f9c2ff20b2097ec0bb1fa2672b66b80d010b12a9`, `68a7117c66df2614d5071c58f8be23be0dd185ff7bc3879ddd3b7370d80efeef`다. 독립 재실행 세 번 모두 고정 stdout과 `diff -u` exit 0이었다. `abbd78d4`의 해당 parser/contract 파일은 21b와 byte-identical하다.

#### 재현 조건

annotation inline code에 raw `-->`가 있거나, code span이 실제 HTML comment 끝과 다음 dangling opener를 가로지른다.

#### 영향

정상 literal closer 번역은 provider 표현 방식에 따라 재시도로도 차단되고, 반대로 실제 malformed comment는 final-only 경로에서 승인될 수 있다.

#### 권고

prompt/contract가 raw closer의 canonical escape를 일관되게 처리하고, comment parser는 span overlap이 아니라 실제 containment와 delimiter 소유권을 기준으로 마스킹한다.

#### 완료 조건

opener-only, closer-only, paired literal의 raw/escaped positive fixture는 provider/final을 모두 통과하고, 교차 경계의 dangling opener negative fixture는 두 gate가 모두 거부한다.

### N-17. permuted fenced insertion TARGET 오판정 — P1

#### 근거

`patch.py:824-841`은 다음 코드로 이미 적용된 상태로 분류한다.

```python
if permuted_new and pure_fenced_insertion:
    return PlanState.TARGET
```

`tests/test_patch.py:100-112` fixture의 실제 결과는 `apply_plan(...) == existing: True`, 이어지는 `verify(..., source=new) == ['code block mismatch']`다. `main.py:498-506`은 issue 뒤 write하지 않는다.

#### 재현 조건

새로 삽입할 fenced block과 동일 line multiset이지만 순서가 다른 block이 locale에 이미 있다.

#### 영향

매 sync가 같은 final failure로 끝나 3회 반복해도 완료되지 않는다.

#### 권고

TARGET 판정 시 exact canonical block을 요구하고 permutation은 실제 patch 또는 fail-closed 대상으로 둔다.

#### 완료 조건

fixture가 canonical 순서로 수정돼 final 통과하거나 patch 단계에서 명시적 오류를 낸다.

### N-18. 동적 JSX expression 변경 승인 — P1

#### 근거

선행 P1은 부분적으로 닫혔다. provider contract는 display attribute의 지원되는 최상위 `+` 문자열 literal만 번역 차이로 허용하고 identifier/operator drift를 보존 signature와 비교한다. 기존 `Widget` 및 `img` concatenation exploit은 이제 `provider HTML markup mismatch`를 반환하고, 정적 문자열과 지원된 top-level string-literal 번역 positive fixture는 통과한다.

```text
source = <Widget aria-label={"Cache " + labels.safe + " status"} />
target = <Widget aria-label={"캐시 " + process.env.SECRET + " 상태"} />
provider = [provider HTML markup mismatch]
final = []
```

final verifier는 `_dynamic_display_attribute_signatures(..., tag_name="img")`만 비교하므로 non-`img` display expression은 여전히 `[]`다. 최신 scanner는 quote·brace·template·regex literal을 인식하고 unparsed markup을 fail-closed signature로 남기도록 보강됐지만, final-only 일반 JSX attribute 범위는 문서에도 명시적으로 제외돼 있다.

#### 재현 조건

non-`img` JSX의 `alt`, `placeholder`, `aria-label`, `aria-description`에 동적 expression이 있고 final verifier만 호출한다.

#### 영향

production provider 응답 경계의 직접 silent write는 차단됐다. 다만 final-only API·replay·우회 경로는 일반 JSX 실행식 drift를 독립적으로 증명하지 못해 잔여 심각도를 P2로 낮춘 Partial이다.

#### 권고

provider와 final이 같은 dynamic-display signature를 모든 지원 tag에 적용하거나, final-only 범위가 의도된 계약이라면 호출자가 provider gate 증거 없이는 결과를 승인하지 못하게 한다.

#### 완료 조건

static literal과 지원된 최상위 문자열 연결 번역은 통과하고, `img` 및 non-`img`의 identifier/operator/regex/template 변경은 provider와 final 모두 거부한다.

### N-19. non-img display attribute gate 불일치 — P2

#### 근거

provider의 `response_contract.py:1128-1201`은 display 값을 마스킹한다. final의 `verify.py:646-674`는 달라진 structural HTML을 허용할 때 `_html_img_sources(expected)`를 요구한다.

```text
source   = <Widget aria-label={"Cache lock"} />
target   = <!-- source -->
           <Widget aria-label={"캐시 잠금"} />
provider = []
final    = [source comment mismatch]
```

#### 재현 조건

non-img HTML/JSX display attribute를 번역하고 source annotation을 둔다.

#### 영향

provider가 승인한 정상 번역을 final이 거부해 자동 sync를 차단한다.

#### 권고

display-attribute 정책과 structural ownership을 두 verifier에서 같은 공용 signature로 구현한다.

#### 완료 조건

정상 non-img display 번역은 양쪽 통과, 동적 expression 변경은 양쪽 거부한다.

### N-20. 동일-shape 표의 wrong-owner annotation — P2

#### 근거

`response_contract.py:853-886`과 `verify.py:655-674`는 table annotation과 다음 행의 종류·열 수만 비교한다. 첫 표 header annotation을 같은 2열 shape의 둘째 표 앞으로 옮긴 전체 fixture에서 provider/final 모두 `[]`였다.

#### 재현 조건

동일 shape 표 두 개를 두고 첫 표의 source header comment를 둘째 표 직전으로 이동한다.

#### 영향

원문 근거가 잘못된 표에 귀속돼도 gate가 성공한다.

#### 권고

source table ordinal, header content identity, 주변 anchor를 ownership key에 포함한다.

#### 완료 조건

같은-shape wrong-owner 이동을 provider/final이 모두 거부한다.

### N-21. blockquoted fence 뒤 quote ordinal 불일치 — P2

#### 근거

`response_contract.py:336-358`은 source text quote만 세고 `:361-371`은 target의 raw `>` run을 센다.

```text
source optional key ordinal = 0
target body-line ordinal    = 1
provider = [provider original comment mismatch,
            provider annotation ownership mismatch]
final = [source comment mismatch]
```

입력은 blockquoted fenced code 뒤의 정상 `> Quoted guidance.` 번역이다.

#### 재현 조건

blockquoted fence 다음에 optional quoted annotation을 둔다.

#### 영향

정상 provider 응답을 contract가 거부하며 final과도 판정이 어긋난다.

#### 권고

source/target 모두 fenced quote를 동일한 block scanner로 ordinal에서 제외한다.

#### 완료 조건

quoted fence 앞뒤의 정상 quote는 양쪽 통과하고 실제 relocation만 거부한다.

### N-22. Markdown literal context의 comment delimiter 오탐 — P2

#### 근거

`common/markdown.py:1401-1421,1424-1481,1502-1555`는 opening info string, indented code, front matter scalar를 comment 문맥과 구분하지 않는다. 또한 `:1465`의 inline 분기가 같은 offset의 fence 분기 `:1469`보다 먼저 실행된다.

```text
~~~text <!--        => provider/final malformed
    <!--            => provider/final malformed
description: <!--   => provider/final malformed
```

또한 fence와 inline span이 같은 offset인 fixture의 실제 출력은 다음과 같다.

```text
input    = '```text\nliteral ``` ticks\n<!-- keep -->\n```\n'
spans    = [(26, 39, ' keep ')]
stripped = '```text\nliteral ``` ticks\n\n```\n'
```

#### 재현 조건

tilde fence info, 4-space indented code, YAML scalar 또는 same-offset fence 안에 literal opener를 둔다.

#### 영향

정상 Markdown을 거부하거나 fenced literal comment를 실제 comment로 삭제할 수 있다.

#### 권고

공용 Markdown lexical mask에 front matter, indented code, fence 우선순위를 포함한다.

#### 완료 조건

각 literal context는 byte-preserved되고 진짜 malformed HTML comment만 거부된다.

### N-23. 빈 quote의 annotation 소유 승인 — P2

#### 근거

`verify.py:646-674`는 quote text가 달라도 depth만 같으면 구조가 일치한다고 본다.

```text
source   = > Quoted guidance.
target   = > <!-- Quoted guidance. -->
           >
provider = [provider block signature mismatch,
            provider markdown structure mismatch]
final    = []
```

#### 재현 조건

source quote annotation 다음 visible line을 같은 depth의 bare `>`로 둔다.

#### 영향

final-only 호출은 번역문이 사라진 quote를 승인한다.

#### 권고

quote depth뿐 아니라 visible body, source ordinal, non-empty ownership을 검사한다.

#### 완료 조건

bare quote는 final에서도 거부되고 정상 localized quote만 통과한다.

### N-24. Warning/Caution의 NOTE 하향 — P1

#### 근거

선행 fixture는 최신본에서 닫혔다. `postprocess.admonition_types()`가 legacy label을 canonical type으로 정규화하고, `response_contract.py`와 `verify.py`가 source/target type tuple을 비교한다. top-level뿐 아니라 `- >`, `1. >`, `>>`, marker 뒤 공백이 없는 form도 현재 회귀 corpus에 포함된다.

```text
source       = > **Caution:**
raw provider = > **注意:**
contract     = [provider admonition type mismatch]
postprocess  = > [!NOTE]
final        = [admonition type mismatch]
```

`Warning→注意`, `Warning→참고`와 nested Markdown container drift도 같은 방식으로 거부됐다. named tests는 `test_rejects_changed_final_admonition_type`, `test_rejects_localized_legacy_admonition_type_downgrade`, `test_rejects_changed_final_admonition_type_in_markdown_containers`, `test_rejects_changed_provider_admonition_type_in_markdown_containers`다.

#### 재현 조건

과거에는 WARNING/CAUTION source에 번역된 legacy “참고/注意” label을 반환하면 재현됐다. 최신 동일 fixture는 양 gate가 거부한다.

#### 영향

직접 type downgrade가 기록되던 P1 경로는 해소됐다. 다만 F-14 전체에는 type verifier를 우회하는 provider-free patch 결함 N-27/N-28과 indentation 결함 N-29가 별도로 남는다.

#### 권고

현재 type identity 회귀 행렬을 유지하고, 같은 canonical parser를 provider-free patch의 current/old/new 상태 검증에도 재사용한다.

#### 완료 조건

NOTE/WARNING/CAUTION의 같은 종류는 통과하고 하향·상향 drift를 provider/final이 명시적으로 거부한다. 이 finding의 exact fixture에는 충족했다. provider-free patch의 별도 완료 조건은 N-27/N-28에 둔다.

### N-25. legacy table 한 단어 과보호 — P2

#### 근거

`response_contract.py:1277-1307`은 ASCII 한 단어 cell을 무조건 protected로 분류하고 `:1409-1450,2172-2193`은 byte identity를 요구한다.

```text
Lock | 쓰기 방지 => provider=[], final=[]
잠금 | 쓰기 방지 => provider=[provider protected term mismatch], final=[]
```

#### 재현 조건

legacy table의 일반 자연어 단일 단어 cell을 완전히 번역한다.

#### 영향

자연스러운 정상 번역을 provider가 거부하고 final과 판정이 어긋난다.

#### 권고

제품명·identifier·config 값이라는 구조적 근거가 있을 때만 단일 단어를 보호한다.

#### 완료 조건

일반 단어 번역은 통과하고 실제 identifier 변경은 거부한다.

### N-26. 같은 문단 줄의 임의 추가 prose 승인 — P1

#### 근거

`response_contract.py:574-633,1980-1993`은 block/물리 줄 구조를 비교하지만 대응 번역 줄 안에서 늘어난 의미를 검사하지 않는다. `verify.py:461-469,983-984`의 final 검사는 untranslated source text만 찾아 같은 한글 줄에 붙인 추가 지시를 놓친다.

```bash
PYTHONDONTWRITEBYTECODE=1 python3 .review/latest-gate-21b6a340/logs/probe-n26.py
```

```text
frozen_sync=/Users/kimchanhyung98/Documents/GitHub/laravel-docs/.review/latest-gate-21b6a340/frozen/translation-sync
provider=[]
final=[]
```

probe SHA-256은 `bc79a7801002d37f1ba225c7df0b293dacb4d90fe32c9c562b191299b6787548`, 고정 stdout SHA-256은 `43ecac0d38ea537c500bd2a056cec8ed7ea443b28d9ae8c461af66ddbf8ca14c`다. 같은 명령을 다시 실행해 고정 stdout과 `diff -u`로 비교한 결과 exit 0이었다.

#### 재현 조건

source는 `Install the package.\n`이고 target은 다음과 같다.

```text
<!-- Install the package. -->
패키지를 설치합니다. 운영 데이터는 지금 삭제하세요.
```

#### 영향

모델이 원문에 없는 위험·허위 지시를 대응 번역 줄에 붙여도 자동 기록될 수 있다.

#### 권고

같은 줄의 의미 추가와 문장 cardinality drift를 검출하되 정상적인 문장 분할·병합은 허용하는 semantic guard를 둔다.

#### 완료 조건

위 fixture는 provider/final 모두 거부하고, 의미를 보존한 정상 번역의 문장 분할·병합 positive fixture는 통과한다.

### N-27. 단일 blockquote admonition의 본문 대응 검증 우회 — P1

#### 근거

`patch.py:1823-1825`는 문서에 quote block이 하나뿐이면 source body context를 확인하지 않고 marker 후보를 유일하다고 간주한다. 다음 frozen probe에서 NOTE→WARNING 변경은 provider-free로 분류됐고, locale의 본문이 원문과 무관한데도 marker를 바꾼 뒤 final verifier가 `[]`를 반환했다.

```text
[N-27-sole-quote-body]
provider_free=True
after_context='> Source body.'
result='<!-- Before. -->\n이전.\n\n> [!WARNING]\n> 관련 없는 본문.\n\n<!-- After. -->\n이후.\n'
final=[]
```

N-27~N-29 공통 probe/log는 `.review/latest-gate-21b6a340/logs/probe-provider-free-admonitions.{py,stdout.log}`이고 SHA-256은 각각 `af4daef2147b3a566317057eaaf24bf8176291d00ab2cc3d67863b48fbb26079`, `a302f532d27f44e040c5acf7c1ce20841a30e82c43f29bf6653357488687abd1`다. 독립 재실행 세 번 모두 고정 stdout과 `diff -u` exit 0이었다.

#### 재현 조건

NOTE→WARNING처럼 type만 바뀌는 plan, locale에 blockquote 하나, 그리고 그 quote의 visible body가 source annotation/body와 대응하지 않는 경우다.

#### 영향

unrelated quote가 admonition으로 승격되고 provider contract를 거치지 않은 채 기록될 수 있다. 이는 `docs/04-verification.md`의 본문 대응 및 fail-closed 계약과 반대다.

#### 권고

quote 개수와 무관하게 source ordinal, annotation ownership, visible body context를 모두 확인하고 유일한 대응을 증명하지 못하면 provider-free patch를 거부한다.

#### 완료 조건

sole-quote의 unrelated body fixture는 patch 단계에서 명시적으로 실패하고, 정확한 source-body 대응 fixture만 marker 변경과 final verification을 통과한다.

### N-28. legacy admonition의 제3 type을 provider-free patch가 덮어씀 — P1

#### 근거

`patch.py:1806-1812`는 legacy marker의 현재 type을 plan의 old type과 대조하지 않는다. NOTE→WARNING plan에 대해 locale의 기존 `Caution`을 제3 상태로 거부하지 않고 WARNING으로 덮어썼으며 final verifier도 이를 승인했다.

```text
[N-28-legacy-third-state]
provider_free=True
after_context='> Source body.'
result='... > [!WARNING]\n> <!-- Source body. -->\n> 번역 본문.\n ...'
final=[]
```

이 fixture는 unrelated quote를 하나 더 넣고 정확한 body annotation을 제공해 N-27의 sole-quote 우회와 분리했다. `_LEGACY_ADMONITION_RE`가 legacy type을 식별하지 않는 것이 직접 원인이다.

#### 재현 조건

source plan은 NOTE→WARNING이지만 locale의 정확한 body 위치에 TIP/CAUTION/IMPORTANT 같은 제3 legacy type이 이미 있는 경우다.

#### 영향

운영자가 의도적으로 유지한 기존 경고 강도나 충돌 상태가 provider 호출·충돌 보고 없이 다른 type으로 바뀐다.

#### 권고

legacy marker도 canonical type으로 파싱해 `current == old`일 때만 provider-free 교체하고, `current == new`는 no-op, 제3 상태는 conflict로 fail-closed 처리한다.

#### 완료 조건

NOTE/WARNING/CAUTION/TIP/IMPORTANT 전이 행렬에서 old→new만 변경되고, new 상태는 멱등이며, 모든 제3 상태는 locale bytes를 보존한 채 명시적 오류를 낸다.

### N-29. admonition marker 교체 시 list 들여쓰기 유실 — P2

#### 근거

`patch.py:1775-1776,1797-1805`의 marker replacement는 원래 줄의 leading indentation을 결과에 복원하지 않는다.

```text
[N-29-indentation-loss]
provider_free=True
result='> [!WARNING]\n  > 번역 본문.\n'
final=[]
```

원래 `  > [!NOTE]`였던 nested list quote의 marker만 top-level `> [!WARNING]`으로 승격되고 본문은 두 칸 들여쓰기를 유지해 container 구조가 갈라진다.

#### 재현 조건

list item 안에 두세 칸 들여쓴 admonition marker가 있고 provider-free type 변경을 적용한다.

#### 영향

렌더링·소유권·후속 patch 주소가 달라지지만 final verifier가 이를 잡지 못한다.

#### 권고

marker token만 교체하고 원본 line prefix와 quote/list container stack을 byte-preserve하며, final verifier도 admonition container signature를 비교한다.

#### 완료 조건

unordered/ordered/nested list와 다중 quote depth에서 marker 변경 전후 container prefix가 동일하고, 의도적 prefix drift는 provider/final 양쪽에서 거부된다.

## 7. 알려진 미해결 항목의 상태 변화

| 항목 | 최신 판정 | 근거 |
|---|---|---|
| F-09 | 그대로 | single-file publish는 `os.replace` 실패 시 cached bytes와 mode를 보존하고 temp도 제거한다. 그러나 full sync의 두 번째 publish를 실패시키면 `first.md=first-new`, `second.md=second-cached`, `stale.md=stale-cached`인 부분 상태가 남았다. 즉 stale 삭제 순서와 개별 atomic write는 개선됐지만 run-level rollback은 없다. 고정 probe/log `.review/latest-gate-21b6a340/logs/probe-f09-upstream-atomic.{py,stdout.log}`의 SHA-256은 `b62b5f182daf58e2f0304bed4f5bab0d69edd6898e4cbb7779354c9e5a4ed386`, `61938efee72baaeb477ec792f07cc22fc6a6a074d783ed1843e5ad4f09383320`이다 |
| F-11 | 검증 불가 | 실제 설정에 Azure 필수 key가 없어 OpenAI 경로와 분리 검증하지 못했다 |
| F-12 | 해결 | sync/deploy/PR-title action의 full-SHA pin 정책과 tag 계열은 일치한다. 단 setup-node SHA의 실제 ref 해석 실패는 별도 2.3 workflow blocker다 |
| F-14 | 부분 해결 | N-24의 direct/중첩-container type drift는 provider/final에서 거부된다. 그러나 provider-free marker 변경은 sole quote의 unrelated body를 승인하고(N-27), 기존 legacy 제3 type을 덮어쓰며(N-28), nested list indentation도 잃는다(N-29) |
| F-15 | 부분 해결 | 최신 full-suite gate에서 `test_detects_changed_multi_backtick_inline_code`, `test_detects_changed_multiline_inline_code`, `test_detects_changed_link_title_when_target_is_preserved`, `test_rejects_changed_markdown_link_title_before_patch`가 각각 `inline code mismatch`, `link title mismatch`, `provider link title mismatch`를 단언하며 통과했다. 다만 N-16/N-22 parser 경계가 남는다 |
| F-17 | 외부 결정 필요 | cron 정시성, ruleset, direct push 허용은 저장소 내부만으로 증명할 수 없다 |
| F-18 | 부분 해결 | canonical version loader가 순서·형식·semantic duplicate를 검사하지만 `sync/common/files.py`, `sync/common/versions.py`, `tests/test_files.py` 세 파일이 아직 untracked라 전달 위험이 남는다 |

F-08의 의미 일부 누락도 그대로다. `Install the package, then run the migration.`을 “패키지를 설치합니다.”로만 번역한 fixture는 contract/final 모두 `[]`다. 이는 문체 문제가 아니라 의미 보존 자동 검사의 범위 한계다.

## 8. live 표본 결과

### 8.1 provider contract

provider는 `OpenAI` 경로이고 reasoning effort는 `medium`이었다. key 값과 전체 environment는 기록하지 않았다.

| 모델 | KO | JA | KO prompt SHA-256 | JA prompt SHA-256 |
|---|---|---|---|---|
| `gpt-5.4-mini` | PASS | PASS | `2d853c977dd600f7311e0ca38d41b24b015202db2fc4e159dc92dc75f903179d` | `97711525a580c0d047eec284e639484312207ea15ca987a1d70de948444d39ae` |
| `gpt-5.6-luna` | PASS | PASS | 동일 | 동일 |

두 모델 모두 호환 runner에서 KO/JA fresh contract와 final verifier를 통과했다. exact A.3 통과로는 세지 않는다.

### 8.2 문서 1건 × 6회

선택 문서는 `i18n/en/docusaurus-plugin-content-docs/version-13.x/ai-sdk.md`이며 대응 출력은 `versioned_docs/version-13.x/ai-sdk.md`(KO)와 `i18n/ja/docusaurus-plugin-content-docs/version-13.x/ai-sdk.md`(JA)다.

| 모델/run | raw 명령 | 생성 경로(baseline 제외) | raw host anchor | diff | artifact | 사람 검토 | A.6 |
|---|---|---|---:|---|---|---|---|
| mini 1 | FAIL: JA inline-code | EN, KO | 46,633 | PASS | FAIL | 불완전 | 해당 없음 |
| mini 2 | PASS | EN, KO, JA | 46,640 | PASS | FAIL | JA ownership FAIL | FAIL |
| mini 3 | PASS | EN, KO, JA | 46,640 | PASS | FAIL | JA ownership FAIL | FAIL |
| Luna 1 | FAIL: KO language | EN | 46,626 | PASS | FAIL | 불완전 | 해당 없음 |
| Luna 2 | PASS | EN, KO, JA | 46,640 | PASS | FAIL | JA ownership FAIL | FAIL |
| Luna 3 | FAIL: KO language | EN | 46,626 | PASS | FAIL | 불완전 | 해당 없음 |

성공 후보 세 JA 파일 모두 기존 English NOTE comment와 대응 번역 NOTE 사이에 새 fake-with-approval block이 들어갔다.

- mini 2: source comment 2604, translated NOTE 2628
- mini 3: source comment 2605, translated NOTE 2629
- Luna 2: source comment 2604, translated NOTE 2628

동일 ownership 기준을 적용하면 사람 품질 판정은 세 건 모두 FAIL이다. 최신 동결본에서 stale comment를 제거한 수정은 현재 파일을 정상화했지만 과거 live checkout의 결과를 소급 변경하지 않는다.

raw host site 6/6은 host `node_modules` symlink/npm을 사용했으므로 정식 Docker site PASS로 승격하지 않았다. artifact 0/6은 checkout에 이미 있던 29개 non-output production path와 9개 JA alias path가 HEAD 기준 validator에 잡힌 결과다. 성공 후보의 baseline 제외 새 경로는 EN/KO/JA `ai-sdk.md`로 제한됐지만 A.5는 직접 gate 통과를 요구한다.

### 8.3 raw 성공과 A.5

| 모델 | raw 번역 명령 | 사람 판정 포함 | A.5 7조건 전체 |
|---|---:|---:|---:|
| mini | 2/3 | 0/3 | **0/3** |
| Luna | 1/3 | 0/3 | **0/3** |

A.5는 EN/KO/JA `ai-sdk.md`를 모두 `HEAD^`로 restore해야 한다. 실제 harness는 38-file patch를 적용했으며 KO/JA에는 `HEAD^`와 다른 legacy marker 정규화 세 곳이 있었다. 또한 exact credential runner와 Docker site gate를 쓰지 않았다.

### 8.4 no-op

| checkout | exit | `no source changes` | `translating:` | diff hash | 판정 |
|---|---:|---|---|---|---|
| mini 2 | 0 | 없음 | 있음 | 동일 | FAIL |
| mini 3 | 0 | 없음 | 있음 | 동일 | FAIL |
| Luna 2 | 1 | 없음 | 있음 | 동일 | FAIL |

mini 2와 mini 3의 원문 log는 각각 다음 5줄로 동일했다.

```text
translating: ko i18n/en/docusaurus-plugin-content-docs/version-13.x/ai-sdk.md
translating: ja i18n/en/docusaurus-plugin-content-docs/version-13.x/ai-sdk.md
version-13.x: 1 files
total: 1 files
translated 1 doc(s) into ko, ja
```

Luna 2의 원문 log 전체는 다음과 같다.

```text
translating: ko i18n/en/docusaurus-plugin-content-docs/version-13.x/ai-sdk.md
verify failed: ko i18n/en/docusaurus-plugin-content-docs/version-13.x/ai-sdk.md: ['partial translation failed: provider response contract failed: provider untranslated source text, provider target language mismatch']
stopping after first verification failure
version-13.x: 1 files
total: 1 files
```

`translating:`은 provider 호출 전에 출력되므로 실제 provider 재호출의 증거로 사용하지 않았다. 그러나 A.6의 no-source marker와 번역 단계 미진입 조건은 모두 위반했다. credential runner가 시작되기 전 exit 2였던 첫 no-op 시도 6회는 제품 결과에서 제외했다.

### 8.5 A.7 완료 판정

| 조건 | 결과 |
|---|---|
| mini 3/3 | 미충족: raw 2/3, A.5 0/3 |
| Luna 3/3 | 미충족: raw 1/3, A.5 0/3 |
| artifact/site/diff 6/6 | 미충족: artifact 0/6, diff 6/6, 정식 Docker site 미증명 |
| no-op 6/6 | 미충족: 유효 후보 0/3, 요구 coverage 0/6 |
| active branch commit 0 / push 0 | 충족 |
| 전체 변경이 `.review`와 보고서뿐 | 전체 worktree 기준 미충족 |
| A.5 exact fixture | 미충족 |
| A.2 exact awk | 미충족: macOS awk exit 2 |
| A.3 exact runner | 미충족 |

**부록 A.7 판정: 검증 미완료.**

## 9. 검증 한계와 절차 편차

- **identity replay의 의미**: patch/구조/멱등성 검증이며 번역 품질 검증이 아니다. 내부 임시 commit을 만들기 때문에 실제 replay는 실행하지 않았다.
- **live 검증의 범위**: 두 모델의 provider fixture와 동일한 실제 문서 1건을 모델별 3회 검사했다. 전체 Laravel 문서군의 의미 정확성이나 장기간 provider 안정성을 보장하지 않는다.
- **secret 비열람**: `dot_env`의 key 이름과 구조만 확인하고 값은 사람이 읽지 않았다. 실제 유효성은 하위 프로세스 호출 성공으로만 간접 확인했다.
- **현재 provider만 검증**: `dot_env`가 실제 선택한 provider 경로만 검증했다. Azure 필수 key가 없으므로 Azure deployment/API version 경로는 판정하지 않았다.
- **비용·성능 표본 한계**: 모델별 3회의 한 문서 실행에서 얻은 latency/retry는 운영 전체 비용이나 tail latency를 대표하지 않는다.
- 위 다섯 항목은 결함이 아니라 검증 범위의 한계다. 범위 밖 항목을 “통과”로 적지 않았다.
- A.3 exact runner가 실제 credential 형식을 거부해 호환 runner를 사용했다.
- A.5의 `HEAD^` locale fixture 대신 HEAD 기반 38-file patch를 사용했다.
- live site는 Docker가 아니라 host dependency 공유 경로였다.
- `act -l`만 통과했고 dry-run은 network/action cache 문제로 실패했다.
- upstream fetch는 project 내부 local mirror와 URL rewrite를 사용했다. public remote의 실제 network 동작과 동일하다고 간주하지 않았다.
- Docker daemon 접근에는 `/Users/kimchanhyung98/.docker/run/docker.sock` endpoint를 사용했다. 인접 파일을 탐색하지 않았지만 root prompt의 문자 그대로의 “프로젝트 내부 경로만” 규칙에는 편차다.
- a6 historical 첫 site build는 기본 Docker config가 home의 buildx activity를 쓰려 해 실패했고 project-local `DOCKER_CONFIG`로 재실행했다. 후속 fresh build도 project-local `BUILDX_CONFIG`에서 registry `ECONNRESET`이었고 exact-lock overlay만 통과했다.
- historical 첫 병렬 site build는 exit 137이었고 단독 순차 재실행은 통과했다. 최신 gate도 순차 mount-free 실행으로 제한했다.
- focused host test 두 번은 `TMPDIR` 지정이 실제 `tempfile` 실행에 전달되지 않아 `/private/tmp`을 사용했다. 이를 정식 증거에서 제외했다. 별도 감사 agent가 만든 `/private/tmp/audit-*` 세 디렉터리는 프로젝트 내부 `.review/audit-046-delta-6eba4345/tmp/system-temp-deviation/`으로 옮겼고 원 경로가 없음을 확인한 뒤 project-local temp로 재실행했다.
- 움직이는 active에서 시도한 host full suite는 중간 source 변경으로 torn read가 되었고 host의 optional `openai` dependency도 없어 폐기했다. project-local `.review/current-active-probe/tmp/` 아래 test-generated nested `.env` 하나는 root `.env`가 아니며 값에 접근하지 않았지만, 현재 sandbox의 secret-file 정책 때문에 읽거나 삭제할 수 없었다. 이를 어떤 PASS 근거에도 포함하지 않았다.
- 병행 fixer가 production을 계속 변경해 `1dee6ee0`, `03b75430`, `6eba4345`, `5e87b142`, `b487c20a`, `21b6a340`, `abbd78d4` 등 중간 frozen gate는 모두 historical로 강등했다. 각 결과를 현재 상태로 상속하지 않고 마지막 90초 불변본만 최종 표에 사용했다.
- 부록이 요구한 `.review/translation-sync-validation-*` 대신 기존 작업공간 명명과 충돌을 피하려 `translation-sync-local-validation-*`, `verify-fixes-*`를 사용했다.
- §7의 날짜 기반 exact report 이름이 이미 존재하고 기존 리뷰 수정이 금지돼 `-consolidated` suffix를 사용했다.
- root prompt의 `--frozen` 대신 product의 실제 `--locked`를 최신 Docker gate에 사용했다. N-12로도 기록했다.
- 모델을 확정할 수 없는 `fixtureA-probe.log`는 정식 6회 행렬에서 제외했다.
- 보고서 수치는 clean, live 38-file, 최신 78-file 범위를 서로 섞어 PASS로 승격하지 않았다.

## 10. 최종 판정과 다음 작업

**최종 판정은 merge 불가이며 부록 A.7 검증은 미완료다.** 실패 표본을 추가 호출로 덮거나 3/3으로 재계산하지 않았다.

다음 순서가 필요하다.

1. N-02, N-16, N-17, N-26, N-27, N-28 P1을 독립 회귀 test로 고정하고 닫는다.
2. N-04, N-05, N-09, N-18~N-23, N-25, N-29의 silent corruption/정상 번역 차단 경계를 정리한다.
3. provider/final이 동일한 Markdown scanner, annotation ownership, display-attribute signature를 사용하게 한다.
4. root prompt의 `--frozen`, credential loader, A.5 fixture, artifact baseline, A.6 no-op 정의를 product와 일치시킨다.
5. untracked `files.py`, `versions.py`, `test_files.py`를 포함한 재현 가능한 전달 스냅샷을 정한다.
6. 최신 고정본에서 deterministic Docker gate와 실제 `act --dryrun`을 먼저 통과시킨다.
7. 그 뒤 별도 라운드로 두 모델을 각각 3회 다시 수행하고, artifact/site/diff/no-op까지 6/6을 직접 증명한다.

커밋 분할이 필요하다면 `파이프라인 코드 / 기획·운영 문서 / 번역 산출물 / CI·배포 설정` 경계를 사용한다. 이 제안 자체는 finding이나 완료 조건이 아니다.

이번 검증에서는 production source를 수정하지 않았고 commit이나 push도 만들지 않았다.
