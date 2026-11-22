@echo off
chcp 65001 >nul
cd /d "%~dp0.."
for %%n in (server game home) do (
    echo %%n
    call run.bat -o out\%%n.xml < tests\examples\%%n.conf
    type out\%%n.xml
    echo.
)