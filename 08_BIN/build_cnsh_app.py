#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·丙酉·癸亥·巳时·䷫姤-CNSH-IDE-BUILD-v1.0-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""
🐉 CNSH IDE 打包脚本

用法:
  python3 08_BIN/build_cnsh_app.py
  python3 08_BIN/build_cnsh_app.py --onefile
  python3 08_BIN/build_cnsh_app.py --target macos_app
  python3 08_BIN/build_cnsh_app.py --target windows_exe

输出:
  dist/CNSH_IDE/          # 单目录分发
  dist/CNSH_IDE.app/      # macOS .app (默认)
  dist/CNSH_IDE.exe       # Windows 单文件 (需 Windows 环境)
"""

import os
import sys
import json
import shutil
import subprocess
import argparse
import platform
from pathlib import Path
from datetime import datetime

# ═══════════════════════════════════════════════════════
# 配置
# ═══════════════════════════════════════════════════════
ROOT = Path(__file__).resolve().parent.parent
BIN_DIR = ROOT / "08_BIN"
BUILD_DIR = ROOT / "build_ide"
DIST_DIR = ROOT / "dist_ide"
VENV_DIR = BUILD_DIR / "venv"

APP_NAME = "CNSH IDE"
APP_VERSION = "1.0.0"
ENTRY_SCRIPT = BIN_DIR / "cnsh_web_ide.py"

REQUIRED_PACKAGES = [
    "fastapi>=0.100",
    "uvicorn[standard]>=0.23",
    "requests>=2.31.0",
    "pyinstaller>=6.0",
]

# 必须打包的引擎模块（与 cnsh_web_ide.py 同目录）
HIDDEN_IMPORTS = [
    "cnsh_editor",
    "cnsh_compiler",
    "cnsh_ui",
    "cnsh_complete",
    "cnsh_interpreter",
    "cnsh_gateway",
    "cnsh_ai_providers",
    "cnsh_bagua_router",
    "lh_agent_cosmos",
]

# ═══════════════════════════════════════════════════════
# 工具函数
# ═══════════════════════════════════════════════════════
def run(cmd, cwd=None, check=True):
    print(f"$ {' '.join(str(c) for c in cmd)}")
    result = subprocess.run(cmd, cwd=cwd, check=check, text=True, capture_output=True)
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)
    return result


def python_in_venv() -> Path:
    """返回 venv 中的 python 可执行文件路径"""
    if sys.platform == "win32":
        return VENV_DIR / "Scripts" / "python.exe"
    return VENV_DIR / "bin" / "python3"


def ensure_venv():
    """创建隔离构建环境"""
    if VENV_DIR.exists():
        print(f"⚠️ 发现已有 venv，将复用: {VENV_DIR}")
    else:
        print(f"📦 创建构建虚拟环境: {VENV_DIR}")
        run([sys.executable, "-m", "venv", str(VENV_DIR)])

    py = python_in_venv()
    print("⬆️ 升级 pip 并安装依赖...")
    run([str(py), "-m", "pip", "install", "--upgrade", "pip"])
    run([str(py), "-m", "pip", "install"] + REQUIRED_PACKAGES)


def collect_pyinstaller_args(target: str, onefile: bool) -> list:
    """生成 PyInstaller 参数"""
    py = python_in_venv()
    # 静态资源（Ace Editor 等）需要打包进应用
    separator = ";" if sys.platform == "win32" else ":"
    static_data = f"--add-data={ROOT / 'static'}{separator}static"

    args = [
        str(py), "-m", "PyInstaller",
        "--noconfirm",
        "--clean",
        f"--name={APP_NAME.replace(' ', '_')}",
        f"--distpath={DIST_DIR}",
        f"--workpath={BUILD_DIR / 'work'}",
        f"--specpath={BUILD_DIR}",
        f"--paths={BIN_DIR}",
        static_data,
        "--hidden-import=fastapi",
        "--hidden-import=uvicorn",
        "--hidden-import=uvicorn.logging",
        "--hidden-import=uvicorn.loops",
        "--hidden-import=uvicorn.loops.auto",
        "--hidden-import=uvicorn.protocols",
        "--hidden-import=uvicorn.protocols.http",
        "--hidden-import=uvicorn.protocols.http.auto",
        "--hidden-import=uvicorn.lifespan",
        "--hidden-import=uvicorn.lifespan.on",
        "--hidden-import=starlette",
        "--hidden-import=pydantic",
        "--hidden-import=requests",
        "--hidden-import=requests.adapters",
        "--hidden-import=urllib3",
    ]

    for mod in HIDDEN_IMPORTS:
        args.append(f"--hidden-import={mod}")

    if onefile or target == "windows_exe":
        args.append("--onefile")
    else:
        args.append("--onedir")

    if target == "macos_app":
        args.append("--windowed")
        args.append(f"--osx-bundle-identifier=cn.longhun.cnsh.ide.{APP_VERSION}")

    args.append(str(ENTRY_SCRIPT))
    return args


def write_launcher():
    """为单目录分发写入一个启动脚本"""
    launcher = DIST_DIR / "启动CNSH_IDE.sh"
    launcher.write_text(
        f"#!/bin/bash\n"
        f"# DNA: #龍芯⚡️丙午·丙酉·癸亥·巳时·䷫姤-CNSH-IDE-LAUNCHER-UID9622\n"
        f"cd \"$(dirname \"$0\")\"\n"
        f"./{APP_NAME.replace(' ', '_')}/{APP_NAME.replace(' ', '_')} \"$@\"\n",
        encoding="utf-8"
    )
    launcher.chmod(0o755)
    print(f"🚀 启动脚本已生成: {launcher}")


def write_manifest(target: str, onefile: bool):
    """写入交付清单"""
    manifest = DIST_DIR / "manifest.json"
    data = {
        "app": APP_NAME,
        "version": APP_VERSION,
        "built_at": datetime.now().isoformat(),
        "platform": platform.platform(),
        "target": target,
        "onefile": onefile,
        "entry": str(ENTRY_SCRIPT.relative_to(ROOT)),
        "engines": HIDDEN_IMPORTS,
        "dna": f"#龍芯⚡️{datetime.now().strftime('%Y-%m-%d')}-CNSH-IDE-BUILD-{os.urandom(4).hex().upper()}-UID9622",
        "confirm": "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z",
    }
    manifest.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"📄 交付清单已生成: {manifest}")


def main():
    parser = argparse.ArgumentParser(description="🐉 CNSH IDE 打包脚本")
    parser.add_argument("--target", choices=["macos_app", "windows_exe", "onedir"],
                        default="macos_app" if sys.platform == "darwin" else "onedir",
                        help="打包目标")
    parser.add_argument("--onefile", action="store_true", help="打包为单个可执行文件")
    parser.add_argument("--skip-venv", action="store_true", help="跳过创建 venv（使用当前 Python）")
    args = parser.parse_args()

    print("=" * 60)
    print(f"🐉 开始打包 {APP_NAME} v{APP_VERSION}")
    print(f"   目标: {args.target}")
    print(f"   入口: {ENTRY_SCRIPT}")
    print("=" * 60)

    if not ENTRY_SCRIPT.exists():
        print(f"❌ 入口脚本不存在: {ENTRY_SCRIPT}")
        sys.exit(1)

    # 清理旧构建
    if DIST_DIR.exists():
        print(f"🧹 清理旧输出: {DIST_DIR}")
        shutil.rmtree(DIST_DIR)
    if BUILD_DIR.exists():
        shutil.rmtree(BUILD_DIR)
    BUILD_DIR.mkdir(parents=True, exist_ok=True)
    DIST_DIR.mkdir(parents=True, exist_ok=True)

    if not args.skip_venv:
        ensure_venv()

    py = python_in_venv() if not args.skip_venv else sys.executable

    print("🔨 运行 PyInstaller...")
    pi_args = collect_pyinstaller_args(args.target, args.onefile)
    run([str(py)] + pi_args[1:])  # py 已经在 python_in_venv 中指定

    write_manifest(args.target, args.onefile)
    if args.target == "onedir":
        write_launcher()

    print("=" * 60)
    print("✅ 打包完成")
    print(f"   输出目录: {DIST_DIR}")
    print(f"   下一步: 进入 {DIST_DIR} 运行应用或分发")
    print("=" * 60)


if __name__ == "__main__":
    main()
