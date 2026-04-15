@setlocal enabledelayedexpansion
REM Set UTF-8 encoding
chcp 65001

REM Set input parameters
set ZIP_FILE=%1
echo First input parameter: %1, which is the path of plugin built .zip file, for example: "CodeElfPlugin\build\distributions\CodeArts_Doer_for_Coding_223-243_1735390420980_1e7ee3bd-103.12.1.zip"

set TEMP_DIR=.\zip_temp

:: EMPTY_DIR为空文件夹，用于通过robocopy指令覆盖zip_temp，防止zip_temp中出现超长路径导致删除失败的文件
for /f "tokens=2 delims==" %%a in ('wmic os get localdatetime /value') do set "datetime=%%a"
set "timestamp=%datetime:~0,8%_%datetime:~8,6%"
set EMPTY_DIR=.\zip_empty_%timestamp%

set ZIP_TOOL=%2
echo Second input parameter: %2, which is the path of zip tool, for example: "D:\Program Files\7-Zip\7z.exe"

set BRAND_NAME=%3
echo Third input parameter: %3, which is the target brand name, for example: HaiCode

set SRC_EN_NAME=CodeArts Agent
set SRC_ZH_NAME=CodeArts代码智能体

REM Check if files exist
if not exist %ZIP_FILE% (
    echo ZIP file not found: %ZIP_FILE%
    goto :eof
)

if not exist %ZIP_TOOL% (
    echo Zip tool not found: %ZIP_TOOL%
    goto :eof
)

rem check file extension
set "ext=%ZIP_FILE:~-4%"
if "%ext%"==".zip" (
    echo file %ZIP_FILE% is end with .zip
) else (
    echo file %ZIP_FILE% invalid because file is not end with .zip.
    goto :eof
)

REM get unzip dir
:: get zip file name
for %%i in (%ZIP_FILE%) do set "ZIP_FILE_NAME=%%~nxi"
echo ZIP_FILE_NAME: %ZIP_FILE_NAME% 
:: 获取字符串的长度
set len=0
set tmpName=!ZIP_FILE_NAME!
:loop
if not "!tmpName!"=="" (
    set "tmpName=!tmpName:~1!"
    set /a len+=1
    goto :loop
)

:: 反向查找最后一个 "-"
for /l %%i in (!len!,-1,0) do (
    echo ZIP_FILE_NAME: %ZIP_FILE_NAME% 
    set char=!ZIP_FILE_NAME:~%%i,1!
    if "!char!"=="-" (
        set last_dash=%%i
        goto :found
    )
)
:found
:: 截取最后一个 "-" 之前的所有字符
REM CodeArts_Snap_223-243_1735390420980_1e7ee3bd\lib
set SUB_DIR=!ZIP_FILE_NAME:~0,%last_dash%!\lib
set VERSION=!ZIP_FILE_NAME:~%last_dash%,-4!
set TEMP_SUFFIX=

REM Clean and create temporary directory
if exist "%TEMP_DIR%" (rmdir /s /q %TEMP_DIR%)
mkdir %TEMP_DIR%

mkdir %EMPTY_DIR%

REM Extract ZIP file to temporary directory
%ZIP_TOOL% x "%ZIP_FILE%" -o%TEMP_DIR%
REM Extract JAR file to temporary directory
:: init array
setlocal enabledelayedexpansion
set index=3
set JAR_NAME[0]=CodeElfCommon
set JAR_NAME[1]=CodeChat
set JAR_NAME[2]=CodeElfPlugin%VERSION%
set JAR_NAME[3]=Toolkit
:: extract all target jar file
for /L %%i in (0, 1, %index%) do (

    set TARGET_JAR=%TEMP_DIR%\%SUB_DIR%\!JAR_NAME[%%i]!.jar
    set JAR_TEMP_DIR=%TEMP_DIR%\%SUB_DIR%\!JAR_NAME[%%i]!%TEMP_SUFFIX%
    echo target jar path: !TARGET_JAR! 
    echo unzip jar dir path:  !JAR_TEMP_DIR!
    
    if exist "!JAR_TEMP_DIR!" (rmdir /s /q !JAR_TEMP_DIR!)
    mkdir !JAR_TEMP_DIR!

    %ZIP_TOOL% x !TARGET_JAR! -o!JAR_TEMP_DIR!
)

