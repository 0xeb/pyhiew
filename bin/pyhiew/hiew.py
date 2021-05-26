# -----------------------------------------------------------------------
# PyHiew - Python bindings for the Hiew SDK
# (c) Elias Bachaalany
import _hiew
import traceback
import os
from glob import glob

# -----------------------------------------------------------------------
# From _hiew
VERSION = _hiew.VERSION # Hiew and HEM version
"""
Version information stored in a dictionary with these keys:
        major
        minor
        sdkmajor
        sdkminor
"""
PYHIEW_PATH = _hiew.PYHIEW_PATH
"""Path to pyhiew's scripts"""

PYHIEW_VERSION = _hiew.PYHIEW_VERSION
"""
pyhiew plugin version dictionary: major, minor, build
"""

# -----------------------------------------------------------------------
# Testing switch: Turn on to have the startup script reload each time
PYHIEW_RELOAD_STARTUP_SCRIPT = True
PYHIEW_SHOW_EXEC_ERRORS = False

# -----------------------------------------------------------------------
# From hem_en.txt
HEM_MAX_DUALSTR_LEN =  20
HEM_MAX_FINDSTR_LEN =  20

# -----------------------------------------------------------------------
# Startup scripts
PYHIEW_STARTUP_SCRIPT = None
PYHIEW_STARTUP_DICT = None
PYHIEW_STARTUP_FUNCTION = None
PYHIEW_STARTUP_SCRIPT_EXECUTED = False

# Script browser excluded scripts
PYHIEW_EXCLUDED_SCRIPTS = set(['init', 'hiew', '_hiew'])

# -----------------------------------------------------------------------
# Meta
# -----
# defines RE
# /s: #define *([^ ]+) +([^ ]+)
# /r: \1 \2
# comment header
# /s: ////////////////////////////////////////////////////////////
# /r: # -----------------------------------------------------------------------

# -----------------------------------------------------------------------
#// HEM keys line
#//  Active x12  | Caption 6x12
__HIEW_KEY_LINES = "123456789ABC|F1____F2____F3____F4____F5____F6____F7____F8____F9____F10___F11___F12___"

HIEW_KEY_LABEL_LEN   = 6
HIEW_EMPTY_KEY_LABEL = ' ' * HIEW_KEY_LABEL_LEN
HEM_FNKEY_DELIMITER  = '|'

#<defines>
HEM_FNKEY_F1                    = 0xFF3B
HEM_FNKEY_F2                    = 0xFF3C
HEM_FNKEY_F3                    = 0xFF3D
HEM_FNKEY_F4                    = 0xFF3E
HEM_FNKEY_F5                    = 0xFF3F
HEM_FNKEY_F6                    = 0xFF40
HEM_FNKEY_F7                    = 0xFF41
HEM_FNKEY_F8                    = 0xFF42
HEM_FNKEY_F9                    = 0xFF43
HEM_FNKEY_F10                   = 0xFF44
HEM_FNKEY_F11                   = 0xFF85
HEM_FNKEY_F12                   = 0xFF86

HEM_FNKEY_ALTF1                 = 0xFF68
HEM_FNKEY_ALTF2                 = 0xFF69
HEM_FNKEY_ALTF3                 = 0xFF6A
HEM_FNKEY_ALTF4                 = 0xFF6B
HEM_FNKEY_ALTF5                 = 0xFF6C
HEM_FNKEY_ALTF6                 = 0xFF6D
HEM_FNKEY_ALTF7                 = 0xFF6E
HEM_FNKEY_ALTF8                 = 0xFF6F
HEM_FNKEY_ALTF9                 = 0xFF70
HEM_FNKEY_ALTF10                = 0xFF71
HEM_FNKEY_ALTF11                = 0xFF8B
HEM_FNKEY_ALTF12                = 0xFF8C

