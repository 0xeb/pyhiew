"""
PyHiew - Python bindings for the Hiew SDK
(c) Elias Bachaalany
"""
from __future__ import annotations

import _hiew
import traceback
import os
from dataclasses import dataclass, field
from glob import glob
from typing import Any, Callable

# ---------------------------------------------------------------------------
# From _hiew
VERSION: dict = _hiew.VERSION
"""Version info dict: major, minor, sdkmajor, sdkminor"""

PYHIEW_PATH: str = _hiew.PYHIEW_PATH
"""Path to pyhiew's scripts"""

PYHIEW_VERSION: dict = _hiew.PYHIEW_VERSION
"""pyhiew plugin version: major, minor, build"""

# ---------------------------------------------------------------------------
# Testing switch: Turn on to have the startup script reload each time
PYHIEW_RELOAD_STARTUP_SCRIPT = True
PYHIEW_SHOW_EXEC_ERRORS = False

# ---------------------------------------------------------------------------
# From hem_en.txt
HEM_MAX_DUALSTR_LEN = 20
HEM_MAX_FINDSTR_LEN = 20

# ---------------------------------------------------------------------------
# Startup scripts
PYHIEW_STARTUP_SCRIPT: str | None = None
PYHIEW_STARTUP_DICT: dict | None = None
PYHIEW_STARTUP_FUNCTION: str | None = None
PYHIEW_STARTUP_SCRIPT_EXECUTED = False

# Script browser excluded scripts
PYHIEW_EXCLUDED_SCRIPTS: set[str] = {'init', 'hiew', '_hiew'}

# ---------------------------------------------------------------------------
# HEM keys line
# Active x12 | Caption 6x12
HIEW_KEY_LABEL_LEN = 6
HIEW_EMPTY_KEY_LABEL = ' ' * HIEW_KEY_LABEL_LEN
HEM_FNKEY_DELIMITER = '|'

# Function keys
HEM_FNKEY_F1 = 0xFF3B
HEM_FNKEY_F2 = 0xFF3C
HEM_FNKEY_F3 = 0xFF3D
HEM_FNKEY_F4 = 0xFF3E
HEM_FNKEY_F5 = 0xFF3F
HEM_FNKEY_F6 = 0xFF40
HEM_FNKEY_F7 = 0xFF41
HEM_FNKEY_F8 = 0xFF42
HEM_FNKEY_F9 = 0xFF43
HEM_FNKEY_F10 = 0xFF44
HEM_FNKEY_F11 = 0xFF85
HEM_FNKEY_F12 = 0xFF86

HEM_FNKEY_ALTF1 = 0xFF68
HEM_FNKEY_ALTF2 = 0xFF69
HEM_FNKEY_ALTF3 = 0xFF6A
HEM_FNKEY_ALTF4 = 0xFF6B
HEM_FNKEY_ALTF5 = 0xFF6C
HEM_FNKEY_ALTF6 = 0xFF6D
HEM_FNKEY_ALTF7 = 0xFF6E
HEM_FNKEY_ALTF8 = 0xFF6F
HEM_FNKEY_ALTF9 = 0xFF70
HEM_FNKEY_ALTF10 = 0xFF71
HEM_FNKEY_ALTF11 = 0xFF8B
HEM_FNKEY_ALTF12 = 0xFF8C

HEM_FNKEY_CTRLF1 = 0xFF5E
HEM_FNKEY_CTRLF2 = 0xFF5F
HEM_FNKEY_CTRLF3 = 0xFF60
HEM_FNKEY_CTRLF4 = 0xFF61
HEM_FNKEY_CTRLF5 = 0xFF62
HEM_FNKEY_CTRLF6 = 0xFF63
HEM_FNKEY_CTRLF7 = 0xFF64
HEM_FNKEY_CTRLF8 = 0xFF65
HEM_FNKEY_CTRLF9 = 0xFF66
HEM_FNKEY_CTRLF10 = 0xFF67
HEM_FNKEY_CTRLF11 = 0xFF89
HEM_FNKEY_CTRLF12 = 0xFF8A

