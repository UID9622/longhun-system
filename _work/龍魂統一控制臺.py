#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🐉 龍魂統一控制臺 v1.0
Dragon Soul Unified Control Panel

DNA追溯碼：#龍芯⚡️2026-05-27-UNIFIED-CONTROL-PANEL-v1.0
CONFIRM：#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z ✅
GPG：A2D0092CEE2E5BA87035600924C3704A8CC26D5F

功能：
  • 統一管理所有龍魂系統服務
  • 單一入口啟動所有服務器
  • 多服務器和操作臺管理
  • 簡單易用的菜單界面
  • 無需分散配置，一鍵啟動

使用：
  python3 龍魂統一控制臺.py
"""

import os
import sys
import time
import subprocess
import threading
from datetime import datetime
from pathlib import Path

# 導入配置管理器
sys.path.insert(0, str(Path(__file__).parent))
try:
    from 配置读取器 import CONFIG
    CONFIG_AVAILABLE = True
except ImportError:
    CONFIG_AVAILABLE = False
    print("⚠️  警告: 配置讀取器不可用，使用預設端口")

# 定義所有服務（從統一配置讀取端口）
def get_services():
    """動態獲取服務配置"""
    if CONFIG_AVAILABLE:
        fastapi_port = CONFIG.get('CNSH_FASTAPI_PORT', 8000)
        api_port = CONFIG.get('THREE_SYSTEM_API_PORT', 5000)
    else:
        fastapi_port = 8000
        api_port = 5000

    return {
        "1": {
            "name": "🌐 CNSH 翻譯系統 (無限監聽)",
            "command": "python3 cnsh_translator_complete.py",
            "description": "多語言翻譯 + Notion 看板 + AI 處理",
            "port": "Local Queue",
            "status": "⏹️  停止"
        },
        "2": {
            "name": "⚡ CNSH FastAPI 任務提交接口",
            "command": "python3 cnsh_fastapi_interface.py",
            "description": "接收外部 JSON 任務 → 放入隊列",
            "port": str(fastapi_port),
            "status": "⏹️  停止"
        },
        "3": {
            "name": "🎯 三系統 API 服務器 (排序算法)",
            "command": "python3 longhun_api_server_stdlib.py",
            "description": "6 種排序 + PoW 記賬 + 3D 可視化",
            "port": str(api_port),
            "status": "⏹️  停止"
        },
        "4": {
            "name": "🔐 DNA 識別鎖 (驗證簽名)",
            "command": "python3 longhun_dna_parser.py",
            "description": "驗證龍魂簽名 + Tier 分級",
            "port": "N/A (Library)",
            "status": "✅ 就緒"
        },
        "5": {
            "name": "🌍 意圖翻譯官 (語義路由)",
            "command": "python3 longhun_intent_parser.py",
            "description": "自然語言 → 系統指令",
            "port": "N/A (Library)",
            "status": "✅ 就緒"
        },
    }

# 初始化服務配置
SERVICES = get_services()

# 存儲正在運行的進程
running_processes = {}
running_threads = {}

# ============================================================================
# 顯示菜單
# ============================================================================

def show_banner():
    """顯示系統横幅"""
    print("\n" + "=" * 80)
    print("🐉 龍魂統一控制臺 v1.0")
    print("=" * 80)
    print(f"DNA: #龍芯⚡️2026-05-27-UNIFIED-CONTROL-PANEL-v1.0")
    print(f"時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S CST')}")
    print(f"狀態: 準備就緒\n")


def show_services_status():
    """顯示所有服務狀態"""
    print("📋 可用服務:")
    print("-" * 80)

    for key, service in SERVICES.items():
        status = "🟢 運行中" if key in running_processes else service["status"]
        print(f"\n  {key}️⃣  {service['name']}")
        print(f"      端口: {service['port']}")
        print(f"      說明: {service['description']}")
        print(f"      狀態: {status}")


def show_main_menu():
    """顯示主菜單"""
    print("\n" + "-" * 80)
    print("\n📡 主菜單:")
    print("  1-5     啟動對應服務")
    print("  all     啟動所有服務 (推薦)")
    print("  stop    停止所有服務")
    print("  status  查看服務狀態")
    print("  clear   清理日誌和緩存")
    print("  test    運行集成測試")
    print("  help    查看幫助信息")
    print("  exit    退出系統\n")


# ============================================================================
# 服務管理
# ============================================================================

def start_service(service_key):
    """啟動單個服務"""
    if service_key not in SERVICES:
        print(f"❌ 無效的服務鍵: {service_key}")
        return False

    if service_key in running_processes:
        print(f"⚠️  服務已運行: {SERVICES[service_key]['name']}")
        return False

    service = SERVICES[service_key]
    print(f"\n🚀 啟動服務: {service['name']}")
    print(f"   命令: {service['command']}")

    try:
        # 啟動進程
        process = subprocess.Popen(
            service['command'].split(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=Path(__file__).parent
        )

        running_processes[service_key] = process
        print(f"✅ 服務已啟動 (PID: {process.pid})")
        print(f"   訪問: http://localhost:{service['port']}" if service['port'] != "Local Queue" and service['port'] != "N/A (Library)" else "")

        return True

    except Exception as e:
        print(f"❌ 啟動失敗: {e}")
        return False


def start_all_services():
    """啟動所有服務"""
    print("\n" + "=" * 80)
    print("🚀 正在啟動所有服務...")
    print("=" * 80)

    for key in ["1", "2", "3"]:  # 只啟動需要進程的服務
        start_service(key)
        time.sleep(1)

    print("\n✅ 所有服務已啟動")
    print("\n📱 訪問地址:")
    fastapi_port = SERVICES['2']['port']
    api_port = SERVICES['3']['port']
    print(f"   - CNSH 任務提交: http://localhost:{fastapi_port}/docs")
    print(f"   - 三系統 API: http://localhost:{api_port}/control")
    print("   - CNSH 隊列: Local Queue (後台監聽)")
    print("\n⏳ 服務初始化中，請稍候 5 秒...")
    time.sleep(5)


def stop_all_services():
    """停止所有服務"""
    print("\n🛑 正在停止所有服務...")

    for key, process in list(running_processes.items()):
        try:
            process.terminate()
            process.wait(timeout=5)
            del running_processes[key]
            print(f"✅ 已停止: {SERVICES[key]['name']}")
        except Exception as e:
            print(f"❌ 停止失敗: {e}")
            try:
                process.kill()
            except:
                pass

    print("\n✅ 所有服務已停止")


def show_status():
    """顯示服務狀態"""
    print("\n" + "=" * 80)
    print("📊 服務狀態統計")
    print("=" * 80)

    running_count = len(running_processes)
    total_count = len([s for s in SERVICES.values() if "Library" not in s["port"] and "Local Queue" not in s["port"]])

    print(f"\n運行中: {running_count}")
    print(f"總數: {total_count}")
    print(f"成功率: {running_count}/{total_count}\n")

    for key in ["1", "2", "3"]:
        status = "🟢 運行中" if key in running_processes else "⏹️  停止"
        print(f"  {SERVICES[key]['name']}: {status}")

    print(f"\n就緒服務:")
    for key in ["4", "5"]:
        print(f"  {SERVICES[key]['name']}: ✅ 就緒")


def run_tests():
    """運行集成測試"""
    print("\n" + "=" * 80)
    print("🧪 運行集成測試")
    print("=" * 80)

    try:
        result = subprocess.run(
            ["python3", "longhun_integration_test.py"],
            cwd=Path(__file__).parent,
            capture_output=True,
            text=True,
            timeout=30
        )

        print(result.stdout)
        if result.returncode == 0:
            print("\n✅ 測試全部通過")
        else:
            print(f"\n❌ 測試失敗 (exit code: {result.returncode})")
            if result.stderr:
                print(f"錯誤: {result.stderr}")

    except subprocess.TimeoutExpired:
        print("❌ 測試超時")
    except Exception as e:
        print(f"❌ 測試失敗: {e}")


def clear_cache():
    """清理日誌和緩存"""
    print("\n🧹 清理日誌和緩存...")

    try:
        cache_dirs = [
            "~/.longhun",
            "~/.notion_cache",
            "./__pycache__",
            "./*.log"
        ]

        for cache_dir in cache_dirs:
            expanded_path = os.path.expanduser(cache_dir)
            if os.path.exists(expanded_path):
                if os.path.isdir(expanded_path):
                    import shutil
                    shutil.rmtree(expanded_path, ignore_errors=True)
                    print(f"✅ 已清理: {expanded_path}")

        print("\n✅ 清理完成")

    except Exception as e:
        print(f"❌ 清理失敗: {e}")


def show_help():
    """顯示幫助信息"""
    print("\n" + "=" * 80)
    print("📖 龍魂統一控制臺 使用指南")
    print("=" * 80)

    help_text = """
