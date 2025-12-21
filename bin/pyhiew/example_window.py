"""Example: Window usage."""
import hiew

# Simple window
hiew.Window.FromString(
    "Window Title",
    "This is a simple window.\nWith multiple lines.\nPress any key to close."
)

# Window with function keys
window = hiew.Window()
window.Create(
    title="Window with Keys",
    lines=[f"Line {i}" for i in range(10)],
    width=40,
    main_keys={1: "Help", 10: "Exit"}
)

while True:
    _, key = window.Show()
    if key == hiew.HEM_FNKEY_F10 or key == 0:
        break
    elif key == hiew.HEM_FNKEY_F1:
        hiew.Message("Help", "This is help!")
