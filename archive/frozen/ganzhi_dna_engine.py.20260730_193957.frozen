#!/usr/bin/env python3
#龍芯⚡️丙午·癸未·丙申·申时·䷜坎-GANZHI-DNA-ENGINE-V1.0-P0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════════╗
║              干支时辰 DNA 引擎 v1.0 · 天干地支四柱·梅花易数起卦              ║
║              Ganzhi-SolarTerm DNA Engine · v∞ Format Generator           ║
╠══════════════════════════════════════════════════════════════════════════╣
║  DNA: #龍芯⚡️丙午·癸未·丙申·申时·䷜坎-GANZHI-DNA-ENGINE-V1.0-P0          ║
║  规格源: dna-gen v2.1（v∞ 推荐格式）                                     ║
║  铁律: 天干永为甲→癸·地支永为子→亥·卦名按模块德性定·哈希SHA256前8位          ║
╚══════════════════════════════════════════════════════════════════════════╝

用法:
    from bin.ganzhi_dna_engine import DNA生成

    dna = DNA生成(模块="API-TAIJI-ANT", 动作="ENGINE", 版本="V1.0", 级别="P0")
    # → '#龍芯⚡️丙午·癸未·丙申·申时·䷜坎-API-TAIJI-ANT-ENGINE-V1.0-P0'

    python3 bin/ganzhi_dna_engine.py          # 交互式生成
    python3 bin/ganzhi_dna_engine.py test     # 11条测试向量
    python3 bin/ganzhi_dna_engine.py now      # 输出当前时刻的干支四柱
