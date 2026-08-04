# 龍魂系统 · Windows 安装脚本 (PowerShell)
# DNA: #龍芯⚡️20260731-INSTALL-PS-v1.0-UID9622
# 使用: 以管理员身份运行 PowerShell，执行 .\bin\install.ps1

Write-Host "🐉 龍魂系统 · Windows 安装脚本 v1.0" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

# 检查 Python
Write-Host "[1/5] 检测 Python..." -ForegroundColor Yellow
$pythonCmd = $null
foreach ($cmd in @("python", "python3", "py")) {
    try {
        $v = & $cmd --version 2>$null
        if ($v -match "3\.(\d+)" -and [int]$Matches[1] -ge 11) {
            $pythonCmd = $cmd
            Write-Host "  ✅ Python: $v ($cmd)" -ForegroundColor Green
            break
        } elseif ($v) {
            Write-Host "  ❌ Python 版本过低: $v (需要 >= 3.11)" -ForegroundColor Red
        }
    } catch {}
}
if (-not $pythonCmd) {
    Write-Host "  ❌ 未找到 Python 3.11+。请从 https://python.org 下载安装。" -ForegroundColor Red
    Write-Host "  💡 安装时请勾选 'Add Python to PATH'" -ForegroundColor Yellow
    exit 1
}

# 创建虚拟环境
Write-Host "[2/5] 创建虚拟环境..." -ForegroundColor Yellow
if (Test-Path ".venv") {
    Write-Host "  ⚠️  .venv 已存在，跳过" -ForegroundColor Yellow
} else {
    & $pythonCmd -m venv .venv
    if ($LASTEXITCODE -ne 0) {
        Write-Host "  ❌ 虚拟环境创建失败" -ForegroundColor Red
        exit 1
    }
    Write-Host "  ✅ 虚拟环境创建成功" -ForegroundColor Green
}

# 激活并安装依赖
Write-Host "[3/5] 安装 Python 依赖..." -ForegroundColor Yellow
$venvPython = ".\.venv\Scripts\python.exe"
try {
    & $venvPython -m pip install --upgrade pip -q
    & $venvPython -m pip install -r requirements.txt -q
    Write-Host "  ✅ 依赖安装完成" -ForegroundColor Green
} catch {
    Write-Host "  ❌ 依赖安装失败: $_" -ForegroundColor Red
    exit 1
}

# 配置 .env
Write-Host "[4/5] 配置环境..." -ForegroundColor Yellow
if (-not (Test-Path ".env")) {
    if (Test-Path ".env.example") {
        Copy-Item ".env.example" ".env"
        Write-Host "  ✅ .env 已从模板创建，请根据需要编辑" -ForegroundColor Green
    } else {
        @"
# 龍魂系统 · 环境配置
# 编辑后保存
LH_ENV=local
LH_PORT=9622
"@ | Out-File -FilePath ".env" -Encoding utf8
        Write-Host "  ✅ .env 已创建默认配置" -ForegroundColor Green
    }
} else {
    Write-Host "  ⚠️  .env 已存在，跳过" -ForegroundColor Yellow
}

# 设置 lh 命令
Write-Host "[5/5] 注册 lh 命令..." -ForegroundColor Yellow
$lhScript = @"
@echo off
call .\.venv\Scripts\activate.bat
python "%~dp0..\bin\lh.py" %*
"@
$lhScriptPath = ".venv\Scripts\lh.bat"
$lhScript | Out-File -FilePath $lhScriptPath -Encoding ascii
Write-Host "  ✅ lh.bat 已创建" -ForegroundColor Green
Write-Host "  💡 使用: .venv\Scripts\lh.bat --help" -ForegroundColor Yellow
Write-Host "  💡 或直接: python bin\lh.py --help" -ForegroundColor Yellow

# 最终验证
Write-Host ""
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "🐉 安装完成！" -ForegroundColor Green
Write-Host ""
Write-Host "快速验证:" -ForegroundColor White
Write-Host "  .venv\Scripts\lh.bat --help" -ForegroundColor Yellow
Write-Host "  python bin\lh.py status" -ForegroundColor Yellow
Write-Host ""
Write-Host "启动API服务:" -ForegroundColor White
Write-Host "  python bin\lh_api_server.py --port 9622" -ForegroundColor Yellow
Write-Host ""
Write-Host "文档: INSTALL.md" -ForegroundColor White
Write-Host "=========================================" -ForegroundColor Cyan