HEM_FNKEY_CTRLF1                = 0xFF5E
HEM_FNKEY_CTRLF2                = 0xFF5F
HEM_FNKEY_CTRLF3                = 0xFF60
HEM_FNKEY_CTRLF4                = 0xFF61
HEM_FNKEY_CTRLF5                = 0xFF62
HEM_FNKEY_CTRLF6                = 0xFF63
HEM_FNKEY_CTRLF7                = 0xFF64
HEM_FNKEY_CTRLF8                = 0xFF65
HEM_FNKEY_CTRLF9                = 0xFF66
HEM_FNKEY_CTRLF10               = 0xFF67
HEM_FNKEY_CTRLF11               = 0xFF89
HEM_FNKEY_CTRLF12               = 0xFF8A

HEM_FNKEY_SHIFTF1               = 0xFF54
HEM_FNKEY_SHIFTF2               = 0xFF55
HEM_FNKEY_SHIFTF3               = 0xFF56
HEM_FNKEY_SHIFTF4               = 0xFF57
HEM_FNKEY_SHIFTF5               = 0xFF58
HEM_FNKEY_SHIFTF6               = 0xFF59
HEM_FNKEY_SHIFTF7               = 0xFF5A
HEM_FNKEY_SHIFTF8               = 0xFF5B
HEM_FNKEY_SHIFTF9               = 0xFF5C
HEM_FNKEY_SHIFTF10              = 0xFF5D
HEM_FNKEY_SHIFTF11              = 0xFF87
HEM_FNKEY_SHIFTF12              = 0xFF88

# -----------------------------------------------------------------------
# HEM SDK version, Major version will compatible!

HEM_SDK_VERSION_MAJOR = 0
HEM_SDK_VERSION_MINOR = 53

# -----------------------------------------------------------------------
# Length of strings

HEM_FILENAME_MAXLEN  = 260
HEM_SHORTNAME_SIZE   = 16
HEM_NAME_SIZE        = 60
HEM_ABOUT_SIZE       = 48

# -----------------------------------------------------------------------
# Bits of the hemFlag

HEM_FLAG_MARKEDBLOCK    = 0x80000000

HEM_FLAG_FILEMASK       = 0x00003FD8
HEM_FLAG_ELF64          = 0x00002000
HEM_FLAG_PE64           = 0x00001000
HEM_FLAG_ELF            = 0x00000800
HEM_FLAG_NLM            = 0x00000400
HEM_FLAG_PE             = 0x00000200
HEM_FLAG_LX             = 0x00000100
HEM_FLAG_LE             = 0x00000080
HEM_FLAG_NE             = 0x00000040
HEM_FLAG_FILE           = 0x00000010
HEM_FLAG_DISK           = 0x00000008

HEM_FLAG_MODEMASK       = 0x00000007
HEM_FLAG_CODE           = 0x00000004
HEM_FLAG_HEX            = 0x00000002
HEM_FLAG_TEXT           = 0x00000001

# -----------------------------------------------------------------------
# Bits of the returnActionFlag

HEM_RETURN_SETOFFSET     = 0x00000001
HEM_RETURN_FILERELOAD    = 0x00000002
HEM_RETURN_SETMODE       = 0x00000004

HEM_RETURN_MODE_TEXT     = 1
HEM_RETURN_MODE_HEX      = 2
HEM_RETURN_MODE_CODE     = 3

# -----------------------------------------------------------------------
# Bits of the Find()

HEM_FIND_NEXT            = 0x00000001
HEM_FIND_BACKWARD        = 0x00000002
HEM_FIND_CASESENSITIVE   = 0x00000004
HEM_FIND_INMARK          = 0x00000008
HEM_FIND_USEMASK         = 0x00000010

# -----------------------------------------------------------------------
# Return code of the hem interface