HEM_FNKEY_SHIFTF1 = 0xFF54
HEM_FNKEY_SHIFTF2 = 0xFF55
HEM_FNKEY_SHIFTF3 = 0xFF56
HEM_FNKEY_SHIFTF4 = 0xFF57
HEM_FNKEY_SHIFTF5 = 0xFF58
HEM_FNKEY_SHIFTF6 = 0xFF59
HEM_FNKEY_SHIFTF7 = 0xFF5A
HEM_FNKEY_SHIFTF8 = 0xFF5B
HEM_FNKEY_SHIFTF9 = 0xFF5C
HEM_FNKEY_SHIFTF10 = 0xFF5D
HEM_FNKEY_SHIFTF11 = 0xFF87
HEM_FNKEY_SHIFTF12 = 0xFF88

# ---------------------------------------------------------------------------
# HEM SDK version
HEM_SDK_VERSION_MAJOR = 0
HEM_SDK_VERSION_MINOR = 54

# ---------------------------------------------------------------------------
# Length of strings
HEM_FILENAME_MAXLEN = 260
HEM_SHORTNAME_SIZE = 16
HEM_NAME_SIZE = 60
HEM_ABOUT_SIZE = 48

# ---------------------------------------------------------------------------
# Bits of the hemFlag
HEM_FLAG_MARKEDBLOCK = 0x80000000

HEM_FLAG_FILEMASK = 0x00003FD8
HEM_FLAG_ELF64 = 0x00002000
HEM_FLAG_PE64 = 0x00001000
HEM_FLAG_ELF = 0x00000800
HEM_FLAG_NLM = 0x00000400
HEM_FLAG_PE = 0x00000200
HEM_FLAG_LX = 0x00000100
HEM_FLAG_LE = 0x00000080
HEM_FLAG_NE = 0x00000040
HEM_FLAG_FILE = 0x00000010
HEM_FLAG_DISK = 0x00000008

HEM_FLAG_MODEMASK = 0x00000007
HEM_FLAG_CODE = 0x00000004
HEM_FLAG_HEX = 0x00000002
HEM_FLAG_TEXT = 0x00000001

# ---------------------------------------------------------------------------
# Bits of the returnActionFlag
HEM_RETURN_SETOFFSET = 0x00000001
HEM_RETURN_FILERELOAD = 0x00000002
HEM_RETURN_SETMODE = 0x00000004

HEM_RETURN_MODE_TEXT = 1
HEM_RETURN_MODE_HEX = 2
HEM_RETURN_MODE_CODE = 3

# ---------------------------------------------------------------------------
# Find flags
HEM_FIND_NEXT = 0x00000001
HEM_FIND_BACKWARD = 0x00000002
HEM_FIND_CASESENSITIVE = 0x00000004
HEM_FIND_INMARK = 0x00000008
HEM_FIND_USEMASK = 0x00000010

# ---------------------------------------------------------------------------
# Return codes
HEM_ERR_INTERNAL = -21
HEM_ERR_INVALID_ARGUMENT = -20
HEM_ERR_HIEW_VERSION_INVALID = -19
HEM_ERR_FNKEYS_INVALID = -18
HEM_ERR_READONLYFILE = -17
HEM_ERR_POINTER_IS_NULL = -16
HEM_ERR_HIEWDATA_SIZE_MISMATCH = -15
HEM_ERR_HEMINFO_SIZE_MISMATCH = -14
HEM_ERR_HEMINFO_IS_NULL = -13
HEM_ERR_HEM2HEMGATE_IS_NULL = -12
HEM_ERR_HEM_NOTFOUND = -11
HEM_ERR_HIEWGATE_PARM_INVALID = -10
HEM_ERR_HIEWGATE_ID_INVALID = -9
HEM_ERR_HANDLE_INVALID = -8
HEM_ERR_NOADDRESS_HIEWGATE = -7
HEM_ERR_NOENTRYPOINT = -6
HEM_ERR_UNLOADED = -5
HEM_ERR_SDKVER_INCOMPATIBLE = -4
HEM_ERR_NOADDRESS_LOAD = -3
HEM_ERR_LOADDLL = -2
HEM_ERROR = -1
HEM_OK = 0

