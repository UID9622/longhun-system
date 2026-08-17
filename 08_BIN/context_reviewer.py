#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# -*- coding: utf-8 -*-
"""
🐉 上下文复盘模块
获取会话历史、项目状态、用户偏好，关联输入到当前任务链

DNA: #龍芯⚡️丙午·丙申·壬戌·辰时-CONTEXT-REVIEW-UID9622
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List


class ContextReviewer:
    """上下文复盘器"""

    def __init__(self, project_root: str = None, longhun_home: str = None):
        self.project_root = Path(project_root or os.environ.get("LONGHUN_HOME", str(Path.home() / "longhun-system")))
        self.longhun_home = Path(longhun_home or os.environ.get("LONGHUN_USER_HOME", str(Path.home() / ".longhun")))

        self.memory_dir = self.longhun_home / "memory"
        self.memory_dir.mkdir(parents=True, exist_ok=True)

        self.state_dir = self.project_root / ".state"
        self.state_dir.mkdir(parents=True, exist_ok=True)

        self.config_dir = self.longhun_home / "configs"
        self.config_dir.mkdir(parents=True, exist_ok=True)

    def get_conversation_history(self, limit: int = 20) -> List[Dict]:
        """获取会话历史"""
        history_file = self.memory_dir / "conversation_history.jsonl"
        history = []
        if history_file.exists():
            with open(history_file, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        record = json.loads(line)
                        history.append(record)
                    except Exception:
                        continue
        return history[-limit:]

    def get_project_state(self) -> Dict:
        """获取项目当前状态"""
        state_file = self.state_dir / "emotion_project_state.json"
        if state_file.exists():
            try:
                with open(state_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return {
            "last_action": "无",
            "current_task": "无",
            "files": [],
            "updated_at": datetime.now().isoformat(),
        }

    def get_user_preferences(self) -> Dict:
        """获取用户偏好设置"""
        pref_file = self.config_dir / "user_preferences.json"
        if pref_file.exists():
            try:
                with open(pref_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return {
            "default_execution_mode": "dry-run",
            "emotion_handling": "ignore",
            "auto_correct_typos": True,
            "dangerous_commands_policy": "block",
            "max_history": 100,
        }

    def review(self, input_text: str) -> Dict:
        """执行上下文复盘"""
        history = self.get_conversation_history()
        state = self.get_project_state()
        prefs = self.get_user_preferences()

        recent_tasks = []
        for record in history[-10:]:
            if record.get("intent") in ["execute", "query", "fix", "config", "deploy", "test"]:
                recent_tasks.append(record)

        likely_task = None
        for task in recent_tasks:
            keywords = task.get("keywords", []) + [task.get("target", "")]
            if any(kw and kw in input_text for kw in keywords):
                likely_task = task
                break

        return {
            "history": history,
            "state": state,
            "preferences": prefs,
            "recent_tasks": recent_tasks,
            "likely_task": likely_task,
        }

    def update_state(self, new_state: Dict):
        """更新项目状态"""
        state_file = self.state_dir / "emotion_project_state.json"
        current = {}
        if state_file.exists():
            try:
                with open(state_file, "r", encoding="utf-8") as f:
                    current = json.load(f)
            except Exception:
                pass
        current.update(new_state)
        current["updated_at"] = datetime.now().isoformat()
        with open(state_file, "w", encoding="utf-8") as f:
            json.dump(current, f, indent=2, ensure_ascii=False)

    def append_history(self, record: Dict):
        """追加会话历史"""
        history_file = self.memory_dir / "conversation_history.jsonl"
        with open(history_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")


# 测试
if __name__ == "__main__":
    reviewer = ContextReviewer()
    sample = [
        {"role": "user", "content": "帮我修复登录bug", "intent": "fix", "keywords": ["登录", "bug"], "target": "登录服务"},
        {"role": "assistant", "content": "执行了登录修复", "intent": "fix_done"},
    ]
    for rec in sample:
        reviewer.append_history(rec)

    context = reviewer.review("这个登录问题怎么还没好，赶紧处理")
    print(json.dumps(context, indent=2, ensure_ascii=False, default=str))
