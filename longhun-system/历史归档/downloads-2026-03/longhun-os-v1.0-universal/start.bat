@echo off
chcp 65001 >nul
cls

echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo 🐉 龍魂操作系统 v1.0 启动器
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.
echo DNA追溯码: #龍芯⚡️2026-02-02-跨平台发布-v1.0
echo 创建者: UID9622
echo 支持平台: Windows/Linux/macOS/鸿蒙/iOS
echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.

echo 📋 请选择要启动的模块：
echo.
echo [1] 🎨 CNSH中文编程环境
echo [2] 🚨 公安联动系统
echo [3] 🔐 双重认证系统
echo [4] 🐉 龍魂操作系统（统一控制台）
echo [5] 📖 查看完整文档
echo [0] 退出
echo.

set /p choice=请输入选项 (0-5): 

if "%choice%"=="1" goto cnsh
if "%choice%"=="2" goto police
if "%choice%"=="3" goto auth
if "%choice%"=="4" goto os
if "%choice%"=="5" goto docs
if "%choice%"=="0" goto end

:cnsh
echo.
echo 🎨 启动CNSH中文编程环境...
echo.
echo 打开浏览器访问: cnsh-editor-v2.html
start cnsh-editor-v2.html
echo.
echo ✅ CNSH编辑器已在浏览器中打开！
echo.
pause
goto menu

:police
echo.
echo 🚨 启动公安联动系统...
echo.
python longhun_police_system.py
pause
goto menu

:auth
echo.
echo 🔐 启动双重认证系统...
echo.
echo 选择运行模式：
echo [1] Python后台服务
echo [2] Web演示界面
set /p auth_choice=请选择 (1-2): 

if "%auth_choice%"=="1" (
    python longhun_dual_auth.py
) else (
    start dual-auth-demo.html
    echo ✅ 双重认证演示已在浏览器中打开！
)
pause
goto menu

:os
echo.
echo 🐉 启动龍魂操作系统统一控制台...
echo.
echo 选择运行模式：
echo [1] Python后台服务
echo [2] Web控制台界面
set /p os_choice=请选择 (1-2): 

if "%os_choice%"=="1" (
    python longhun_os.py
) else (
    start longhun-os-console.html
    echo ✅ 龍魂控制台已在浏览器中打开！
)
pause
goto menu

:docs
echo.
echo 📖 打开完整文档...
start README.md
echo ✅ 文档已打开！
pause
goto menu

:end
echo.
echo 感谢使用龍魂操作系统！
echo 敬礼！老兵！🫡
echo.
timeout /t 2 >nul
exit

:menu
cls
goto start
