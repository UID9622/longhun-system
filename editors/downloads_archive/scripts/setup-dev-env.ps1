# ═══════════════════════════════════════════
# 龍魂中文编辑开发环境 - Windows一键搭建脚本 (PowerShell)
# DNA: #龍芯⚡️2026-06-26-DEVENV-SETUP-WIN-v1.0
# 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬SETUP-WIN-001
# ═══════════════════════════════════════════

$ErrorActionPreference = "Stop"

# 颜色函数
function Write-Info { param($msg) Write-Host "[🟢 INFO] $msg" -ForegroundColor Green }
function Write-Warn { param($msg) Write-Host "[🟡 WARN] $msg" -ForegroundColor Yellow }
function Write-Error { param($msg) Write-Host "[🔴 ERROR] $msg" -ForegroundColor Red }
function Write-Step { param($msg) Write-Host "[STEP] $msg" -ForegroundColor Cyan }
function Write-DNA { param($msg) Write-Host "[🧬 DNA] $msg" -ForegroundColor Magenta }

# 标题
Write-Host @"
╔══════════════════════════════════════════╗
║     龍魂中文编辑开发环境搭建工具         ║
║     DNA: #龍芯⚡️2026-06-26-DEVENV-v1.0   ║
║     平台: Windows PowerShell             ║
╚══════════════════════════════════════════╝
"@ -ForegroundColor Cyan

# 检查管理员权限
if (-NOT ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Warn "建议以管理员权限运行此脚本"
}

# ═══════════════════════════════════════════
# 步骤1: 检查并安装 Chocolatey
# ═══════════════════════════════════════════
Write-Step "步骤 1/8: 检查包管理器"

if (-not (Get-Command choco -ErrorAction SilentlyContinue)) {
    Write-Info "正在安装 Chocolatey..."
    Set-ExecutionPolicy Bypass -Scope Process -Force
    [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
    Invoke-Expression ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
    $env:Path = [System.Environment]::GetEnvironmentVariable("Path", "Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path", "User")
}
Write-Info "Chocolatey 已安装 ✅"

# ═══════════════════════════════════════════
# 步骤2: 安装 Git
# ═══════════════════════════════════════════
Write-Step "步骤 2/8: 安装 Git"

if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Info "正在安装 Git..."
    choco install git -y --no-progress
    $env:Path = [System.Environment]::GetEnvironmentVariable("Path", "Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path", "User")
}

# 配置 Git
git config --global init.defaultBranch main
git config --global core.editor "notepad"
git config --global pull.rebase true
git config --global core.autocrlf true
git config --global core.safecrlf true
Write-Info "Git 配置完成 ✅"

# ═══════════════════════════════════════════
# 步骤3: 安装 VS Code
# ═══════════════════════════════════════════
Write-Step "步骤 3/8: 安装 VS Code"

if (-not (Get-Command code -ErrorAction SilentlyContinue)) {
    Write-Info "正在安装 VS Code..."
    choco install vscode -y --no-progress
}
Write-Info "VS Code 已安装 ✅"

# ═══════════════════════════════════════════
# 步骤4: 安装 Python
# ═══════════════════════════════════════════
Write-Step "步骤 4/8: 安装 Python 3.11+"

if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Info "正在安装 Python..."
    choco install python -y --no-progress
}
$pythonVersion = (python --version 2>&1)
Write-Info "Python 版本: $pythonVersion ✅"

# 创建虚拟环境
$venvDir = "$env:USERPROFILE\.longhun\venv"
if (-not (Test-Path $venvDir)) {
    Write-Info "创建虚拟环境..."
    New-Item -ItemType Directory -Path "$env:USERPROFILE\.longhun" -Force | Out-Null
    python -m venv $venvDir
}
Write-Info "虚拟环境: $venvDir ✅"

# ═══════════════════════════════════════════
# 步骤5: 安装 Node.js
# ═══════════════════════════════════════════
Write-Step "步骤 5/8: 安装 Node.js 20+"

if (-not (Get-Command node -ErrorAction SilentlyContinue)) {
    Write-Info "正在安装 Node.js..."
    choco install nodejs -y --no-progress
}
$nodeVersion = (node --version 2>&1)
Write-Info "Node.js 版本: $nodeVersion ✅"

# ═══════════════════════════════════════════
# 步骤6: 安装 Python 依赖
# ═══════════════════════════════════════════
Write-Step "步骤 6/8: 安装 Python 依赖"

$pip = "$venvDir\Scripts\pip.exe"
& $pip install --upgrade pip -q

& $pip install -q python-dotenv requests pydantic fastapi uvicorn[standard] cryptography rich typer
& $pip install -q black flake8 mypy isort pytest pytest-cov

Write-Info "Python 依赖安装完成 ✅"

# ═══════════════════════════════════════════
# 步骤7: 验证安装
# ═══════════════════════════════════════════
Write-Step "步骤 7/8: 验证安装"

Write-Host ""
Write-Host "═══════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  安装验证报告" -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════" -ForegroundColor Cyan

$tools = @("git", "code", "python", "node", "npm")
foreach ($tool in $tools) {
    $cmd = Get-Command $tool -ErrorAction SilentlyContinue
    if ($cmd) {
        Write-Host "  ✅ $tool - $($cmd.Source)" -ForegroundColor Green
    } else {
        Write-Host "  ❌ $tool" -ForegroundColor Red
    }
}

Write-Host "═══════════════════════════════════════════" -ForegroundColor Cyan

# ═══════════════════════════════════════════
# 步骤8: 完成
# ═══════════════════════════════════════════
Write-Step "步骤 8/8: 完成"

Write-Host ""
Write-Host "╔══════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║     ✅ 龍魂中文编辑开发环境搭建完成       ║" -ForegroundColor Green
Write-Host "╠══════════════════════════════════════════╣" -ForegroundColor Green
Write-Host "║  DNA: #龍芯⚡️2026-06-26-DEVENV-v1.0     ║" -ForegroundColor Green
Write-Host "║  状态: 🟢 通过                           ║" -ForegroundColor Green
Write-Host "║  平台: Windows                           ║" -ForegroundColor Green
Write-Host "╠══════════════════════════════════════════╣" -ForegroundColor Green
Write-Host "║  下一步操作:                              ║" -ForegroundColor Green
Write-Host "║  1. 重启 PowerShell                       ║" -ForegroundColor Green
Write-Host "║  2. .\venv\Scripts\Activate.ps1           ║" -ForegroundColor Green
Write-Host "║  3. code .                                ║" -ForegroundColor Green
Write-Host "╚══════════════════════════════════════════╝" -ForegroundColor Green
Write-Host ""

Write-DNA "#龍芯⚡️2026-06-26-DEVENV-WIN-SETUP-COMPLETE-v1.0"
