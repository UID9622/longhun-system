#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  五彩石色卡引擎 · 龍魂语义视觉熔断系统                                         ║
║  DNA: #龍芯⚡️2026-05-22-WUCAISHI-COLOR-ENGINE-v1.0                           ║
║  GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F                               ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  作者: 诸葛鑫 (UID9622)                                                      ║
║  理论指导: 曾仕强老师（永恒显示）                                              ║
║  献礼: 中华文化 · 女娲补天五彩石                                               ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  核心逻辑:                                                                    ║
║  1. 字符串 → Unicode累加 → 数字根(dr) 1-9                                     ║
║  2. dr → 五行映射 (1/2木 3/4火 5土 6/7金 8/9水)                               ║
║  3. 五行 → 五彩石色卡 (青赤黄白玄)                                            ║
║  4. 369特殊共振数 → 熔断级别标记                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import json
import hashlib
from typing import Dict, Tuple, List, Optional
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

# ═══════════════════════════════════════════════════════════════════════════════
# 五行枚举
# ═══════════════════════════════════════════════════════════════════════════════

class WuXing(Enum):
    """五行·天地万物之本"""
    MU = "木"    # 青龍·东方·生长
    HUO = "火"   # 朱雀·南方·光明
    TU = "土"    # 黄龍·中央·承载
    JIN = "金"   # 白虎·西方·坚固
    SHUI = "水"  # 玄武·北方·流动


class FuseLevel(Enum):
    """熔断级别"""
    NORMAL = 0      # 普通
    CAUTION = 1     # 注意（369共振）
    CRITICAL = 3    # 关键（核心语义）
    ABSOLUTE = 9    # 绝对（铁律级）


# ═══════════════════════════════════════════════════════════════════════════════
# 五彩石色卡定义 · 女娲补天之石
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class WuCaiShiColor:
    """五彩石颜色定义"""
    name: str           # 色名
    wuxing: WuXing      # 五行
    hex_code: str       # HEX色值
    rgb: Tuple[int, int, int]  # RGB
    ansi_fg: str        # 终端前景色
    ansi_bg: str        # 终端背景色
    meaning: str        # 寓意
    fuse_weight: float  # 熔断权重 (0-1)


# 五彩石色卡 · 源自《淮南子》女娲炼石补天
WUCAISHI_PALETTE: Dict[WuXing, WuCaiShiColor] = {
    WuXing.MU: WuCaiShiColor(
        name="青石",
        wuxing=WuXing.MU,
        hex_code="#2E8B57",      # 海绿色·生机
        rgb=(46, 139, 87),
        ansi_fg="\033[38;5;35m",
        ansi_bg="\033[48;5;35m",
        meaning="生长·东方青龍·春·仁",
        fuse_weight=0.3
    ),
    WuXing.HUO: WuCaiShiColor(
        name="赤石",
        wuxing=WuXing.HUO,
        hex_code="#DC143C",      # 绯红色·光明
        rgb=(220, 20, 60),
        ansi_fg="\033[38;5;196m",
        ansi_bg="\033[48;5;196m",
        meaning="光明·南方朱雀·夏·礼",
        fuse_weight=0.6
    ),
    WuXing.TU: WuCaiShiColor(
        name="黄石",
        wuxing=WuXing.TU,
        hex_code="#DAA520",      # 金麒麟黄·承载
        rgb=(218, 165, 32),
        ansi_fg="\033[38;5;178m",
        ansi_bg="\033[48;5;178m",
        meaning="承载·中央黄龍·季·信",
        fuse_weight=0.5
    ),
    WuXing.JIN: WuCaiShiColor(
        name="白石",
        wuxing=WuXing.JIN,
        hex_code="#C0C0C0",      # 银白色·坚固
        rgb=(192, 192, 192),
        ansi_fg="\033[38;5;7m",
        ansi_bg="\033[48;5;7m",
        meaning="坚固·西方白虎·秋·义",
        fuse_weight=0.8
    ),
    WuXing.SHUI: WuCaiShiColor(
        name="玄石",
        wuxing=WuXing.SHUI,
        hex_code="#191970",      # 玄青色·深邃
        rgb=(25, 25, 112),
        ansi_fg="\033[38;5;18m",
        ansi_bg="\033[48;5;18m",
        meaning="流动·北方玄武·冬·智",
        fuse_weight=0.9
    ),
}

