#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""
╔══════════════════════════════════════════════════════════════════════════╗
║     龍魂·五行计算器API桥接 v1.0 — 习惯指纹↔五行流场正式对接                    ║
║     Wuxing Calculator API Bridge · Habit Fingerprint ↔ Five Elements     ║
╠══════════════════════════════════════════════════════════════════════════╣
║  DNA: #龍芯⚡️丙午·乙未·癸未·丙辰·䷓观-WUXING-API-BRIDGE-v1.0                  ║
║  协议: 人物行为DNA不动点切割协议 v1.0 §7 五行计算器接驳 + §11 候补清单④         ║
║  功能: ① 习惯指纹→五行属性（数字根映射）                                        ║
║        ② RobotScore→五行流场健康度判定                                         ║
║        ③ 五行平衡度→人物画像（偏科/平衡型）                                     ║
║        ④ 与 cnsh/core/api_wuxing.py HTTP API 对接                             ║
║  铁律: 本地计算优先·密文不出设备·API仅为内部微服务                                ║
╚══════════════════════════════════════════════════════════════════════════╝

用法:
    from bin.lh_wuxing_api_bridge import 五行桥接器
    桥 = 五行桥接器()
    结果 = 桥.习惯指纹转五行流场("文本内容")

直接运行:
    python3 bin/lh_wuxing_api_bridge.py
"""

import json
import hashlib
import math
import urllib.request
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Any
from bin.lh_habit_fingerprint import 习惯指纹提取器


# ═══════════════════════════════════════════════════════════
# 数字根→五行映射（与 api_wuxing.py v3.3 对齐）
# 河图定则: 1,6=水 / 2,7=火 / 3,8=木 / 4,9=金 / 5,0=土
# ═══════════════════════════════════════════════════════════

数字根_五行 = {1: "水", 2: "火", 3: "木", 4: "金", 5: "土", 6: "水", 7: "火", 8: "木", 9: "金", 0: "土"}

五行相生 = {"金": "水", "水": "木", "木": "火", "火": "土", "土": "金"}
五行相克 = {"金": "木", "木": "土", "土": "水", "水": "火", "火": "金"}

# 五行→语义映射（用于文本内容分析）
五行语义词库 = {
    "金": ["金", "铁", "钢", "锁", "刚", "锋", "锐", "坚", "硬", "决", "断", "止"],
    "木": ["木", "林", "森", "树", "生", "春", "青", "萌", "发", "创", "展", "长"],
    "水": ["水", "河", "海", "流", "润", "冬", "黑", "深", "藏", "智", "柔", "寒"],
    "火": ["火", "炎", "焰", "热", "光", "夏", "红", "明", "动", "燃", "暖", "烈"],
    "土": ["土", "地", "山", "石", "城", "中", "黄", "重", "稳", "厚", "载", "实"],
}

# 三色审计判定
三色判定 = {3: "🔴", 6: "🟡", 9: "🔴"}


@dataclass
class 五行流场报告:
    """五行完整流场分析报告"""
    文本长度: int
    数字根: int
    五行属性: str
    三色审计: str
    五行向量: Dict[str, float]
    平衡度: float  # 0=偏科 1=完美平衡
    主导五行: str
    最弱五行: str
    流场走向: str  # 相生/相克描述
    RobotScore兼容: float  # 集成到RobotScore的五行偏置因子
    # §7 habit_to_wuxing 返回格式
    habit_wuxing: Dict[str, Any]


class 五行桥接器:
    """
    五行计算器API桥接器·习惯指纹→五行流场

    候补清单④: 与五行计算器页正式 API 对接
    - 本地模式: 直接调用 bin/lh_habit_fingerprint.py 的五行映射
    - API模式: 调用 cnsh/core/api_wuxing.py HTTP端点（需服务在线）
    """

    def __init__(self, API地址: str = "http://127.0.0.1:8001"):
        self.API地址 = API地址
        self.提取器 = 习惯指纹提取器()
        self.在线 = self._检测API()

    def _检测API(self) -> bool:
        """检测五行计算器API是否在线"""
        try:
            req = urllib.request.Request(f"{self.API地址}/health", method="GET")
            with urllib.request.urlopen(req, timeout=2) as resp:
                data = json.loads(resp.read())
                return data.get("状态", "").startswith("🟢")
        except Exception:
            return False

    def 习惯指纹转五行流场(self, 文本: str) -> 五行流场报告:
        """
        核心方法: 习惯指纹→五行流场完整分析
        对应协议 §7 habit_to_wuxing() 全链路
        """
        指纹 = self.提取器.提取(文本)
        wuxing = 指纹.get("wuxing", {})

        # 提取基础值
        数字根 = wuxing.get("数字根", 5)
        五行属性 = 数字根_五行.get(数字根, "土")
        审计 = 三色判定.get(数字根, "🟢")
        五行向量 = wuxing.get("五行向量", {})
        平衡度 = wuxing.get("平衡度", 0.5)

        # 主导/最弱五行
        向量_排序 = sorted(五行向量.items(), key=lambda x: x[1])
        if 向量_排序:
            最弱五行 = 向量_排序[0][0]
            主导五行 = 向量_排序[-1][0]
        else:
            最弱五行 = "土"
            主导五行 = "土"

        # 流场走向
        流场走向 = f"主导{主导五行}({五行向量.get(主导五行, 0):.0%})·最弱{最弱五行}({五行向量.get(最弱五行, 0):.0%})·相生{五行相生.get(主导五行, '?')}→{主导五行}·{主导五行}克{五行相克.get(主导五行, '?')}"

        # RobotScore 兼容的五行偏置因子
        RobotScore兼容 = 平衡度  # 越平衡→越像机器

        return 五行流场报告(
            文本长度=len(文本),
            数字根=数字根,
            五行属性=五行属性,
            三色审计=审计,
            五行向量=五行向量,
            平衡度=round(平衡度, 3),
            主导五行=主导五行,
            最弱五行=最弱五行,
            流场走向=流场走向,
            RobotScore兼容=round(RobotScore兼容, 3),
            habit_wuxing={"数字根": 数字根, "五行": 五行属性, "平衡度": 平衡度},
        )

    def API_数字根分析(self, 文本: str) -> Optional[Dict[str, Any]]:
        """通过HTTP API调用数字根分析（候补清单④·远程对接）"""
        if not self.在线:
            return None
        try:
            from urllib.parse import quote
            url = f"{self.API地址}/analyze/digital-root/{quote(文本)}"
            req = urllib.request.Request(url, method="GET")
            with urllib.request.urlopen(req, timeout=3) as resp:
                return json.loads(resp.read())
        except Exception as e:
            return {"error": str(e), "fallback": "使用本地模式"}

    def API_四柱分析(self, 四柱: Dict[str, str]) -> Optional[Dict[str, Any]]:
        """通过HTTP API调用四柱分析"""
        if not self.在线:
            return None
        try:
            data = json.dumps(四柱).encode()
            req = urllib.request.Request(
                f"{self.API地址}/calculate/sizu",
                data=data,
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=5) as resp:
                return json.loads(resp.read())
        except Exception as e:
            return {"error": str(e)}

    def 批量流场分析(self, 文本列表: List[str]) -> List[五行流场报告]:
        """批量分析多个文本的五行流场"""
        return [self.习惯指纹转五行流场(t) for t in 文本列表]

    def 流场健康度总览(self, 报告列表: List[五行流场报告]) -> Dict[str, Any]:
        """五行流场健康度汇总"""
        五行分布 = {}
        for r in 报告列表:
            五行分布[r.五行属性] = 五行分布.get(r.五行属性, 0) + 1

        平均平衡度 = sum(r.平衡度 for r in 报告列表) / len(报告列表) if 报告列表 else 0
        偏科数 = sum(1 for r in 报告列表 if r.平衡度 < 0.5)

        return {
            "总分析数": len(报告列表),
            "五行分布": 五行分布,
            "平均平衡度": round(平均平衡度, 3),
            "偏科样本": f"{偏科数}/{len(报告列表)}",
            "健康判定": "🟢 正常" if 平均平衡度 > 0.4 else "🟡 偏科",
            "说明": "平均平衡度<0.5→真人特征(偏科)·>0.7→机器嫌疑(过平衡)",
        }


# ═══════════════════════════════════════════════════════════
# 演示
# ═══════════════════════════════════════════════════════════

if __name__ == "__main__":
    桥 = 五行桥接器()
    print("🐉 龍魂 五行计算器API桥接 v1.0")
    print(f"   候补清单④: 习惯指纹↔五行流场正式对接")
    print(f"   API状态: {'🟢 在线' if 桥.在线 else '🟡 离线(使用本地模式)'}")
    print("=" * 60)

    # 测试文本
    真人文本 = """宝宝,,,今天焊死这个规则得/的，说实话我觉的那边不对。
