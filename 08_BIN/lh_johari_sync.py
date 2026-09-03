#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 🐉 龍魂系统 · 乔哈里视窗 数据同步引擎 v1.0
# DNA: #龍芯⚡️2026-08-31-JOHARI-WINDOW-SYNC-v1.0-UID9622
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# 功能: 扫描真实系统 → 生成乔哈里四象限数据 johari_data.json
#       开放区=真实焊点(MEMORY.md §1) · 盲区=实时轻扫描 · 隐藏/未知=主权占位
# 用法: python3 08_BIN/lh_johari_sync.py [--out 10_PORTAL/johari_data.json]
# 原则: 按需触发·用完即沉默·不做全量扫描（节能协议 v1.1）

import json
import os
import re
import sys
import datetime

ROOT = os.path.expanduser("~/longhun-system")
OUT_DEFAULT = os.path.join(ROOT, "10_PORTAL", "johari_data.json")

CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
GPG = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
DNA = "#龍芯⚡️2026-08-31-JOHARI-WINDOW-SYNC-v1.0-UID9622"
NOW = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S+08:00")


# ────────────────────────── 开放区：真实焊点 ──────────────────────────
def load_open_zone():
    """从 MEMORY.md §1 身份焊死提取真实焊点（每条一行）"""
    items = []
    path = os.path.join(ROOT, ".codebuddy", "memory", "MEMORY.md")
    try:
        with open(path, encoding="utf-8") as f:
            content = f.read()
        section = re.search(r"## §1\. 身份焊死(.*?)(?=\n## )", content, re.S)
        if section:
            for line in section.group(1).splitlines():
                line = line.strip()
                m = re.match(r"- \*\*(.+?)\*\*.*?[:：]\s*(.+)", line)
                if m:
                    title = m.group(1).replace("**", "")
                    desc = m.group(2).strip()
                    if len(desc) > 60:
                        desc = desc[:60] + "…"
                    items.append({"title": title, "desc": desc, "tag": "焊点"})
        if not items:
            raise ValueError("empty")
    except Exception:
        items = [
            {"title": "人民币主权·自主可控", "desc": "API自给自足·自研优先·外部隔离·评估流水线", "tag": "铁律"},
            {"title": "P0焊死天条", "desc": "为人民服务·数据主权归用户·零黑箱·诚实不编造", "tag": "焊点"},
            {"title": "GPG数字主权", "desc": "私钥物理隔离·永不入云·全设备授权", "tag": "焊点"},
            {"title": "焊死修复律", "desc": "焊死≠不动·冲突可修·口误以真实意图为准·走修订流程", "tag": "焊点"},
        ]
    # 附加 P0 天条（不来自记忆文件，固定焊死）
    items.insert(0, {"title": "P0-ETERNAL 永恒锁", "desc": "龙魂系统根本大法·主权唯一 UID9622", "tag": "宪法"})
    return items


# ────────────────────────── 盲区：实时轻扫描 ──────────────────────────
def _recent_mtime(path):
    """目录内最新 mtime；不存在返回 None"""
    try:
        if not os.path.isdir(path):
            return None
        latest = 0
        for name in os.listdir(path):
            full = os.path.join(path, name)
            if os.path.isfile(full) or os.path.islink(full):
                try:
                    latest = max(latest, os.path.getmtime(full))
                except OSError:
                    pass
        return latest or None
    except OSError:
        return None


def _new_protocols_unverified(days=7):
    """近 N 天 01_protocols 新增 .md 且无 .asc 签名的数量（轻量·限定单目录）"""
    d = datetime.timedelta(days=days)
    now = datetime.datetime.now()
    base = os.path.join(ROOT, "01_protocols")
    try:
        names = [n for n in os.listdir(base) if n.endswith(".md")]
    except OSError:
        return 0
    cnt = 0
    for n in names:
        p = os.path.join(base, n)
        try:
            if now - datetime.datetime.fromtimestamp(os.path.getmtime(p)) <= d:
                if not os.path.exists(p + ".asc"):
                    cnt += 1
        except OSError:
            pass
    return cnt


def _disk_usage():
    """本地根磁盘用量（MB）"""
    try:
        st = os.statvfs(ROOT)
        total = st.f_blocks * st.f_frsize / 1024 / 1024
        free = st.f_bavail * st.f_frsize / 1024 / 1024
        return {"total_gb": round(total / 1024, 1), "free_gb": round(free / 1024, 1)}
    except OSError:
        return {"total_gb": 0, "free_gb": 0}


