# Installation

1. Copy `pyhiew.hem` to `%HIEW%`
2. Copy `pyhiew` folder to `%HIEW%\pyhiew`

## pyhiew folder

This folder should contain:

System scripts:

- `init.py`: This is a special file that gets executed once when pyhiew initializes. One of its uses is to set the startup script.
- `hiew.py`: The pyhiew python library. Please check the documents folder.
- `scriptbrowser.py`: The standard script browsers (set as startup script). It lets you select and run other Python scripts in the folder.

Sample scripts:

- `IDA-Names-Server.py` and `3rdparty/IDA-Names-Client.py`: Client server plugins to transfer symbols from IDA to Hiew
- `test_pyshell.py`: A Python shell with Hiew as the Python host.
- `_test_startup.py`: A test startup script. Configure in `init.py`
- `ClipText.py`: Allows you to copy selected bytes from Hiew into the clipboard (as C/Python/Pascal source code)
- All other scripts: various examples

Documentation in `pyhiew/doc/index.html`.

# Building instructions

1. Make sure that Python 3.8+ (32bits) is installed
2. Open the vcxproj file with Visual Studio, and update both the include and the linker folder locations
3. Compile!

