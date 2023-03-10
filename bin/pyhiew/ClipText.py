"""
Hiew script to copy data from hiew to text.


Usage
========
This script can copy data to various formats (source code representation, plain text)

$ pip install pywin32

Copy to:
----------
- Plain text
- C source
- Pascal source


TODO
=====
- Pasting from
  - Plain text

History
=========
- 1.0      - initial version
"""
import hiew

try:
    import win32clipboard
except:
    hiew.Message("Error", "win32clipboard module not installed!")
    raise

# -----------------------------------------------------------------------
def buf_to_c_array(buf):
    i = 1
    out = []
    for ch in buf:
        out.append('0x%02x, ' % ch)
        if i % CLIP_TEXT_ITEMS_PER_LINE == 0:
            i = 1
            out.append('\n\t')
        else:
            i += 1
    out = ''.join(out).rstrip()[:-1]
    return ('static unsigned char data[%d] = \n{\n\t%s\n};' %
            (len(buf), out))

# -----------------------------------------------------------------------
def buf_to_python_string(buf):
    out = []
    for ch in buf:
        out.append('\\%02x' % ch)
    out = ''.join(out)
    return ('"%s"' % out)

# -----------------------------------------------------------------------
def buf_to_pascal_array(buf):
    i = 1
    out = []
    for ch in buf:
        out.append('$%02x, ' % ch)
        if i % CLIP_TEXT_ITEMS_PER_LINE == 0:
            i = 1
            out.append('\n\t')
        else:
            i += 1
    out = ''.join(out).rstrip()[:-1]
    return ('const data: array[0..%d] of Byte = \n(\n\t%s\n);' %
            (len(buf)-1, out))

# -----------------------------------------------------------------------
def copy_text_to_clipboard(text):
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardText(text)
    win32clipboard.CloseClipboard()
    return True

# -----------------------------------------------------------------------
def hiew_main():

    try:
        buf = hiew.Data.GetSelData()
        if not buf:
            hiew.Message("Error", "Nothing is selected!")
            return

        global CLIP_TEXT_CHOICE
        m = hiew.Menu()
        m.Create(
            title = "Copy/Paste",
            lines = ["Copy as plain text",    #0
                     "Copy as C array",       #1
                     "Copy as Pascal array",  #2
                     "Copy as Python string", #3
                     "Cancel"                 #4
                     ],
            width = 30)

        n, k = m.Show(CLIP_TEXT_CHOICE)
        if n == 0:
            if copy_text_to_clipboard(buf):
                hiew.Message("Info", "Copied to clipboard as plain text!")
        elif n == 1:
            if copy_text_to_clipboard(buf_to_c_array(buf)):
                hiew.Message("Info", "Copied to clipboard as C array!")
        elif n == 2:
            if copy_text_to_clipboard(buf_to_pascal_array(buf)):
                hiew.Message("Info", "Copied to clipboard as pascal array!")
        elif n == 3:
            if copy_text_to_clipboard(buf_to_python_string(buf)):
                hiew.Message("Info", "Copied to clipboard as Python string!")
        elif n == 4:
            pass
        else:
            return
    except Exception as e:
        hiew.MessageBox(str(e), 'Exception')
    CLIP_TEXT_CHOICE = n

# -----------------------------------------------------------------------
try:
    CLIP_TEXT_CHOICE
    CLIP_TEXT_ITEMS_PER_LINE
except:
    CLIP_TEXT_CHOICE = 0
    CLIP_TEXT_ITEMS_PER_LINE = 16

hiew_main()
