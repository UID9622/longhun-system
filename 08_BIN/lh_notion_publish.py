#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 🐉 龍魂·Notion Publish 半自动工具 v1.0
# DNA: #龍芯⚡️2026-09-06-NOTION-PUBLISH-v1.0-UID9622
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# 协议: 工程实现层 MulanPSL v2 · 核心思想层 CC BY-NC-SA 4.0
#
# 物理事实: Notion API 无 publish 能力 → 浏览器 Share→Publish 为唯一人闸。
# 本工具做到「能自动的全自动」: 一键打开直达页(免手输URL) → 收公开链接 →
# 自动登记+校验 → 生成 iframe 看板页 → mkdocs 构建 → rsync 鲲鹏 → 线上验证。
# 纯 stdlib · 禁代理 · 幂等。

import argparse
import json
import os
import re
import subprocess
import sys
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

VERSION = "v1.0"
ENGINE_NAME = "lh_notion_publish.py"
HOME = Path.home()
STATE_FILE = HOME / ".longhun" / "notion_public.json"
LOG_FILE = HOME / ".longhun" / "notion_publish.log"
ROOT = Path(__file__).resolve().parent.parent  # longhun-system
DOCS_SITE = ROOT / "docs-site"
DOCS_DIR = DOCS_SITE / "docs"
LIVE_PAGE = "notion-live.md"
MKDOCS_YML = DOCS_SITE / "mkdocs.yml"
MKDOCS_BIN = HOME / "Library/Python/3.14/bin/mkdocs"
SSH_KEY = HOME / ".ssh" / "longhun_kunpeng_ed25519"
KUNPENG = "root@119.13.90.27:/opt/longhun-system/docs-site/"
PUBLIC_BASE = "https://uid9622.cn/docs/"

# ── 默认库注册表（key → 名称 / database_id / 打开 URL）──────────────
DEFAULT_DBS = {
    "snapshot": {"name": "🏥 龍魂健康快照", "db": "3d27125a-9c9f-814a-9d11-d96c60f07517"},
    "events":   {"name": "🧩 拓扑变更事件", "db": "3d27125a-9c9f-81d9-89fd-ed1a227162ac"},
    "report":   {"name": "📋 一周健康报告", "db": "3d27125a-9c9f-8142-aade-d72b258a13cf"},
    "memory":   {"name": "🧠 龍魂记忆外接大脑", "db": "3d27125a-9c9f-81c8-ab40-da544c652da9"},
    "task":     {"name": "🧭 龍魂任务池", "db": "3d27125a-9c9f-811e-b211-c301b7124586"},
}

STATE_KEYS = ["version", "dbs", "registered_at", "deployed_at"]


def log(msg: str) -> None:
    ts = datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")
    try:
        LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
        with LOG_FILE.open("a", encoding="utf-8") as f:
            f.write(f"[{ts}] {msg}\n")
    except Exception:
        pass


# ── 状态存取 ─────────────────────────────────────────────────────
def load_state() -> dict:
    st = {"version": VERSION, "dbs": {}, "registered_at": "", "deployed_at": ""}
    if STATE_FILE.exists():
        try:
            raw = json.loads(STATE_FILE.read_text(encoding="utf-8"))
            for k in ("version", "dbs", "registered_at", "deployed_at"):
                if k in raw:
                    st[k] = raw[k]
        except Exception as e:
            print(f"⚠️ 状态文件解析失败({e})→ 用默认重建")
    for key, meta in DEFAULT_DBS.items():
        st["dbs"].setdefault(key, {"name": meta["name"], "db": meta["db"],
                                   "public_url": "", "registered_at": "",
                                   "deployed": False})
    return st


def save_state(st: dict) -> None:
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(st, ensure_ascii=False, indent=2),
                          encoding="utf-8")


def open_url(page_url: str) -> str:
    """Notion 页直达 URL: https://www.notion.so/<dbid去横线>"""
    return f"https://www.notion.so/{page_url.replace('-', '')}"


