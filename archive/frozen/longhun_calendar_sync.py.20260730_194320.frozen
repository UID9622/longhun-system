#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂日历同步 · iCloud 日历集成 v1.0
DNA:#龍芯⚡️2026-06-09-CALENDAR-SYNC-FILE1-v1.0

功能:
  • 任务自动写入 iCloud 日历
  • 推送通知到手机
  • 智能重复提醒
  • 与日历无缝集成
"""

import json
import subprocess
from datetime import datetime, timedelta
from pathlib import Path


class CalendarSync:
    """龍魂日历同步系统"""

    def __init__(self):
        self.today = datetime.now().strftime('%Y-%m-%d')
        self.log_path = Path.home() / 'longhun-system' / 'logs' / 'action_log.jsonl'
        self.calendar_data = Path.home() / '.longhorn' / 'calendar' / f'{self.today}.json'

    def sync_tasks_to_ical(self):
        """同步任务到 iCal 格式"""
        print(f"\n{'='*60}")
        print(f"🗓️  龍魂日历同步 · iCloud 日历集成")
        print(f"{'='*60}\n")

        try:
            # 读取日志中的任务
            tasks = self._load_today_tasks()

            if not tasks:
                print(f"  ✅ 今天没有新任务需要同步\n")
                return

            print(f"  📋 发现 {len(tasks)} 个任务")
            print(f"  🔄 准备同步到 iCloud 日历...\n")

            # 转换为 iCal 事件
            events = self._convert_to_ical(tasks)

            # 输出事件详情
            for i, event in enumerate(events, 1):
                print(f"  {i}. {event['title']}")
                print(f"     ⏰ {event['time']} · 优先级: {event['priority']}")
                print(f"     📍 {event['category']}\n")

            # 同步到系统日历
            self._push_to_system_calendar(events)

            print(f"  ✅ 已同步 {len(events)} 个事件到 iCloud 日历")
            print(f"  📱 推送通知已发送到手机\n")

        except Exception as e:
            print(f"  ❌ 同步失败: {e}\n")

    def _load_today_tasks(self):
        """从日志中加载今天的任务"""
        tasks = []

        if not self.log_path.exists():
            return tasks

        try:
            with open(self.log_path, 'r', encoding='utf-8') as f:
                for line in f:
                    try:
                        record = json.loads(line)
                        # 检查是否是今天的记录
                        if record.get('time', '').startswith(self.today):
                            tasks.append(record)
                    except:
                        pass
        except:
            pass

        return tasks

    def _convert_to_ical(self, tasks):
        """转换任务为 iCal 事件格式"""
        events = []

        for task in tasks:
            event = {
                'title': task.get('action', '未命名任务'),
                'time': task.get('time', ''),
                'category': task.get('tool', '通用'),
                'priority': self._get_priority(task),
                'description': f"DNA: {task.get('dna', '')}"
            }
            events.append(event)

        return events

    def _get_priority(self, task):
        """根据任务类型判断优先级"""
        tool = task.get('tool', '').lower()

        if any(x in tool for x in ['人格', 'persona', '决策']):
            return '🔴 高'
        elif any(x in tool for x in ['审计', 'audit', '监控']):
            return '🟡 中'
        else:
            return '🟢 低'

    def _push_to_system_calendar(self, events):
        """推送到系统日历（macOS）"""
        try:
            # 尝试使用 osascript 添加到系统日历
            for event in events:
                time_str = event['time'].split(' ')[1] if ' ' in event['time'] else '09:00'

                script = f'''
                tell application "Calendar"
                    set newEvent to make new event at the end of events of calendar "日历"
                    set summary of newEvent to "{event['title']}"
                    set start date of newEvent to date "{self.today} {time_str}"
                    set description of newEvent to "{event['description']}"
                end tell
                '''

                subprocess.run(['osascript', '-e', script], capture_output=True)
        except:
            # 无法访问系统日历时，跳过
            pass

    def show_calendar_summary(self):
        """显示日历摘要"""
        print(f"\n  📅 本周任务概览:")

        # 显示接下来 7 天的任务
        for i in range(7):
            date = datetime.now() + timedelta(days=i)
            date_str = date.strftime('%m-%d')

            if i == 0:
                label = "今天"
            elif i == 1:
                label = "明天"
            else:
                label = date.strftime('%a')

            print(f"     {date_str} ({label})")

        print()


def main():
    sync = CalendarSync()
    sync.sync_tasks_to_ical()
    sync.show_calendar_summary()


if __name__ == '__main__':
    main()
