import json
import os
import re
import shlex
import shutil
import socket
import subprocess
import time
from pathlib import Path

from dotenv import load_dotenv
import openai
from openai.types.chat import ChatCompletionSystemMessageParam, ChatCompletionUserMessageParam

import structure_validator


REPO_ROOT = Path(__file__).resolve().parents[2]
UPDATER_ROOT = Path(__file__).resolve().parent
UPSTREAM_REPO = "https://github.com/laravel/docs.git"
BRANCHES = ["master", "13.x", "12.x", "11.x", "10.x", "9.x", "8.x"]
EXCLUDED_FILES = {"license.md", "readme.md", "documentation.md"}
MAX_CHUNK_LINES = 400
CLI_TRANSLATION_PROVIDERS = {"cli", "ai-cli", "local"}
REUSABLE_TRANSLATION_BRANCHES = ["13.x", "12.x", "11.x", "10.x", "9.x", "8.x", "master"]

_cached_client = None
_cached_model = None
_cached_prompt = None


class AnchorValidationError(Exception):
    """번역본의 anchor 정의/참조가 원본과 다를 때."""


class TransientCliError(RuntimeError):
    """일시적 CLI 오류. 재시도 가능."""


class FatalCliError(RuntimeError):
    """영속적 CLI 오류. 재시도 무의미."""


# 일시적 오류 — 자동 재시도 대상 (네트워크·서비스 오류).
TRANSIENT_EXCEPTIONS = (
    openai.RateLimitError,
    openai.APITimeoutError,
    openai.APIConnectionError,
    openai.InternalServerError,
    socket.timeout,
    TimeoutError,
    TransientCliError,
)

# 번역 검증 실패 — 자동 재시도 대상 (LLM 출력의 변형).
VALIDATION_EXCEPTIONS = (
    AnchorValidationError,
)

# 영속적 오류 — 재시도 무의미. 즉시 raise.
FATAL_EXCEPTIONS = (
    openai.AuthenticationError,
    openai.PermissionDeniedError,
    openai.BadRequestError,
    ValueError,
    FatalCliError,
)


def _read_int_env(name, default, minimum=0):
    """환경변수에서 양의 정수를 읽되, 잘못된 값이면 기본값 사용."""
    raw = os.environ.get(name)
    if raw is None:
        return default
    try:
        value = int(raw)
        if value < minimum:
            raise ValueError
        return value
    except ValueError:
        print(f"{name} 값이 유효하지 않아 기본값 {default}을 사용합니다.")
        return default


def _retry_delays(attempts, base=5):
    """5s, 15s, 45s, ... 3배수 지수 백오프 — attempts 회만큼."""
    return [base * (3 ** i) for i in range(attempts)]


def run_command(args, cwd=None):
    result = subprocess.run(
        args,
        cwd=cwd,
        check=True,
        text=True,
        capture_output=True,
    )
    return result.stdout.strip()


def clone_docs(temp_dir, repo_url=UPSTREAM_REPO):
    temp_path = Path(temp_dir)
    if temp_path.exists():
        shutil.rmtree(temp_path)

    try:
        run_command(
            [
                "git",
                "clone",
                "--depth",
                "1",
                "--no-single-branch",
                repo_url,
                str(temp_path),
            ]
        )
        return True
    except subprocess.CalledProcessError as error:
        print(f"원문 가져오기 실패: {error}")
        return False


def checkout_branch(repo_dir, branch):
    run_command(
        ["git", "checkout", "--force", "-B", branch, f"origin/{branch}"],
        cwd=repo_dir,
    )


def docs_dir_for(repo_root, branch):
    return Path(repo_root) / "versioned_docs" / f"version-{branch}"


def source_dir_for(updater_root, branch):
    return Path(updater_root) / "source" / f"version-{branch}"


