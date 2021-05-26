import hiew

# Set the actions when this script returns:

hiew.ResetReturnAction()
# 1. Switch to disassembly
hiew.ReturnMode(hiew.HEM_RETURN_MODE_CODE)
# 2. Seek to 0x17
hiew.ReturnOffset(0x17)