【快速開始】

1. 啟動所有服務:
   輸入 "all"

2. 訪問 CNSH 任務提交:
   http://localhost:8000/docs

3. 訪問三系統 API:
   http://localhost:5000/control

【單個服務】

CNSH 翻譯系統 (1)
  - 後台無限監聽任務隊列
  - 自動翻譯和質量評分

CNSH FastAPI (2)
  - REST API 接收外部任務
  - 端口: 8000
  - 文檔: http://localhost:8000/docs

三系統 API (3)
  - 6 種排序算法
  - PoW 工作量證明
  - 3D 可視化
  - 端口: 5000
  - 控制面板: http://localhost:5000/control

【命令】

all     - 啟動所有服務 ⭐ 推薦
1-5     - 啟動特定服務
stop    - 停止所有服務
status  - 查看服務狀態
test    - 運行集成測試
clear   - 清理緩存
help    - 查看此幫助
exit    - 退出

【故障排除】

端口被佔用?
  → 運行 "stop" 停止所有服務
  → 或使用 lsof -i :8000

服務無法啟動?
  → 檢查依賴: pip install fastapi uvicorn pydantic requests
  → 運行 "test" 進行診斷

【聯繫信息】

DNA: #龍芯⚡️2026-05-27-UNIFIED-CONTROL-PANEL-v1.0
責任: UID9622·龍芯北辰
    """

    print(help_text)


# ============================================================================
# 主循環
# ============================================================================

def main():
    """主函數"""
    show_banner()

    while True:
        try:
            show_services_status()
            show_main_menu()

            command = input("👉 輸入命令 (all/1-5/stop/status/test/clear/help/exit): ").strip().lower()

            if command == "exit":
                print("\n👋 感謝使用龍魂統一控制臺")
                stop_all_services()
                sys.exit(0)

            elif command == "all":
                start_all_services()

            elif command in SERVICES:
                start_service(command)

            elif command == "stop":
                stop_all_services()

            elif command == "status":
                show_status()

            elif command == "test":
                run_tests()

            elif command == "clear":
                clear_cache()

            elif command == "help":
                show_help()

            else:
                print("❌ 無效的命令，請重試")

            # 短暫停頓，避免快速循環
            time.sleep(0.5)

        except KeyboardInterrupt:
            print("\n\n👋 收到退出信號...")
            stop_all_services()
            sys.exit(0)

        except Exception as e:
            print(f"\n❌ 出錯: {e}")
            time.sleep(1)


if __name__ == "__main__":
    main()
