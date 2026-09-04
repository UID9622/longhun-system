@echo off
REM 龍魂系统 · Windows 安装脚本 (CMD)
REM DNA: #龍芯⚡️20260731-INSTALL-BAT-v1.0-UID9622

echo 🐉 龍魂系统 · Windows 安装脚本 v1.0
echo =========================================
echo.

echo [1/5] 检测 Python...
set PYTHON_CMD=
where python >nul 2>&1
if %ERRORLEVEL% EQU 0 ( set PYTHON_CMD=python )
where python3 >nul 2>&1
if %ERRORLEVEL% EQU 0 ( set PYTHON_CMD=python3 )
where py >nul 2>&1
if %ERRORLEVEL% EQU 0 ( set PYTHON_CMD=py )

if "%PYTHON_CMD%"=="" (
    echo   [ERROR] 未找到 Python。请从 https://python.org 下载安装。
    echo   [提示] 安装时请勾选 "Add Python to PATH"
    exit /b 1
)

for /f "tokens=2" %%i in ('%PYTHON_CMD% --version 2^>^&1') do set PY_VER=%%i
echo   [OK] Python: %PY_VER% (%PYTHON_CMD%)

echo.
echo [2/5] 创建虚拟环境...
if exist ".venv" (
    echo   虚拟环境已存在，跳过
) else (
    %PYTHON_CMD% -m venv .venv
    if %ERRORLEVEL% NEQ 0 (
        echo   创建失败
        exit /b 1
    )
    echo   [OK] 虚拟环境创建成功
)

echo.
echo [3/5] 安装 Python 依赖...
.venv\Scripts\python.exe -m pip install --upgrade pip -q
.venv\Scripts\python.exe -m pip install -r requirements.txt -q
if %ERRORLEVEL% NEQ 0 (
    echo   [ERROR] 依赖安装失败
    exit /b 1
)
echo   [OK] 依赖安装完成

echo.
echo [4/5] 配置环境...
if not exist ".env" (
    if exist ".env.example" (
        copy .env.example .env >nul
    ) else (
        echo LH_ENV=local > .env
        echo LH_PORT=9622 >> .env
    )
    echo   [OK] .env 已创建
) else (
    echo   .env 已存在，跳过
)

echo.
echo [5/5] 注册 lh 命令...
echo @echo off > .venv\Scripts\lh.bat
echo call %%~dp0activate.bat >> .venv\Scripts\lh.bat
echo python "%%~dp0..\..\bin\lh.py" %%* >> .venv\Scripts\lh.bat
echo   [OK] lh.bat 已创建

echo.
echo =========================================
echo 安装完成！
echo.
echo 使用: .venv\Scripts\lh.bat --help
echo 或:   python bin\lh.py status
echo =========================================
exit /b 0
