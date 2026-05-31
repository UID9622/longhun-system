#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂 Notion 集成 · 同步運行器

DNA: #龍芯⚇️2026-06-01-SYNC-RUNNER-v1.0
Purpose: 執行同步任務的命令行入口

Usage:
  python3 sync_runner.py stage2        # 執行 Stage 2 (CNSH)
  python3 sync_runner.py stage3        # 執行 Stage 3 (Knowledge)
  python3 sync_runner.py stage4        # 執行 Stage 4 (Audit)
  python3 sync_runner.py daemon        # 啟動後臺調度器
  python3 sync_runner.py status        # 查看調度器狀態
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime

current_dir = str(Path(__file__).parent)
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

try:
    from .notion_config import NotionConfigManager
    from .notion_client import NotionClient
    from .cnsh_sync import CNSHNotionSync
    from .knowledge_sync import KnowledgeNotionSync
    from .audit_sync import AuditNotionSync
    from .scheduler import SyncScheduler
except ImportError:
    from notion_config import NotionConfigManager
    from notion_client import NotionClient
    from cnsh_sync import CNSHNotionSync
    from knowledge_sync import KnowledgeNotionSync
    from audit_sync import AuditNotionSync
    from scheduler import SyncScheduler


def load_config():
    """加載配置"""
    try:
        manager = NotionConfigManager()
        return manager.load()
    except ValueError as e:
        print(f"❌ 配置加載失敗: {e}")
        sys.exit(1)


def run_stage_sync(stage: int):
    """執行 Stage 同步"""
    config = load_config()

    try:
        client = NotionClient(config)

        if stage == 2:
            print("🔄 執行 Stage 2: CNSH 基準測試同步")
            sync = CNSHNotionSync(client, config)

        elif stage == 3:
            print("🔄 執行 Stage 3: 知識圖譜同步")
            sync = KnowledgeNotionSync(client, config)

        elif stage == 4:
            print("🔄 執行 Stage 4: 審計日誌同步")
            sync = AuditNotionSync(client, config)

        else:
            print(f"❌ 無效的 Stage: {stage}")
            sys.exit(1)

        # 執行同步
        start_time = datetime.now()
        success = sync.sync_all()
        duration = (datetime.now() - start_time).total_seconds()

        if success:
            print(f"\n✅ Stage {stage} 同步完成 ({duration:.1f} 秒)")
            _log_sync_event(stage, "success", duration)
            sys.exit(0)
        else:
            print(f"\n❌ Stage {stage} 同步失敗")
            _log_sync_event(stage, "failed", duration)
            sys.exit(1)

    except Exception as e:
        print(f"\n❌ 執行錯誤: {e}")
        import traceback
        traceback.print_exc()
        _log_sync_event(stage, "error", 0, str(e))
        sys.exit(1)


def run_daemon():
    """啟動後臺調度器"""
    config = load_config()
    scheduler = SyncScheduler(config)

    try:
        # 加載配置
        config_file = Path.home() / ".龍魂_config" / "daemon_config.json"

        schedules = {}
        if config_file.exists():
            with open(config_file) as f:
                daemon_config = json.load(f)
                schedules = daemon_config.get("schedules", {})

        if not schedules:
            # 默認時間表
            print("⚠️  未找到配置文件，使用默認時間表")
            scheduler.schedule_cnsh_sync("daily", "02:00")
            scheduler.schedule_knowledge_sync("daily", "03:00")
            scheduler.schedule_audit_sync("daily", "04:00")
        else:
            # 加載配置的時間表
            for stage, sched in schedules.items():
                stage_int = int(stage)
                if stage_int == 2:
                    scheduler.schedule_cnsh_sync(
                        sched.get("frequency", "daily"),
                        sched.get("time_of_day", "02:00")
                    )
                elif stage_int == 3:
                    scheduler.schedule_knowledge_sync(
                        sched.get("frequency", "daily"),
                        sched.get("time_of_day", "03:00")
                    )
                elif stage_int == 4:
                    scheduler.schedule_audit_sync(
                        sched.get("frequency", "daily"),
                        sched.get("time_of_day", "04:00")
                    )

        # 啟動調度器
        print("🚀 啟動同步調度器...")
        print("   按 Ctrl+C 停止")

        workers, monitor = scheduler.start_scheduler(worker_threads=3)

        # 主線程等待
        try:
            while True:
                import time
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n⏹️  正在停止調度器...")
            scheduler.stop_scheduler()

    except Exception as e:
        print(f"❌ 啟動失敗: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


def show_status():
    """顯示調度器狀態"""
    config = load_config()
    scheduler = SyncScheduler(config)

    scheduler.print_status()

    # 顯示最近的同步記錄
    log_file = Path.home() / ".龍魂" / "sync_schedule.jsonl"
    if log_file.exists():
        print("\n📋 最近同步記錄 (最新 5 條):")
        with open(log_file) as f:
            lines = f.readlines()
            for line in lines[-5:]:
                try:
                    entry = json.loads(line)
                    print(f"   - Stage {entry.get('stage')}: {entry.get('status')} "
                          f"({entry.get('completed_at', 'N/A')})")
                except:
                    pass


def show_help():
    """顯示幫助信息"""
    print("""
🐉 龍魂 Notion 集成 · 同步運行器
DNA: #龍芯⚇️2026-06-01-SYNC-RUNNER-v1.0

用法:
  python3 sync_runner.py <command> [options]

命令:
  stage2                  執行 Stage 2 (CNSH 基準測試同步)
  stage3                  執行 Stage 3 (知識圖譜同步)
  stage4                  執行 Stage 4 (審計日誌同步)
  daemon                  啟動後臺調度器
  status                  查看調度器狀態
  help                    顯示此幫助信息

示例:
  python3 sync_runner.py stage2          # 立即執行 CNSH 同步
  python3 sync_runner.py daemon          # 啟動自動調度器
  python3 sync_runner.py status          # 查看狀態

環境變量:
  NOTION_TOKEN            Notion API Token
  NOTION_*_DB             各個數據庫 ID

配置文件:
  ~/.龍魂_config/daemon_config.json     調度器配置
  ~/.龍魂/sync_schedule.jsonl           同步歷史日誌
    """)


def _log_sync_event(stage: int, status: str, duration: float, error: str = None):
    """記錄同步事件"""
    try:
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "stage": stage,
            "status": status,
            "duration_seconds": duration,
        }
        if error:
            log_entry["error"] = error

        log_file = Path.home() / ".龍魂" / "sync_runner.jsonl"
        log_file.parent.mkdir(parents=True, exist_ok=True)

        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')
    except:
        pass


def main():
    """主函數"""
    if len(sys.argv) < 2:
        show_help()
        sys.exit(0)

    command = sys.argv[1].lower()

    if command == "stage2":
        run_stage_sync(2)
    elif command == "stage3":
        run_stage_sync(3)
    elif command == "stage4":
        run_stage_sync(4)
    elif command == "daemon":
        run_daemon()
    elif command == "status":
        show_status()
    elif command in ["help", "-h", "--help"]:
        show_help()
    else:
        print(f"❌ 無效的命令: {command}")
        print("使用 'help' 命令查看幫助信息")
        sys.exit(1)


if __name__ == "__main__":
    main()
