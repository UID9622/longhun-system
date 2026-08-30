#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·甲申·癸巳·申时·䷣明夷-CNSH-FONT-ENGINE-v4.0-UID9622
# 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 主权锚定: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# 协议: 工程层 MulanPSL v2 · 思想层 CC BY-NC-SA 4.0
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# 状态: 🟢 v4.0 融合（来源: 云上CNSH军人的编辑器 cnsh_font_engine_uid9622.py）
# 版本: 4.0.0

"""
🔤 CNSH字体引擎 - 使用CNSH字体渲染CNSH代码

为CNSH中文编程语言提供专用的等宽字体支持，
确保代码在不同平台上显示一致。

用法:
    python cnsh_font_engine.py check        # 检查字体安装状态
    python cnsh_font_engine.py install      # 安装字体
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

# 字体配置
FONT_NAME = "CNSH"
FONT_FILENAMES = [
    "CNSH-Regular.ttf",
    "CNSH-Italic.ttf",
    "CNSH-Bold.ttf",
    "CNSH-BoldItalic.ttf",
]


def get_font_dir() -> Path:
    """获取字体目录"""
    if sys.platform == "darwin":  # macOS
        return Path.home() / "Library" / "Fonts"
    elif sys.platform.startswith("linux"):
        return Path.home() / ".local" / "share" / "fonts"
    elif sys.platform == "win32":
        return Path(os.environ.get("LOCALAPPDATA", Path.home())) / "Microsoft" / "Windows" / "Fonts"
    else:
        return Path.home() / ".fonts"


def get_asset_dir() -> Path:
    """获取字体资产目录"""
    # 优先使用本地字体资产
    local_candidates = [
        Path(__file__).parent.parent / "longhun-font",
        Path(__file__).parent.parent / "fonts",
        Path(__file__).parent.parent / "assets" / "fonts",
    ]
    
    for path in local_candidates:
        if path.exists():
            return path
    
    return local_candidates[0]


def check_font_installed() -> dict:
    """检查字体安装状态"""
    font_dir = get_font_dir()
    installed = []
    missing = []
    
    for filename in FONT_FILENAMES:
        font_path = font_dir / filename
        if font_path.exists():
            installed.append(filename)
        else:
            missing.append(filename)
    
    return {
        "installed": installed,
        "missing": missing,
        "font_dir": str(font_dir),
        "complete": len(missing) == 0
    }


def install_font() -> bool:
    """安装字体"""
    status = check_font_installed()
    
    if status["complete"]:
        print(f"✅ CNSH字体已安装（{status['font_dir']}）")
        return True
    
    asset_dir = get_asset_dir()
    font_dir = get_font_dir()
    
    if not asset_dir.exists():
        print(f"❌ 字体资产目录不存在: {asset_dir}")
        return False
    
    font_dir.mkdir(parents=True, exist_ok=True)
    
    installed_count = 0
    for filename in status["missing"]:
        src = asset_dir / filename
        if src.exists():
            dst = font_dir / filename
            shutil.copy2(src, dst)
            print(f"  ✅ 已安装: {filename}")
            installed_count += 1
        else:
            print(f"  ⚠️ 资产缺失: {filename}（预期位置: {src}）")
    
    if installed_count > 0:
        # macOS 刷新字体缓存
        if sys.platform == "darwin":
            subprocess.run(
                ["atsutil", "databases", "-removeUser", "-quiet"],
                capture_output=True
            )
            print("  ℹ️ 已刷新字体缓存")
        
        print(f"✅ 安装完成: {installed_count} 个字体文件")
        return True
    
    return False


def main():
    """主函数"""
    command = sys.argv[1] if len(sys.argv) > 1 else "check"
    
    if command == "check":
        status = check_font_installed()
        print(f"🔤 CNSH字体引擎")
        print(f"  字体目录: {status['font_dir']}")
        print(f"  已安装: {status['installed'] or '无'}")
        print(f"  缺失: {status['missing'] or '无'}")
        print(f"  状态: {'✅ 完整' if status['complete'] else '❌ 不完整'}")
        
        if not status["complete"]:
            print(f"\n  提示: 运行 'python cnsh_font_engine.py install' 安装")
        return 0
    
    elif command == "install":
        print("🔤 正在安装CNSH字体...")
        success = install_font()
        return 0 if success else 1
    
    else:
        print(f"用法: python {sys.argv[0]} [check|install]")
        return 1


if __name__ == '__main__':
    exit(main())
