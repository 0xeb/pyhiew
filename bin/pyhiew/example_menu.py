"""Example: Menu usage."""
import hiew

menu = hiew.Menu()
menu.Create(
    title="Menu title",
    lines=[f"Line {i}" for i in range(10)],
    width=30,
    main_keys={1: "-Help", 4: "-Disabled"},
    alt_keys={1: "AHelp", 4: "Reload"}
)

selection = 0
while True:
    selection, key = menu.Show(selection)
    hiew.Message("Selection", f"n={selection} k={key}")
    if selection == -1:
        break