# 369特殊色（宇宙共振数）
COSMIC_369_COLORS = {
    3: ("#FF4500", "炎"),   # 火中火·橙红
    6: ("#FFD700", "锐"),   # 金中金·纯金
    9: ("#000080", "渊"),   # 水中水·深渊蓝
}

RESET = "\033[0m"


# ═══════════════════════════════════════════════════════════════════════════════
# 核心计算函数
# ═══════════════════════════════════════════════════════════════════════════════

def calc_digital_root(s: str) -> int:
    """
    计算字符串的数字根(dr)
    规则：Unicode码累加 → 反复求和 → 直到个位数(1-9)
    """
    if not s:
        return 0

    # Unicode累加
    total = sum(ord(c) for c in s)

    # 反复求和直到个位数
    while total > 9:
        total = sum(int(d) for d in str(total))

    return total if total > 0 else 9  # 0映射到9


def dr_to_wuxing(dr: int) -> WuXing:
    """
    数字根 → 五行映射

    映射规则（源自《易经》先天八卦数理）：
    - 1, 2 → 木（甲乙·东方·生数）
    - 3, 4 → 火（丙丁·南方·长数）
    - 5    → 土（戊己·中央·成数）
    - 6, 7 → 金（庚辛·西方·收数）
    - 8, 9 → 水（壬癸·北方·藏数）
    """
    mapping = {
        1: WuXing.MU, 2: WuXing.MU,
        3: WuXing.HUO, 4: WuXing.HUO,
        5: WuXing.TU,
        6: WuXing.JIN, 7: WuXing.JIN,
        8: WuXing.SHUI, 9: WuXing.SHUI,
    }
    return mapping.get(dr, WuXing.TU)


def is_cosmic_369(dr: int) -> bool:
    """判断是否为369宇宙共振数"""
    return dr in (3, 6, 9)


def calc_fuse_level(keyword: str, is_core: bool = False) -> FuseLevel:
    """
    计算熔断级别

    规则：
    - 普通关键字 dr非369 → NORMAL
    - 普通关键字 dr是369 → CAUTION
    - 核心关键字 → CRITICAL
    - 铁律关键字 → ABSOLUTE
    """
    dr = calc_digital_root(keyword)

    if is_core:
        return FuseLevel.ABSOLUTE if "铁律" in keyword or "熔断" in keyword else FuseLevel.CRITICAL

    return FuseLevel.CAUTION if is_cosmic_369(dr) else FuseLevel.NORMAL


# ═══════════════════════════════════════════════════════════════════════════════
# 语义分析结果
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class SemanticColorResult:
    """语义颜色分析结果"""
    keyword: str
    dr: int
    wuxing: WuXing
    color: WuCaiShiColor
    fuse_level: FuseLevel
    is_369: bool
    hex_code: str

    def to_dict(self) -> dict:
        return {
            "keyword": self.keyword,
            "dr": self.dr,
            "wuxing": self.wuxing.value,
            "color_name": self.color.name,
            "hex": self.hex_code,
            "rgb": self.color.rgb,
            "fuse_level": self.fuse_level.name,
            "is_369": self.is_369,
            "meaning": self.color.meaning,
        }

    def terminal_display(self) -> str:
        """终端彩色显示"""
        color = self.color
        badge_369 = " ⚡369" if self.is_369 else ""
        fuse_badge = f" [熔断:{self.fuse_level.name}]" if self.fuse_level.value > 0 else ""

        return (
            f"{color.ansi_fg}█ {self.keyword}{RESET} "
            f"dr={self.dr} {self.wuxing.value}{color.name}{badge_369}{fuse_badge}"
        )


def analyze_keyword(keyword: str, is_core: bool = False) -> SemanticColorResult:
    """分析单个关键字"""
    dr = calc_digital_root(keyword)
    wuxing = dr_to_wuxing(dr)
    color = WUCAISHI_PALETTE[wuxing]
    fuse_level = calc_fuse_level(keyword, is_core)
    is_369 = is_cosmic_369(dr)

    # 369特殊色覆盖
    hex_code = COSMIC_369_COLORS[dr][0] if is_369 else color.hex_code

    return SemanticColorResult(
        keyword=keyword,
        dr=dr,
        wuxing=wuxing,
        color=color,
        fuse_level=fuse_level,
        is_369=is_369,
        hex_code=hex_code
    )


