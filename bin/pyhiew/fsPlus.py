"""
Hiew script to load fsPlus into Hiew's process memory

This script loads fsPlus.dll via LoadLibraryA().
fsPlus will hook various File I/O APIs to provide "Process to File" interface.
Inside Hiew, press F9 to list files and processes. Please see fsPlus.ini for more information
"""

# -----------------------------------------------------------------------
from ctypes import *
import hiew

# -----------------------------------------------------------------------
def load_fsplus():
    k32 = windll.kernel32

    # Inject fsPlus into Hiew process
    h = k32.LoadLibraryA(hiew.PYHIEW_PATH + r"\fsPlus.dll")
    if h == 0:
        return ("Info", "Failed to load fsPlus (GLE=%d)" % k32.GetLastError())
    else:
        return ("Info", "fsPlus+ loaded! Now press F9 to list files and processes")

# -----------------------------------------------------------------------
try:
    # Check if installed
    FSPLUS_LOADED

except:
    FSPLUS_LOADED = load_fsplus()

hiew.Message(*FSPLUS_LOADED)