HEM_ERR_INTERNAL                            = (-21)
HEM_ERR_INVALID_ARGUMENT                    = (-20)
HEM_ERR_HIEW_VERSION_INVALID                = (-19)
HEM_ERR_FNKEYS_INVALID                      = (-18)
HEM_ERR_READONLYFILE                        = (-17)
HEM_ERR_POINTER_IS_NULL                     = (-16)
HEM_ERR_HIEWDATA_SIZE_MISMATCH              = (-15)
HEM_ERR_HEMINFO_SIZE_MISMATCH               = (-14)
HEM_ERR_HEMINFO_IS_NULL                     = (-13)
HEM_ERR_HEM2HEMGATE_IS_NULL                 = (-12)
HEM_ERR_HEM_NOTFOUND                        = (-11)
HEM_ERR_HIEWGATE_PARM_INVALID               = (-10)
HEM_ERR_HIEWGATE_ID_INVALID                 = (-9)
HEM_ERR_HANDLE_INVALID                      = (-8)
HEM_ERR_NOADDRESS_HIEWGATE                  = (-7)
HEM_ERR_NOENTRYPOINT                        = (-6)
HEM_ERR_UNLOADED                            = (-5)
HEM_ERR_SDKVER_INCOMPATIBLE                 = (-4)
HEM_ERR_NOADDRESS_LOAD                      = (-3)
HEM_ERR_LOADDLL                             = (-2)
HEM_ERROR                                   = (-1)
HEM_OK                                      = 0

HEM_INPUT_ESC                               = 0
HEM_INPUT_CR                                = 1
HEM_KEYBREAK                                = 2
HEM_OFFSET_NOT_FOUND                        = -1

#</defines>

# -----------------------------------------------------------------------
#int HiewGate_Menu(HEM_BYTE *title, HEM_BYTE **lines, int linesCount,
#                  int width, int startItem, HEM_FNKEYS *fnKeys,
#                  HEM_UINT *returnFnKey,
#                  HEM_BYTE * (*CallbackLine)( int, void * ), void *pData );
# Refer to the Menu wrapper class


# -----------------------------------------------------------------------
#int HiewGate_Window(HEM_BYTE *title, HEM_BYTE **lines, int linesCount,
#                    int width, HEM_FNKEYS *fnKeys, HEM_UINT *returnFnKey );
# Refer to the Window wrapper class


# -----------------------------------------------------------------------
#int HiewGate_FileOpenForWrite(void);
def FileOpenForWrite():
    """Reopens file for writing"""
    return _hiew.HiewGate_FileOpenForWrite()

# -----------------------------------------------------------------------
#int HiewGate_FileRead(HEM_QWORD offset, HEM_UINT bytes, HEM_BYTE *buffer);
def FileRead(offset, bytes):
    """
    Reads from the file

    @param offset: file offset
    @param bytes: amount of bytes to read

    @return:
        - (rc != HEM_OK, None)
        - (rc == HEM_OK, buffer)
    """
    return _hiew.HiewGate_FileRead(offset, bytes)

# -----------------------------------------------------------------------
#int HiewGate_FileWrite(HEM_QWORD offset, HEM_UINT bytes, HEM_BYTE *buffer);
def FileWrite(offset, buf):
    """
    Writes buffer to file

    @param offset: file offset
    @param buf: buffer to write
    @return: HEM_ERR_xxx
    """
    return _hiew.HiewGate_FileWrite(offset, buf)

# -----------------------------------------------------------------------
#int HiewGate_GetData(HIEWGATE_GETDATA *hiewData);
def GetData():
    """
    Returns a Data class instance
    see HIEWGATE_GETDATA structure
    """
    return _hiew.HiewGate_GetData()

# -----------------------------------------------------------------------
#int HiewGate_GetLastResult(void);
def GetLastResult():
    return _hiew.HiewGate_GetLastResult()

# -----------------------------------------------------------------------
#int HiewGate_Message(HEM_BYTE *title, HEM_BYTE *msg);
def Message(title, msg):
    """Displays single-line message to user"""
    return _hiew.HiewGate_Message(title, msg)

# -----------------------------------------------------------------------
#int HiewGate_MarkBlock(HEM_QWORD offset1, HEM_QWORD offset2);
def MarkBlock(offset1, offset2):
    """
    Marks a block
    @param offset1: start pos
    @param offset2: end pos
    @return: HEM_ERR_xxx
    """
    return _hiew.HiewGate_MarkBlock(offset1, offset2)

