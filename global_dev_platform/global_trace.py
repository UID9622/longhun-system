#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂全球开发者平台 · 全球痕迹系统 v1.0
DNA: #龍芯⚡️丙午·丙申·壬戌·亥时·䷲震-GLOBAL-TRACE-v1.0
创建者: 诸葛鑫（UID9622）
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
协议: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
核心理念:
  每个人在这个世界的每一次创造·每一行代码·每一次发布
  都应该被记录、被承认、永久存在。
  这不是日志，这是「存在证明」。
  DNA 一律走统一干支卦引擎。
"""

import json
import uuid
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any, List

from lh_dna import lh_dna

TRACE_ROOT = Path.home() / "longhun-system" / "global_dev_platform" / "traces"


class GlobalTrace:
    """
    全球痕迹系统
    每一次创作行为都生成一条不可篡改的痕迹记录
    格式: JSONL append-only（和沙箱审计钩子同一设计哲学）
    """

    EVENT_TYPES = {
        "FIRST_CODE":    "✨ 第一行代码",
        "APP_CREATED":   "🏗️ App 骨架诞生",
        "APP_BUILT":     "🔨 应用构建成功",
        "APP_TESTED":    "✅ 测试通过",
        "APP_LAUNCHED":  "🚀 应用已发布",
        "SHORTCUT_RUN":  "⚡️ 快捷指令执行",
        "SCREENSHOT":    "📸 截图留存",
        "WORLD_MARK":    "🌍 世界足迹打点",
        "IDEA_BORN":     "💡 想法诞生",
        "CODE_COMMIT":   "📝 代码提交",
    }

    def __init__(self, user_id: str = "UID9622"):
        self.user_id   = user_id
        self.trace_dir = TRACE_ROOT / user_id
        self.trace_dir.mkdir(parents=True, exist_ok=True)
        self.trace_file = self.trace_dir / "traces.jsonl"
        self.world_file = TRACE_ROOT / "world_traces.jsonl"  # 全球共享
        self.world_file.parent.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def _dna(event: str, user_id: str) -> str:
        """统一 DNA · 干支卦引擎"""
        return lh_dna(module="TRACE", action=event[:12].upper(), version="v1.0",
                      anchor=f"{event}:{user_id}")

    def record(self, event_type: str,
               title: str,
               detail: str = "",
               platform: str = "both",
               location: Optional[str] = None,
               extra: Optional[Dict] = None) -> str:
        """
        记录一条存在痕迹
        返回 DNA（存在证明）
        """
        dna = self._dna(event_type, self.user_id)
        trace_id = str(uuid.uuid4())[:8].upper()

        entry = {
            "trace_id":   trace_id,
            "user_id":    self.user_id,
            "event_type": event_type,
            "event_label": self.EVENT_TYPES.get(event_type, event_type),
            "title":      title,
            "detail":     detail,
            "platform":   platform,
            "location":   location,
            "timestamp":  datetime.now().isoformat(),
            "dna":        dna,
            "extra":      extra or {},
        }

        # 写入个人痕迹
        with open(self.trace_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

        # 写入全球痕迹（匿名化）
        world_entry = {
            "trace_id":  trace_id,
            "event_type": event_type,
            "platform":  platform,
            "timestamp": entry["timestamp"],
            "location":  location,
            "dna":       dna,
        }
        with open(self.world_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(world_entry, ensure_ascii=False) + "\n")

        print(f"  {self.EVENT_TYPES.get(event_type, '📌')} {title}")
        print(f"     DNA (存在证明): {dna}")
        return dna

    def my_traces(self, n: int = 20) -> List[Dict]:
        """查看我的最近痕迹"""
        try:
            lines = self.trace_file.read_text("utf-8").strip().splitlines()
            return [json.loads(l) for l in lines[-n:] if l.strip()]
        except FileNotFoundError:
            return []

    def world_count(self) -> int:
        """全球痕迹总数"""
        try:
            return len(self.world_file.read_text("utf-8").strip().splitlines())
        except FileNotFoundError:
            return 0

    def print_my_story(self) -> None:
        """打印我的创作故事"""
        traces = self.my_traces(50)
        if not traces:
            print("  还没有痕迹——写下第一行代码，就从这里开始 🌱")
            return
        print(f"\n🐉 {self.user_id} 的创作故事 ({len(traces)} 条)\n")
        for t in traces:
            ts = t["timestamp"][:16].replace("T", " ")
            print(f"  {ts}  {t['event_label']}  {t['title']}")
        print(f"\n  全球共有 {self.world_count()} 条存在痕迹 🌍")


if __name__ == "__main__":
    trace = GlobalTrace(user_id="UID9622")
    trace.record("FIRST_CODE",  "龍魂笔记 iOS",      platform="iOS",     location="中国")
    trace.record("FIRST_CODE",  "龍魂笔记 HarmonyOS", platform="harmony", location="中国")
    trace.record("APP_CREATED", "双平台 App 骨架诞生", platform="both")
    trace.print_my_story()
