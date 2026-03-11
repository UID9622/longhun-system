#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
notion_sync_rules.py  —  Notion→本地规则同步
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Copyright © 2026 UID9622 诸葛鑫（龍芯北辰）
Licensed under the Apache License, Version 2.0

作者：UID9622 诸葛鑫（龍芯北辰）
创作地：中华人民共和国
GPG指纹：A2D0092CEE2E5BA87035600924C3704A8CC26D5F
理论指导：曾仕强老师（永恒显示）
DNA追溯码：#龍芯⚡️20260311-NOTION-SYNC-RULES-v1.0
确认码：#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

共建致谢：
  Claude (Anthropic PBC) · 技术协作与代码共创
  Notion · 知识底座与结构化存储
  没有你们，就没有龍魂系统的一切。

献礼：新中国成立77周年（1949-2026）· 丙午马年
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

架构定位：
                Notion（展现出口）
                      ↓ 只读同步
              rules/（本地规则库）
                      ↓
         加工厂：auditor.py / sync_bridge.py
                      ↓
              结果输出 / 公开审计

用法：
  python3 notion_sync_rules.py sync           # 全量同步所有规则页
  python3 notion_sync_rules.py sync --force   # 强制重新下载（忽略缓存）
  python3 notion_sync_rules.py list           # 列出已同步规则
  python3 notion_sync_rules.py show <name>    # 显示某条规则内容
  python3 notion_sync_rules.py check         # 对齐检测：本地 vs Notion
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import urllib.request
import urllib.error
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Optional

# ─── 路径 ─────────────────────────────────────────────────────────────────────

BASE       = Path.home() / "longhun-system"
ENV_FILE   = BASE / ".env"
RULES_DIR  = BASE / "rules"
INDEX_FILE = RULES_DIR / "index.json"
AUDIT_DB   = BASE / "logs" / "audit_events.jsonl"
TZ_CN      = timezone(timedelta(hours=8))
GPG_FP     = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"

RULES_DIR.mkdir(parents=True, exist_ok=True)
(BASE / "logs").mkdir(parents=True, exist_ok=True)

# ─── 要同步的规则关键词（会在 Notion 搜索这些词） ──────────────────────────

RULE_QUERIES = [
    ("L0-伦理",         ["伦理边界", "L0", "反驳博弈", "AI伦理"]),
    ("L1-架构",         ["L1", "DNA追溯", "记忆压缩", "闭环检测"]),
    ("L2-行为规则",     ["L2", "文字陷阱", "一票否决", "创作权利"]),
    ("龙魂铁律",        ["龙魂系统使用规则", "数据主权", "铁律", "分级管理"]),
    ("多AI协作",        ["多AI协作", "人格", "共生"]),
    ("DNA标准",         ["DNA", "追溯码", "签名"]),
    ("质检报告",        ["质检", "巡检", "审计"]),
    ("向政府建议",      ["建议书", "网信", "AI监管"]),
]

# ─── 工具 ─────────────────────────────────────────────────────────────────────

def now_cn(fmt: str = "%Y-%m-%d %H:%M:%S") -> str:
    return datetime.now(tz=TZ_CN).strftime(fmt)

def now_iso() -> str:
    return datetime.now(tz=TZ_CN).isoformat()

def short_hash(s: str, n: int = 8) -> str:
    return hashlib.sha256(s.encode()).hexdigest()[:n].upper()

def gen_dna(tag: str, content: str = "") -> str:
    d = datetime.now(tz=TZ_CN).strftime("%Y%m%d")
    h = short_hash((content or now_cn()) + tag)
    return f"#龍芯⚡️{d}-{tag}-{h}-UID9622"

def load_env() -> dict[str, str]:
    env: dict[str, str] = {}
    if not ENV_FILE.exists():
        return env
    for line in ENV_FILE.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" in line:
            k, _, v = line.partition("=")
            env[k.strip()] = v.strip().strip("'\"")
    return env

ENV = load_env()

def get_key(name: str) -> Optional[str]:
    v = ENV.get(name)
    if not v or v.startswith("填入") or v.startswith("sk-ant-填"):
        return None
    return v

def _http_get(url: str, headers: dict) -> tuple[int, bytes]:
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=12) as resp:
            return resp.status, resp.read()
    except urllib.error.HTTPError as e:
        return e.code, e.read()
    except Exception as e:
        return -1, str(e).encode()

def _http_post(url: str, headers: dict, data: dict) -> tuple[int, bytes]:
    body = json.dumps(data).encode()
    req  = urllib.request.Request(url, data=body, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=12) as resp:
            return resp.status, resp.read()
    except urllib.error.HTTPError as e:
        return e.code, e.read()
    except Exception as e:
        return -1, str(e).encode()

