#!/usr/bin/env python3
"""per-file 병기/검증 CLI (docs/05 T2).

사용:
  python annotate_cli.py <version> <name>           # 진단(드리프트·검증 차이 출력, 미기록)
  python annotate_cli.py <version> <name> --write    # 정렬·검증 통과 시에만 병기본 기록

annotate는 내부에서 raw EN을 preprocess+postprocess한 정규본(verify의 expected와 동일)으로
맞춰 정렬한다. 따라서 KO 본문을 현재 EN에 일치시키면 통과한다.
"""
from __future__ import annotations
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from sync import annotate, preprocess, postprocess, verify

REPO = Path(__file__).resolve().parents[1]


def main() -> int:
    if len(sys.argv) < 3:
        print("usage: annotate_cli.py <version> <name> [--write]", file=sys.stderr)
        return 2
    version, name = sys.argv[1], sys.argv[2]
    write = "--write" in sys.argv

    enp = REPO / f"i18n/en/docusaurus-plugin-content-docs/version-{version}/{name}"
    kop = REPO / f"versioned_docs/version-{version}/{name}"
    en = enp.read_text(encoding="utf-8")
    ko = kop.read_text(encoding="utf-8")

    out, drifts = annotate.annotate(en, ko, version)
    pre = preprocess.preprocess(en)
    expected = postprocess.postprocess(pre.text, version, pre.placeholders)
    issues = verify.verify(out, source=expected)

    clean = (not drifts) and (not issues)
    if clean and write:
        kop.write_text(out, encoding="utf-8")
        print(f"OK written: {version}/{name}")
        return 0

    print(f"{'CLEAN' if clean else 'NEEDS-FIX'}: {version}/{name}  drift={len(drifts)} issues={issues}")

    for d in drifts:
        if d.op == "delete":
            print("  [EN-only / KO 누락 → 번역 추가 필요]")
            for l in d.en_lines:
                if l.strip():
                    print(f"    EN+ {l}")
        elif d.op == "insert":
            print("  [KO-only / EN 없음 → front matter면 유지, 아니면 제거]")
            for l in d.ko_lines[:4]:
                print(f"    KO  {l}")
        else:
            print("  [replace / 종류 어긋남]")
            for l in d.en_lines[:3]:
                print(f"    EN~ {l}")
            for l in d.ko_lines[:3]:
                print(f"    KO~ {l}")

    if issues:
        ic_en, ic_ko = verify._inline_codes(expected), verify._inline_codes(out)
        if (ic_en - ic_ko) or (ic_ko - ic_en):
            print(f"  inline code only_EN={dict(ic_en - ic_ko)}  only_KO={dict(ic_ko - ic_en)}")
        lt_en, lt_ko = verify._link_targets(expected), verify._link_targets(out)
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
