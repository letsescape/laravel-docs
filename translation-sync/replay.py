#!/usr/bin/env python3
"""Run the production translation sync in an isolated local clone."""
from __future__ import annotations

import argparse
import hashlib
import os
import secrets
import shutil
import stat
import subprocess
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
MANIFEST_ENV = "TRANSLATION_UPSTREAM_MANIFEST"

EXIT_OK = 0
EXIT_SYNC_FAILED = 1
EXIT_REPLAY_ERROR = 2
EXIT_WORKTREE_CHANGED = 3

_PASSTHROUGH_ENV = {
    "PATH",
    "LANG",
    "LC_ALL",
    "SSL_CERT_FILE",
    "SSL_CERT_DIR",
    "TMPDIR",
    "TMP",
    "TEMP",
    "SYSTEMROOT",
    "UV_CACHE_DIR",
    "TRANSLATION_UPSTREAM_MANIFEST",
}


class ReplayError(RuntimeError):
    """The isolated replay could not be prepared or executed."""


def _command(
    args: list[str],
    *,
    cwd: Path,
    input_data: bytes | None = None,
) -> subprocess.CompletedProcess[bytes]:
    try:
        return subprocess.run(
            args,
            cwd=cwd,
            env=_git_environment(),
            input=input_data,
            capture_output=True,
            check=True,
        )
    except subprocess.CalledProcessError as exc:
        stderr = (exc.stderr or b"").decode("utf-8", errors="replace").strip()
        detail = f": {stderr}" if stderr else ""
        raise ReplayError(f"command failed ({' '.join(args)}){detail}") from exc


def _git_environment() -> dict[str, str]:
    env = {
        key: value
        for key, value in os.environ.items()
        if key in _PASSTHROUGH_ENV or key.startswith("LC_")
    }
    env.update(
        {
            "HOME": os.devnull,
            "XDG_CONFIG_HOME": os.devnull,
            "GIT_CONFIG_GLOBAL": os.devnull,
            "GIT_CONFIG_SYSTEM": os.devnull,
            "GIT_CONFIG_NOSYSTEM": "1",
            "GIT_TERMINAL_PROMPT": "0",
        }
    )
    return env


def _git(
    repo: Path, *args: str, input_data: bytes | None = None
) -> subprocess.CompletedProcess[bytes]:
    return _command(["git", *args], cwd=repo, input_data=input_data)


def _worktree_status(repo: Path) -> bytes:
    return _git(
        repo,
        "status",
        "--porcelain=v1",
        "-z",
        "--untracked-files=all",
    ).stdout


def _worktree_fingerprint(repo: Path) -> bytes:
    digest = hashlib.sha256()
    digest.update(b"HEAD\0")
    digest.update(_git(repo, "rev-parse", "HEAD").stdout)
    digest.update(b"TREE\0")
    digest.update(_git(repo, "rev-parse", "HEAD^{tree}").stdout)
    digest.update(_worktree_status(repo))
    digest.update(_git(repo, "diff", "--binary", "--full-index", "HEAD", "--").stdout)
    digest.update(
        _git(
            repo,
            "diff",
            "--cached",
            "--binary",
            "--full-index",
            "HEAD",
            "--",
        ).stdout
    )
    untracked = _git(
        repo, "ls-files", "--others", "--exclude-standard", "-z"
    ).stdout
    for raw_path in sorted(path for path in untracked.split(b"\0") if path):
        path = repo / Path(os.fsdecode(raw_path))
        digest.update(raw_path)
        if path.is_symlink():
            digest.update(b"L")
            digest.update(os.fsencode(os.readlink(path)))
        else:
            digest.update(b"F")
            digest.update((path.stat().st_mode & 0o7777).to_bytes(2, "big"))
            with path.open("rb") as handle:
                for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                    digest.update(chunk)
    return digest.digest()


