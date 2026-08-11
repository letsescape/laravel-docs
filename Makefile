.PHONY: help dev check claude init speckit translate translation-prepare translation-publish translation-deploy translation-run translation-test translation-replay-diagnostic translation-provider-diagnostic translation-path-diagnostic translation-diagnostic site-test site-check preflight

.DEFAULT_GOAL := help

TRANSLATION_PUSH_ENV_KEYS := GH_TOKEN GITHUB_TOKEN GH_ENTERPRISE_TOKEN GITHUB_ENTERPRISE_TOKEN GH_HOST GH_REPO GIT_ASKPASS GIT_ASKPASS_REQUIRE SSH_ASKPASS SSH_ASKPASS_REQUIRE SSH_AUTH_SOCK GIT_SSH GIT_SSH_COMMAND GIT_TERMINAL_PROMPT GIT_CONFIG_GLOBAL GIT_CONFIG_SYSTEM GIT_CONFIG_NOSYSTEM GIT_CONFIG_COUNT TRANSLATION_SYNC_PUSH_TOKEN TRANSLATION_SYNC_PUSH_USERNAME
TRANSLATION_PROVIDER_ENV_KEYS := TRANSLATION_PROVIDER TRANSLATION_MODEL TRANSLATION_MODEL_PROFILE TRANSLATION_REASONING_EFFORT TRANSLATION_CONTEXT_WINDOW_TOKENS TRANSLATION_RESERVED_OUTPUT_TOKENS TRANSLATION_REQUEST_TIMEOUT_SECONDS TRANSLATION_RUN_TIMEOUT_SECONDS TRANSLATION_WORKFLOW_TIMEOUT_SECONDS TRANSLATION_TOKENIZER_ENCODING TRANSLATION_CLI_COMMAND TRANSLATION_CLI_TIMEOUT OPENAI_API_KEY AZURE_OPENAI_API_KEY AZURE_OPENAI_API_VERSION AZURE_OPENAI_ENDPOINT CODEX_ACCESS_TOKEN CODEX_API_KEY CODEX_HOME
TRANSLATION_NETWORK_ENV_KEYS := ALL_PROXY CURL_CA_BUNDLE FTP_PROXY GIT_SSL_CAINFO GIT_SSL_CAPATH HTTPS_PROXY HTTP_PROXY NO_PROXY REQUESTS_CA_BUNDLE SSL_CERT_DIR SSL_CERT_FILE all_proxy ftp_proxy http_proxy https_proxy no_proxy
TRANSLATION_FORWARD_ENV = $(foreach key,$(1),$(if $(filter undefined,$(origin $(key))),,-e $(key)))

help: ## 사용 가능한 명령어 목록 출력
	@awk 'BEGIN {FS = ":.*##"; printf "\n사용법:\n  make \033[36m<target>\033[0m\n\n명령어:\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

dev: ## 전체 설정 (init + claude + speckit)
	@$(MAKE) init
	@$(MAKE) claude
	@$(MAKE) speckit

check: translation-test site-test ## 빠른 단위 검사 실행

translate: ## Docker에서 격리 prepare/publish/deploy 전체 실행
	@test -n "$${DOCKER_ARTIFACT_ROOT:-}" || { echo 'DOCKER_ARTIFACT_ROOT is required (use a unique path below /artifacts).' >&2; exit 1; }
	@test -n "$${PUSH_ENDPOINT:-}" || { echo 'PUSH_ENDPOINT is required.' >&2; exit 1; }
	@test -n "$${BRANCH:-}" || { echo 'BRANCH is required.' >&2; exit 1; }
	@test -n "$${REPOSITORY:-}" || { echo 'REPOSITORY is required (owner/name).' >&2; exit 1; }
	@case "$$DOCKER_ARTIFACT_ROOT" in /artifacts/?*) ;; *) echo 'DOCKER_ARTIFACT_ROOT must be below /artifacts.' >&2; exit 1;; esac
	@docker compose build translate
	@docker compose run --rm --no-deps \
		$(foreach key,$(TRANSLATION_PUSH_ENV_KEYS),-e $(key)=) \
		$(foreach key,$(TRANSLATION_PROVIDER_ENV_KEYS),-e $(key)=) \
		--entrypoint mkdir translate \
		-m 0700 -- "$$DOCKER_ARTIFACT_ROOT"
	@set -- prepare \
		--artifact-root "$$DOCKER_ARTIFACT_ROOT" \
		--push-endpoint "$$PUSH_ENDPOINT" \
		--branch "$$BRANCH" \
		--repository "$$REPOSITORY"; \
	if [ -n "$${VERSION:-}" ]; then set -- "$$@" --version "$$VERSION"; fi; \
	if [ -n "$${DOC:-}" ]; then set -- "$$@" --doc "$$DOC"; fi; \
		docker compose run --rm --no-deps \
			$(foreach key,$(TRANSLATION_PUSH_ENV_KEYS),-e $(key)=) \
			$(call TRANSLATION_FORWARD_ENV,$(TRANSLATION_PROVIDER_ENV_KEYS)) \
			$(call TRANSLATION_FORWARD_ENV,$(TRANSLATION_NETWORK_ENV_KEYS)) \
			translate "$$@"
	@docker compose run --rm --no-deps \
		$(foreach key,$(TRANSLATION_PROVIDER_ENV_KEYS),-e $(key)=) \
		$(call TRANSLATION_FORWARD_ENV,$(TRANSLATION_PUSH_ENV_KEYS)) \
		$(call TRANSLATION_FORWARD_ENV,$(TRANSLATION_NETWORK_ENV_KEYS)) \
		translate publish --artifact-root "$$DOCKER_ARTIFACT_ROOT"
	@if [ "$$BRANCH" = 'main' ]; then \
		docker compose run --rm --no-deps \
			$(foreach key,$(TRANSLATION_PROVIDER_ENV_KEYS),-e $(key)=) \
			$(call TRANSLATION_FORWARD_ENV,$(TRANSLATION_PUSH_ENV_KEYS)) \
			$(call TRANSLATION_FORWARD_ENV,$(TRANSLATION_NETWORK_ENV_KEYS)) \
			translate deploy --artifact-root "$$DOCKER_ARTIFACT_ROOT"; \
	else \
		echo "Branch '$$BRANCH' is not main; deployment skipped."; \
	fi