def _audit(event_type: str, detail: str, decision: str = "🟢") -> None:
    if not AUDIT_DB.exists():
        return
    record = {
        "ts": now_iso(), "event_type": event_type,
        "color": decision, "action": "记录", "detail": detail,
    }
    with AUDIT_DB.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")

# ─── Notion 读取器（只读） ────────────────────────────────────────────────────

NOTION_BASE    = "https://api.notion.com/v1"
NOTION_VERSION = "2022-06-28"

def _notion_headers() -> dict:
    token = get_key("NOTION_TOKEN")
    if not token:
        raise RuntimeError("NOTION_TOKEN 未配置，请检查 ~/longhun-system/.env")
    return {
        "Authorization": f"Bearer {token}",
        "Notion-Version": NOTION_VERSION,
        "Content-Type": "application/json",
    }

def notion_search(query: str, limit: int = 3) -> list[dict]:
    """搜索 Notion，返回页面列表。"""
    status, body = _http_post(
        f"{NOTION_BASE}/search",
        _notion_headers(),
        {"query": query, "page_size": limit, "filter": {"value": "page", "property": "object"}}
    )
    if status != 200:
        return []
    results = json.loads(body).get("results", [])
    pages   = []
    for r in results:
        if r.get("object") != "page":
            continue
        title = _extract_title(r)
        pages.append({
            "id":          r["id"],
            "title":       title,
            "url":         r.get("url", ""),
            "last_edited": r.get("last_edited_time", "")[:10],
        })
    return pages

def _extract_title(page_obj: dict) -> str:
    props = page_obj.get("properties", {})
    for v in props.values():
        if v.get("type") == "title":
            t = v.get("title", [])
            if t:
                return "".join(x.get("plain_text", "") for x in t)
    # fallback: icon + 前缀
    icon = page_obj.get("icon", {})
    icon_text = icon.get("emoji", "") if icon.get("type") == "emoji" else ""
    return icon_text + " (无标题)"

def notion_read_blocks(page_id: str, max_blocks: int = 200) -> str:
    """读取一个页面的所有文字内容（只读）。"""
    lines: list[str] = []
    cursor = None

    while True:
        url = f"{NOTION_BASE}/blocks/{page_id}/children?page_size=100"
        if cursor:
            url += f"&start_cursor={cursor}"
        status, body = _http_get(url, _notion_headers())
        if status != 200:
            break
        data     = json.loads(body)
        blocks   = data.get("results", [])
        has_more = data.get("has_more", False)
        next_cur = data.get("next_cursor")

        for b in blocks:
            text = _block_to_text(b)
            if text:
                lines.append(text)
            if len(lines) >= max_blocks:
                has_more = False
                break

        if not has_more or not next_cur:
            break
        cursor = next_cur

    return "\n".join(lines)

def _block_to_text(block: dict) -> str:
    """把一个 Notion block 转为纯文本。"""
    bt   = block.get("type", "")
    data = block.get(bt, {})

    # 常见 block 类型
    if bt in ("paragraph", "heading_1", "heading_2", "heading_3",
              "bulleted_list_item", "numbered_list_item",
              "toggle", "quote", "callout", "code"):
        rich = data.get("rich_text", [])
        text = "".join(x.get("plain_text", "") for x in rich)
        # heading 加前缀
        prefix = {"heading_1": "# ", "heading_2": "## ", "heading_3": "### "}.get(bt, "")
        return prefix + text if text else ""

    if bt == "divider":
        return "─────────────────────────────────────"

    return ""

# ─── 同步单条规则 ─────────────────────────────────────────────────────────────

