@echo off
REM #---------------BY 3verlaster---------------#
echo Apex RAT made with love by 3verlaster
echo Requirements installer for Apex RAT Builder
REM #-------------START-INSTALLING--------------#
echo [/] installation started.
echo [*] uninstalling library "pyinstaller" ... 
pip uninstall pyinstaller
echo [*] installing an older library "Pyinstaller" ... [for .py to .exe compiling]
pip install pyinstaller==5.11.0
echo [+] library "Pyinstaller" installed.
echo [*] uninstalling library "pyarmor" ... 
pip uninstall pyarmor
echo [*] installing an older library "pyarmor" ... 
pip install pyarmor==7.7.4
echo [+] library "pyarmor" installed.
REM #--------------------END---------------------#