HEM_INPUT_ESC = 0
HEM_INPUT_CR = 1
HEM_KEYBREAK = 2
HEM_OFFSET_NOT_FOUND = -1


# ---------------------------------------------------------------------------
# API Functions
# ---------------------------------------------------------------------------

def FileOpenForWrite() -> int:
    """Reopens file for writing."""
    return _hiew.HiewGate_FileOpenForWrite()


def FileRead(offset: int, size: int) -> tuple[int, bytes | None]:
    """
    Reads from the file.

    Args:
        offset: File offset
        size: Number of bytes to read

    Returns:
        Tuple of (return_code, buffer or None)
    """
    return _hiew.HiewGate_FileRead(offset, size)


def FileWrite(offset: int, buf: bytes) -> int:
    """
    Writes buffer to file.

    Args:
        offset: File offset
        buf: Buffer to write

    Returns:
        HEM_ERR_xxx code
    """
    return _hiew.HiewGate_FileWrite(offset, buf)


def GetData() -> 'Data':
    """Returns a Data instance with current file info."""
    return _hiew.HiewGate_GetData()


def GetLastResult() -> int:
    """Returns the last HiewGate result code."""
    return _hiew.HiewGate_GetLastResult()


def Message(title: str, msg: str) -> int:
    """Displays a single-line message to user."""
    return _hiew.HiewGate_Message(title, msg)


def MarkBlock(offset1: int, offset2: int) -> int:
    """
    Marks a block.

    Args:
        offset1: Start position
        offset2: End position

    Returns:
        HEM_ERR_xxx code
    """
    return _hiew.HiewGate_MarkBlock(offset1, offset2)


def UnmarkBlock() -> int:
    """Unmarks the current selection."""
    return _hiew.HiewGate_UnmarkBlock()


def Find(flags: int, offset: int, data: bytes, mask: bytes | None = None) -> int | None:
    """
    Finds data in file.

    Args:
        flags: HEM_FIND_xxx flags
        offset: Starting offset
        data: Data to find (max HEM_MAX_FINDSTR_LEN bytes)
        mask: Currently unused

    Returns:
        Offset of match, or None if not found
    """
    return _hiew.HiewGate_Find(flags, offset, data)


def FindNext() -> int | None:
    """Returns the next find offset, or None if not found."""
    return _hiew.HiewGate_FindNext()


def GetString(title: str, max_input: int, init_val: str = "") -> str | None:
    """
    Gets one line of user input.

    Args:
        title: Prompt title
        max_input: Maximum input length
        init_val: Initial input value

    Returns:
        User input string, or None if ESC pressed
    """
    return _hiew.HiewGate_GetString(title, max_input, init_val)


def GetStringDual(
    title: str,
    max_input: int,
    init_val: bytes = b"",
    on_hex_line: bool = False
) -> tuple[int, bytes] | None:
    """
    Gets ascii/hex dual-line input from user.

    Args:
        title: Prompt title
        max_input: Max input (up to HEM_MAX_DUALSTR_LEN)
        init_val: Initial binary value
        on_hex_line: Focus on hex line initially

    Returns:
        Tuple of (on_hex_line, data) or None if ESC pressed
    """
    return _hiew.HiewGate_GetStringDual(title, max_input, init_val, on_hex_line)


def GetFilename(title: str, filename: str = "") -> bytes | None:
    """
    Gets filename with F9 browser support.

    Args:
        title: Prompt title
        filename: Initial filename

    Returns:
        Selected filename, or None if ESC pressed
    """
    return _hiew.HiewGate_GetFilename(title, filename)


def IsKeyBreak() -> bool:
    """Returns True if user pressed ESC during wait dialog."""
    return _hiew.HiewGate_IsKeyBreak()


