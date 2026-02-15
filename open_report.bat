@echo off
set PROJECT_DIR=%~dp0
set REPORT_DIR=%PROJECT_DIR%reports\allure-report

IF NOT EXIST "%REPORT_DIR%" (
    echo Allure report not found!
    echo Please run tests first.
    pause
    exit /b
)

cd /d "%REPORT_DIR%"

echo Opening Allure Report...
start http://localhost:8000

python -m http.server 8000

pause
