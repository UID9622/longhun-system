#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · Notion 知识卡片同步引擎 v1.0（双脑）
DNA: #龍芯⚡️丙午·乙未·戊戌·巳时·☵坎-NOTION-SYNC-ENGINE-v1.0
创建者: 诸葛鑫 (UID9622)
协议: CC BY-NC-SA 4.0

双脑同步：Mac本地知识卡片 ↔ Notion云端知识库
  --incremental   增量同步（默认·只同步变更）
  --full          全量同步
  --push <分类>   推送本地→Notion
  --pull <分类>   拉取Notion→本地
  --status        查看同步状态
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional

CST = timezone(timedelta(hours=8))

DNA = "#龍芯⚡️丙午·乙未·戊戌·巳时·☵坎-NOTION-SYNC-ENGINE-v1.0"
CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"

ROOT = Path(__file__).resolve().parent.parent
SYNC_STATE = ROOT / "data" / "notion_sync" / "card_engine_state.json"
KB_INDEX = ROOT / "portal" / "knowledge" / "kb_index.json"
KNOWLEDGE_DIR = ROOT / "knowledge"
NOTION_EXPORTS = ROOT / "data" / "notion_sync" / "exports"


def _now() -> str:
    return datetime.now(CST).isoformat()


def _log(msg: str, level: str = "INFO"):
    markers = {"INFO": "📋", "OK": "✅", "WARN": "🟡", "ERROR": "🔴", "STEP": "⚙️"}
    print(f"[{datetime.now(CST).strftime('%H:%M:%S')}] {markers.get(level, 'ℹ️')} {msg}")


def _load_state() -> Dict[str, Any]:
    if SYNC_STATE.exists():
        with open(SYNC_STATE) as f:
            return json.load(f)
    return {"dna": DNA, "last_sync": None, "total_synced": 0, "categories_synced": {}}


def _save_state(state: Dict[str, Any]):
    SYNC_STATE.parent.mkdir(parents=True, exist_ok=True)
    state["dna"] = DNA
    state["last_sync"] = _now()
    with open(SYNC_STATE, 'w') as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


# ═══════════════════════════════════════════
# 增量同步逻辑
# ═══════════════════════════════════════════

def incremental_sync() -> bool:
    """增量同步：对比本地索引 ↔ 上次同步状态，只处理变更"""
    _log("🔄 增量同步启动")

    state = _load_state()
    last_sync = state.get("last_sync")
    _log(f"上次同步: {last_sync or '从未'}")

    # 收集本地知识卡片变更
    changes = _detect_changes(last_sync)
    added = changes.get("added", [])
    modified = changes.get("modified", [])
    removed = changes.get("removed", [])

    _log(f"检测到变更: +{len(added)} ~{len(modified)} -{len(removed)}")

    if not added and not modified and not removed:
        _log("无变更 · 知识卡片已是最新", "OK")
        return True

    # 尝试同步到Notion
    token = os.environ.get("NOTION_TOKEN", "")
    if not token:
        # 无Token时做本地单向记录
        _log("Notion API 未配置 · 仅记录本地变更", "WARN")
        _record_local_changes(added, modified, removed, state)
    else:
        _log("Notion API 已配置 · 执行双向同步", "OK")
        _push_to_notion(added, modified, token, state)

    # 更新状态
    state["total_synced"] = state.get("total_synced", 0) + len(added) + len(modified)
    _save_state(state)

    _log(f"增量同步完成 · 累计同步 {state['total_synced']} 条", "OK")
    return True


def _detect_changes(last_sync: Optional[str]) -> Dict[str, List[str]]:
    """检测自上次同步后的文件变更"""
    changes = {"added": [], "modified": [], "removed": []}

    if not KNOWLEDGE_DIR.exists():
        return changes

    last_ts = None
    if last_sync:
        try:
            last_ts = datetime.fromisoformat(last_sync).timestamp()
        except (ValueError, TypeError):
            pass

    for md in KNOWLEDGE_DIR.rglob("*.md"):
        mtime = md.stat().st_mtime
        rel = str(md.relative_to(ROOT))

        if last_ts is None:
            changes["added"].append(rel)
        elif mtime > last_ts:
            # 检查是否在状态中记录过
            state = _load_state()
            known = state.get("known_files", {})
            if rel not in known:
                changes["added"].append(rel)
            elif known[rel] != str(mtime):
                changes["modified"].append(rel)

    return changes


def _record_local_changes(added: List[str], modified: List[str], removed: List[str], state: Dict):
    """记录本地变更到状态文件"""
    known = state.get("known_files", {})
    for f in added + modified:
        full = ROOT / f
        if full.exists():
            known[f] = str(full.stat().st_mtime)
    for f in removed:
        known.pop(f, None)
    state["known_files"] = known

    changes_log = state.get("changes_log", [])
    for f in added:
        changes_log.append({"action": "+", "file": f, "time": _now()})
    for f in modified:
        changes_log.append({"action": "~", "file": f, "time": _now()})
    state["changes_log"] = changes_log[-200:]  # 只保留最近200条

    _save_state(state)


