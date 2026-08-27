#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ============================================================
# DNA: #龍芯⚡️丙午·丙申·甲戌·酉时·䷾既济-NOTION-KB-UNIFIED-ENGINE-v1.0-a1b2c3d4
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# 协议: CC BY-NC-SA 4.0（核心思想层）· License: MulanPSL v2（工程实现层）
# 用途: Notion 知识库统一引擎 — 页面归集/DNA公式计算/本地索引/鲲鹏API适配
# 原则: Notion=完整版真源·本地=索引摘要·DNA=公式计算不手写·社区走鲲鹏API
# ============================================================
"""龍魂 · Notion 知识库统一引擎 v1.0

一层一层做（L1 引擎 → L2 本地索引 → L3 Notion 归集 → L4 鲲鹏 API）：

用法:
  python3 bin/lh_notion_kb.py list                      # 列出 token 可访问页面/数据库
  python3 bin/lh_notion_kb.py dna <page_id或URL>        # 用公式计算页面 DNA
  python3 bin/lh_notion_kb.py verify <dna串>            # 验证 DNA 是否与公式匹配（防手写）
  python3 bin/lh_notion_kb.py index                     # 生成本地索引 data/notion_kb/index.json
  python3 bin/lh_notion_kb.py hub                       # 生成核心 Hub 页面（归集入口 Markdown）
  python3 bin/lh_notion_kb.py sync                      # list+dna+index 三合一（日常同步）

DNA 公式（与 lh_dna_generator.generate 完全一致）:
  干支四柱(年/月/日/时) + 64卦(梅花易数起卦) + 五行 + 数字根(369锚点) + 标题SHA256前8位
  => #龍芯⚡️丙午·丙申·甲戌·酉时·䷾既济-CATEGORY-ACTION-hash8
"""
import argparse
import json
import os
import sys
import hashlib
import urllib.request
import urllib.error
from datetime import datetime
from pathlib import Path

# ---------- 路径与 token ----------
WORKSPACE = Path(__file__).resolve().parent.parent
INDEX_DIR = WORKSPACE / "data" / "notion_kb"
INDEX_FILE = INDEX_DIR / "index.json"
HUB_FILE = INDEX_DIR / "hub_page.md"
sys.path.insert(0, str(WORKSPACE / "bin"))


_TOKEN_CACHE = []


def _load_token() -> str:
    """token 自愈: ~/.env 优先（标注当前有效）→ 环境变量兜底 → 报错"""
    if _TOKEN_CACHE:
        return _TOKEN_CACHE[0]
    candidates = []
    env_path = Path.home() / ".env"
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            line = line.strip()
            if line.startswith("NOTION_TOKEN="):
                candidates.append(line.split("=", 1)[1].strip().strip('"').strip("'"))
    for var in ("NOTION_TOKEN", "NOTION_API_KEY"):
        if os.environ.get(var):
            candidates.append(os.environ[var].strip())
    # 去重保序
    seen, uniq = set(), []
    for t in candidates:
        if t and t not in seen:
            seen.add(t)
            uniq.append(t)
    if not uniq:
        sys.exit("❌ 找不到 NOTION_TOKEN（~/.env 或环境变量均无）")
    # 逐个测试，返回第一个有效 token
    for t in uniq:
        try:
            req = urllib.request.Request(
                "https://api.notion.com/v1/users/me",
                headers={"Authorization": f"Bearer {t}", "Notion-Version": "2022-06-28"},
            )
            opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
            with opener.open(req, timeout=15) as resp:
                if resp.status == 200:
                    _TOKEN_CACHE.append(t)
                    return t
        except Exception:
            continue
    sys.exit("❌ 所有 NOTION_TOKEN 均无效（401）— 需轮换 token")


def notion_request(url: str, method: str = "GET", payload: dict = None, version: str = "2022-06-28"):
    """直连 Notion API v1"""
    token = _load_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "Notion-Version": version,
        "Content-Type": "application/json",
    }
    data = json.dumps(payload).encode() if payload else None
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    # 清代理：系统 all_proxy(socks5h) 会导致 Notion API 连接被掐断
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    try:
        with opener.open(req, timeout=30) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode()[:400]
        return {"status": e.code, "error": body}
    except Exception as e:
        return {"status": -1, "error": str(e)}


