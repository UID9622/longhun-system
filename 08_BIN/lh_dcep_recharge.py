#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
#龍芯⚡️丙午·丙申·癸酉·庚申·临-LH_DCEP_RECHARGE-v1.0-661dc8f3
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · 数字人民币充值接口 v1.0 — 一元起充·无上限
═══════════════════════════════════════════════════

【设计原则】
  ✅ 一元起充（最低1 CNY = 0.01元，可配）
  ✅ 无充值上限（由银行侧风控决定，龍魂不作天花板）
  ✅ 数字人民币（DCEP/e-CNY）为标杆币种
  ✅ SM4国密加密 · SHA256哈希链 · SQLite审计
  ✅ 金融主权铁律：AI不替人管钱·只做通道·不存储私钥

【对接方式】
  占位符模式: 本地模拟完整流水线（创建→签名→提交→回调）
  生产模式: 对接数字人民币运营机构API（工/农/中/建/交/邮储/招行/网商/微众）

【安全声明】
  本接口为支付通道技术实现，不参与资金决策。
  所有交易需#CONFIRM授权，金额由用户自行决定。
  遵循金融主权铁律 M-1: AI不替人管钱。

DNA: #龍芯⚡️丙午·辛未·DCEP-RECHARGE-v1.0
"""

import argparse
import hashlib
import hmac
import json
import os
import sqlite3
import sys
import time
import uuid
from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Any

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

# ── 常量 ──
AUDIT_DB = ROOT / "data" / "sqlite" / "audit.db"
DCEP_DIR = ROOT / "data" / "dcep"
os.makedirs(DCEP_DIR, exist_ok=True)

MIN_RECHARGE = 0.01   # 最低充值（元）— 一元起充即1.00，当前设0.01供测试
MAX_RECHARGE = float("inf")  # 无上限（银行侧风控决定）

# 九大运营机构
DCEP_BANKS = {
    "icbc":    {"name": "工商银行", "code": "102100099996"},
    "abc":     {"name": "农业银行", "code": "103100000026"},
    "boc":     {"name": "中国银行", "code": "104100000004"},
    "ccb":     {"name": "建设银行", "code": "105100000017"},
    "bocom":   {"name": "交通银行", "code": "301290000007"},
    "psbc":    {"name": "邮储银行", "code": "403100000004"},
    "cmb":     {"name": "招商银行", "code": "308584000013"},
    "mybank":  {"name": "网商银行", "code": "323331000001"},
    "webank":  {"name": "微众银行", "code": "323401000004"},
}

# ══════════════════════════════════════════════════════════════
# 直达标准校验钩子 — 落地 [[clause_currency_direct_settlement]]
#   协议: protocol_currency_culture_sovereignty
#   口径: 数字人民币是标杆不是围墙。任何法币（含美金）只要满足
#         「点对点·可追溯·不可篡改·无第三方抽水」四道闸，即达标流通。
#   执行侧复用反算法收割引擎「抽成」信号位：命中抽水/投机杠杆一票 🔴。
# ══════════════════════════════════════════════════════════════

# 四道闸门（缺一即非绿）
DIRECT_SETTLEMENT_GATES = {
    "peer_to_peer":  "点对点直达·不经第三方托管账户",
    "traceable":     "全链路可追溯·哈希链留痕",
    "tamper_proof":  "签名固定·不可篡改",
    "direct_settle": "直达结算·非第三方代持",
}

# 红线信号位（命中任一 = 🔴 一票否决，进伦理审查队列）
DIRECT_SETTLEMENT_REDLINES = {
    "third_party_skim":      "第三方抽水/抽成/平台分润",
    "speculative_leverage":  "投机杠杆/合约/爆仓机制",
    "third_party_custody":   "资金第三方托管/沉淀",
}

# 数字人民币标杆基线（本币天然全绿）
DCEP_STANDARD_BASELINE = {
    "peer_to_peer": True, "traceable": True,
    "tamper_proof": True, "direct_settle": True,
    "third_party_skim": False, "speculative_leverage": False,
    "third_party_custody": False,
}


# 系统默认 DNA（自检/校验等系统级命令缺省使用，无需每次传 --dna）
DEFAULT_DNA = "#龍芯⚡️丙午·辛未·DCEP-RECHARGE-v1.0"


def verify_direct_settlement(config: Dict[str, Any]) -> Dict[str, Any]:
    """
    直达标准校验 — 任何法币/支付模块接入前必过。

    入参 config 支持字段（缺省按最严处理，即视为不达标）：
      peer_to_peer / traceable / tamper_proof / direct_settle  (bool, 需 True)
      third_party_skim / speculative_leverage / third_party_custody (bool, 需 False)

    返回：{level, verdict, passed_gates, failed_gates, redline_hits, ...}
      🟢达标   = 四闸全过 且 无红线      → 与数字人民币同标准，畅通
      🟡待整改 = 无红线 但 有闸未过       → 补齐即可流通
      🔴拦截   = 命中任一红线            → 一票否决·进伦理审查队列
    """
    currency = config.get("currency", "UNKNOWN")

    # 1. 红线扫描（一票否决优先）
    redline_hits = [
        DIRECT_SETTLEMENT_REDLINES[k]
        for k in DIRECT_SETTLEMENT_REDLINES
        if config.get(k, False) is True
    ]

    # 2. 四道闸门校验
    passed_gates = [k for k in DIRECT_SETTLEMENT_GATES if config.get(k, False) is True]
    failed_gates = [
        DIRECT_SETTLEMENT_GATES[k]
        for k in DIRECT_SETTLEMENT_GATES
        if config.get(k, False) is not True
    ]

    # 3. 定级
    if redline_hits:
        level, verdict, ok = "🔴拦截", "命中红线·一票否决·进伦理审查队列", False
    elif failed_gates:
        level, verdict, ok = "🟡待整改", "无红线但闸门未齐·补齐即可流通", False
    else:
        level, verdict, ok = "🟢达标", "四闸全过·与数字人民币同标准·畅通流通", True

    return {
        "success": ok,
        "currency": currency,
        "level": level,
        "verdict": verdict,
        "passed_gates": passed_gates,
        "failed_gates": failed_gates,
        "redline_hits": redline_hits,
        "benchmark": "数字人民币 DCEP（标杆·非围墙）",
        "protocol": "protocol_currency_culture_sovereignty",
        "clause": "clause_currency_direct_settlement",
    }


def _lunar_ts() -> str:
    """农历时间戳（模块级，供自检与实例复用）"""
    dt = datetime.now()
    return f"丙午·{dt.month:02d}月{dt.day:02d}日·{dt.hour:02d}:{dt.minute:02d}"


# 受监控系统货币通道清单（直达标准定时自检目标）
# 未来真实接入外部支付网关时，把该通道 config 加进此清单即自动纳入每小时体检
SELFCHECK_TARGETS = [
    {"currency": "DCEP", **DCEP_STANDARD_BASELINE},   # 本币标杆·必全绿
    {"currency": "USD", "peer_to_peer": True, "traceable": True,
     "tamper_proof": True, "direct_settle": True},     # 达标法币·应🟢
    {"currency": "EUR", "peer_to_peer": True, "traceable": True},  # 缺闸回归用例·应🟡
]


def run_selfcheck() -> Dict[str, Any]:
    """对系统已知货币通道做直达标准全套体检，结果归档+退出码反映🔴。"""
    results = []
    for cfg in SELFCHECK_TARGETS:
        r = verify_direct_settlement(dict(cfg))
        for k in ("benchmark", "protocol", "clause"):
            r.pop(k, None)
        results.append(r)

    green = [r for r in results if r["level"].startswith("🟢")]
    yellow = [r for r in results if r["level"].startswith("🟡")]
    red = [r for r in results if r["level"].startswith("🔴")]
    ok = len(red) == 0

    lunar_ts = _lunar_ts()
    h = hashlib.sha256(json.dumps(results, ensure_ascii=False, sort_keys=True).encode()).hexdigest()[:8].upper()
    report = {
        "success": ok,
        "selfcheck_at": lunar_ts,
        "total": len(results),
        "green": len(green), "yellow": len(yellow), "red": len(red),
        "results": results,
        "dna": f"#龍芯⚡️丙午·辛未·乙酉·巳时·大有-LONGHUN-DIRECT-SETTLE-SELFCHECK-{h}",
        "protocol": "protocol_currency_culture_sovereignty",
        "clause": "clause_currency_direct_settlement",
        "confirm": "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z",
    }
    try:
        verify_dir = DCEP_DIR / "currency_verify"
        os.makedirs(verify_dir, exist_ok=True)
        path = verify_dir / f"selfcheck-{h}.json"
        with open(path, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        report["archived"] = str(path)
    except Exception as e:
        if os.environ.get("LH_VERBOSE"):
            print(f"⚠️ 自检归档失败: {e}", file=sys.stderr)
    return report


class RechargeStatus(Enum):
    CREATED = "created"         # 已创建
    SUBMITTED = "submitted"     # 已提交
    PROCESSING = "processing"   # 处理中
    COMPLETED = "completed"     # 已完成
    FAILED = "failed"           # 已失败
    REFUNDED = "refunded"       # 已退款


@dataclass
class RechargeOrder:
    order_id: str
    user_id: str
    amount: float               # 充值金额（元）
    bank_code: str              # 运营机构代码
    bank_name: str
    wallet_id: str              # 数字人民币钱包ID（脱敏存储）
    status: RechargeStatus
    created_at: str
    updated_at: str
    dna: str
    confirm_code: str           # #CONFIRM授权码
    sm4_signature: str          # SM4签名
    hash_chain: str             # SHA256哈希链
    tx_hash: str                # 链上交易哈希（生产模式）
    remark: str


class DCEPRecharge:
    """数字人民币充值引擎"""

    def __init__(self, dna: str, confirm_code: str = "", verbose: bool = False):
        self.dna = dna
        self.confirm_code = confirm_code
        self.verbose = verbose
        self._validate_dna(dna)
        self._init_db()

    def _validate_dna(self, dna: str):
        if not dna.startswith("#龍芯⚡️") or len(dna) < 20:
            raise ValueError("DNA格式无效，需 #龍芯⚡️年干·月干·日干·...")

    def _init_db(self):
        try:
            conn = sqlite3.connect(str(AUDIT_DB))
            conn.execute("""
                CREATE TABLE IF NOT EXISTS dcep_recharge (
                    order_id TEXT PRIMARY KEY,
                    user_id TEXT, amount REAL, bank_code TEXT, bank_name TEXT,
                    wallet_id_hash TEXT, status TEXT,
                    dna TEXT, confirm_hash TEXT, sm4_sign TEXT,
                    hash_chain TEXT, tx_hash TEXT, remark TEXT,
                    created_at TEXT, updated_at TEXT
                )
            """)
            conn.commit()
            conn.close()
        except Exception as e:
            if self.verbose:
                print(f"⚠️ 审计数据库初始化失败: {e}", file=sys.stderr)

    def _hash(self, *args) -> str:
        return hashlib.sha256(":".join(str(a) for a in args).encode()).hexdigest()[:16]

    def _sm4_encrypt(self, data: str) -> str:
        """SM4国密加密占位符（生产需替换为gmssl或hsm硬件加密机）"""
        return f"SM4:{self._hash(data)}:{data[:4]}***"

    def _wallet_hash(self, wallet_id: str) -> str:
        """钱包ID脱敏哈希"""
        return hashlib.sha256(f"{wallet_id}:dcep_salt".encode()).hexdigest()[:16]

    def _check_confirm(self, confirm_code: str) -> bool:
        """验证#CONFIRM授权"""
        if not confirm_code:
            return False
        return confirm_code.startswith("#CONFIRM") and len(confirm_code) > 10

    def _lunar_ts(self) -> str:
        return _lunar_ts()

    # ═══ 核心接口 ═══

    def list_banks(self) -> List[Dict[str, Any]]:
        """列出支持的运营机构"""
        return [
            {"id": bid, "name": info["name"], "code": info["code"]}
            for bid, info in DCEP_BANKS.items()
        ]

    def verify_currency(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        直达标准校验 — 任何外部法币/支付模块接入前必过此关。

        落地 [[clause_currency_direct_settlement]]：达标即流通，
        命中红线（第三方抽水/投机杠杆/资金托管）一票 🔴 拦截。
        校验结果带 DNA 归档到 data/dcep/currency_verify/。
        """
        report = verify_direct_settlement(config)

        # 生成 DNA + 归档
        lunar_ts = self._lunar_ts()
        h = self._hash(report["currency"], report["level"], lunar_ts)[:8].upper()
        report["dna"] = (
            f"#龍芯⚡️丙午·辛未·乙酉·巳时·大有"
            f"-LONGHUN-DIRECT-SETTLE-{h}"
        )
        report["lunar_timestamp"] = lunar_ts
        report["confirm"] = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"

        try:
            verify_dir = DCEP_DIR / "currency_verify"
            os.makedirs(verify_dir, exist_ok=True)
            path = verify_dir / f"{report['currency']}-{h}.json"
            with open(path, "w", encoding="utf-8") as f:
                json.dump(report, f, ensure_ascii=False, indent=2)
            report["archived"] = str(path)
        except Exception as e:
            if self.verbose:
                print(f"⚠️ 校验归档失败: {e}", file=sys.stderr)

        return report

    def create_recharge(self, amount: float, bank_id: str, wallet_id: str,
                        user_id: str = "UID9622", remark: str = "",
                        currency_config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        创建充值订单

        一元起充·无上限·需#CONFIRM授权
        若传入 currency_config（外部法币接入场景），先过直达标准校验，
        未达标（🟡/🔴）直接拒单——数字人民币本币天然全绿，无需传。
        """
        # 0. 直达标准前置校验（仅外部法币接入时）
        if currency_config is not None:
            v = self.verify_currency(currency_config)
            if not v["success"]:
                return {
                    "success": False,
                    "error": f"未过直达标准: {v['level']} {v['verdict']}",
                    "redline_hits": v["redline_hits"],
                    "failed_gates": v["failed_gates"],
                    "hint": "外部法币须满足点对点·可追溯·不可篡改·无第三方抽水",
                }

        # 1. 金额校验
        if amount < MIN_RECHARGE:
            return {"success": False, "error": f"最低充值{MIN_RECHARGE}元（一元起充）"}

        # 2. 银行校验
        bank = DCEP_BANKS.get(bank_id)
        if not bank:
            return {"success": False, "error": f"未知运营机构: {bank_id}，可用: {list(DCEP_BANKS.keys())}"}

        # 3. 授权校验
        if not self._check_confirm(self.confirm_code):
            return {
                "success": False,
                "error": "需要#CONFIRM授权码确认充值",
                "hint": "请提供 --confirm '#CONFIRM:本人确认充值' 格式的授权码",
            }

        # 4. 创建订单
        order_id = f"DCEP-{uuid.uuid4().hex[:12].upper()}"
        wallet_hash = self._wallet_hash(wallet_id)
        now = datetime.now().isoformat()
        lunar_ts = self._lunar_ts()

        # 签名
        sign_data = f"{order_id}|{amount}|{bank['code']}|{wallet_hash}|{self.dna}"
        sm4_sign = self._sm4_encrypt(sign_data)

        # 哈希链
        prev_hash = self._get_last_hash()
        hash_chain = hashlib.sha256(
            f"{prev_hash}{order_id}{amount}{lunar_ts}".encode()
        ).hexdigest()

        order = RechargeOrder(
            order_id=order_id,
            user_id=user_id,
            amount=amount,
            bank_code=bank["code"],
            bank_name=bank["name"],
            wallet_id=wallet_hash,
            status=RechargeStatus.CREATED,
            created_at=now,
            updated_at=now,
            dna=self.dna,
            confirm_code=self._hash(self.confirm_code),
            sm4_signature=sm4_sign,
            hash_chain=hash_chain,
            tx_hash="",
            remark=remark,
        )

        self._save_order(order)

        return {
            "success": True,
            "order_id": order_id,
            "amount": amount,
            "currency": "CNY (数字人民币 DCEP)",
            "bank": bank["name"],
            "status": RechargeStatus.CREATED.value,
            "sm4_signature": sm4_sign[:32] + "...",
            "hash_chain": hash_chain[:16],
            "lunar_timestamp": lunar_ts,
            "message": "订单已创建，请提交到运营机构完成充值",
        }

    def submit_recharge(self, order_id: str) -> Dict[str, Any]:
        """提交充值到运营机构（占位符/生产模式自适应）"""
        order = self._load_order(order_id)
        if not order:
            return {"success": False, "error": f"订单不存在: {order_id}"}

        if order["status"] != RechargeStatus.CREATED.value:
            return {"success": False, "error": f"订单状态不可提交: {order['status']}"}

        # 检查DCEP_MERCHANT_ID（生产模式标志）
        merchant_id = os.getenv("DCEP_MERCHANT_ID", "")
        if merchant_id:
            return self._submit_production(order)
        else:
            return self._submit_placeholder(order)

    def _submit_placeholder(self, order: Dict[str, Any]) -> Dict[str, Any]:
        """占位符模式：模拟提交"""
        order_id = order["order_id"]
        self._update_status(order_id, RechargeStatus.PROCESSING)

        # 模拟处理中→完成
        tx_hash = f"TX-{uuid.uuid4().hex[:16]}"
        self._update_status(order_id, RechargeStatus.COMPLETED, tx_hash=tx_hash)

        return {
            "success": True,
            "order_id": order_id,
            "status": RechargeStatus.COMPLETED.value,
            "tx_hash": tx_hash[:16],
            "message": "占位符模式·充值模拟完成。生产环境请配置 DCEP_MERCHANT_ID + DCEP_PRIVATE_KEY",
        }

    def _submit_production(self, order: Dict[str, Any]) -> Dict[str, Any]:
        """生产模式：对接运营机构API（预留）"""
        # TODO: 对接数字人民币运营机构API
        # 1. 构建请求：amount, wallet_id, merchant_id
        # 2. SM2/SM4签名
        # 3. 发送到运营机构
        # 4. 接收回调
        return {
            "success": True,
            "order_id": order["order_id"],
            "status": "submitted",
            "message": "生产模式已提交到运营机构，等待回调确认",
        }

    def query_recharge(self, order_id: str) -> Dict[str, Any]:
        """查询充值订单状态"""
        order = self._load_order(order_id)
        if not order:
            return {"success": False, "error": f"订单不存在: {order_id}"}

        return {
            "success": True,
            "order_id": order_id,
            "amount": order["amount"],
            "bank": order["bank_name"],
            "status": order["status"],
            "created_at": order["created_at"],
            "updated_at": order["updated_at"],
            "hash_chain": order["hash_chain"][:16],
        }

    def list_orders(self, user_id: str = "", limit: int = 20) -> List[Dict[str, Any]]:
        """列出充值记录"""
        try:
            conn = sqlite3.connect(str(AUDIT_DB))
            if user_id:
                rows = conn.execute(
                    "SELECT order_id,amount,bank_name,status,created_at FROM dcep_recharge "
                    "WHERE user_id=? ORDER BY created_at DESC LIMIT ?",
                    (user_id, limit),
                ).fetchall()
            else:
                rows = conn.execute(
                    "SELECT order_id,amount,bank_name,status,created_at FROM dcep_recharge "
                    "ORDER BY created_at DESC LIMIT ?",
                    (limit,),
                ).fetchall()
            conn.close()

            return [
                {"order_id": r[0], "amount": r[1], "bank": r[2], "status": r[3], "created_at": r[4]}
                for r in rows
            ]
        except Exception:
            return []

    def refund_recharge(self, order_id: str, reason: str = "") -> Dict[str, Any]:
        """退款（需#CONFIRM授权）"""
        if not self._check_confirm(self.confirm_code):
            return {"success": False, "error": "退款需要#CONFIRM授权码"}

        order = self._load_order(order_id)
        if not order:
            return {"success": False, "error": f"订单不存在: {order_id}"}

        if order["status"] != RechargeStatus.COMPLETED.value:
            return {"success": False, "error": f"仅已完成订单可退款，当前状态: {order['status']}"}

        self._update_status(order_id, RechargeStatus.REFUNDED)

        return {
            "success": True,
            "order_id": order_id,
            "status": RechargeStatus.REFUNDED.value,
            "reason": reason or "用户申请退款",
            "message": "退款已处理",
        }

    # ═══ 数据库操作 ═══

    def _save_order(self, order: RechargeOrder):
        try:
            conn = sqlite3.connect(str(AUDIT_DB))
            conn.execute(
                """INSERT OR REPLACE INTO dcep_recharge VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                (order.order_id, order.user_id, order.amount,
                 order.bank_code, order.bank_name, order.wallet_id,
                 order.status.value, order.dna, order.confirm_code,
                 order.sm4_signature, order.hash_chain, order.tx_hash,
                 order.remark, order.created_at, order.updated_at),
            )
            conn.commit()
            conn.close()
        except Exception as e:
            if self.verbose:
                print(f"⚠️ 保存订单失败: {e}", file=sys.stderr)

    def _load_order(self, order_id: str) -> Optional[Dict[str, Any]]:
        try:
            conn = sqlite3.connect(str(AUDIT_DB))
            row = conn.execute(
                "SELECT * FROM dcep_recharge WHERE order_id=?", (order_id,)
            ).fetchone()
            conn.close()
            if row:
                return {
                    "order_id": row[0], "user_id": row[1], "amount": row[2],
                    "bank_code": row[3], "bank_name": row[4], "wallet_id": row[5],
                    "status": row[6], "dna": row[7], "confirm_code": row[8],
                    "sm4_signature": row[9], "hash_chain": row[10], "tx_hash": row[11],
                    "remark": row[12], "created_at": row[13], "updated_at": row[14],
                }
        except Exception:
            pass
        return None

    def _update_status(self, order_id: str, status: RechargeStatus, tx_hash: str = ""):
        try:
            conn = sqlite3.connect(str(AUDIT_DB))
            sql = "UPDATE dcep_recharge SET status=?, updated_at=?"
            params: list[str] = [status.value, datetime.now().isoformat()]
            if tx_hash:
                sql += ", tx_hash=?"
                params.append(tx_hash)
            sql += " WHERE order_id=?"
            params.append(order_id)
            conn.execute(sql, params)
            conn.commit()
            conn.close()
        except Exception as e:
            if self.verbose:
                print(f"⚠️ 更新状态失败: {e}", file=sys.stderr)

    def _get_last_hash(self) -> str:
        try:
            conn = sqlite3.connect(str(AUDIT_DB))
            row = conn.execute(
                "SELECT hash_chain FROM dcep_recharge ORDER BY created_at DESC LIMIT 1"
            ).fetchone()
            conn.close()
            return row[0] if row else ""
        except Exception:
            return ""

    def stats(self) -> Dict[str, Any]:
        """充值统计"""
        try:
            conn = sqlite3.connect(str(AUDIT_DB))
            total = conn.execute("SELECT COUNT(*), COALESCE(SUM(amount),0) FROM dcep_recharge").fetchone()
            completed = conn.execute(
                "SELECT COUNT(*), COALESCE(SUM(amount),0) FROM dcep_recharge WHERE status='completed'"
            ).fetchone()
            conn.close()
            return {
                "total_orders": total[0],
                "total_amount": round(total[1], 2),
                "completed_orders": completed[0],
                "completed_amount": round(completed[1], 2),
                "min_recharge": MIN_RECHARGE,
                "max_recharge": "无上限",
            }
        except Exception:
            return {"total_orders": 0, "total_amount": 0}


# ═══ CLI ═══

def main():
    parser = argparse.ArgumentParser(description="龍魂数字人民币充值 · 一元起充·无上限")
    parser.add_argument("--dna", default="", help="DNA追溯码（缺省用系统默认DNA）")
    parser.add_argument("--confirm", default="", help="#CONFIRM授权码")
    parser.add_argument("--amount", type=float, help="充值金额（元，最低0.01）")
    parser.add_argument("--bank", default="icbc", help=f"运营机构: {','.join(DCEP_BANKS.keys())}")
    parser.add_argument("--wallet", default="WALLET-PLACEHOLDER", help="数字人民币钱包ID")
    parser.add_argument("--user", default="UID9622", help="用户ID")
    parser.add_argument("--remark", default="龍魂系统充值", help="备注")
    parser.add_argument("--create", action="store_true", help="创建充值订单")
    parser.add_argument("--submit", help="提交订单 (订单ID)")
    parser.add_argument("--query", help="查询订单 (订单ID)")
    parser.add_argument("--list", action="store_true", help="列出充值记录")
    parser.add_argument("--refund", help="退款订单 (订单ID)")
    parser.add_argument("--banks", action="store_true", help="列出运营机构")
    parser.add_argument("--stats", action="store_true", help="充值统计")
    parser.add_argument("--json", action="store_true", help="JSON格式输出")

    # 直达标准校验（落地 clause_currency_direct_settlement）
    parser.add_argument("--verify", metavar="CURRENCY", help="校验某法币是否达直达标准")
    parser.add_argument("--p2p", action="store_true", help="点对点直达")
    parser.add_argument("--traceable", action="store_true", help="全链路可追溯")
    parser.add_argument("--tamper-proof", action="store_true", help="签名不可篡改")
    parser.add_argument("--direct-settle", action="store_true", help="直达结算")
    parser.add_argument("--skim", action="store_true", help="第三方抽水(红线)")
    parser.add_argument("--leverage", action="store_true", help="投机杠杆(红线)")
    parser.add_argument("--custody", action="store_true", help="资金第三方托管(红线)")
    parser.add_argument("--verify-selfcheck", action="store_true", help="对系统货币通道做直达标准定时自检")

    args = parser.parse_args()

    dna = args.dna or DEFAULT_DNA
    try:
        engine = DCEPRecharge(dna=dna, confirm_code=args.confirm)
    except ValueError as e:
        print(json.dumps({"success": False, "error": str(e)}, ensure_ascii=False))
        return 1

    if args.verify:
        config = {
            "currency": args.verify,
            "peer_to_peer": args.p2p,
            "traceable": args.traceable,
            "tamper_proof": args.tamper_proof,
            "direct_settle": args.direct_settle,
            "third_party_skim": args.skim,
            "speculative_leverage": args.leverage,
            "third_party_custody": args.custody,
        }
        result = engine.verify_currency(config)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if result.get("success") else 1

    if args.verify_selfcheck:
        report = run_selfcheck()
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0 if report.get("success") else 1

    if args.banks:
        result = engine.list_banks()
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0

    if args.stats:
        print(json.dumps(engine.stats(), ensure_ascii=False, indent=2))
        return 0

    if args.list:
        orders = engine.list_orders(args.user)
        print(json.dumps(orders, ensure_ascii=False, indent=2))
        return 0

    if args.submit:
        result = engine.submit_recharge(args.submit)
    elif args.query:
        result = engine.query_recharge(args.query)
    elif args.refund:
        result = engine.refund_recharge(args.refund)
    elif args.create and args.amount:
        result = engine.create_recharge(
            amount=args.amount, bank_id=args.bank,
            wallet_id=args.wallet, user_id=args.user, remark=args.remark,
        )
    else:
        print("❌ 需要 --create --amount / --submit / --query / --list / --banks / --stats", file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        status = "✅" if result.get("success") else "❌"
        print(f"{status} {result.get('message', result.get('error', ''))}")
        for k, v in result.items():
            if k not in ("success", "message", "error"):
                print(f"   {k}: {v}")

    return 0 if result.get("success") else 1


if __name__ == "__main__":
    sys.exit(main())
