#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 🐉 龍魂系统 · ASI 能力落地台账引擎 v1.0
# DNA: #龍芯⚡️丙午·丁酉·癸未·ASI-CAPABILITY-LEDGER-v1.0-UID9622
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# 功能: 读取 08_STATE/asi_capability_ledger.json（规划五层30项能力对照台账）
#       输出三色 GAP 报告；check 勾选回写完成状态 = 落地进度可机器追踪。
# 用法:
#   python3 08_BIN/lh_asi_ledger.py summary   # 三色统计
#   python3 08_BIN/lh_asi_ledger.py list      # 全量清单（层/项/状态/证据摘要）
#   python3 08_BIN/lh_asi_ledger.py gap       # 红黄缺口 + 决策点 + 待建 todo
#   python3 08_BIN/lh_asi_ledger.py show B3   # 单项详情
#   python3 08_BIN/lh_asi_ledger.py check T2  # 勾选完成（写回 json·幂等）
# 原则: 按需触发·用完即沉默（节能协议 v1.1）· 数据源唯一权威=json
import datetime
import json
import os
import sys

ROOT = os.path.expanduser("~/longhun-system")
LEDGER = os.path.join(ROOT, "08_STATE", "asi_capability_ledger.json")
GPG = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
COLOR = {"g": "🟢", "y": "🟡", "r": "🔴"}


def _load():
    with open(LEDGER, encoding="utf-8") as f:
        return json.load(f)


def _save(data):
    with open(LEDGER, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def _stamp():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M")


def _summary(data):
    rows = [it for lay in data["layers"] for it in lay["items"]]
    g = sum(1 for x in rows if x["status"] == "g")
    y = sum(1 for x in rows if x["status"] == "y")
    r = sum(1 for x in rows if x["status"] == "r")
    done = sum(1 for x in rows if x.get("done"))
    tdone = sum(1 for t in data.get("todos", []) if t.get("done"))
    print(f"ASI 能力落地台账 v{data['_meta']['version']} · {len(rows)}项")
    print(f"🟢 绿(实物可证): {g} | 🟡 黄(部分/缺口): {y} | 🔴 红(真缺/硬件): {r} | 能力项done: {done} | todo完成: {tdone}")
    print(f"决策点 {len(data['decisions_needed'])} 项(已裁{sum(1 for d in data['decisions_needed'] if d.get('decision'))}) · 待建 todo {len(data['todos'])} 项")
    return g, y, r


def cmd_summary():
    data = _load()
    _summary(data)
    meta = data["_meta"]
    print(f"DNA: {meta['dna']}")


def cmd_list():
    data = _load()
    _summary(data)
    for lay in data["layers"]:
        print(f"\n■ {lay['layer']}")
        for it in lay["items"]:
            mark = "✓" if it.get("done") else " "
            ev = it.get("evidence", "")[:52]
            print(f"  [{mark}]{COLOR[it['status']]} {it['id']} {it['capability']} | {it['owner']} | {ev}")


def cmd_gap():
    data = _load()
    print("== 🔴 红(真缺/方向待裁决) ==")
    for it in [x for lay in data["layers"] for x in lay["items"] if x["status"] == "r"]:
        print(f"  {COLOR['r']}{it['id']} {it['capability']} —— {it['gap']}")
    print("\n== 🟡 黄(部分落地/有缺口) ==")
    for it in [x for lay in data["layers"] for x in lay["items"] if x["status"] == "y"]:
        print(f"  {COLOR['y']}{it['id']} {it['capability']} —— {it['gap']}")
    print("\n== 决策点(老大拍板) ==")
    for d in data["decisions_needed"]:
        if d.get("decision"):
            print(f"  ✅ {d['id']} {d['topic']} | {d['decision']}（{d.get('decision_date','')}）")
            if d.get("note"):
                print(f"     注: {d['note']}")
        else:
            print(f"  🎯 {d['id']} {d['topic']} | 建议: {d['suggest']}（待老大裁决）")
    print("\n== 待建 todo ==")
    for t in data["todos"]:
        done = "✓" if t.get("done") else "○"
        print(f"  [{done}] {t['id']} {t['task']} | 责任:{t['owner']} 阶段:{t['phase']} 依赖:{t['depends']}")


def cmd_show(item_id):
    data = _load()
    for it in [x for lay in data["layers"] for x in lay["items"]]:
        if it["id"].lower() == item_id.lower():
            print(f"{COLOR[it['status']]} {it['id']} {it['capability']}")
            print(f"  技术栈: {it['stack']}")
            print(f"  证据: {it['evidence']}")
            print(f"  缺口: {it['gap']}")
            print(f"  责任: {it['owner']} | 阶段: {it['phase']} | 形态: {it['form']}")
            if it.get("done"):
                print(f"  已勾选完成: {it['done']}")
            return
    for t in data["todos"]:
        if t["id"].lower() == item_id.lower():
            print(f"TODO {t['id']} {t['task']}")
            print(f"  责任: {t['owner']} | 阶段: {t['phase']} | 依赖: {t['depends']}")
            if t.get("done"):
                print(f"  已勾选完成: {t['done']}")
            return
    for d in data["decisions_needed"]:
        if d["id"].lower() == item_id.lower():
            print(f"🎯 {d['id']} {d['topic']}")
            print(f"  详情: {d.get('detail','')}")
            print(f"  影响: {d.get('impact','')}")
            print(f"  建议: {d.get('suggest','')}")
            if d.get("decision"):
                print(f"  老大拍板({d.get('decision_date','')}): ✅ {d['decision']}")
            if d.get("note"):
                print(f"  注: {d['note']}")
            return
    print(f"❌ 未找到 {item_id}")


def cmd_check(item_id):
    data = _load()
    found = False
    now = _stamp()
    for it in [x for lay in data["layers"] for x in lay["items"]]:
        if it["id"].lower() == item_id.lower():
            it["done"] = now
            found = True
    for t in data["todos"]:
        if t["id"].lower() == item_id.lower():
            t["done"] = now
            found = True
    if not found:
        print(f"❌ 未找到 {item_id}（可用 list 查看全部 id）")
        return 1
    _save(data)
    print(f"✅ {item_id} 已勾选完成 @ {now}")
    return 0


def main():
    args = sys.argv[1:]
    cmd = args[0] if args else "summary"
    table = {
        "summary": cmd_summary,
        "list": cmd_list,
        "gap": cmd_gap,
        "show": lambda: cmd_show(args[1]),
        "check": lambda: cmd_check(args[1]),
    }
    if cmd not in table:
        print("用法: summary | list | gap | show <id> | check <id>")
        return 1
    if cmd in ("show", "check") and len(args) < 2:
        print(f"用法: {cmd} <id>")
        return 1
    table[cmd]()
    return 0


if __name__ == "__main__":
    sys.exit(main())
