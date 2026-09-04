#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""
🐉 龍魂系统 · 任务管理引擎 v2.0
Task Manager v2.0 · 支持跳跃式操作 + 自动去重

DNA: #龍芯⚡️丙午·癸巳·庚戌·壬午·䷕贲-TASK-MANAGER-v2.0
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any
import hashlib

HOME = Path.home()
TASK_QUEUE = HOME / ".龍魂/task_queue.jsonl"
DEDUP_REGISTRY = HOME / ".龍魂/dedup_registry.json"
JUMP_LOG_DIR = HOME / ".龍魂/jump_log"

# ═══════════════════════════════════════════════════════════════════════════
# 任务管理类
# ═══════════════════════════════════════════════════════════════════════════

class TaskManager:
    def __init__(self):
        self.tasks = self.load_tasks()
        self.dedup_registry = self.load_dedup_registry()
        self.ensure_dirs()

    def ensure_dirs(self):
        """确保所有目录存在"""
        TASK_QUEUE.parent.mkdir(parents=True, exist_ok=True)
        JUMP_LOG_DIR.mkdir(parents=True, exist_ok=True)

    def load_tasks(self) -> List[Dict]:
        """加载任务队列"""
        tasks = []
        if TASK_QUEUE.exists():
            with open(TASK_QUEUE, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        tasks.append(json.loads(line))
        return tasks

    def load_dedup_registry(self) -> Dict[str, Any]:
        """加载去重登记簿"""
        if DEDUP_REGISTRY.exists():
            with open(DEDUP_REGISTRY, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {"dedup_rules": [], "redundant_items": []}

    def add_task(self, title: str, priority: int = 3, labels: List[str] = None) -> str:
        """添加新任务"""
        task_id = f"TASK-{datetime.now().strftime('%Y%m%d-%H%M%S')}"

        task = {
            "task_id": task_id,
            "title": title,
            "status": "pending",
            "priority": priority,
            "created_at": datetime.now().isoformat(),
            "due_at": None,
            "assigned_to": "UID9622",
            "depends_on": [],
            "labels": labels or [],
            "description": "",
            "jump_log": [],
            "owner_context": "",
            "dna_signature": self.generate_dna(title),
            "updated_at": datetime.now().isoformat()
        }

        self.tasks.append(task)
        self.save_tasks()
        return task_id

    def jump_task(self, from_task_id: str, to_task_id: str, reason: str = ""):
        """记录任务跳跃"""
        # 找到源任务和目标任务
        from_task = next((t for t in self.tasks if t['task_id'] == from_task_id), None)
        to_task = next((t for t in self.tasks if t['task_id'] == to_task_id), None)

        if not from_task or not to_task:
            print("❌ 任务不存在")
            return

        # 暂停源任务
        from_task['status'] = 'paused'
        from_task['updated_at'] = datetime.now().isoformat()

        # 开始目标任务
        to_task['status'] = 'in_progress'
        to_task['updated_at'] = datetime.now().isoformat()

        # 记录跳跃
        jump_record = {
            "from": from_task_id,
            "to": to_task_id,
            "reason": reason,
            "at": datetime.now().isoformat()
        }

        from_task['jump_log'].append(jump_record)
        self.save_tasks()
        self.log_jump(from_task_id, to_task_id, reason)

        print(f"✅ 跳跃记录: {from_task_id} → {to_task_id}")
        print(f"   理由: {reason}")

    def get_pending_tasks(self) -> List[Dict]:
        """获取所有未完成任务 (按优先级排序)"""
        pending = [t for t in self.tasks if t['status'] != 'completed']

        # 应用优先级衰减
        for task in pending:
            task['current_priority'] = self.calculate_priority_decay(task)

        # 按优先级排序
        pending.sort(key=lambda x: x['current_priority'], reverse=True)
        return pending

    def calculate_priority_decay(self, task: Dict[str, Any]) -> float:
        """计算考虑衰减的优先级"""
        created = datetime.fromisoformat(task['created_at'])
        age_days = (datetime.now() - created).days

        # Decay 函数
        if age_days < 1:
            decay = 1.0
        elif age_days < 3:
            decay = 0.9
        elif age_days < 7:
            decay = 0.7
        elif age_days < 30:
            decay = 0.4
        else:
            decay = 0.1

        return task['priority'] * decay

    def auto_deduplicate(self) -> Dict[str, Any]:
        """自动去重"""
        duplicates = []

        # 简单的相似度检查 (通过标签)
        for i, task1 in enumerate(self.tasks):
            for task2 in self.tasks[i+1:]:
                # 检查是否有公共标签且标题相似
                common_labels = set(task1.get('labels', [])) & set(task2.get('labels', []))

                if common_labels and task1['status'] != 'completed' and task2['status'] != 'completed':
                    # 计算标题相似度 (简单版本)
                    if self.string_similarity(task1['title'], task2['title']) > 0.7:
                        duplicates.append({
                            "task1": task1['task_id'],
                            "task2": task2['task_id'],
                            "similarity": 0.85,
                            "labels": list(common_labels)
                        })

        # 记录去重建议
        if duplicates:
            for dup in duplicates:
                self.dedup_registry['redundant_items'].append({
                    "items": [dup['task1'], dup['task2']],
                    "appears_in": [dup['task1'], dup['task2']],
                    "deduplicated": False,
                    "canonical_source": dup['task1'],
                    "reason": f"相似度 {dup['similarity']:.1%}，标签 {dup['labels']}"
                })

            self.save_dedup_registry()

        return {"duplicates_found": len(duplicates), "items": duplicates}

    def generate_dna(self, content: str) -> str:
        """为任务生成 DNA 签证"""
        hash_val = hashlib.sha256(content.encode()).hexdigest()[:8]
        return f"#龍芯⚡️{datetime.now().strftime('%Y%m%d%H%M%S')}-TASK-{hash_val.upper()}"

    def string_similarity(self, s1: str, s2: str) -> float:
        """计算字符串相似度 (简单版)"""
        longer = s1 if len(s1) > len(s2) else s2
        shorter = s2 if len(s1) > len(s2) else s1

        if len(longer) == 0:
            return 1.0

        edit_distance = self.edit_distance(longer, shorter)
        return (len(longer) - edit_distance) / float(len(longer))

    def edit_distance(self, s1: str, s2: str) -> int:
        """计算编辑距离"""
        if len(s1) < len(s2):
            return self.edit_distance(s2, s1)

        if len(s2) == 0:
            return len(s1)

        previous_row = range(len(s2) + 1)
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row

        return previous_row[-1]

    def log_jump(self, from_id: str, to_id: str, reason: str):
        """记录跳跃到日志文件"""
        log_file = JUMP_LOG_DIR / f"jump_log_{datetime.now().strftime('%Y%m%d')}.json"

        jump_entry = {
            "timestamp": datetime.now().isoformat(),
            "from": from_id,
            "to": to_id,
            "reason": reason
        }

        logs = []
        if log_file.exists():
            with open(log_file, 'r', encoding='utf-8') as f:
                logs = json.load(f)

        logs.append(jump_entry)

        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump(logs, f, indent=2, ensure_ascii=False)

    def save_tasks(self):
        """保存任务队列"""
        with open(TASK_QUEUE, 'w', encoding='utf-8') as f:
            for task in self.tasks:
                f.write(json.dumps(task, ensure_ascii=False) + '\n')

    def save_dedup_registry(self):
        """保存去重登记簿"""
        with open(DEDUP_REGISTRY, 'w', encoding='utf-8') as f:
            json.dump(self.dedup_registry, f, indent=2, ensure_ascii=False)

    def display_pending_tasks(self):
        """显示未完成任务"""
        pending = self.get_pending_tasks()

        print("【上次遗留的任务】")
        print("══════════════════════════════════════════════════════")

        for i, task in enumerate(pending[:10], 1):  # 只显示前 10 个
            age = (datetime.now() - datetime.fromisoformat(task['created_at'])).days
            current_priority = self.calculate_priority_decay(task)

            status_icon = {
                'pending': '⏳',
                'in_progress': '▶️',
                'paused': '⏸',
                'blocked': '🚫',
                'completed': '✅'
            }.get(task['status'], '❓')

            print(f"{i}. {status_icon} {task['task_id']}: {task['title']}")
            print(f"   优先级: {task['priority']} → {current_priority:.1f} (衰减 {age} 天)")
            print(f"   标签: {', '.join(task.get('labels', []))}")
            print()

# ═══════════════════════════════════════════════════════════════════════════
# 主程序
# ═══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import sys

    manager = TaskManager()

    if len(sys.argv) < 2:
        print("用法: python3 task_manager_v2.py [command] [options]")
        print("\n命令:")
        print("  add --title '标题' --priority 3 --label tag1,tag2")
        print("  jump --from TASK-001 --to TASK-002 --reason '原因'")
        print("  list")
        print("  dedup")
        sys.exit(1)

    command = sys.argv[1]

    if command == "add":
        title = sys.argv[sys.argv.index("--title") + 1] if "--title" in sys.argv else "未命名任务"
        priority = int(sys.argv[sys.argv.index("--priority") + 1]) if "--priority" in sys.argv else 3
        labels = sys.argv[sys.argv.index("--label") + 1].split(",") if "--label" in sys.argv else []

        task_id = manager.add_task(title, priority, labels)
        print(f"✅ 任务已添加: {task_id}")
        print(f"   标题: {title}")
        print(f"   优先级: {priority}")
        print(f"   标签: {labels}")

    elif command == "jump":
        from_id = sys.argv[sys.argv.index("--from") + 1] if "--from" in sys.argv else None
        to_id = sys.argv[sys.argv.index("--to") + 1] if "--to" in sys.argv else None
        reason = sys.argv[sys.argv.index("--reason") + 1] if "--reason" in sys.argv else ""

        if from_id and to_id:
            manager.jump_task(from_id, to_id, reason)
        else:
            print("❌ 需要指定 --from 和 --to")

    elif command == "list":
        manager.display_pending_tasks()

    elif command == "dedup":
        result = manager.auto_deduplicate()
        print(f"✅ 去重完成")
        print(f"   检测到 {result['duplicates_found']} 个可能的重复任务")
        for dup in result['items']:
            print(f"   - {dup['task1']} ≈ {dup['task2']}")

    else:
        print(f"❌ 未知命令: {command}")
