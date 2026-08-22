#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · 中英双语命令路由器 v1.0
# 层级: L1_引擎层
# DNA: #龍芯⚡️丙午·丙申·丁酉·癸卯·䷵归妹-BILINGUAL-ROUTER-UID9622
# 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# License: MulanPSL v2

功能:
  让龍魂系统命令同时接受英文规范名与中文/其他语言别名，
  不强制任何语言作为计算机底座。英文是 canonical（机器稳定名），
  其他语言是 alias（人类友好入口）。

用法:
  router = BilingualCommandRouter()
  router.resolve_command("评估")       # -> "assess"
  router.resolve_command("assess")     # -> "assess"
  router.resolve_command("批量评估")   # -> "all-assess"
  router.resolve_pain_point("数据主权") # -> "data_sovereignty"
"""

import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_MAP_PATH = PROJECT_ROOT / "config" / "bilingual_command_map.json"
ENV_VAR = "LH_BILINGUAL_CMD_FILE"

DNA = "#龍芯⚡️丙午·丙申·丁酉·癸卯·䷵归妹-BILINGUAL-ROUTER-UID9622"
CONFIRM_CODE = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
GPG_KEY = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"


def _normalize(s: str) -> str:
    """统一归一化：去首尾空白、统一连字符、小写"""
    return s.strip().lower().replace("_", "-").replace(" ", "-")


class BilingualCommandRouter:
    """双语命令路由器"""

    def __init__(self, map_path: Optional[Path] = None):
        self.map_path = map_path or self._default_path()
        self.data: Dict[str, Any] = self._load()
        self._index: Dict[str, Dict[str, str]] = {}
        self._build_index()

    @staticmethod
    def _default_path() -> Path:
        env = os.environ.get(ENV_VAR, "").strip()
        if env:
            p = Path(env).expanduser()
            if p.exists():
                return p.resolve()
        return DEFAULT_MAP_PATH.resolve()

    def _load(self) -> Dict[str, Any]:
        empty = {"meta": {}, "commands": {}, "pain_points": {}}
        if not self.map_path.exists():
            return empty
        try:
            with open(self.map_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            if not isinstance(data, dict):
                print(f"🟡 双语映射文件格式异常（非 dict）: {self.map_path}")
                return empty
            return data
        except Exception as e:
            print(f"🟡 双语映射文件解析失败: {self.map_path} -> {e}")
            return empty

    def _build_index(self) -> None:
        """构建 alias -> canonical 反向索引"""
        self._index = {}
        for category in ("commands", "pain_points"):
            self._index[category] = {}
            entries = self.data.get(category, {})
            for canonical, langs in entries.items():
                # 规范名自身也加入索引
                self._index[category][_normalize(canonical)] = canonical
                for lang, aliases in langs.items():
                    for alias in aliases:
                        self._index[category][_normalize(alias)] = canonical

    def resolve(self, name: str, category: str = "commands") -> Optional[str]:
        """将任意别名解析为规范英文名；未命中返回 None"""
        if not name:
            return None
        return self._index.get(category, {}).get(_normalize(name))

    def resolve_command(self, name: str) -> Optional[str]:
        return self.resolve(name, "commands")

    def resolve_pain_point(self, name: str) -> Optional[str]:
        return self.resolve(name, "pain_points")

    def aliases(self, canonical: str, category: str = "commands") -> List[str]:
        """返回某个规范名在所有语言下的全部别名"""
        entry = self.data.get(category, {}).get(canonical, {})
        result: List[str] = []
        for aliases in entry.values():
            result.extend(aliases)
        return result

    def add_alias(self, canonical: str, alias: str, category: str = "commands", lang: str = "zh") -> None:
        """运行时动态添加别名（不写回文件）"""
        self.data.setdefault(category, {}).setdefault(canonical, {}).setdefault(lang, []).append(alias)
        self._build_index()

    def supported_canonicals(self, category: str = "commands") -> List[str]:
        return list(self.data.get(category, {}).keys())


def cli():
    import argparse
    parser = argparse.ArgumentParser(description="龍魂中英双语命令路由器")
    parser.add_argument("name", help="待解析的命令或痛点名")
    parser.add_argument("--category", choices=["commands", "pain_points"], default="commands", help="映射类别")
    parser.add_argument("--map", help=f"自定义映射文件路径（默认 {DEFAULT_MAP_PATH}）")
    args = parser.parse_args()

    router = BilingualCommandRouter(Path(args.map) if args.map else None)
    canonical = router.resolve(args.name, args.category)
    if canonical:
        print(f"{args.name} -> {canonical}")
        aliases = router.aliases(canonical, args.category)
        if aliases:
            print(f"  aliases: {', '.join(aliases)}")
    else:
        print(f"🟡 未识别: {args.name}")
        print(f"  可用规范名: {', '.join(router.supported_canonicals(args.category))}")


if __name__ == "__main__":
    cli()

# ⛓️ 龍魂DNA接龍链 ──────────────────────────────
# DNA:V1|丙午·丙申·癸亥·辰时·䷗复|P04鲁班|创建|双语路由封装|bhash:89a45426|chash:6d92f33d|←GENESIS
# ⛓️ 龍魂DNA接龍末端 ──────────────────────────────
