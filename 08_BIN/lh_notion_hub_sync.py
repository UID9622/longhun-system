#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · Notion 中枢同步引擎 v2.0（三地）
DNA: #龍芯⚡️丙午·乙未·戊戌·巳时·䷜坎-NOTION-HUB-SYNC-v2.0
创建者: 诸葛鑫 (UID9622)
协议: CC BY-NC-SA 4.0

三地数据中枢同步：Mac本地 ↔ Notion云端 ↔ 鲲鹏服务器
  --sync-all      全量拉取Notion页面→本地归档
  --search <词>   搜特定知识锁→直接拉取
  --push-repos    生成Notion可粘贴的展示页
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional

CST = timezone(timedelta(hours=8))

DNA = "#龍芯⚡️丙午·乙未·戊戌·巳时·䷜坎-NOTION-HUB-SYNC-v2.0"
CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
CREATOR = "诸葛鑫（UID9622·龍芯北辰）"

ROOT = Path(__file__).resolve().parent.parent
HOME = Path.home()
SYNC_DIR = ROOT / "data" / "notion_sync"
MIRROR_DIR = ROOT / "docs" / "notion_mirror"
CONFIG_FILE = ROOT / "config" / "notion_sync.json"
STATE_FILE = SYNC_DIR / "hub_sync_state.json"


def _now() -> str:
    return datetime.now(CST).isoformat()


def _now_ts() -> str:
    return datetime.now(CST).strftime("%Y%m%d-%H%M%S")


def _log(msg: str, level: str = "INFO"):
    markers = {"INFO": "📋", "OK": "✅", "WARN": "🟡", "ERROR": "🔴", "STEP": "⚙️"}
    print(f"[{datetime.now(CST).strftime('%H:%M:%S')}] {markers.get(level, 'ℹ️')} {msg}")


# ═══════════════════════════════════════════
# API 凭证
# ═══════════════════════════════════════════

def get_notion_token() -> str:
    token = os.environ.get("NOTION_TOKEN", "")
    if not token:
        secrets_file = HOME / ".longhun" / "config" / "龍智守_config.json"
        if secrets_file.exists():
            try:
                with open(secrets_file) as f:
                    cfg = json.load(f)
                token = cfg.get("notion", {}).get("token", "")
            except Exception:
                pass
    if not token:
        _log("NOTION_TOKEN 未配置 · 设置环境变量或在 ~/.longhun/config/龍智守_config.json 中配置", "ERROR")
        sys.exit(1)
    return token


# ═══════════════════════════════════════════
# 核心功能
# ═══════════════════════════════════════════

def sync_all() -> bool:
    """全量拉取 Notion → 本地归档"""
    _log("🚀 Notion 全量同步启动 (三地中枢)", "STEP")
    SYNC_DIR.mkdir(parents=True, exist_ok=True)

    # 调用已有脚本
    sync_scripts = [
        ("全量扫描+整理", ["python3", str(ROOT / "bin" / "lh_notion_full_sync.py")]),
        ("知识卡片同步", ["python3", str(ROOT / "bin" / "lh_notion_sync_engine.py"), "--incremental"]),
        ("术语提取", ["python3", str(ROOT / "bin" / "lh_notion_term_extractor.py")])
    ]

    all_ok = True
    for name, cmd in sync_scripts:
        _log(f"执行: {name}", "STEP")
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
            ok = result.returncode == 0
            _log(f"  {name} → {'完成' if ok else '异常'}", "OK" if ok else "WARN")
            if not ok and result.stderr.strip():
                _log(f"  {result.stderr.strip()[:200]}", "WARN")
        except subprocess.TimeoutExpired:
            _log(f"  {name} → 超时", "WARN")
            ok = False
        except FileNotFoundError:
            _log(f"  {name} → 脚本缺失", "WARN")
            ok = False
        all_ok = all_ok and ok

    # 写入状态
    state = {
        "dna": DNA,
        "last_sync": _now(),
        "mode": "full",
        "scripts_run": len(sync_scripts),
        "all_ok": all_ok,
    }
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, ensure_ascii=False, indent=2)

    # 统计
    pages = len(list(MIRROR_DIR.rglob("*.md"))) if MIRROR_DIR.exists() else 0
    _log(f"三地同步完成 · 镜像 {pages} 页 · 状态 {'🟢' if all_ok else '🟡'}")
    return all_ok


