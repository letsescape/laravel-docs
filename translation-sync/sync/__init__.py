"""번역 동기화 구현체 패키지.

원문, 전처리, 번역, 후처리, 검증 및 사이드바 관련 책임을 하위 패키지로 분리.
기존 최상위 import 경로는 모듈 별칭으로 유지.
``sync.sidebar``는 하위 모듈을 포함한 패키지이므로 별칭으로 덮어쓰지 않음.
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