def MessageWaitOpen(msg: str = "") -> int:
    """
    Opens a wait message dialog.

    Args:
        msg: Message to display (default: "Processing...")
    """
    return _hiew.HiewGate_MessageWaitOpen(msg)


def MessageWaitClose() -> None:
    """Closes the wait message dialog."""
    return _hiew.HiewGate_MessageWaitClose()


def SetErrorMsg(error_msg: str) -> int:
    """Sets an error message visible in F6 info."""
    return _hiew.HiewGate_SetErrorMsg(error_msg)


def MessageBox(message: str, title: str = 'Info') -> None:
    """Shows a Windows message box."""
    return _hiew.MessageBox(title, message)


def dbg(msg: str) -> None:
    """Outputs a debug string (OutputDebugString)."""
    _hiew.od(msg)


def ReturnOffset(offset: int) -> None:
    """Sets the cursor offset on script exit."""
    return _hiew.ReturnOffset(offset)


def ReturnMode(mode: int) -> None:
    """
    Sets the view mode on script exit.

    Args:
        mode: HEM_RETURN_MODE_xxx constant
    """
    return _hiew.ReturnMode(mode)


def ReturnReload() -> None:
    """Reloads the file on script exit."""
    return _hiew.ReturnReload()


def ResetReturnAction() -> None:
    """Clears all ReturnXxx() settings."""
    return _hiew.ResetReturnAction()


def ReturnCode(rc: int) -> None:
    """
    Sets the return code on script exit.

    Args:
        rc: HEM_ERR_xxx code
    """
    return _hiew.ReturnCode(rc)


# ---------------------------------------------------------------------------
# Helper Functions
# ---------------------------------------------------------------------------

def _make_keys(key_def: dict[int, str]) -> str:
    """
    Constructs a Hiew keys line string.

    Args:
        key_def: Dict mapping key number (1-12) to label.
                 Prefix label with '-' for inactive key.

    Returns:
        Hiew keys line string
    """
    if not key_def:
        return ""

    keys = []
    labels = []

    for i in range(1, 13):
        label = key_def.get(i, '')
        if label.startswith('-'):
            key = '0'
            label = label[1:]
        elif label:
            key = '1'
        else:
            key = '0'
            label = HIEW_EMPTY_KEY_LABEL

        # Pad or truncate to HIEW_KEY_LABEL_LEN
        label = label[:HIEW_KEY_LABEL_LEN].ljust(HIEW_KEY_LABEL_LEN)
        keys.append(key)
        labels.append(label)

    return ''.join(keys) + HEM_FNKEY_DELIMITER + ''.join(labels)


# ---------------------------------------------------------------------------
# Control Classes
# ---------------------------------------------------------------------------

class Control:
    """Base class for Hiew UI controls (Menu/Window)."""

    def __init__(self):
        self._control = None
        self._is_window = False

    def _clear_control(self) -> None:
        """Clears an already setup control."""
        if self._control:
            _hiew.ControlClear(self._control)
            self._control = None

    def __del__(self):
        self._clear_control()

    def Create(
        self,
        title: str,
        lines: list[str],
        width: int,
        is_window: bool,
        main_keys: dict[int, str] | str = "",
        alt_keys: dict[int, str] | str = "",
        ctrl_keys: dict[int, str] | str = "",
        shift_keys: dict[int, str] | str = ""
    ) -> bool:
        """
        Creates a control (does not show it).

        Args:
            title: Control title
            lines: List of lines
            width: Control width
            is_window: True for window, False for menu
            main_keys: Main function keys
            alt_keys: Alt function keys
            ctrl_keys: Ctrl function keys
            shift_keys: Shift function keys

        Returns:
            True if created successfully
        """
        self._clear_control()

        # Convert key dicts to strings
        if isinstance(main_keys, dict):
            main_keys = _make_keys(main_keys)
        if isinstance(alt_keys, dict):
            alt_keys = _make_keys(alt_keys)
        if isinstance(ctrl_keys, dict):
            ctrl_keys = _make_keys(ctrl_keys)
        if isinstance(shift_keys, dict):
            shift_keys = _make_keys(shift_keys)

        result = _hiew.ControlCreate(
            self, title, lines, width, is_window,
            main_keys, alt_keys, ctrl_keys, shift_keys
        )
        if not result:
            return False

        self._control = result
        self._is_window = is_window
        return True

    def Show(self, sel_line: int = 0) -> tuple[int, int]:
        """
        Shows the control.

        Args:
            sel_line: Initial selected line (0-based, for menus)

        Returns:
            Tuple of (selected_line or -1, fnkey or 0)
        """
        if not self._control:
            return (HEM_ERR_INVALID_ARGUMENT, 0)

        r, fnkey = _hiew.ControlShow(self._control, sel_line)

        if self._is_window:
            return (r, fnkey)
        else:
            return (r - 1, fnkey) if r > 0 else (-1, 0)


