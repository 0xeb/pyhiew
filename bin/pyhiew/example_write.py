"""Example: File writing (use with caution!)."""
import hiew

if hiew.AskYesNo("Write 'TEST' at offset 0?\n\nThis will modify the file!"):
    rc = hiew.FileOpenForWrite()
    if rc == hiew.HEM_OK:
        hiew.FileWrite(0, b'TEST')
        hiew.ReturnReload()
        hiew.Message("Done", "Wrote 4 bytes at offset 0")
    else:
        hiew.Message("Error", f"Could not open for write: rc={rc}")
