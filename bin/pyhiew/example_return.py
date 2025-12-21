"""Example: Return actions (executed when script exits)."""
import hiew

# Clear any previous return actions
hiew.ResetReturnAction()

# Jump to offset 0x100 and switch to disassembly mode
hiew.ReturnOffset(0x100)
hiew.ReturnMode(hiew.HEM_RETURN_MODE_CODE)

hiew.Message("Done", "Will jump to 0x100 in code mode")