# -----------------------------------------------------------------------
#int HiewGate_UnmarkBlock(void);
def UnmarkBlock():
    """
    Unmarks selection
    @return: HEM_ERR_xxx
    """
    return _hiew.HiewGate_UnmarkBlock()

# -----------------------------------------------------------------------
#HEM_QWORD HiewGate_Find(int flags, HEM_QWORD offset, HEM_BYTE *pData, int dataLength /* <= 20 */, HEM_BYTE *pMask);
def Find(flags, offset, data, mask = None):
    """
    @param flags: one of HEM_FIND_XXXX flags
    @param offset: starting offset
    @param data: data buffer to find ; len is max HEM_MAX_FINDSTR_LEN
    @param mask: currently unused

    @return:
        None - not found
        Offset - offset of the match
    """
    return _hiew.HiewGate_Find(flags, offset, data)

# -----------------------------------------------------------------------
#HEM_QWORD HiewGate_FindNext(void);
def FindNext():
    """Returns the find next offset or None"""
    return _hiew.HiewGate_FindNext()

# -----------------------------------------------------------------------
#int HiewGate_GetString(HEM_BYTE *title, HEM_BYTE *string, int stringLen);
def GetString(title, max_input, init_val = ""):
    """
    Gets one line of user input
    @param title: prompt title
    @param max_input: max input
    @param init_val: initial input value
    @return: string or None (if user pressed ESC)
    """
    return _hiew.HiewGate_GetString(title, max_input, init_val)

# -----------------------------------------------------------------------
#int HiewGate_GetStringDual( HEM_BYTE *title, HEM_BYTE *string, int stringLenMax /* <= 20 */, int stringLen, int *bOnHexLine );
def GetStringDual(title, max_input, init_val = "", on_hex_line = False):
    """
    Gets ascii/hex line from user

    @param title: prompt title
    @param max_input: max input; HEM_MAX_DUALSTR_LEN
    @param init_val: initial input value (contains binary data)
    @param on_hex_line: focus on hex line
    @return:
        None (if user pressed ESC)
        tuple(1, string) if user pressed enter on the hex line
        tuple(0, string) if user pressed enter on the string line
    """
    return _hiew.HiewGate_GetStringDual(title, max_input, init_val, on_hex_line)

# -----------------------------------------------------------------------
#int HiewGate_GetFilename(HEM_BYTE *title, HEM_BYTE *filename);
def GetFilename(title, filename = ""):
    """
    Gets line with filename. Hiew offers the F9 key to browse for a filename
    @param title: prompt title
    @param filename: initial filename value
    @return: string or None
    """
    return _hiew.HiewGate_GetFilename(title, filename)

# -----------------------------------------------------------------------
#int HiewGate_IsKeyBreak(void);
def IsKeyBreak():
    """
    Checks if the wait dialog is cancelled
    @return: Boolean
    """
    return _hiew.HiewGate_IsKeyBreak()

# -----------------------------------------------------------------------
#int HiewGate_MessageWaitOpen(HEM_BYTE *msg);
def MessageWaitOpen(msg = ""):
    """
    Open single-line message to user.
    @param msg: the wait message. If empty then message will "Processing..."
    """
    return _hiew.HiewGate_MessageWaitOpen(msg)

# -----------------------------------------------------------------------
#int HiewGate_MessageWaitClose(void);
def MessageWaitClose():
    return _hiew.HiewGate_MessageWaitClose()

# -----------------------------------------------------------------------
#int HiewGate_SetErrorMsg(HEM_BYTE *errorMsg);
def SetErrorMsg(error_msg):
    return _hiew.HiewGate_SetErrorMsg(error_msg)

