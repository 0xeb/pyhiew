"""Example: File reading."""
import hiew

# Read first 16 bytes
rc, data = hiew.FileRead(0, 16)

if rc > 0 and data:
    hex_str = ' '.join(f'{b:02X}' for b in data)
    hiew.Message("First 16 bytes", hex_str)
else:
    hiew.Message("Error", f"Read failed: rc={rc}")
