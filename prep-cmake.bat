@echo off

:: check the Batchography book [http://amzn.to/1X3tQ4K]

setlocal

if not exist build cmake -A Win32 -B build
if "%1"=="build" cmake --build build --config Release

echo.
echo All done!
echo.