translation-prepare: ## 외부 artifact root에 replay·fixture·candidate·publication evidence 준비
	@test -n "$${ARTIFACT_ROOT:-}" || { echo 'ARTIFACT_ROOT is required.' >&2; exit 1; }
	@test -d "$$ARTIFACT_ROOT" || { echo 'ARTIFACT_ROOT must be an existing directory.' >&2; exit 1; }
	@test -n "$${PUSH_ENDPOINT:-}" || { echo 'PUSH_ENDPOINT is required.' >&2; exit 1; }
	@test -n "$${BRANCH:-}" || { echo 'BRANCH is required.' >&2; exit 1; }
	@test -n "$${REPOSITORY:-}" || { echo 'REPOSITORY is required (owner/name).' >&2; exit 1; }
	@cd translation-sync && \
		set -- prepare \
			--artifact-root "$$ARTIFACT_ROOT" \
			--push-endpoint "$$PUSH_ENDPOINT" \
			--branch "$$BRANCH" \
			--repository "$$REPOSITORY"; \
		if [ -n "$${VERSION:-}" ]; then set -- "$$@" --version "$$VERSION"; fi; \
		if [ -n "$${DOC:-}" ]; then set -- "$$@" --doc "$$DOC"; fi; \
		env $(foreach key,$(TRANSLATION_PUSH_ENV_KEYS),-u $(key)) \
			uv run --locked --python 3.14 python workflow.py "$$@"

translation-publish: ## 봉인된 evidence를 검증하고 원격 branch를 CAS 갱신
	@test -n "$${ARTIFACT_ROOT:-}" || { echo 'ARTIFACT_ROOT is required.' >&2; exit 1; }
	@cd translation-sync && \
		env $(foreach key,$(TRANSLATION_PROVIDER_ENV_KEYS),-u $(key)) \
			uv run --locked --python 3.14 python workflow.py publish \
			--artifact-root "$$ARTIFACT_ROOT"

translation-deploy: ## main publication의 정확한 commit을 배포하고 결과 대기
	@test -n "$${ARTIFACT_ROOT:-}" || { echo 'ARTIFACT_ROOT is required.' >&2; exit 1; }
	@cd translation-sync && \
		env $(foreach key,$(TRANSLATION_PROVIDER_ENV_KEYS),-u $(key)) \
			uv run --locked --python 3.14 python workflow.py deploy \
			--artifact-root "$$ARTIFACT_ROOT"

translation-run: ## 동일 artifact root로 prepare→publish→main deploy 순차 실행
	@$(MAKE) translation-prepare
	@$(MAKE) translation-publish
	@if [ "$${BRANCH:-}" = 'main' ]; then \
		$(MAKE) translation-deploy; \
	else \
		echo "Branch '$${BRANCH:-}' is not main; deployment skipped."; \
	fi

translation-test: ## translation sync 단위 테스트
	@cd translation-sync && \
		PYTHONPATH=. uv run --locked --python 3.14 \
		python -m unittest discover -s tests

