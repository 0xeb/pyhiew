"""Example: Dual hex/ascii input."""
import hiew

# Initial value as bytes
initial = b"\x11\x22\x33\x44"

result = hiew.GetStringDual("Enter hex/ascii:", 10, initial, on_hex_line=False)

if result:
    on_hex, data = result
    mode = "hex line" if on_hex else "ascii line"
    hex_str = ' '.join(f'{b:02X}' for b in data)
    hiew.Message(f"Entered on {mode}", hex_str)
else:
    hiew.Message("Cancelled", "You pressed ESC")