# ═══════════════════════════════════════════════════════════════════════════════
# 龍魂核心语义关键字库
# ═══════════════════════════════════════════════════════════════════════════════

LONGHUN_CORE_KEYWORDS = {
    # 铁律级（绝对熔断）
    "铁律": True,
    "熔断": True,
    "主权": True,
    "UID9622": True,
    "CONFIRM": True,
    "GPG": True,

    # 核心语义
    "龍魂": True,
    "龍芯": True,
    "龍": True,
    "三才": True,
    "五行": True,
    "五彩石": True,
    "曾老": True,
    "三色审计": True,
    "DNA": True,

    # 系统关键字
    "cnsh": False,
    "longhun": False,
    "persona": False,
    "skill": False,
    "hook": False,
    "notion": False,
    "memory": False,
    "audit": False,

    # 安全边界
    "token": False,
    "secret": False,
    "password": False,
    "key": False,
    "credential": False,
}


def analyze_all_keywords() -> List[SemanticColorResult]:
    """分析全部龍魂关键字"""
    results = []
    for kw, is_core in LONGHUN_CORE_KEYWORDS.items():
        results.append(analyze_keyword(kw, is_core))
    return results


# ═══════════════════════════════════════════════════════════════════════════════
# 熔断检测器
# ═══════════════════════════════════════════════════════════════════════════════

class FuseDetector:
    """
    熔断检测器 · 看颜色就知道是不是自己人

    原理：
    1. 预计算所有龍魂关键字的 dr+颜色 签名
    2. 新代码进来 → 扫描关键字 → 比对签名
    3. 颜色不对 = 被塞进来的野码 → 自动熔断
    """

    def __init__(self):
        self.signatures: Dict[str, SemanticColorResult] = {}
        self._build_signatures()

    def _build_signatures(self):
        """构建签名库"""
        for kw, is_core in LONGHUN_CORE_KEYWORDS.items():
            self.signatures[kw.lower()] = analyze_keyword(kw, is_core)

    def check_code(self, code: str) -> List[dict]:
        """
        检查代码中的关键字
        返回：可疑项列表
        """
        suspicious = []

        for kw, expected in self.signatures.items():
            if kw in code.lower():
                # 找到关键字在代码中的实际形态
                import re
                pattern = re.compile(re.escape(kw), re.IGNORECASE)
                matches = pattern.findall(code)

                for match in matches:
                    actual = analyze_keyword(match, expected.fuse_level.value >= 3)

                    # 比对：dr不一致 = 可疑
                    if actual.dr != expected.dr:
                        suspicious.append({
                            "keyword": match,
                            "expected_dr": expected.dr,
                            "actual_dr": actual.dr,
                            "expected_color": expected.hex_code,
                            "actual_color": actual.hex_code,
                            "fuse_level": expected.fuse_level.name,
                            "verdict": "⚠️ 签名不匹配·可能被篡改"
                        })

        return suspicious

    def should_fuse(self, code: str) -> Tuple[bool, str]:
        """
        是否应该熔断
        返回：(是否熔断, 原因)
        """
        suspicious = self.check_code(code)

        if not suspicious:
            return False, "✅ 代码签名验证通过"

        # 有铁律级可疑项 → 立即熔断
        for item in suspicious:
            if item["fuse_level"] == "ABSOLUTE":
                return True, f"🔴 铁律级关键字被篡改: {item['keyword']}"

        # 多个可疑项 → 熔断
        if len(suspicious) >= 3:
            return True, f"🔴 检测到{len(suspicious)}处签名异常"

        return False, f"🟡 检测到{len(suspicious)}处可疑·建议人工审核"


# ═══════════════════════════════════════════════════════════════════════════════
# 输出生成器
# ═══════════════════════════════════════════════════════════════════════════════

def generate_color_card_terminal():
    """生成终端彩色色卡"""
    print("\n" + "═" * 60)
    print("  五彩石色卡 · 龍魂语义视觉系统")
    print("═" * 60 + "\n")

    # 五行基础色
    print("【五行基础色】\n")
    for wuxing, color in WUCAISHI_PALETTE.items():
        print(f"  {color.ansi_bg}    {RESET} {color.name} ({wuxing.value}) {color.hex_code}")
        print(f"      {color.meaning}\n")

    # 369共振色
    print("\n【369宇宙共振色】\n")
    for dr, (hex_code, name) in COSMIC_369_COLORS.items():
        print(f"  dr={dr} → {name} {hex_code}")

    # 关键字分析
    print("\n" + "═" * 60)
    print("  龍魂关键字色卡")
    print("═" * 60 + "\n")

    results = analyze_all_keywords()
    for r in sorted(results, key=lambda x: x.dr):
        print(f"  {r.terminal_display()}")

    print("\n" + "═" * 60 + "\n")


