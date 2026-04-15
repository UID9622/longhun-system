@echo off
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo 🐉 龍魂系统·熵梦演算台 v2.0
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.
echo 正在启动...
echo.

python shangmeng_console_v2_complete.py

if errorlevel 1 (
    echo.
    echo ❌ 启动失败！
    echo.
    echo 可能原因：
    echo   1. Python未安装
    echo   2. 依赖库未安装
    echo.
    echo 解决方案：
    echo   双击运行: install_shangmeng.bat
    echo.
    pause
)
