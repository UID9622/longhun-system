# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
#龍芯⚡️丙午·辛未·乙酉·PROMPT-LIBRARY-LOADER-v1.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
龍魂·提示词库查询加载器 v1.0
===========================
DNA: #龍芯⚡️丙午·辛未·乙酉·PROMPT-LIBRARY-LOADER-v1.0
用途: 供 lh_claude_bridge / 语义注册表 / 任意 AI 助手在对话时直接调用提示词库。
      加载 L7_数据层/notion_prompt_library/library_v2.json，提供按助手/关键词检索。

用法 (作为模块):
  from bin.lh_prompt_library import 提示词库
  lib = 提示词库()
  lib.按助手("宝宝")            # → 该助手全部真模板
  lib.搜索("DNA")              # → 含关键词的模板
  lib.系统附录(助手="宝宝")      # → 拼好的 system 附录字符串

用法 (命令行):
  python3 bin/lh_prompt_library.py list 宝宝
  python3 bin/lh_prompt_library.py search DNA
  python3 bin/lh_prompt_library.py assistants
"""

import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Any

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_LIBRARY = ROOT / "L7_数据层" / "notion_prompt_library" / "library_v2.json"

# 助手别名归一
ASSISTANT_ALIASES = {
    "宝宝": "宝宝", "baobao": "宝宝", "baby": "宝宝", "p02": "宝宝",
    "通心译": "通心译", "tongxinyi": "通心译", "tx": "通心译",
    "claude": "Claude", "克劳德": "Claude",
    "通用": "通用", "common": "通用", "共享": "通用", "all": "通用",
}


def 归一助手(name: str) -> str:
    if not name:
        return "通用"
    return ASSISTANT_ALIASES.get(name.strip().lower(), name.strip())


class 提示词库:
    def __init__(self, path: Optional[Path] = None):
        self.path = Path(path) if path else DEFAULT_LIBRARY
        self._data = None
        self._loaded = False

    def 加载(self) -> dict[str, Any]:
        if self._loaded:
            return self._data
        if not self.path.exists():
            self._data = {"meta": {}, "prompts": []}
            self._loaded = True
            return self._data
        try:
            self._data = json.loads(self.path.read_text(encoding="utf-8"))
        except Exception:
            self._data = {"meta": {}, "prompts": []}
        self._loaded = True
        return self._data

    @property
    def 条目(self) -> List[dict]:
        return self.加载().get("prompts", [])

    def 按助手(self, assistant: str) -> List[dict]:
        a = 归一助手(assistant)
        return [p for p in self.条目 if p.get("assistant") == a]

    def 搜索(self, keyword: str, assistant: Optional[str] = None) -> List[dict]:
        kw = keyword.lower()
        pool = self.按助手(assistant) if assistant else self.条目
        return [p for p in pool if kw in p.get("content", "").lower()
                or kw in p.get("title", "").lower()]

    def 系统附录(self, assistant: Optional[str] = None,
              keyword: Optional[str] = None, max_chars: int = 3000) -> str:
        """拼一段可注入 system 提示词的附录。"""
        if keyword:
            items = self.搜索(keyword, assistant)
        elif assistant:
            items = self.按助手(assistant)
        else:
            items = self.条目

        if not items:
            return ""

        a_label = 归一助手(assistant) if assistant else "全部"
        head = f"\n\n{'='*20}\n【龍魂提示词库·{a_label}】以下为可复用提示词模板，按需调用：\n"
        lines = [head]
        used = len(head)
        for i, p in enumerate(items, 1):
            block = f"\n[{p['assistant']}·{p['kind']}] {p['content']}"
            if used + len(block) > max_chars:
                lines.append(f"\n… (已截断，共 {len(items)} 条，更多见 library_v2.json)")
                break
            lines.append(block)
            used += len(block)
        return "".join(lines)

    def 统计(self) -> dict[str, Any]:
        d = self.加载()
        return {
            "assistants": d.get("meta", {}).get("by_assistant", {}),
            "total": d.get("meta", {}).get("total_prompts", 0),
            "pages": d.get("meta", {}).get("total_pages", 0),
        }


# ── 命令行入口 ──
def _cli():
    lib = 提示词库()
    cmd = sys.argv[1] if len(sys.argv) > 1 else "stats"
    if cmd == "assistants":
        print("助手分库:", json.dumps(lib.统计()["assistants"], ensure_ascii=False))
    elif cmd == "stats":
        print(json.dumps(lib.统计(), ensure_ascii=False, indent=2))
    elif cmd == "list":
        a = sys.argv[2] if len(sys.argv) > 2 else "通用"
        for i, p in enumerate(lib.按助手(a), 1):
            print(f"{i}. [{p['kind']}] {p['content'][:90]}")
    elif cmd == "search":
        kw = sys.argv[2] if len(sys.argv) > 2 else ""
        a = sys.argv[3] if len(sys.argv) > 3 else None
        for i, p in enumerate(lib.搜索(kw, a), 1):
            print(f"{i}. [{p['assistant']}] {p['content'][:90]}")
    else:
        print("用法: list <助手> | search <词> [助手] | assistants | stats")


if __name__ == "__main__":
    _cli()