class Menu(Control):
    """Menu control."""

    def __init__(self):
        super().__init__()

    def Create(
        self,
        title: str,
        lines: list[str],
        width: int,
        main_keys: dict[int, str] | str = "",
        alt_keys: dict[int, str] | str = "",
        ctrl_keys: dict[int, str] | str = "",
        shift_keys: dict[int, str] | str = ""
    ) -> bool:
        """Creates a menu. See Control.Create()."""
        return super().Create(
            title, lines, width, False,
            main_keys, alt_keys, ctrl_keys, shift_keys
        )

    def Show(self, sel_line: int = 0) -> tuple[int, int]:
        """
        Shows the menu.

        Args:
            sel_line: Initial selected line (0-based)

        Returns:
            Tuple of (selected_line or -1, fnkey or 0)
        """
        return super().Show(sel_line)


class Window(Control):
    """Window control."""

    def __init__(self):
        super().__init__()

    def Create(
        self,
        title: str,
        lines: list[str],
        width: int,
        main_keys: dict[int, str] | str = "",
        alt_keys: dict[int, str] | str = "",
        ctrl_keys: dict[int, str] | str = "",
        shift_keys: dict[int, str] | str = ""
    ) -> bool:
        """Creates a window. See Control.Create()."""
        return super().Create(
            title, lines, width, True,
            main_keys, alt_keys, ctrl_keys, shift_keys
        )

    def Show(self) -> tuple[int, int]:
        """
        Shows the window.

        Returns:
            Tuple of (0, fnkey)
        """
        return super().Show()

    @staticmethod
    def FromString(
        title: str,
        msg: str | list[str],
        width: int = 70,
        main_keys: dict[int, str] | str = "",
        alt_keys: dict[int, str] | str = "",
        ctrl_keys: dict[int, str] | str = "",
        shift_keys: dict[int, str] | str = ""
    ) -> tuple[int, int]:
        """
        Quick way to show a window from a string.

        Args:
            title: Window title
            msg: Message string (with newlines) or list of lines
            width: Window width

        Returns:
            Tuple of (0, fnkey)
        """
        w = Window()
        lines = msg.split('\n') if isinstance(msg, str) else msg
        w.Create(
            title=title,
            lines=lines,
            width=width,
            main_keys=main_keys,
            alt_keys=alt_keys,
            ctrl_keys=ctrl_keys,
            shift_keys=shift_keys
        )
        return w.Show()


# ---------------------------------------------------------------------------
# Data Class
# ---------------------------------------------------------------------------