# ── URL 可达性探测（curl 子进程 · 幂等）────────────────────────────
# ⚠️ 两个物理坑(实测焊点):
#   1. Notion 公开页拒 HEAD/非浏览器 UA → 须 GET+浏览器 UA
#   2. 本机 socks5h://127.0.0.1:1080 代理 · urllib 不认 socks5h → 直连被断
#      (Remote end closed) · curl/libcurl 原生支持 socks5h → 用 curl 探测
def _probe(url: str, timeout: int = 10) -> tuple[int, str]:
    """返回 (http_code, url) · 失败返回 (0, err)"""
    try:
        r = subprocess.run(
            ["curl", "-s", "-o", "/dev/null", "-L", "--max-time", str(timeout),
             "-A", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                   "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36",
             "-w", "%{http_code}", url],
            capture_output=True, text=True)
        code = r.stdout.strip()
        return (int(code), url) if code.isdigit() else (0, f"curl: {r.stderr[:60]}")
    except Exception as e:
        return 0, str(e)[:80]


# ── 子命令实现 ────────────────────────────────────────────────────
def cmd_list(st: dict) -> int:
    print(f"🐉 Notion Publish 登记表 {VERSION} · 状态 {STATE_FILE}\n")
    print(f"{'key':<9} {'库':<20} {'database_id':<38} 公开链接/状态")
    print("-" * 120)
    for key, meta in st["dbs"].items():
        pub = meta.get("public_url", "")
        if pub:
            code, _ = _probe(pub)
            state = f"🟢 {code} {pub[:52]}" if code == 200 else f"🔴 {code} 需复查"
        else:
            state = "🟡 未发布 → 一键打开: " + open_url(meta["db"])
        print(f"{key:<9} {meta['name']:<20} {meta['db']:<38} {state}")
    print("\n💡 已登记且部署: lh notion-publish deploy 一键嵌 iframe → 文档站")
    return 0


def cmd_open(st: dict, key: str | None) -> int:
    dbs = st["dbs"]
    if key is None:
        print("请指定库 key，可选:")
        for k, m in dbs.items():
            print(f"  {k:<9} {m['name']}")
        return 0
    meta = dbs.get(key) or _find_by_name(dbs, key)
    if not meta:
        print(f"❌ 未找到库: {key}")
        return 1
    url = open_url(meta["db"])
    print(f"🔓 打开 {meta['name']} → {url}")
    subprocess.run(["open", url], check=False)
    print("👉 在打开的页面右上角点 Share → 若弹权限提示选「Publish to web」→\n"
          "   Allow anyone with the link to view → 复制公开链接")
    return 0


def cmd_check(st: dict, url: str | None, all_: bool) -> int:
    if url:
        code, final = _probe(url)
        print(f"{'🟢 200 可访问' if code == 200 else f'🔴 不可达 ({code})'} {url}")
        if code == 200 and final != url:
            print(f"  ↳ 跳转至: {final}")
        return 0 if code == 200 else 1
    if all_:
        bad = 0
        for key, meta in st["dbs"].items():
            pub = meta.get("public_url", "")
            if not pub:
                continue
            code, _ = _probe(pub)
            flag = "🟢" if code == 200 else "🔴"
            print(f"{flag} {key:<9} {code} {pub}")
            if code != 200:
                bad += 1
        return 1 if bad else 0
    print("用法: lh notion-publish check <公开链接> | --all")
    return 0


def cmd_link(st: dict, key: str, url: str, auto_deploy: bool) -> int:
    url = url.strip().rstrip("/")
    if not re.search(r"\.notion\.site/", url):
        print("❌ 公开链接应形如 https://<workspace>.notion.site/<标题>-<id>")
        return 1
    meta = st["dbs"].get(key)
    if not meta:
        # 通用库：按 key 现建登记（名=key 中文提示，db 未知留空）
        meta = {"name": key, "db": "", "public_url": "", "registered_at": "",
                "deployed": False}
        st["dbs"][key] = meta
    meta["public_url"] = url
    meta["registered_at"] = datetime.now(timezone.utc).astimezone().isoformat(
        timespec="seconds")
    st["registered_at"] = meta["registered_at"]
    save_state(st)
    code, _ = _probe(url)
    print(f"{'🟢 登记成功 · 可访问' if code == 200 else f'🟡 已登记但当前探测 {code}'} "
          f"{meta['name']} → {url}")
    log(f"link {key} -> {url} (probe {code})")
    if auto_deploy and code == 200:
        print("→ 自动部署中…")
        return cmd_deploy(st)
    print("→ 下一步: lh notion-publish deploy 生成 iframe 看板并上线")
    return 0


