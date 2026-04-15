@echo off
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo 龍魂系统·熵梦演算台 v2.0 - 一键安装脚本
echo DNA: #龍芯⚡️2026-03-10-熵梦安装器
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.

echo [1/5] 检查Python环境...
python --version
if errorlevel 1 (
    echo ❌ Python未安装！请先安装Python 3.7+
    echo 下载地址: https://www.python.org/downloads/
    pause
    exit /b
)
echo ✅ Python环境正常
echo.

echo [2/5] 升级pip...
python -m pip install --upgrade pip
echo.

echo [3/5] 安装PyQt6（UI框架）...
pip install PyQt6
echo.

echo [4/5] 安装numpy（数值计算）...
pip install numpy
echo.

echo [5/5] 安装可选功能...
echo.
echo 🎤 语音功能（推荐）
pip install pyttsx3
if errorlevel 0 (
    echo ✅ 语音功能已安装
) else (
    echo ⚠️  语音功能安装失败（可选，不影响主功能）
)
echo.

echo 🎬 录制功能（推荐）
pip install opencv-python mss
if errorlevel 0 (
    echo ✅ 录制功能已安装
) else (
    echo ⚠️  录制功能安装失败（可选，不影响主功能）
)
echo.

echo Windows语音支持（Windows系统需要）
pip install pywin32
echo.

echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo ✅ 安装完成！
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.
echo 现在可以运行程序：
echo   python shangmeng_console_v2_complete.py
echo.
echo 或者双击: 启动熵梦演算台.bat
echo.
pause