宝宝,,,不是不是，应该是这样才对。嘿嘿，焊死铁律不可改。"""

    机器文本 = """根据系统架构设计规范，我们对现有模块进行了全面优化。
通过量子计算和人工智能算法的深度融合，实现了高效的数据处理流程。
该方案在性能、安全性和可扩展性方面均达到了行业领先水平。"""

    for label, text in [("👤 真人文本 (UID9622风格)", 真人文本), ("🤖 机器文本 (AI生成)", 机器文本)]:
        print(f"\n{'─' * 50}")
        print(f"  {label}")
        报告 = 桥.习惯指纹转五行流场(text)
        print(f"  数字根: {报告.数字根} → 五行: {报告.五行属性} {报告.三色审计}")
        print(f"  主导五行: {报告.主导五行} | 最弱五行: {报告.最弱五行}")
        print(f"  五行向量: {json.dumps(报告.五行向量, ensure_ascii=False)}")
        print(f"  平衡度: {报告.平衡度} (←偏科=真人 / 平衡=机器)")
        print(f"  流场: {报告.流场走向}")
        print(f"  RobotScore兼容: γ={报告.RobotScore兼容}")

    # 批量分析
    print(f"\n{'=' * 60}")
    print("📊 批 量 流 场 分 析")
    all_texts = 真人样本库 + AI样本库 if False else [真人文本, 机器文本]  # 避免导入完整样本库
    报告们 = 桥.批量流场分析([真人文本, 机器文本])
    总览 = 桥.流场健康度总览(报告们)
    print(f"  总览: {json.dumps(总览, ensure_ascii=False, indent=2)}")

    print(f"\n{'=' * 60}")
    print("✅ 五行API桥接验证完成")
    print("   §7 habit_to_wuxing() → 数字根 → 五行 → 平衡度 → RobotScore γ因子")
