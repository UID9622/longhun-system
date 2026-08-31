#!/usr/bin/env python3
# DNA: #龍芯⚡️丙午·丙申·庚午·戌时·䷭升-LOGS-TO-NOTION-v1.1-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 创建者: 诸葛鑫（UID9622）
# 协议: CC BY-NC-SA 4.0（核心思想层）
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""
═══════════════════════════════════════════
🐉 龍魂·操作日志入库引擎 v1.1
═══════════════════════════════════════════
用途: 将 .codebuddy/memory/YYYY-MM-DD.md 每日操作日志全量入库 Notion。
      每份日志 = 数据库一行（日期/标题/GPG/三色/摘要/DNA 属性），
      正文全文分块写入（Notion 全文可检索），哈希去重增量同步。

v1.1 修复清单（vs v1.0）:
  [BUG1] load_index 返回 {"schema_version","logs":{}} 但 sync_log 直接用
         idx.get(date)、idx[date]=... 操作顶层 → 应全部走 idx["logs"]
  [BUG2] clear_children 改为逐块 DELETE /v1/blocks/{block_id}
         （v1.0 的 PATCH children 带 block id 也是 Notion 官方删除语法，
          但 v1.1 采用 DELETE 逐块，语义更明确、更保守）
  [BUG3] notion_call 补空 body 处理（DELETE 返回 200 空 body →
         json.loads 会抛错）+ 兜底 except Exception
  [BUG4] 三色 emoji 判断改为显式列表成员检测
  [BUG5] parse_head DNA 提取重写：优先 **DNA:** / DNA: 前缀，fallback 扫龍芯⚡️
  [BUG6] 移除 cmd_sync 中 "2025-08-09" 遗留死代码
  [BUG7] clear_children 循环翻页拉全量 block_id（v1.0 只取第一页 100 个）
  [新增] --dry-run 预演模式 / 写操作后 sleep 防 rate-limit / 仅变更时落盘
  [保留] v1.0 已验证防坑: 建页空建(children 后补) + 正文每批≤8 blocks 追加
         → 防 Cloudflare 403 拦截大请求体（45KB 日志曾触发）
  [增强] load_index 迁移: v1.0 坏索引的日期键存顶层且 logs 键为空 →
         合并进 idx["logs"]，避免升级后重复建页

用法:
  python3 bin/lh_logs_sync.py sync            # 增量同步（只入新增/变更）
  python3 bin/lh_logs_sync.py sync --force    # 全部重写
  python3 bin/lh_logs_sync.py sync --date 2026-08-26
  python3 bin/lh_logs_sync.py sync --dry-run  # 预演，不写 Notion
  python3 bin/lh_logs_sync.py status          # 统计
  python3 bin/lh_logs_sync.py sign            # GPG 签名