@dataclass
class Data:
    """File information from Hiew (HIEWGATE_GETDATA)."""
    hemHandle: int = 0
    callId: int = 0
    filename: str | None = None
    filelength: int = 0
    offsetCurrent: int = 0
    offsetMark1: int = 0
    offsetMark2: int = 0
    sizeMark: int = 0
    filenameW: str | None = None  # Unicode filename (SDK 0.54+)

    @staticmethod
    def GetCurrentOffset() -> int:
        """Returns the current file offset."""
        return GetData().offsetCurrent

    @staticmethod
    def GetFileName() -> str | None:
        """Returns the opened filename."""
        return GetData().filename

    @staticmethod
    def GetSel() -> tuple[int, int, int]:
        """
        Returns selection information.

        Returns:
            Tuple of (start, end, size)
        """
        d = GetData()
        return (d.offsetMark1, d.offsetMark2, d.sizeMark)

    @staticmethod
    def GetSelData() -> bytes | None:
        """Returns the selected bytes, or None if nothing selected."""
        mark1, mark2, mark_sz = Data.GetSel()
        if mark_sz == 0:
            return None

        rc, data = FileRead(mark1, mark_sz)
        return data if rc > 0 else None


# ---------------------------------------------------------------------------
# Names Class
# ---------------------------------------------------------------------------

class Names:
    """Name/symbol management."""

    @staticmethod
    def Clear() -> int:
        """Clears all names."""
        return _hiew.HiewGate_Names_Clear()

    @staticmethod
    def AddLocal(offset: int, name: str) -> int:
        """Adds a local name at offset."""
        return _hiew.HiewGate_Names_AddLocal(offset, name)

    @staticmethod
    def AddGlobal(offset: int, name: str) -> int:
        """Adds a global name at offset."""
        return _hiew.HiewGate_Names_AddGlobal(offset, name)

    @staticmethod
    def AddLocalComment(offset: int, comment: str) -> int:
        """Adds a local comment at offset."""
        return _hiew.HiewGate_Names_AddLocalComment(offset, comment)

    @staticmethod
    def AddGlobalComment(offset: int, comment: str) -> int:
        """Adds a global comment at offset."""
        return _hiew.HiewGate_Names_AddGlobalComment(offset, comment)

    @staticmethod
    def DelGlobalComment(offset: int) -> int:
        """Deletes a global comment at offset."""
        return _hiew.HiewGate_Names_DelGlobalComment(offset)

    @staticmethod
    def DelLocalComment(offset: int) -> int:
        """Deletes a local comment at offset."""
        return _hiew.HiewGate_Names_DelLocalComment(offset)

    @staticmethod
    def DelLocal(offset: int) -> int:
        """Deletes a local name at offset."""
        return _hiew.HiewGate_Names_DelLocal(offset)

    @staticmethod
    def DelGlobal(offset: int) -> int:
        """Deletes a global name at offset."""
        return _hiew.HiewGate_Names_DelGlobal(offset)

    @staticmethod
    def CountLocal() -> int:
        """Returns the count of local names."""
        return _hiew.HiewGate_Names_CountLocal()

    @staticmethod
    def CountGlobal() -> int:
        """Returns the count of global names."""
        return _hiew.HiewGate_Names_CountGlobal()

    @staticmethod
    def CountNames() -> int:
        """Returns the total name count."""
        return _hiew.HiewGate_Names_CountName()

    @staticmethod
    def FindName(name: str) -> tuple[int, bool] | None:
        """
        Finds a name.

        Returns:
            Tuple of (offset, is_local) or None if not found
        """
        result = _hiew.HiewGate_Names_FindName(name)
        if result is None:
            return None
        return (result[0], bool(result[1]))

    @staticmethod
    def FindLocalName(name: str) -> int | None:
        """Finds a local name, returns offset or None."""
        r = Names.FindName(name)
        return r[0] if r and r[1] else None

    @staticmethod
    def FindGlobalName(name: str) -> int | None:
        """Finds a global name, returns offset or None."""
        r = Names.FindName(name)
        return r[0] if r and not r[1] else None


# ---------------------------------------------------------------------------
# Dialog Helpers
# ---------------------------------------------------------------------------

def AskYesNo(
    msg: str,
    title: str = 'Please confirm',
    width: int = 70,
    yesno_keys: dict[int, str] | None = None
) -> bool:
    """
    Shows a Yes/No confirmation dialog.

    Returns:
        True for Yes, False for No/ESC
    """
    if yesno_keys is None:
        yesno_keys = {1: "Yes", 2: "No"}

    w = Window()
    if not w.Create(title, msg.split('\n'), width=width, main_keys=yesno_keys):
        return False

    while True:
        _, k = w.Show()
        if k == HEM_FNKEY_F1:
            return True
        elif k == HEM_FNKEY_F2:
            return False
        elif k == 0:  # ESC
            return False