REM Haier need to hide advisor, complaint, and disclaimer links
set SWITCH_FILE=%TEMP_DIR%\%SUB_DIR%\%JAR_NAME[0]%%TEMP_SUFFIX%\env_version.properties
if exist "%SWITCH_FILE%" (
    powershell -Command "(Get-Content '%SWITCH_FILE%' -Encoding UTF8) -replace 'hideAdvisorEntry:false', 'hideAdvisorEntry:true' | Set-Content %SWITCH_FILE% -Encoding UTF8"
    powershell -Command "(Get-Content '%SWITCH_FILE%' -Encoding UTF8) -replace 'hideComplaintEntry:false', 'hideComplaintEntry:true' | Set-Content %SWITCH_FILE% -Encoding UTF8"
    powershell -Command "(Get-Content '%SWITCH_FILE%' -Encoding UTF8) -replace 'hideDisclaimerLinkEntry:false', 'hideDisclaimerLinkEntry:true' | Set-Content %SWITCH_FILE% -Encoding UTF8"
    powershell -Command "(Get-Content '%SWITCH_FILE%' -Encoding UTF8) -replace 'projectLevelRootName=.*', 'projectLevelRootName=.%BRAND_NAME%' | Set-Content %SWITCH_FILE% -Encoding UTF8"
) else (
    echo File not found: %SWITCH_FILE%
    goto :eof
)

set COMMON_BUNDLE_FILE=%TEMP_DIR%\%SUB_DIR%\%JAR_NAME[0]%%TEMP_SUFFIX%\CommonBundle.properties
set I18N_BUNDLE_EN_FILE=%TEMP_DIR%\%SUB_DIR%\%JAR_NAME[0]%%TEMP_SUFFIX%\messages\I18nBundle_en.properties
set I18N_BUNDLE_ZH_FILE=%TEMP_DIR%\%SUB_DIR%\%JAR_NAME[0]%%TEMP_SUFFIX%\messages\I18nBundle_zh.properties
if exist "%COMMON_BUNDLE_FILE%" (
    powershell -Command "(Get-Content '%COMMON_BUNDLE_FILE%' -Encoding UTF8) -replace 'custom.plugin.name=', 'custom.plugin.name=%BRAND_NAME%' | Set-Content %COMMON_BUNDLE_FILE% -Encoding UTF8"
    powershell -Command "(Get-Content '%COMMON_BUNDLE_FILE%' -Encoding UTF8) -replace 'logStorageDays=.*', 'logStorageDays=180' | Set-Content %COMMON_BUNDLE_FILE% -Encoding UTF8"
    powershell -Command "(Get-Content '%COMMON_BUNDLE_FILE%' -Encoding UTF8) -replace 'logStorageSize=.*', 'logStorageSize=3600' | Set-Content %COMMON_BUNDLE_FILE% -Encoding UTF8"
) else (
    echo File not found: %COMMON_BUNDLE_FILE%
    goto :eof
)
if exist "%I18N_BUNDLE_EN_FILE%" (
    powershell -Command "(Get-Content '%I18N_BUNDLE_EN_FILE%' -Encoding UTF8) -replace 'hc.plugin.name=%SRC_EN_NAME%', 'hc.plugin.name=%BRAND_NAME%' | Set-Content %I18N_BUNDLE_EN_FILE% -Encoding UTF8"
) else (
    echo File not found: %I18N_BUNDLE_EN_FILE%
    goto :eof
)
if exist "%I18N_BUNDLE_ZH_FILE%" (
    powershell -Command "(Get-Content '%I18N_BUNDLE_ZH_FILE%' -Encoding UTF8) -replace 'hc.plugin.name=%SRC_ZH_NAME%', 'hc.plugin.name=%BRAND_NAME%' | Set-Content %I18N_BUNDLE_ZH_FILE% -Encoding UTF8"
) else (
    echo File not found: %I18N_BUNDLE_ZH_FILE%
    goto :eof
)


