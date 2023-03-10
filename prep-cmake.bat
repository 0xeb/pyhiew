@echo off

:: check the Batchography book [http://amzn.to/1X3tQ4K]

setlocal

if not exist build (
    mkdir build
    pushd build
    cmake -A Win32 ..
    popd
)

if "%1"=="build" (
    pushd build
    cmake --build . --config Release
    popd
)
echo.
echo All done!
echo.