def generate_color_card_json(output_path: Optional[str] = None) -> str:
    """生成JSON格式色卡"""
    results = analyze_all_keywords()

    output = {
        "meta": {
            "name": "五彩石色卡",
            "version": "1.0",
            "dna": "#龍芯⚡️2026-05-22-WUCAISHI-COLOR-ENGINE-v1.0",
        },
        "palette": {
            wx.value: {
                "name": color.name,
                "hex": color.hex_code,
                "rgb": color.rgb,
                "meaning": color.meaning,
            }
            for wx, color in WUCAISHI_PALETTE.items()
        },
        "cosmic_369": COSMIC_369_COLORS,
        "keywords": [r.to_dict() for r in results],
    }

    json_str = json.dumps(output, ensure_ascii=False, indent=2)

    if output_path:
        Path(output_path).write_text(json_str, encoding="utf-8")
        print(f"✅ 色卡已导出: {output_path}")

    return json_str


def generate_css_variables() -> str:
    """生成CSS变量（给前端用）"""
    lines = [":root {", "  /* 五彩石色卡 · 龍魂系统 */", ""]

    # 五行基础色
    lines.append("  /* 五行基础色 */")
    for wuxing, color in WUCAISHI_PALETTE.items():
        var_name = f"--wucai-{wuxing.name.lower()}"
        lines.append(f"  {var_name}: {color.hex_code};  /* {color.name} */")

    lines.append("")
    lines.append("  /* 369共振色 */")
    for dr, (hex_code, name) in COSMIC_369_COLORS.items():
        lines.append(f"  --cosmic-{dr}: {hex_code};  /* {name} */")

    lines.append("")
    lines.append("  /* 熔断级别色 */")
    lines.append("  --fuse-normal: #28a745;")
    lines.append("  --fuse-caution: #ffc107;")
    lines.append("  --fuse-critical: #fd7e14;")
    lines.append("  --fuse-absolute: #dc3545;")

    lines.append("}")

    return "\n".join(lines)


# ═══════════════════════════════════════════════════════════════════════════════
# CLI入口
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    import sys

    if len(sys.argv) < 2:
        # 默认：终端色卡
        generate_color_card_terminal()
        return

    cmd = sys.argv[1]

    if cmd == "json":
        output = sys.argv[2] if len(sys.argv) > 2 else None
        print(generate_color_card_json(output))

    elif cmd == "css":
        print(generate_css_variables())

    elif cmd == "check":
        if len(sys.argv) < 3:
            print("用法: python 五彩石色卡引擎.py check <文件路径>")
            return

        file_path = sys.argv[2]
        code = Path(file_path).read_text(encoding="utf-8")

        detector = FuseDetector()
        should_fuse, reason = detector.should_fuse(code)

        print(f"\n{'🔴 熔断' if should_fuse else '✅ 通过'}: {reason}\n")

        suspicious = detector.check_code(code)
        if suspicious:
            print("可疑项:")
            for item in suspicious:
                print(f"  - {item['keyword']}: {item['verdict']}")

    elif cmd == "analyze":
        keyword = sys.argv[2] if len(sys.argv) > 2 else "龍魂"
        result = analyze_keyword(keyword, keyword in LONGHUN_CORE_KEYWORDS)
        print(f"\n{result.terminal_display()}")
        print(f"  HEX: {result.hex_code}")
        print(f"  RGB: {result.color.rgb}")
        print(f"  寓意: {result.color.meaning}\n")

    else:
        print("用法:")
        print("  python 五彩石色卡引擎.py          # 显示终端色卡")
        print("  python 五彩石色卡引擎.py json     # 输出JSON")
        print("  python 五彩石色卡引擎.py css      # 输出CSS变量")
        print("  python 五彩石色卡引擎.py check <file>  # 检查文件")
        print("  python 五彩石色卡引擎.py analyze <关键字>  # 分析单个词")


if __name__ == "__main__":
    main()
