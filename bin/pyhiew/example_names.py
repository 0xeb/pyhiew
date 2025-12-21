"""Example: Names/symbols management."""
import hiew
from hiew import Names, Data

# Get current offset
offset = Data.GetCurrentOffset()

# Add various names and comments
Names.AddGlobal(offset, f"mark_{offset:X}")
Names.AddGlobalComment(offset, "This is a global comment")
Names.AddLocalComment(offset + 1, "This is a local comment")

Names.AddGlobal(offset + 100, "GlobalName")
Names.AddLocal(offset + 101, "LocalName")

# Show counts
lines = [
    f"Local names: {Names.CountLocal()}",
    f"Global names: {Names.CountGlobal()}",
    f"Total: {Names.CountNames()}",
    "",
]

# Find names
result = Names.FindName("LocalName")
if result:
    off, is_local = result
    lines.append(f"LocalName at 0x{off:X} (local={is_local})")

result = Names.FindGlobalName("GlobalName")
if result:
    lines.append(f"GlobalName at 0x{result:X}")

result = Names.FindLocalName("LocalName")
if result:
    lines.append(f"LocalName (local) at 0x{result:X}")

# Show that wrong type returns None
if Names.FindGlobalName("LocalName") is None:
    lines.append("LocalName not found as global (correct!)")

if Names.FindLocalName("GlobalName") is None:
    lines.append("GlobalName not found as local (correct!)")

hiew.Window.FromString("Names Demo", lines, width=50)