def _copy_untracked(source: Path, sandbox: Path) -> None:
    output = _git(
        source, "ls-files", "--others", "--exclude-standard", "-z"
    ).stdout
    for raw_path in output.split(b"\0"):
        if not raw_path:
            continue
        relative = Path(os.fsdecode(raw_path))
        src = source / relative
        dest = sandbox / relative
        dest.parent.mkdir(parents=True, exist_ok=True)
        if src.is_symlink():
            raise ReplayError(f"untracked symlink is not replay-safe: {relative}")
        shutil.copy2(src, dest)


def _reject_changed_tracked_symlinks(source: Path) -> None:
    output = _git(source, "diff", "--name-only", "-z", "HEAD", "--").stdout
    for raw_path in output.split(b"\0"):
        if not raw_path:
            continue
        relative = Path(os.fsdecode(raw_path))
        if (source / relative).is_symlink():
            raise ReplayError(f"tracked symlink is not replay-safe: {relative}")


def _reject_external_tracked_symlinks(source: Path) -> None:
    root = source.resolve()
    output = _git(source, "ls-files", "-z").stdout
    for raw_path in output.split(b"\0"):
        if not raw_path:
            continue
        relative = Path(os.fsdecode(raw_path))
        link = source / relative
        if not link.is_symlink():
            continue
        target = Path(os.readlink(link))
        lexical_target = Path(os.path.abspath(link.parent / target))
        try:
            resolved_target = link.resolve(strict=False)
        except (OSError, RuntimeError) as exc:
            raise ReplayError(
                f"could not resolve tracked symlink: {relative}"
            ) from exc
        if (
            target.is_absolute()
            or not lexical_target.is_relative_to(root)
            or not resolved_target.is_relative_to(root)
        ):
            raise ReplayError(f"tracked symlink escapes repository: {relative}")


def _sandbox_parent(source: Path, requested: Path | None) -> Path:
    temp_parent = Path(tempfile.gettempdir()).resolve()
    if temp_parent == source or temp_parent.is_relative_to(source):
        raise ReplayError(
            f"temporary directory is inside active repository: {temp_parent}"
        )
    parent = requested.resolve() if requested is not None else temp_parent
    if parent == source or parent.is_relative_to(source):
        raise ReplayError(f"sandbox parent is inside active repository: {parent}")
    return parent


def _path_is_within_directory(path: Path, root: Path) -> bool:
    current = path
    while True:
        try:
            if current.samefile(root):
                return True
        except FileNotFoundError:
            pass
        parent = current.parent
        if parent == current:
            return False
        current = parent


def _manifest_destination(repo_root: Path) -> Path | None:
    value = os.environ.get(MANIFEST_ENV, "").strip()
    if not value:
        return None
    lexical_destination = Path(os.path.abspath(value))
    if lexical_destination.is_symlink():
        raise ReplayError(
            f"upstream manifest target must not be a symlink: {lexical_destination}"
        )
    if lexical_destination.exists() and not lexical_destination.is_file():
        raise ReplayError(
            f"upstream manifest target must be a regular file: {lexical_destination}"
        )
    destination = (
        lexical_destination.parent.resolve(strict=False)
        / lexical_destination.name
    )
    if (
        lexical_destination == repo_root
        or lexical_destination.is_relative_to(repo_root)
        or destination == repo_root
        or destination.is_relative_to(repo_root)
        or _path_is_within_directory(destination, repo_root)
    ):
        raise ReplayError(
            "upstream manifest destination is inside active repository: "
            f"{lexical_destination}"
        )
    return destination


def _snapshot_manifest(
    path: Path,
    *,
    repo_root: Path | None = None,
) -> bytes | None:
    flags = os.O_RDONLY
    if hasattr(os, "O_CLOEXEC"):
        flags |= os.O_CLOEXEC
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    if hasattr(os, "O_NONBLOCK"):
        flags |= os.O_NONBLOCK

    try:
        parent_descriptor, _ = _open_manifest_parent(
            path,
            create=False,
            repo_root=repo_root,
        )
    except FileNotFoundError:
        return None
    descriptor = -1
    try:
        try:
            descriptor = os.open(
                path.name,
                flags,
                dir_fd=parent_descriptor,
            )
        except FileNotFoundError:
            return None
        if not stat.S_ISREG(os.fstat(descriptor).st_mode):
            raise ReplayError(
                f"upstream manifest target must be a regular file: {path}"
            )
        with os.fdopen(descriptor, "rb", closefd=False) as input_stream:
            return input_stream.read()
    finally:
        try:
            if descriptor >= 0:
                os.close(descriptor)
        finally:
            os.close(parent_descriptor)