def sync_rule(name: str, queries: list[str], force: bool = False) -> dict:
    """
    搜索并同步一个规则类别到 rules/{name}.md + rules/{name}.json
    返回同步结果摘要。
    """
    safe_name = re.sub(r"[^\w\u4e00-\u9fff\-]", "_", name)
    md_file   = RULES_DIR / f"{safe_name}.md"
    meta_file = RULES_DIR / f"{safe_name}.meta.json"

    # 缓存检测（非强制模式下，当天已同步则跳过）
    if not force and meta_file.exists():
        try:
            meta = json.loads(meta_file.read_text(encoding="utf-8"))
            if meta.get("sync_date") == now_cn()[:10]:
                return {"name": name, "status": "cached", "pages": meta.get("pages", [])}
        except Exception:
            pass

    print(f"  ⏳ 同步规则「{name}」…", end="", flush=True)

    found_pages: list[dict] = []
    all_content: list[str]  = [f"# {name}\n", f"> 同步自 Notion · {now_cn()} · DNA: {gen_dna('RULE-SYNC', name)}\n"]

    for q in queries:
        pages = notion_search(q, limit=2)
        for p in pages:
            if any(fp["id"] == p["id"] for fp in found_pages):
                continue  # 去重
            found_pages.append(p)
            content = notion_read_blocks(p["id"], max_blocks=150)
            if content.strip():
                all_content.append(f"\n---\n## {p['title']}\n")
                all_content.append(f"> 来源: {p['url']}  编辑: {p['last_edited']}\n\n")
                all_content.append(content)

    if not found_pages:
        print(" ⚠️  未找到")
        return {"name": name, "status": "not_found", "pages": []}

    full_text = "\n".join(all_content)
    md_file.write_text(full_text, encoding="utf-8")

    meta = {
        "name":      name,
        "sync_date": now_cn()[:10],
        "sync_ts":   now_iso(),
        "pages":     found_pages,
        "char_count": len(full_text),
        "dna":       gen_dna("RULE-SYNC", name),
        "hash":      short_hash(full_text),
    }
    meta_file.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f" ✅ {len(found_pages)} 页  {len(full_text)} 字")
    _audit("NOTION_READ", f"规则同步: {name} · {len(found_pages)}页 · {len(full_text)}字")
    return {"name": name, "status": "ok", "pages": found_pages, "chars": len(full_text)}

# ─── 构建本地索引 ─────────────────────────────────────────────────────────────

def build_index(results: list[dict]) -> None:
    """生成 rules/index.json 和 rules/RULES_CONTEXT.md（供 Claude 加载）。"""

    index = {
        "generated_at": now_cn(),
        "dna":          gen_dna("RULES-INDEX"),
        "gpg":          GPG_FP,
        "rules":        results,
        "total_rules":  len([r for r in results if r["status"] in ("ok", "cached")]),
    }
    INDEX_FILE.write_text(json.dumps(index, ensure_ascii=False, indent=2), encoding="utf-8")

    # 生成 RULES_CONTEXT.md — 这个文件是本地 Claude 的"规则上下文入口"
    ctx_lines = [
        "# 龍魂规则库上下文入口",
        f"> 生成时间: {now_cn()}  DNA: {index['dna']}",
        f"> 来源: Notion（展现出口）→ 本地（加工厂）  只读同步",
        "",
        "## 已同步规则清单",
        "",
    ]
    for r in results:
        if r["status"] in ("ok", "cached"):
            safe_name = re.sub(r"[^\w\u4e00-\u9fff\-]", "_", r["name"])
            page_titles = " · ".join(p["title"][:30] for p in r.get("pages", [])[:2])
            ctx_lines.append(f"- **{r['name']}** → `rules/{safe_name}.md`  ({page_titles})")
    ctx_lines += [
        "",
        "## 加载方式（Claude 本地读取）",
        "",
        "```bash",
        "# 查看某条规则",
        "python3 notion_sync_rules.py show L0-伦理",
        "",
        "# 全量同步（每天一次）",
        "python3 notion_sync_rules.py sync",
        "",
        "# 对齐检测",
        "python3 notion_sync_rules.py check",
        "```",
        "",
        "## 架构说明",
        "",
        "```",
        "Notion（展现出口）",
        "       ↓ 只读同步（notion_sync_rules.py）",
        "rules/ 本地规则库  ←── 加工厂底层上下文",
        "       ↓",
        "auditor.py · sync_bridge.py · longhun_qa_bot.py",
        "       ↓",
        "quality reports + audit events + DNA stamps",
        "       ↓",
        "qa_report.html（公开展示）← 再写回 Notion（未来）",
        "```",
        "",
        f"---",
        f"DNA: {index['dna']}",
        f"GPG: {GPG_FP}",
        f"确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z",
        f"共建: Claude (Anthropic PBC) · Notion",
    ]
    (RULES_DIR / "RULES_CONTEXT.md").write_text("\n".join(ctx_lines), encoding="utf-8")

# ─── 对齐检测 ─────────────────────────────────────────────────────────────────

