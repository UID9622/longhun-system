#!/usr/bin/env python3
#龍芯⚡️丙午·丙申·癸酉·庚申·临-LH_ANTI_COUNTERFEIT-v1.0-2a5ce56d
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════════╗
║       龍魂打假雷達 · 物理锚点向量化 + DNA登记册联动 v1.0                ║
║       LongHun Anti-Counterfeit Radar · Physical Anchor to DNA           ║
╠══════════════════════════════════════════════════════════════════════════╣
║  底座: lh_unified_dna_registry.py (Merkle根哈希·一世一双人)             ║
║  增强: 千问"物理特征→数字指纹"概念 + 龍魂向量化相似度匹配               ║
║  铁律: 物理特征永不明文存储 · 哈希可验证 · 相似度可查 · 不可篡改       ║
║  📇 身份 · 联系 · 支持 → assets/PUBLIC_IDENTITY.md                      ║
╚══════════════════════════════════════════════════════════════════════════╝

核心理念（千问贡献 + 龍魂加固）：
  千问: "信息归拢 + 唯一性验证 = 降维打假" → 方向正确 ✅
  龍魂增强:
    1. 物理特征向量化而非字符串拼接（抗微小变化）
    2. 相似度匹配而非二值判定（0-100% 置信度）
    3. 物理特征仅存哈希·永不明文（隐私保护）
    4. 挂载到统一DNA Merkle树（一世一双人·不可篡改）
    5. 三色审计 + append-only日志（每步可追溯）
    6. 反时光回溯检测（登记时间 > 声称购入时间 → 假货）

用法:
  python3 bin/lh_anti_counterfeit.py register <uid> <资产类型> <序列号> --traits 特征JSON
  python3 bin/lh_anti_counterfeit.py verify <uid> <资产类型> <序列号> --traits 特征JSON
  python3 bin/lh_anti_counterfeit.py scan-market <序列号> --traits 特征JSON
  python3 bin/lh_anti_counterfeit.py collision-report <序列号>
  python3 bin/lh_anti_counterfeit.py status

资产类型（与 lh_unified_dna_registry.py 共享）:
  watch 手表 | vehicle 车辆 | painting 画作 | antique 古董
  luxury_bag 奢侈包 | jewelry 珠宝 | wine 名酒 | collectible 收藏品
