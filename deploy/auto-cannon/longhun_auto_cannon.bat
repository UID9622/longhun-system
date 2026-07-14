@echo off
chcp 65001 >nul
REM ==============================================================================
REM ⚡ 龍魂系統·全自動機槍啟動器 (Windows)
REM =============================================================================
REM DNA: #龍芯⚡️2026-07-11-AUTO-CANNON-v1.0
REM 效果: 雙擊一下，去抽根煙，回來全搞定
REM ==============================================================================

title 龍魂系統·全自動機槍 v1.0

echo.
echo ╔══════════════════════════════════════════════════════════════════╗
echo ║                                                                  ║
echo ║     龍魂系統·全自動機槍 v1.0 啟動中...                          ║
echo ║     DNA: #龍芯⚡️2026-07-11-AUTO-CANNON-v1.0                     ║
echo ║                                                                  ║
echo ╚══════════════════════════════════════════════════════════════════╝
echo.

REM 檢查 Python3
python3 --version >nul 2>&1
if %errorlevel% neq 0 (
    python --version >nul 2>&1
    if %errorlevel% neq 0 (
        echo [ERROR] 未找到 Python3，請先安裝 Python 3.10+
        pause
        exit /b 1
    ) else (
        set PYTHON_CMD=python
    )
) else (
    set PYTHON_CMD=python3
)

echo [OK] Python: %PYTHON_CMD%
echo [OK] 當前目錄: %CD%
echo.

REM 確保輸出目錄存在
if not exist "%USERPROFILE%\.龍魂\reports" mkdir "%USERPROFILE%\.龍魂\reports" 2>nul
if not exist "%USERPROFILE%\.龍魂\logs" mkdir "%USERPROFILE%\.龍魂\logs" 2>nul

REM 尋找主腳本
set MAIN_SCRIPT=%~dp0longhun_auto_cannon.py
if not exist "%MAIN_SCRIPT%" (
    set MAIN_SCRIPT=longhun_auto_cannon.py
)

if not exist "%MAIN_SCRIPT%" (
    echo [ERROR] 找不到 longhun_auto_cannon.py
    echo        請確保 .bat 和 .py 在同一目錄
    pause
    exit /b 1
)

echo [OK] 找到主腳本: %MAIN_SCRIPT%
echo.

REM 解析參數
set ARGS=
if "%1"=="--scan" (
    set ARGS=--scan
    echo [MODE] 僅掃描
) else if "%1"=="--fix" (
    set ARGS=--fix
    echo [MODE] 掃描+修復
) else if "%1"=="--report" (
    set ARGS=--report
    echo [MODE] 僅生成報告
) else if "%1"=="--daemon" (
    set ARGS=--daemon
    echo [MODE] 全自動 + 啟動守護進程
) else (
    echo [MODE] 全自動 (掃描+修復+報告)
    echo        提示: 加 --daemon 參數可同時啟動守護進程
)

echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.

REM 執行!
set START_TIME=%TIME%
%PYTHON_CMD% "%MAIN_SCRIPT%" %ARGS%
set EXIT_CODE=%errorlevel%
set END_TIME=%TIME%

echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.

if %EXIT_CODE% equ 0 (
    echo [DONE] 全自動機槍執行完成!
    echo        報告位置: %USERPROFILE%\.龍魂\reports\
    echo.
    echo 你可以去抽根煙了，回來全搞定。
) else (
    echo [ERROR] 執行過程中出現錯誤 (返回碼: %EXIT_CODE%)
)

echo.
pause
