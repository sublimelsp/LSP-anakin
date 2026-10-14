from __future__ import annotations

from LSP.plugin import AbstractPlugin
from pathlib import Path
from typing import Any
from typing_extensions import override
import os
import re
import shutil
import sublime
import subprocess


class Anakin(AbstractPlugin):
    @classmethod
    @override
    def name(cls) -> str:
        return "anakin"

    @classmethod
    @override
    def additional_variables(cls) -> dict[str, str] | None:
        variables: dict[str, str] = {}
        variables["sublime_py_files_dir"] = os.path.dirname(sublime.__file__)
        variables["sublime_packages_dir"] = sublime.packages_path()
        variables["anakinls"] = cls.server_exe()
        return variables

    @classmethod
    def basedir(cls) -> str:
        return os.path.join(sublime.cache_path(), "LSP-anakin")

    @classmethod
    def bindir(cls) -> str:
        # Virtual environments keep their executables in "Scripts" on Windows.
        return os.path.join(cls.basedir(), "Scripts" if sublime.platform() == "windows" else "bin")

    @classmethod
    def exe(cls, name: str) -> str:
        return os.path.join(cls.bindir(), name + (".exe" if sublime.platform() == "windows" else ""))

    @classmethod
    def server_exe(cls) -> str:
        return cls.exe("anakinls")

    @classmethod
    def pip_exe(cls) -> str:
        return cls.exe("pip")

    @classmethod
    def version_str(cls) -> str:
        settings = sublime.load_settings("LSP-anakin.sublime-settings")
        return str(settings.get("version"))

    @classmethod
    def python_exe(cls) -> str:
        settings = sublime.load_settings("LSP-anakin.sublime-settings")
        python = settings.get("python")
        if isinstance(python, str) and python:
            return python
        return "python" if sublime.platform() == "windows" else "python3"

    @classmethod
    def run(cls, *args: Any, **kwargs: Any) -> bytes:
        if sublime.platform() == "windows":
            startupinfo = subprocess.STARTUPINFO()  # type: ignore
            flag = subprocess.STARTF_USESHOWWINDOW  # type: ignore
            startupinfo.dwFlags |= flag
        else:
            startupinfo = None
        # Sublime Text has no console on Windows, so give the child process its own stdin and stderr. Otherwise Python
        # fails to flush stderr on exit and exits with status 120, even after "pip install" succeeded.
        return subprocess.check_output(
            args=args,
            cwd=kwargs.get("cwd"),
            startupinfo=startupinfo,
            stdin=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
        )

    @classmethod
    @override
    def needs_update_or_installation(cls) -> bool:
        if Path(cls.server_exe()).exists():
            first_line = cls.run(cls.server_exe(), "--version").decode("ascii").splitlines()[0]
            match = re.search(r"anakinls v(.+)", first_line)
            if match:
                current_version_str = match.group(1)
                return current_version_str != cls.version_str()
        return True

    @classmethod
    @override
    def install_or_update(cls) -> None:
        shutil.rmtree(cls.basedir(), ignore_errors=True)
        try:
            Path(cls.basedir()).mkdir(exist_ok=True, parents=True)
            cls.run(cls.python_exe(), "-m", "venv", "LSP-anakin", cwd=sublime.cache_path())
            anakin = f"anakin-language-server=={cls.version_str()}"
            cls.run(cls.pip_exe(), "install", anakin)
        except Exception:
            shutil.rmtree(cls.basedir(), ignore_errors=True)
            raise
