#!/usr/bin/env python3
# DNA: #龍芯⚡️丙午·丙申·甲戌·卯时·䷐随-QUAD-SYNC-v1.0-ATTRIBUTION-8c26d5f
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# -*- coding: utf-8 -*-
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
"""🐉 lh asset · 资产管理命令行"""
import sys, os, json, argparse, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from asset_center import 资产中心

DB = os.path.expanduser("~/.longhun/asset_center.db")

def main():
    p = argparse.ArgumentParser(prog="lh asset", description="龍魂历史资产管理中心")
    sub = p.add_subparsers(dest="cmd")
    i = sub.add_parser("init"); i.add_argument("--scan", metavar="目录", required=True)
    sub.add_parser("list"); 
    s = sub.add_parser("show"); s.add_argument("键")
    q = sub.add_parser("search"); q.add_argument("--type", default=None); q.add_argument("--tag", default="")
    g = sub.add_parser("graph"); g.add_argument("键")
    h = sub.add_parser("history"); h.add_argument("键")
    e = sub.add_parser("export"); e.add_argument("--format", default="json")
    r = sub.add_parser("retire"); r.add_argument("键"); r.add_argument("--reason", default="")
    v = sub.add_parser("revive"); v.add_argument("键")
    sub.add_parser("verify")
    l = sub.add_parser("link"); l.add_argument("甲"); l.add_argument("乙"); l.add_argument("--rel", default="depends_on")
    a = p.parse_args()

    os.makedirs(os.path.dirname(DB), exist_ok=True)
    ac = 资产中心(DB)

    if a.cmd == "init":
        统计 = ac.扫描(a.scan)
        print(f"🐉 init --scan 完成: {统计} | 验链: {ac.验链()}")
    elif a.cmd == "list":
        for r_ in ac.查询(): print(f"  {r_[0]} [{r_[1]}] {r_[2]} {r_[3]}")
    elif a.cmd == "show":
        d = ac.详情(a.键)
        if not d: print("未找到"); sys.exit(1)
        rec = d["记录"]
        print(f"🧬 {rec[0]} [{rec[2]}] {rec[3]}\n  DNA: {rec[1]}\n  状态: {rec[8]} 位置: {rec[9]}\n  描述: {rec[10]} 标签: {rec[11]}")
        print("  历史:", [f"{time.strftime('%m-%d %H:%M',time.localtime(x[0]))} {x[1]}" for x in d["历史"]])
        print("  关系:", d["关系"] or "无")
    elif a.cmd == "search":
        for r_ in ac.查询(关键词=a.tag, 类型=a.type): print(f"  {r_[0]} [{r_[1]}] {r_[2]}")
    elif a.cmd == "graph":
        for f,t,rel in ac.图(a.键): print(f"  {f} --{rel}--> {t}")
    elif a.cmd == "history":
        d = ac.详情(a.键)
        for x in (d["历史"] if d else []): print(f"  {time.strftime('%Y-%m-%d %H:%M',time.localtime(x[0]))} {x[1]} {x[2][:12]}")
    elif a.cmd == "export":
        print(json.dumps(ac.导出(), ensure_ascii=False, indent=2))
    elif a.cmd == "retire":
        aid = ac.注销(a.键, a.reason); print(f"⚪ 已注销(冻结·可revive): {aid}")
    elif a.cmd == "revive":
        ac.复活(a.键); print("🟢 已复活")
    elif a.cmd == "verify":
        print(f"验链: {ac.验链()}")
    elif a.cmd == "link":
        ac.关联(a.甲, a.乙, a.rel); print(f"🔗 {a.甲} --{a.rel}--> {a.乙}")

if __name__ == "__main__":
    main()
