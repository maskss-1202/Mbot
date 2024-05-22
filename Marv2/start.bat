@echo off
:run_python
echo Starting Discord Bot...
ping 127.0.0.1 -n 1 > nul
echo Starting Bot...
py main.py
if %errorlevel% neq 0 (
    echo An error occurred. Restarting...
    timeout /t 5 /nobreak >nul
    goto run_python
)
echo Press any key to exit...

:ping_loop
cls
echo Pinging...
ping 127.0.0.1 -n 1 > nul
timeout /t 2 >nul
goto ping_loop

pause >nul
