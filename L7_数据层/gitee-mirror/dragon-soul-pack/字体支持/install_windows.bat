@echo off
REM DNA追溯码:#龍芯⚡️2026-06-22-LONGHUN-FONT-INSTALL-WINDOWS-v1.0
REM
REM LonghunFont Windows installer
REM 将 LonghunFont-Regular.otf 安装到 Windows 系统字体目录。
REM
REM 用法：
REM   1. 在文件资源管理器中右键点击本脚本，选择“以管理员身份运行”。
REM   2. 或者在命令提示符（CMD）中以管理员权限执行：
REM        install_windows.bat
REM
REM 注意：
REM   - 安装字体需要管理员权限，否则会复制失败。
REM   - 安装完成后建议注销并重新登录，或重启部分应用程序以加载新字体。

chcp 65001 >nul 2>&1

setlocal enabledelayedexpansion

set "FONT_NAME=LonghunFont-Regular.otf"
set "FONT_SOURCE=%~dp0output\%FONT_NAME%"
set "FONT_TARGET=C:\Windows\Fonts\%FONT_NAME%"

REM 1. 操作系统检查
if /I not "%OS%"=="Windows_NT" (
    echo [错误] 本安装脚本仅适用于 Windows 系统。
    pause
    exit /b 1
)

REM 2. 字体文件检查
if not exist "%FONT_SOURCE%" (
    echo [错误] 未找到字体文件：%FONT_SOURCE%
    echo [提示] 请确保 output\%FONT_NAME% 与本脚本位于同一目录下。
    pause
    exit /b 1
)

REM 3. 复制字体到系统字体目录
copy /Y "%FONT_SOURCE%" "%FONT_TARGET%" >nul
if errorlevel 1 (
    echo [错误] 字体安装失败，无法复制到 %FONT_TARGET%。
    echo [提示] 请确认您已使用管理员身份运行此脚本。
    pause
    exit /b 1
)

echo.
echo [成功] 龍魂字体 %FONT_NAME% 已安装到 Windows 字体目录。
echo [提示] 若字体未立即生效，请注销并重新登录或重启应用程序。
echo DNA追溯码:#龍芯⚡️2026-06-22-LONGHUN-FONT-INSTALL-WINDOWS-v1.0

pause
exit /b 0
