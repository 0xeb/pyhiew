"""
PyHiew initialization script.

This script runs once when pyhiew loads and sets the startup script.
Edit the 'mode' variable to change behavior.
"""
from enum import IntEnum

import hiew


class Mode(IntEnum):
    RELEASE = 0  # Use scriptbrowser.py (default)
    DEVMODE = 1  # Use _test_startup.py for development
    DOCGEN = 2   # Generate documentation


mode = Mode.RELEASE

if mode == Mode.DOCGEN:
    hiew.SetStartupScript('_gendocs.py', globals(), 'docgen')
elif mode == Mode.DEVMODE:
    hiew.SetStartupScript('_test_startup.py', globals(), 'testMain')
else:
    hiew.SetStartupScript('scriptbrowser.py', globals(), 'ScriptBrowserMain')
