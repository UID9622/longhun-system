#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""
🐉 龍魂 · 工作间三端同步引擎 v1.0

整理本地工作间内容 → 同步到 Notion 镜像库 + 鲲鹏服务器。

三端联动:
  Mac本地 longhun-system  ──→  Notion 镜像库（检索/展示）
        │
        └──────────────→  鲲鹏服务器（备份/协作中枢）

用法:
  python3 bin/lh_workspace_sync.py --scan           # 1️⃣ 整理：扫描本地核心层 → 生成工作间清单
  python3 bin/lh_workspace_sync.py --to-notion      # 2️⃣ 推送：清单+核心文档 → Notion 镜像库
  python3 bin/lh_workspace_sync.py --to-kunpeng     # 3️⃣ 联动：同步到鲲鹏（rsync 全量 + collab 协作）
  python3 bin/lh_workspace_sync.py --all            # 🚀 一键三端全跑

DNA: #龍芯⚡️丙午·丙申·己未·未时·䷋否-WORKSPACE-SYNC-v1.0
创建者: 诸葛鑫（UID9622·龍芯北辰）
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, List

CST = timezone(timedelta(hours=8))
DNA = "#龍芯⚡️丙午·丙申·己未·未时·䷋否-WORKSPACE-SYNC-v1.0"
CREATOR = "诸葛鑫（UID9622·龍芯北辰）"

ROOT = Path(__file__).resolve().parent.parent
HOME = Path.home()

# ─── Notion 目标镜像库（8/31 建库）───
NOTION_MIRROR_DB = "3cd7125a-9c9f-8131-98ee-c033afa8f63d"
NOTION_TOKEN_KEY = "NOTION_TOKEN"

# ─── 本地同步状态 ───
STATE_DIR = HOME / ".longhun"
STATE_FILE = STATE_DIR / "workspace_sync_state.json"

# ─── 扫描范围：核心层白名单（只整理这些，节能）───
CORE_PATTERNS = [
    "STATE.md", "AGENTS.md", "CONSTITUTION.md", "P0_ETERNAL_LOCK.md",
    "功能清单.md", "MASTER_REGISTRY.md", "CNSH-PROTOCOL.md", "ATTRIBUTION.md",
    ".codebuddy/COMMAND_INDEX.md", ".codebuddy/memory/MEMORY.md",
    "01_protocols/*.md", "12_DOCS/*.md", "02_SKILLS/*.md",
]

# 推送到 Notion 的精选上限（防滥建页面）
PUSH_MAX = 60
# 精选规则：根级关键文件永远推；其余按"近 N 天修改"优先
RECENT_DAYS = 30

SKIP_DIRS = {".git", "__pycache__", ".venv", "venv", "node_modules", "dist",
             "build", "models", "weights", "backups", "backup", "archive",
             "_work", "_QUARANTINE", "11_DATA", "logs", "audit", "龙魂成片",
             "videos", "voices", "training", "test_logs", "test_reports",
             ".codebuddy/teams", ".codebuddy/memory/archive"}


def _now() -> str:
    return datetime.now(CST).isoformat(timespec="seconds")


def _log(msg: str, level: str = "INFO"):
    markers = {"INFO": "📋", "OK": "✅", "WARN": "🟡", "ERROR": "🔴", "STEP": "⚙️"}
    print(f"[{datetime.now(CST).strftime('%H:%M:%S')}] {markers.get(level, 'ℹ️')} {msg}")


def _make_dna(op: str) -> str:
    ts = datetime.now().strftime("%Y-%m-%d-%H%M%S")
    raw = f"{op}-{ts}-{os.urandom(4).hex()}"
    h = hashlib.sha256(raw.encode()).hexdigest()[:8].upper()
    return f"#龍芯⚡️{ts}-WORKSPACE-{op}-{h}"


def _clean_env() -> Dict[str, str]:
    env = dict(os.environ)
    for k in ("HTTP_PROXY", "HTTPS_PROXY", "http_proxy", "https_proxy",
              "ALL_PROXY", "all_proxy"):
        env.pop(k, None)
    env["NO_PROXY"] = "*"
    env["no_proxy"] = "*"
    return env


def get_notion_token() -> str:
    """优先 vault（真相源），其次环境变量"""
    tok = ""
    try:
        r = subprocess.run(
            ["python3", str(ROOT / "bin" / "lh_vault.py"), "get", "NOTION_TOKEN"],
            capture_output=True, text=True, timeout=30, env=_clean_env())
        tok = r.stdout.strip() if r.returncode == 0 else ""
    except Exception:
        tok = ""
    if not tok:
        _log("NOTION_TOKEN 获取失败（vault + 环境变量均无）", "ERROR")
        sys.exit(1)
    return tok


