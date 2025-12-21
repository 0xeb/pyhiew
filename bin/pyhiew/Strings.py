"""
Strings - Display strings in a file using SysInternals strings.exe.

Requires strings.exe from SysInternals in PATH.
https://docs.microsoft.com/en-us/sysinternals/downloads/strings
"""
from __future__ import annotations

import os

import hiew


class StringsViewer:
    """Displays and navigates strings found in the current file."""

    def __init__(self):
        self.cache: list[tuple[int, str]] | None = None
        self.menu = hiew.Menu()
        self.last_filename: str | None = None
        self.selection = 0
        self.search_text: str | None = None

    @property
    def filename(self) -> str | None:
        return hiew.Data.GetFileName()

    @staticmethod
    def extract_strings(filename: str) -> list[tuple[int, str]] | None:
        """Runs strings.exe and parses output."""
        try:
            with os.popen(f'strings.exe -nobanner -o "{filename}"') as f:
                lines = f.readlines()

            result = []
            for line in lines:
                line = line.strip()
                if ':' in line:
                    offset_str, text = line.split(':', 1)
                    result.append((int(offset_str), text))

            return result if result else None
        except Exception:
            return None

    def refresh(self) -> bool:
        """Refreshes the string list from the current file."""
        self.selection = 0
        self.cache = self.extract_strings(self.filename)

        if not self.cache:
            self.menu.Create(
                title="Strings",
                lines=["No strings found", "Press F5 to refresh"],
                width=70,
                main_keys={5: "Reload"}
            )
            return False

        # Truncate long strings for display
        lines = [text[:60] for _, text in self.cache]

        self.menu.Create(
            title=f"Strings: {os.path.basename(self.filename)}",
            lines=lines,
            width=70,
            main_keys={5: "Reload", 7: "Find"},
            shift_keys={7: "Next"}
        )
        return True

    def search(self) -> int:
        """Prompts for search text and finds first match."""
        self.search_text = hiew.GetString("Search for:", 50)
        return self.search_next(start_offset=0)

    def search_next(self, start_offset: int = 1) -> int:
        """Finds next match starting from current selection + offset."""
        if not self.search_text or not self.cache:
            return self.selection

        for i in range(self.selection + start_offset, len(self.cache)):
            if self.search_text.lower() in self.cache[i][1].lower():
                return i

        return self.selection  # No match found

    def run(self) -> None:
        """Main interaction loop."""
        # Refresh if file changed
        if self.last_filename != self.filename:
            if not self.refresh():
                hiew.Message("Error", "strings.exe not found or no strings in file")
                return
            self.last_filename = self.filename

        while True:
            n, key = self.menu.Show(self.selection)

            if n == -1:  # ESC
                break

            if key == hiew.HEM_FNKEY_F5:
                self.refresh()
                continue

            if not self.cache:
                continue

            if key == hiew.HEM_FNKEY_F7:
                self.selection = self.search()
            elif key == hiew.HEM_FNKEY_SHIFTF7:
                self.selection = self.search_next()
            else:
                self.selection = n
                hiew.ReturnOffset(self.cache[self.selection][0])
                break


# Module-level instance
_viewer: StringsViewer | None = None


def StringsMain() -> None:
    global _viewer
    if _viewer is None:
        _viewer = StringsViewer()
    _viewer.run()


StringsMain()