def cmd_reset(st: dict, key: str) -> int:
    if key not in st["dbs"]:
        print(f"❌ 未登记库: {key}")
        return 1
    st["dbs"][key] = {"name": st["dbs"][key]["name"], "db": st["dbs"][key]["db"],
                      "public_url": "", "registered_at": "", "deployed": False}
    save_state(st)
    print(f"🧹 已清除 {key} 的公开链接登记")
    return 0


# ── 生成 docs 页 + 部署 ───────────────────────────────────────────
def _find_by_name(dbs: dict, text: str) -> dict | None:
    for m in dbs.values():
        if text in m["name"] or m["name"] in text or text in m["db"]:
            return m
    return None


def _gen_live_md(st: dict) -> str:
    lines = []
    lines.append("---")
    lines.append("icon: material/notebook-heart-outline")
    lines.append("comments: true")
    lines.append("---")
    lines.append("")
    lines.append("# 📡 龍魂实时看板 · Notion 公开化")
    lines.append("")
    lines.append("> 归属名: 诸葛鑫 | UID9622 · 龍芯北辰 · 由 `lh notion-publish deploy` 自动刷新 · "
                 "勿手改本文件")
    lines.append("")
    published = 0
    for key, meta in st["dbs"].items():
        pub = meta.get("public_url", "")
        lines.append(f"## {meta['name']}")
        if pub:
            code, _ = _probe(pub)
            if code == 200:
                published += 1
                lines.append("")
                lines.append(f"<div class='notion-frame'><iframe src='{pub}' width='100%' "
                             f"height='760' frameborder='0' allowfullscreen "
                             f"loading='lazy'></iframe></div>")
            else:
                lines.append("")
                lines.append(f"> ⚠️ 已登记但探测 {code}，请复查链接是否仍公开。")
        else:
            lines.append("")
            lines.append(f"> 🟡 尚未 Publish to web · 点击打开 → "
                         f"[{meta['name']}]({open_url(meta['db'])}) · 右上角 Share → "
                         f"Publish to web → 复制链接 → `lh notion-publish link {key} <链接>`")
        lines.append("")
    lines.append("---")
    lines.append("")
    lines.append(f"🟢 已嵌入 {published}/{len(st['dbs'])} 库 · 刷新时间 "
                 f"{datetime.now(timezone.utc).astimezone().isoformat(timespec='seconds')}")
    lines.append("")
    lines.append("> 📮 问题反馈: [GitHub Issue](https://github.com/UID9622/longhun-system/issues/new) · "
                 "🛡️ 拓扑根哈希见 [/docs/topology/](topology/index.md)")
    return "\n".join(lines)


def _ensure_nav(page_rel: str) -> bool:
    """在 mkdocs.yml nav 插入页面项；幂等（已存在返回 True）。"""
    text = MKDOCS_YML.read_text(encoding="utf-8")
    if f"{page_rel}" in text:
        return True
    new_line = f"  - 📡 龍魂实时看板: {page_rel}"
    anchors = [f"topology/index.md", f"- 首页: index.md"]
    for a in anchors:
        m = re.search(rf"^(\s*)-[^\n]*{re.escape(a)}[^\n]*$", text, re.M)
        if m:
            line = m.group(0)
            text = text.replace(line, line + "\n" + new_line, 1)
            MKDOCS_YML.write_text(text, encoding="utf-8")
            log(f"nav 插入 {page_rel} 于 {a} 后")
            return True
    print("⚠️ 未找到 nav 锚点，请手动把 notion-live.md 加入 mkdocs.yml nav")
    return False


def _mkdocs_cmd() -> str:
    if MKDOCS_BIN.exists():
        return str(MKDOCS_BIN)
    return "mkdocs"