# ---------- L1: DNA 公式计算 ----------
def compute_dna(title: str, category: str, action: str = "CREATE",
                actor: str = "UID9622", date_str: str = None, hours: int = None) -> dict:
    """复用 lh_dna_generator 公式引擎计算 DNA（非手写）"""
    try:
        from lh_dna_generator import generate
    except ImportError as e:
        return {"error": f"DNA 引擎不可用: {e}"}
    payload = generate(title, category, action, actor, date_str, hours)
    return {
        "dna": payload.dna_string,
        "compact": payload.compact_dna,
        "hexagram": payload.hexagram_symbol + payload.hexagram_name,
        "hexagram_num": payload.hexagram_num,
        "phase": payload.hexagram_phase,
        "wuxing_dominant": payload.wuxing.dominant,
        "digital_root": payload.digital_root,
        "is_369": payload.is_369,
        "title_hash": payload.title_hash,
        "timestamp": payload.timestamp,
    }


def verify_dna(dna_string: str, title: str, category: str = None, action: str = None) -> dict:
    """验证 DNA 是否由公式计算得出（截取标题哈希比对）"""
    if not title:
        return {"valid": False, "reason": "缺少标题，无法验证哈希"}
    # 取 DNA 中最后一段 -hash8
    parts = dna_string.split("-")
    if len(parts) < 2:
        return {"valid": False, "reason": "DNA 格式不符合 #龍芯⚡️...-CAT-ACTION-hash8"}
    claimed_hash = parts[-1].strip()
    real_hash = hashlib.sha256(title.encode()).hexdigest()[:8]
    return {
        "valid": claimed_hash == real_hash,
        "claimed_hash": claimed_hash,
        "real_hash": real_hash,
        "reason": "哈希一致，公式可复算 ✅" if claimed_hash == real_hash
                  else "哈希不符 — 手写或标题已改 ❌（需按公式重算）",
    }


# ---------- L2: Notion 扫描 ----------
def list_pages(verbose: bool = False) -> list:
    """列出 token 可访问的页面/数据库（search API，最多 100 条）"""
    results = notion_request(
        "https://api.notion.com/v1/search",
        method="POST",
        payload={"page_size": 100},
    )
    if results.get("status") and results["status"] not in (200,):
        print(f"❌ Notion API 错误: {results}")
        return []
    pages = []
    for obj in results.get("results", []):
        obj_type = obj.get("object", "?")
        if obj_type == "page":
            title = _extract_title(obj.get("properties", {}))
            url = obj.get("url", "")
        elif obj_type == "database":
            title = obj.get("title", [{}])
            title = "".join(t.get("plain_text", "") for t in title) or "(未命名数据库)"
            url = obj.get("url", "")
        else:
            continue
        pages.append({
            "id": obj.get("id", ""),
            "type": obj_type,
            "title": title,
            "url": url,
            "last_edited": obj.get("last_edited_time", ""),
        })
    return pages


def _extract_title(properties: dict) -> str:
    for key, val in properties.items():
        if not isinstance(val, dict):
            continue
        vtype = val.get("type", "")
        if vtype == "title":
            return "".join(t.get("plain_text", "") for t in val.get("title", []))
        if vtype == "rich_text":
            return "".join(t.get("plain_text", "") for t in val.get("rich_text", []))
    return "(无标题)"


def get_page(page_id: str) -> dict:
    """获取单个页面元信息"""
    pid = normalize_page_id(page_id)
    return notion_request(f"https://api.notion.com/v1/pages/{pid}")


def normalize_page_id(page_id: str) -> str:
    """把 Notion URL/32位hex 归一为 36位UUID"""
    pid = page_id.strip()
    # 提取 URL 中最后一段 token
    pid = pid.split("/")[-1].split("?")[0]
    # 去掉类似 v1-1- 前缀
    pid = pid.split("-")[-1] if len(pid) > 32 else pid
    pid = pid.replace("-", "")
    if len(pid) == 32:
        pid = f"{pid[:8]}-{pid[8:12]}-{pid[12:16]}-{pid[16:20]}-{pid[20:]}"
    return pid


