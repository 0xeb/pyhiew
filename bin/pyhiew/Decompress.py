"""
Decompress - Decompress selected bytes using zlib.

Select compressed data in Hiew, run this script, and save to a file.
"""
from __future__ import annotations

import zlib

import hiew

# Remember last used filename
_last_filename = ""


def main() -> None:
    global _last_filename

    # Get selected data
    buf = hiew.Data.GetSelData()
    if not buf:
        hiew.Message("Error", "Nothing is selected!")
        return

    # Try to decompress
    try:
        decompressed = zlib.decompress(buf)
    except zlib.error as e:
        hiew.Window.FromString("Decompression Failed", str(e), width=60)
        return

    # Get output filename
    filename = hiew.GetFilename("Save decompressed data to:", _last_filename)
    if not filename:
        return

    # Write to file
    try:
        with open(filename, 'wb') as f:
            f.write(decompressed)
        _last_filename = filename
        hiew.Message("Success", f"Wrote {len(decompressed)} bytes to file")
    except IOError as e:
        hiew.Message("Error", f"Failed to write: {e}")


main()
