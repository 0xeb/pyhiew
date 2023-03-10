# Introduction

![pyhiew](src/pyhiew.ico) _pyhiew_ is a Python wrapper for [Hiew](http://hiew.io). It allows you to write Python scripts to extend Hiew's functionality.

# Installation

1. Copy `pyhiew.hem` to `%HIEW%` (or to `%HIEW%\hem`)
2. Copy `pyhiew` folder to `%HIEW%\pyhiew`

If you have multiple versions of Python installed (especially 64-bits and 32-bits), you may need to adjust your PATH environment variable so the correct version of Python is used.

Perhaps use a modified copy of the [hiewrun.bat](bin/hiewrun.bat) batch file or permanently adjust the `PATH` environment variable:

```batch
@echo off

set path=C:\Python311-32;%path%
"%~dp0\hiew32.exe" %*
```

Documentation can be found in `pyhiew/doc/index.html`.

## Built-in scripts

pyhiew comes with a few built-in scripts in the [pyhiew](bin/pyhiew) folder.

### System scripts:

- `init.py`: This is a special file that gets executed once when pyhiew initializes. One of its uses is to set the startup script.
- `hiew.py`: The pyhiew python library. Please check the documents folder.
- `scriptbrowser.py`: The standard script browsers (set as startup script). It lets you select and run other Python scripts in the folder.

### Sample scripts:

- `ClipText.py`: Allows you to copy selected bytes from Hiew into the clipboard (as C/Python/Pascal source code). This requires the pywin32 package (`pip install pywin32`).
- `IDA-Names-Server.py` and `3rdparty/IDA-Names-Client.py`: Client server plugins to transfer symbols from IDA to Hiew
- `test_pyshell.py`: A Python shell with Hiew as the Python host.
- `_test_startup.py`: A test startup script. Configure in `init.py`.
- `Decompress.py`: Uses `zlib.decompress` to decompress the selected bytes.
- All other scripts: various examples.

# Building instructions

This project requires Python 3 [(32bits)](https://www.python.org/ftp/python/3.11.2/python-3.11.2.exe), CMake and Visual Studio compiler.

```bash
git clone https://github.com/0xeb/pyhiew.git
cd pyhiew
mkdir build
cd build
cmake -A Win32 ..
cmake --build . --config Release
```

For testing, make a copy of your Hiew installation into the [bin](bin) folder. If you are using Visual Studio, you should be able to build and run without any additional steps.

You may also use the `prep-cmake.bat` script to prepare the build environment. Run `prep-cmake.bat build` to directly build the project.