def sync_branch_docs(upstream_dir, source_dir, docs_dir, excluded_files):
    upstream_path = Path(upstream_dir)
    source_path = Path(source_dir)
    docs_path = Path(docs_dir)
    version = source_path.name.removeprefix("version-")
    source_path.mkdir(parents=True, exist_ok=True)
    docs_path.mkdir(parents=True, exist_ok=True)

    markdown_files = sorted(path.name for path in upstream_path.glob("*.md"))
    current_files = set(markdown_files)

    for existing in source_path.glob("*.md"):
        if existing.name not in current_files:
            existing.unlink()
            translated = docs_path / existing.name
            if translated.exists():
                translated.unlink()
            print(f"  삭제: {existing.name}")

    excluded = {name.lower() for name in excluded_files}
    for filename in markdown_files:
        source = upstream_path / filename
        shutil.copy2(source, source_path / filename)
        if filename.lower() in excluded:
            content = source.read_text(encoding="utf-8")
            rendered = replace_version_placeholder(content, version)
            (docs_path / filename).write_text(rendered, encoding="utf-8")


def latest_stable_version(versions):
    return next((version for version in versions if version != "master"), versions[0])


def parse_documentation_md(content, version, latest_stable=None):
    sidebar = {"tutorialSidebar": []}
    current_category = None

    for line in content.splitlines():
        category = re.match(r"^- ## (.+)$", line)
        if category:
            current_category = {
                "type": "category",
                "label": category.group(1),
                "collapsed": True,
                "items": [],
            }
            sidebar["tutorialSidebar"].append(current_category)
            continue

        item = re.match(
            r"^\s+- \[[^\]]+\]\(/docs/\{\{\s*version\s*\}\}/([^)]+)\)$",
            line,
        )
        if item and current_category:
            item_path = item.group(1).split("#", 1)[0]
            current_category["items"].append(item_path)
            continue

        api_link = re.match(r"^- \[API Documentation\]\((.+)\)$", line)
        if api_link:
            api_version = latest_stable if version == "master" and latest_stable else version
            href = replace_version_placeholder(api_link.group(1), api_version)
            sidebar["tutorialSidebar"].append(
                {"type": "link", "label": "API Documentation", "href": href}
            )

    if (
        len(sidebar["tutorialSidebar"]) > 1
        and sidebar["tutorialSidebar"][1].get("type") == "category"
    ):
        sidebar["tutorialSidebar"][1]["collapsed"] = False

    return sidebar


def generate_sidebar(
    repo_root,
    version,
    updater_root=UPDATER_ROOT,
    latest_stable=None,
):
    repo_path = Path(repo_root)
    source = source_dir_for(updater_root, version) / "documentation.md"
    target = repo_path / "versioned_sidebars" / f"version-{version}-sidebars.json"

    if not source.exists():
        print(f"  documentation.md 없음: {version}")
        return False

    target.parent.mkdir(parents=True, exist_ok=True)
    sidebar = parse_documentation_md(
        source.read_text(encoding="utf-8"),
        version,
        latest_stable=latest_stable,
    )
    target.write_text(json.dumps(sidebar, indent=2) + "\n", encoding="utf-8")
    print(f"  사이드바 생성: {version}")
    return True


def generate_sidebars(repo_root, branches=BRANCHES, updater_root=UPDATER_ROOT):
    ok = True
    latest_stable = latest_stable_version(branches)
    for branch in branches:
        ok = (
            generate_sidebar(
                repo_root,
                branch,
                updater_root=updater_root,
                latest_stable=latest_stable,
            )
            and ok
        )
    return ok


def extract_changed_source_files(status_output):
    changed = set()
    for line in status_output.splitlines():
        if not line.strip() or len(line) < 4:
            continue

        path = line[3:].strip()
        if " -> " in path:
            path = path.rsplit(" -> ", 1)[1]

        normalized = path.replace("\\", "/")
        if re.match(
            r"^\.github/docs-updater/source/version-[^/]+/[^/]+\.md$",
            normalized,
        ):
            changed.add(normalized)

    return sorted(changed)


def get_changed_source_files(repo_root):
    status = run_command(
        ["git", "status", "--porcelain", "--untracked-files=all"],
        cwd=repo_root,
    )
    return extract_changed_source_files(status)


def get_translation_source_files(repo_root, branches=BRANCHES, updater_root=None):
    repo_path = Path(repo_root)
    updater_path = Path(updater_root) if updater_root is not None else UPDATER_ROOT
    required = set(get_changed_source_files(repo_path))

    for branch in branches:
        source_dir = source_dir_for(updater_path, branch)
        docs_dir = docs_dir_for(repo_path, branch)
        if not source_dir.exists():
            continue

        for source in source_dir.glob("*.md"):
            if source.name.lower() in EXCLUDED_FILES:
                continue
            if not (docs_dir / source.name).exists():
                required.add(source.relative_to(repo_path).as_posix())

    return sorted(required)