def _create_sandbox(source: Path, sandbox_parent: Path | None) -> Path:
    _reject_external_tracked_symlinks(source)
    if sandbox_parent is not None:
        sandbox_parent.mkdir(parents=True, exist_ok=True)
    sandbox = Path(
        tempfile.mkdtemp(prefix="translation-replay-", dir=sandbox_parent)
    )
    try:
        head = _git(source, "rev-parse", "HEAD").stdout.strip().decode("ascii")
        _command(
            [
                "git",
                "clone",
                "--local",
                "--no-hardlinks",
                "--quiet",
                "--no-checkout",
                str(source),
                str(sandbox),
            ],
            cwd=source,
        )
        _git(sandbox, "checkout", "--detach", "--quiet", head)
    except BaseException:
        shutil.rmtree(sandbox, ignore_errors=True)
        raise
    return sandbox


def _overlay_worktree(source: Path, sandbox: Path) -> None:
    _reject_external_tracked_symlinks(source)
    _reject_changed_tracked_symlinks(source)
    patch = _git(source, "diff", "--binary", "--full-index", "HEAD", "--").stdout
    if patch:
        _git(
            sandbox,
            "apply",
            "--binary",
            "--whitespace=nowarn",
            "-",
            input_data=patch,
        )
    _copy_untracked(source, sandbox)


def _commit_snapshot(sandbox: Path, message: str) -> str:
    _git(sandbox, "add", "-A")
    _git(
        sandbox,
        "-c",
        "user.name=translation-replay",
        "-c",
        "user.email=translation-replay@localhost",
        "-c",
        "commit.gpgsign=false",
        "commit",
        "--allow-empty",
        "--no-verify",
        "--quiet",
        "-m",
        message,
    )
    return _git(sandbox, "rev-parse", "HEAD").stdout.strip().decode("ascii")


def _commit_baseline(sandbox: Path) -> str:
    return _commit_snapshot(sandbox, "chore: local translation replay baseline")


def _sandbox_manifest_path(sandbox: Path) -> Path:
    return sandbox / ".git" / "translation-upstream-refs.json"


def _directory_open_flags() -> int:
    required_dir_fd_operations = (
        os.open,
        os.mkdir,
        os.stat,
        os.unlink,
        os.link,
    )
    if (
        not hasattr(os, "O_DIRECTORY")
        or not hasattr(os, "O_NOFOLLOW")
        or any(
            operation not in os.supports_dir_fd
            for operation in required_dir_fd_operations
        )
    ):
        raise ReplayError("secure upstream manifest paths are not supported")
    flags = os.O_RDONLY
    if hasattr(os, "O_CLOEXEC"):
        flags |= os.O_CLOEXEC
    flags |= os.O_DIRECTORY | os.O_NOFOLLOW
    return flags


def _directory_fd_is_within(
    descriptor: int,
    root_status: os.stat_result,
) -> bool:
    current = os.dup(descriptor)
    try:
        while True:
            current_status = os.fstat(current)
            if os.path.samestat(current_status, root_status):
                return True
            parent = os.open("..", _directory_open_flags(), dir_fd=current)
            parent_status = os.fstat(parent)
            if os.path.samestat(current_status, parent_status):
                os.close(parent)
                return False
            previous = current
            current = parent
            os.close(previous)
    finally:
        os.close(current)


