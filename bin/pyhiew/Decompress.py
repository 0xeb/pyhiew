"""
Hiew script to decompress streams

It currently supports gzip streams

TODO
=====
- add menu and allow users to select decompression method
- make automatic stream begin/end detection
"""

import zlib
import hiew

# -----------------------------------------------------------------------
def hiew_main():
    buf = hiew.Data.GetSelData()
    if not buf:
        hiew.Message("Error", "Nothing is selected!")
        return

    # Decompress data
    try:
        ubuf = zlib.decompress(buf)
    except Exception as e:
        hiew.Window.FromString("Failed to decompress buffer!", str(e))
        return

    # Get filename
    global DECOMPRESS_FILENAME
    fn = hiew.GetFilename("Enter file name:", DECOMPRESS_FILENAME)
    if not fn:
        return

    # Write decompressed data
    try:
        f = open(fn, 'wb')
        f.write(ubuf)
        f.close()

        # Remember decompressed file name
        DECOMPRESS_FILENAME = fn

        hiew.Message("Okay", "Decompressed successfully!")
    except:
        hiew.Message("Error", "Failed to write decompressed data!")
        return

# -----------------------------------------------------------------------
try:
    DECOMPRESS_FILENAME
except:
    DECOMPRESS_FILENAME = ""

hiew_main()