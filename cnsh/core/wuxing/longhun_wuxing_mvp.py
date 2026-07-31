# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# -*- coding: utf-8 -*-
##龍芯⚡️2026-06-21-CORE-LONGHUN_WUXING_MVP-FILE1-v1.0-2
# 君子协议: 本文件受龍魂DNA追溯保护

#!/usr/bin/env python3
"""
龍魂五行MVP · 八字洛书引擎
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
UID9622 · 诸葛鑫 · 龍芯北辰
DNA: #龍芯⚡️20260426-CODE-WX01
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

功能：
  五行属性推断（木火土金水）
  八字数字根映射
  洛书方阵生成与查询
  CNSH三色审计输出

用法：
  python longhun_wuxing_mvp.py
  python longhun_wuxing_mvp.py --demo
  python longhun_wuxing_mvp.py --check 9622
"""

import sys
import hashlib
from datetime import datetime
from pathlib import Path

# 引入计算优化模块
sys.path.insert(0, str(Path(__file__).resolve().parent))
from wuxing_calc_optimizations import robust_digital_root

# ═══════════════════════════════
# 五行基础数据
# ═══════════════════════════════

# 五行属性
WUXING = {
    "木": {"color": "青", "direction": "东", "season": "春", "number": 3, "organ": "肝", "virtue": "仁"},
    "火": {"color": "赤", "direction": "南", "season": "夏", "number": 2, "organ": "心", "virtue": "礼"},
    "土": {"color": "黄", "direction": "中", "season": "季月", "number": 5, "organ": "脾", "virtue": "信"},
    "金": {"color": "白", "direction": "西", "season": "秋", "number": 4, "organ": "肺", "virtue": "义"},
    "水": {"color": "黑", "direction": "北", "season": "冬", "number": 1, "organ": "肾", "virtue": "智"},
}

# 五行生克关系
SHENG = {"木": "火", "火": "土", "土": "金", "金": "水", "水": "木"}   # 相生
KE   = {"木": "土", "土": "水", "水": "火", "火": "金", "金": "木"}   # 相克

# 数字→五行映射（洛书数）
NUM_TO_WUXING = {
    1: "水", 2: "火", 3: "木", 4: "金",
    5: "土", 6: "金", 7: "火", 8: "木", 9: "水"
}

# 天干
TIANGAN = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
TG_WUXING = {
    "甲": "木", "乙": "木", "丙": "火", "丁": "火", "戊": "土",
    "己": "土", "庚": "金", "辛": "金", "壬": "水", "癸": "水"
}

# 地支
DIZHI = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
DZ_WUXING = {
    "子": "水", "丑": "土", "寅": "木", "卯": "木", "辰": "土", "巳": "火",
    "午": "火", "未": "土", "申": "金", "酉": "金", "戌": "土", "亥": "水"
}

# ═══════════════════════════════
# 洛书九宫方阵
# ═══════════════════════════════
LOSHU = [
    [4, 9, 2],
    [3, 5, 7],
    [8, 1, 6],
]

LOSHU_PALACE = {
    1: "坎·北·水", 2: "坤·西南·土", 3: "震·东·木",
    4: "巽·东南·木", 5: "中宫·土", 6: "干·西北·金",
    7: "兑·西·金", 8: "艮·东北·土", 9: "离·南·火"
}

# ═══════════════════════════════
# 工具函数
# ═══════════════════════════════

def digital_root(n) -> int:
    """
    计算数字根（反复对各位数字求和直到个位）。
    已接入鲁棒数字根：支持全角数字、中文数字、负数、小数。
    """
    return robust_digital_root(n)

