.PHONY: help dev check claude init speckit translate translation-test translation-replay translation-check translation-run translation-provider-check translation-artifact-check site-test site-check preflight

.DEFAULT_GOAL := help

help: ## 사용 가능한 명령어 목록 출력
	@awk 'BEGIN {FS = ":.*##"; printf "\n사용법:\n  make \033[36m<target>\033[0m\n\n명령어:\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

dev: ## 전체 설정 (init + claude + speckit)
	@$(MAKE) init
	@$(MAKE) claude
	@$(MAKE) speckit

check: translation-test site-test ## 빠른 단위 검사 실행

translate: ## Docker 번역 동기화 실행
	@set -- --fail-fast; \
	if [ -n "$${VERSION:-}" ]; then set -- "$$@" --version "$$VERSION"; fi; \
	if [ -n "$${DOC:-}" ]; then set -- "$$@" --doc "$$DOC"; fi; \
	docker compose run --rm --build translate \
		uv run --locked --python 3.14 python main.py "$$@"

translation-test: ## translation sync 단위 테스트
	@cd translation-sync && \
		PYTHONPATH=. uv run --locked --python 3.14 \
		python -m unittest discover -s tests

translation-replay: ## API 키 없이 격리된 translation sync 통합 검증
	@cd translation-sync && \
		set --; \
		if [ -n "$${VERSION:-}" ]; then set -- "$$@" --version "$$VERSION"; fi; \
		if [ -n "$${DOC:-}" ]; then set -- "$$@" --doc "$$DOC"; fi; \
		TRANSLATION_UPSTREAM_MANIFEST="$${MANIFEST:-}" \
		uv run --locked --python 3.14 python replay.py "$$@"

translation-check: translation-test translation-replay ## Actions와 같은 번역 preflight

translation-run: ## provider를 사용한 실제 번역 동기화
	@cd translation-sync && \
		set -- --fail-fast; \
		if [ -n "$${VERSION:-}" ]; then set -- "$$@" --version "$$VERSION"; fi; \
		if [ -n "$${DOC:-}" ]; then set -- "$$@" --doc "$$DOC"; fi; \
		TRANSLATION_UPSTREAM_MANIFEST="$${MANIFEST:-}" \
		uv run --locked --python 3.14 python main.py "$$@"

translation-provider-check: ## 문서를 수정하지 않고 live provider 응답 계약 검사
	@cd translation-sync && \
		set --; \
		if [ -n "$${LOCALE:-}" ]; then set -- "$$@" --locale "$$LOCALE"; fi; \
		uv run --locked --python 3.14 python provider_check.py "$$@"

translation-artifact-check: ## 번역 실행이 허용된 산출 경로만 변경했는지 검사
	@cd translation-sync && \
		uv run --locked --python 3.14 python validate_generated_changes.py

site-test: ## Markdown 링크 유틸리티 단위 테스트
	@npm run test:markdown-links

site-check: site-test ## 배포와 같은 사이트 검증
	@npm run typecheck -- --pretty false
	@npm run build
	@npm run validate-anchors

preflight: translation-check site-check ## 번역 및 배포 전체 로컬 검증

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
	@docker run --rm -v $$(pwd):/app -w /app node:26-alpine sh -c "apk add --no-cache git && npm install"

speckit: ## speckit 설치 (AGENT=claude, 예: make speckit AGENT=copilot)
	@if ! command -v specify >/dev/null 2>&1; then \
		echo "[speckit] specify not found"; \
		echo "[speckit] run: uv tool install specify-cli --from git+https://github.com/github/spec-kit.git"; \
		exit 1; \
	fi
	@yes | specify init --here --ai "$(or $(AGENT),claude)" --script sh