# ---------------------------------------------------------------------------
# Script Execution
# ---------------------------------------------------------------------------

def PyHiew_ExecuteScript(
    script: str,
    g: dict,
    strip_path: bool = False
) -> str | None:
    """
    Executes a script file.

    Args:
        script: Script filename
        g: Global scope dict

    Returns:
        None on success, error string on failure
    """
    try:
        with open(script, "rb") as f:
            code = compile(f.read(), script, 'exec')
        exec(code, g)
        return None
    except Exception as e:
        err = f"{e}\n{traceback.format_exc()}"
        if strip_path:
            base_path = script[:-len(os.path.basename(script))]
            err = err.replace(base_path, '')
        if PYHIEW_SHOW_EXEC_ERRORS:
            MessageBox(err)
        return err


def PyHiew_ExecuteCallable(
    func_name: str,
    g: dict,
    *args,
    **kwargs
) -> str | None:
    """
    Executes a callable from the given scope.

    Args:
        func_name: Function name
        g: Global scope dict

    Returns:
        None on success, error string on failure
    """
    try:
        g[func_name](*args, **kwargs)
        return None
    except Exception as e:
        return f"{e}\n{traceback.format_exc()}"


def PyHiew_GetScriptFileName(script: str) -> str:
    """Returns full path for a script name."""
    return os.path.join(PYHIEW_PATH, f"{script}.py")


def SetStartupScript(
    st_script: str,
    st_dict: dict,
    st_func: str
) -> None:
    """
    Sets the startup script.

    Args:
        st_script: Script name (with or without .py)
        st_dict: Global scope for the script
        st_func: Entry function name
    """
    global PYHIEW_EXCLUDED_SCRIPTS, PYHIEW_STARTUP_DICT
    global PYHIEW_STARTUP_FUNCTION, PYHIEW_STARTUP_SCRIPT
    global PYHIEW_STARTUP_SCRIPT_EXECUTED

    # Strip extension
    if st_script.endswith('.py'):
        st_script = st_script[:-3]

    # Remove previous from exclusion
    if PYHIEW_STARTUP_SCRIPT:
        PYHIEW_EXCLUDED_SCRIPTS.discard(PYHIEW_STARTUP_SCRIPT)

    PYHIEW_STARTUP_SCRIPT_EXECUTED = False
    PYHIEW_STARTUP_DICT = st_dict
    PYHIEW_STARTUP_FUNCTION = st_func
    PYHIEW_STARTUP_SCRIPT = st_script
    PYHIEW_EXCLUDED_SCRIPTS.add(st_script)


def PyHiew_Main() -> int:
    """Main entry point for PyHiew."""
    global PYHIEW_STARTUP_SCRIPT_EXECUTED

    if not PYHIEW_STARTUP_SCRIPT:
        Message("Error!", "No startup script specified!")
        return HEM_ERR_NOENTRYPOINT

    if not PYHIEW_STARTUP_SCRIPT_EXECUTED:
        script_path = PyHiew_GetScriptFileName(PYHIEW_STARTUP_SCRIPT)
        err = PyHiew_ExecuteScript(script_path, PYHIEW_STARTUP_DICT, True)

        if err is None:
            PYHIEW_STARTUP_SCRIPT_EXECUTED = not PYHIEW_RELOAD_STARTUP_SCRIPT
        else:
            Window.FromString("Startup script file execution error", err)
            return HEM_ERR_INTERNAL

    err = PyHiew_ExecuteCallable(PYHIEW_STARTUP_FUNCTION, PYHIEW_STARTUP_DICT)
    if err is not None:
        err = err.replace(PYHIEW_PATH + '\\', '')
        Window.FromString("Startup script function execution error", err)

    return HEM_OK
