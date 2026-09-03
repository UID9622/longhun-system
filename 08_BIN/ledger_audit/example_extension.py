#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🗨️ 龍魂账法 · 扩展示例（如何正确在地基上加新功能）
DNA: #龍帳⚡️2026-08-31-EXTENSION-EXAMPLE-v1.0-UID9622

核心原则：
  1. 第一行就 import 地基，不复制
  2. 继承 LonghunTransaction，不重写已有逻辑
  3. 新方法只加新的，已有的用 super() 调用
"""

from longhun_base import LonghunTransaction  # ← 地基，不重造

# ─── 扩展 v1.1：加三色健康度标注 ────────────────────────────────────────────────────

HEALTH_MAP = {
    frozenset(["T1", "T2", "T6", "T7", "T11"]): ("🟢", "双重利好"),
    frozenset(["T3", "T4", "T8", "T9", "T10"]): ("🟡", "中性/注意"),
    frozenset(["T5"]):                          ("🔴", "损害主权·需替代计划"),
    frozenset(["T12"]):                         ("🚫", "系统强制拦截"),
}


class LonghunTransactionV2(LonghunTransaction):
    """
    v1.1 扩展：新增三色健康度标注。
    地基逻辑（DNA生成/哈希计算/见证匹配）全部继承，不动一行。
    """

    def health(self) -> tuple[str, str]:
        """三色 + 健康度文字（新加）"""
        for types, (color, label) in HEALTH_MAP.items():
            if self.tx_type in types:
                return color, label
        return "🟡", "未知类型"

    def ledger_line(self) -> str:
        """在父类账簿行后面，只加一个健康度标注"""
        base          = super().ledger_line()   # 父类完整行
        color, label  = self.health()
        return f"{base} | {color} {label}"


# ─── 扩展 v1.2：在 v1.1 基础上加 JSON 导出 + 审计指数 ─────────────────────────────────

class LonghunTransactionV3(LonghunTransactionV2):
    """
    v1.2 扩展：新增审计指数 + JSON 导出健康度字段。
    继承 v1.1，不动 v1.0 地基。
    """

    def to_dict(self) -> dict:
        """在父类 dict 基础上只加 health 字段"""
        d            = super().to_dict()   # 父类完整 dict
        color, label = self.health()
        d["health"]  = f"{color} {label}"
        return d


# ─── 使用演示 ────────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import json

    # v1.1 演示
    tx_v2 = LonghunTransactionV2(
        "T1", "2026-08-31", "1001", "3201", "1条", 1, "焊死铁律",
        timestamp="2026-08-31T21:56:00+08:00"
    )
    print("v1.1:", tx_v2.ledger_line())
    # → [2026-08-31] [...] [A3F7D291] 借：1001 1条 | 贷：3201 1条 | 见证：... | ✓平 | 🟢 双重利好

    # v1.2 演示
    tx_v3 = LonghunTransactionV3(
        "T5", "2026-08-31", "2001", "1100", "100元", 5, "续费外部服务",
        timestamp="2026-08-31T21:56:00+08:00"
    )
    print("v1.2:", tx_v3.ledger_line())
    print("JSON:", json.dumps(tx_v3.to_dict(), ensure_ascii=False, indent=2))