def _open_manifest_parent(
    destination: Path,
    *,
    create: bool,
    repo_root: Path | None,
) -> tuple[int, Path]:
    parent_path = destination.parent.resolve(strict=False)
    parts = parent_path.parts
    if not parent_path.is_absolute() or not parts:
        raise ReplayError(
            f"upstream manifest destination must be absolute: {destination}"
        )

    root_status = repo_root.stat() if repo_root is not None else None
    descriptor = os.open(parts[0], _directory_open_flags())
    try:
        for component in parts[1:]:
            if (
                root_status is not None
                and _directory_fd_is_within(descriptor, root_status)
            ):
                raise ReplayError(
                    "upstream manifest destination is inside active repository: "
                    f"{destination}"
                )
            try:
                child = os.open(
                    component,
                    _directory_open_flags(),
                    dir_fd=descriptor,
                )
            except FileNotFoundError:
                if not create:
                    raise
                try:
                    os.mkdir(component, mode=0o777, dir_fd=descriptor)
                except FileExistsError:
                    pass
                child = os.open(
                    component,
                    _directory_open_flags(),
                    dir_fd=descriptor,
                )
            previous = descriptor
            descriptor = child
            os.close(previous)

        if (
            root_status is not None
            and _directory_fd_is_within(descriptor, root_status)
        ):
            raise ReplayError(
                "upstream manifest destination is inside active repository: "
                f"{destination}"
            )
        return descriptor, parent_path
    except BaseException:
        os.close(descriptor)
        raise


def _manifest_parent_is_stable(
    descriptor: int,
    path: Path,
    *,
    repo_root: Path | None,
) -> bool:
    if repo_root is not None and _directory_fd_is_within(
        descriptor,
        repo_root.stat(),
    ):
        return False
    try:
        path_status = path.stat()
    except OSError:
        return False
    return os.path.samestat(os.fstat(descriptor), path_status)


def _unlink_temp_manifest(
    parent_descriptor: int,
    name: str,
    expected_status: os.stat_result,
) -> None:
    try:
        current_status = os.stat(
            name,
            dir_fd=parent_descriptor,
            follow_symlinks=False,
        )
    except OSError:
        return
    if not os.path.samestat(current_status, expected_status):
        return
    try:
        os.unlink(name, dir_fd=parent_descriptor)
    except OSError:
        pass


def _export_manifest(
    source: Path | bytes,
    destination: Path,
    *,
    repo_root: Path | None = None,
) -> None:
    if isinstance(source, Path):
        contents = _snapshot_manifest(source)
        if contents is None:
            raise ReplayError(
                f"sandbox did not produce an upstream manifest: {source}"
            )
    else:
        contents = source

    destination = destination.parent.resolve(strict=False) / destination.name
    temp_name = f".translation-replay-{secrets.token_hex(16)}.tmp"
    parent_descriptor, parent_path = _open_manifest_parent(
        destination,
        create=True,
        repo_root=repo_root,
    )
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    if hasattr(os, "O_CLOEXEC"):
        flags |= os.O_CLOEXEC
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW

    temp_descriptor: int | None = None
    temp_status: os.stat_result | None = None
    try:
        temp_descriptor = os.open(
            temp_name,
            flags,
            0o600,
            dir_fd=parent_descriptor,
        )
        temp_status = os.fstat(temp_descriptor)
        remaining = memoryview(contents)
        while remaining:
            written = os.write(temp_descriptor, remaining)
            if written == 0:
                raise OSError("could not write upstream manifest")
            remaining = remaining[written:]
        os.fsync(temp_descriptor)

        if not _manifest_parent_is_stable(
            parent_descriptor,
            parent_path,
            repo_root=repo_root,
        ):
            raise ReplayError(
                f"upstream manifest parent changed during replay: {parent_path}"
            )
        try:
            os.link(
                temp_name,
                destination.name,
                src_dir_fd=parent_descriptor,
                dst_dir_fd=parent_descriptor,
                follow_symlinks=False,
            )
        except FileExistsError as exc:
            raise ReplayError(
                f"upstream manifest destination already exists: {destination}"
            ) from exc
    finally:
        try:
            if temp_status is None and temp_descriptor is not None:
                try:
                    temp_status = os.fstat(temp_descriptor)
                except OSError:
                    pass
            if temp_status is not None:
                _unlink_temp_manifest(
                    parent_descriptor,
                    temp_name,
                    temp_status,
                )
        finally:
            try:
                if temp_descriptor is not None:
                    os.close(temp_descriptor)
            finally:
                os.close(parent_descriptor)


