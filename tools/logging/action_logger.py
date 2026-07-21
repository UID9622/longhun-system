#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""龍魂操作日志记录器 · 全系统审计
DNA:#龍芯⚡️2026-06-09-ACTION-LOGGER-v1.0

用途: 在任何操作前后记录到 action_log.jsonl
支持: 完整操作跟踪·性能分析·每日审计
"""

import json
import os
import sys
import time
from datetime import datetime, timezone, timedelta
from pathlib import Path
from contextlib import contextmanager

HOME = Path.home()
LOG_DIR = HOME / "longhun-system" / "logs"
LOG_FILE = LOG_DIR / "action_log.jsonl"

# 确保日志目录存在
LOG_DIR.mkdir(parents=True, exist_ok=True)

def now_bj():
    """北京时间"""
    return datetime.now(timezone(timedelta(hours=8)))

class ActionLogger:
    """操作日志记录器"""

    @staticmethod
    def log(action, tool, status="success", persona=None, result=None, duration=None, dna=None, **kwargs):
        """记录单个操作

        Args:
            action (str): 操作名称 (例: "系统扫描")
            tool (str): 工具名称 (例: "system_scan")
            status (str): 状态 ("success", "failed", "warning")
            persona (str): 执行人格 (例: "P01诸葛亮")
            result (str): 执行结果 (例: "100% 通过")
            duration (float): 执行时长 (秒)
            dna (str): DNA 签署码
            **kwargs: 其他自定义字段
        """
        now = now_bj()

        record = {
            "date": now.strftime("%Y-%m-%dT%H:%M:%S"),
            "time": now.strftime("%Y-%m-%d %H:%M:%S"),
            "action": action,
            "tool": tool,
            "status": status,
        }

        # 可选字段
        if persona:
            record["persona"] = persona
        if result:
            record["result"] = result
        if duration is not None:
            record["duration"] = duration
        if dna:
            record["dna"] = dna

        # 添加自定义字段
        record.update(kwargs)

        # 写入日志
        try:
            with open(LOG_FILE, "a", encoding="utf-8") as f:
                f.write(json.dumps(record, ensure_ascii=False) + "\n")
        except Exception as e:
            print(f"❌ 日志写入失败: {e}", file=sys.stderr)

    @staticmethod
    def get_today_logs():
        """获取今天的所有日志"""
        if not LOG_FILE.exists():
            return []

        today = now_bj().strftime("%Y-%m-%d")
        logs = []

        try:
            with open(LOG_FILE) as f:
                for line in f:
                    try:
                        record = json.loads(line)
                        if record.get("date", "").startswith(today):
                            logs.append(record)
                    except json.JSONDecodeError:
                        pass
        except Exception as e:
            print(f"❌ 日志读取失败: {e}", file=sys.stderr)

        return logs

    @staticmethod
    def get_stats(logs=None):
        """统计日志数据

        Returns:
            dict: 统计信息 (总数·工具·人格·状态)
        """
        if logs is None:
            logs = ActionLogger.get_today_logs()

        stats = {
            "total": len(logs),
            "tools": {},
            "personas": {},
            "status": {"success": 0, "failed": 0, "warning": 0},
            "total_duration": 0.0,
        }

        for log in logs:
            # 工具统计
            tool = log.get("tool", "unknown")
            stats["tools"][tool] = stats["tools"].get(tool, 0) + 1

            # 人格统计
            persona = log.get("persona", "unknown")
            stats["personas"][persona] = stats["personas"].get(persona, 0) + 1

            # 状态统计
            status = log.get("status", "unknown")
            if status in stats["status"]:
                stats["status"][status] += 1

            # 时长统计
            duration = log.get("duration", 0)
            if isinstance(duration, (int, float)):
                stats["total_duration"] += duration

        return stats

    @staticmethod
    def print_stats():
        """打印统计信息"""
        logs = ActionLogger.get_today_logs()
        stats = ActionLogger.get_stats(logs)

        print("\n╔════════════════════════════════════════════════════════════╗")
        print("║          龍魂每日操作统计 · Action Log Stats                ║")
        print("╚════════════════════════════════════════════════════════════╝\n")

        print(f"📊 总体统计")
        print(f"  • 今日操作: {stats['total']} 笔")
        print(f"  • 总耗时: {stats['total_duration']:.2f} 秒")
        print(f"  • 成功: {stats['status']['success']} 笔")
        print(f"  • 失败: {stats['status']['failed']} 笔")
        print(f"  • 警告: {stats['status']['warning']} 笔")

        print(f"\n🔧 工具分布 ({len(stats['tools'])} 个)")
        for tool, count in sorted(stats['tools'].items(), key=lambda x: -x[1]):
            print(f"  • {tool}: {count} 笔")

        print(f"\n👥 人格分布 ({len(stats['personas'])} 个)")
        for persona, count in sorted(stats['personas'].items(), key=lambda x: -x[1]):
            print(f"  • {persona}: {count} 笔")

        print("")

    @staticmethod
    def export_report(date=None):
        """导出日志报告

        Args:
            date (str): 日期 (YYYY-MM-DD，默认今天)

        Returns:
            str: 报告文本
        """
        if date is None:
            date = now_bj().strftime("%Y-%m-%d")

        logs = []
        if LOG_FILE.exists():
            with open(LOG_FILE) as f:
                for line in f:
                    try:
                        record = json.loads(line)
                        if record.get("date", "").startswith(date):
                            logs.append(record)
                    except:
                        pass

        stats = ActionLogger.get_stats(logs)

        report = f"""