def search_notion(query: str) -> bool:
    """搜特定知识 → 直接拉取对应页面"""
    _log(f"🔍 Notion 搜索: '{query}'")

    # 先查本地镜像
    hits_local = []
    if MIRROR_DIR.exists():
        import re
        for md in MIRROR_DIR.rglob("*.md"):
            try:
                content = md.read_text(encoding='utf-8', errors='ignore')
                if query.lower() in content.lower() or query.lower() in md.name.lower():
                    hits_local.append(md)
            except Exception:
                pass

    if hits_local:
        _log(f"本地镜像命中 {len(hits_local)} 个文件:", "OK")
        for h in hits_local[:10]:
            size = h.stat().st_size
            print(f"  📄 {h.relative_to(ROOT)} ({size//1024}KB)")
        if len(hits_local) > 10:
            print(f"  ... 还有 {len(hits_local)-10} 个")

    # 尝试调Notion API搜索
    token = os.environ.get("NOTION_TOKEN", "")
    if not token:
        _log("Notion API 未配置 · 仅显示本地结果", "WARN")
        return len(hits_local) > 0

    # 通过Notion搜索API拉取
    try:
        import urllib.request
        import urllib.error

        req = urllib.request.Request(
            "https://api.notion.com/v1/search",
            data=json.dumps({
                "query": query,
                "sort": {"direction": "descending", "timestamp": "last_edited_time"},
                "page_size": 10,
            }).encode(),
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
                "Notion-Version": "2022-06-28",
            },
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode())

        results = data.get("results", [])
        _log(f"API 命中 {len(results)} 条")
        for r in results:
            title_parts = []
            for k in ("title", "Name", "名称"):
                prop = r.get("properties", {}).get(k, {})
                for t in prop.get("title", []) if isinstance(prop.get("title"), list) else []:
                    title_parts.append(t.get("plain_text", ""))
            title = " ".join(title_parts)
            page_type = r.get("object", "?")
            page_id = r.get("id", "?").replace("-", "")
            url = r.get("url", f"https://notion.so/{page_id}")
            print(f"  🔗 [{page_type}] {title or '(无标题)'} → {url}")

    except urllib.error.HTTPError as e:
        _log(f"API 错误: {e.code} {e.reason}", "ERROR")
        return False
    except Exception as e:
        _log(f"搜索异常: {e}", "WARN")

    return True