"""

import hashlib
import json
import sys
import time
import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict, field
from datetime import datetime, timezone

# ═══════════════════════════════════════════════════════════
# L0 常量 · 焊死
# ═══════════════════════════════════════════════════════════

打假数据目录 = Path.home() / ".龍魂" / "anti_counterfeit"
打假数据目录.mkdir(parents=True, exist_ok=True)

# 物理特征权重表 — 不同特征的可信度不同
# 权重越高 = 越难伪造 = 判别力越强
物理特征权重 = {
    # 手表类
    "机芯编号":       0.25,  # 几乎不可伪造
    "机芯打磨纹路":   0.20,  # 高度专业
    "表壳材质":       0.15,  # 可检测
    "表盘纹理":       0.12,  # 微观特征
    "表带编号":       0.08,  # 可更换
    "保卡编号":       0.10,  # 官方记录
    "购买价格":       0.05,  # 辅助参考
    "特定划痕/磨损":  0.05,  # 唯一但会变化

    # 奢侈包类
    "五金件编号":     0.22,
    "皮质纹理":       0.20,
    "缝线密度":       0.15,
    "内衬编号":       0.13,
    "防尘袋编号":     0.08,
    "购买小票编号":   0.12,
    "特定使用痕迹":   0.10,

    # 画作/古董类
    "作者签名位置":   0.20,
    "画布纹理":       0.18,
    "颜料光谱特征":   0.22,
    "装裱编号":       0.10,
    "流传记录":       0.15,
    "专家鉴定编号":   0.15,

    # 通用默认
    "序列号":         0.30,
    "材质":           0.20,
    "工艺":           0.20,
    "尺寸":           0.15,
    "重量":           0.15,
}

# 三色阈值（打假场景 · 更严格）
# 打假场景下 🟡 阈值更高，宁可错杀不可放过
打假三色阈值 = {
    "🟢": 0.85,   # 相似度 ≥ 85% → 可信真品
    "🟡": 0.60,   # 60% ≤ 相似度 < 85% → 可疑·需人工
    "🔴": 0.0,    # < 60% → 高度疑似假货
}


# ═══════════════════════════════════════════════════════════
# 核心数据结构
# ═══════════════════════════════════════════════════════════

@dataclass
class 物理锚点记录:
    """一条资产的物理特征向量化记录"""
    资产类型: str
    序列号哈希: str           # SHA256(序列号) → 前16位 · 永不明文
    特征向量哈希: str          # SHA256(特征向量JSON) → 前16位
    特征权重列表: Dict[str, float]  # {"机芯编号": 0.25, "表壳材质": 0.15, ...}
    特征值哈希: Dict[str, str]     # {"机芯编号": SHA256(具体值)[:8], ...}
    登记时间: str
    登记干支: str
    DNA码: str                # 与统一登记册联动的DNA
    主DNA哈希: str            # 所属人的主DNA（Merkle根）
    验证状态: str             # 已验证/待验证/争议中
    备注哈希: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "物理锚点记录":
        return cls(**d)


@dataclass
class 打假报告:
    """一次验证操作产生的完整报告"""
    报告时间: str
    目标序列号哈希: str
    匹配结果: str              # 🟢真品 🟡可疑 🔴疑似假货
    相似度: float              # 0.0 ~ 1.0
    匹配到的DNA: str           # 如果匹配到已登记真品
    匹配到的特征: List[str]    # 匹配了哪些特征
    未匹配的特征: List[str]    # 哪些特征对不上
    权重加权分: float          # 按权重的加权得分
    DNA码: str
    建议: str                  # 下一步行动建议


# ═══════════════════════════════════════════════════════════
# 核心算法
# ═══════════════════════════════════════════════════════════

def 哈希值(原始值: str) -> str:
    """SHA256 哈希，返回前 16 位。原始值永不明文存储。"""
    return hashlib.sha256(原始值.encode()).hexdigest()[:16]


def 特征值短哈希(原始值: str) -> str:
    """特征值哈希前8位，用于比对时不暴露原文"""
    return hashlib.sha256(原始值.encode()).hexdigest()[:8]


def 向量化特征(
    资产类型: str,
    特征字典: Dict[str, str]
) -> Tuple[Dict[str, float], Dict[str, str], str]:
    """
    将物理特征转为向量化表示。
    千问原始做法: SHA256("序列号" + "物理特征字符串拼接")
    问题: 标点变了就对不上 → "60万入手/钛金属" vs "60万入手,钛金属" = 完全不同hash

    龍魂增强: 逐特征独立哈希 + 权重分配 + 整体向量哈希
    - 每个特征独立hash，比对时不依赖字符串顺序
    - 权重按资产类型自动分配
    - 整体向量哈希用于快速去重
    """
    权重结果: Dict[str, float] = {}
    值哈希结果: Dict[str, str] = {}

    for 特征名, 特征值 in 特征字典.items():
        # 查权重表，找不到用默认0.10
        权重 = 物理特征权重.get(特征名, 0.10)
        权重结果[特征名] = 权重
        值哈希结果[特征名] = 特征值短哈希(特征值)

    # 整体向量哈希（用于快速索引）
    向量原始串 = json.dumps({"type": 资产类型, "fields": sorted(特征字典.keys())}, sort_keys=True)
    向量哈希 = 哈希值(向量原始串)

    return 权重结果, 值哈希结果, 向量哈希


def 计算特征相似度(
    登记特征: Dict[str, str],    # 已登记的: {特征名: 哈希值}
    目标特征: Dict[str, str],    # 待验证的: {特征名: 原始值}
    权重表: Dict[str, float]     # 各特征权重
) -> Tuple[float, List[str], List[str], float]:
    """
    计算两组物理特征的加权相似度。

    算法:
      similarity = Σ(matched_weight) / Σ(total_weight)

    对于每个已登记的特征名:
      - 如果目标也提供了该特征 → 值完全匹配(+权重) / 不匹配(+0)
      - 如果目标未提供该特征 → 不算分(不扣也不加)

    返回: (相似度, 匹配的特征名列表, 未匹配的特征名列表, 加权原始分)
    """
    if not 登记特征 or not 权重表:
        return 0.0, [], list(登记特征.keys()), 0.0

    总权重 = sum(权重表.values())
    if 总权重 == 0:
        return 0.0, [], list(登记特征.keys()), 0.0

    匹配权重和: float = 0.0
    匹配特征: List[str] = []
    未匹配特征: List[str] = []

    for 特征名, 登记哈希 in 登记特征.items():
        if 特征名 in 目标特征:
            目标哈希 = 特征值短哈希(目标特征[特征名])
            if 目标哈希 == 登记哈希:
                匹配权重和 += 权重表.get(特征名, 0.10)
                匹配特征.append(特征名)
            else:
                未匹配特征.append(f"{特征名}(值不匹配)")
        else:
            # 目标未提供该特征，不扣分
            pass

    # 检查目标多提供了哪些已登记没有的特征
    for 特征名 in 目标特征:
        if 特征名 not in 登记特征:
            未匹配特征.append(f"{特征名}(已登记无此特征)")

    相似度 = 匹配权重和 / 总权重 if 总权重 > 0 else 0.0
    return min(相似度, 1.0), 匹配特征, 未匹配特征, 匹配权重和


def 反时光回溯检查(登记时间_str: str, 声称购入时间: Optional[str]) -> Tuple[bool, str]:
    """
    如果"真品"登记时间晚于声称的购入时间 → 不可能 → 假货
    真品不可能在登记之后才被"发现"登记
    """
    if not 声称购入时间:
        return True, "未提供购入时间，跳过时光回溯检查"

    try:
        登记时间 = datetime.fromisoformat(登记时间_str.replace("Z", "+00:00"))
        购入时间 = datetime.fromisoformat(声称购入时间)
    except (ValueError, TypeError):
        return True, f"时间格式异常: 登记={登记时间_str} 购入={声称购入时间}"

    if 购入时间 < 登记时间:
        return False, (
            f"🔴 时光回溯异常！声称购入于 {声称购入时间}，"
            f"但真品登记于 {登记时间_str}。"
            f"真品不可能在登记之后才被人买走。"
        )
    return True, "时光回溯检查通过 ✅"


# ═══════════════════════════════════════════════════════════
# CRUD 操作
# ═══════════════════════════════════════════════════════════

def 载入打假库() -> Dict[str, 物理锚点记录]:
    """从本地加载全部打假记录"""
    idx_path = 打假数据目录 / "index.json"
    if not idx_path.exists():
        return {}
    with open(idx_path, "r", encoding="utf-8") as f:
        raw = json.load(f)
    return {k: 物理锚点记录.from_dict(v) for k, v in raw.items()}


def 保存打假库(数据库: Dict[str, 物理锚点记录]):
    """保存打假库（append-only语义·先备份）"""
    idx_path = 打假数据目录 / "index.json"
    if idx_path.exists():
        backup = 打假数据目录 / f"index.{int(time.time())}.json"
        idx_path.rename(backup)
    with open(idx_path, "w", encoding="utf-8") as f:
        json.dump({k: v.to_dict() for k, v in 数据库.items()}, f, ensure_ascii=False, indent=2)


def 获取干支() -> str:
    """获取当前农历干支"""
    try:
        项目根 = Path(__file__).parent.parent
        sys.path.insert(0, str(项目根 / "calendar-context-logger"))
        from calendar_core import LunarEngine  # type: ignore[import-untyped]
        g = LunarEngine().get_ganzhi()
        return f"{g['year_zhu']}·{g['month_zhu']}·{g['day_zhu']}·{g['hour_zhu']}"
    except Exception:
        return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S")


def 登记真品(
    uid: str,
    资产类型: str,
    序列号: str,
    特征字典: Dict[str, str],
    主DNA哈希: str = "",
    备注: str = "",
) -> Tuple[bool, str, Optional[str]]:
    """
    登记一件真品到打假雷达。
    步骤:
      1. 序列号 → SHA256哈希（永不明文）
      2. 物理特征 → 逐特征独立哈希 + 权重分配
      3. 检查冲突（同序列号已有不同特征 = 假警报）
      4. 写入 append-only 数据库
      5. 建议同步到 unified_dna_registry
    """
    数据库 = 载入打假库()

    序列号哈希 = 哈希值(序列号)
    权重表, 值哈希表, 向量哈希 = 向量化特征(资产类型, 特征字典)
    备注哈希 = hashlib.sha256(备注.encode()).hexdigest()[:16] if 备注 else ""

    # 冲突检测：同序列号但不同特征 = 潜在假货
    if 序列号哈希 in 数据库:
        已有记录 = 数据库[序列号哈希]
        if 已有记录.特征向量哈希 != 向量哈希:
            return False, (
                f"🔴 冲突警报！序列号 {序列号[:4]}*** 已登记，但物理特征向量不匹配。\n"
                f"   已有DNA: {已有记录.DNA码}\n"
                f"   登记时间: {已有记录.登记时间}\n"
                f"   这可能是: (1)序列号被克隆 (2)同一物品两次登记特征描述不同\n"
                f"   如确认是真品，请用不同描述重新登记；或先 resolve 冲突。"
            ), None

    # 反时光回溯（第一次登记没有历史可回溯，跳过）

    干支 = 获取干支()
    时间戳 = datetime.now(timezone.utc).isoformat() + "Z"
    dna码 = hashlib.sha256(f"{uid}:{资产类型}:{序列号哈希}:{时间戳}".encode()).hexdigest()[:12]

    记录 = 物理锚点记录(
        资产类型=资产类型,
        序列号哈希=序列号哈希,
        特征向量哈希=向量哈希,
        特征权重列表=权重表,
        特征值哈希=值哈希表,
        登记时间=时间戳,
        登记干支=干支,
        DNA码=dna码,
        主DNA哈希=主DNA哈希,
        验证状态="已验证",
        备注哈希=备注哈希,
    )

    数据库[序列号哈希] = 记录
    保存打假库(数据库)

    return True, (
        f"✅ 真品 [{资产类型}] 已登记\n"
        f"   序列号哈希: {序列号哈希}\n"
        f"   特征向量: {向量哈希}\n"
        f"   DNA: {dna码}\n"
        f"   主DNA: {主DNA哈希 or '(未关联·建议同步到统一登记册)'}"
    ), dna码


def 验证物品(
    资产类型: str,
    序列号: str,
    特征字典: Dict[str, str],
    声称购入时间: Optional[str] = None,
) -> 打假报告:
    """
    打假核心：验证市面上出现的物品是否与已登记真品匹配。

    判定流程:
      1. 查序列号是否已登记
         - 未登记 → 🟡 未知物品
         - 已登记 → 继续
      2. 物理特征加权相似度计算
         - ≥ 85% → 🟢 真品（高置信）
         - 60-85% → 🟡 可疑（部分特征对不上）
         - < 60% → 🔴 疑似假货（序列号克隆）
      3. 时光回溯检查
         - 购入时间早于登记时间 → 🔴 不可能
      4. 生成完整打假报告
    """
    数据库 = 载入打假库()
    序列号哈希 = 哈希值(序列号)
    报告时间 = datetime.now(timezone.utc).isoformat() + "Z"

    # 情况1：序列号未登记
    if 序列号哈希 not in 数据库:
        return 打假报告(
            报告时间=报告时间,
            目标序列号哈希=序列号哈希,
            匹配结果="🟡",
            相似度=0.0,
            匹配到的DNA="",
            匹配到的特征=[],
            未匹配的特征=[f"序列号 {序列号[:4]}*** 未在打假库中登记"],
            权重加权分=0.0,
            DNA码="",
            建议="⚠️ 未知物品 · 序列号未登记。可能是未登记真品，也可能是纯假货。建议要求卖家提供购买凭证。",
        )

    登记记录 = 数据库[序列号哈希]

    # 计算相似度
    相似度, 匹配特征, 未匹配特征, 加权分 = 计算特征相似度(
        登记记录.特征值哈希,
        特征字典,
        登记记录.特征权重列表,
    )

    # 时光回溯检查
    时光ok, 时光信息 = 反时光回溯检查(登记记录.登记时间, 声称购入时间)
    if not 时光ok:
        相似度 = min(相似度, 0.50)  # 时光异常强制降分
        未匹配特征.append(时光信息)

    # 判定
    if not 时光ok:
        # 时光回溯异常 = 立即🔴，不管相似度
        结果 = "🔴"
        建议 = 时光信息
    elif 相似度 >= 打假三色阈值["🟢"]:
        结果 = "🟢"
        建议 = (
            f"✅ 验证通过 · 高置信度真品 ({相似度*100:.1f}%)\n"
            f"   主DNA: {登记记录.主DNA哈希}\n"
            f"   该物品与登记记录物理特征高度吻合。"
        )
    elif 相似度 >= 打假三色阈值["🟡"]:
        结果 = "🟡"
        建议 = (
            f"🟡 可疑物品 · 相似度 {相似度*100:.1f}%\n"
            f"   序列号匹配，但部分物理特征对不上: {', '.join(未匹配特征[:5])}\n"
            f"   建议: 要求卖家提供更多物理特征照片/视频，或线下实物鉴定。"
        )
    else:
        # 相似度 < 60% 但序列号匹配 → 典型序列号克隆假货
        结果 = "🔴"
        建议 = (
            f"🔴 高度疑似假货！相似度仅 {相似度*100:.1f}%\n"
            f"   序列号 {序列号[:4]}*** 与已登记真品相同，\n"
            f"   但物理特征严重不匹配: {', '.join(未匹配特征[:5])}\n"
            f"   这是典型的「序列号克隆 + 粗制假货」。\n"
            f"   真品DNA: {登记记录.DNA码}"
        )

    return 打假报告(
        报告时间=报告时间,
        目标序列号哈希=序列号哈希,
        匹配结果=结果,
        相似度=round(相似度, 4),
        匹配到的DNA=登记记录.主DNA哈希,
        匹配到的特征=匹配特征,
        未匹配的特征=未匹配特征,
        权重加权分=round(加权分, 4),
        DNA码=登记记录.DNA码,
        建议=建议,
    )


def 市场扫描(序列号: str, 特征字典: Dict[str, str]) -> 打假报告:
    """
    扫市场：给定一个物品，看它是不是假货。
    等价于 验证物品() 但面向"买家在二手市场看到的东西"
    """
    # 从特征中推断资产类型
    资产类型 = "watch"  # 默认，CLI层可覆盖
    return 验证物品(资产类型, 序列号, 特征字典)


def 碰撞报告(序列号: str) -> Dict[str, Any]:
    """
    查某个序列号是否已被登记，是否有冲突记录。
    用于"买之前先扫一下"
    """
    数据库 = 载入打假库()
    序列号哈希 = 哈希值(序列号)

    if 序列号哈希 not in 数据库:
        return {
            "序列号": f"{序列号[:4]}***",
            "状态": "未登记",
            "风险": "🟡 未知 · 可能是真品也可能不是",
            "建议": "无法验证归属。建议要求卖家提供可验证的购买证明。",
        }

    记录 = 数据库[序列号哈希]
    return {
        "序列号": f"{序列号[:4]}***",
        "序列号哈希": 序列号哈希,
        "状态": "已登记",
        "登记时间": 记录.登记时间,
        "DNA": 记录.DNA码,
        "主DNA": 记录.主DNA哈希 or "(未关联)",
        "验证状态": 记录.验证状态,
        "风险": "🟢 已知真品已登记 · 如市面上有同序列号物品 → 必然有假",
        "建议": (
            "此序列号已绑定到特定物理特征。市面上任何自称此序列号的物品，"
            "必须通过物理特征验证才可能是真品。"
        ),
    }


def 打假库状态() -> Dict[str, Any]:
    """打假雷达库整体状态"""
    数据库 = 载入打假库()
    return {
        "总登记数": len(数据库),
        "数据库路径": str(打假数据目录 / "index.json"),
        "资产类型分布": _统计类型分布(数据库),
        "最近登记": _最近登记(数据库),
    }


def _统计类型分布(数据库: Dict[str, 物理锚点记录]) -> Dict[str, int]:
    dist: Dict[str, int] = {}
    for r in 数据库.values():
        dist[r.资产类型] = dist.get(r.资产类型, 0) + 1
    return dist


def _最近登记(数据库: Dict[str, 物理锚点记录], n: int = 5) -> List[Dict[str, str]]:
    排序 = sorted(数据库.values(), key=lambda r: r.登记时间, reverse=True)
    return [
        {"类型": r.资产类型, "DNA": r.DNA码, "时间": r.登记时间}
        for r in 排序[:n]
    ]


# ═══════════════════════════════════════════════════════════
# 与统一DNA登记册的桥接
# ═══════════════════════════════════════════════════════════

def 同步到统一登记册(uid: str, 资产类型: str, 序列号: str, 标签: Optional[List[str]] = None) -> Tuple[bool, str]:
    """
    将打假雷达中的资产同步到统一DNA登记册。
    这样一件物理资产的DNA就会进入人的Merkle树。
    """
    try:
        sys.path.insert(0, str(Path(__file__).parent))
        from lh_unified_dna_registry import 注册资产, 资产类型表  # type: ignore[import-untyped]

        if 资产类型 not in 资产类型表:
            return False, f"资产类型 [{资产类型}] 不在统一登记册中。可用: {list(资产类型表.keys())[:10]}..."

        ok, msg, dna = 注册资产(uid, 资产类型, 序列号, 标签 or ["打假雷达"])
        return ok, msg
    except ImportError as e:
        return False, f"无法导入统一登记册: {e}"
    except Exception as e:
        return False, f"同步失败: {e}"


# ═══════════════════════════════════════════════════════════
# CLI 入口
# ═══════════════════════════════════════════════════════════

def _print_banner():
    print("""
