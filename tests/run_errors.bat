@echo off
chcp 65001 >nul
cd /d "%~dp0.."
for %%f in (tests\examples\broken.conf tests\errors\*.conf) do (
    echo %%f
    call run.bat -o out\e.xml < %%f
    echo.
)