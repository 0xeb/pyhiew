# pyhiew

Python scripting for [Hiew](http://hiew.io) hex editor/disassembler.

Write Python scripts to automate tasks, add new features, and extend Hiew's functionality through the HEM (Hiew Extension Module) plugin interface.

## Features

- Full access to Hiew's file reading/writing, navigation, and UI
- Menu and window creation for interactive scripts
- Symbol/name management for annotations
- Search functionality with pattern matching
- Block selection and manipulation

## Requirements

- Windows (Hiew is Windows-only)
- Python 3.10+ 32-bit (Hiew is 32-bit)
- Hiew 8.x or later

## Installation

1. Copy `pyhiew.hem` to your Hiew folder (or `hem` subfolder)
2. Copy the `pyhiew` folder to your Hiew folder

If you have multiple Python versions, use a launcher script:

```batch
@echo off
set PATH=C:\Python312-32;%PATH%
"%~dp0\hiew32.exe" %*
```

## Building

```bash
git clone --recursive https://github.com/0xeb/pyhiew.git
cd pyhiew
mkdir build && cd build
cmake -A Win32 ..
cmake --build . --config Release
```

Output: `bin/pyhiew.hem`

**Note**: Uses [hiew-sdk-cpp](https://github.com/0xeb/hiew-sdk-cpp) as a submodule. The `--recursive` flag is required.

## Included Scripts

Located in `bin/pyhiew/`:

| Script | Description |
|--------|-------------|
| `scriptbrowser.py` | Default startup - browse and run scripts |
| `ClipText.py` | Copy bytes as C/Python/Pascal code (`pip install pyperclip`) |
| `Decompress.py` | Decompress selected bytes with zlib |
| `Strings.py` | Display strings using SysInternals strings.exe |
| `PEiD.py` | PE file identification |
| `example_*.py` | API usage examples |

## Quick Start

```python
import hiew

# Show a message
hiew.Message("Hello", "Hello from PyHiew!")

# Get file info
data = hiew.GetData()
print(f"File: {data.filename}, Size: {data.filelength}")

# Read bytes
rc, buf = hiew.FileRead(0, 16)

# Create a menu
menu = hiew.Menu()
menu.Create("Options", ["Option 1", "Option 2"], width=30)
selection, key = menu.Show()
```

See `bin/pyhiew/example_*.py` for more examples and `pyhiew/doc/` for API documentation.

## License

MIT
