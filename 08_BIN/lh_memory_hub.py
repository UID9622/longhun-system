#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·丙申·乙丑·壬午·䷨损-MEMORY-HUB-v1.0-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CREATOR: 诸葛鑫 (UID9622)
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""
═══════════════════════════════════════════
🐉 龍魂·跨AI协作记忆库引擎 v1.0
═══════════════════════════════════════════
用途: CodeBuddy × Kimi × 任何AI 共享同一份记忆。
      Notion(云端主库·全文检索) + 本地JSON(向量检索·零依赖) 双索引。

能力:
  init     初始化本地库 + 在Notion创建记忆库(幂等)
  add      操作后填写记忆(本地+Notion+协作签名+非空校验)
  search   关键词检索(本地+Notion)
  vector   向量检索(字符n-gram哈希·零依赖·余弦相似度)
  pull     从Notion拉取全部 → 本地缓存(启动自动读取)
  push     本地 → Notion 增量同步
  backfill 回填本地现有记忆源(MEMORY.md铁律/每日日志/索引库)
  check    非空校验(必填字段扫描·不能留空)
  status   统计状态
  sign     本地文件GPG签名

运行: python3 bin/lh_memory_hub.py <子命令> [参数]
"""
import argparse
import hashlib
import json
import math
import os
import re
import subprocess
import sys
import urllib.request
import urllib.error
from datetime import datetime, timezone
from pathlib import Path

# ────────────────────────────────────────────
# 常量
# ────────────────────────────────────────────
BASE = Path.home() / "longhun-system"
HUB_DIR = BASE / "12_DOCS" / "dragon-soul-open-hub"
LOCAL_JSON = HUB_DIR / "memory-hub.json"
CONFIG_JSON = HUB_DIR / "memory-hub-config.json"
NOTION_VERSION = "2022-06-28"
DB_TITLE = "🐉 龍魂·跨AI协作记忆库 v1.0"

# 必填字段(非空校验·不能留空)
REQUIRED_FIELDS = ["title", "content", "category", "creator", "signature", "dna", "status"]

# 分类枚举
CATEGORIES = ["身份", "铁律", "里程碑", "教训", "技术", "人格", "部署", "协议", "偏好", "其他"]

# Notion 数据库属性定义(建库用)
NOTION_PROPERTIES = {
    "记忆标题": {"title": {}},
    "记忆内容": {"rich_text": {}},
    "分类": {"select": {"options": [{"name": c, "color": "blue"} for c in CATEGORIES]}},
    "关键词": {"multi_select": {}},
    "创建者": {"select": {"options": [
        {"name": "UID9622", "color": "red"},
        {"name": "CodeBuddy", "color": "green"},
        {"name": "Kimi", "color": "purple"},
        {"name": "龍魂AI", "color": "orange"},
        {"name": "其他", "color": "gray"},
    ]}},
    "协作签名": {"rich_text": {}},
    "DNA追溯码": {"rich_text": {}},
    "状态": {"select": {"options": [
        {"name": "active", "color": "green"},
        {"name": "frozen", "color": "yellow"},
        {"name": "archived", "color": "gray"},
    ]}},
    "优先级": {"number": {"format": "number"}},
    "来源": {"rich_text": {}},
    "最近更新": {"date": {}},
    "关联ID": {"rich_text": {}},
}


# ────────────────────────────────────────────
# 工具函数
# ────────────────────────────────────────────
def get_token():
    """从 ~/.env 读取 NOTION_TOKEN，不打印明文"""
    env = Path.home() / ".env"
    if not env.exists():
        print("🔴 ~/.env 不存在")
        return None
    for line in env.read_text().splitlines():
        line = line.strip()
        if line.startswith("NOTION_TOKEN="):
            return line.split("=", 1)[1].strip().strip('"').strip("'")
    print("🔴 ~/.env 中未找到 NOTION_TOKEN")
    return None


def notion_call(token, path, method="GET", data=None):
    """调用 Notion API"""
    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(
        f"https://api.notion.com/v1/{path}", data=body, method=method,
        headers={
            "Authorization": f"Bearer {token}",
            "Notion-Version": NOTION_VERSION,
            "Content-Type": "application/json",
        })
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        detail = e.read().decode()[:600]
        return {"error": e.code, "detail": detail}


def now_iso():
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def make_dna(module="MEMORY-HUB", n=8):
    """生成 DNA 追溯码"""
    h = hashlib.sha1(f"{module}-{datetime.now().timestamp()}".encode()).hexdigest()[:n].upper()
    return f"#龍芯⚡️{datetime.now().strftime('%Y%m%d')}-{module}-{h}"


def text_vector(text, dim=256):
    """字符 n-gram 哈希向量(零依赖·中文友好·低算力)"""
    vec = [0.0] * dim
    t = re.sub(r"\s+", "", (text or "").lower())
    if not t:
        return vec
    grams = [t[i:i + 2] for i in range(len(t) - 1)] or [t]
    for g in grams:
        h = int(hashlib.md5(g.encode()).hexdigest(), 16) % dim
        vec[h] += 1.0
    norm = math.sqrt(sum(v * v for v in vec))
    return [v / norm for v in vec] if norm else vec


def cosine(a, b):
    return sum(x * y for x, y in zip(a, b))


def load_local():
    if LOCAL_JSON.exists():
        try:
            return json.loads(LOCAL_JSON.read_text(encoding="utf-8"))
        except Exception:
            return {"schema_version": "1.0.0", "entries": []}
    return {"schema_version": "1.0.0", "entries": []}


def save_local(data):
    """写本地库 + 写后验证非空(记错本 DELIVER-001 防坑)"""
    LOCAL_JSON.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    size = LOCAL_JSON.stat().st_size
    if size < 10:
        print(f"🔴 本地写入异常: 仅 {size} 字节")
        return False
    return True


def load_config():
    if CONFIG_JSON.exists():
        try:
            return json.loads(CONFIG_JSON.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}


def save_config(cfg):
    CONFIG_JSON.write_text(json.dumps(cfg, ensure_ascii=False, indent=2), encoding="utf-8")


def signature_of(creator, dna):
    """协作签名: 创建者@UTC时间@DNA短码"""
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    short = dna.split("-")[-1] if "-" in dna else dna[:8]
    return f"{creator}@{ts}@{short}"


def clean_ms(kw):
    """Notion multi_select 不允许逗号 → 过滤并截断"""
    cleaned = []
    for k in kw or []:
        k = str(k).strip().replace(",", " ").replace("，", " ")[:80]
        if k and k not in cleaned:
            cleaned.append(k)
    return cleaned[:20]


def validate(entry):
    """非空校验·不能留空"""
    missing = [f for f in REQUIRED_FIELDS if not entry.get(f)]
    return missing


# ────────────────────────────────────────────
# 子命令实现
# ────────────────────────────────────────────
def cmd_init(token, args):
    """初始化: 创建本地库 + Notion建库(幂等)"""
    cfg = load_config()
    db_id = cfg.get("notion_database_id")

    if not db_id:
        # 查找是否已存在同名库
        res = notion_call(token, "search", "POST",
                          {"filter": {"value": "database", "property": "object"},
                           "query": DB_TITLE, "page_size": 5})
        if "error" not in res:
            for r in res.get("results", []):
                t = r.get("title", [{}])
                title = t[0].get("plain_text", "") if t else ""
                if title == DB_TITLE:
                    db_id = r["id"]
                    break
    if not db_id:
        # 创建数据库(挂在「宪法与协议」页下)
        parent_page = "34d7125a-9c9f-810b-a891-efd64794db8b"
        payload = {
            "parent": {"page_id": parent_page},
            "title": [{"type": "text", "text": {"content": DB_TITLE}}],
            "properties": NOTION_PROPERTIES,
        }
        res = notion_call(token, "databases", "POST", payload)
        if "error" in res:
            print(f"🔴 创建 Notion 库失败: {res}")
            sys.exit(1)
        db_id = res["id"]
        print(f"✅ 已在 Notion 创建数据库: {DB_TITLE}")
    else:
        print(f"✅ 复用现有 Notion 数据库: {DB_TITLE}")

    cfg["notion_database_id"] = db_id
    cfg["schema_version"] = "1.0.0"
    cfg["initialized_at"] = now_iso()
    cfg["dna"] = make_dna("MEMORY-HUB-INIT")
    save_config(cfg)

    # 初始化本地库
    data = load_local()
    if not data.get("entries"):
        data["schema_version"] = "1.0.0"
        data["notion_database_id"] = db_id
        data["initialized_at"] = now_iso()
        data["entries"] = []
        save_local(data)

    print(f"✅ 本地库就绪: {LOCAL_JSON}")
    print(f"📌 Notion 库 ID: {db_id}")
    print("下一步: python3 bin/lh_memory_hub.py backfill  # 回填现有记忆")
    print("        python3 bin/lh_memory_hub.py pull      # 启动时自动拉取")


def cmd_add(token, args):
    """操作后填写记忆"""
    cfg = load_config()
    db_id = cfg.get("notion_database_id")
    if not db_id:
        print("🔴 未初始化，先跑: python3 bin/lh_memory_hub.py init")
        sys.exit(1)

    creator = args.creator or "CodeBuddy"
    dna = make_dna("MEM-HUB-ADD")
    entry = {
        "title": args.title,
        "content": args.content,
        "category": args.category if args.category in CATEGORIES else "其他",
        "keywords": args.keywords or [],
        "creator": creator,
        "signature": signature_of(creator, dna),
        "dna": dna,
        "status": args.status,
        "priority": args.priority,
        "source": args.source or "",
        "vector": text_vector(args.content),
        "created_at": now_iso(),
        "updated_at": now_iso(),
    }

    missing = validate(entry)
    if missing:
        print(f"🔴 必填字段为空，不能留空: {', '.join(missing)}")
        sys.exit(1)

    # 写本地
    data = load_local()
    data["entries"].append(entry)
    if not save_local(data):
        sys.exit(1)
    print(f"✅ 已写入本地记忆: {entry['title']}")

    # 写 Notion
    if token:
        props = {
            "记忆标题": {"title": [{"type": "text", "text": {"content": entry["title"]}}]},
            "记忆内容": {"rich_text": [{"type": "text", "text": {"content": entry["content"]}}]},
            "分类": {"select": {"name": entry["category"]}},
            "关键词": {"multi_select": [{"name": k} for k in clean_ms(entry["keywords"])]},
            "创建者": {"select": {"name": creator}},
            "协作签名": {"rich_text": [{"type": "text", "text": {"content": entry["signature"]}}]},
            "DNA追溯码": {"rich_text": [{"type": "text", "text": {"content": dna}}]},
            "状态": {"select": {"name": entry["status"]}},
            "优先级": {"number": entry["priority"]},
            "来源": {"rich_text": [{"type": "text", "text": {"content": entry["source"]}}]},
            "最近更新": {"date": {"start": entry["created_at"][:10]}},
            "关联ID": {"rich_text": [{"type": "text", "text": {"content": str(len(data["entries"]))}}]},
        }
        res = notion_call(token, "pages", "POST",
                          {"parent": {"database_id": db_id}, "properties": props})
        if "error" in res:
            print(f"🟡 Notion 写入失败(本地已存): {res}")
        else:
            print(f"✅ 已写入 Notion: {entry['title']}")
    return entry


def cmd_search(token, args):
    """关键词检索"""
    data = load_local()
    q = args.query.lower()
    hits = []
    for e in data.get("entries", []):
        hay = json.dumps({k: v for k, v in e.items() if k != "vector"}, ensure_ascii=False).lower()
        if q in hay:
            hits.append(e)
    print(f"🔍 本地关键词检索「{args.query}」→ {len(hits)} 条")
    for e in hits[:args.limit]:
        print(f"  [{e['category']}] {e['title']} | {e['creator']} | {e['status']}")
        print(f"    {e['content'][:80]}...")
    if token and args.notion:
        res = notion_call(token, "search", "POST",
                          {"query": args.query, "page_size": args.limit,
                           "filter": {"value": "page", "property": "object"}})
        if "error" not in res:
            print(f"\n🌐 Notion 检索 → {len(res.get('results', []))} 条")
            for r in res.get("results", [])[:args.limit]:
                t = r.get("properties", {}).get("记忆标题", {}).get("title", [])
                title = t[0].get("plain_text", "?") if t else "?"
                print(f"  - {title}")


def cmd_vector(args):
    """向量检索(零依赖)"""
    data = load_local()
    qv = text_vector(args.query)
    scored = []
    for e in data.get("entries", []):
        ev = e.get("vector") or text_vector(e.get("content", ""))
        scored.append((cosine(qv, ev), e))
    scored.sort(key=lambda x: -x[0])
    print(f"🧭 向量检索「{args.query}」→ Top {args.limit}")
    for score, e in scored[:args.limit]:
        if score < args.threshold:
            break
        print(f"  [{score:.3f}] {e['title']} | {e['category']} | {e['creator']}")
        print(f"    {e['content'][:80]}...")


def cmd_pull(token, args):
    """从 Notion 拉取全部 → 本地缓存(启动自动读取)"""
    cfg = load_config()
    db_id = cfg.get("notion_database_id")
    if not db_id or not token:
        print("🔴 未初始化或无 token")
        sys.exit(1)
    results = []
    has_more = True
    cursor = None
    while has_more:
        payload = {"page_size": 100}
        if cursor:
            payload["start_cursor"] = cursor
        res = notion_call(token, f"databases/{db_id}/query", "POST", payload)
        if "error" in res:
            print(f"🔴 Notion 拉取失败: {res}")
            sys.exit(1)
        results.extend(res.get("results", []))
        has_more = res.get("has_more", False)
        cursor = res.get("next_cursor")

    entries = []
    for r in results:
        p = r.get("properties", {})
        def rt(name):
            arr = p.get(name, {}).get("rich_text", [])
            return arr[0].get("plain_text", "") if arr else ""
        def tt(name):
            arr = p.get(name, {}).get("title", [])
            return arr[0].get("plain_text", "") if arr else ""
        def ms(name):
            return [o.get("name", "") for o in p.get(name, {}).get("multi_select", [])]
        def sel(name):
            s = p.get(name, {}).get("select")
            return s.get("name", "") if s else ""
        entries.append({
            "title": tt("记忆标题"),
            "content": rt("记忆内容"),
            "category": sel("分类"),
            "keywords": ms("关键词"),
            "creator": sel("创建者"),
            "signature": rt("协作签名"),
            "dna": rt("DNA追溯码"),
            "status": sel("状态"),
            "priority": (p.get("优先级", {}).get("number") or 0),
            "source": rt("来源"),
            "vector": text_vector(rt("记忆内容")),
            "synced_at": now_iso(),
        })
    data = load_local()
    data["entries"] = entries
    data["synced_at"] = now_iso()
    if save_local(data):
        print(f"✅ 已从 Notion 拉取 {len(entries)} 条记忆 → 本地缓存")
        print(f"   最近: {entries[0]['title']}" if entries else "   空库")


def cmd_push(token, args):
    """本地 → Notion 增量同步"""
    cfg = load_config()
    db_id = cfg.get("notion_database_id")
    if not db_id or not token:
        print("🔴 未初始化或无 token")
        sys.exit(1)
    data = load_local()
    # 拉 Notion 现有 DNA 集合
    res = notion_call(token, f"databases/{db_id}/query", "POST", {"page_size": 100})
    if "error" in res:
        print(f"🔴 查询失败: {res}")
        sys.exit(1)
    existing = set()
    for r in res.get("results", []):
        arr = r.get("properties", {}).get("DNA追溯码", {}).get("rich_text", [])
        if arr:
            existing.add(arr[0].get("plain_text", ""))
    added = 0
    for e in data.get("entries", []):
        if e.get("dna") in existing:
            continue
        props = {
            "记忆标题": {"title": [{"type": "text", "text": {"content": e["title"]}}]},
            "记忆内容": {"rich_text": [{"type": "text", "text": {"content": e["content"]}}]},
            "分类": {"select": {"name": e.get("category", "其他")}},
            "关键词": {"multi_select": [{"name": k} for k in clean_ms(e.get("keywords", []))]},
            "创建者": {"select": {"name": e.get("creator", "其他")}},
            "协作签名": {"rich_text": [{"type": "text", "text": {"content": e.get("signature", "")}}]},
            "DNA追溯码": {"rich_text": [{"type": "text", "text": {"content": e.get("dna", "")}}]},
            "状态": {"select": {"name": e.get("status", "active")}},
            "优先级": {"number": e.get("priority", 0)},
            "来源": {"rich_text": [{"type": "text", "text": {"content": e.get("source", "")}}]},
            "最近更新": {"date": {"start": e.get("updated_at", now_iso())[:10]}},
        }
        res2 = notion_call(token, "pages", "POST",
                           {"parent": {"database_id": db_id}, "properties": props})
        if "error" not in res2:
            added += 1
        else:
            print(f"🟡 写入失败 {e['title']}: {res2}")
    print(f"✅ 增量同步完成: 新增 {added} 条到 Notion")


def cmd_backfill(token, args):
    """回填本地现有记忆源"""
    data = load_local()
    existing_titles = {e["title"] for e in data.get("entries", [])}
    added = 0

    sources = []

    # ① MEMORY.md 铁律(§3)
    mem = BASE / ".codebuddy" / "memory" / "MEMORY.md"
    if mem.exists():
        for line in mem.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if re.match(r"^\d+\.", line):
                title = line.split("):", 1)[0].replace("**", "")[:60] if "):" in line else line[:60]
                sources.append({"title": title, "content": line[:500],
                                "category": "铁律", "keywords": ["MEMORY", "铁律"]})

    # ② 今日日志(最近条目)
    today = BASE / ".codebuddy" / "memory" / "2026-08-19.md"
    if today.exists():
        for line in today.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line.startswith("- **") and len(line) > 20:
                title = line.split("**")[1][:50] if len(line.split("**")) > 1 else line[:50]
                sources.append({"title": f"日志·{title}", "content": line[:500],
                                "category": "里程碑", "keywords": ["日志"]})

    # ③ 统一索引库
    idx = HUB_DIR / "unified-index-hub.json"
    if idx.exists():
        try:
            hub = json.loads(idx.read_text(encoding="utf-8"))
            for e in hub.get("entries", [])[:50]:
                sources.append({"title": e.get("title", "?"), "content": e.get("description", ""),
                                "category": "索引", "keywords": e.get("keywords", [])[:5],
                                "source": e.get("source_file", "")})
        except Exception as ex:
            print(f"🟡 索引库读取失败: {ex}")

    # ④ 人格不动点注册表
    fp = HUB_DIR / "persona-fixpoint-registry.json"
    if fp.exists():
        try:
            reg = json.loads(fp.read_text(encoding="utf-8"))
            for e in reg.get("personas", [])[:50]:
                sources.append({"title": f"不动点·{e.get('persona_name', '?')}",
                                "content": e.get("duty", ""), "category": "人格",
                                "keywords": ["不动点"], "source": "persona-fixpoint-registry"})
        except Exception:
            pass

    for s in sources:
        if not s.get("content"):
            continue
        if s["title"] in existing_titles:
            continue
        creator = "回填机器人"
        dna = make_dna("BACKFILL")
        entry = {
            "title": s["title"],
            "content": s["content"],
            "category": s.get("category", "其他"),
            "keywords": s.get("keywords", []),
            "creator": creator,
            "signature": signature_of(creator, dna),
            "dna": dna,
            "status": "active",
            "priority": 1,
            "source": s.get("source", ""),
            "vector": text_vector(s["content"]),
            "created_at": now_iso(),
            "updated_at": now_iso(),
        }
        data["entries"].append(entry)
        added += 1

    if save_local(data):
        print(f"✅ 回填完成: 新增 {added} 条 · 本地记忆库现有 {len(data['entries'])} 条")
        if token:
            print("   运行 push 同步到 Notion: python3 bin/lh_memory_hub.py push")


def cmd_check(args):
    """非空校验"""
    data = load_local()
    bad = []
    for e in data.get("entries", []):
        missing = validate(e)
        if missing:
            bad.append((e.get("title", "?"), missing))
    print(f"📋 记忆库共 {len(data.get('entries', []))} 条")
    if bad:
        print(f"🔴 非空校验失败 {len(bad)} 条:")
        for title, miss in bad:
            print(f"  - {title}: 缺 {', '.join(miss)}")
        sys.exit(1)
    print("✅ 全部必填字段非空·校验通过·不能留空 ✔")


def cmd_status(args):
    """统计"""
    data = load_local()
    entries = data.get("entries", [])
    from collections import Counter
    cats = Counter(e.get("category", "?") for e in entries)
    creators = Counter(e.get("creator", "?") for e in entries)
    status = Counter(e.get("status", "?") for e in entries)
    print(f"🐉 跨AI协作记忆库 · 共 {len(entries)} 条")
    print(f"  分类: {dict(cats)}")
    print(f"  创建者: {dict(creators)}")
    print(f"  状态: {dict(status)}")
    print(f"  本地: {LOCAL_JSON}")
    cfg = load_config()
    print(f"  Notion 库: {cfg.get('notion_database_id', '未初始化')}")


def cmd_sign(args):
    """本地文件 GPG 签名"""
    for f in [LOCAL_JSON, CONFIG_JSON, Path(__file__)]:
        if f.exists():
            cmd = ["python3", str(BASE / "bin" / "lh_gpg_sign.py"), "sign", "--force", str(f)]
            try:
                r = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
                ok = "✅" in r.stdout + r.stderr or "✓" in r.stdout + r.stderr or r.returncode == 0
                print(f"{'✅' if ok else '🟡'} 签名 {f.name}: {r.stdout.strip()[-80:] if r.stdout else r.stderr.strip()[-80:]}")
            except Exception as ex:
                print(f"🟡 签名失败 {f.name}: {ex}")


# ────────────────────────────────────────────
# 主入口
# ────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(prog="lh_memory_hub",
                                     description="🐉 龍魂·跨AI协作记忆库引擎")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("init", help="初始化本地库+Notion建库")
    p.set_defaults(fn=cmd_init)

    p = sub.add_parser("add", help="操作后填写记忆")
    p.add_argument("--title", required=True)
    p.add_argument("--content", required=True)
    p.add_argument("--category", default="其他", choices=CATEGORIES)
    p.add_argument("--keywords", nargs="*", default=[])
    p.add_argument("--creator", default="CodeBuddy")
    p.add_argument("--status", default="active")
    p.add_argument("--priority", type=int, default=1)
    p.add_argument("--source", default="")
    p.set_defaults(fn=cmd_add)

    p = sub.add_parser("search", help="关键词检索")
    p.add_argument("query")
    p.add_argument("--limit", type=int, default=10)
    p.add_argument("--notion", action="store_true", help="同时搜 Notion")
    p.set_defaults(fn=cmd_search)

    p = sub.add_parser("vector", help="向量检索")
    p.add_argument("query")
    p.add_argument("--limit", type=int, default=5)
    p.add_argument("--threshold", type=float, default=0.1)
    p.set_defaults(fn=cmd_vector)

    p = sub.add_parser("pull", help="从Notion拉取→本地")
    p.set_defaults(fn=cmd_pull)

    p = sub.add_parser("push", help="本地→Notion同步")
    p.set_defaults(fn=cmd_push)

    p = sub.add_parser("backfill", help="回填本地记忆源")
    p.set_defaults(fn=cmd_backfill)

    p = sub.add_parser("check", help="非空校验")
    p.set_defaults(fn=cmd_check)

    p = sub.add_parser("status", help="统计状态")
    p.set_defaults(fn=cmd_status)

    p = sub.add_parser("sign", help="GPG签名")
    p.set_defaults(fn=cmd_sign)

    args = parser.parse_args()
    token = get_token() if args.cmd in ("init", "add", "search", "pull", "push", "backfill") else None

    # 非网络命令也传 token 给需要处
    if args.cmd in ("add", "search"):
        args._token = token
    args.fn(token, args) if args.cmd in ("init", "pull", "push", "backfill") else \
        (args.fn(token, args) if args.cmd == "add" else
         (args.fn(token, args) if args.cmd == "search" else args.fn(args)))


if __name__ == "__main__":
    main()
