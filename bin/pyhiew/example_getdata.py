"""Example: GetData usage."""
import hiew

data = hiew.GetData()

lines = [
    f"Filename: {data.filename}",
    f"Length: {data.filelength}",
    f"Offset: 0x{data.offsetCurrent:X}",
    f"Mark1: 0x{data.offsetMark1:X}",
    f"Mark2: 0x{data.offsetMark2:X}",
    f"Selection size: {data.sizeMark}",
]

hiew.Window.FromString("File Data", lines, width=60)
