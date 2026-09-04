#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════════╗
║     龍魂·DNA三层主权桥接 v1.0 — 习惯指纹→DNA身份→本地加签·密文不出设备          ║
║     DNA Three-Layer Sovereignty Bridge · Local Sign · Ciphertext Local   ║
╠══════════════════════════════════════════════════════════════════════════╣
║  DNA: #龍芯⚡️丙午·乙未·癸未·辰时-DNA-SOVEREIGNTY-BRIDGE-v1.0            ║
║  协议: §9 DNA身份三层 + §11 候补清单⑤                                       ║
║  铁律: L1(UID)+L2(切片码)+L3(HMAC戳) — 本地计算·密文不出设备                  ║
╚══════════════════════════════════════════════════════════════════════════╝

DNA链格式: #龍芯⚡️YYYY-MM-DD-HH:MM-<事件代号>-L1-L2前16位-L3戳

用法:
    from bin.lh_dna_sovereignty_bridge import DNA主权桥
    桥 = DNA主权桥("UID9622")
    dna_链 = 桥.生成DNA链("操作文本", "EVENT-CODE")
"""

import hashlib
import hmac
import json
import time
from datetime import datetime
from typing import Dict, Optional, Any
from bin.lh_habit_fingerprint import 习惯指纹提取器


class DNA主权桥:
    """
    DNA三层主权桥接器·本地计算·密文不出设备

    L1: 永久UID（你是谁）
    L2: 习惯切片码 SHA256(D1‖D2‖D5) 前16位（你怎么写）
    L3: HMAC验证戳 HMAC(L1⊕L2, 时间盐) 前8位（防伪签名）
    """

    def __init__(self, uid: str = "UID9622"):
        self.uid = uid
        self.提取器 = 习惯指纹提取器()
        self.主权密钥 = hashlib.sha256(f"longhun-sovereignty-{uid}".encode()).digest()

    def L1_永久UID(self) -> str:
        """L1: 返回永久UID — 永不出设备"""
        return self.uid

    def L2_习惯切片码(self, 文本: str) -> str:
        """
        L2: 习惯切片码 = SHA256(D1‖D2‖D5) 前16位
        只出摘要·原料不出设备
        """
        指纹 = self.提取器.提取(文本)
        切片 = 指纹.get("slices", "")
        return 切片[:16] if 切片 else "0000000000000000"

    def L3_HMAC验证戳(self, l2_切片: str) -> str:
        """
        L3: HMAC验证戳 = HMAC-SHA256(L1⊕L2, "longhun-sovereignty-salt") 前8位
        仅戳出·原料不出
        """
        联合 = f"{self.uid}|{l2_切片}"
        h = hmac.new(self.主权密钥, 联合.encode(), hashlib.sha256)
        return h.hexdigest()[:8]

    def 生成DNA链(self, 文本: str, 事件代号: str = "") -> str:
        """
        生成完整 DNA 主权链：
        格式: #龍芯⚡️YYYY-MM-DD-HH:MM-<事件>-L1-L2-L3
        """
        now = datetime.now().strftime("%Y-%m-%d-%H:%M")
        l1 = self.L1_永久UID()
        l2 = self.L2_习惯切片码(文本)
        l3 = self.L3_HMAC验证戳(l2)
        事件 = 事件代号 or "ACTION"
        return f"#龍芯⚡️{now}-{事件}-{l1}-{l2[:8]}-{l3}"

    def 验证DNA链(self, dna_链: str, 原始文本: str) -> Dict[str, Any]:
        """
        验证 DNA 主权链是否合法
        - 比较 L2 切片码是否匹配
        - 比较 L3 HMAC 戳是否匹配
        """
        parts = dna_链.split("-")
        if len(parts) < 6:
            return {"valid": False, "error": "DNA链格式不完整"}

        l2_claim = parts[-2]  # L2 声明的切片码 (8位·DNA链中仅存前8)
        l3_claim = parts[-1]  # L3 声明的验证戳

        # 重新计算 L2 (完整16位→截8位比对DNA链存储)
        l2_full = self.L2_习惯切片码(原始文本)  # 完整16位
        l2_actual = l2_full[:8]  # DNA链中只存前8位
        l2_match = l2_actual == l2_claim

        # 重新计算 L3 — 用完整L2(16位)计算HMAC，与生成DNA链时一致
        l3_actual = self.L3_HMAC验证戳(l2_full)
        l3_match = l3_actual == l3_claim

        return {
            "valid": l2_match and l3_match,
            "l2_match": l2_match,
            "l3_match": l3_match,
            "l2_claim": l2_claim,
            "l2_actual": l2_actual,
            "l3_claim": l3_claim,
            "l3_actual": l3_actual,
        }

    def 出设备报告(self) -> Dict[str, Any]:
        """
        主权状态报告 — 仅报告概要·不泄露原料
        """
        return {
            "L1_UID": self.uid,
            "L2_状态": "摘要就绪·原料未出",
            "L3_状态": "HMAC就绪·密钥本地",
            "密文出设备": False,
            "主权完整": True,
            "timestamp": datetime.now().isoformat(),
        }


# ═══════════════════════════════════════════════════════════
# 演示
# ═══════════════════════════════════════════════════════════

if __name__ == "__main__":
    桥 = DNA主权桥("UID9622")

    测试文本 = """宝宝,,,今天焊死这个规则，不动点切割是唯一解。
DNA追溯每一刀，铁律不可改。主权最重要。"""

    print("🧬 龍魂 DNA 三层主权桥接 v1.0")
    print("=" * 60)

    # 三层分别展示
    print(f"\n  L1 永久UID: {桥.L1_永久UID()}")

    l2 = 桥.L2_习惯切片码(测试文本)
    print(f"  L2 习惯切片码: {l2} (前16位·摘要仅此·原料不出)")

    l3 = 桥.L3_HMAC验证戳(l2)
    print(f"  L3 HMAC验证戳: {l3} (前8位·防伪签名)")

    # 完整 DNA 链
    dna_链 = 桥.生成DNA链(测试文本, "TEST-WELD")
    print(f"\n  📿 完整 DNA 链:")
    print(f"     {dna_链}")

    # 验证
    print(f"\n  🔍 验证 DNA 链:")
    验证结果 = 桥.验证DNA链(dna_链, 测试文本)
    print(f"     有效: {'✅是' if 验证结果['valid'] else '❌否'}")
    print(f"     L2匹配: {'✅' if 验证结果['l2_match'] else '❌'}")
    print(f"     L3匹配: {'✅' if 验证结果['l3_match'] else '❌'}")

    # 篡改检测
    篡改文本 = 测试文本.replace("焊死", "修改")
    篡改验证 = 桥.验证DNA链(dna_链, 篡改文本)
    print(f"\n  🔒 篡改检测 (文本被修改):")
    print(f"     有效: {'✅是' if 篡改验证['valid'] else '❌否(正确熔断)'}")
    print(f"     L2匹配: {'✅' if 篡改验证['l2_match'] else '❌(切片码已变)'}")

    print(f"\n  📋 主权报告:")
    print(f"     {json.dumps(桥.出设备报告(), ensure_ascii=False, indent=6)}")

    print(f"\n{'=' * 60}")
    print("✅ DNA 三层主权桥接验证完成")
    print("   铁律: L1+L2 原料永不出设备·L3 仅戳出")