# -----------------------------------------------------------------------
#int        HiewGate_Names_DelName( HEM_BYTE *name );
#HEM_BYTE  *HiewGate_Names_GetLocal( HEM_QWORD offset, HEM_BYTE *retname, int retnameBufferLength );
#HEM_BYTE  *HiewGate_Names_GetGlobal( HEM_QWORD offset, HEM_BYTE *retname, int retnameBufferLength );
#HEM_BYTE  *HiewGate_Names_GetLocalComment( HEM_QWORD offset, HEM_BYTE *retname, int retnameBufferLength );
#HEM_BYTE  *HiewGate_Names_GetGlobalComment( HEM_QWORD offset, HEM_BYTE *retname, int retnameBufferLength );

#HEM_QWORD  HiewGate_Global2Local( HEM_QWORD offsetGlobal );
#HEM_QWORD  HiewGate_Local2Global( HEM_QWORD offsetLocal );

# -----------------------------------------------------------------------
#int        HiewGate_GetHem2HemGate( HIEWGATE_GETHEM2HEMGATE *tag, HEM_BYTE *shortName );


# -----------------------------------------------------------------------
def _make_keys(key_def):
    """
    Constructs a hiew keys line string

    @param key_def: A dictionary where:
                    - key: function_key_number
                    - value: key_label -> active key
                    - value: -key_label -> inactive key

    @return: hiew keys line
    """
    keys = []
    labels = []

    # no keys? return an empty string
    if len(key_def) == 0:
        return ""

    for i in range(1, 12 + 1):
        try:
            key, label = i, key_def[i]
            if label.startswith('-'):
                key = '0'
                label = label[1:]
            else:
                key = '1'
        except KeyError:
            key = '0'
            label = HIEW_EMPTY_KEY_LABEL

        t = len(label)
        if t > HIEW_KEY_LABEL_LEN:
            label = label[0:HIEW_KEY_LABEL_LEN]
        else:
            label += ' ' * (HIEW_KEY_LABEL_LEN - t)

        keys.append(key)
        labels.append(label)

    return ''.join(keys) + HEM_FNKEY_DELIMITER + ''.join(labels)

# -----------------------------------------------------------------------
class Control:
    """
    Hiew control class
    """
    def __init__(self):
        self.__control = None


    def _clear_control(self):
        """Clears an already setup control"""
        if self.__control:
            _hiew.ControlClear(self.__control)
            self.__control = None


    def __del__(self):
        self._clear_control()


    def Create(self,
             title,
             lines,
             width,
             is_window,
             main_keys = "",
             alt_keys = "",
             ctrl_keys = "",
             shift_keys = ""):
        """
        Creates a control but does not show it.

        @param title: control title
        @param lines: a list of lines
        @param width: control width
        @param is_window: control type
        @param main_keys: main key lines (optional)
        @param alt_keys: main key lines (optional)
        @param ctrl_keys: ctrl key lines (optional)
        @param shift_keys: shift key lines (optional)

        @return: Boolean == control was compiled successfully
        """

        # Clear previous control
        self._clear_control()

        # Convert key dictionary to Hiew key lines string
        if main_keys:
            main_keys = _make_keys(main_keys)
        if alt_keys:
            alt_keys = _make_keys(alt_keys)
        if ctrl_keys:
            ctrl_keys = _make_keys(ctrl_keys)
        if shift_keys:
            shift_keys = _make_keys(shift_keys)

        # Call the wrapper
        r = _hiew.ControlCreate(self, title, lines, width, is_window, main_keys, alt_keys, ctrl_keys, shift_keys)
        if not r:
            return False

        # Bind
        self.__control = r
        self.__is_window = is_window

        return True


    def Show(self, sel_line = 0):
        """
        Shows an already setup control. If no control is setup HEM_ERR_INVALID_ARGUMENT will be returned
        @param sel_line: The initial line (0 based)

        @return: tuple(-1|lineno, 0|HEM_FNKEY_xxx)
        """
        if not self.__control:
            return HEM_ERR_INVALID_ARGUMENT

        r, fnkey = _hiew.ControlShow(self.__control, sel_line)
        if self.__is_window:
            return (r, fnkey)
        else:
            if r <= 0:
                return (-1, 0)
            else:
                return (r-1, fnkey)

