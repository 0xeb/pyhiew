"""Example: Find functionality."""
import hiew

# Find first occurrence of 0xCC 0xCC (int 3 breakpoints)
offset = hiew.Find(flags=0, offset=0, data=b"\xCC\xCC")

if offset is None:
    hiew.Message("Info", "Pattern not found")
else:
    hiew.Message("Found", f"First match at 0x{offset:X}")

    # Find next occurrence
    next_offset = hiew.FindNext()
    if next_offset is not None:
        hiew.Message("Found", f"Next match at 0x{next_offset:X}")

        # Search backward from there
        back_offset = hiew.Find(
            flags=hiew.HEM_FIND_BACKWARD,
            offset=next_offset,
            data=b"\xCC\xCC"
        )
        if back_offset is not None:
            hiew.Message("Found", f"Previous match at 0x{back_offset:X}")
