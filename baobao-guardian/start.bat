@echo off
REM 龍魂宝宝守护助手 · 一键启动脚本 (Windows)
REM DNA:#龍芯⚡️2026-06-04-START-SCRIPT-WINDOWS-v1.0

setlocal enabledelayedexpansion

echo.
echo ╔════════════════════════════════════════════════════╗
echo ║  🐉 龍魂宝宝守护助手启动器 v1.0                  ║
echo ║  UID9622 · 诸葛鑫 · 龍芯北辰                     ║
echo ╚════════════════════════════════════════════════════╝
echo.

setlocal
set PROJECT_ROOT=%~dp0
set FRONTEND_DIR=%PROJECT_ROOT%frontend
set BACKEND_DIR=%PROJECT_ROOT%backend

echo 📁 项目目录: %PROJECT_ROOT%
echo.

REM ═══════════════════════════════════════════════════════════
REM 检查环境
REM ═══════════════════════════════════════════════════════════

echo 🔍 检查环境...

where node >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Node.js 未安装，请先安装 Node.js 18+
    pause
    exit /b 1
)

where python >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Python 3 未安装，请先安装 Python 3.11+
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('node --version') do set NODE_VERSION=%%i
for /f "tokens=*" %%i in ('python --version') do set PYTHON_VERSION=%%i

echo ✅ Node.js 版本: %NODE_VERSION%
echo ✅ Python 版本: %PYTHON_VERSION%
echo.

REM ═══════════════════════════════════════════════════════════
REM 启动后端
REM ═══════════════════════════════════════════════════════════

echo 🚀 启动后端服务...

cd /d "%BACKEND_DIR%"

REM 检查虚拟环境
if not exist "venv" (
    echo 📦 创建 Python 虚拟环境...
    python -m venv venv
)

REM 激活虚拟环境
call venv\Scripts\activate.bat

REM 安装依赖
echo 📦 安装 Python 依赖...
pip install -q -r requirements.txt

echo ✅ 后端环境就绪
echo.

REM 在新窗口启动后端
echo 🔥 启动 FastAPI 服务器...
start "龍魂后端 - FastAPI" python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

timeout /t 2 /nobreak

echo ✅ 后端已启动
echo    访问地址: http://localhost:8000
echo    WebSocket: ws://localhost:8000/ws/overlay
echo.

REM ═══════════════════════════════════════════════════════════
REM 启动前端
REM ═══════════════════════════════════════════════════════════

echo 🚀 启动前端开发服务器...

cd /d "%FRONTEND_DIR%"

REM 检查依赖
if not exist "node_modules" (
    echo 📦 安装 npm 依赖...
    call npm install
)

echo ✅ 前端环境就绪
echo.

REM 在新窗口启动前端
echo 🔥 启动 Vite 开发服务器...
start "龍魂前端 - React" cmd /k npm run dev

REM ═══════════════════════════════════════════════════════════
REM 启动完成
REM ═══════════════════════════════════════════════════════════

echo.
echo ╔════════════════════════════════════════════════════╗
echo ║  ✅ 龍魂宝宝守护助手已启动！                      ║
echo ╚════════════════════════════════════════════════════╝
echo.
echo 📖 快速链接:
echo    🌐 前端应用: http://localhost:5173
echo    🔗 API 文档: http://localhost:8000/docs
echo    📊 健康检查: http://localhost:8000/health
echo.
echo 💡 提示: 关闭任意窗口即可停止相应服务
echo.

pause