# -----------------------------------------------------------------------
class Menu(Control):
    """Menu control"""
    def __init__(self):
        Control.__init__(self)


    def Show(self, sel_line = 0):
        return Control.Show(sel_line)


    def Create(self,
             title,
             lines,
             width,
             main_keys = "",
             alt_keys = "",
             ctrl_keys = "",
             shift_keys = ""):
        #
        return Control.Create(self, title, lines,
                       width, False, main_keys,
                       alt_keys, ctrl_keys, shift_keys)


    def Show(self, sel_line = 0):
        """
        Shows the main menu. Refer to Control.Show()
        @param sel_line: Initial selected line
        """
        return Control.Show(self, sel_line)


# -----------------------------------------------------------------------
class Window(Control):
    """Window control"""
    def __init__(self):
        Control.__init__(self)


    def Show(self):
        """
        Shows the main window.

        Refer to Control.Show()

        @return: (n=0, fnkey)
        """
        return Control.Show(self)


    @staticmethod
    def FromString(
        title,
        msg,
        width = 70,
        main_keys = "",
        alt_keys = "",
        ctrl_keys = "",
        shift_keys = ""):
        """
        Static method to quickly construct a window from a string with
        embedded new lines
        @param title: The window title
        @param msg: The message (containing embedded new lines) or an array of lines

        @return: (n=0, fnkey)
        """
        w = Window()
        r = w.Create(
            title = title,
            lines = (msg.split('\n') if isinstance(msg, str) else msg),
            width = width,
            main_keys = main_keys,
            alt_keys = alt_keys,
            ctrl_keys = ctrl_keys,
            shift_keys = shift_keys)

        return w.Show()


    def Create(self,
             title,
             lines,
             width,
             main_keys = "",
             alt_keys = "",
             ctrl_keys = "",
             shift_keys = ""):
        """
        Creates a window. Refer to Control() class
        """
        return Control.Create(self, title, lines,
                       width, True, main_keys,
                       alt_keys, ctrl_keys, shift_keys)


# -----------------------------------------------------------------------
class Data(object):
    """Class representing HIEWGATE_GETDATA"""
    def __init__(self,
            hemHandle = 0,
            callId = 0,
            filename = None,
            filelength = 0,
            offsetCurrent = 0,
            offsetMark1 = 0,
            offsetMark2 = 0,
            sizeMark = 0):

        self.hemHandle      = hemHandle
        self.callId         = callId
        self.filename       = filename
        self.filelength     = filelength
        self.offsetCurrent  = offsetCurrent
        self.offsetMark1    = offsetMark1
        self.offsetMark2    = offsetMark2
        self.sizeMark       = sizeMark

    @staticmethod
    def GetCurrentOffset():
        """Returns the current file offset"""
        return GetData().offsetCurrent

    @staticmethod
    def GetFileName():
        """
        Returns the opened file name
        """
        return GetData().filename

    @staticmethod
    def GetSel():
        """
        Returns selection information
        @return: (start, end, size)
        """
        d = GetData()
        return (d.offsetMark1, d.offsetMark2, d.sizeMark)

    @staticmethod
    def GetSelData():
        """
        Returns the selected buffer or None
        """
        mark1, mark2, mark_sz = Data.GetSel()
        if mark_sz == 0:
            return None

        r, s = FileRead(mark1, mark_sz)
        return None if not r else s


