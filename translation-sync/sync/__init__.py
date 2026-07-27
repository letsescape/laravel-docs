"""번역 동기화 구현체 패키지.

단계별 책임은 translation-sync/docs를 단일 기준으로 따른다. 기존 flat
import 경로는 모듈 alias로 유지하지만 ``sync.sidebar``는 하위 모듈을
가진 패키지이므로 alias로 덮지 않는다.
"""
from __future__ import annotations

import sys

from .annotation import annotate
from .postprocessing import postprocess, repair
from .preprocessing import preprocess
from .runtime import config
from . import sidebar
from .source import diff, upstream
from .translation import patch, prompt, translate
from .verification import response_contract, verify

_ALIASES = {
    "annotate": annotate,
    "config": config,
    "diff": diff,
    "patch": patch,
    "postprocess": postprocess,
    "preprocess": preprocess,
    "prompt": prompt,
    "repair": repair,
    "response_contract": response_contract,
    "sidebar": sidebar,
    "translate": translate,
    "upstream": upstream,
    "verify": verify,
}

for name, module in _ALIASES.items():
    if name != "sidebar":
        sys.modules[f"{__name__}.{name}"] = module

__all__ = tuple(_ALIASES)