def notion_api(method: str, path: str, payload: Dict | None = None,
               token: str | None = None) -> Dict:
    """调 Notion REST API（curl 子进程，规避代理坑）"""
    token = token or get_notion_token()
    cmd = ["curl", "-s", "-m", "60", "-X", method,
           f"https://api.notion.com{path}",
           "-H", f"Authorization: Bearer {token}",
           "-H", "Notion-Version: 2022-06-28",
           "-H", "Content-Type: application/json"]
    if payload is not None:
        cmd += ["-d", json.dumps(payload, ensure_ascii=False)]
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=90,
                           env=_clean_env())
        if not r.stdout.strip():
            return {"object": "error", "message": r.stderr[:200]}
        return json.loads(r.stdout)
    except Exception as e:
        return {"object": "error", "message": str(e)}


# ═══════════════════════════════════════════
# 1️⃣ 整理：扫描本地核心层 → 工作间清单
# ═══════════════════════════════════════════
def scan_workspace() -> Dict[str, Any]:
    """扫描白名单核心层，生成内容清单"""
    _log("扫描工作间核心层 ...", "STEP")
    items: List[Dict[str, Any]] = []

    def should_skip(p: Path) -> bool:
        return any(part in SKIP_DIRS for part in p.parts)

    def walk(dir_path: Path, depth: int = 0) -> None:
        if depth > 4 or not dir_path.is_dir():
            return
        try:
            entries = sorted(dir_path.iterdir())
        except PermissionError:
            return
        for e in entries:
            if e.name.startswith(".") or should_skip(e):
                continue
            if e.is_dir():
                walk(e, depth + 1)
            elif e.is_file() and e.suffix in (".md", ".py", ".sh", ".json"):
                try:
                    st = e.stat()
                    rel = e.relative_to(ROOT)
                    if str(rel) == "STATE.md" or any(
                        rel.match(pat) for pat in CORE_PATTERNS
                    ):
                        items.append({
                            "name": e.name,
                            "path": str(rel),
                            "size": st.st_size,
                            "mtime": datetime.fromtimestamp(st.st_mtime, CST)
                                    .isoformat(timespec="seconds"),
                            "sha256": hashlib.sha256(
                                e.read_bytes()[:64 * 1024]
                            ).hexdigest()[:16],
                        })
                except (OSError, UnicodeDecodeError):
                    pass

    # 只走有限个核心目录
    for sub in ["01_protocols", "12_DOCS", "02_SKILLS", ".codebuddy/memory"]:
        p = ROOT / sub
        if p.exists():
            walk(p)
    # 根级关键文件
    for f in ["STATE.md", "AGENTS.md", "CONSTITUTION.md", "功能清单.md",
              "P0_ETERNAL_LOCK.md", ".codebuddy/COMMAND_INDEX.md"]:
        p = ROOT / f
        if p.exists():
            try:
                st = p.stat()
                items.append({
                    "name": p.name,
                    "path": f,
                    "size": st.st_size,
                    "mtime": datetime.fromtimestamp(st.st_mtime, CST)
                            .isoformat(timespec="seconds"),
                    "sha256": hashlib.sha256(
                        p.read_bytes()[:64 * 1024]).hexdigest()[:16],
                })
            except OSError:
                pass

    items.sort(key=lambda x: (x["path"],))
    total_size = sum(i["size"] for i in items)
    manifest = {
        "dna": DNA,
        "creator": CREATOR,
        "generated_at": _now(),
        "root": str(ROOT),
        "count": len(items),
        "total_size": total_size,
        "items": items,
    }
    out_json = ROOT / "12_DOCS" / "workspace_inventory.json"
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(manifest, ensure_ascii=False, indent=2),
                        encoding="utf-8")
    _log(f"清单已生成: {out_json}（{len(items)} 项 / {total_size/1024:.0f} KB）", "OK")
    return manifest


# ═══════════════════════════════════════════
# 2️⃣ 推送 → Notion 镜像库
# ═══════════════════════════════════════════
def _load_prev_state() -> Dict[str, str]:
    if STATE_FILE.exists():
        try:
            return json.loads(STATE_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {}


def _save_state(synced: Dict[str, str]) -> None:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(synced, ensure_ascii=False, indent=2),
                          encoding="utf-8")