"""

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

# ────────────────────────────────────────────
# 常量配置
# ────────────────────────────────────────────
BASE        = Path.home() / "longhun-system"
MEMORY_DIR  = BASE / ".codebuddy" / "memory"
HUB_DIR     = BASE / "12_DOCS" / "dragon-soul-open-hub"
INDEX_FILE  = HUB_DIR / "logs-notion-index.json"
CONFIG_FILE = HUB_DIR / "logs-notion-config.json"

NOTION_VERSION = "2022-06-28"
DB_TITLE    = "🐉 龍魂·操作日志库 v1.0"
PARENT_PAGE = "2d87125a-9c9f-8028-89e2-e18002f7cf4f"
GPG_KEY     = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"

BLOCK_LIMIT  = 1900   # 单 block rich_text 上限（Notion 2000，留余量）
MAX_CHILDREN = 8      # 单次 append-children 上限（小批防 Cloudflare 403）
API_SLEEP    = 0.35   # 每次 Notion 写操作后 sleep，防 rate-limit

# [FIX-BUG4] 用列表，不用字符串迭代
COLOR_EMOJIS = ["🟢", "🟡", "🔴"]

# ────────────────────────────────────────────
# Notion API 工具
# ────────────────────────────────────────────
def notion_call(token, path, method="GET", data=None) -> dict[str, Any]:
    """
    封装 Notion REST 调用。
    [FIX-BUG3] 空 body 安全处理（DELETE 返回 200 空 body），
               并兜底捕获一切请求异常，不再裸崩。
    """
    body = json.dumps(data).encode("utf-8") if data is not None else None
    req = urllib.request.Request(
        f"https://api.notion.com/v1/{path}",
        data=body,
        method=method,
        headers={
            "Authorization": f"Bearer {token}",
            "Notion-Version": NOTION_VERSION,
            "Content-Type": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            raw = r.read()
            return json.loads(raw) if raw.strip() else {}   # DELETE 返回空 body
    except urllib.error.HTTPError as e:
        detail = e.read().decode(errors="replace")[:800]
        print(f"  ⚠️  Notion API 错误 [{method} {path}] {e.code}: {detail}")
        return {"error": e.code, "detail": detail}
    except Exception as exc:
        print(f"  ⚠️  Notion 请求异常 [{method} {path}]: {exc}")
        return {"error": str(exc)}

# ────────────────────────────────────────────
# Token 获取（四级降级）
# ────────────────────────────────────────────
def get_token():
    """顺序取 token: lh_vault(Keychain权威) → config/notion_config.json → ~/.env → env"""
    # 1) lh_vault
    try:
        r = subprocess.run(
            [sys.executable, str(BASE / "bin" / "lh_vault.py"), "get", "NOTION_TOKEN"],
            capture_output=True, text=True, timeout=30,
        )
        if r.returncode == 0:
            v = r.stdout.strip().strip('"').strip("'")
            if v and v.startswith(("ntn_", "secret_")):
                return v
    except Exception:
        pass

    # 2) config/notion_config.json
    cfg = BASE / "config" / "notion_config.json"
    if cfg.exists():
        try:
            d = json.loads(cfg.read_text(encoding="utf-8"))
            if d.get("notion_token"):
                return d["notion_token"].strip()
        except Exception:
            pass

    # 3) ~/.env
    env = Path.home() / ".env"
    if env.exists():
        for line in env.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line.startswith("NOTION_TOKEN="):
                return line.split("=", 1)[1].strip().strip('"').strip("'")

    # 4) 环境变量
    return os.environ.get("NOTION_TOKEN", "").strip() or None

# ────────────────────────────────────────────
# 本地索引 I/O
# ────────────────────────────────────────────
def load_index():
    """
    索引结构（v1.1）：
      {
        "schema_version": "1.1.0",
        "logs": {
          "2026-08-26": {"page_id": "...", "sha256": "...", "synced_at": "..."}
        }
      }
    [FIX-BUG1] v1.0 里 sync_log 用 idx.get(date) / idx[date]= 操作顶层，
               与 load_index 返回的 {"logs":{}} 结构不一致。
    [增强] v1.0 坏索引可能同时存在「空的 logs 键」+「顶层日期键」：
           必须把顶层日期键合并进 idx["logs"]，否则升级后 logs 为空、
           会误判全部待入库并重复建页。这里同时处理两种坏索引。
    """
    if INDEX_FILE.exists():
        try:
            raw = json.loads(INDEX_FILE.read_text(encoding="utf-8"))
            if "logs" not in raw:
                # 坏索引A: 完全无 logs 键 → 顶层日期键全部迁移
                migrated = {"schema_version": "1.1.0", "logs": {}}
                for k, v in raw.items():
                    if re.match(r"^\d{4}-\d{2}-\d{2}$", k):
                        migrated["logs"][k] = v
                return migrated
            # 坏索引B: logs 键存在但空 + 顶层还挂着日期键 → 合并
            logs = raw["logs"]
            moved = False
            for k, v in list(raw.items()):
                if re.match(r"^\d{4}-\d{2}-\d{2}$", k):
                    if k not in logs:
                        logs[k] = v
                    del raw[k]
                    moved = True
            if moved:
                raw["schema_version"] = "1.1.0"
                save_index(raw)
            return raw
        except Exception:
            pass
    return {"schema_version": "1.1.0", "logs": {}}

def save_index(idx):
    INDEX_FILE.parent.mkdir(parents=True, exist_ok=True)
    INDEX_FILE.write_text(json.dumps(idx, ensure_ascii=False, indent=2), encoding="utf-8")

def load_config():
    if CONFIG_FILE.exists():
        try:
            return json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {}

def save_config(cfg):
    CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
    CONFIG_FILE.write_text(json.dumps(cfg, ensure_ascii=False, indent=2), encoding="utf-8")

# ────────────────────────────────────────────
# 文件扫描 & 哈希
# ────────────────────────────────────────────
def log_files():
    """扫描所有 YYYY-MM-DD.md 每日日志，按日期升序返回。"""
    out = []
    for f in sorted(MEMORY_DIR.glob("*.md")):
        if re.match(r"^\d{4}-\d{2}-\d{2}\.md$", f.name):
            out.append((f.stem, f))   # stem = YYYY-MM-DD
    return out

def sha256_of(path):
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()

def now_iso():
    return datetime.now(UTC).astimezone().isoformat(timespec="seconds")

# ────────────────────────────────────────────
# 日志解析
# ────────────────────────────────────────────
def parse_head(text):
    """
    从日志头部（前 30 行）提取 DNA/GPG/三色/性质/确认码。
    [FIX-BUG5] DNA 提取重写：
      - 优先匹配 **DNA:** 或 DNA: 开头的行
      - fallback：找第一行含「龍芯⚡️」的行作为 DNA
    """
    head = {"dna": "", "gpg": "", "color": "", "nature": "", "confirm": ""}
    dna_fallback = ""

    for line in text.splitlines()[:30]:
        s = line.strip()

        if s.startswith("**DNA:**") or re.match(r"^DNA\s*:", s):
            head["dna"] = s.split(":", 1)[1].strip().strip("`").strip()[:200]
        elif s.startswith("**GPG:**") or re.match(r"^GPG\s*:", s):
            head["gpg"] = s.split(":", 1)[1].strip().strip("`")[:100]
        elif s.startswith("**三色:**") or re.match(r"^三色\s*:", s):
            head["color"] = s.split(":", 1)[1].strip()[:30]
        elif s.startswith("**性质:**") or re.match(r"^性质\s*:", s):
            head["nature"] = s.split(":", 1)[1].strip()[:100]
        elif s.startswith("**确认码:**") or re.match(r"^确认码\s*:", s):
            head["confirm"] = s.split(":", 1)[1].strip().strip("`")[:80]

        # fallback: 行内含「龍芯⚡️」且还没找到 DNA
        if not dna_fallback and not head["dna"] and "龍芯⚡️" in line:
            dna_fallback = s.strip("`|").strip()[:200]

    if not head["dna"] and dna_fallback:
        head["dna"] = dna_fallback

    return head

def make_summary(text, head):
    """摘要 = 头部关键行 + 主要章节标题（≤1900 字符）"""
    out = []
    key_prefixes = ("**DNA:**", "**GPG:**", "**三色:**", "**性质:**", "**确认码:**", "**ROOT-SEAL:**")
    for line in text.splitlines()[:30]:
        s = line.strip()
        if not s:
            continue
        if any(s.startswith(p) for p in key_prefixes):
            out.append(s.replace("**", "")[:100])
    out.append("")
    for line in text.splitlines():
        if re.match(r"^#{1,3}\s", line) and len(line) <= 60:
            out.append(line.strip())
    return "\n".join(out)[:1900]

def chunk_text(text, limit=BLOCK_LIMIT):
    """按行合并成 ≤limit 字符的段落块列表。"""
    lines = text.splitlines()
    blocks, buf = [], ""
    for ln in lines:
        if len(ln) > limit:
            if buf:
                blocks.append(buf)
                buf = ""
            while len(ln) > limit:
                blocks.append(ln[:limit])
                ln = ln[limit:]
            buf = ln
            continue
        candidate = buf + ("\n" if buf else "") + ln
        if len(candidate) <= limit:
            buf = candidate
        else:
            blocks.append(buf)
            buf = ln
    if buf:
        blocks.append(buf)
    return blocks

def make_blocks(chunks):
    return [
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {"rich_text": [{"type": "text", "text": {"content": c}}]},
        }
        for c in chunks
    ]

# ────────────────────────────────────────────
# Notion 数据库 & 页面操作
# ────────────────────────────────────────────
def ensure_database(token, dry_run=False):
    """查找/创建日志数据库（幂等）。返回 database_id。"""
    cfg   = load_config()
    db_id = cfg.get("notion_database_id", "")

    if not db_id:
        res = notion_call(token, "search", "POST", {
            "filter": {"value": "database", "property": "object"},
            "query": DB_TITLE, "page_size": 5,
        })
        if "error" not in res:
            for r in res.get("results", []):
                t = r.get("title", [{}])
                if t and t[0].get("plain_text", "") == DB_TITLE:
                    db_id = r["id"]
                    break

    if not db_id:
        if dry_run:
            print("  [dry-run] 将创建 Notion 数据库，跳过")
            return "__DRY_RUN__"
        props = {
            "日志日期": {"date": {}},
            "标题":    {"title": {}},
            "GPG":     {"rich_text": {}},
            "三色":    {"select": {"options": [
                            {"name": "🟢", "color": "green"},
                            {"name": "🟡", "color": "yellow"},
                            {"name": "🔴", "color": "red"},
                       ]}},
            "摘要":    {"rich_text": {}},
            "DNA":     {"rich_text": {}},
            "同步状态": {"select": {"options": [
                            {"name": "synced",  "color": "green"},
                            {"name": "changed", "color": "yellow"},
                       ]}},
            "最近同步": {"date": {}},
        }
        payload = {
            "parent": {"page_id": PARENT_PAGE},
            "title":  [{"type": "text", "text": {"content": DB_TITLE}}],
            "properties": props,
        }
        res = notion_call(token, "databases", "POST", payload)
        if "error" in res:
            print(f"🔴 创建日志库失败: {res}")
            sys.exit(1)
        db_id = res["id"]
        print(f"✅ 已在 Notion 创建日志库: {DB_TITLE}")

    cfg["notion_database_id"] = db_id
    cfg["initialized_at"] = now_iso()
    save_config(cfg)
    return db_id

def find_page_by_date(token, db_id, date):
    """
    按「日志日期」属性精确查询数据库中已有行。
    utility 函数，供手动校验用；sync_log 优先走本地 index 做去重。
    """
    payload = {
        "filter": {"property": "日志日期", "date": {"equals": date}},
        "page_size": 1,
    }
    res = notion_call(token, f"databases/{db_id}/query", "POST", payload)
    if "error" in res:
        return None, res
    results = res.get("results", [])
    return (results[0], None) if results else (None, None)

def build_properties(date, head, summary):
    # [FIX-BUG4] 用列表成员检测，不用字符串字符迭代
    color = head.get("color", "").strip()
    matched = next((e for e in COLOR_EMOJIS if e in color), "🟡")

    dna_val = (head.get("dna") or f"#龍芯⚡️{date}-DAILY-LOG")[:1900]
    gpg_val = (head.get("gpg") or GPG_KEY)[:100]

    return {
        "日志日期": {"date": {"start": date}},
        "标题":    {"title": [{"type": "text", "text": {"content": f"{date} 龍魂日志"}}]},
        "GPG":     {"rich_text": [{"type": "text", "text": {"content": gpg_val}}]},
        "三色":    {"select": {"name": matched}},
        "摘要":    {"rich_text": [{"type": "text", "text": {"content": summary}}]},
        "DNA":     {"rich_text": [{"type": "text", "text": {"content": dna_val}}]},
        "同步状态": {"select": {"name": "synced"}},
        "最近同步": {"date": {"start": now_iso()[:10]}},
    }

def clear_children(token, page_id, dry_run=False):
    """
    删除页面上已有的所有 blocks。
    [FIX-BUG7] 循环翻页拉全量 block_id（v1.0 只取第一页 100 个）。
    [FIX-BUG2] 逐块 DELETE /v1/blocks/{block_id}（Notion 官方删除接口）。
    """
    block_ids = []
    cursor = None
    while True:
        url = f"blocks/{page_id}/children?page_size=100"
        if cursor:
            url += f"&start_cursor={cursor}"
        res = notion_call(token, url, "GET")
        if "error" in res:
            return
        for b in res.get("results", []):
            block_ids.append(b["id"])
        if not res.get("has_more") or not res.get("next_cursor"):
            break
        cursor = res["next_cursor"]

    if not block_ids:
        return

    if dry_run:
        print(f"    [dry-run] 将删除 {len(block_ids)} 个 blocks")
        return

    for bid in block_ids:
        notion_call(token, f"blocks/{bid}", "DELETE")
        time.sleep(0.1)

def append_blocks(token, page_id, blocks, dry_run=False):
    """分批追加正文 blocks（每批 ≤ MAX_CHILDREN=8，防 Cloudflare 403）。"""
    if dry_run:
        print(f"    [dry-run] 将追加 {len(blocks)} 个 blocks")
        return
    for i in range(0, len(blocks), MAX_CHILDREN):
        batch = blocks[i : i + MAX_CHILDREN]
        notion_call(token, f"blocks/{page_id}/children", "PATCH", {"children": batch})
        time.sleep(API_SLEEP)

# ────────────────────────────────────────────
# 核心同步逻辑
# ────────────────────────────────────────────
def sync_log(token, db_id, date, path, idx, force=False, dry_run=False):
    """
    同步单个日志文件到 Notion。
    返回 (status, page_id)，status ∈ {"added", "updated", "skip", "error"}。

    [FIX-BUG1] 所有 index 读写均走 idx["logs"]，不再操作顶层键。
    [保留] 建页时 payload 不带 children（空建），正文一律由 append_blocks
           小批追加 → 防止 45KB 级请求体触发 Cloudflare 403。
    """
    logs = idx.setdefault("logs", {})          # 保证 logs 键存在

    text   = path.read_text(encoding="utf-8")
    digest = sha256_of(path)
    prev   = logs.get(date)                    # [FIX-BUG1] 从 idx["logs"] 取

    if prev and prev.get("sha256") == digest and not force:
        return "skip", prev.get("page_id")

    head    = parse_head(text)
    summary = make_summary(text, head)
    chunks  = chunk_text(text)
    blocks  = make_blocks(chunks)
    props   = build_properties(date, head, summary)

    page_id = prev.get("page_id") if prev else None

    if dry_run:
        action = "update" if page_id else "create"
        print(f"    [dry-run] 将{action} Notion 页面（{len(blocks)} blocks）")
        return ("updated" if page_id else "added"), page_id

    if page_id:
        # ── 更新已有页面 ──
        res = notion_call(token, f"pages/{page_id}", "PATCH", {"properties": props})
        if "error" in res:
            return "error", None
        time.sleep(API_SLEEP)
        clear_children(token, page_id)
        append_blocks(token, page_id, blocks)
        status = "updated"
    else:
        # ── 新建页面（空建，正文后补）──
        payload = {"parent": {"database_id": db_id}, "properties": props}
        res = notion_call(token, "pages", "POST", payload)
        if "error" in res:
            return "error", None
        page_id = res["id"]
        time.sleep(API_SLEEP)
        append_blocks(token, page_id, blocks)
        status = "added"

    # [FIX-BUG1] 写回 idx["logs"]，不写顶层
    logs[date] = {"page_id": page_id, "sha256": digest, "synced_at": now_iso()}
    return status, page_id

# ────────────────────────────────────────────
# 子命令
# ────────────────────────────────────────────
def cmd_sync(token, args):
    if not token:
        print("🔴 未找到 NOTION_TOKEN（lh_vault / notion_config.json / ~/.env / 环境变量均无）")
        sys.exit(1)

    dry_run = getattr(args, "dry_run", False)
    db_id   = ensure_database(token, dry_run=dry_run)

    files = log_files()
    if not files:
        print(f"⚠️  未在 {MEMORY_DIR} 找到任何 YYYY-MM-DD.md 文件")
        return

    if args.date:
        files = [(d, f) for d, f in files if d == args.date]
        if not files:
            print(f"🔴 未找到 {args.date} 对应的日志文件")
            sys.exit(1)

    idx     = load_index()
    added   = updated = skipped = 0
    errs    = []
    changed = False

    for date, path in files:
        status, pid = sync_log(token, db_id, date, path, idx, force=args.force, dry_run=dry_run)
        icon = {"added": "🆕", "updated": "✏️", "skip": "⏭️", "error": "🔴"}.get(status, "❓")
        suffix = f"  → {pid}" if pid and status in ("added", "updated") else ""
        print(f"  {icon} {date}: {status}{suffix}")

        if status == "added":
            added += 1
            changed = True
        elif status == "updated":
            updated += 1
            changed = True
        elif status == "skip":
            skipped += 1
        else:
            errs.append((date, status))

    # [改进] 只有真正有写入时才落盘索引
    if changed and not dry_run:
        save_index(idx)

    tag = " [dry-run]" if dry_run else ""
    ok  = "✅" if not errs else "🟡"
    print(f"\n{ok} 入库完成{tag}: 新增 {added} · 更新 {updated} · 跳过 {skipped} · 失败 {len(errs)}")
    if errs:
        print(f"🔴 失败条目: {errs}")

def cmd_status(_token, _args):
    files   = log_files()
    idx     = load_index()
    logs    = idx.get("logs", {})
    synced  = [d for d, _ in files if d in logs]
    pending = [d for d, _ in files if d not in logs]
    cfg     = load_config()

    print("🐉 操作日志入库引擎 v1.1")
    print(f"  MEMORY_DIR : {MEMORY_DIR}")
    print(f"  本地日志   : {len(files)} 份")
    print(f"  已入库     : {len(synced)} 份")
    print(f"  待入库     : {len(pending)} 份")
    if pending:
        for d in pending[:10]:
            print(f"    - {d}")
        if len(pending) > 10:
            print(f"    ... 共 {len(pending)} 份")
    print(f"  Notion 库  : {cfg.get('notion_database_id', '未初始化')}")
    print(f"  索引文件   : {INDEX_FILE}")
    if synced:
        latest = max(synced)
        print(f"  最新同步   : {latest}  → {logs[latest].get('synced_at', '?')}")

def cmd_sign(_token, _args):
    targets = [Path(__file__), INDEX_FILE, CONFIG_FILE]
    for f in targets:
        if not f.exists():
            print(f"  ⏭️  跳过（不存在）: {f.name}")
            continue
        cmd = [sys.executable, str(BASE / "bin" / "lh_gpg_sign.py"), "sign", "--force", str(f)]
        try:
            r  = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            ok = ("✅" in r.stdout + r.stderr) or r.returncode == 0
            print(f"  {'✅' if ok else '🟡'} 签名 {f.name}")
        except Exception as ex:
            print(f"  🟡 签名失败 {f.name}: {ex}")

# ────────────────────────────────────────────
# 入口
# ────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        prog="lh_logs_sync",
        description="🐉 龍魂·操作日志入库引擎 v1.1",
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("sync", help="增量同步每日日志到 Notion")
    p.add_argument("--date",    default="",   help="只同步指定日期，格式 YYYY-MM-DD")
    p.add_argument("--force",   action="store_true", help="强制全部重写（忽略哈希缓存）")
    p.add_argument("--dry-run", action="store_true", dest="dry_run",
                   help="预演模式，不实际写 Notion")
    p.set_defaults(fn=cmd_sync)

    p = sub.add_parser("status", help="统计本地 vs 已入库日志数")
    p.set_defaults(fn=cmd_status)

    p = sub.add_parser("sign", help="GPG 签名脚本+索引+配置")
    p.set_defaults(fn=cmd_sign)

    args  = parser.parse_args()
    token = get_token() if args.cmd == "sync" else None
    args.fn(token, args)

if __name__ == "__main__":
    main()
