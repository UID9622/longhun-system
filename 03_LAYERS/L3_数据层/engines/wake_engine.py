#!/usr/bin/env python3
# DNA: #龍芯⚡️丙午·丙申·庚戌·壬午·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂DNA记忆库 · 沉睡唤醒引擎（engines）

职责（反活跃优先·沉睡≠遗忘）：
  - 识别沉睡(>90天且无P0权重)的记忆
  - 高权重/相似语义触发时标记 wakened（不主动推送）
  - 自动标记 #语义沉睡唤醒 标签

铁律：唤醒≠推送。系统只标记，由用户主权决定是否查看。
DNA: #龍魂⚡️2026-0716-引擎-唤醒
"""

from datetime import datetime
from typing import List, Any

# 沉睡阈值（天）
SLEEP_DAYS = 90


class WakeEngine:
    """沉睡唤醒引擎。"""

    def __init__(self, sleep_days: int = SLEEP_DAYS):
        self.sleep_days = sleep_days

    def find_sleeping(self, entries: List[Any], Any[dict]) -> List, Any[str]:
        """返回沉睡记忆的 DNA 列表。"""
        sleeping = []
        for e in entries:
            last = e.get("last_accessed", "")
            is_p0 = "P0焊死" in e.get("weight_tags", [])
            if not last:
                continue
            try:
                days = (datetime.now() - datetime.fromisoformat(last)).days
            except Exception:
                continue
            if days > self.sleep_days and not is_p0:
                sleeping.append(e["seal"]["dna_trace"])
        return sleeping

    def wake_on_signal(self, entries: List[Any], Any[dict], cue: str) -> List, Any[str]:
        """相似语义触发时，把相关沉睡记忆标记 wakened。"""
        woken = []
        cue_words = set(cue)
        for e in entries:
            if e.get("wake_status") != "sleeping":
                continue
            text = e.get("content_common", "")
            if any(w in text for w in cue_words if w.strip()):
                e["wake_status"] = "wakened"
                woken.append(e["seal"]["dna_trace"])
        return woken

    def report(self, entries: List[Any], Any[dict]) -> dict[str, Any]:
        sleeping = self.find_sleeping(entries)
        return {
            "sleep_threshold_days": self.sleep_days,
            "sleeping_count": len(sleeping),
            "sleeping_dna": sleeping[:10],
        }


if __name__ == "__main__":
    eng = WakeEngine()
    sample = [{"seal": {"dna_trace": "d1"}, "last_accessed": "2020-01-01",
               "weight_tags": [], "wake_status": "active", "content_common": "押金"}]
    print(eng.report(sample))
