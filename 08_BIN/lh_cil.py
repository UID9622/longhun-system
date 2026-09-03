#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂系统 CIL（命令行交互层）v4.0 — 意识流场终端
DNA: #龍芯⚡️2026-09-01-龍魂CIL-v4.0-UID9622
创建者: 诸葛鑫（UID9622）
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
协议: CC BY-NC-SA 4.0（核心思想层）
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
算法口径对齐: 01_protocols/LH-WUXING-CALC-WELD-v4.0.md（焊死·唯一权威源）
  · 数字根五行: 1水 2火 3木 4金 5土 6水 7火 8木 9金 0土
  · 熔断 {3,9}→🔴 · 待审 6→🟡 · 其余→🟢
  · H = 克制×0.30 + 疏导×0.25 + 补益×0.20 + 均衡×0.15 + 链路×0.10 · 阈值 0.80/0.50

命令: bazi(四柱全量) / flow(文本→流场节点) / audit(三色审计) / route(六门路由) / shell(交互REPL)
双模式: 彩色人类可读 / --json 机器可读 · 无第三方依赖(仅Python标准库)
集成: lh cil <子命令> · 直接运行本文件亦可
"""

import sys
import json
import hashlib
import argparse
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Union

# ============================================================
# 一、核心常量（与焊死协议 LH-WUXING-CALC-WELD-v4.0 对齐）
# ============================================================
天干五行表 = {
    "甲": "木", "乙": "木", "丙": "火", "丁": "火",
    "戊": "土", "己": "土", "庚": "金", "辛": "金",
    "壬": "水", "癸": "水",
}
地支五行表 = {
    "子": "水", "丑": "土", "寅": "木", "卯": "木",
    "辰": "土", "巳": "火", "午": "火", "未": "土",
    "申": "金", "酉": "金", "戌": "土", "亥": "水",
}
五行相生 = {"金": "水", "水": "木", "木": "火", "火": "土", "土": "金"}
五行相克 = {"金": "木", "木": "土", "土": "水", "水": "火", "火": "金"}
# 焊死口径: 1水 2火 3木 4金 5土 6水 7火 8木 9金 0土
数字根五行表 = {0: "土", 1: "水", 2: "火", 3: "木", 4: "金",
                5: "土", 6: "水", 7: "火", 8: "木", 9: "金"}

位置权重表 = {
    "年柱": {"天干": 1.0, "地支": 0.8},
    "月柱": {"天干": 1.5, "地支": 1.2},
    "日柱": {"天干": 2.0, "地支": 1.6},
    "时柱": {"天干": 1.2, "地支": 1.0},
}

五行视觉 = {
    "金": {"color": "gold",   "emoji": "🟡", "ansi": "\033[93m"},
    "木": {"color": "green",  "emoji": "🟢", "ansi": "\033[92m"},
    "水": {"color": "blue",   "emoji": "🔵", "ansi": "\033[94m"},
    "火": {"color": "red",    "emoji": "🔴", "ansi": "\033[91m"},
    "土": {"color": "yellow", "emoji": "🟠", "ansi": "\033[93m"},
}
RESET = "\033[0m"

五行补益表 = {
    "金": {"颜色": ["白", "金", "银"], "方位": "西", "建议": "多用白色·朝西·增肺活量"},
    "木": {"颜色": ["绿", "青"],       "方位": "东", "建议": "多亲近植物·朝东·护肝"},
    "水": {"颜色": ["黑", "深蓝"],     "方位": "北", "建议": "多喝水·朝北·保护肾"},
    "火": {"颜色": ["红", "橙", "紫"], "方位": "南", "建议": "多晒太阳·朝南·护心"},
    "土": {"颜色": ["黄", "棕"],       "方位": "中", "建议": "规律饮食·接地气·护脾胃"},
}
熔断数字根 = [3, 9]

# 六门路由（CIL v4.0 设计）· 集合匹配避免子串误判
六门 = {
    "民生":     {"土"},
    "教育":     {"木"},
    "权益":     {"金"},
    "技术":     {"木", "金"},
    "数据主权": {"水"},
    "创作":     {"火"},
}

# ============================================================
# 二、核心算法引擎
# ============================================================
class 龍魂引擎:
    @staticmethod
    def 计算数字根(text: Union[str, int]) -> int:
        """健壮版数字根：兼容 Unicode 全角数字（int() 原生支持），无数字→0"""
        s = str(text)
        digits = [int(c) for c in s if c.isdigit()]
        if not digits:
            return 0
        n = sum(digits)
        while n >= 10:
            n = sum(int(c) for c in str(n))
        return n

    @staticmethod
    def 三色审计(dr: int) -> str:
        if dr in [3, 9]:
            return "🔴"
        if dr == 6:
            return "🟡"
        return "🟢"

    @staticmethod
    def 判断关系(a: str, b: Optional[str]) -> Tuple[str, str]:
        if not b:
            return "起点", f"{a}为起始"
        if a == b:
            return "比和", f"{a}遇{b}·力量加倍"
        if 五行相生.get(a) == b:
            return "相生", f"{a}生{b}·{b}增强"
        if 五行相克.get(a) == b:
            return "相克", f"{a}克{b}·需审计"
        if 五行相生.get(b) == a:
            return "相泄", f"{b}生{a}反向·消耗自身"
        if 五行相克.get(b) == a:
            return "相耗", f"{b}克{a}·高消耗"
        return "混合", "无直接生克"

    @staticmethod
    def 计算五行强度(四柱: Dict) -> Dict:
        得分 = {k: 0.0 for k in ["金", "木", "水", "火", "土"]}
        for 柱位, 干支 in 四柱.items():
            w = 位置权重表[柱位]
            if 干支.get("天干") in 天干五行表:
                得分[天干五行表[干支["天干"]]] += w["天干"]
            if 干支.get("地支") in 地支五行表:
                得分[地支五行表[干支["地支"]]] += w["地支"]
        总分 = sum(得分.values()) or 1
        均值 = 总分 / 5
        方差 = sum((v - 均值) ** 2 for v in 得分.values()) / 5
        均衡指数 = max(0.0, round(1.0 - (方差 ** 0.5) / (均值 + 1e-6), 3))
        缺失 = [k for k, v in 得分.items() if v == 0]
        最强 = max(得分, key=得分.get)
        最弱 = min(得分, key=得分.get)
        return {"得分": 得分, "最强": 最强, "最弱": 最弱, "均衡指数": 均衡指数, "缺失": 缺失}

    @staticmethod
    def 链路分析(得分: Dict) -> Dict:
        顺序 = ["金", "水", "木", "火", "土"]
        健康度 = 100
        预警 = []
        for i in range(5):
            src, tgt = 顺序[i], 顺序[(i + 1) % 5]
            if 得分.get(src, 0) > 0 and 得分.get(tgt, 0) == 0:
                预警.append(f"🔴 断链：{src}→{tgt}(0分)")
                健康度 -= 15
        总分 = sum(得分.values()) or 1
        for k, v in 得分.items():
            if v / 总分 > 0.4:
                疏导 = 五行相生[k]
                预警.append(f"🟡 过旺：{k}占{v / 总分:.0%}·引生{疏导}")
                健康度 -= 10
        return {"健康度": max(0, 健康度), "预警": 预警}

    @staticmethod
    def 计算H指数(强度: Dict, 链路: Dict) -> Dict:
        得分 = 强度["得分"]
        总分 = sum(得分.values()) or 1
        过旺 = [k for k, v in 得分.items() if v / 总分 > 0.4]
        克制分 = 1.0
        if 过旺:
            命中 = sum(1 for k in 过旺 for src, tgt in 五行相克.items() if tgt == k and 得分.get(src, 0) > 0)
            克制分 = round(命中 / len(过旺), 3) if 过旺 else 1.0
        疏导分 = 1.0
        if 过旺:
            命中 = sum(1 for k in 过旺 if 得分.get(五行相生[k], 0) > 0)
            疏导分 = round(命中 / len(过旺), 3) if 过旺 else 1.0
        缺失 = len(强度.get("缺失", []))
        补益分 = 1.0 if 缺失 == 0 else round(max(0, 1 - 缺失 / 5), 3)
        均衡 = 强度.get("均衡指数", 0)
        链路分 = 链路.get("健康度", 0) / 100

        H = round(
            克制分 * 0.30 + 疏导分 * 0.25 + 补益分 * 0.20 +
            均衡 * 0.15 + 链路分 * 0.10, 3
        )
        if H >= 0.8:
            状态, action = "🟢 对冲充分", "enter"
        elif H >= 0.5:
            状态, action = "🟡 对冲不足", "hold"
        else:
            状态, action = "🔴 对冲失败", "fuse"
        return {"H": H, "状态": 状态, "action": action,
                "分项": {"克制": 克制分, "疏导": 疏导分, "补益": 补益分, "均衡": 均衡, "链路": 链路分}}

    @staticmethod
    def 生成节点(text: str, title: str = "流场节点") -> Dict:
        dr = 龍魂引擎.计算数字根(text)
        el = 数字根五行表[dr]
        audit = 龍魂引擎.三色审计(dr)
        hash8 = hashlib.sha256(text.encode("utf-8")).hexdigest()[:8].upper()
        return {
            "node_id": f"FLOW-9622-{datetime.now().strftime('%Y%m%d')}-{hash8}",
            "title": title,
            "digital_root": dr,
            "element": el,
            "audit": audit,
            "action": "enter" if audit == "🟢" else ("hold" if audit == "🟡" else "fuse"),
            # visual 只含纯数据（色名+emoji），ansi 转义仅用于显示层，避免污染 JSON
            "visual": {"emoji": 五行视觉[el]["emoji"], "color": 五行视觉[el]["color"]},
            "sancai": {"天": 0.35, "地": 0.15, "人": 0.50},
        }

    @staticmethod
    def 六门路由(dr: int, el: str) -> Dict:
        match = [k for k, v in 六门.items() if el in v]
        if not match:
            match = ["中宫"]
        return {"门": match[0], "默认五行": el, "数字根": dr}


# ============================================================
# 三、终端美化工具
# ============================================================
def c(text: str, color: str = "white") -> str:
    codes = {"gold": "93", "green": "92", "blue": "94", "red": "91",
             "yellow": "93", "white": "97", "cyan": "96", "magenta": "95"}
    return f"\033[{codes.get(color, '97')}m{text}{RESET}"


def 打印标题() -> None:
    print(c("\n╔══════════════════════════════════════════════════════════════╗", "gold"))
    print(c("║              🐉 龍魂·系统 CIL  v4.0                      ║", "gold"))
    print(c("║          文化主权：五行不翻译·天干地支不翻译             ║", "gold"))
    print(c("╚══════════════════════════════════════════════════════════════╝\n", "gold"))


# ============================================================
# 四、CLI 命令处理器
# ============================================================
def cmd_bazi(args) -> None:
    四柱 = {
        "年柱": {"天干": args.year_gan, "地支": args.year_zhi},
        "月柱": {"天干": args.month_gan, "地支": args.month_zhi},
        "日柱": {"天干": args.day_gan, "地支": args.day_zhi},
        "时柱": {"天干": args.hour_gan, "地支": args.hour_zhi},
    }
    eng = 龍魂引擎()
    强度 = eng.计算五行强度(四柱)
    链路 = eng.链路分析(强度["得分"])
    H = eng.计算H指数(强度, 链路)
    # 节点基于完整四柱文本（而非仅年柱）
    四柱文本 = "".join(v["天干"] + v["地支"] for v in 四柱.values())
    节点 = eng.生成节点(四柱文本, title="四柱节点")
    路由 = eng.六门路由(节点["digital_root"], 节点["element"])
    补益 = 五行补益表.get(强度["最弱"])

    if args.json:
        print(json.dumps({"四柱": 四柱, "强度": 强度, "链路": 链路, "对冲": H,
                          "节点": 节点, "路由": 路由, "补益": 补益},
                         ensure_ascii=False, indent=2))
        return

    print(c("\n📊 四柱五行强度", "cyan"))
    for k, v in 强度["得分"].items():
        em = 五行视觉[k]["emoji"]
        bar = "█" * int(v * 2)
        print(f"  {em} {k}: {c(str(round(v, 2)), 'white')} {c(bar, 'white')}")
    print(f"  ⚡ 最强: {c(强度['最强'], 'gold')} | 最弱: {c(强度['最弱'], 'blue')}")
    print(f"  ⚖️  均衡指数: {c(str(强度['均衡指数']), 'cyan')}")
    print(f"  ❌ 缺失: {c(', '.join(强度['缺失']) if 强度['缺失'] else '无', 'green')}")

    print(c("\n🔗 链路健康度", "cyan"))
    print(f"  健康度: {链路['健康度']}%")
    for w in 链路["预警"]:
        print(f"  {w}")

    print(c(f"\n⚖️  对冲指数 H = {H['H']}  {H['状态']}", "magenta"))
    print(f"  Action: {c(H['action'].upper(), 'gold')}")
    print(f"  分项: {json.dumps(H['分项'], ensure_ascii=False)}")

    print(c("\n💊 补益建议", "cyan"))
    if 补益:
        print(f"  最弱五行: {强度['最弱']} → {补益['建议']} · 方位: {补益['方位']} · 颜色: {'/'.join(补益['颜色'])}")
    else:
        print("  五行齐备，无需特别补益")

    print(c("\n🧬 流场节点", "cyan"))
    print(f"  ID: {节点['node_id']}")
    print(f"  数字根: {节点['digital_root']} → {节点['element']}")
    print(f"  审计: {节点['audit']} → Action: {节点['action']}")
    print(f"  路由: {路由['门']} ({路由['默认五行']})")


def cmd_flow(args) -> None:
    eng = 龍魂引擎()
    node = eng.生成节点(args.text, args.title)
    route = eng.六门路由(node["digital_root"], node["element"])
    if args.json:
        print(json.dumps({"node": node, "route": route}, ensure_ascii=False, indent=2))
        return
    print(c(f"\n🧬 流场压缩结果: {args.title}", "cyan"))
    print(f"  ID: {node['node_id']}")
    print(f"  数字根: {node['digital_root']} → {node['element']}")
    print(f"  审计: {node['audit']} → Action: {node['action']}")
    print(f"  六门路由: {route['门']}")
    print(f"  三才权重: {node['sancai']}")


def cmd_audit(args) -> None:
    eng = 龍魂引擎()
    dr = eng.计算数字根(args.text)
    audit = eng.三色审计(dr)
    el = 数字根五行表[dr]
    route = eng.六门路由(dr, el)
    if args.json:
        print(json.dumps({"text": args.text, "digital_root": dr, "element": el,
                          "audit": audit, "route": route}, ensure_ascii=False, indent=2))
        return
    print(c(f"\n🔍 三色审计: {args.text}", "cyan"))
    print(f"  数字根: {dr} → {el} → {audit}")
    print(f"  熔断判定: {c('🔴 熔断(3/9)' if audit == '🔴' else ('🟡 待审(6)' if audit == '🟡' else '🟢 放行'), 'gold')}")
    print(f"  六门路由: {route['门']}")


def cmd_route(args) -> None:
    eng = 龍魂引擎()
    dr = eng.计算数字根(args.text)
    el = 数字根五行表[dr]
    route = eng.六门路由(dr, el)
    if args.json:
        print(json.dumps({"text": args.text, "digital_root": dr, "element": el,
                          "route": route}, ensure_ascii=False, indent=2))
        return
    print(c(f"\n🧭 六门路由: {args.text}", "cyan"))
    print(f"  数字根: {dr} → {el} → 门: {route['门']}")


def cmd_shell(args) -> None:
    打印标题()
    print(c("⚡ 进入交互式龍魂终端 (输入 'exit' 或 Ctrl+D 退出)", "cyan"))
    print(c("  命令: bazi <年干> <年支> <月干> <月支> <日干> <日支> <时干> <时支>", "yellow"))
    print(c("        flow <文本内容>", "yellow"))
    print(c("        audit <数字/文本>", "yellow"))
    print(c("        route <文本>", "yellow"))
    print(c("        help / exit", "yellow"))
    print("-" * 60)
    eng = 龍魂引擎()
    while True:
        try:
            cmd = input(c("\n🐉 > ", "green")).strip()
            if not cmd:
                continue
            if cmd in ["exit", "quit", "q"]:
                break
            if cmd in ["help", "h", "?"]:
                print(c("  bazi 年干 年支 月干 月支 日干 日支 时干 时支", "yellow"))
                print(c("  flow <文本>  |  audit <文本>  |  route <文本>  |  exit", "yellow"))
                continue
            parts = cmd.split()
            if parts[0] == "bazi" and len(parts) == 9:
                args_b = type('obj', (object,), {
                    "year_gan": parts[1], "year_zhi": parts[2],
                    "month_gan": parts[3], "month_zhi": parts[4],
                    "day_gan": parts[5], "day_zhi": parts[6],
                    "hour_gan": parts[7], "hour_zhi": parts[8],
                    "json": False,
                })()
                cmd_bazi(args_b)
            elif parts[0] == "flow":
                text = " ".join(parts[1:])
                args_f = type('obj', (object,), {"text": text, "title": "Shell节点", "json": False})()
                cmd_flow(args_f)
            elif parts[0] == "audit":
                text = " ".join(parts[1:]) or "0"
                args_a = type('obj', (object,), {"text": text, "json": False})()
                cmd_audit(args_a)
            elif parts[0] == "route":
                text = " ".join(parts[1:]) or "0"
                args_r = type('obj', (object,), {"text": text, "json": False})()
                cmd_route(args_r)
            else:
                print(c("未知命令。支持: bazi, flow, audit, route, help, exit", "red"))
        except (KeyboardInterrupt, EOFError):
            print("\n退出。")
            break


# ============================================================
# 五、主入口
# ============================================================
def main() -> None:
    parser = argparse.ArgumentParser(prog="lh cil", description="🐉 龍魂系统 CIL v4.0", add_help=False)
    parser.add_argument("--help", action="help", help="显示帮助信息")
    parser.add_argument("--version", action="store_true", help="版本信息")
    subparsers = parser.add_subparsers(dest="command", help="子命令")

    # bazi 命令
    p_bazi = subparsers.add_parser("bazi", help="计算八字五行强度")
    for p in ["year", "month", "day", "hour"]:
        p_bazi.add_argument(f"--{p}-gan", required=True, help=f"{p}天干")
        p_bazi.add_argument(f"--{p}-zhi", required=True, help=f"{p}地支")
    p_bazi.add_argument("--json", action="store_true", help="输出JSON")

    # flow 命令
    p_flow = subparsers.add_parser("flow", help="压缩文本为流场节点")
    p_flow.add_argument("text", help="输入文本")
    p_flow.add_argument("--title", default="流场节点", help="节点标题")
    p_flow.add_argument("--json", action="store_true", help="输出JSON")

    # audit 命令
    p_audit = subparsers.add_parser("audit", help="三色审计文本")
    p_audit.add_argument("text", help="输入文本")
    p_audit.add_argument("--json", action="store_true", help="输出JSON")

    # route 命令
    p_route = subparsers.add_parser("route", help="六门路由判定")
    p_route.add_argument("text", help="输入文本")
    p_route.add_argument("--json", action="store_true", help="输出JSON")

    # shell 命令
    subparsers.add_parser("shell", help="进入交互式终端")

    # 无参数默认进入 shell
    if len(sys.argv) == 1:
        sys.argv.append("shell")

    args = parser.parse_args()

    if args.version:
        print("🐉 龍魂系统 CIL v4.0 · DNA: #龍芯⚡️2026-09-01-龍魂CIL-v4.0-UID9622")
        return

    if args.command == "bazi":
        cmd_bazi(args)
    elif args.command == "flow":
        cmd_flow(args)
    elif args.command == "audit":
        cmd_audit(args)
    elif args.command == "route":
        cmd_route(args)
    elif args.command == "shell":
        cmd_shell(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