REM Replace brand name in files
for %%f in (
    %TEMP_DIR%\%SUB_DIR%\!JAR_NAME[0]!%TEMP_SUFFIX%\META-INF\common-extension.xml
    %TEMP_DIR%\%SUB_DIR%\!JAR_NAME[0]!%TEMP_SUFFIX%\CommonBundle.properties
    %TEMP_DIR%\%SUB_DIR%\!JAR_NAME[1]!%TEMP_SUFFIX%\META-INF\code-chat-extension.xml
    %TEMP_DIR%\%SUB_DIR%\!JAR_NAME[1]!%TEMP_SUFFIX%\promptGPTs\en\defaultGPTsList.json
    %TEMP_DIR%\%SUB_DIR%\!JAR_NAME[1]!%TEMP_SUFFIX%\promptGPTs\zh\defaultGPTsList.json
    %TEMP_DIR%\%SUB_DIR%\!JAR_NAME[1]!%TEMP_SUFFIX%\i18n\codespirit.properties
    %TEMP_DIR%\%SUB_DIR%\!JAR_NAME[1]!%TEMP_SUFFIX%\i18n\codespirit_zh.properties
    %TEMP_DIR%\%SUB_DIR%\!JAR_NAME[2]!%TEMP_SUFFIX%\META-INF\plugin.xml
    %TEMP_DIR%\%SUB_DIR%\!JAR_NAME[3]!%TEMP_SUFFIX%\config.properties
    %TEMP_DIR%\%SUB_DIR%\!JAR_NAME[3]!%TEMP_SUFFIX%\messages\SwingText.properties
    %TEMP_DIR%\%SUB_DIR%\!JAR_NAME[3]!%TEMP_SUFFIX%\messages\SwingText_en_US.properties
    %TEMP_DIR%\%SUB_DIR%\!JAR_NAME[3]!%TEMP_SUFFIX%\messages\SwingText_zh_CN.properties

) do (
    echo current file path: %%f
    if exist "%%f" (
        powershell -Command "(Get-Content '%%f' -Encoding UTF8) -replace '%SRC_EN_NAME%', '%BRAND_NAME%' | Set-Content '%%f' -Encoding UTF8"
        powershell -Command "(Get-Content '%%f' -Encoding UTF8) -replace '%SRC_ZH_NAME%', '%BRAND_NAME%' | Set-Content '%%f' -Encoding UTF8"
    ) else (
        echo File not found: %%f
        goto :eof
    )
)

REM Use PowerShell to remove BOM from files
powershell -Command ^
"^
$files = @(^
    '%TEMP_DIR%\%SUB_DIR%\!JAR_NAME[0]!%TEMP_SUFFIX%\META-INF\common-extension.xml',^
    '%TEMP_DIR%\%SUB_DIR%\!JAR_NAME[0]!%TEMP_SUFFIX%\CommonBundle.properties',^
    '%TEMP_DIR%\%SUB_DIR%\!JAR_NAME[1]!%TEMP_SUFFIX%\META-INF\code-chat-extension.xml',^
    '%TEMP_DIR%\%SUB_DIR%\!JAR_NAME[1]!%TEMP_SUFFIX%\promptGPTs\en\defaultGPTsList.json',^
    '%TEMP_DIR%\%SUB_DIR%\!JAR_NAME[1]!%TEMP_SUFFIX%\promptGPTs\zh\defaultGPTsList.json',^
    '%TEMP_DIR%\%SUB_DIR%\!JAR_NAME[1]!%TEMP_SUFFIX%\i18n\codespirit.properties',^
    '%TEMP_DIR%\%SUB_DIR%\!JAR_NAME[1]!%TEMP_SUFFIX%\i18n\codespirit_zh.properties',^
    '%TEMP_DIR%\%SUB_DIR%\!JAR_NAME[2]!%TEMP_SUFFIX%\META-INF\plugin.xml',^
    '%TEMP_DIR%\%SUB_DIR%\!JAR_NAME[3]!%TEMP_SUFFIX%\config.properties',^
    '%TEMP_DIR%\%SUB_DIR%\!JAR_NAME[3]!%TEMP_SUFFIX%\messages\SwingText.properties',^
    '%TEMP_DIR%\%SUB_DIR%\!JAR_NAME[3]!%TEMP_SUFFIX%\messages\SwingText_en_US.properties',^
    '%TEMP_DIR%\%SUB_DIR%\!JAR_NAME[3]!%TEMP_SUFFIX%\messages\SwingText_zh_CN.properties'^
    ); ^
foreach ($file in $files) { ^
    $content = Get-Content -Path $file -Encoding Byte; ^
    if ($content.Length -gt 3 -and $content[0] -eq 0xEF -and $content[1] -eq 0xBB -and $content[2] -eq 0xBF) { ^
        $content = $content[3..($content.Length-1)]; ^
        [System.IO.File]::WriteAllBytes($file, $content); ^
    } ^
} ^
"

