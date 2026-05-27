#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🐉 龍魂系統診斷工具
Dragon Soul System Diagnostic Tool

檢查所有服務是否就緒，識別問題並提出解決方案
"""

import subprocess
import sys
import os
from pathlib import Path
from datetime import datetime

def check_python_version():
    """檢查 Python 版本"""
    version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    print(f"✅ Python 版本: {version}")
    if sys.version_info.major < 3 or sys.version_info.minor < 8:
        print("⚠️  建議使用 Python 3.8 或更高版本")
    return True


def check_dependencies():
    """檢查必要的依賴"""
    dependencies = {
        "fastapi": "Web 框架",
        "uvicorn": "ASGI 服務器",
        "pydantic": "數據驗證",
        "requests": "HTTP 客戶端"
    }

    print("\n📦 檢查依賴:")
    missing = []

    for module, description in dependencies.items():
        try:
            __import__(module)
            print(f"  ✅ {module:15} - {description}")
        except ImportError:
            print(f"  ❌ {module:15} - {description} (缺失)")
            missing.append(module)

    if missing:
        print(f"\n⚠️  缺少的包: {', '.join(missing)}")
        print("\n安裝命令:")
        print(f"  pip install --user {' '.join(missing)}")
        return False

    return True


def check_core_files():
    """檢查核心文件"""
    core_files = {
        "龍魂統一控制臺.py": "主控制菜單",
        "cnsh_translator_complete.py": "CNSH 翻譯系統",
        "cnsh_fastapi_interface.py": "FastAPI 接口",
        "longhun_api_server_stdlib.py": "三系統 API",
        "longhun_dna_parser.py": "DNA 驗證",
        "longhun_intent_parser.py": "意圖路由",
        "longhun_integration_test.py": "集成測試"
    }

    print("\n📁 檢查核心文件:")
    missing = []

    for filename, description in core_files.items():
        filepath = Path(__file__).parent / filename
        if filepath.exists():
            size = filepath.stat().st_size / 1024  # KB
            print(f"  ✅ {filename:35} - {description:20} ({size:.1f}KB)")
        else:
            print(f"  ❌ {filename:35} - {description:20} (缺失)")
            missing.append(filename)

    if missing:
        print(f"\n⚠️  缺少的文件: {', '.join(missing)}")
        return False

    return True


def check_ports():
    """檢查端口是否被佔用"""
    print("\n🔌 檢查端口:")

    ports = {
        "8000": "CNSH FastAPI",
        "5000": "三系統 API"
    }

    for port, service in ports.items():
        try:
            result = subprocess.run(
                f"lsof -i :{port}",
                shell=True,
                capture_output=True,
                text=True,
                timeout=2
            )

            if result.returncode == 0 and result.stdout:
                print(f"  ⚠️  端口 {port} 被佔用 ({service})")
                print(f"      運行 'sudo lsof -i :{port}' 查看詳情")
            else:
                print(f"  ✅ 端口 {port} 可用 ({service})")

        except Exception as e:
            print(f"  ⚠️  端口 {port} 檢查失敗: {e}")


def check_directories():
    """檢查必要的目錄"""
    print("\n📂 檢查目錄:")

    directories = {
        "~/.longhun": "本地任務數據庫",
        "~/.notion_cache": "Notion 緩存"
    }

    for dirname, description in directories.items():
        expanded = os.path.expanduser(dirname)
        if os.path.exists(expanded):
            size = sum(f.stat().st_size for f in Path(expanded).rglob('*') if f.is_file()) / 1024 / 1024
            print(f"  ✅ {dirname:20} - {description:20} ({size:.1f}MB)")
        else:
            print(f"  ℹ️  {dirname:20} - {description:20} (不存在，首次會自動創建)")


def check_connectivity():
    """檢查網絡連接"""
    print("\n🌐 檢查網絡連接:")

    try:
        result = subprocess.run(
            "ping -c 1 8.8.8.8",
            shell=True,
            capture_output=True,
            timeout=3
        )

        if result.returncode == 0:
            print("  ✅ 互聯網連接正常")
        else:
            print("  ⚠️  互聯網連接可能有問題 (Notion 同步可能失敗)")

    except:
        print("  ⚠️  無法檢查網絡連接")


def generate_report():
    """生成診斷報告"""
    print("\n" + "=" * 80)
    print("🐉 龍魂系統診斷報告")
    print("=" * 80)
    print(f"時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S CST')}")
    print()

    checks = [
        ("Python 版本", check_python_version),
        ("依賴檢查", check_dependencies),
        ("核心文件", check_core_files),
        ("端口狀態", check_ports),
        ("本地目錄", check_directories),
        ("網絡連接", check_connectivity)
    ]

    results = []
    for check_name, check_func in checks:
        try:
            result = check_func()
            results.append(result)
        except Exception as e:
            print(f"\n❌ {check_name} 檢查失敗: {e}")
            results.append(False)

    # 生成總結
    print("\n" + "=" * 80)
    print("📊 診斷總結")
    print("=" * 80)

    passed = sum(1 for r in results if r)
    total = len(results)

    print(f"\n通過: {passed}/{total}")

    if passed == total:
        print("\n✅ 所有檢查都通過！系統已就緒。")
        print("\n🚀 立即啟動:")
        print("  python3 龍魂統一控制臺.py")
        print("  或")
        print("  ./启动.sh")
    else:
        print("\n⚠️  某些檢查未通過。請查看上方說明進行修復。")

    print("\n" + "=" * 80)


if __name__ == "__main__":
    generate_report()