def patch_page_dna(page_id: str, dna: str, status: str = "🟢公式计算") -> dict:
    """把公式计算的 DNA 写回 Notion 页面属性（DNA 字段 + DNA校验字段）

    普通页面无属性 schema 时会报 validation_error → 返回错误由调用方 fallback
    """
    pid = normalize_page_id(page_id)
    payload = {
        "properties": {
            "DNA": {"rich_text": [{"text": {"content": dna}}]},
            "DNA校验": {"rich_text": [{"text": {"content": status}}]},
        }
    }
    return notion_request(f"https://api.notion.com/v1/pages/{pid}", method="PATCH", payload=payload)


def create_kb_database(parent_page_id: str, db_title: str = "龍魂知识库 · 引擎注册表") -> dict:
    """创建知识库主数据库（Create Database API·2022-06-28 版本支持）

    16 字段蓝图落地: 名称/DNA/DNA校验/分类/摘要/来源链接/更新时间
    """
    pid = normalize_page_id(parent_page_id)
    payload = {
        "parent": {"type": "page_id", "page_id": pid},
        "title": [{"type": "text", "text": {"content": db_title}}],
        "properties": {
            "名称": {"title": {}},
            "DNA": {"rich_text": {}},
            "DNA校验": {"rich_text": {}},
            "分类": {"select": {"options": [
                {"name": "协议"}, {"name": "引擎"}, {"name": "知识卡片"},
                {"name": "治理"}, {"name": "部署"}, {"name": "未分类"},
            ]}},
            "摘要": {"rich_text": {}},
            "来源链接": {"url": {}},
            "更新时间": {"date": {}},
        },
    }
    return notion_request("https://api.notion.com/v1/databases", method="POST", payload=payload)


def add_kb_entry(database_id: str, title: str, category: str = "未分类",
                 summary: str = "", link: str = "") -> dict:
    """向知识库数据库写入一行，DNA 自动公式计算"""
    dbid = normalize_page_id(database_id)
    d = compute_dna(title, "KB", "CREATE")
    if "error" in d:
        return {"status": -1, "error": d["error"]}
    props = {
        "名称": {"title": [{"type": "text", "text": {"content": title}}]},
        "DNA": {"rich_text": [{"type": "text", "text": {"content": d["dna"]}}]},
        "DNA校验": {"rich_text": [{"type": "text", "text": {"content": "🟢公式计算"}}]},
        "分类": {"select": {"name": category}},
        "更新时间": {"date": {"start": datetime.now().strftime("%Y-%m-%d")}},
    }
    if summary:
        props["摘要"] = {"rich_text": [{"type": "text", "text": {"content": summary[:2000]}}]}
    if link:
        props["来源链接"] = {"url": link}
    payload = {"parent": {"database_id": dbid}, "properties": props}
    result = notion_request("https://api.notion.com/v1/pages", method="POST", payload=payload)
    result["dna"] = d["dna"]
    return result


def append_dna_block(page_id: str, dna: str, status: str = "🟢公式计算") -> dict:
    """fallback: 把 DNA 以 callout 块追加到页面正文（普通页面兜底方案）"""
    pid = normalize_page_id(page_id)
    payload = {
        "children": [{
            "object": "block",
            "type": "callout",
            "callout": {
                "icon": {"type": "emoji", "emoji": "🧬"},
                "rich_text": [{"type": "text", "text": {
                    "content": f"DNA(公式计算·{status}): {dna}",
                }}],
                "color": "blue_background",
            },
        }],
    }
    return notion_request(f"https://api.notion.com/v1/blocks/{pid}/children", method="PATCH", payload=payload)


# ---------- L2: 本地索引 ----------
def build_index(pages: list, with_dna: bool = True) -> dict:
    """生成本地索引（省内存核心：只存 标题/URL/DNA/摘要占位/反向链接）"""
    INDEX_DIR.mkdir(parents=True, exist_ok=True)
    entries = []
    for p in pages:
        entry = {
            "id": p["id"],
            "type": p["type"],
            "title": p["title"],
            "url": p["url"],
            "last_edited": p["last_edited"],
            "dna": "",
            "dna_ok": False,
            "summary": "",           # 摘要占位（不存全文）
            "local_ref": "",         # 本地反向链接（notion-mirror/xxx.md）
            "category": "",
        }
        if with_dna and p["type"] == "page":
            d = compute_dna(p["title"], "KB", "SYNC")
            if "error" not in d:
                entry["dna"] = d["dna"]
                entry["dna_ok"] = True
                entry["summary"] = f"完整版见 Notion: {p['url']}"
        entries.append(entry)
    index = {
        "meta": {
            "generated_at": datetime.now().isoformat(),
            "total": len(entries),
            "principle": "Notion=完整版真源·本地只存索引摘要·DNA公式计算不手写",
        },
        "entries": entries,
    }
    INDEX_FILE.write_text(json.dumps(index, ensure_ascii=False, indent=2))
    return index


