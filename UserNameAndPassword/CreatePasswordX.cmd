@echo off
cd /D %~dp0%
echo %1% | CreatePassword.py | CreatePasswordX.py
