#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂 Notion 集成 · Stage 5 調度配置

DNA: #龍芯⚇️2026-06-01-SETUP-SCHEDULER-v1.0
Purpose: 配置自動化同步調度，支持 cron 和 systemd

Features:
  - 交互式配置流程
  - 支持多種調度方式
  - 自動生成 cron 任務
  - 自動生成 systemd 服務
  - 配置驗證和測試
"""

import os
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional

current_dir = str(Path(__file__).parent)
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

try:
    from .notion_config import NotionConfigManager, NotionConfig
    from .notion_client import NotionClient, NotionAuthError
    from .scheduler import SyncScheduler
except ImportError:
    from notion_config import NotionConfigManager, NotionConfig
    from notion_client import NotionClient, NotionAuthError
    from scheduler import SyncScheduler


def print_header(title: str):
    """打印標題"""
    print("\n" + "=" * 70)
    print(f"🐉 {title}")
    print("=" * 70)


def step_1_verify_connection():
    """第一步：驗證連接"""
    print_header("第一步：驗證 Notion API 連接")

    manager = NotionConfigManager()
    try:
        config = manager.load()
    except ValueError as e:
        print(f"❌ {e}")
        return None

    try:
        client = NotionClient(config)
        if not client.test_connection():
            print("❌ 連接測試失敗")
            return None
        print("✅ API 連接正常")
        return client, config
    except NotionAuthError as e:
        print(f"❌ 認證失敗: {e}")
        return None
    except Exception as e:
        print(f"❌ 連接失敗: {e}")
        return None


def step_2_select_scheduler_type():
    """第二步：選擇調度方式"""
    print_header("第二步：選擇同步調度方式")

    print("""
請選擇調度方式：

1. 🔵 Cron (推薦用於 Linux/macOS)
   - 輕量級，系統原生支持
   - 定時執行，可配置頻率
   - 適合生產環境

2. 🟡 Systemd Timer (推薦用於 systemd 系統)
   - 高級定時功能
   - 服務依賴管理
   - 完整的日誌集成

3. 🟢 Manual (推薦用於開發和測試)
   - 手動執行同步
   - 靈活控制
   - 適合調試