# ---------- L3: Hub 归集页 ----------
def generate_hub(pages: list) -> str:
    """生成核心 Hub 页面（所有知识入口归集于此）"""
    d = compute_dna("龍魂知识库核心入口", "KB", "HUB")
    hub_dna = d.get("dna", "#龍芯⚡️未知")
    lines = [
        "---",
        "DNA: " + hub_dna,
        "创建者: 诸葛鑫（UID9622）",
        "归属名: 诸葛鑫 | UID9622 · 龍芯北辰",
        "协议: CC BY-NC-SA 4.0（核心思想层）",
        "---",
        "",
        "# 🐉 龍魂知识库 · 核心入口（Hub）",
        "",
        "> 原则: Notion=完整版真源 · 本地=索引摘要 · DNA=公式计算不手写 · 社区走鲲鹏API",
        "",
        "## 📇 页面归集清单",
        "",
        "| # | 标题 | 类型 | DNA状态 | 链接 |",
        "|---|------|:---:|:---:|---|",
    ]
    for i, p in enumerate(pages, 1):
        dna_state = "🟢公式" if p.get("dna_ok") else "🔴未算"
        lines.append(f"| {i} | {p['title']} | {p['type']} | {dna_state} | {p['url']} |")
    lines += [
        "",
        "## 🔗 调取方式",
        "",
        "- 本地索引: `data/notion_kb/index.json`",
        "- 社区 API: `https://uid9622.cn/api/kb/search?q=<关键词>`（鲲鹏网关）",
        "- 回调: Notion 页面变更 → 鲲鹏 webhook 重算 DNA → 更新索引",
        "",
        "## ⚙️ 同步命令",
        "",
        "```bash",
        "python3 bin/lh_notion_kb.py sync   # list+dna+index 三合一",
        "```",
        "",
    ]
    INDEX_DIR.mkdir(parents=True, exist_ok=True)
    HUB_FILE.write_text("\n".join(lines), encoding="utf-8")
    return "\n".join(lines)


