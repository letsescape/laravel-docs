#!/usr/bin/env python3
"""단일 번역 문서의 영어 원문 주석 진단·기록 CLI.

사용법:
  python annotate_cli.py <version> <name>           # 진단(드리프트·검증 차이 출력, 미기록)
  python annotate_cli.py <version> <name> --write    # 정렬·검증 통과 시에만 병기본 기록

영어 원문에 전처리와 후처리를 적용해 정규화한 뒤 한국어 본문과 정렬.
정규화한 원문은 검증 기댓값과 동일하며, 한국어 본문과 현재 영어 원문의 일치 여부가 통과 조건.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from sync import annotate, preprocess, postprocess, verify
from sync.common.files import atomic_write_text

REPO = Path(__file__).resolve().parents[1]
_VERSION_RE = re.compile(r"^(?:master|(?:0|[1-9]\d*)\.x)$")
_DOCUMENT_RE = re.compile(r"^[^/\\]+\.md$")


def _expected_locale_roots(repo: Path) -> frozenset[Path]:
    """진단과 기록을 허용할 영어·한국어·일본어 문서 루트 반환."""

    return frozenset(
        (
            repo / "versioned_docs",
            repo / "i18n/en/docusaurus-plugin-content-docs",
            repo / "i18n/ja/docusaurus-plugin-content-docs",
        )
    )


def _has_symlink_component(path: Path, boundary: Path) -> bool:
    """경계부터 대상까지 심볼릭 링크인 경로 구성 요소가 있는지 판별."""

    current = boundary
    if current.is_symlink():
        return True
    for component in path.relative_to(boundary).parts:
        current /= component
        if current.is_symlink():
            return True
    return False


def _document_path(root: Path, version: str, name: str) -> Path:
    """허용된 로케일 루트 안에서 심볼릭 링크를 거치지 않는 문서 경로 검증."""

    lexical_repo = REPO.absolute()
    lexical_root = root.absolute()
    if lexical_root not in _expected_locale_roots(lexical_repo):
        raise ValueError(f"unexpected locale root: {lexical_root}")
    if _has_symlink_component(lexical_root, lexical_repo):
        raise ValueError(f"invalid locale root: {lexical_root}")

    repo_root = lexical_repo.resolve()
    locale_root = lexical_root.resolve()
    version_root = lexical_root / f"version-{version}"
    lexical_candidate = version_root / name
    candidate = lexical_candidate.resolve()
    if not locale_root.is_relative_to(repo_root) or not candidate.is_relative_to(
        locale_root
    ):
        raise ValueError(f"document path escapes locale root: {candidate}")
    if version_root.is_symlink() or lexical_candidate.is_symlink():
        raise ValueError(f"invalid document path: {lexical_candidate}")
    return candidate


def main() -> int:
    """명령줄 진입점 실행."""

    if len(sys.argv) < 3:
        print("usage: annotate_cli.py <version> <name> [--write]", file=sys.stderr)
        return 2
    version, name = sys.argv[1], sys.argv[2]
    if not _VERSION_RE.fullmatch(version):
        print(f"invalid version: {version}", file=sys.stderr)
        return 2
    if Path(name).name != name or not _DOCUMENT_RE.fullmatch(name):
        print(f"invalid document: {name}", file=sys.stderr)
        return 2
    write = "--write" in sys.argv

    try:
        enp = _document_path(
            REPO / "i18n/en/docusaurus-plugin-content-docs",
            version,
            name,
        )
        kop = _document_path(REPO / "versioned_docs", version, name)
    except ValueError as exc:
        print(exc, file=sys.stderr)
        return 2
    en = enp.read_text(encoding="utf-8")
    ko = kop.read_text(encoding="utf-8")

    out, drifts = annotate.annotate(en, ko, version)
    pre = preprocess.preprocess(en)
    expected = postprocess.postprocess(pre.text, version, pre.placeholders)
    issues = verify.verify(out, source=expected, version=version)

    clean = (not drifts) and (not issues)
    if clean and write:
        atomic_write_text(kop, out)
        print(f"OK written: {version}/{name}")
        return 0

    print(f"{'CLEAN' if clean else 'NEEDS-FIX'}: {version}/{name}  drift={len(drifts)} issues={issues}")

    for drift in drifts:
        if drift.op == "delete":
            print("  [EN-only / KO 누락 → 번역 추가 필요]")
            for line in drift.en_lines:
                if line.strip():
                    print(f"    EN+ {line}")
        elif drift.op == "insert":
            print("  [KO-only / EN 없음 → front matter면 유지, 아니면 제거]")
            for line in drift.ko_lines[:4]:
                print(f"    KO  {line}")
        else:
            print("  [replace / 종류 어긋남]")
            for line in drift.en_lines[:3]:
                print(f"    EN~ {line}")
            for line in drift.ko_lines[:3]:
                print(f"    KO~ {line}")

    if issues:
        ic_en, ic_ko = verify._inline_codes(expected), verify._inline_codes(out)
        if (ic_en - ic_ko) or (ic_ko - ic_en):
            print(f"  inline code only_EN={dict(ic_en - ic_ko)}  only_KO={dict(ic_ko - ic_en)}")
        lt_en = verify._link_targets(expected, version=version)
        lt_ko = verify._link_targets(out, version=version)
        if (lt_en - lt_ko) or (lt_ko - lt_en):
            print(f"  link only_EN={dict(lt_en - lt_ko)}  only_KO={dict(lt_ko - lt_en)}")
        cb_en, cb_ko = verify._fenced_code_blocks(expected), verify._fenced_code_blocks(out)
        if cb_en != cb_ko:
            se, sk = set(cb_en), set(cb_ko)
            for b in list(se - sk)[:3]:
                print(f"  codeblock only_EN: {b[:160]!r}")
            for b in list(sk - se)[:3]:
                print(f"  codeblock only_KO: {b[:160]!r}")
        if "missing original comment" in issues:
            req, got = verify._required_comments(expected), verify._translated_comments(out)
            for c in [c for c in req if c not in got][:8]:
                print(f"  missing comment: {c[:160]}")
    return 0 if clean else 1


if __name__ == "__main__":
    raise SystemExit(main())
