"""
PyHiew ScriptBrowser startup script

This script acts like a shell. It displays other scripts found in the pyhiew directory
and allows the user to executes them.

(c) Elias Bachaalany
"""
import hiew
from hiew import Menu
from glob import glob
import os

# -----------------------------------------------------------------------
class PyScriptBrowser(Menu):
    def __init__(self):
        Menu.__init__(self)

        # Refresh files
        self.RefreshFiles()


    def RefreshFiles(self):
        """
        Refresh the files list and recompiles the menu
        """
        L = len(hiew.PYHIEW_PATH) + 1
        self.files = []
        self.lastsel = 0

        for fn in glob(hiew.PYHIEW_PATH + '\\*.py'):
            # Strip path and extension
            short_fn = fn[L:-3]
            if short_fn[0] == '_' or short_fn in hiew.PYHIEW_EXCLUDED_SCRIPTS:
                continue

            self.files.append(short_fn)

        # No files?
        if not self.files:
            return False

        # Compile menu
        r = self.Create(
            title = " Script browser %s " % ("" if gPyScriptBrowserSER == 0 else gPyScriptBrowserSER),
            lines = self.files,
            width = 30,
            main_keys = {1: "-Help", 4: "-Edit", 8: "-Delete"},
            alt_keys  = {5: "Refresh"})

        if not r:
            self.Message("Could not create menu!" + str(r))
            return False
        return True

    # -----------------------------------------------------------------------
    def Message(self, msg, title = "Info"):
        Message(title = title, msg = msg)

    # -----------------------------------------------------------------------
    def Show(self):
        while True:
            # No files?
            if not self.files:
                self.Message("No script files found!")
                return

            # Show the menu
            n = self.lastsel
            n, k = Menu.Show(self, n)
            if n == -1:
                return

            # Update last selection
            self.lastsel = n

            # Refresh?
            if k == hiew.HEM_FNKEY_ALTF4:
                self.RefreshFiles()
                continue

            script_fn = hiew.PyHiew_GetScriptFileName(self.files[n])
            err = hiew.PyHiew_ExecuteScript(
                    script_fn,
                    globals(),
                    True)

            if err is not None:
                hiew.Window.FromString(" Script error ", err)

            return

# -----------------------------------------------------------------------
def ScriptBrowserMain():
    global gPyScriptBrowser, gPyScriptBrowserSER
    debug = False
    hiew.PYHIEW_RELOAD_STARTUP_SCRIPT = debug

    try:
        gPyScriptBrowser
        gPyScriptBrowserSER += 1
    except:
        gPyScriptBrowserSER = 0
        gPyScriptBrowser = PyScriptBrowser()

    if debug:
        gPyScriptBrowser = PyScriptBrowser()

    gPyScriptBrowser.Show()