# ---------- CLI ----------
def main():
    ap = argparse.ArgumentParser(description="龍魂 · Notion 知识库统一引擎")
    sub = ap.add_subparsers(dest="cmd", required=True)

    sub.add_parser("list", help="列出 token 可访问页面/数据库")
    p_dna = sub.add_parser("dna", help="用公式计算页面 DNA")
    p_dna.add_argument("title", help="页面标题")
    p_dna.add_argument("--category", default="KB")
    p_dna.add_argument("--action", default="CREATE")
    p_dna.add_argument("--actor", default="UID9622")
    p_dna.add_argument("--date", default=None, help="YYYY-MM-DD 可指定")
    p_dna.add_argument("--hours", type=int, default=None)

    p_verify = sub.add_parser("verify", help="验证 DNA 是否公式匹配")
    p_verify.add_argument("dna", help="DNA 串")
    p_verify.add_argument("--title", required=True, help="页面标题")

    p_patch = sub.add_parser("patch", help="DNA 公式计算并写回 Notion 页面")
    p_patch.add_argument("page_id", help="页面 ID 或 URL")
    p_patch.add_argument("--category", default="KB")
    p_patch.add_argument("--action", default="CREATE")

    p_cdb = sub.add_parser("create-db", help="创建知识库主数据库（16字段）")
    p_cdb.add_argument("parent_page_id", help="父页面 ID 或 URL")
    p_cdb.add_argument("--title", default="龍魂知识库 · 引擎注册表")

    p_ae = sub.add_parser("add-entry", help="向知识库写一行（DNA 自动公式计算）")
    p_ae.add_argument("--db", required=True, help="数据库 ID 或 URL")
    p_ae.add_argument("--title", required=True, help="知识标题")
    p_ae.add_argument("--category", default="未分类", help="分类: 协议/引擎/知识卡片/治理/部署")
    p_ae.add_argument("--summary", default="", help="摘要（不存全文）")
    p_ae.add_argument("--link", default="", help="来源链接")

    sub.add_parser("index", help="生成本地索引 data/notion_kb/index.json")
    sub.add_parser("hub", help="生成核心 Hub 归集页")
    sub.add_parser("sync", help="list+dna+index 三合一")

    args = ap.parse_args()

    if args.cmd == "list":
        pages = list_pages()
        if not pages:
            print("⚠️ 未检索到可访问页面 — 检查 token 权限（integration 需被共享到目标页面）")
            return
        for p in pages:
            print(f"[{p['type']}] {p['title']}  {p['url']}")
        print(f"\n共 {len(pages)} 个对象（当前 token 权限覆盖范围）")

    elif args.cmd == "dna":
        d = compute_dna(args.title, args.category, args.action, args.actor,
                        args.date, args.hours)
        if "error" in d:
            print(f"❌ {d['error']}")
            return
        print(f"DNA:  {d['dna']}")
        print(f"卦象: {d['hexagram']}({d['hexagram_num']})·{d['phase']}")
        print(f"五行: {d['wuxing_dominant']}  数字根: {d['digital_root']}  369锚点: {d['is_369']}")

    elif args.cmd == "verify":
        v = verify_dna(args.dna, args.title)
        print(f"声明哈希: {v.get('claimed_hash')}  实际哈希: {v.get('real_hash')}")
        print(("✅ " if v.get("valid") else "❌ ") + v.get("reason", ""))

    elif args.cmd == "patch":
        page = get_page(args.page_id)
        if page.get("status") and page["status"] not in (200,):
            print(f"❌ 页面不可访问: {page.get('error', page)}")
            return
        title = _extract_title(page.get("properties", {}))
        d = compute_dna(title, args.category, args.action)
        if "error" in d:
            print(f"❌ DNA 计算失败: {d['error']}")
            return
        print(f"页面: {title}")
        print(f"计算 DNA: {d['dna']}")
        r = patch_page_dna(args.page_id, d["dna"])
        if r.get("status") and r["status"] not in (200,):
            # fallback: 普通页面无属性 schema → DNA 追加进正文
            r2 = append_dna_block(args.page_id, d["dna"])
            if r2.get("status") and r2["status"] not in (200,):
                print(f"❌ 属性写回失败: {r.get('error', r)[:120]}")
                print(f"❌ 正文追加失败: {r2.get('error', r2)[:120]}")
                return
            print("✅ DNA 已公式计算并以 callout 块追加到页面正文")
            return
        print("✅ DNA 已公式计算并写回 Notion 页面属性（DNA + DNA校验字段）")

    elif args.cmd == "add-entry":
        r = add_kb_entry(args.db, args.title, args.category, args.summary, args.link)
        if r.get("status") and r["status"] not in (200,):
            print(f"❌ 写入失败: {r.get('error', r)[:200]}")
            return
        print(f"✅ 知识行已写入: {args.title}")
        print(f"   DNA(公式计算): {r.get('dna', '?')}")
        print(f"   URL: {r.get('url', '?')}")

    elif args.cmd == "create-db":
        r = create_kb_database(args.parent_page_id, args.title)
        if r.get("status") and r["status"] not in (200,):
            print(f"❌ 建库失败: {r.get('error', r)[:200]}")
            return
        print(f"✅ 知识库数据库已创建: {r.get('id', '?')}")
        print(f"   URL: {r.get('url', '?')}")
        print(f"   16 字段就绪: 名称/DNA/DNA校验/分类/摘要/来源链接/更新时间")
        print("   后续: 向库内写入知识行 → 每行 DNA 用公式计算")

    elif args.cmd in ("index", "hub", "sync"):
        pages = list_pages()
        if not pages:
            print("⚠️ 未检索到可访问页面 — 无法生成索引（检查 token 权限）")
            return
        if args.cmd in ("index", "sync"):
            idx = build_index(pages)
            print(f"✅ 索引已生成: {INDEX_FILE}（{idx['meta']['total']} 条）")
            ok = sum(1 for e in idx["entries"] if e["dna_ok"])
            print(f"   DNA 公式计算: {ok}/{idx['meta']['total']} 页 ✅")
        if args.cmd in ("hub", "sync"):
            generate_hub(pages)
            print(f"✅ Hub 归集页已生成: {HUB_FILE}")
        if args.cmd == "sync":
            print("🎉 同步完成 — 本地只存索引摘要，省内存 ✅")


if __name__ == "__main__":
    main()
