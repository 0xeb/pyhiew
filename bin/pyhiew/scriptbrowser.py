"""
PyHiew ScriptBrowser - Default startup script

Displays scripts in the pyhiew directory and allows execution.

(c) Elias Bachaalany
"""
from __future__ import annotations

import os
from glob import glob

import hiew
from hiew import Menu, Window


class ScriptBrowser(Menu):
    """Script browser menu."""

    def __init__(self):
        super().__init__()
        self.files: list[str] = []
        self.lastsel = 0
        self.refresh_files()

    def refresh_files(self) -> bool:
        """Refreshes the file list and recreates the menu."""
        base_len = len(hiew.PYHIEW_PATH) + 1
        self.files = []

        for path in glob(os.path.join(hiew.PYHIEW_PATH, '*.py')):
            # Strip path and extension
            name = path[base_len:-3]

            # Skip hidden and excluded scripts
            if name.startswith('_') or name in hiew.PYHIEW_EXCLUDED_SCRIPTS:
                continue

            self.files.append(name)

        if not self.files:
            return False

        return self.Create(
            title=f" Script browser {_instance_count or ''} ",
            lines=self.files,
            width=30,
            main_keys={1: "-Help", 4: "-Edit", 8: "-Delete"},
            alt_keys={5: "Refresh"}
        )

    def run(self) -> None:
        """Shows the browser and handles user interaction."""
        while True:
            if not self.files:
                hiew.Message("Info", "No script files found!")
                return

            n, k = self.Show(self.lastsel)

            if n == -1:
                return

            self.lastsel = n

            # Alt+F5: Refresh
            if k == hiew.HEM_FNKEY_ALTF5:
                self.refresh_files()
                continue

            # Execute selected script
            script_path = hiew.PyHiew_GetScriptFileName(self.files[n])
            err = hiew.PyHiew_ExecuteScript(script_path, globals(), True)

            if err is not None:
                Window.FromString(" Script error ", err)

            return


# Module-level state
_browser: ScriptBrowser | None = None
_instance_count = 0


def ScriptBrowserMain() -> None:
    """Entry point for the script browser."""
    global _browser, _instance_count

    debug = False
    hiew.PYHIEW_RELOAD_STARTUP_SCRIPT = debug

    if _browser is None or debug:
        _browser = ScriptBrowser()
        _instance_count = 0
    else:
        _instance_count += 1

    _browser.run()