def check_alignment() -> None:
    """检测本地规则 vs Notion 最新版本，找出过期的规则。"""
    if not INDEX_FILE.exists():
        print("⚠️  还没有索引，先运行: python3 notion_sync_rules.py sync")
        return

    index = json.loads(INDEX_FILE.read_text(encoding="utf-8"))
    today = now_cn()[:10]

    print(f"\n━━━ 规则对齐检测 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"  索引生成: {index['generated_at']}")
    print(f"  今日日期: {today}")
    print()

    stale_count = 0
    for r in index.get("rules", []):
        safe_name = re.sub(r"[^\w\u4e00-\u9fff\-]", "_", r["name"])
        meta_file = RULES_DIR / f"{safe_name}.meta.json"
        if meta_file.exists():
            meta = json.loads(meta_file.read_text(encoding="utf-8"))
            sync_date = meta.get("sync_date", "")
            icon = "🟢" if sync_date == today else ("🟡" if sync_date >= today[:7] else "🔴")
            if icon != "🟢":
                stale_count += 1
            pages = meta.get("pages", [])
            latest_notion = max((p.get("last_edited", "") for p in pages), default="?")
            print(f"  {icon} {r['name']}")
            print(f"      本地同步: {sync_date}  Notion最新: {latest_notion}")
        else:
            stale_count += 1
            print(f"  🔴 {r['name']} — 未找到元数据文件")

    print()
    if stale_count == 0:
        print("  ✅ 所有规则与 Notion 保持同步（今日已更新）")
    else:
        print(f"  ⚠️  {stale_count} 条规则需要重新同步")
        print(f"  运行: python3 notion_sync_rules.py sync --force")
    print()
    _audit("LOCAL_READ", f"对齐检测完成 · 过期规则:{stale_count}")

# ─── CLI ─────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(description="Notion→本地规则同步 · notion_sync_rules.py")
    sub = parser.add_subparsers(dest="cmd")

    p_sync = sub.add_parser("sync", help="同步所有规则（从 Notion 拉取）")
    p_sync.add_argument("--force", action="store_true", help="强制重新下载（忽略今日缓存）")
    p_sync.add_argument("--rule", default="", help="只同步某条规则（名称关键词）")

    sub.add_parser("list", help="列出已同步规则")
    sub.add_parser("check", help="对齐检测")

    p_show = sub.add_parser("show", help="显示某条规则内容")
    p_show.add_argument("name", help="规则名称（部分匹配）")

    args = parser.parse_args()

    if args.cmd == "sync":
        print("\n🔄 龍魂规则库同步 · Notion → 本地")
        print(f"   北京时间: {now_cn()}")
        print(f"   规则目录: {RULES_DIR}")
        print()

        queries_to_run = RULE_QUERIES
        if args.rule:
            queries_to_run = [(n, q) for n, q in RULE_QUERIES if args.rule.lower() in n.lower()]
            if not queries_to_run:
                print(f"⚠️  找不到规则: {args.rule}")
                return

        results = []
        for name, queries in queries_to_run:
            r = sync_rule(name, queries, force=args.force)
            results.append(r)

        build_index(results)

        ok_count = sum(1 for r in results if r["status"] in ("ok", "cached"))
        print(f"\n✅ 同步完成：{ok_count}/{len(results)} 条规则在线")
        print(f"   规则入口: {RULES_DIR / 'RULES_CONTEXT.md'}")
        print(f"   索引文件: {INDEX_FILE}")
        dna = gen_dna("SYNC-COMPLETE")
        _audit("SYNC_EXECUTED", f"规则同步完成 {ok_count}/{len(results)}")
        print(f"   DNA: {dna}")

    elif args.cmd == "list":
        if not INDEX_FILE.exists():
            print("⚠️  还没有规则，先运行: python3 notion_sync_rules.py sync")
            return
        index = json.loads(INDEX_FILE.read_text(encoding="utf-8"))
        print(f"\n📚 本地规则库（{index['generated_at']}）")
        for r in index.get("rules", []):
            status_icon = "✅" if r["status"] in ("ok", "cached") else "❌"
            pages_info  = f"{len(r.get('pages', []))}页" if r.get("pages") else "未找到"
            chars_info  = f"{r.get('chars', 0)}字" if r.get("chars") else ""
            print(f"  {status_icon} {r['name']}  ({pages_info} {chars_info})")
        print(f"\n  入口文件: rules/RULES_CONTEXT.md")

    elif args.cmd == "check":
        check_alignment()

    elif args.cmd == "show":
        # 匹配规则文件
        matched = [f for f in RULES_DIR.glob("*.md")
                   if args.name.lower() in f.stem.lower() and "RULES_CONTEXT" not in f.name]
        if not matched:
            print(f"⚠️  找不到规则: {args.name}  已有规则:")
            for f in sorted(RULES_DIR.glob("*.md")):
                print(f"    {f.stem}")
            return
        content = matched[0].read_text(encoding="utf-8")
        # 只显示前 100 行避免刷屏
        lines = content.splitlines()[:100]
        print("\n".join(lines))
        if len(content.splitlines()) > 100:
            print(f"\n  … （共 {len(content.splitlines())} 行，省略后续）")
            print(f"  完整内容: cat {matched[0]}")

    else:
        parser.print_help()
        print(f"\n  DNA: #龍芯⚡️20260311-NOTION-SYNC-RULES-v1.0")
        print(f"  快速开始: python3 notion_sync_rules.py sync")

if __name__ == "__main__":
    main()