"""

import hashlib
import time
from datetime import datetime, timedelta
from typing import Tuple, Optional, Dict

# ═══════════════════════════════════════════════════════════
# 天干地支基表 · L0 不可变
# ═══════════════════════════════════════════════════════════

十天干 = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
十二地支 = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
十二时辰 = ["子时", "丑时", "寅时", "卯时", "辰时", "巳时",
            "午时", "未时", "申时", "酉时", "戌时", "亥时"]

# 六十四卦（上卦·下卦对应）
八卦名 = ["乾", "兑", "离", "震", "巽", "坎", "艮", "坤"]  # 1→8
八卦象 = {"乾": "☰", "兑": "☱", "离": "☲", "震": "☳",
          "巽": "☴", "坎": "☵", "艮": "☶", "坤": "☷"}
八卦德 = {"乾": "天·健", "兑": "泽·悦", "离": "火·明", "震": "雷·动",
          "巽": "风·入", "坎": "水·流", "艮": "山·止", "坤": "地·藏"}

# 模块→卦德映射（按八宫API域协议第五章）
# 🔥 按关键词长度降序匹配——长关键词（具体模块）优先于短关键词（通用域）
模块宫映射: Dict[str, str] = {
    # 长关键词优先 — 具体模块匹配
    "CODEBUDDY": "乾", "ALIGNMENT": "乾", "CONSTITUTION": "乾",
    "GOVERNANCE": "乾", "PROTOCOL": "乾", "WHITE": "乾", "RULES": "乾",
    "REGISTER-MAIL": "坎", "DUALVIEW": "离", "DASHBOARD": "离",
    "SOVEREIGNTY": "艮", "PRIVACY": "艮",
    "INTEGRATION": "离", "PERSONA": "巽", "PHEROMONE": "巽",
    "SCHEDULE": "巽", "SOLDIER": "震", "MELTDOWN": "震",
    "SECURITY": "震", "CRAWLER": "坎", "STREAM": "坎",
    # 中等关键词
    "ARCHIVE": "坤", "BACKUP": "坤", "MEMORY": "坤",
    "SCOUT": "坎", "NOTIFY": "坎", "MAIL": "坎",
    "GUARD": "震", "MINOR": "震", "ALARM": "震", "DNA": "震",
    "QUEEN": "巽", "WORKER": "巽", "ROUTE": "巽",
    "TRUST": "兑", "ECOM": "兑", "ECO": "兑", "REGISTER": "兑",
    "NAMING": "乾", "MATH": "离", "AUDIT": "离", "TEST": "离",
    # 短关键词 — 最后匹配
    "MODEL": "巽", "DEPLOY": "巽", "TRAIN": "巽",
    "DATA": "坤", "SYNC": "坎", "TAIJI": "坎", "STATE": "离",
    "ENGINE": "坎", "RISK": "乾", "RULE": "乾", "GATE": "艮",
}
# 默认卦（未匹配模块用坎·水流）
默认卦 = "坎"

# 排序：按关键词长度降序（长关键词优先匹配）
_模块宫排序列表 = sorted(模块宫映射.keys(), key=len, reverse=True)


def _年干支(year: int) -> str:
    """计算年干支：2026→丙午"""
    base = year - 4  # 公元4年为甲子年
    gan = 十天干[base % 10]
    zhi = 十二地支[base % 12]
    return gan + zhi


def _月干支(year: int, month: int) -> Tuple[str, str]:
    """
    计算月干支（按节气，非农历月）
    返回 (月干支, 月份支)
    
    年上起月法（五虎遁）：
    甲己之年丙作首，乙庚之岁戊为头，
    丙辛必定寻庚起，丁壬壬位顺行流，
    若问戊癸何方发，甲寅之上好追求。
    """
    # 节气分界矩阵（近似日期，精确到日）
    # 立春≈2/4, 惊蛰≈3/6, 清明≈4/5, 立夏≈5/6, 芒种≈6/6,
    # 小暑≈7/7, 立秋≈8/8, 白露≈9/8, 寒露≈10/9, 立冬≈11/8,
    # 大雪≈12/7, 小寒≈1/6
    节气日 = [6, 4, 6, 5, 6, 6, 7, 8, 8, 9, 8, 7]  # 每月节气日（近似）
    
    # 确定月支
    idx = month - 1  # 0-based
    if idx == 0:  # 1月：小寒(1/6)后为丑月
        月支_idx = 0 if True else 1  # fixed: always 丑 for simplicity
    else:
        月支_idx = idx  # 2月→寅=2, 3月→卯=3, ...

    # 简化：阳历月份直接映射月支
    # 1丑 2寅 3卯 4辰 5巳 6午 7未 8申 9酉 10戌 11亥 12子
    月支映射 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 0]  # 地支索引
    月支_idx = 月支映射[month - 1]
    
    # 年上起月：确定寅月天干
    年干 = 十天干.index(_年干支(year)[0])
    # 甲己→丙寅(2,2), 乙庚→戊寅(4,2), 丙辛→庚寅(6,2),
    # 丁壬→壬寅(8,2), 戊癸→甲寅(0,2)
    寅月干映射 = [2, 4, 6, 8, 0, 2, 4, 6, 8, 0]  # 甲0→丙2, 乙1→戊4, ...
    寅月干 = 寅月干映射[年干]
    
    # 当前月天干 = 寅月干 + (月支_idx - 2)  （寅=索引2）
    offset = (月支_idx - 2) % 12  # 从寅月偏移
    月干 = (寅月干 + offset) % 10
    
    return 十天干[月干] + 十二地支[月支_idx], 十二地支[月支_idx]


def _日干支(year: int, month: int, day: int) -> str:
    """
    计算日干支（精确算法）
    公式: 基数 = (年尾+7)*5 + 15 + (年尾+19)/4（取整）
          日序 = 基数 + 该年第N天
          日干支序 = 日序 % 60
    """
    yy = year % 100  # 年尾两位
    # 日干支基数
    base = (yy + 7) * 5 + 15 + (yy + 19) // 4
    base %= 60
    
    # 闰年判定
    is_leap = (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)
    
    # 月累计天数
    月天数 = [31, 29 if is_leap else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    day_of_year = sum(月天数[:month - 1]) + day
    
    seq = (base + day_of_year) % 60
    gan = 十天干[(seq - 1) % 10]
    zhi = 十二地支[(seq - 1) % 12]
    return gan + zhi


def _时辰(hour: Optional[int] = None) -> str:
    """小时→时辰: 23-1子, 1-3丑, 3-5寅, 5-7卯, 7-9辰, 9-11巳,
       11-13午, 13-15未, 15-17申, 17-19酉, 19-21戌, 21-23亥"""
    if hour is None:
        hour = datetime.now().hour
    idx = ((hour + 1) // 2) % 12
    return 十二时辰[idx]


def _梅花易数起卦(content: str = "") -> str:
    """
    梅花易数起卦：取内容SHA256的首字节 mod 8 → 上卦·下卦
    返回卦象符号如 '䷜坎'
    """
    if content:
        h = hashlib.sha256(content.encode()).digest()
        upper = h[0] % 8  # 上卦
        lower = h[1] % 8  # 下卦
    else:
        # 无内容时用当前秒数
        t = int(time.time())
        upper = t % 8
        lower = (t // 60) % 8
    
    上卦名 = 八卦名[upper]
    下卦名 = 八卦名[lower]
    卦序 = upper * 8 + lower  # 0-63
    
    # 六十四卦名（上卦·下卦组合）
    六十四卦名 = [
        "䷀乾","䷫姤","䷌同人","䷉履","䷈小畜","䷍大有","䷊泰","䷋否",  # 乾上
        "䷠遯","䷞咸","䷢晋","䷎谦","䷽小过","䷵归妹","䷼中孚","䷻节",  # 兑上
        "䷤家人","䷰革","䷝离","䷶丰","䷣明夷","䷔噬嗑","䷀乾","䷕贲",  # 离上
        "䷩益","䷐随","䷔噬嗑","䷲震","䷟恒","䷧解","䷵归妹","䷽小过",  # 震上
        "䷓观","䷑蛊","䷱鼎","䷟恒","䷸巽","䷼中孚","䷺涣","䷴渐",  # 巽上
        "䷅讼","䷮困","䷿未济","䷧解","䷺涣","䷜坎","䷃蒙","䷦蹇",  # 坎上
        "䷠遯","䷞咸","䷃蒙","䷽小过","䷴渐","䷦蹇","䷳艮","䷎谦",  # 艮上
        "䷇比","䷬萃","䷢晋","䷏豫","䷓观","䷇比","䷖剥","䷁坤",  # 坤上
    ]
    return 六十四卦名[卦序]


def _模块起卦(模块: str) -> str:
    """按关键词长度降序匹配模块→卦德，长关键词优先"""
    模块_upper = 模块.upper()
    for keyword in _模块宫排序列表:  # 已按长度降序排列
        if keyword in 模块_upper:
            return 模块宫映射[keyword]
    return 默认卦


def _哈希8(内容: str) -> str:
    """SHA256前8位hex"""
    return hashlib.sha256(内容.encode()).hexdigest()[:8]


# ═══════════════════════════════════════════════════════════
# 主接口：DNA生成（v∞格式）
# ═══════════════════════════════════════════════════════════

def DNA生成(模块: str, 动作: str = "", 版本: str = "", 级别: str = "",
           timestamp: Optional[datetime] = None,
           内容锚点: str = "") -> str:
    """
    生成 v∞ 干支卦 DNA 追溯码

    Args:
        模块: 模块英文名（如 API-TAIJI-ANT）
        动作: 动作（如 ENGINE/MATH/PROTOCOL）
        版本: 版本号（如 V1.0）
        级别: 安全级别（如 P0/P0++）
        timestamp: 指定时间戳，默认当前时间
        内容锚点: 用于梅花易数起卦的内容

    Returns:
        v∞ DNA: #龍芯⚡️丙午·癸未·丙申·申时·䷜坎-API-TAIJI-ANT-ENGINE-V1.0-P0

    Example:
        >>> DNA生成(模块="API-TAIJI-ANT", 动作="ENGINE", 版本="V1.0", 级别="P0")
        '#龍芯⚡️丙午·癸未·丙申·申时·䷜坎-API-TAIJI-ANT-ENGINE-V1.0-P0'
    """
    if timestamp is None:
        timestamp = datetime.now()
    
    年 = _年干支(timestamp.year)
    月, _ = _月干支(timestamp.year, timestamp.month)
    日 = _日干支(timestamp.year, timestamp.month, timestamp.day)
    时 = _时辰(timestamp.hour)
    
    # 卦：优先梅花易数，fallback 模块德性起卦
    if 内容锚点:
        卦 = _梅花易数起卦(内容锚点)
    else:
        宫 = _模块起卦(模块)
        卦象 = 八卦象[宫]
        卦 = f"{卦象}{宫}"
    
    # 组装后缀
    后缀_部分 = [p for p in [模块, 动作, 版本, 级别] if p]
    后缀 = "-".join(后缀_部分)
    
    # 哈希8（对完整DNA主体内容取hash）
    dna_主体 = f"丙午·癸未·丙申·申时·{卦}-{后缀}"
    哈希 = _哈希8(dna_主体 + timestamp.isoformat())
    
    return f"#龍芯⚡️{年}·{月}·{日}·{时}·{卦}-{后缀}-{哈希}"


def DNA解析(dna: str) -> Dict:
    """解析 v∞ DNA 为结构化字典"""
    import re
    pattern = r"^#龍芯⚡️(\S+)·(\S+)·(\S+)·(\S+)·(\S+)-(.+)-([a-f0-9]{8})$"
    m = re.match(pattern, dna)
    if not m:
        return {"有效": False, "原因": "格式不符"}
    return {
        "有效": True,
        "年干支": m.group(1),
        "月干支": m.group(2),
        "日干支": m.group(3),
        "时辰": m.group(4),
        "卦象": m.group(5),
        "模块路径": m.group(6),
        "哈希8": m.group(7),
    }


def 当前干支() -> Dict:
    """返回当前时刻的干支四柱"""
    now = datetime.now()
    return {
        "时间": now.isoformat(),
        "年干支": _年干支(now.year),
        "月干支": _月干支(now.year, now.month)[0],
        "日干支": _日干支(now.year, now.month, now.day),
        "时辰": _时辰(now.hour),
        "v∞前缀": f"#龍芯⚡️{_年干支(now.year)}·{_月干支(now.year, now.month)[0]}·{_日干支(now.year, now.month, now.day)}·{_时辰(now.hour)}",
    }


# ═══════════════════════════════════════════════════════════
# 测试向量
# ═══════════════════════════════════════════════════════════

测试向量 = [
    # (模块, 动作, 版本, 级别, 期望特征)
    ("API-TAIJI-ANT", "ENGINE", "V1.0", "P0", "丙午·乙未"),
    ("REGISTER-MAIL", "NOTIFY", "V1.0", "P0", "坎"),
    ("MINOR-GUARD", "ENGINE", "V1.0", "P0", "震"),
    ("ECOM-TRUST", "ENGINE", "V1.0.1", "P0", "兑"),
    ("API-NAMING", "MATH", "V1.0", "P0", "乾"),
    ("REGISTER-MAIL", "MATH", "V1.0", "", "坎"),
    ("MINOR-GUARD", "MATH", "V1.0", "P0", "震"),
    ("STATE", "UNIFIED-ENTRY", "v1.3", "", "离"),
    ("CODEBUDDY", "ALIGNMENT-RULES", "V2.1", "FUSION", "乾"),
    ("GANZHI-DNA", "ENGINE", "V1.0", "P0", "震"),
    ("DUALVIEW", "V3-LANDING", "V1.0", "P0", "离"),
]


def run_tests() -> Tuple[int, int]:
    """运行测试向量，返回 (通过, 总数)"""
    通过 = 0
    ts = datetime(2026, 7, 21, 15, 30, 0)  # 固定时间戳用于测试
    
    for i, (模块, 动作, 版本, 级别, 特征) in enumerate(测试向量, 1):
        dna = DNA生成(模块=模块, 动作=动作, 版本=版本, 级别=级别, timestamp=ts)
        解析 = DNA解析(dna)
        
        ok = True
        errors = []
        
        if not 解析["有效"]:
            ok = False
            errors.append(f"DNA无效: {解析['原因']}")
        
        if 特征 not in dna:
            ok = False
            errors.append(f"缺特征'{特征}'")
        
        if 模块 not in dna:
            ok = False
            errors.append(f"缺模块'{模块}'")
        
        if not dna.startswith("#龍芯⚡️"):
            ok = False
            errors.append("缺前缀")
        
        # 验证哈希8长度
        if 解析["有效"] and len(解析["哈希8"]) != 8:
            ok = False
            errors.append(f"哈希非8位: {解析['哈希8']}")
        
        if ok:
            print(f"  T{i:02d} ✅ {dna}")
            通过 += 1
        else:
            print(f"  T{i:02d} ❌ {dna}")
            for e in errors:
                print(f"       → {e}")
    
    return 通过, len(测试向量)


# ═══════════════════════════════════════════════════════════
# CLI入口
# ═══════════════════════════════════════════════════════════

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "test":
        print("=" * 60)
        print("  干支时辰 DNA 引擎 · v∞ 测试向量")
        print("=" * 60)
        ok, total = run_tests()
        print("-" * 60)
        if ok == total:
            print(f"  🟢 {ok}/{total} 全绿")
        else:
            print(f"  🔴 {ok}/{total} 通过")
        sys.exit(0 if ok == total else 1)

    elif len(sys.argv) > 1 and sys.argv[1] == "now":
        info = 当前干支()
        print(f"当前干支: {info['v∞前缀']}")
        print(f"年: {info['年干支']}  月: {info['月干支']}  日: {info['日干支']}  时辰: {info['时辰']}")

    elif len(sys.argv) > 1 and sys.argv[1] == "gen":
        模块 = sys.argv[2] if len(sys.argv) > 2 else "MODULE"
        动作 = sys.argv[3] if len(sys.argv) > 3 else "ACTION"
        版本 = sys.argv[4] if len(sys.argv) > 4 else "V1.0"
        级别 = sys.argv[5] if len(sys.argv) > 5 else ""
        dna = DNA生成(模块=模块, 动作=动作, 版本=版本, 级别=级别)
        print(dna)

    else:
        # 交互模式
        info = 当前干支()
        print(f"干支时辰 DNA 引擎 v1.0")
        print(f"当前: {info['v∞前缀']}")
        print()
        
        模块 = input("模块名: ").strip()
        动作 = input("动作: ").strip()
        版本 = input("版本 (默认V1.0): ").strip() or "V1.0"
        级别 = input("级别 (默认P0): ").strip() or "P0"
        
        dna = DNA生成(模块=模块, 动作=动作, 版本=版本, 级别=级别)
        print(f"\n{'='*60}")
        print(f"  {dna}")
        print(f"{'='*60}")
        
        解析 = DNA解析(dna)
        if 解析["有效"]:
            print(f"  年干支: {解析['年干支']}  月干支: {解析['月干支']}")
            print(f"  日干支: {解析['日干支']}  时辰: {解析['时辰']}")
            print(f"  卦象: {解析['卦象']}  哈希: {解析['哈希8']}")
