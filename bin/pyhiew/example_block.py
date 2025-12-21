"""Example: Block marking."""
import hiew

# Unmark any existing block
hiew.UnmarkBlock()

# Mark first 256 bytes
hiew.MarkBlock(0, 255)
hiew.Message("Done", "Marked bytes 0x00-0xFF")
