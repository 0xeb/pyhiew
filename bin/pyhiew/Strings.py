"""
Strings.py - A hiew script to display strings in a file (c) Elias Bachaalany

This script uses "strings.exe" utility from SysInternals
"""
import hiew
import os

# -----------------------------------------------------------------------
class StringsScript(object):

    @staticmethod
    def get_strings_from_file(filename):
        try:
            f = os.popen(r'strings.exe -nobanner -o %s' % filename)
            lines = f.readlines()
            f.close()
            data = []
            for line in lines:
                line = line.strip()
                i = line.find(':')
                data.append((int(line[:i]), line[i+1:]))

            return data if len(data) else None
        except:
            return None


    FileName = property(lambda self: hiew.Data.GetFileName())


    def __init__(self):
        self.cache = None
        self.menu = hiew.Menu()
        self.last_filename = None
        self.sel = None
        self.last_text = None


    def refresh(self):
        """
        Refreshes the string list
        """

        # Reset selection
        self.sel = 0

        # Get open filename
        filename = self.FileName

        # Extract strings
        self.cache = self.get_strings_from_file(filename)
        if not self.cache:
            return False

        # No strings? Display an info line
        main_keys = {5: "ReLoad"}
        if not self.cache:
            lines = ["No items",
                    "-> press F5 to refresh"
                    "-> press F7 to search",
                    "-> press Shift-F7 to search next"]
            alt_keys = shift_keys = {}
        else:
            lines = [x[:60] for _, x in self.cache]
            main_keys[7] = "Find"
            shift_keys = {7: "Next"}

        # Compile the menu
        self.menu.Create(
            title = "Strings for %s" % os.path.basename(filename),
            lines = lines,
            width = 70,
            main_keys = main_keys,
            shift_keys = shift_keys)

        return True


    def search(self):
        self.last_text = hiew.GetString("Enter search string", 50)
        return self.search_next(0)



    def search_next(self, delta = 1):
        txt = self.last_text
        if txt:
            c = len(self.cache)
            i = self.sel + delta
            while i < c:
                if self.cache[i][1].find(txt) != -1:
                    return i
                i += 1

        # Return same index on no match
        return self.sel


    def execute(self):
        """
        Executes the script
        """

        filename = self.FileName
        if self.last_filename != filename:
            if not self.refresh():
                hiew.Window.FromString("Error", "Strings utility from SysInternals is not present")
                return False

            self.last_filename = filename

        while True:
            n, k = self.menu.Show(self.sel)
            # ESC?
            if n == -1:
                break

            # Refresh?
            if k == hiew.HEM_FNKEY_F5:
                self.refresh()
                continue

            # No data? Do nothing
            if not self.cache:
                continue

            # Search?
            if k == hiew.HEM_FNKEY_F7:
                self.sel = self.search()
            # Search next?
            elif k == hiew.HEM_FNKEY_SHIFTF7:
                self.sel = self.search_next()
            else:
                # Save last selection
                self.sel = n

            # Jump in file
            hiew.ReturnOffset(self.cache[self.sel][0])

            break

        return True

# -----------------------------------------------------------------------
def StringsMain():
    global STRINGS_SCRIPT
    try:
        # Instantiated?
        STRINGS_SCRIPT
    except:
        # Init
        STRINGS_SCRIPT = StringsScript()

    STRINGS_SCRIPT.execute()

# -----------------------------------------------------------------------
StringsMain()
