setlocal

:: pip install epydoc

pushd ..\bin\pyhiew

copy ..\..\src\pyhiewdoc.cfg
\Python27-32\python.exe ..\..\src\pyhiewdoc.py
del pyhiewdoc.cfg