def _replay_environment(sandbox: Path) -> dict[str, str]:
    env = {
        key: value
        for key, value in os.environ.items()
        if key in _PASSTHROUGH_ENV or key.startswith("LC_")
    }
    replay_home = sandbox / ".git" / "translation-replay-home"
    replay_home.mkdir(exist_ok=True)
    env.update(
        {
            "HOME": str(replay_home),
            "XDG_CONFIG_HOME": str(replay_home),
            "GIT_CONFIG_GLOBAL": os.devnull,
            "GIT_CONFIG_SYSTEM": os.devnull,
            "GIT_CONFIG_NOSYSTEM": "1",
            "GIT_TERMINAL_PROMPT": "0",
            "TRANSLATION_PROVIDER": "identity",
            "TRANSLATION_REPLAY": "1",
        }
    )
    env[MANIFEST_ENV] = str(_sandbox_manifest_path(sandbox))
    return env


def _execute_sync(sandbox: Path, *, version: str | None, doc: str | None) -> int:
    args = [sys.executable, "main.py"]
    if version:
        args.extend(["--version", version])
    if doc:
        args.extend(["--doc", doc])

    env = _replay_environment(sandbox)
    first = subprocess.run(
        args, cwd=sandbox / "translation-sync", env=env, check=False
    )
    if first.returncode:
        return first.returncode

    _commit_snapshot(sandbox, "chore: translation replay first pass")
    first_fingerprint = _worktree_fingerprint(sandbox)
    second = subprocess.run(
        args, cwd=sandbox / "translation-sync", env=env, check=False
    )
    if second.returncode:
        return second.returncode
    if _worktree_fingerprint(sandbox) != first_fingerprint:
        print(
            "[translation-replay] second sync changed the first sync result",
            file=sys.stderr,
        )
        return EXIT_SYNC_FAILED
    return EXIT_OK


def _display_status(status: bytes) -> str:
    lines = [
        os.fsdecode(item)
        for item in status.split(b"\0")
        if item
    ]
    return "\n".join(lines) if lines else "(clean)"


