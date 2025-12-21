"""Example: Wait dialog with cancellation."""
import hiew
import time

# Show a wait dialog with custom message
hiew.MessageWaitOpen("Processing... Press ESC to cancel")

# Simulate work, checking for cancellation
for i in range(10):
    if hiew.IsKeyBreak():
        hiew.MessageWaitClose()
        hiew.Message("Cancelled", "Operation cancelled by user")
        break
    time.sleep(0.5)
else:
    hiew.MessageWaitClose()
    hiew.Message("Done", "Operation completed!")
