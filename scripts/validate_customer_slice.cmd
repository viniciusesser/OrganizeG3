@echo off
setlocal
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0validate_customer_slice.ps1"
exit /b %ERRORLEVEL%