# -----------------------------------------------------------------------
class Names(object):
    """Name management class"""
    @staticmethod
    def Clear():
        """Clear all names"""
        return _hiew.HiewGate_Names_Clear()


    @staticmethod
    def AddLocal(offset, name):
        """
        Adds a local name

        @param offset: the offset to add the name at
        @param name: local name
        """
        return _hiew.HiewGate_Names_AddLocal(offset, name)


    @staticmethod
    def AddGlobal(offset, name):
        """
        Adds a global name

        @param offset: the offset to add the name at
        @param name: global name
        """
        return _hiew.HiewGate_Names_AddGlobal(offset, name)


    @staticmethod
    def AddLocalComment(offset, comment):
        """
        Adds a local comment

        @param offset: the offset
        @param comment: comment
        """
        return _hiew.HiewGate_Names_AddLocalComment(offset, comment)


    @staticmethod
    def AddGlobalComment(offset, comment):
        """
        Adds a global comment

        @param offset: the offset
        @param comment: comment
        """
        return _hiew.HiewGate_Names_AddGlobalComment(offset, comment)


    @staticmethod
    def DelGlobalComment(offset):
        """
        Deletes a global comment

        @param offset: the offset
        """
        return _hiew.HiewGate_Names_DelGlobalComment(offset)


    @staticmethod
    def DelLocalComment(offset):
        """
        Deletes a local comment

        @param offset: the offset
        """
        return _hiew.HiewGate_Names_DelLocalComment(offset)


    @staticmethod
    def DelLocal(offset):
        """
        Deletes a local name

        @param offset: the offset
        """
        return _hiew.HiewGate_Names_DelLocal(offset)


    @staticmethod
    def DelGlobal(offset):
        """
        Deletes a global name

        @param offset: the offset
        """
        return _hiew.HiewGate_Names_DelGlobal(offset)


    @staticmethod
    def CountLocal():
        """
        Returns the local names count
        """
        return _hiew.HiewGate_Names_CountLocal()


    @staticmethod
    def CountGlobal():
        """
        Returns the global names count
        """
        return _hiew.HiewGate_Names_CountGlobal()


    @staticmethod
    def CountNames():
        """
        Returns all the name count
        """
        return _hiew.HiewGate_Names_CountName()


    @staticmethod
    def FindName(name):
        """
        Finds any name

        @return: tuple(name offset, local ? 1 : 0) or None
        """
        return _hiew.HiewGate_Names_FindName(name)


    @staticmethod
    def FindLocalName(name):
        """
        Finds a local name
        """
        r = Names.FindName(name)
        return None if r is None or r[1] == 0 else r[0]


    @staticmethod
    def FindGlobalName(name):
        """
        Finds a global name

        @return: Global name offset
        """
        r = Names.FindName(name)
        return None if r is None or r[1] != 0 else r[0]


# -----------------------------------------------------------------------
def MessageBox(message, title = 'Info'):
    return _hiew.MessageBox(title, message)


# -----------------------------------------------------------------------
dbg = lambda msg: _hiew.od(msg)
"""Output debug string"""

# -----------------------------------------------------------------------
def ReturnOffset(offset):
    """
    Changes the offset upon the script termination
    @param offset: new offset
    """
    return _hiew.ReturnOffset(offset)

# -----------------------------------------------------------------------
def ReturnMode(mode):
    """
    Changes the view mode upon script termination
    @param mode: one of HEM_RETURN_MODE_XXXX
    """
    return _hiew.ReturnMode(mode)

# -----------------------------------------------------------------------
def ReturnReload():
    """
    Reloads the file upon script termination
    """
    return _hiew.ReturnReload()

# -----------------------------------------------------------------------
def ResetReturnAction():
    """
    Clears the returnActionFlag value.
    This will clear all the ReturnXXX() arguments that were set.
    """
    return _hiew.ResetReturnAction()

# -----------------------------------------------------------------------
def ReturnCode(rc):
    """
    Changes the return code upon script termination
    (set the return value of Hem_EntryPoint())
    @param rc: one of HEM_ERR_XXX
    """
    return _hiew.ReturnCode(rc)


# -----------------------------------------------------------------------
def AskYesNo(msg,
            title='Please confirm',
            width=70,
            yesno_keys={1: "Yes", 2: "No"}):
    """
    Creates a window and prompts the user to answer Yes or No

    @return: Boolean. False = No, True = Yes
    """
    w = Window()
    k = w.Create(title,
             msg.split('\n'),
             width=width,
             main_keys=yesno_keys)
    if not k:
        return False

    while True:
        ln, k = w.Show()
        if k == HEM_FNKEY_F1:
            return True
        elif k == HEM_FNKEY_F2:
            return False