4. 🟣 Python Daemon (後臺常駐)
   - Python 級別的調度
   - 完整的控制能力
   - 適合生產環境（推薦）
    """)

    while True:
        choice = input("請選擇 (1-4): ").strip()
        if choice in ['1', '2', '3', '4']:
            return ['cron', 'systemd', 'manual', 'daemon'][int(choice) - 1]
        print("❌ 無效選擇，請重試")


def step_3_configure_schedules(config: NotionConfig):
    """第三步：配置同步時間表"""
    print_header("第三步：配置同步時間表")

    schedules = {}

    print("\n請為每個同步任務配置運行時間")
    print("(使用 HH:MM 格式，例如: 02:00)\n")

    stages = [
        (2, "CNSH 基準測試", "02:00"),
        (3, "知識圖譜", "03:00"),
        (4, "審計日誌", "04:00")
    ]

    for stage, name, default_time in stages:
        print(f"📌 Stage {stage}: {name}")

        frequency = input(f"   同步頻率 (daily/hourly/every_6h) [默認: daily]: ").strip() or "daily"
        time_of_day = input(f"   運行時間 [默認: {default_time}]: ").strip() or default_time

        schedules[stage] = {
            "name": name,
            "frequency": frequency,
            "time_of_day": time_of_day
        }

    return schedules


def step_4_generate_config(scheduler_type: str, schedules: dict):
    """第四步：生成配置文件"""
    print_header("第四步：生成配置文件")

    config_dir = Path.home() / ".龍魂_config"
    config_dir.mkdir(parents=True, exist_ok=True)

    if scheduler_type == "cron":
        _generate_cron_config(config_dir, schedules)
    elif scheduler_type == "systemd":
        _generate_systemd_config(config_dir, schedules)
    elif scheduler_type == "daemon":
        _generate_daemon_config(config_dir, schedules)
    else:  # manual
        _generate_manual_config(config_dir, schedules)

    print(f"✅ 配置已生成到 {config_dir}")


def _generate_cron_config(config_dir: Path, schedules: dict):
    """生成 Cron 配置"""
    print("\n📝 生成 Cron 配置...")

    cron_file = config_dir / "notion_sync.cron"
    cron_lines = ["# 龍魂 Notion 同步 Cron 任務\n"]

    # 計算 cron 表達式
    for stage, config in schedules.items():
        hour, minute = config["time_of_day"].split(':')
        freq = config["frequency"]

        if freq == "daily":
            cron_expr = f"{minute} {hour} * * *"
        elif freq == "hourly":
            cron_expr = f"{minute} * * * *"
        elif freq == "every_6h":
            cron_expr = f"{minute} */6 * * *"
        else:
            cron_expr = f"{minute} {hour} * * *"

        cmd = f"python3 ~/longhun-system/notion/sync_runner.py stage{stage}"
        cron_lines.append(f"{cron_expr} {cmd}  # Stage {stage}: {config['name']}\n")

    with open(cron_file, 'w') as f:
        f.writelines(cron_lines)

    print(f"✅ Cron 配置: {cron_file}")
    print("\n使用方法:")
    print(f"   crontab {cron_file}")
    print(f"   # 或手動複製以下行到 crontab:")
    print(f"   crontab -e")
    for line in cron_lines[1:]:
        print(f"   {line.strip()}")


def _generate_systemd_config(config_dir: Path, schedules: dict):
    """生成 Systemd 配置"""
    print("\n📝 生成 Systemd 配置...")

    service_dir = config_dir / "systemd"
    service_dir.mkdir(parents=True, exist_ok=True)

    # 生成服務文件
    service_content = """[Unit]
Description=龍魂 Notion 同步服務
After=network.target

[Service]
Type=simple
User={user}
WorkingDirectory={home}/longhun-system/notion
ExecStart=python3 sync_runner.py daemon
Restart=on-failure
RestartSec=300

[Install]
WantedBy=multi-user.target
"""

    service_file = service_dir / "longhun-notion-sync.service"
    with open(service_file, 'w') as f:
        f.write(service_content.format(
            user=os.getenv("USER", "nobody"),
            home=str(Path.home())
        ))

    # 生成 Timer 文件
    timer_content = """[Unit]
Description=龍魂 Notion 同步計時器
Requires=longhun-notion-sync.service

[Timer]
OnCalendar=*-*-* {hour}:{minute}:00
Persistent=true