def cmd_deploy(st: dict, skip_build: bool = False) -> int:
    target = DOCS_DIR / LIVE_PAGE
    target.write_text(_gen_live_md(st), encoding="utf-8")
    print(f"✅ 页面已生成 {target}")

    if not skip_build:
        _ensure_nav(LIVE_PAGE)
        print("🔨 mkdocs build …")
        r = subprocess.run([_mkdocs_cmd(), "build", "-f", str(MKDOCS_YML)],
                           capture_output=True, text=True, timeout=300,
                           cwd=str(DOCS_SITE))
        if r.returncode != 0:
            print("❌ build 失败:\n" + r.stdout[-1500:] + r.stderr[-1500:])
            return 1
        print(f"✅ build ok (site/ 已生成)")

    if not SSH_KEY.exists():
        print("⚠️ 跳过 rsync：未找到 SSH 密钥")
        return 2
    print("🚀 rsync → 鲲鹏 …")
    r = subprocess.run(["rsync", "-az", "--delete", "-e",
                        f"ssh -i {SSH_KEY} -o StrictHostKeyChecking=no",
                        str(DOCS_SITE / "site") + "/", KUNPENG],
                       capture_output=True, text=True, timeout=300)
    if r.returncode != 0:
        print("❌ rsync 失败:\n" + r.stderr[-1000:])
        return 1
    print("✅ 已同步鲲鹏")

    code, _ = _probe(PUBLIC_BASE + LIVE_PAGE)
    flag = "🟢 线上 200" if code == 200 else f"⚠️ 探测 {code}"
    print(f"🔍 线上验证: {PUBLIC_BASE + LIVE_PAGE} → {flag}")
    if code == 200:
        st["deployed_at"] = datetime.now(timezone.utc).astimezone().isoformat(
            timespec="seconds")
        for m in st["dbs"].values():
            if m.get("public_url"):
                m["deployed"] = True
        save_state(st)
    return 0 if code == 200 else 1


def cmd_status(st: dict) -> int:
    pub = sum(1 for m in st["dbs"].values() if m.get("public_url"))
    dep = sum(1 for m in st["dbs"].values() if m.get("deployed"))
    print(f"📊 Notion Publish 进度 · {pub}/{len(st['dbs'])} 库已登记 · {dep} 已嵌入")
    for key, meta in st["dbs"].items():
        u = meta.get("public_url", "")
        mark = "🟢 线上" if u and meta.get("deployed") else ("🟡 已登记" if u else "⚪ 未发布")
        print(f"  {mark} {key:<9} {meta['name']}" + (f"  {u[:60]}" if u else ""))
    print("\n下一步速查:")
    print("  打开库页:      lh notion-publish open <key>")
    print("  登记链接:      lh notion-publish link <key> https://xxx.notion.site/…")
    print("  一键上线:      lh notion-publish deploy")
    print("  校验链接:      lh notion-publish check <url> | --all")
    return 0


# ── 入口 ──────────────────────────────────────────────────────────
def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="lh notion-publish",
                                description="🐉 Notion Publish 半自动工具 v1.0")
    sub = p.add_subparsers(dest="cmd")

    sub.add_parser("list", help="登记表总览")
    sub.add_parser("status", help="进度总览+下一步")
    o = sub.add_parser("open", help="一键打开库页(浏览器直达 Share/Publish)")
    o.add_argument("key", nargs="?", default=None)

    c = sub.add_parser("check", help="探测公开链接可达性")
    c.add_argument("url", nargs="?", default=None)
    c.add_argument("--all", action="store_true", dest="all_")

    l = sub.add_parser("link", help="登记公开链接")
    l.add_argument("key")
    l.add_argument("url")
    l.add_argument("--deploy", action="store_true", help="登记后自动部署")

    d = sub.add_parser("deploy", help="生成 iframe 看板页并上线鲲鹏")
    d.add_argument("--skip-build", action="store_true")

    r = sub.add_parser("reset", help="清除某库登记")
    r.add_argument("key")

    args = p.parse_args(argv)
    if not args.cmd:
        p.print_help()
        return 0

    st = load_state()
    if args.cmd == "list":
        return cmd_list(st)
    if args.cmd == "status":
        return cmd_status(st)
    if args.cmd == "open":
        return cmd_open(st, args.key)
    if args.cmd == "check":
        return cmd_check(st, args.url, args.all_)
    if args.cmd == "link":
        return cmd_link(st, args.key, args.url, args.deploy)
    if args.cmd == "deploy":
        return cmd_deploy(st, args.skip_build)
    if args.cmd == "reset":
        return cmd_reset(st, args.key)
    return 0


if __name__ == "__main__":
    sys.exit(main())