def run_replay(
    *,
    repo_root: Path = REPO_ROOT,
    version: str | None = None,
    doc: str | None = None,
    sandbox_parent: Path | None = None,
) -> int:
    repo_root = repo_root.resolve()
    sandbox: Path | None = None
    manifest_destination: Path | None = None
    manifest_input: bytes | None = None

    try:
        manifest_destination = _manifest_destination(repo_root)
        manifest_input = (
            _snapshot_manifest(
                manifest_destination,
                repo_root=repo_root,
            )
            if manifest_destination is not None
            else None
        )
        sandbox_parent = _sandbox_parent(repo_root, sandbox_parent)
        before_status = _worktree_status(repo_root)
        before_fingerprint = _worktree_fingerprint(repo_root)
    except (OSError, ReplayError) as exc:
        print(f"[translation-replay] setup failed: {exc}", file=sys.stderr)
        return EXIT_REPLAY_ERROR

    result = EXIT_REPLAY_ERROR
    try:
        sandbox = _create_sandbox(repo_root, sandbox_parent)
        print(f"[translation-replay] sandbox: {sandbox}", flush=True)
        _overlay_worktree(repo_root, sandbox)
        baseline = _commit_baseline(sandbox)
        if manifest_input is not None:
            sandbox_manifest = _sandbox_manifest_path(sandbox)
            sandbox_manifest.write_bytes(manifest_input)
            sandbox_manifest.chmod(0o400)
        print(f"[translation-replay] baseline: {baseline}", flush=True)
        print("[translation-replay] provider: identity", flush=True)

        sync_result = _execute_sync(sandbox, version=version, doc=doc)
        if sync_result == 0:
            result = EXIT_OK
        else:
            print(
                f"[translation-replay] translation sync exited {sync_result}",
                file=sys.stderr,
            )
            result = EXIT_SYNC_FAILED
    except KeyboardInterrupt:
        print("[translation-replay] interrupted", file=sys.stderr)
        result = EXIT_REPLAY_ERROR
    except (OSError, ReplayError) as exc:
        print(f"[translation-replay] replay failed: {exc}", file=sys.stderr)
        result = EXIT_REPLAY_ERROR

    try:
        after_status = _worktree_status(repo_root)
        after_fingerprint = _worktree_fingerprint(repo_root)
    except KeyboardInterrupt:
        print(
            "[translation-replay] interrupted while verifying active worktree",
            file=sys.stderr,
        )
        result = EXIT_REPLAY_ERROR
    except (OSError, ReplayError) as exc:
        print(
            f"[translation-replay] could not verify active worktree status: {exc}",
            file=sys.stderr,
        )
        result = EXIT_WORKTREE_CHANGED
    else:
        if after_fingerprint != before_fingerprint:
            print(
            "[translation-replay] active repository state changed during replay",
                file=sys.stderr,
            )
            print(
                f"[translation-replay] before:\n{_display_status(before_status)}",
                file=sys.stderr,
            )
            print(
                f"[translation-replay] after:\n{_display_status(after_status)}",
                file=sys.stderr,
            )
            result = EXIT_WORKTREE_CHANGED

    manifest_output: bytes | None = None
    if (
        result == EXIT_OK
        and sandbox is not None
        and manifest_destination is not None
        and manifest_input is None
    ):
        sandbox_manifest = _sandbox_manifest_path(sandbox)
        try:
            manifest_output = _snapshot_manifest(sandbox_manifest)
            if manifest_output is None:
                raise ReplayError(
                    "sandbox did not produce an upstream manifest: "
                    f"{sandbox_manifest}"
                )
        except (OSError, ReplayError) as exc:
            print(
                f"[translation-replay] could not stage upstream manifest: {exc}",
                file=sys.stderr,
            )
            result = EXIT_REPLAY_ERROR

    if result == EXIT_OK and sandbox is not None:
        try:
            shutil.rmtree(sandbox)
        except KeyboardInterrupt:
            print(
                f"[translation-replay] interrupted while removing sandbox {sandbox}",
                file=sys.stderr,
            )
            return EXIT_REPLAY_ERROR
        except OSError as exc:
            print(
                f"[translation-replay] could not remove sandbox {sandbox}: {exc}",
                file=sys.stderr,
            )
            return EXIT_REPLAY_ERROR
        sandbox = None

    if (
        result == EXIT_OK
        and manifest_output is not None
        and manifest_destination is not None
    ):
        try:
            _export_manifest(
                manifest_output,
                manifest_destination,
                repo_root=repo_root,
            )
        except KeyboardInterrupt:
            print(
                "[translation-replay] interrupted while exporting upstream manifest",
                file=sys.stderr,
            )
            result = EXIT_REPLAY_ERROR
        except (OSError, ReplayError) as exc:
            print(
                f"[translation-replay] could not export upstream manifest: {exc}",
                file=sys.stderr,
            )
            result = EXIT_REPLAY_ERROR

    if result == EXIT_OK:
        print("[translation-replay] completed; sandbox removed")
    elif sandbox is not None:
        print(f"[translation-replay] failed; sandbox preserved: {sandbox}", file=sys.stderr)

    return result


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Replay the production translation sync in an isolated clone."
    )
    parser.add_argument("--version", help="Optional version filter, for example 13.x")
    parser.add_argument("--doc", help="Optional Markdown document filter")
    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    return run_replay(version=args.version, doc=args.doc)


if __name__ == "__main__":
    raise SystemExit(main())
