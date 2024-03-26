@echo off
title ShellExt4
set currentdir=%~dp0
color 02
if exist "%windir%\system32\reg.exe" goto regexist
title Missing component&echo.&echo  REG command core file could not be found. Cannot continue.&echo  You can still download missing component from GTweak's site.&echo.&echo  After file [reg.zip] is downloaded, unpack proper files to %windir%\system32&echo  and start this script again. Everything will work as it should.
:rch
set rch=
set/p rch= Would you like to execute download site right now? [y/n] 
if /i "%rch%"=="y" start /w http://gtweak.110mb.com/files/reg.zip&&goto end
if /i "%rch%"=="n" goto end
goto rch
:regexist
echo.&echo  Hiew (c)1991-2011 Eugeny Suslikov&echo  Hiew ShellExt Script (c)2009-2011 Michal Hanebach&echo.&echo  Select an action..&echo.&echo  1 Add context menu entry&echo  2 Remove context menu entry&echo  3 exit
:oep
echo.&set ch=&set/p ch=úYour choice  &call:tbl&goto oep
:tbl
if "%ch%"=="1" call:in&exit/b
if "%ch%"=="2" call:un&exit/b
if "%ch%"=="3" goto end
exit/b
:un
echo.
reg query "HKCR\*\shell\Open with Hacker's View">nul 2>&1||echo  It look like that menu entry has already been removed&&exit/b1
reg delete "HKCR\*\shell\Open with Hacker's View" /f>nul 2>&1&&echo  Done&&exit/b
echo  Error (probably insufficient permissions)
echo.
echo  Make sure you run ShellExt4 using rightclick ^> Run as Administrator
exit/b1
:in
echo.
if not exist "%currentdir%\hiew32.exe" echo  Place this script where [hiew32.exe] is placed and run script again...&&echo.&echo  ^<^ Any key to exit ^>&&pause>nul 2>&1&&goto end
reg add "HKCR\*\shell\Open with Hacker's View\command" /v "" /t "REG_SZ" /d ^""""%"""%%currentdir%hiew32.exe%^%%"""%""" ""%%1^"^"^" /f>nul 2>&1&&echo  Done&&exit/b
echo  Error (probably insufficient permissions)
echo.
echo  Make sure you run ShellExt4 using rightclick ^> Run as Administrator
exit/b1
:end
exit