def load_blind_zone():
    """AI 掌握、主权人可能未查阅的真实风险/模式"""
    now = datetime.datetime.now()
    items = []

    # 1) 备份新鲜度
    bk = _recent_mtime(os.path.join(ROOT, "backup"))
    if bk:
        age_days = int((now - datetime.datetime.fromtimestamp(bk)).total_seconds() // 86400)
        if age_days >= 1:
            items.append({
                "title": "备份新鲜度", "desc": "backup/ 最近更新于 %d 天前%s"
                % (age_days, "（建议 <7 天）" if age_days >= 7 else ""),
                "level": "red" if age_days >= 7 else "yellow",
            })
        else:
            items.append({"title": "备份新鲜度", "desc": "backup/ 今日已更新", "level": "green"})

    # 2) 近7天新协议未签章
    n = _new_protocols_unverified(7)
    if n:
        items.append({
            "title": "待签章协议", "desc": "近 7 天新增 %d 份协议未补 GPG 签名" % n, "level": "yellow",
        })

    # 3) 磁盘
    du = _disk_usage()
    items.append({"title": "磁盘水位", "desc": "本地磁盘 剩余 %.1fG / 共 %.1fG" % (du["free_gb"], du["total_gb"]), "level": "green"})

    # 4) 每日记忆活跃度
    today = now.strftime("%Y-%m-%d")
    daily = os.path.join(ROOT, ".codebuddy", "memory", today + ".md")
    try:
        with open(daily, encoding="utf-8") as f:
            lines = f.readlines()
        items.append({"title": "今日记忆", "desc": "今日日志 %d 行·系统持续在记账" % len(lines), "level": "green"})
    except OSError:
        items.append({"title": "今日记忆", "desc": "今日尚未产生日志条目", "level": "green"})

    # 5) STATE.md 待办
    try:
        with open(os.path.join(ROOT, "STATE.md"), encoding="utf-8") as f:
            s = f.read()
        todo = len(re.findall(r"\[ \]", s)) + len(re.findall(r"- \[ \]", s))
        if todo:
            items.append({"title": "待办积压", "desc": "STATE.md 标记未完成事项 %d 项" % todo, "level": "yellow"})
    except OSError:
        pass

    return items


# ────────────────────────── 隐藏区：主权占位 ──────────────────────────
def load_hidden_zone():
    return [
        {"title": "部署环境细节", "desc": "只有主权人掌握的机器/网络/物理环境信息", "tag": "主权"},
        {"title": "真实预算与资源上限", "desc": "对外预算 vs 实际可动用上限，未披露部分", "tag": "主权"},
        {"title": "线下关系与情报", "desc": "线下掌握、尚未进入系统的信息", "tag": "主权"},
        {"title": "最终决策权限", "desc": "哪些事只有老大拍板，AI 不得代行", "tag": "主权"},
    ]


# ────────────────────────── 未知区：共同边疆 ──────────────────────────
def load_unknown_zone():
    return [
        {"title": "量子计算威胁面", "desc": "对当前加密体系的长期威胁评估", "tag": "边疆"},
        {"title": "未来 6 个月 API 需求", "desc": "尚未触发的新能力需求", "tag": "边疆"},
        {"title": "未定义的新威胁向量", "desc": "AI 与主权人都没见过的风险形状", "tag": "边疆"},
        {"title": "认知边界的下一层", "desc": "乔哈里视窗本身如何演进", "tag": "边疆"},
    ]


# ────────────────────────── 主流程 ──────────────────────────
def main():
    out = OUT_DEFAULT
    if "--out" in sys.argv:
        out = sys.argv[sys.argv.index("--out") + 1]

    data = {
        "dna": DNA,
        "generated_at": NOW,
        "confirm": CONFIRM,
        "gpg": GPG,
        "open": load_open_zone(),
        "blind": load_blind_zone(),
        "hidden": load_hidden_zone(),
        "unknown": load_unknown_zone(),
    }

    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    # 三色：盲区有 red 即黄，否则绿
    colors = [i["level"] for i in data["blind"] if i.get("level")]
    tri = "🟡" if "red" in colors else "🟢"
    print("✅ johari_data.json 已生成 → %s" % out)
    print("   开放区 %d · 盲区 %d · 隐藏区 %d · 未知区 %d · %s"
          % (len(data["open"]), len(data["blind"]), len(data["hidden"]), len(data["unknown"]), tri))
    print("   生成时间: %s" % NOW)
    return 0


if __name__ == "__main__":
    sys.exit(main())
