"""
ClipText - Copy selected bytes to clipboard in various formats.

Usage:
    Select bytes in Hiew, then run this script.

Requires:
    pip install pyperclip

Formats:
    - Plain text
    - C array
    - Pascal array
    - Python string

(c) Elias Bachaalany
"""
from __future__ import annotations

import hiew

try:
    import pyperclip
except ImportError:
    hiew.Message("Error", "pyperclip module not installed! Run: pip install pyperclip")
    raise


# Configuration
ITEMS_PER_LINE = 16


def buf_to_c_array(buf: bytes) -> str:
    """Converts bytes to C array declaration."""
    lines = []
    for i, byte in enumerate(buf):
        if i % ITEMS_PER_LINE == 0:
            if i > 0:
                lines.append('\n\t')
        lines.append(f'0x{byte:02x}, ')

    content = ''.join(lines).rstrip()[:-1]  # Remove trailing comma
    return f'static unsigned char data[{len(buf)}] = \n{{\n\t{content}\n}};'


def buf_to_pascal_array(buf: bytes) -> str:
    """Converts bytes to Pascal array declaration."""
    lines = []
    for i, byte in enumerate(buf):
        if i % ITEMS_PER_LINE == 0:
            if i > 0:
                lines.append('\n\t')
        lines.append(f'${byte:02x}, ')

    content = ''.join(lines).rstrip()[:-1]  # Remove trailing comma
    return f'const data: array[0..{len(buf) - 1}] of Byte = \n(\n\t{content}\n);'


def buf_to_python_string(buf: bytes) -> str:
    """Converts bytes to Python hex string."""
    return ''.join(f'\\x{byte:02x}' for byte in buf)


def copy_to_clipboard(text: str) -> bool:
    """Copies text to clipboard."""
    try:
        pyperclip.copy(text)
        return True
    except Exception:
        return False


def main() -> None:
    """Main entry point."""
    buf = hiew.Data.GetSelData()
    if not buf:
        hiew.Message("Error", "Nothing is selected!")
        return

    menu = hiew.Menu()
    menu.Create(
        title="Copy to Clipboard",
        lines=[
            "Plain text",
            "C array",
            "Pascal array",
            "Python string",
            "Cancel"
        ],
        width=30
    )

    global _last_choice
    n, _ = menu.Show(_last_choice)

    if n == -1 or n == 4:  # ESC or Cancel
        return

    _last_choice = n

    formats = [
        ("plain text", lambda b: b.decode('latin-1', errors='replace')),
        ("C array", buf_to_c_array),
        ("Pascal array", buf_to_pascal_array),
        ("Python string", buf_to_python_string),
    ]

    name, converter = formats[n]
    if copy_to_clipboard(converter(buf)):
        hiew.Message("Info", f"Copied to clipboard as {name}!")


# Module state
_last_choice = 0

main()
