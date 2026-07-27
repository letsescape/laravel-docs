"""Safe file publication helpers."""
from __future__ import annotations

import os
import stat
import tempfile
from pathlib import Path


def _fsync_parent(path: Path) -> None:
    descriptor = os.open(
        path.parent,
        os.O_RDONLY | getattr(os, "O_DIRECTORY", 0),
    )
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def unlink_file(path: Path, *, missing_ok: bool = False) -> bool:
    try:
        path.unlink()
    except FileNotFoundError:
        if missing_ok:
            return False
        raise
    _fsync_parent(path)
    return True


def atomic_write_text(
    path: Path,
    text: str,
    *,
    encoding: str = "utf-8",
) -> None:
    """Publish text without opening the destination inode for writing."""
    try:
        current_status = path.lstat()
    except FileNotFoundError:
        current_mode = 0o644
    else:
        current_mode = (
            stat.S_IMODE(current_status.st_mode)
            if stat.S_ISREG(current_status.st_mode)
            else 0o644
        )

    temporary: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding=encoding,
            dir=path.parent,
            prefix=f".{path.name}.",
            suffix=".tmp",
            delete=False,
        ) as stream:
            temporary = Path(stream.name)
            os.fchmod(stream.fileno(), current_mode)
            stream.write(text)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
        _fsync_parent(path)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def atomic_write_bytes(path: Path, content: bytes) -> None:
    """Publish bytes without opening the destination inode for writing."""
    try:
        current_status = path.lstat()
    except FileNotFoundError:
        current_mode = 0o644
    else:
        current_mode = (
            stat.S_IMODE(current_status.st_mode)
            if stat.S_ISREG(current_status.st_mode)
            else 0o644
        )

    temporary: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="wb",
            dir=path.parent,
            prefix=f".{path.name}.",
            suffix=".tmp",
            delete=False,
        ) as stream:
            temporary = Path(stream.name)
            os.fchmod(stream.fileno(), current_mode)
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
        _fsync_parent(path)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)
