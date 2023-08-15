@echo off
REM #---------------BY 3verlaster---------------#
echo Apex RAT made with love by 3verlaster
echo Requirements installer for Apex RAT Builder
REM #-------------START-INSTALLING--------------#
echo [/] installation started.
echo [*] installing library "Pyinstaller" ... [for .py to .exe compiling]
pip install pyinstaller
echo [+] library "Pyinstaller" installed.
echo [*] installing library "pyarmor" ... [for .py to .exe (obfuscated)]
pip install pyarmor
echo [+] library "pyarmor" installed.
REM #--------------------END---------------------#