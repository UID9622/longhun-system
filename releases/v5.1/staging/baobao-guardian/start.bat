@echo off
REM 龍魂宝宝守護助手 · 一鍵啟動腳本 (Windows)
REM DNA:#龍芯⚡️2026-06-04-START-SCRIPT-WINDOWS-FILE1-v1.0

setlocal enabledelayedexpansion

echo.
echo ╔════════════════════════════════════════════════════╗
echo ║  🐉 龍魂宝宝守護助手啟動器 v1.0                  ║
echo ║  UID9622 · 諸葛鑫 · 龍芯北辰                     ║
echo ╚════════════════════════════════════════════════════╝
echo.

setlocal
set PROJECT_ROOT=%~dp0
set FRONTEND_DIR=%PROJECT_ROOT%frontend
set BACKEND_DIR=%PROJECT_ROOT%backend

echo 📁 項目目錄: %PROJECT_ROOT%
echo.

REM ═══════════════════════════════════════════════════════════
REM 檢查環境
REM ═══════════════════════════════════════════════════════════

echo 🔍 檢查環境...

where node >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Node.js 未安裝，請先安裝 Node.js 18+
    pause
    exit /b 1
)

where python >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Python 3 未安裝，請先安裝 Python 3.11+
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('node --version') do set NODE_VERSION=%%i
for /f "tokens=*" %%i in ('python --version') do set PYTHON_VERSION=%%i

echo ✅ Node.js 版本: %NODE_VERSION%
echo ✅ Python 版本: %PYTHON_VERSION%
echo.

REM ═══════════════════════════════════════════════════════════
REM 啟動後端
REM ═══════════════════════════════════════════════════════════

echo 🚀 啟動後端服務...

cd /d "%BACKEND_DIR%"

REM 檢查虛擬環境
if not exist "venv" (
    echo 📦 創建 Python 虛擬環境...
    python -m venv venv
)

REM 激活虛擬環境
call venv\Scripts\activate.bat

REM 安裝依賴
echo 📦 安裝 Python 依賴...
pip install -q -r requirements.txt

echo ✅ 後端環境就緒
echo.

REM 在新窗口啟動後端
echo 🔥 啟動 FastAPI 服務器...
start "龍魂後端 - FastAPI" python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

timeout /t 2 /nobreak

echo ✅ 後端已啟動
echo    訪問地址: http://localhost:8000
echo    WebSocket: ws://localhost:8000/ws/overlay
echo.

REM ═══════════════════════════════════════════════════════════
REM 啟動前端
REM ═══════════════════════════════════════════════════════════

echo 🚀 啟動前端開發服務器...

cd /d "%FRONTEND_DIR%"

REM 檢查依賴
if not exist "node_modules" (
    echo 📦 安裝 npm 依賴...
    call npm install
)

echo ✅ 前端環境就緒
echo.

REM 在新窗口啟動前端
echo 🔥 啟動 Vite 開發服務器...
start "龍魂前端 - React" cmd /k npm run dev

REM ═══════════════════════════════════════════════════════════
REM 啟動完成
REM ═══════════════════════════════════════════════════════════

echo.
echo ╔════════════════════════════════════════════════════╗
echo ║  ✅ 龍魂宝宝守護助手已啟動！                      ║
echo ╚════════════════════════════════════════════════════╝
echo.
echo 📖 快速鏈接:
echo    🌐 前端應用: http://localhost:5173
echo    🔗 API 文檔: http://localhost:8000/docs
echo    📊 健康檢查: http://localhost:8000/health
echo.
echo 💡 提示: 關閉任意窗口即可停止相應服務
echo.

pause