def _select_curated(items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """精选：根级关键文件 + 近 RECENT_DAYS 天修改的，上限 PUSH_MAX"""
    root_key = {
        "STATE.md", "AGENTS.md", "CONSTITUTION.md", "P0_ETERNAL_LOCK.md",
        "功能清单.md", ".codebuddy/COMMAND_INDEX.md",
        ".codebuddy/memory/MEMORY.md",
    }
    now = datetime.now(CST)
    always = [i for i in items if i["path"] in root_key]
    rest = [i for i in items if i["path"] not in root_key]
    rest.sort(key=lambda x: x["mtime"], reverse=True)
    recent = []
    for i in rest:
        try:
            mt = datetime.fromisoformat(i["mtime"])
            if (now - mt).days <= RECENT_DAYS:
                recent.append(i)
        except Exception:
            continue
    curated = always + recent
    if len(curated) > PUSH_MAX:
        curated = curated[:PUSH_MAX]
    curated.sort(key=lambda x: x["path"])
    return curated


def push_overview(manifest: Dict[str, Any]) -> None:
    """建/更新总览页：把全量清单以列表形式写入一个页面"""
    _log("同步总览页（全量清单索引）...", "INFO")
    token = get_notion_token()
    title = f"🗂️ 龍魂·工作间内容总览｜{manifest['generated_at'][:10]}｜{manifest['count']}项"

    # 找已有总览页：优先本地状态，其次 search
    overview_page = _load_prev_state().get("_overview_page")
    if not overview_page:
        try:
            r = notion_api("POST", "/v1/search",
                           {"query": "龍魂·工作间内容总览", "page_size": 5}, token)
            for p in r.get("results", []):
                if p.get("object") == "page" and "工作间内容总览" in json.dumps(
                        p.get("properties", {}), ensure_ascii=False):
                    overview_page = p["id"]
                    break
        except Exception:
            pass

    # 总览页只放统计 + 目录级分组（具体文件在镜像库查，避免巨型页面）
    list_blocks: List[Dict[str, Any]] = [
        {"object": "block", "type": "paragraph",
         "paragraph": {"rich_text": [{"type": "text",
            "text": {"content": f"📊 共 {manifest['count']} 项 / 总大小 "
                                f"{manifest['total_size']/1024:.0f} KB / 生成于 "
                                f"{manifest['generated_at']}"}}]}},
        {"object": "block", "type": "paragraph",
         "paragraph": {"rich_text": [{"type": "text",
            "text": {"content": "👉 具体文件明细请查「🐉 龍魂·工作间镜像库 v1.0」"}}]}},
    ]
    groups: Dict[str, List[Dict[str, Any]]] = {}
    for i in manifest["items"]:
        d = i["path"].split("/")[0] if "/" in i["path"] else "(根目录)"
        groups.setdefault(d, []).append(i)
    for d in sorted(groups.keys()):
        grp = groups[d]
        list_blocks.append({"object": "block", "type": "bulleted_list_item",
                            "bulleted_list_item": {"rich_text": [{"type": "text",
                            "text": {"content": f"📁 {d}｜{len(grp)} 项"}}]}})

    def _clear_blocks(page_id: str) -> None:
        """清空页面所有子 block（更新前防重复）"""
        while True:
            r = notion_api("GET", f"/v1/blocks/{page_id}/children?page_size=100",
                           None, token)
            children = r.get("results", [])
            if not children:
                break
            for c in children:
                notion_api("DELETE", f"/v1/blocks/{c['id']}", None, token)
            time.sleep(0.3)

    def _append_batches(page_id: str) -> bool:
        """分批 append blocks（每批 ≤90）"""
        ok = True
        for i in range(0, len(list_blocks), 90):
            batch = list_blocks[i:i + 90]
            r = notion_api("PATCH",
                           f"/v1/blocks/{page_id}/children",
                           {"children": batch}, token)
            if r.get("object") != "list":
                _log(f"追加 block 失败: {r.get('message', r)}", "WARN")
                ok = False
            time.sleep(0.5)
        return ok

    if overview_page:
        r = notion_api("PATCH", f"/v1/pages/{overview_page}",
                       {"properties": {"title": {
                           "title": [{"type": "text", "text": {"content": title}}]}}},
                       token)
        _clear_blocks(overview_page)
        _append_batches(overview_page)
        _log("总览页已更新", "OK")
    else:
        # 创建时只放前 90 个 block，其余 append
        r = notion_api("POST", "/v1/pages",
                       {"parent": {"page_id": "2d87125a-9c9f-8028-89e2-e18002f7cf4f"},
                        "properties": {"title": {"title": [{"type": "text",
                            "text": {"content": title}}]}},
                        "children": list_blocks[:90]}, token)
        overview_page = r.get("id")
        if overview_page:
            if len(list_blocks) > 90:
                _append_batches(overview_page)
            _log("总览页已创建", "OK")
        else:
            _log(f"总览页创建失败: {r.get('message', r)}", "ERROR")
    return overview_page


def push_to_notion(manifest: Dict[str, Any]) -> None:
    """增量推送精选变更文件 → Notion 镜像库"""
    curated = _select_curated(manifest["items"])
    _log(f"推送精选文件（{len(curated)}/{len(manifest['items'])} 项）→ Notion 镜像库",
         "STEP")
    token = get_notion_token()

    # 读上一次已同步指纹
    prev = _load_prev_state()
    synced = dict(prev)

    # 查库里现有条目（标题→page_id），避免重复建
    existing: Dict[str, str] = {}
    cursor = None
    while True:
        payload: Dict[str, Any] = {"page_size": 100}
        if cursor:
            payload["start_cursor"] = cursor
        r = notion_api("POST", f"/v1/databases/{NOTION_MIRROR_DB}/query",
                       payload, token)
        if r.get("object") != "list":
            _log(f"查询失败: {r.get('message', r)}", "ERROR")
            break
        for p in r.get("results", []):
            title = ""
            try:
                t = p["properties"]["文件名"]["title"]
                title = t[0]["plain_text"] if t else ""
            except (KeyError, IndexError):
                pass
            if title:
                existing[title] = p["id"]
        cursor = r.get("next_cursor")
        if not cursor:
            break

    _log(f"库内现有条目 {len(existing)} 条", "INFO")

    # 总览页：全量清单索引（每轮更新）
    try:
        op_id = push_overview(manifest)
        if op_id:
            synced["_overview_page"] = op_id
    except Exception as e:
        _log(f"总览页更新失败: {e}", "WARN")

    created = updated = skipped = 0
    for item in curated:
        title = f"{item['name']}｜{item['path']}"
        if title in existing:
            page_id = existing[title]
        else:
            page_id = None

        if page_id:
            # 已存在：内容变化才更新
            if prev.get(title) == item["sha256"]:
                skipped += 1
                continue
            props = {
                "更新时间": {"date": {"start": item["mtime"][:10]}},
                "同步状态": {"select": {"name": "synced"}},
                "三色": {"select": {"name": "🟢"}},
                "DNA": {"rich_text": [{"text": {"content": _make_dna("UPDATE")}}]},
            }
            r = notion_api("PATCH", f"/v1/pages/{page_id}",
                           {"properties": props}, token)
            if r.get("object") == "page":
                updated += 1
                synced[title] = item["sha256"]
        else:
            # 新建（title 统一用「文件名｜路径」格式，与查找 key 一致）
            props = {
                "文件名": {"title": [{"text": {"content": title}}]},
                "本地路径": {"rich_text": [{"text": {"content": item["path"]}}]},
                "文件大小": {"number": item["size"]},
                "更新时间": {"date": {"start": item["mtime"][:10]}},
                "同步状态": {"select": {"name": "synced"}},
                "三色": {"select": {"name": "🟢"}},
                "DNA": {"rich_text": [{"text": {"content": _make_dna("CREATE")}}]},
                "备注": {"rich_text": [{"text": {"content": "由工作间同步引擎自动入库"}}]},
            }
            r = notion_api("POST", "/v1/pages",
                           {"parent": {"database_id": NOTION_MIRROR_DB},
                            "properties": props}, token)
            if r.get("object") == "page":
                created += 1
                synced[title] = item["sha256"]

        # 防限流：每 5 条休息 1 秒
        if (created + updated) % 5 == 0 and (created + updated) > 0:
            time.sleep(1)

    _save_state(synced)
    _log(f"Notion 同步完成: 新建 {created} / 更新 {updated} / 跳过 {skipped}",
         "OK")


# ═══════════════════════════════════════════
# 3️⃣ 联动 → 鲲鹏服务器
# ═══════════════════════════════════════════
def _ssh_base(host: str = "119.13.90.27", port: int = 22,
              key: str = "~/.ssh/longhun_kunpeng_ed25519") -> List[str]:
    return ["ssh", "-p", str(port), "-i", os.path.expanduser(key),
            "-o", "StrictHostKeyChecking=accept-new", "-o", "ConnectTimeout=15",
            f"root@{host}"]


def _rsync_remote() -> List[str]:
    return ["rsync", "-az", "--delete",
            "-e", "ssh -i ~/.ssh/longhun_kunpeng_ed25519 -o StrictHostKeyChecking=accept-new"]


def push_to_kunpeng() -> None:
    """轻量重点同步（核心目录）→ 鲲鹏 + 协作中枢（sync-collab.sh push）"""
    _log("同步到鲲鹏服务器 ...", "STEP")

    # 3.1 文档层轻量 rsync（核心价值层；代码层 08_BIN 7.6G 走 sync-to-kunpeng.sh 全量）
    core_dirs = ["01_protocols", "12_DOCS", "02_SKILLS", "deploy/scripts",
                 ".codebuddy/memory"]
    remote_root = "/opt/longhun-system"
    excludes = ["--exclude=.git", "--exclude=__pycache__", "--exclude=*.asc",
                "--exclude=*.db", "--exclude=*.sqlite*", "--exclude=*.log",
                "--exclude=*.pyc", "--exclude=*.wav", "--exclude=*.mp4",
                "--exclude=*.png", "--exclude=*.jpg", "--exclude=*.jpeg",
                "--exclude=*.otf", "--exclude=*.woff*", "--exclude=*.zip"]
    ok = True
    for d in core_dirs:
        src = ROOT / d
        if not src.exists():
            continue
        cmd = _rsync_remote() + excludes + [str(src) + "/",
              f"root@119.13.90.27:{remote_root}/{d}/"]
        _log(f"rsync {d} ...", "INFO")
        try:
            r = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
            if r.returncode != 0:
                _log(f"rsync {d} 异常: {r.stderr[-200:]}", "WARN")
                ok = False
        except subprocess.TimeoutExpired:
            _log(f"rsync {d} 超时（跳过）", "WARN")
            ok = False
    if ok:
        _log("鲲鹏核心目录同步 ✅", "OK")
    else:
        _log("鲲鹏同步部分失败（见上方 🟡）", "WARN")

    # 3.2 工作间清单/索引也推一份
    for f in ["STATE.md", "12_DOCS/workspace_inventory.json"]:
        p = ROOT / f
        if p.exists():
            try:
                subprocess.run(
                    _ssh_base() + [f"mkdir -p {remote_root}/{p.parent.name}"],
                    capture_output=True, text=True, timeout=30)
                subprocess.run(["scp", "-i", "~/.ssh/longhun_kunpeng_ed25519",
                                "-o", "StrictHostKeyChecking=accept-new",
                                str(p), f"root@119.13.90.27:{remote_root}/{f}"],
                               capture_output=True, text=True, timeout=120)
            except Exception:
                pass

    # 3.3 协作中枢（collab + handoffs）
    script2 = ROOT / "deploy" / "sync-collab.sh"
    if script2.exists():
        _log("执行协作中枢同步（collab push）...", "INFO")
        r = subprocess.run(["bash", str(script2), "push"],
                           capture_output=True, text=True, timeout=300)
        if r.returncode == 0:
            _log("协作中枢同步 ✅", "OK")
        else:
            _log(f"协作中枢同步异常: {r.stderr[-300:]}", "WARN")
    else:
        _log("缺少 deploy/sync-collab.sh，跳过协作中枢", "WARN")


# ═══════════════════════════════════════════
# 主流程
# ═══════════════════════════════════════════
def main() -> int:
    ap = argparse.ArgumentParser(description="龍魂·工作间三端同步引擎 v1.0")
    ap.add_argument("--scan", action="store_true", help="整理：扫描生成工作间清单")
    ap.add_argument("--to-notion", action="store_true", help="推送：清单+变更→Notion 镜像库")
    ap.add_argument("--to-kunpeng", action="store_true", help="联动：同步到鲲鹏服务器")
    ap.add_argument("--all", action="store_true", help="一键三端全跑")
    args = ap.parse_args()

    t0 = time.time()

    if args.all:
        args.scan = args.to_notion = args.to_kunpeng = True
    if not (args.scan or args.to_notion or args.to_kunpeng):
        ap.print_help()
        return 0

    manifest: Dict[str, Any] = {"items": []}
    if args.scan:
        manifest = scan_workspace()
    if args.to_notion:
        if not manifest.get("items"):
            manifest = scan_workspace()
        push_to_notion(manifest)
    if args.to_kunpeng:
        push_to_kunpeng()

    _log(f"🏁 全部完成，耗时 {time.time()-t0:.1f}s | DNA: {DNA}", "OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