def replace_version_placeholder(content, version):
    return re.sub(r"\{\{\s*version\s*\}\}", version, content)


def normalize_known_anchor_references(content):
    if (
        "#agents-integration" in content
        and '<a name="agent-integration"></a>' in content
        and '<a name="agents-integration"></a>' not in content
    ):
        content = content.replace("#agents-integration", "#agent-integration")
    return content


def prepare_translation_content(content, version):
    return normalize_known_anchor_references(
        replace_version_placeholder(content, version)
    )


def ensure_docs_front_matter(content, filename):
    if filename != "installation.md" or content.startswith("---\n"):
        return content

    return f"---\nslug: /\n---\n\n{content}"


def normalize_anchor_spacing(content):
    return re.sub(r"(?<!\n)\n(<a\s+name=[\"'][^\"']+[\"']\s*/?>)", r"\n\n\1", content)


def finalize_translation_content(content, filename):
    content = normalize_anchor_spacing(content)
    return ensure_docs_front_matter(content, filename)


def _is_fence_line(line):
    stripped = line.lstrip()
    return stripped.startswith("```") or stripped.startswith("~~~")


def split_markdown_chunks(content, max_lines=MAX_CHUNK_LINES):
    lines = content.splitlines(keepends=True)
    if len(lines) <= max_lines:
        return [content] if content else []

    chunks = []
    current = []
    in_fence = False
    overflow_limit = max_lines + max(10, max_lines // 5)

    for line in lines:
        current.append(line)

        if _is_fence_line(line):
            in_fence = not in_fence

        if in_fence:
            continue

        if len(current) >= max_lines and not line.strip():
            chunks.append("".join(current))
            current = []
        elif len(current) >= overflow_limit:
            chunks.append("".join(current))
            current = []

    if current:
        chunks.append("".join(current))

    return chunks


def _strip_code(text):
    stripped_lines = []
    in_fence = False
    fence_marker = None

    for line in text.splitlines(keepends=True):
        stripped = line.lstrip()
        marker = stripped[:3]
        if marker in {"```", "~~~"}:
            if not in_fence:
                in_fence = True
                fence_marker = marker
            elif marker == fence_marker:
                in_fence = False
                fence_marker = None
            continue

        if in_fence:
            continue

        stripped_lines.append(_strip_inline_code(line))

    return "".join(stripped_lines)


def _strip_inline_code(line):
    output = []
    index = 0
    while index < len(line):
        if line[index] == "`":
            end = line.find("`", index + 1)
            newline = line.find("\n", index + 1)
            if end >= 0 and (newline < 0 or end < newline):
                index = end + 1
                continue

        output.append(line[index])
        index += 1

    return "".join(output)


def extract_anchor_definitions(markdown):
    return set(
        re.findall(r"<a\s+name=[\"']([^\"']+)[\"']\s*/?>", _strip_code(markdown))
    )


def extract_anchor_references(markdown):
    return set(
        ref.strip()
        for ref in re.findall(r"\[[^\]]*\]\(#([^\s)]+)", _strip_code(markdown))
        if ref.strip()
    )


def validate_anchors(source, translated):
    source_anchors = extract_anchor_definitions(source)
    translated_anchors = extract_anchor_definitions(translated)
    translated_refs = extract_anchor_references(translated)
    errors = []

    missing = source_anchors - translated_anchors
    if missing:
        errors.append(f"번역본에서 누락된 앵커: {sorted(missing)}")

    extra = translated_anchors - source_anchors
    if extra:
        errors.append(f"번역본에 추가된 앵커: {sorted(extra)}")

    broken = translated_refs - translated_anchors
    if broken:
        errors.append(f"정의되지 않은 앵커 참조: {sorted(broken)}")

    return not errors, errors


def get_translation_client():
    global _cached_client, _cached_model
    if _cached_client is not None:
        return _cached_client, _cached_model

    provider = os.environ.get("TRANSLATION_PROVIDER", "openai").lower()
    model = os.environ.get("TRANSLATION_MODEL", "gpt-5")
    request_timeout = _read_int_env("TRANSLATION_REQUEST_TIMEOUT", 120, minimum=10)
    sdk_max_retries = _read_int_env("TRANSLATION_SDK_RETRIES", 0, minimum=0)
    common_kwargs = {"timeout": request_timeout, "max_retries": sdk_max_retries}

    if provider == "openai":
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY 미설정")
        _cached_client = openai.OpenAI(api_key=api_key, **common_kwargs)
    elif provider == "azure":
        api_key = os.environ.get("AZURE_OPENAI_API_KEY")
        endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")
        api_version = os.environ.get("AZURE_OPENAI_API_VERSION", "2025-05-01-preview")
        if not api_key or not endpoint:
            raise ValueError("AZURE_OPENAI_API_KEY 또는 AZURE_OPENAI_ENDPOINT 미설정")
        _cached_client = openai.AzureOpenAI(
            api_key=api_key,
            azure_endpoint=endpoint,
            api_version=api_version,
            **common_kwargs,
        )
    else:
        raise ValueError(f"미지원 번역 제공자: {provider}")

    _cached_model = model
    return _cached_client, _cached_model


def read_cli_timeout():
    try:
        return int(os.environ.get("TRANSLATION_CLI_TIMEOUT", "1800"))
    except ValueError as error:
        raise ValueError("TRANSLATION_CLI_TIMEOUT 값이 유효하지 않습니다.") from error


def build_cli_prompt(text, system_prompt):
    return (
        "아래 시스템 지침을 엄격히 따르고, 번역된 Markdown 본문만 출력하세요.\n\n"
        "[시스템 지침]\n"
        f"{system_prompt.rstrip()}\n\n"
        "[번역할 원문]\n"
        f"{text}"
    )


_CLI_TRANSIENT_KEYWORDS = (
    "rate limit",
    "timeout",
    "timed out",
    "connection",
    "502",
    "503",
    "504",
)


def translate_text_with_cli(text, system_prompt):
    command = os.environ.get("TRANSLATION_CLI_COMMAND")
    if not command:
        raise FatalCliError("TRANSLATION_CLI_COMMAND 미설정")

    args = shlex.split(command)
    if not args:
        raise FatalCliError("TRANSLATION_CLI_COMMAND 미설정")

    try:
        result = subprocess.run(
            args,
            input=build_cli_prompt(text, system_prompt),
            text=True,
            capture_output=True,
            check=True,
            timeout=read_cli_timeout(),
        )
    except subprocess.TimeoutExpired as error:
        raise TransientCliError("번역 CLI 실행 시간이 초과되었습니다.") from error
    except subprocess.CalledProcessError as error:
        stderr = (error.stderr or "").strip()
        lowered = stderr.lower()
        if any(keyword in lowered for keyword in _CLI_TRANSIENT_KEYWORDS):
            raise TransientCliError(f"번역 CLI 일시 오류: {stderr}") from error
        message = f"번역 CLI 실행 실패: {stderr}" if stderr else "번역 CLI 실행 실패"
        raise FatalCliError(message) from error

    if not result.stdout.strip():
        raise TransientCliError("CLI returned empty content")
    return result.stdout


def get_system_prompt():
    global _cached_prompt
    if _cached_prompt is None:
        _cached_prompt = (UPDATER_ROOT / "prompt.md").read_text(encoding="utf-8")
    return _cached_prompt


def translate_text(text, system_prompt):
    provider = os.environ.get("TRANSLATION_PROVIDER", "openai").lower()
    if provider in CLI_TRANSLATION_PROVIDERS:
        return translate_text_with_cli(text, system_prompt)

    client, model = get_translation_client()
    response = client.chat.completions.create(
        model=model,
        messages=[
            ChatCompletionSystemMessageParam(role="system", content=system_prompt),
            ChatCompletionUserMessageParam(role="user", content=text),
        ],
    )

    if not response.choices:
        raise ValueError("API returned empty choices")

    content = response.choices[0].message.content
    if content is None:
        raise ValueError("API returned empty content")
    return content


def translate_markdown_content(content, system_prompt, max_lines=MAX_CHUNK_LINES):
    chunks = split_markdown_chunks(content, max_lines=max_lines)
    if len(chunks) > 1:
        print(f"  청크 번역: {len(chunks)}개")

    translated = []
    for index, chunk in enumerate(chunks, start=1):
        if len(chunks) > 1:
            print(f"  청크 {index}/{len(chunks)}")
        translated.append(_translate_chunk_with_retry(chunk, system_prompt, index))

    return "".join(translated)


def _translate_chunk_with_retry(chunk, system_prompt, chunk_index, max_attempts=None):
    """청크 단위 재시도. transient/검증 실패는 재시도, fatal 은 즉시 raise."""
    if max_attempts is None:
        max_attempts = _read_int_env("TRANSLATION_CHUNK_MAX_ATTEMPTS", 2, minimum=1)
    delays = _retry_delays(max_attempts - 1)
    last_error = None

    for attempt in range(1, max_attempts + 1):
        try:
            return translate_text(chunk, system_prompt)
        except FATAL_EXCEPTIONS:
            raise
        except (TRANSIENT_EXCEPTIONS + VALIDATION_EXCEPTIONS) as error:
            last_error = error
            if attempt < max_attempts:
                wait = delays[attempt - 1]
                print(
                    f"    청크 {chunk_index} 일시 오류({type(error).__name__}). "
                    f"{wait}초 대기 후 재시도 {attempt + 1}/{max_attempts}"
                )
                time.sleep(wait)

    raise last_error


def extract_version_from_path(path):
    normalized = str(path).replace("\\", "/")
    match = re.search(r"\.github/docs-updater/source/version-([^/]+)/", normalized)
    return match.group(1) if match else None


def translate_file(source_file, target_file, max_lines=MAX_CHUNK_LINES):
    source_path = Path(source_file)
    target_path = Path(target_file)
    content = source_path.read_text(encoding="utf-8")

    if not content.strip():
        print(f"빈 파일: {source_path}")
        return False

    version = extract_version_from_path(source_path)
    if version is None:
        raise ValueError(f"버전을 확인할 수 없음: {source_path}")

    print(f"번역 시작: {source_path}")
    prepared = prepare_translation_content(content, version)
    translated = translate_markdown_content(
        prepared,
        get_system_prompt(),
        max_lines=max_lines,
    )

    is_valid, errors = validate_anchors(prepared, translated)
    if not is_valid:
        message = f"앵커 검증 실패: {source_path}"
        for error in errors:
            message += f"\n  - {error}"
        raise AnchorValidationError(message)

    translated = finalize_translation_content(translated, source_path.name)
    target_path.parent.mkdir(parents=True, exist_ok=True)
    target_path.write_text(translated, encoding="utf-8")
    print(f"번역 완료: {source_path} -> {target_path}")
    return True


def reusable_translation_branches(target_branch):
    return [
        branch
        for branch in REUSABLE_TRANSLATION_BRANCHES
        if branch != target_branch
    ]


def has_literal_version_reference(content, version):
    without_placeholders = re.sub(r"\{\{\s*version\s*\}\}", "", content)
    return version in without_placeholders


def try_reuse_translation(
    source_file,
    target_file,
    branch,
    repo_root,
    updater_root=None,
):
    source_path = Path(source_file)
    target_path = Path(target_file)
    updater_path = Path(updater_root) if updater_root is not None else UPDATER_ROOT
    source = source_path.read_text(encoding="utf-8")

    for candidate in reusable_translation_branches(branch):
        candidate_source = source_dir_for(updater_path, candidate) / source_path.name
        candidate_target = docs_dir_for(repo_root, candidate) / source_path.name

        if not candidate_source.exists() or not candidate_target.exists():
            continue
        if candidate_source.read_text(encoding="utf-8") != source:
            continue
        if has_literal_version_reference(source, candidate):
            continue

        translated = candidate_target.read_text(encoding="utf-8")
        reused = translated.replace(candidate, branch)
        is_valid, _errors = validate_anchors(
            prepare_translation_content(source, branch),
            reused,
        )
        if not is_valid:
            continue

        reused = finalize_translation_content(reused, source_path.name)
        target_path.parent.mkdir(parents=True, exist_ok=True)
        target_path.write_text(reused, encoding="utf-8")
        print(f"  번역 재사용: {branch}/{source_path.name} <- {candidate}/{source_path.name}")
        return True

    return False


def parse_source_file_path(path):
    normalized = str(path).replace("\\", "/")
    match = re.match(
        r"^\.github/docs-updater/source/version-([^/]+)/([^/]+\.md)$",
        normalized,
    )
    if not match:
        return None, None
    return match.group(1), match.group(2)


def stage_outputs(repo_root):
    try:
        run_command(
            [
                "git",
                "add",
                ".github/docs-updater/source/",
                "versioned_docs/",
                "versioned_sidebars/",
            ],
            cwd=repo_root,
        )
        return True
    except subprocess.CalledProcessError as error:
        print(f"변경 사항 정리 실패: {error}")
        return False


def read_translation_delay():
    """파일 사이 sleep (초). 기본값 0 — 재시도/백오프가 있어 방어적 sleep 불필요."""
    return _read_int_env("TRANSLATION_DELAY", 0, minimum=0)


def translate_with_retry(source_path, target_path, branch, repo_root, max_attempts=None):
    """파일 단위 재시도. transient/검증 실패는 재시도, fatal 은 즉시 raise."""
    if max_attempts is None:
        max_attempts = _read_int_env("TRANSLATION_MAX_ATTEMPTS", 3, minimum=1)
    delays = _retry_delays(max_attempts - 1)
    last_error = None

    for attempt in range(1, max_attempts + 1):
        try:
            if try_reuse_translation(source_path, target_path, branch, repo_root):
                return True
            translate_file(source_path, target_path)
            return True
        except FATAL_EXCEPTIONS:
            raise
        except (TRANSIENT_EXCEPTIONS + VALIDATION_EXCEPTIONS) as error:
            last_error = error
            if attempt < max_attempts:
                wait = delays[attempt - 1]
                print(
                    f"  일시 오류({type(error).__name__}). "
                    f"{wait}초 대기 후 재시도 {attempt + 1}/{max_attempts}"
                )
                time.sleep(wait)

    raise last_error


def main():
    load_dotenv(UPDATER_ROOT / ".env")
    repo_root = REPO_ROOT
    temp_dir = repo_root / "temp"
    has_errors = False

    print("[1] 원문 가져오기")
    if not clone_docs(temp_dir):
        return 1

    print("[2] 버전별 동기화")
    try:
        for branch in BRANCHES:
            try:
                checkout_branch(temp_dir, branch)
                sync_branch_docs(
                    temp_dir,
                    source_dir_for(UPDATER_ROOT, branch),
                    docs_dir_for(repo_root, branch),
                    EXCLUDED_FILES,
                )
                print(f"  동기화 완료: {branch}")
            except Exception as error:
                has_errors = True
                print(f"  동기화 실패: {branch} - {type(error).__name__}: {error}")
    finally:
        if temp_dir.exists():
            shutil.rmtree(temp_dir)

    print("[3] 사이드바 생성")
    if not generate_sidebars(repo_root):
        has_errors = True

    print("[4] 변경 문서 번역")
    failed_files = []
    processed = set()
    changed_files = get_translation_source_files(repo_root)
    delay = read_translation_delay()

    if not changed_files:
        print("  번역할 변경 문서 없음")

    for relative_path in changed_files:
        branch, filename = parse_source_file_path(relative_path)
        if not branch or not filename:
            continue

        file_key = f"{branch}/{filename}"
        if file_key in processed:
            continue
        processed.add(file_key)

        if filename.lower() in EXCLUDED_FILES:
            print(f"  번역 제외: {file_key}")
            continue

        source_path = repo_root / relative_path
        if not source_path.exists():
            continue

        target_path = docs_dir_for(repo_root, branch) / filename
        try:
            translate_with_retry(source_path, target_path, branch, repo_root)
        except FATAL_EXCEPTIONS:
            # 영속적 오류 — 재시도 무의미. workflow 자체를 중단한다.
            raise
        except Exception as error:
            failed_files.append(file_key)
            print(f"  번역 실패: {file_key} - {type(error).__name__}: {error}")

        if delay:
            time.sleep(delay)

    if failed_files:
        has_errors = True
        print(f"[경고] 번역 실패 문서 {len(failed_files)}개")
        for file_key in failed_files:
            print(f"  - {file_key}")

    print("[5] 번역 구조 검증")
    structure_report = structure_validator.validate_structure(
        UPDATER_ROOT / "source",
        repo_root / "versioned_docs",
    )
    print(structure_validator.render_report(structure_report))
    if structure_report.has_issues:
        has_errors = True

    print("[6] 변경 사항 정리")
    if not stage_outputs(repo_root):
        has_errors = True

    print("갱신 완료")
    return 1 if has_errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
