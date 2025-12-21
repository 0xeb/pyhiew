"""Example: Basic API usage."""
import hiew

# Get file info
data = hiew.GetData()

# Show file info
hiew.Message("File", data.filename or "No file")
hiew.Message("Size", f"{data.filelength} bytes")
hiew.Message("Offset", f"0x{data.offsetCurrent:X}")
