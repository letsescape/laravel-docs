.PHONY: help dev check claude init speckit translate translation-run translation-test site-test site-check preflight

.DEFAULT_GOAL := help

TRANSLATION_API_ENV_KEYS := OPENAI_API_KEY
TRANSLATION_NETWORK_ENV_KEYS := ALL_PROXY CURL_CA_BUNDLE FTP_PROXY GIT_SSL_CAINFO GIT_SSL_CAPATH HTTPS_PROXY HTTP_PROXY NO_PROXY REQUESTS_CA_BUNDLE SSL_CERT_DIR SSL_CERT_FILE all_proxy ftp_proxy http_proxy https_proxy no_proxy
TRANSLATION_FORWARD_ENV = $(foreach key,$(1),$(if $(filter undefined,$(origin $(key))),,-e $(key)))
TRANSLATION_ENV_FILE := .env
define LOAD_TRANSLATION_ENV
if [ -f $(TRANSLATION_ENV_FILE) ]; then \
	while IFS= read -r line; do \
		case "$$line" in ''|\#*) continue ;; esac; \
		key=$${line%%=*}; \
		eval "present=\$${$$key+x}"; \
		[ -n "$$present" ] || eval "export $$line"; \
	done < $(TRANSLATION_ENV_FILE); \
fi;
endef

help: ## 사용 가능한 명령어 목록 출력
	@awk 'BEGIN {FS = ":.*##"; printf "\n사용법:\n  make \033[36m<target>\033[0m\n\n명령어:\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

dev: ## 전체 설정 (init + claude + speckit)
	@$(MAKE) init
	@$(MAKE) claude
	@$(MAKE) speckit

check: translation-test site-test ## 빠른 단위 검사 실행

translate: ## Docker에서 원문 동기화·번역 실행
	@docker compose build translate
	@set --; \
	if [ -n "$${VERSION:-}" ]; then set -- "$$@" --version "$$VERSION"; fi; \
	if [ -n "$${DOC:-}" ]; then set -- "$$@" --doc "$$DOC"; fi; \
		docker compose run --rm --no-deps \
			--user "$$(id -u):$$(id -g)" \
			-e HOME=/tmp \
			-e UV_CACHE_DIR=/tmp/translation-sync-uv-cache \
			-e UV_PROJECT_ENVIRONMENT=/tmp/translation-sync-venv \
			-e TRANSLATION_PROVIDER=openai \
			$(call TRANSLATION_FORWARD_ENV,$(TRANSLATION_API_ENV_KEYS)) \
			$(call TRANSLATION_FORWARD_ENV,$(TRANSLATION_NETWORK_ENV_KEYS)) \
			translate "$$@"

translation-run: ## 로컬에서 원문 동기화·번역 실행
	@$(LOAD_TRANSLATION_ENV) \
	cd translation-sync && \
		set --; \
		if [ -n "$${VERSION:-}" ]; then set -- "$$@" --version "$$VERSION"; fi; \
		if [ -n "$${DOC:-}" ]; then set -- "$$@" --doc "$$DOC"; fi; \
		uv run --locked --python 3.14 python main.py "$$@"

translation-test: ## translation sync 단위 테스트
	@cd translation-sync && \
		PYTHONPATH=. uv run --locked --python 3.14 \
		python -m unittest discover -s tests

site-test: ## Markdown 링크와 보안 경계 단위 테스트
	@npm run test:markdown-links
	@npm run test:security

site-check: site-test ## 배포와 같은 사이트 검증
	@npm run typecheck -- --pretty false
	@npm run build
	@npm run validate-anchors

preflight: translation-test site-check ## 번역 단위 테스트와 사이트 검증

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