╔══════════════════════════════════════════════════════╗
║  🛡️  龍魂打假雷達 · Anti-Counterfeit Radar v1.0     ║
║  物理锚点 → 向量化 → 相似度匹配 → DNA锚定            ║
║  方向:信息归拢+唯一性验证=降维打假 (千问v1 + 龍魂加固) ║
╚══════════════════════════════════════════════════════╝
""")


def _print_usage():
    print("用法:")
    print("  python3 bin/lh_anti_counterfeit.py register <uid> <资产类型> <序列号> <特征JSON>")
    print("  python3 bin/lh_anti_counterfeit.py verify <uid> <资产类型> <序列号> <特征JSON> [购入时间]")
    print("  python3 bin/lh_anti_counterfeit.py scan <序列号> <特征JSON> [资产类型]")
    print("  python3 bin/lh_anti_counterfeit.py report <序列号>")
    print("  python3 bin/lh_anti_counterfeit.py sync <uid> <资产类型> <序列号> [标签...]")
    print("  python3 bin/lh_anti_counterfeit.py status")
    print()
    print("示例:")
    print('  python3 bin/lh_anti_counterfeit.py register UID9622 watch "AP-26400-TI-8888" \\')
    print('    \'{"机芯编号":"Cal.3126/3840","表壳材质":"钛金属","机芯打磨纹路":"日内瓦波纹","保卡编号":"AP-2020-8888"}\'')
    print()
    print('  # 扫二手市场（买家视角）')
    print('  python3 bin/lh_anti_counterfeit.py scan "AP-26400-TI-8888" \\')
    print('    \'{"表壳材质":"廉价合金","机芯打磨纹路":"粗糙倒角","机芯编号":"对不上"}\' watch')
    print()
    print('  # 先查登记状态再决定（碰撞报告）')
    print('  python3 bin/lh_anti_counterfeit.py report "AP-26400-TI-8888"')


def _特征json解析(raw: str) -> Dict[str, str]:
    """解析特征JSON"""
    d = json.loads(raw)
    return {k: str(v) for k, v in d.items()}


if __name__ == "__main__":
    if len(sys.argv) < 2:
        _print_banner()
        _print_usage()
        sys.exit(0)

    cmd = sys.argv[1]

    if cmd == "register" and len(sys.argv) >= 6:
        _print_banner()
        uid = sys.argv[2]
        资产类型 = sys.argv[3]
        序列号 = sys.argv[4]
        特征字典 = _特征json解析(sys.argv[5])
        ok, msg, dna = 登记真品(uid, 资产类型, 序列号, 特征字典)
        print(msg)
        if dna:
            print(f"\n💡 建议同步到统一DNA登记册:")
            print(f"   python3 bin/lh_anti_counterfeit.py sync {uid} {资产类型} \"{序列号}\"")
        sys.exit(0 if ok else 1)

    elif cmd == "verify" and len(sys.argv) >= 6:
        _print_banner()
        uid = sys.argv[2]
        资产类型 = sys.argv[3]
        序列号 = sys.argv[4]
        特征字典 = _特征json解析(sys.argv[5])
        购入时间 = sys.argv[6] if len(sys.argv) >= 7 else None
        报告 = 验证物品(资产类型, 序列号, 特征字典, 购入时间)
        print(f"  序列号哈希: {报告.目标序列号哈希}")
        print(f"  匹配结果: {报告.匹配结果}")
        print(f"  相似度: {报告.相似度*100:.1f}%")
        print(f"  匹配特征: {', '.join(报告.匹配到的特征) if 报告.匹配到的特征 else '(无)'}")
        print(f"  未匹配: {', '.join(报告.未匹配的特征)}")
        print(f"  关联DNA: {报告.匹配到的DNA or '(未关联)'}")
        print(f"  判决DNA: {报告.DNA码}")
        print(f"\n  📋 {报告.建议}")
        sys.exit(0 if 报告.匹配结果 == "🟢" else 1)

    elif cmd == "scan" and len(sys.argv) >= 4:
        _print_banner()
        序列号 = sys.argv[2]
        特征字典 = _特征json解析(sys.argv[3])
        资产类型 = sys.argv[4] if len(sys.argv) >= 5 else "watch"
        报告 = 验证物品(资产类型, 序列号, 特征字典)
        print(f"  🔍 扫描: {资产类型} · 序列号 {序列号[:4]}***")
        print(f"  结果: {报告.匹配结果}  相似度: {报告.相似度*100:.1f}%")
        print(f"  {'✅' if 报告.匹配到的特征 else '❌'} 匹配: {', '.join(报告.匹配到的特征) if 报告.匹配到的特征 else '无'}")
        print(f"  {'❌' if 报告.未匹配的特征 else ''} 不匹配: {', '.join(报告.未匹配的特征)}")
        print(f"\n  {报告.建议}")

    elif cmd == "report" and len(sys.argv) >= 3:
        _print_banner()
        序列号 = sys.argv[2]
        r = 碰撞报告(序列号)
        print(f"  序列号: {r['序列号']}")
        print(f"  状态: {r['状态']}")
        print(f"  风险: {r['风险']}")
        if "DNA" in r:
            print(f"  DNA: {r['DNA']}")
        print(f"\n  {r['建议']}")

    elif cmd == "sync" and len(sys.argv) >= 5:
        _print_banner()
        uid = sys.argv[2]
        资产类型 = sys.argv[3]
        序列号 = sys.argv[4]
        标签 = sys.argv[5:] if len(sys.argv) > 5 else []
        ok, msg = 同步到统一登记册(uid, 资产类型, 序列号, 标签)
        print(f"  {'✅' if ok else '❌'} {msg}")

    elif cmd == "status":
        _print_banner()
        s = 打假库状态()
        print(f"  总登记: {s['总登记数']} 件")
        print(f"  数据库: {s['数据库路径']}")
        if s['资产类型分布']:
            print(f"  类型分布:")
            for t, n in s['资产类型分布'].items():
                print(f"    {t}: {n}件")
        if s['最近登记']:
            print(f"  最近登记:")
            for r in s['最近登记']:
                print(f"    [{r['类型']}] DNA:{r['DNA']} @ {r['时间']}")

    else:
        _print_usage()
        sys.exit(1)

# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬AK7X-339P
# DNA: #龍芯⚡️丙午·乙未·丙辰·午时·乾-ANTI-COUNTERFEIT-v1.0-8F3A2C17