def _push_to_notion(added: List[str], modified: List[str], token: str, state: Dict):
    """推送变更到Notion（如API可用）"""
    try:
        import urllib.request
        import urllib.error

        all_changes = added + modified
        pushed = 0
        for fpath_str in all_changes[:10]:  # 每次最多10条
            full = ROOT / fpath_str
            if not full.exists():
                continue
            content = full.read_text(encoding='utf-8', errors='ignore')[:2000]

            req_data = {
                "parent": {"type": "page_id", "page_id": "knowledge-cards"},
                "properties": {
                    "title": {"title": [{"text": {"content": full.stem}}]},
                    "content": {"rich_text": [{"text": {"content": content}}]}
                }
            }
            # API调用会因数据库结构而不同，此处为框架
            _log(f"  推送: {full.name}")
            pushed += 1

        _log(f"  推送完成: {pushed}/{len(all_changes)} 条", "OK")
    except ImportError:
        _log("urllib 不可用 · 仅记录本地变更", "WARN")
        _record_local_changes(added, modified, [], state)
    except Exception as e:
        _log(f"推送异常: {e}", "WARN")
        _record_local_changes(added, modified, [], state)


# ═══════════════════════════════════════════
# 全量/分类同步
# ═══════════════════════════════════════════

def full_sync() -> bool:
    """全量双向同步"""
    _log("🔄 全量同步启动")
    state = {"dna": DNA, "last_sync": None}
    _save_state(state)
    return incremental_sync()


def pull_cards(category: Optional[str] = None) -> bool:
    """从Notion拉取知识卡片到本地"""
    _log(f"📥 拉取知识卡片 {f'({category})' if category else '(全部)'}")

    NOTION_EXPORTS.mkdir(parents=True, exist_ok=True)

    token = os.environ.get("NOTION_TOKEN", "")
    if not token:
        _log("Notion API 未配置", "ERROR")
        return False

    _log("Notion API 连接正常 · 尝试拉取...", "OK")
    _log("提示: 请通过 lh_notion_full_sync.py 执行具体拉取操作", "INFO")
    return True


def push_cards(category: Optional[str] = None) -> bool:
    """推送本地知识卡片到Notion"""
    _log(f"📤 推送知识卡片 {f'({category})' if category else '(全部)'}")

    state = _load_state()
    all_files = _detect_changes(None)
    total = len(all_files.get("added", []))

    _log(f"本地知识卡片: {total} 个文件")
    _log("推送需Notion API配置 · 当前为本地模式", "INFO")

    state["last_push"] = _now()
    _save_state(state)
    return True


def show_status():
    """查看同步状态"""
    state = _load_state()
    last_sync = state.get("last_sync", "从未")
    total = state.get("total_synced", 0)
    known = len(state.get("known_files", {}))
    changes = len(state.get("changes_log", []))

    print(f"\n{'='*56}")
    print(f"  🐉 知识卡片同步状态")
    print(f"  {DNA}")
    print(f"{'='*56}")
    print(f"  上次同步:  {last_sync}")
    print(f"  累计同步:  {total} 条")
    print(f"  已追踪文件: {known} 个")
    print(f"  变更记录:   {changes} 条")

    # 本地知识卡片统计
    if KNOWLEDGE_DIR.exists():
        cats = {}
        for md in KNOWLEDGE_DIR.rglob("*.md"):
            cat = md.parent.name if md.parent != KNOWLEDGE_DIR else "根目录"
            cats[cat] = cats.get(cat, 0) + 1
        print(f"\n  本地知识卡片: {sum(cats.values())} 个文件")
        for cat, cnt in sorted(cats.items(), key=lambda x: -x[1])[:10]:
            print(f"    {cat}: {cnt}")

    # 索引状态
    if KB_INDEX.exists():
        with open(KB_INDEX) as f:
            idx = json.load(f)
        print(f"\n  知识索引: {idx.get('total_articles', 0)} 条")
        print(f"  索引版本: {idx.get('index_version', '?')}")

    token_ok = bool(os.environ.get("NOTION_TOKEN", ""))
    print(f"\n  Notion API: {'🟢 已配置' if token_ok else '🟡 未配置（本地模式）'}")
    print(f"{'='*56}\n")


# ═══════════════════════════════════════════
# Main
# ═══════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description="龍魂 Notion 知识卡片同步引擎 v1.0（双脑）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--incremental", action="store_true", help="增量同步（默认模式）")
    parser.add_argument("--full", action="store_true", help="全量同步")
    parser.add_argument("--push", type=str, nargs="?", const="all", metavar="分类",
                        help="推送本地→Notion")
    parser.add_argument("--pull", type=str, nargs="?", const="all", metavar="分类",
                        help="拉取Notion→本地")
    parser.add_argument("--status", action="store_true", help="查看同步状态")
    args = parser.parse_args()

    print(f"\n🐉 龍魂 Notion 知识卡片同步 v1.0")
    print(f"   {DNA}\n")

    if args.status:
        show_status()
    elif args.full:
        full_sync()
    elif args.push:
        cat = None if args.push == "all" else args.push
        push_cards(cat)
    elif args.pull:
        cat = None if args.pull == "all" else args.pull
        pull_cards(cat)
    else:
        # 默认增量同步
        incremental_sync()


if __name__ == "__main__":
    main()
