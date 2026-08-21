"""버전별 사이드바 동기화 단계 도우미."""
from __future__ import annotations

from .generator import (
    SidebarResult,
    latest_stable_version,
    load_versions,
    locale_sidebar_paths,
    main,
    parse_documentation,
    resolve_versions,
    sync_version,
    sync_versions,
)

__all__ = (
    "SidebarResult",
    "latest_stable_version",
    "load_versions",
    "locale_sidebar_paths",
    "main",
    "parse_documentation",
    "resolve_versions",
    "sync_version",
    "sync_versions",
)