# -----------------------------------------------------------------------
def PyHiew_ExecuteScript(script, g, strip_path = False):
    """
    Executes a script file and captures the error

    @param script: script file name
    @param g: the global scope

    @return:
        - None: execute successful
        - String: the exception and traceback
    """
    PY_COMPILE_ERR = None
    try:
        exec(compile(open(script, "rb").read(), script, 'exec'), g)
    except Exception as e:
        PY_COMPILE_ERR = str(e) + "\n" + traceback.format_exc()
        PY_COMPILE_ERR = PY_COMPILE_ERR.replace(
            script[:-len(os.path.basename(script))],
            '')
        if PYHIEW_SHOW_EXEC_ERRORS:
            MessageBox(PY_COMPILE_ERR)

    return PY_COMPILE_ERR

# -----------------------------------------------------------------------
def PyHiew_ExecuteCallable(func_name, g, *args, **kwargs):
    """
    Executes a callable and captures the error

    @param func_name: script file name
    @param g: the global scope

    @return:
        - None: execute successful
        - String: the exception and traceback
    """
    PY_COMPILE_ERR = None
    try:
        g[func_name](*args, **kwargs)
    except Exception as e:
        PY_COMPILE_ERR = str(e) + "\n" + traceback.format_exc()
    return PY_COMPILE_ERR


# -----------------------------------------------------------------------
def PyHiew_GetScriptFileName(script):
    """
    Given a script name it returns its full path relative to PYHIEW_PATH
    """
    return '%s\\%s.py' % (PYHIEW_PATH, script)


# -----------------------------------------------------------------------
def SetStartupScript(st_script, st_dict, st_func):
    global PYHIEW_EXCLUDED_SCRIPTS, PYHIEW_STARTUP_DICT, PYHIEW_STARTUP_FUNCTION, PYHIEW_STARTUP_SCRIPT

    # Strip extension
    if st_script.endswith('.py'):
        st_script = st_script[:-3]

    # Remove previous script from exclusion list
    if PYHIEW_STARTUP_SCRIPT:
        PYHIEW_EXCLUDED_SCRIPTS.remove(PYHIEW_STARTUP_SCRIPT)

    PYHIEW_STARTUP_SCRIPT_EXECUTED = False

    # Assign dictionary
    PYHIEW_STARTUP_DICT = st_dict

    # Assign function
    PYHIEW_STARTUP_FUNCTION = st_func

    # Assign startup script
    PYHIEW_STARTUP_SCRIPT = st_script

    # Add startup script to the exclusion list
    PYHIEW_EXCLUDED_SCRIPTS.add(st_script)


# -----------------------------------------------------------------------
def PyHiew_Main():
    """
    Main entry point of PyHiew
    """
    global PYHIEW_STARTUP_SCRIPT_EXECUTED

    # Startup script not set?
    if not PYHIEW_STARTUP_SCRIPT:
        Message("Error!", "No startup script specified!")
        return HEM_ERR_NOENTRYPOINT

    # Execute startup script once
    if not PYHIEW_STARTUP_SCRIPT_EXECUTED:
        # Execute it in the requested scope
        err = PyHiew_ExecuteScript(PyHiew_GetScriptFileName(PYHIEW_STARTUP_SCRIPT), PYHIEW_STARTUP_DICT, True)

        # Success? Remember and do not run the script again
        if err is None:
            PYHIEW_STARTUP_SCRIPT_EXECUTED = not PYHIEW_RELOAD_STARTUP_SCRIPT
        else:
            Window.FromString("Startup script file execution error", err)
            return HEM_ERR_INTERNAL

    # Run main function of the startup script
    err = PyHiew_ExecuteCallable(PYHIEW_STARTUP_FUNCTION, PYHIEW_STARTUP_DICT)
    if err is not None:
        err = err.replace(PYHIEW_PATH+'\\', '')
        Window.FromString("Startup script function execution error", err)

    return HEM_OK
