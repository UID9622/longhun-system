#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂·贡献者铭碑引擎 v1.0 — Merkle 铭碑·贡献者被牢记·永不吞没
================================================================
DNA:    #龍芯⚡️20260902-CONTRIBUTOR-MEMORIAL-v1.0-9622
创建者: 诸葛鑫（UID9622）
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
GPG:    A2D0092CEE2E5BA87035600924C3704A8CC26D5F
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
协议:    CC BY-NC-SA 4.0（核心思想层）

功能:
  --build   扫描 git 贡献者 → Merkle 铭碑(JSON+MD) → 根哈希存档
  --verify  重算根哈希 比对存档 → 铭碑是否被篡改
  --show    展示铭碑(作者/提交数/占比/节点哈希)
  --add     追加非 git 贡献者(文档/测试/资金支持·name:email:note)
  --root    只输出当前 Merkle 根(供发布/校验)

设计原则（M77 零中间层·P0）:
  - 纯标准库·零三方依赖·单文件可跑
  - 每个贡献者 = Merkle 叶节点(哈希不可逆)
  - 根哈希公开存档 → 谁想吞没贡献者 = 根对不上 = 铁证
  - 与耻辱墙联动: 铭碑只认 git 提交+人工登记·天然防造假
"""

import argparse
import hashlib
import json
import os
import subprocess
import sys
from datetime import datetime, timezone

UID = "9622"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # longhun-system/
AUDIT_DIR = os.path.join(ROOT, "07_AUDIT")
MEMORIAL_JSON = os.path.join(AUDIT_DIR, "contributor_memorial.json")
MEMORIAL_MD = os.path.join(AUDIT_DIR, "contributor_memorial.md")
MANUAL_FILE = os.path.join(AUDIT_DIR, "memorial_manual_contributors.json")
ALIAS_FILE = os.path.join(AUDIT_DIR, "memorial_aliases.json")

HEADER = {
    "dna": "#龍芯⚡️20260902-CONTRIBUTOR-MEMORIAL-v1.0-9622",
    "creator": "诸葛鑫（UID9622）",
    "attribution": "诸葛鑫 | UID9622 · 龍芯北辰",
    "gpg": "A2D0092CEE2E5BA87035600924C3704A8CC26D5F",
    "license": "MulanPSL v2",
}


def _h(data: str) -> str:
    """SHA-256 哈希（不可逆·作 Merkle 节点）"""
    return hashlib.sha256(data.encode("utf-8")).hexdigest()


def _run_git(args: list) -> str:
    try:
        p = subprocess.run(
            ["git", "-C", ROOT] + args,
            capture_output=True, text=True, timeout=120,
        )
        return p.stdout
    except Exception:
        return ""


def scan_git_contributors():
    """扫描 git log → {email: {name, commits, first_ts, last_ts}}"""
    out = _run_git(["log", "--format=%an|%ae|%at"])
    stats = {}
    for line in out.splitlines():
        parts = line.split("|")
        if len(parts) < 3:
            continue
        name, email, ts = parts[0], parts[1].strip(), parts[2]
        if not email:
            continue
        email = email.lower()
        ts_int = int(ts) if ts.isdigit() else 0
        s = stats.setdefault(email, {"name": name, "commits": 0, "first": ts_int, "last": ts_int})
        s["commits"] += 1
        s["first"] = min(s["first"], ts_int) if s["first"] else ts_int
        s["last"] = max(s["last"], ts_int)
        if name:
            s["name"] = name
    return stats


def load_manual_contributors():
    """加载人工登记的非 git 贡献者"""
    if not os.path.exists(MANUAL_FILE):
        return []
    try:
        with open(MANUAL_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, list) else []
    except Exception:
        return []


def load_aliases():
    """加载别名合并表: [{"canonical_email", "canonical_name", "aliases": [...]}]"""
    if not os.path.exists(ALIAS_FILE):
        return []
    try:
        with open(ALIAS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, list) else []
    except Exception:
        return []


def merge_aliases(stats: dict) -> dict:
    """按别名表把同人多邮箱归并到规范邮箱（实名归一）"""
    aliases = load_aliases()
    if not aliases:
        return stats
    alias_map = {}  # alias_email.lower -> canonical_email
    canonical_meta = {}  # canonical_email -> {"name":..., "aliases":[...]}
    for m in aliases:
        ce = m.get("canonical_email", "").lower()
        if not ce:
            continue
        canonical_meta[ce] = {"name": m.get("canonical_name", m.get("canonical_email", ce)),
                              "aliases": m.get("aliases", [])}
        for a in m.get("aliases", []):
            alias_map[a.strip().lower()] = ce

    merged = {}
    for email, s in stats.items():
        target = alias_map.get(email, email)
        if target not in merged:
            merged[target] = dict(s)
            merged[target]["name"] = canonical_meta.get(target, {}).get("name", s["name"])
        else:
            t = merged[target]
            t["commits"] += s["commits"]
            t["first"] = min(t["first"], s["first"]) if (t["first"] and s["first"]) else (t["first"] or s["first"])
            t["last"] = max(t["last"], s["last"])
            if s["name"] and canonical_meta.get(target, {}).get("name") in (None, "", target):
                t["name"] = canonical_meta[target]["name"] if target in canonical_meta else s["name"]
    return merged


def add_alias(canonical_email: str, canonical_name: str, aliases: str):
    """追加/更新别名合并规则"""
    os.makedirs(AUDIT_DIR, exist_ok=True)
    data = load_aliases()
    alist = [a.strip() for a in aliases.split(",") if a.strip()]
    entry = {"canonical_email": canonical_email.lower(),
             "canonical_name": canonical_name,
             "aliases": alist}
    data = [e for e in data if e.get("canonical_email") != canonical_email.lower()]
    data.append(entry)
    with open(ALIAS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return f"✅ 别名合并规则已存: {canonical_name} <{canonical_email}> ← {alist}"


def build_merkle(leaves: list):
    """构建 Merkle 树 → (树, 根哈希)"""
    if not leaves:
        return {}, "0" * 64
    tree = {"leaves": dict(leaves)}
    level = [h for _, h in leaves]
    depth = 0
    while len(level) > 1:
        depth += 1
        nxt = []
        for i in range(0, len(level), 2):
            left = level[i]
            right = level[i + 1] if i + 1 < len(level) else left  # 奇数向上复制
            nxt.append(_h(left + right))
        tree[f"level_{depth}"] = nxt
        level = nxt
    tree["root"] = level[0]
    tree["depth"] = depth
    return tree, level[0]


def build_memorial():
    """扫描+构建+存档铭碑"""
    os.makedirs(AUDIT_DIR, exist_ok=True)
    git_stats = merge_aliases(scan_git_contributors())
    manual = load_manual_contributors()

    leaves = []          # (key, hash) → Merkle
    entries = []         # 详情列表
    for email, s in sorted(git_stats.items(), key=lambda x: -x[1]["commits"]):
        first_dt = datetime.fromtimestamp(s["first"], tz=timezone.utc).isoformat() if s["first"] else ""
        last_dt = datetime.fromtimestamp(s["last"], tz=timezone.utc).isoformat() if s["last"] else ""
        leaf_data = f"{s['name']}|{email}|{s['commits']}|{first_dt}|{last_dt}"
        leaf_hash = _h(leaf_data)
        leaves.append((email, leaf_hash))
        entries.append({
            "name": s["name"], "email": email, "source": "git",
            "commits": s["commits"], "first": first_dt, "last": last_dt,
            "node_hash": leaf_hash,
        })

    for m in manual:
        name = m.get("name", "?")
        email = m.get("email", "").lower() or f"manual:{len(entries)}"
        note = m.get("note", "")
        leaf_data = f"{name}|{email}|manual|{note}"
        leaf_hash = _h(leaf_data)
        if email not in [e for e, _ in leaves]:
            leaves.append((email, leaf_hash))
            entries.append({
                "name": name, "email": email, "source": "manual",
                "commits": 0, "first": "", "last": "", "note": note,
                "node_hash": leaf_hash,
            })

    total_commits = sum(s["commits"] for s in git_stats.values())
    for e in entries:
        e["share_pct"] = round(e["commits"] / total_commits * 100, 2) if total_commits else 0.0

    tree, root = build_merkle(leaves)
    memorial = {
        "header": HEADER,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "merkle_root": root,
        "contributor_count": len(entries),
        "total_commits": total_commits,
        "tree": tree,
        "contributors": entries,
    }

    with open(MEMORIAL_JSON, "w", encoding="utf-8") as f:
        json.dump(memorial, f, ensure_ascii=False, indent=2)
    _write_md(memorial)
    return memorial, root


def _write_md(memorial: dict):
    """生成人类可读铭碑 MD"""
    lines = [
        f"<!-- {memorial['header']['dna']} -->",
        "",
        "# 🏛 龍魂·贡献者铭碑",
        "",
        f"> 铭碑根哈希: `{memorial['merkle_root']}`",
        f"> 生成时间: {memorial['generated_at']}",
        f"> 贡献者 {memorial['contributor_count']} 人 · 总提交 {memorial['total_commits']} 次",
        "",
        "> **每一位实质性贡献者的足迹都会被铭刻。哪怕只有一个人，也要写下来。**",
        "> 铭碑不可篡改：任何人可运行 `python3 08_BIN/lh_memorial.py --verify` 校验。",
        "",
        "| # | 贡献者 | 来源 | 提交数 | 占比 | 节点哈希 |",
        "|:---:|:---|:---:|:---:|:---:|:---|",
    ]
    for i, c in enumerate(memorial["contributors"], 1):
        src = "git" if c["source"] == "git" else "登记"
        lines.append(
            f"| {i} | {c['name']} | {src} | {c['commits']} | {c['share_pct']}% | `{c['node_hash'][:12]}…` |"
        )
    lines += [
        "",
        "---",
        "**验证方法**: `python3 08_BIN/lh_memorial.py --verify`",
        "",
        f"**DNA**: {memorial['header']['dna']}",
        f"**归属名**: {memorial['header']['attribution']}",
        "**协议**: CC BY-NC-SA 4.0（核心思想层）· MulanPSL v2（工程层）",
    ]
    with open(MEMORIAL_MD, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def verify_memorial():
    """重算根哈希 vs 存档 → 篡改检测"""
    if not os.path.exists(MEMORIAL_JSON):
        return False, "铭碑不存在，先运行 --build"
    with open(MEMORIAL_JSON, "r", encoding="utf-8") as f:
        saved = json.load(f)
    _, root_now = build_memorial()
    ok = root_now == saved.get("merkle_root")
    msg = (f"根哈希一致 🟢 铭碑未被篡改 · 根={root_now[:16]}…"
           if ok else
           f"根哈希不一致 🔴 铭碑被篡改！存档={saved.get('merkle_root', '?')[:16]}… 实算={root_now[:16]}…")
    return ok, msg


def show_memorial():
    """展示铭碑"""
    if not os.path.exists(MEMORIAL_JSON):
        return "铭碑不存在，先运行 --build"
    with open(MEMORIAL_JSON, "r", encoding="utf-8") as f:
        m = json.load(f)
    lines = [f"🏛 贡献者铭碑 · 根哈希 `{m['merkle_root'][:16]}…`",
             f"   共 {m['contributor_count']} 人 · {m['total_commits']} 次提交"]
    for c in m["contributors"][:20]:
        lines.append(f"   {c['name']:<16} {c['commits']:>5} 次 {c['share_pct']:>6}%  `{c['node_hash'][:12]}…`")
    if len(m["contributors"]) > 20:
        lines.append(f"   … 其余 {len(m['contributors']) - 20} 人")
    return "\n".join(lines)


def add_manual(name: str, email: str, note: str):
    """追加人工登记贡献者"""
    os.makedirs(AUDIT_DIR, exist_ok=True)
    data = load_manual_contributors()
    data.append({"name": name, "email": email, "note": note})
    with open(MANUAL_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return f"✅ 已登记贡献者: {name} <{email}>"


def main():
    ap = argparse.ArgumentParser(description="🐉 龍魂·贡献者铭碑引擎 v1.0")
    ap.add_argument("--build", action="store_true", help="扫描+构建+存档铭碑")
    ap.add_argument("--verify", action="store_true", help="校验铭碑是否被篡改")
    ap.add_argument("--show", action="store_true", help="展示铭碑")
    ap.add_argument("--root", action="store_true", help="只输出 Merkle 根")
    ap.add_argument("--add", metavar="NAME:EMAIL[:NOTE]", help="追加非 git 贡献者")
    ap.add_argument("--merge", metavar="CANON_EMAIL:CANON_NAME:ALIAS1,ALIAS2",
                    help="合并同人多邮箱到规范实名")
    args = ap.parse_args()

    if args.merge:
        parts = args.merge.split(":", 2)
        ce = parts[0].strip()
        cn = parts[1].strip() if len(parts) > 1 else ce
        als = parts[2].strip() if len(parts) > 2 else ""
        if not ce or not als:
            print("🔴 格式: --merge 规范邮箱:显示名:别名1,别名2")
            return 1
        print(add_alias(ce, cn, als))
        return 0

    if args.add:
        parts = args.add.split(":", 2)
        name = parts[0].strip()
        email = parts[1].strip() if len(parts) > 1 else ""
        note = parts[2].strip() if len(parts) > 2 else ""
        if not name:
            print("🔴 名字不能为空")
            return 1
        print(add_manual(name, email, note))
        return 0

    if args.verify:
        ok, msg = verify_memorial()
        print(msg)
        return 0 if ok else 2

    if args.root:
        _, root = build_memorial()
        print(root)
        return 0

    if args.show:
        print(show_memorial())
        return 0

    m, root = build_memorial()
    print(f"🏛 贡献者铭碑已建成 · 根哈希 `{root[:16]}…`")
    print(f"   贡献者 {m['contributor_count']} 人 · 总提交 {m['total_commits']} 次")
    print(f"   存档: {MEMORIAL_JSON}")
    print(f"   阅读: {MEMORIAL_MD}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