translation-replay-diagnostic: ## 진단 전용: API 키 없이 identity replay 실행
	@cd translation-sync && \
		set --; \
		if [ -n "$${VERSION:-}" ]; then set -- "$$@" --version "$$VERSION"; fi; \
		if [ -n "$${DOC:-}" ]; then set -- "$$@" --doc "$$DOC"; fi; \
		TRANSLATION_UPSTREAM_MANIFEST="$${MANIFEST:-}" \
		uv run --locked --python 3.14 python replay.py "$$@"

translation-provider-diagnostic: ## 진단 전용: 문서를 수정하지 않고 live fixture 검사
	@cd translation-sync && \
		diagnostic_root=$$(mktemp -d) && \
		trap 'status=$$?; if [ "$$status" -eq 0 ]; then rmdir -- "$$diagnostic_root"; else echo "Provider fixture failure report directory: $$diagnostic_root" >&2; fi; exit "$$status"' EXIT && \
		deadlines=$$(uv run --locked --python 3.14 python -c 'import os, time; now = time.monotonic(); print(now + 7200, now + int(os.environ["TRANSLATION_RUN_TIMEOUT_SECONDS"]))') && \
		set -- $$deadlines && \
		workflow_deadline=$$1 && \
		run_deadline=$$2 && \
		set -- && \
		if [ -n "$${LOCALE:-}" ]; then set -- "$$@" --locale "$$LOCALE"; fi; \
		TRANSLATION_RUN_ID="diagnostic-$$(date +%s)-$$$$" \
		TRANSLATION_FAILURE_REPORT="$$diagnostic_root/translation-sync-fixture-failure.json" \
		TRANSLATION_WORKFLOW_DEADLINE_MONOTONIC="$$workflow_deadline" \
		TRANSLATION_RUN_DEADLINE_MONOTONIC="$$run_deadline" \
		uv run --locked --python 3.14 python provider_check.py "$$@"

translation-path-diagnostic: ## 진단 전용: 현재 checkout의 산출 경로 검사
	@cd translation-sync && \
		uv run --locked --python 3.14 python validate_generated_changes.py

translation-diagnostic: translation-test translation-replay-diagnostic ## 단위 테스트와 격리 replay 진단

site-test: ## Markdown 링크 유틸리티 단위 테스트
	@npm run test:markdown-links

site-check: site-test ## 배포와 같은 사이트 검증
	@npm run typecheck -- --pretty false
	@npm run build
	@npm run validate-anchors

preflight: translation-diagnostic site-check ## live provider·publication 제외 로컬 진단

claude: ## Claude Code 환경 설정
	@echo "[claude] downloading AGENTS.md..."
	@tmp_claude=$$(mktemp); \
	claude_url="https://raw.githubusercontent.com/forrestchang/andrej-karpathy-skills/main/CLAUDE.md"; \
	if ! curl -fsSL "$$claude_url" -o "$$tmp_claude"; then \
		rm -f "$$tmp_claude"; \
		echo "[claude] AGENTS.md download failed"; \
		exit 1; \
	fi; \
	if [ -f AGENTS.md ] && grep -qF "Behavioral guidelines to reduce common LLM coding mistakes" AGENTS.md; then \
		echo "[claude] AGENTS.md already up to date"; \
	elif [ -f AGENTS.md ]; then \
		printf '\n' >> AGENTS.md; \
		cat "$$tmp_claude" >> AGENTS.md; \
	else \
		mv "$$tmp_claude" AGENTS.md; \
	fi; \
	rm -f "$$tmp_claude"

init: ## 프로젝트 환경 설정
	@if [ ! -f .env ]; then \
		echo "[init] .env not found"; \
		exit 1; \
	fi
	@if ! command -v docker >/dev/null 2>&1; then \
		echo "[init] docker not found"; \
		exit 1; \
	fi
	@if ! docker compose version >/dev/null 2>&1; then \
		echo "[init] docker compose not found"; \
		exit 1; \
	fi
	@if ! docker info >/dev/null 2>&1; then \
		echo "[init] docker is not running"; \
		exit 1; \
	fi
	@if [ -f docker-compose.yml ]; then \
		echo "[init] starting docker containers..."; \
		docker compose up -d; \
	fi
	@echo "[init] installing npm packages..."
	@docker run --rm -v $$(pwd):/app -w /app node:24-alpine sh -c "apk add --no-cache git && npm install"

speckit: ## speckit 설치 (AGENT=claude, 예: make speckit AGENT=copilot)
	@if ! command -v specify >/dev/null 2>&1; then \
		echo "[speckit] specify not found"; \
		echo "[speckit] run: uv tool install specify-cli --from git+https://github.com/github/spec-kit.git"; \
		exit 1; \
	fi
	@yes | specify init --here --ai "$(or $(AGENT),claude)" --script sh