═══════════════════════════════════════════════════════════
龍魂每日操作审计报告 · {date}
═══════════════════════════════════════════════════════════

📊 统计概览
  • 总操作数: {stats['total']} 笔
  • 成功率: {100.0 * stats['status']['success'] / max(1, stats['total']):.1f}%
  • 总耗时: {stats['total_duration']:.2f} 秒
  • 平均耗时: {stats['total_duration'] / max(1, stats['total']):.2f} 秒/笔

🔧 工具使用
"""
        for tool, count in sorted(stats['tools'].items(), key=lambda x: -x[1]):
            report += f"  • {tool}: {count} 笔\n"

        report += f"\n👥 人格参与\n"
        for persona, count in sorted(stats['personas'].items(), key=lambda x: -x[1]):
            report += f"  • {persona}: {count} 笔\n"

        report += f"""
═══════════════════════════════════════════════════════════
#龍芯⚡️{date}-ACTION-LOG-REPORT
"""

        return report


@contextmanager
def log_operation(action, tool, persona=None, dna=None):
    """上下文管理器：自动计时操作

    用法:
        with log_operation("任务执行", "my_tool", persona="P01"):
            # 执行代码
            do_something()
    """
    start = time.time()
    try:
        yield
        duration = time.time() - start
        ActionLogger.log(action, tool, status="success", persona=persona,
                        duration=duration, dna=dna)
    except Exception as e:
        duration = time.time() - start
        ActionLogger.log(action, tool, status="failed", persona=persona,
                        duration=duration, dna=dna, error=str(e))
        raise


# CLI 接口
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法:")
        print("  python3 action_logger.py stats    # 显示今天统计")
        print("  python3 action_logger.py report   # 导出报告")
        print("  python3 action_logger.py log <action> <tool> [persona]")
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "stats":
        ActionLogger.print_stats()
    elif cmd == "report":
        date = sys.argv[2] if len(sys.argv) > 2 else None
        print(ActionLogger.export_report(date))
    elif cmd == "log":
        if len(sys.argv) < 4:
            print("❌ 用法: python3 action_logger.py log <action> <tool> [persona]")
            sys.exit(1)
        action = sys.argv[2]
        tool = sys.argv[3]
        persona = sys.argv[4] if len(sys.argv) > 4 else None
        ActionLogger.log(action, tool, persona=persona)
        print(f"✅ 已记录: {action}")
    else:
        print(f"❌ 未知命令: {cmd}")
        sys.exit(1)