REM Copy custom image files
set CUSTOM_IMG_DIR=%TEMP_DIR%\%SUB_DIR%\!JAR_NAME[1]!%TEMP_SUFFIX%\webview\custom-img\
set CUSTOM_ICONS_DIR=%TEMP_DIR%\%SUB_DIR%\!JAR_NAME[0]!%TEMP_SUFFIX%\icons
set CUSTOM_ICONS_DARK_DIR=%TEMP_DIR%\%SUB_DIR%\!JAR_NAME[0]!%TEMP_SUFFIX%\icons\dark
set CUSTOM_ICONS_LIGHT_DIR=%TEMP_DIR%\%SUB_DIR%\!JAR_NAME[0]!%TEMP_SUFFIX%\icons\light
for %%f in (
    %CUSTOM_IMG_DIR%
    %CUSTOM_ICONS_DIR%
    %CUSTOM_ICONS_DARK_DIR%
    %CUSTOM_ICONS_LIGHT_DIR%
) do (
    echo current file path: %%f
    if exist "%%f" (
        rmdir /s /q %%f
    )
    mkdir %%f
)

set COMMON_ICON_FILE=%TEMP_DIR%\%SUB_DIR%\!JAR_NAME[0]!%TEMP_SUFFIX%\META-INF\pluginIcon.svg
set PLUGIN_ICON_FILE=%TEMP_DIR%\%SUB_DIR%\!JAR_NAME[1]!%TEMP_SUFFIX%\META-INF\pluginIcon.svg
set TOOLKIT_ICON_FILE=%TEMP_DIR%\%SUB_DIR%\!JAR_NAME[3]!%TEMP_SUFFIX%\icons\logo.png
set TOOLKIT_HCS_ICON_FILE=%TEMP_DIR%\%SUB_DIR%\!JAR_NAME[3]!%TEMP_SUFFIX%\icons\hcs-logo.png

copy .\custom-logo\custom-img\logo.png %CUSTOM_IMG_DIR%
copy .\custom-logo\custom-img\posters.png %CUSTOM_IMG_DIR%
copy .\custom-logo\logo.svg %CUSTOM_ICONS_DIR%\logo.svg
copy .\custom-logo\logo_12px.svg %CUSTOM_ICONS_DIR%\logo_12px.svg
copy .\custom-logo\dark\login.svg %CUSTOM_ICONS_DARK_DIR%\login.svg
copy .\custom-logo\dark\logout.svg %CUSTOM_ICONS_DARK_DIR%\logout.svg
copy .\custom-logo\light\login.svg %CUSTOM_ICONS_LIGHT_DIR%\login.svg
copy .\custom-logo\light\logout.svg %CUSTOM_ICONS_LIGHT_DIR%\logout.svg
copy .\custom-logo\logo.svg %COMMON_ICON_FILE%
copy .\custom-logo\logo.svg %PLUGIN_ICON_FILE%
copy .\custom-logo\custom-img\logo.png %TOOLKIT_ICON_FILE%
copy .\custom-logo\custom-img\logo.png %TOOLKIT_HCS_ICON_FILE%

REM Create jar && Clean up temporary directory
for /L %%i in (0, 1, %index%) do (
    set TARGET_JAR=%TEMP_DIR%\%SUB_DIR%\!JAR_NAME[%%i]!.jar
    set JAR_TEMP_DIR=%TEMP_DIR%\%SUB_DIR%\!JAR_NAME[%%i]!%TEMP_SUFFIX%
    echo target jar path: !TARGET_JAR! 
    echo unzip jar dir path:  !JAR_TEMP_DIR!

    del /f /q !TARGET_JAR!
    %ZIP_TOOL% a -tzip !TARGET_JAR! !JAR_TEMP_DIR!\* -r

    robocopy %EMPTY_DIR% !JAR_TEMP_DIR! /mir
    rmdir /s /q !JAR_TEMP_DIR!
)

set OUTPUT_DIR=.\new_extension
REM Clean and create output directory
if exist "%OUTPUT_DIR%" (rmdir /s /q %OUTPUT_DIR%)
mkdir %OUTPUT_DIR%

REM Create new ZIP file

for %%F in ("%ZIP_FILE%") do set "FILE_NAME=%%~nxF"
echo extension file name is: %FILE_NAME%

%ZIP_TOOL% a -tzip %OUTPUT_DIR%\%FILE_NAME% %TEMP_DIR%\* -r

REM Clean up temporary directory
robocopy %EMPTY_DIR% %TEMP_DIR% /mir
rmdir /s /q %TEMP_DIR%
rmdir /s /q %EMPTY_DIR%

echo Modification complete, new .zip file located at %OUTPUT_DIR%/%FILE_NAME%