def push_repos() -> bool:
    """生成 Notion 可粘贴的展示页"""
    _log("📤 生成 Notion 展示页")

    output_dir = ROOT / "data" / "notion_sync" / "display_pages"
    output_dir.mkdir(parents=True, exist_ok=True)

    pages = []

    # 1. 系统概览页
    overview = f"""# 🐉 龍魂系统 · 项目全景

> DNA: {DNA}
> 更新时间: {_now()}
> 确认码: {CONFIRM}

## 📊 核心引擎
| 引擎 | 状态 |
|:---|:---:|
| 知识中枢API | :8766 |
| 胖东来审计API | :8767 |
| 无状态API网关 | :8785 |
| 军团指挥中枢 | :8781 |

## 🧑‍🤝‍🧑 人格内阁
**20人格** · 16核心 + 1安全(P77) + 3子系统(S1-S3)
- 战略层: P00文心 · P01诸葛亮
- 执行层: P02宝宝 · P03雯雯 · P04鲁班 · P07管仲 · P14吕蒙
- 文化层: P08仓颉 · P09孙思邈 · P10苏东坡 · P11李白 · P12屈原
- 守护层: P05上帝之眼 · P06数学大师 · P13姜子牙 · P15乔前辈 · P72龍盾

## 🔐 核心协议
- 系统宪法 (CONSTITUTION.md + P0_ETERNAL_LOCK.md) P0
- 20人格治理白皮书 v1.4 P0
- 德本审计协议 v1.0 P0
- 无后台主权协议 v3.0 P0
- 隐私接入规则 v2.0
- 算法审计与透明协议 v1.0
- 战后整顿协议 v1.0

## 🌐 线上入口
- 知识中枢: https://uid9622.cn
- 胖东来审计: https://uid9622.cn/pangdonglai
- 猎手排行榜: https://uid9622.cn/hunter
- CNSH·如意: https://uid9622.cn/cnsh-ruyi
- 五害曝光台: https://uid9622.cn/five-harms-expose

---
*由 诸葛鑫 (UID9622) 创建 · 龍魂系统自动生成*
"""
    overview_file = output_dir / "01_系统全景.md"
    overview_file.write_text(overview, encoding='utf-8')
    pages.append(("01_系统全景", overview_file))

    # 2. 知识卡片展示
    kb_index = ROOT / "portal" / "knowledge" / "kb_index.json"
    if kb_index.exists():
        with open(kb_index) as f:
            idx = json.load(f)
        kb_display = f"""# 📚 知识库展示

> 共 {idx.get('total_articles', 0)} 篇文章 · 索引版本 {idx.get('index_version', '?')}

## 分类统计
"""
        for cat, info in idx.get("categories", {}).items():
            kb_display += f"- **{cat}**: {info.get('count', 0)} 篇\n"

        kb_display += "\n## 最新文章\n"
        for art in idx.get("articles", [])[:30]:
            title = art.get("title", "无标题")
            source = art.get("source", "未知")
            quality = art.get("quality", 0)
            kb_display += f"- [{source}] {title} (质量: {quality})\n"

        kb_file = output_dir / "02_知识库展示.md"
        kb_file.write_text(kb_display, encoding='utf-8')
        pages.append(("02_知识库展示", kb_file))

    # 3. 协议清单
    protocols_dir = ROOT / "01_protocols"
    if protocols_dir.exists():
        proto_display = f"# 📜 协议清单\n\n更新时间: {_now()}\n\n"
        for proto in sorted(protocols_dir.glob("*.md")):
            name = proto.stem
            proto_display += f"- [{name}]({proto.relative_to(ROOT)})\n"
        proto_file = output_dir / "03_协议清单.md"
        proto_file.write_text(proto_display, encoding='utf-8')
        pages.append(("03_协议清单", proto_file))

    _log(f"生成 {len(pages)} 个展示页:")
    for name, fpath in pages:
        print(f"  📄 {name}: {fpath}")
    print(f"\n💡 将这些 .md 文件内容粘贴到 Notion 即可")
    return True


# ═══════════════════════════════════════════
# Main
# ═══════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description="龍魂 Notion 中枢同步引擎 v2.0（三地）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3 bin/lh_notion_hub_sync.py --sync-all     全量同步
  python3 bin/lh_notion_hub_sync.py --search 易经   搜索并拉取
  python3 bin/lh_notion_hub_sync.py --push-repos    生成展示页
        """
    )
    parser.add_argument("--sync-all", action="store_true", help="全量拉取Notion→本地归档")
    parser.add_argument("--search", type=str, metavar="关键词", help="搜索特定知识锁→直接拉取")
    parser.add_argument("--push-repos", action="store_true", help="生成Notion可粘贴展示页")
    args = parser.parse_args()

    print(f"\n🐉 龍魂 Notion 中枢同步 v2.0")
    print(f"   {DNA}")
    print(f"   {CONFIRM}\n")

    start = time.time()

    if args.sync_all:
        sync_all()
    elif args.search:
        search_notion(args.search)
    elif args.push_repos:
        push_repos()
    else:
        # 默认显示帮助
        parser.print_help()

    dur = time.time() - start
    if any([args.sync_all, args.search, args.push_repos]):
        _log(f"总耗时: {dur:.1f}s", "OK")


if __name__ == "__main__":
    main()