[Install]
WantedBy=timers.target
"""

    for stage, config in schedules.items():
        timer_file = service_dir / f"longhun-notion-sync-stage{stage}.timer"
        with open(timer_file, 'w') as f:
            f.write(timer_content.format(
                hour=config["time_of_day"].split(':')[0],
                minute=config["time_of_day"].split(':')[1]
            ))

    print(f"✅ Systemd 配置: {service_dir}")
    print("\n使用方法:")
    print(f"   sudo cp {service_dir}/* /etc/systemd/system/")
    print(f"   sudo systemctl daemon-reload")
    print(f"   sudo systemctl enable longhun-notion-sync.service")
    print(f"   sudo systemctl start longhun-notion-sync.service")


def _generate_daemon_config(config_dir: Path, schedules: dict):
    """生成 Daemon 配置"""
    print("\n📝 生成 Daemon 配置...")

    import json

    daemon_config = {
        "enabled": True,
        "schedules": schedules,
        "worker_threads": 3,
        "log_level": "INFO",
        "generated_at": datetime.now().isoformat()
    }

    daemon_file = config_dir / "daemon_config.json"
    with open(daemon_file, 'w') as f:
        json.dump(daemon_config, f, indent=2, ensure_ascii=False)

    print(f"✅ Daemon 配置: {daemon_file}")
    print("\n使用方法:")
    print(f"   python3 ~/longhun-system/notion/sync_runner.py daemon")
    print(f"   # 或使用 nohup 後臺運行:")
    print(f"   nohup python3 ~/longhun-system/notion/sync_runner.py daemon &")


def _generate_manual_config(config_dir: Path, schedules: dict):
    """生成 Manual 配置"""
    print("\n📝 生成 Manual 配置...")

    manual_file = config_dir / "manual_schedule.txt"
    lines = ["# 龍魂 Notion 同步時間表\n"]
    lines.append(f"# 生成於: {datetime.now().isoformat()}\n\n")

    for stage, config in schedules.items():
        lines.append(f"Stage {stage}: {config['name']}\n")
        lines.append(f"  頻率: {config['frequency']}\n")
        lines.append(f"  時間: {config['time_of_day']}\n")
        lines.append(f"  命令: python3 ~/longhun-system/notion/sync_runner.py stage{stage}\n\n")

    with open(manual_file, 'w') as f:
        f.writelines(lines)

    print(f"✅ Manual 配置: {manual_file}")
    print("\n使用方法:")
    for stage, config in schedules.items():
        print(f"   # Stage {stage}: {config['name']}")
        print(f"   python3 ~/longhun-system/notion/sync_runner.py stage{stage}")


def step_5_test_scheduler(client: NotionClient, config: NotionConfig):
    """第五步：測試調度器"""
    print_header("第五步：測試同步調度器")

    print("\n是否進行測試同步？")
    print("  1. 是 - 執行一次完整同步測試")
    print("  2. 否 - 跳過測試")

    choice = input("\n請選擇 (1-2) [默認: 2]: ").strip() or "2"

    if choice == "1":
        print("\n🧪 開始測試同步...")

        try:
            scheduler = SyncScheduler(config)

            # 測試各 stage
            for stage in [2, 3, 4]:
                print(f"\n測試 Stage {stage}...")
                task = scheduler._create_task(
                    stage,
                    ["CNSH", "Knowledge", "Audit"][stage - 2],
                    "daily",
                    "02:00"
                )

                if scheduler.resolver.acquire_lock(stage, timeout=10):
                    try:
                        print(f"✅ 成功獲得鎖")
                    finally:
                        scheduler.resolver.release_lock(stage)
                else:
                    print(f"⚠️  無法獲得鎖（可能有同步正在進行）")

            print("\n✅ 測試完成")

        except Exception as e:
            print(f"❌ 測試失敗: {e}")
    else:
        print("⏭️  跳過測試")


def main():
    """主函數"""
    print("""
🐉 龍魂 Notion 集成 · Stage 5 調度配置
DNA: #龍芯⚇️2026-06-01-SETUP-SCHEDULER-v1.0

本腳本將幫助您配置自動化同步調度系統。
    """)

    # 第一步：驗證連接
    result = step_1_verify_connection()
    if not result:
        sys.exit(1)

    client, config = result

    # 第二步：選擇調度方式
    scheduler_type = step_2_select_scheduler_type()
    print(f"\n✅ 已選擇: {scheduler_type}")

    # 第三步：配置時間表
    schedules = step_3_configure_schedules(config)

    # 第四步：生成配置
    step_4_generate_config(scheduler_type, schedules)

    # 第五步：測試調度器
    step_5_test_scheduler(client, config)

    # 完成
    print("\n" + "=" * 70)
    print("✅ 調度配置完成！")
    print("=" * 70)

    if scheduler_type == "cron":
        print("\n下一步: 使用 crontab -e 編輯任務")
    elif scheduler_type == "systemd":
        print("\n下一步: 安裝並啟用 systemd 服務")
    elif scheduler_type == "daemon":
        print("\n下一步: 運行 python3 sync_runner.py daemon 啟動服務")
    else:
        print("\n下一步: 按計劃手動運行同步命令")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️  用戶中斷")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 錯誤: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
