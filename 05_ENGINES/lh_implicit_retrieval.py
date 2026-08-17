#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · 无意识检索引擎 (Implicit Retrieval Engine)
DNA: #龍芯⚡️丙午·丙申·壬戌·巳时-IMPLICIT-RETRIEVAL-UID9622
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
License: MulanPSL v2

功能: 用户无需点击搜索，系统根据当前上下文自动推送可能需要的文件/主题/命令。
      整合：上下文感知 + 向量语义 + 行为权重 + 协同涌现。
      鲲鹏 ARM64 原生：不依赖外部 API，本地 Ollama 可选。
"""

import hashlib
import json
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from engines.lh_context_engine import capture_context
from engines.lh_vector_index import VectorIndex
from engines.lh_behavior_learner import BehaviorLearner
from engines.lh_collective_intel import CollectiveIntel

DATA_DIR = PROJECT_ROOT / ".state" / "implicit_retrieval"
DATA_DIR.mkdir(parents=True, exist_ok=True)

DNA_PREFIX = "#龍芯⚡️"
ENGINE_DNA = f"{DNA_PREFIX}丙午·丙申·壬戌·巳时-IMPLICIT-RETRIEVAL-UID9622"
UID = "UID9622"
CST = timezone(timedelta(hours=8))


def now_iso() -> str:
    return datetime.now(CST).isoformat()


def _file_id(path: str) -> str:
    return hashlib.sha256(path.encode()).hexdigest()[:16]


class ImplicitRetrieval:
    """无意识检索：融合四层信号，零点击推送"""

    def __init__(self):
        self.vector_idx = VectorIndex()
        self.learner = BehaviorLearner()
        self.collective = CollectiveIntel()

    def push(
        self, context: Optional[Dict[str, Any]] = None, top_k: int = 10
    ) -> Dict[str, Any]:
        """根据上下文推送信息"""
        if context is None:
            context = capture_context()

        # 1. 从上下文中抽取查询线索
        clues: List[str] = []
        recent_files = context.get("recent_files", [])[:5]
        recent_py = context.get("recent_py_files", [])[:3]
        clues.extend(Path(f).stem for f in recent_files + recent_py)
        clues.extend(context.get("active_goals", []))
        history = context.get("shell_history", [])
        if history:
            clues.append(history[-1])

        query = " ".join(str(c) for c in clues if c) or "龍魂系统"

        # 2. 向量语义候选
        semantic = self.vector_idx.search(query, top_k=top_k * 2)

        # 3. 行为推荐候选
        recent_ids = [_file_id(str(PROJECT_ROOT / f)) for f in recent_files]
        behavioral = self.learner.recommend_from_context(recent_ids, limit=top_k)

        # 4. 协同涌现候选：取最近文件的共现
        collective: List[Dict[str, Any]] = []
        for f in recent_files:
            fid = _file_id(str(PROJECT_ROOT / f))
            for rel in self.collective.related_items(fid, limit=5):
                collective.append(
                    {"item_id": rel["item"], "score": rel["weight"] * 0.3}
                )

        # 5. 融合打分
        merged: Dict[str, Dict[str, Any]] = {}

        for r in semantic:
            key = r["file_id"]
            merged[key] = {
                "item_id": key,
                "path": r["path"],
                "title": r["title"],
                "summary": r["summary"],
                "score": r["score"] * 1.0,
                "signals": ["semantic"],
            }

        for r in behavioral:
            key = r["item_id"]
            if key in merged:
                merged[key]["score"] += r["weight"] * 0.5
                merged[key]["signals"].append("behavior")
            else:
                merged[key] = {
                    "item_id": key,
                    "path": r.get("name", ""),
                    "title": r.get("name", ""),
                    "summary": "",
                    "score": r["weight"] * 0.5,
                    "signals": ["behavior"],
                }

        for r in collective:
            key = r["item_id"]
            if key in merged:
                merged[key]["score"] += r["score"]
                merged[key]["signals"].append("collective")

        # 排序
        ranked = sorted(merged.values(), key=lambda x: -x["score"])

        return {
            "dna": ENGINE_DNA,
            "timestamp": now_iso(),
            "query": query,
            "context": {
                "cwd": context.get("cwd"),
                "branch": context.get("git_branch"),
                "recent_files": recent_files,
            },
            "recommendations": ranked[:top_k],
        }

    def record_feedback(self, item_id: str, helpful: bool = True):
        """记录用户是否觉得推送有用，强化学习"""
        delta = 1.5 if helpful else -0.5
        self.learner.record(
            item_id=item_id,
            item_type="implicit_push",
            name=item_id,
            weight_delta=delta,
        )


def cli():
    import argparse

    parser = argparse.ArgumentParser(description="龍魂无意识检索引擎")
    parser.add_argument("--push", action="store_true", help="执行零点击推送")
    parser.add_argument("--top", type=int, default=10, help="推送数量")
    parser.add_argument(
        "--feedback", help="记录反馈: item_id=helpful|not_helpful"
    )
    args = parser.parse_args()

    engine = ImplicitRetrieval()

    if args.feedback:
        item_id, rating = args.feedback.split("=", 1)
        engine.record_feedback(item_id, helpful=rating in ("helpful", "true", "1", "yes"))
        print(f"✅ 反馈已记录: {item_id} -> {rating}")
        return

    if args.push or True:
        result = engine.push(top_k=args.top)
        print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    cli()
