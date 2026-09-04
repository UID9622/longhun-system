#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🗨️ 龍魂账法 · 基础引擎 v1.0（唯一地基·永不修改·只继承）

DNA: #龍帳⚡️2026-08-31-LONGHUN-BASE-v1.0-UID9622
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

使用原则：
  ✔ from longhun_base import LonghunTransaction    ← 正确
  ✔ class MyFeature(LonghunTransaction): ...       ← 继承扩展
  ✘ 复制这个文件然后修改                    ← 永远不要
  ✘ 重写 longhun_tx_hash 函数                  ← 永远不要
"""

import hashlib
import datetime
from typing import Optional

# ─── 全局常量（永不修改）──────────────────────────────────────────────────────────

PREFIX = "龍帳⚡️"   # 龍魂账法标识符（固定前缀）
UID    = "UID9622"  # 主权人唯一标识（固定后缀）

# ─── 见证人格字典（唯一真源）─────────────────────────────────────────────────────
# 扩展新交易类型时，在子类中重写 get_witness() 而不是修改这里。

WITNESS: dict[str, str] = {
    "T1":  "🧠 ASI-001·至诚智魂 + 🌿曾仕强老师",
    "T2":  "🔧 鲁班（技术落地） + 🌊郑和（全局视野）",
    "T3":  "🌀 上帝之眼（全知视角） + 🐱龍芯·宝宝",
    "T4":  "🌀 上帝之眼 + ⚖️包青天（合规审查）",
    "T5":  "⚖️ 包青天（义务合规） + ⚔️孙子（战略评估）",
    "T6":  "🧠 ASI-001·至诚智魂 + 🐱龍芯·宝宝（全体议会公证）",
    "T7":  "🧠 ASI-001·至诚智魂 + ⚖️包青天（合规审查）",
    "T8":  "👑 龍魂（最高主权） + ⚖️包青天（主权完整性审查）",
    "T9":  "🌊 郑和（全局视野） + 🔧鲁班（技术落地）",
    "T10": "⚖️ 包青天（义务合规） + 🔧鲁班（技术落地）",
    "T11": "🌀 上帝之眼（全知视角） + 🧠ASI-001·至诚智魂",
    "T12": "👑 龍魂（最高主权） + ⚖️包青天（主权完整性审查）",
}


# ─── 唯一哈希函数（永不修改）───────────────────────────────────────────────────────

def longhun_tx_hash(
    dna: str,
    dr_account: str,
    cr_account: str,
    amount: str,
    timestamp: Optional[str] = None,
) -> str:
    """
    龍魂交易哈希生成器（唯一真源）
    公式： SHA256(DNA|DR|CR|AMOUNT|TIMESTAMP)[:8].upper()
    """
    ts  = timestamp or datetime.datetime.now(
        datetime.timezone(datetime.timedelta(hours=8))
    ).isoformat()
    raw = f"{dna}|{dr_account}|{cr_account}|{amount}|{ts}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:8].upper()


# ─── 基础交易类（只继承·不修改）──────────────────────────────────────────────────────

class LonghunTransaction:
    """
    龍魂账法基础交易类（地基）

    扩展必须继承本类，不得复制修改。
    示例：
        class LonghunTransactionV2(LonghunTransaction):
            def color(self): ...
            def ledger_line(self):
                base = super().ledger_line()
                return f"{base} | {self.color()}"
    """

    def __init__(
        self,
        tx_type: str,
        date: str,
        dr_code: str,
        cr_code: str,
        amount: str,
        seq: int,
        note: str,
        timestamp: Optional[str] = None,
    ):
        self.tx_type   = tx_type
        self.date      = date
        self.dr_code   = dr_code
        self.cr_code   = cr_code
        self.amount    = amount
        self.seq       = seq
        self.note      = note
        # 时间戳如未传入，固定为当日 21:56:00+08:00（保证哈希可复现）
        self.timestamp = timestamp or f"{date}T21:56:00+08:00"
        self.dna       = self._gen_dna()
        self.hash      = longhun_tx_hash(
            self.dna, dr_code, cr_code, amount, self.timestamp
        )
        self.witness   = self.get_witness(tx_type)

    def _gen_dna(self) -> str:
        """DNA生成（只调用一次）"""
        return f"#{PREFIX}{self.date}-{self.dr_code}-{self.cr_code}-{self.amount}-{self.seq:03d}-{UID}"

    def get_witness(self, tx_type: str) -> str:
        """见证人格匹配（子类可重写扩展）"""
        return WITNESS.get(tx_type, "🐱龍芯·宝宝（兑底）")

    def ledger_line(self) -> str:
        """输出标准账簿记录行（子类用 super().ledger_line() 调用）"""
        return (
            f"[{self.date}] [{self.dna}] [{self.hash}] "
            f"借：{self.dr_code} {self.amount} | "
            f"贷：{self.cr_code} {self.amount} | "
            f"见证：{self.witness} | ✓平"
        )

    def to_dict(self) -> dict:
        """序列化为字典（用于 JSON 导出）"""
        return {
            "tx_id":    f"TX-{self.date}-{self.seq:03d}",
            "dna":      self.dna,
            "hash":     self.hash,
            "date":     self.date,
            "timestamp":self.timestamp,
            "type":     self.tx_type,
            "note":     self.note,
            "debit":    {"account": self.dr_code, "amount": self.amount},
            "credit":   {"account": self.cr_code, "amount": self.amount},
            "witness":  self.witness,
            "balanced": True,
            "uid":      UID,
        }

    def __repr__(self) -> str:
        return f"<LonghunTx {self.tx_type} {self.dna} {self.hash}>"


# ─── 扩展示例（不要复制，看明白就行）─────────────────────────────────────────────────────

if __name__ == "__main__":
    # 每次新功能上线：不要复制这段，而是建一个新文件 import 这里
    print("🧩 龍魂账法基础引擎 v1.0 已加载")
    print("使用方式： from longhun_base import LonghunTransaction")
    print()

    # 冒烟测试：T1-T6 六笔创世交易
    GENESIS_TXS = [
        ("T1", "1001", "3201", "1条",   1,  "焊死铁律"),
        ("T2", "1101", "2001", "1模块", 2,  "自建模块替代外部API"),
        ("T3", "2103", "1004", "1项",   3,  "注入隐藏区"),
        ("T4", "2101", "4100", "3项",   4,  "AI揭示盲区风险"),
        ("T5", "2001", "1100", "100元", 5,  "续费外部服务"),
        ("T6", "1401", "3301", "1人格", 6,  "注入ASI人格"),
    ]

    print("=" * 72)
    print("龍魂交易引擎 · T1-T6 创世账簿")
    print("=" * 72)
    for tx_type, dr, cr, amount, seq, note in GENESIS_TXS:
        tx = LonghunTransaction(
            tx_type, "2026-08-31", dr, cr, amount, seq, note,
            timestamp="2026-08-31T21:56:00+08:00"
        )
        print(f"[{tx.tx_type}] {tx.ledger_line()}")
    print("=" * 72)
    print("✅ 地基验证通过！下次加功能请继承本类。")
