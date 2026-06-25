"""번역 동기화 구현체 패키지.

단계별 책임은 translation-sync/docs를 단일 기준으로 따른다.
"""
from __future__ import annotations

import sys

from .annotation import annotate
from .postprocessing import postprocess, repair
from .preprocessing import preprocess
from .runtime import config
from .sidebar import generator as sidebar
from .source import diff, upstream
from .translation import patch, prompt, translate
from .verification import verify

_ALIASES = {
    "annotate": annotate,
    "config": config,
    "diff": diff,
    "patch": patch,
    "postprocess": postprocess,
    "preprocess": preprocess,
    "prompt": prompt,
    "repair": repair,
    "sidebar": sidebar,
    "translate": translate,
    "upstream": upstream,
    "verify": verify,
}

for name, module in _ALIASES.items():
    if name != "sidebar":
        sys.modules[f"{__name__}.{name}"] = module

__all__ = tuple(_ALIASES)