def sha8(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()[:8].upper()

def make_dna(type_code: str, content: str) -> str:
    date = datetime.now().strftime("%Y%m%d")
    return f"#龍芯⚡️{date}-{type_code}-{sha8(content)}"

def tricolor(dr: int) -> str:
    """三色审计：数字根熔断判断"""
    if dr in (3, 9):
        return "🔴"
    elif dr in (1, 2, 4, 5, 6, 7, 8):
        return "🟢"
    else:
        return "🟡"

# ═══════════════════════════════
# 五行核心函数
# ═══════════════════════════════

def number_to_wuxing(n: int) -> str:
    """数字→五行属性"""
    dr = digital_root(abs(n))
    return NUM_TO_WUXING.get(dr, "土")

def wuxing_sheng(element: str) -> str:
    """返回该五行所生的五行"""
    return SHENG.get(element, "未知")

def wuxing_ke(element: str) -> str:
    """返回该五行所克的五行"""
    return KE.get(element, "未知")

def analyze_number(n: int) -> dict[str, Any]:
    """完整分析一个数字的五行属性"""
    dr = digital_root(n)
    wx = number_to_wuxing(n)
    info = WUXING.get(wx, {})
    palace = LOSHU_PALACE.get(dr, "未知宫位")
    tc = tricolor(dr)

    return {
        "input": n,
        "digital_root": dr,
        "wuxing": wx,
        "color": info.get("color", ""),
        "direction": info.get("direction", ""),
        "season": info.get("season", ""),
        "organ": info.get("organ", ""),
        "virtue": info.get("virtue", ""),
        "sheng": wuxing_sheng(wx),
        "ke": wuxing_ke(wx),
        "loshu_palace": palace,
        "tricolor": tc,
        "dna": make_dna("WX", str(n))
    }

def analyze_uid(uid_str: str) -> dict[str, Any]:
    """分析UID字符串的五行属性（已接入鲁棒数字根）"""
    dr = robust_digital_root(uid_str)
    return analyze_number(dr)

# ═══════════════════════════════
# 八字简化推算
# ═══════════════════════════════

def year_ganzhi(year: int) -> tuple[Any, ...]:
    """返回年份的天干地支"""
    tg_idx = (year - 4) % 10
    dz_idx = (year - 4) % 12
    tg = TIANGAN[tg_idx]
    dz = DIZHI[dz_idx]
    return tg, dz, TG_WUXING[tg], DZ_WUXING[dz]

def bazi_wuxing_score(year: int) -> dict[str, Any]:
    """八字年柱五行强度评估"""
    tg, dz, tg_wx, dz_wx = year_ganzhi(year)
    score = {}
    for wx in WUXING:
        score[wx] = 0
    score[tg_wx] += 2
    score[dz_wx] += 1
    dominant = max(score, key=score.get)
    return {
        "year": year,
        "tiangan": tg,
        "dizhi": dz,
        "tg_wuxing": tg_wx,
        "dz_wuxing": dz_wx,
        "score": score,
        "dominant": dominant,
        "dna": make_dna("BA", str(year))
    }

# ═══════════════════════════════
# 洛书方阵显示
# ═══════════════════════════════

def print_loshu():
    """打印洛书九宫格"""
    print("\n╔═══════════════════════════╗")
    print("║       洛 书 九 宫 格       ║")
    print("╠═══════╦═══════╦═══════╣")
    labels = {
        4: "巽木", 9: "离火", 2: "坤土",
        3: "震木", 5: "中土", 7: "兑金",
        8: "艮土", 1: "坎水", 6: "干金"
    }
    for row in LOSHU:
        cells = []
        for num in row:
            cells.append(f" {num}({labels[num]}) ")
        print("║" + "║".join(cells) + "║")
        if row != LOSHU[-1]:
            print("╠═══════╬═══════╬═══════╣")
    print("╚═══════╩═══════╩═══════╝")

# ═══════════════════════════════
# 五行平衡分析
# ═══════════════════════════════

def wuxing_balance_report(scores: dict[str, Any]) -> str:
    """五行平衡报告"""
    total = sum(scores.values()) or 1
    lines = []
    for wx, score in sorted(scores.items(), key=lambda x: -x[1]):
        pct = score / total * 100
        bar = "█" * int(pct / 10) + "░" * (10 - int(pct / 10))
        info = WUXING[wx]
        lines.append(f"  {wx}({info['color']}) [{bar}] {pct:.0f}%  →生{SHENG[wx]} ×克{KE[wx]}")
    return "\n".join(lines)

# ═══════════════════════════════
# CNSH协议输出格式
# ═══════════════════════════════

def cnsh_output(title: str, data: dict[str, Any], tc: str = "🟢"):
    """标准CNSH输出格式"""
    print(f"\n{'━'*50}")
    print(f"  {title}")
    print(f"{'━'*50}")
    for k, v in data.items():
        if k not in ("dna", "tricolor"):
            print(f"  {k:<16} : {v}")
    print(f"{'─'*50}")
    print(f"  三色 : {tc}")
    if "dna" in data:
        print(f"  DNA  : {data['dna']}")
    print(f"{'━'*50}")

# ═══════════════════════════════
# 主演示
# ═══════════════════════════════

def demo():
    print("""
╔══════════════════════════════════════════════╗
║  龍魂五行MVP · 八字洛书引擎 v1.0 · UID9622  ║
║  DNA: #龍芯⚡️20260426-CODE-WX01              ║
╠══════════════════════════════════════════════╣
║  五行映射 | 洛书九宫 | 数字根熔断 | CNSH    ║
╚══════════════════════════════════════════════╝
    """)

    # 洛书展示
    print_loshu()

    # UID9622 分析
    uid_result = analyze_uid("9622")
    cnsh_output("UID9622 五行分析", uid_result, uid_result["tricolor"])

    # 当前年份八字
    year = datetime.now().year
    bazi = bazi_wuxing_score(year)
    cnsh_output(f"{year}年 八字年柱", bazi, "🟢")

    # 五行平衡报告
    print(f"\n{'━'*50}")
    print(f"  {year}年 五行强度分布")
    print(f"{'━'*50}")
    print(wuxing_balance_report(bazi["score"]))

    # 数字测试组
    print(f"\n{'━'*50}")
    print("  数字根熔断测试（dr∈{{3,9}}→🔴）")
    print(f"{'━'*50}")
    test_nums = [9622, 3, 9, 12, 27, 100, 5]
    for n in test_nums:
        dr = digital_root(n)
        tc = tricolor(dr)
        wx = number_to_wuxing(n)
        print(f"  {n:<6} → dr={dr} {wx} {tc}")

    print(f"\n🟢 五行MVP演示完成 · {make_dna('WX', 'demo')}")

def check_number(n_str: str):
    """检查单个数字/UID"""
    try:
        n = int(n_str)
        result = analyze_number(n)
        cnsh_output(f"五行分析: {n}", result, result["tricolor"])
    except ValueError:
        # 当作UID字符串处理
        result = analyze_uid(n_str)
        cnsh_output(f"UID五行分析: {n_str}", result, result["tricolor"])

# ═══════════════════════════════
# Flask API（可选启动）
# ═══════════════════════════════

def run_server(port: int = 9624):
    """启动五行API服务"""
    try:
        from flask import Flask, request, jsonify
        app = Flask(__name__)

        @app.route("/wuxing/<number>")
        def api_wuxing(number):
            result = analyze_number(int(number))
            return jsonify(result)

        @app.route("/bazi/<int:year>")
        def api_bazi(year):
            result = bazi_wuxing_score(year)
            return jsonify(result)

        @app.route("/health")
        def health():
            return jsonify({
                "status": "🟢",
                "service": "五行MVP v1.0",
                "port": port,
                "dna": make_dna("SYS", "health")
            })

        print(f"五行MVP API 启动 → :  {port}")
        app.run(host="127.0.0.1", port=port, debug=False)
    except ImportError:
        print("❌ Flask未安装: pip install flask --break-system-packages")

# ═══════════════════════════════
# 入口
# ═══════════════════════════════

if __name__ == "__main__":
    if len(sys.argv) == 1 or "--demo" in sys.argv:
        demo()
    elif "--check" in sys.argv:
        idx = sys.argv.index("--check")
        if idx + 1 < len(sys.argv):
            check_number(sys.argv[idx + 1])
        else:
            print("用法: python longhun_wuxing_mvp.py --check 9622")
    elif "--server" in sys.argv:
        run_server()
    else:
        check_number(sys.argv[1])
