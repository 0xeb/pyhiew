"""Example: String input."""
import hiew

result = hiew.GetString("Enter your name:", 50, "Anonymous")

if result:
    hiew.Message("Hello", f"Hello, {result}!")
else:
    hiew.Message("Cancelled", "You pressed ESC")
