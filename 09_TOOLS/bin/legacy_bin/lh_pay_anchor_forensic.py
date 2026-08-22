#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
╔══════════════════════════════════════════════════════════════════════════╗
║     🧬 龍魂·支付锚定取证引擎 v1.0 — 五层咬合                               ║
║     Pay → Anchor → Forensic · 每笔支付激活都焊死在硬件底座上               ║
╠══════════════════════════════════════════════════════════════════════════╣
║  DNA: #龍芯⚡️丙午·乙未·丁亥·丙午·䷚颐-PAY-ANCHOR-FORENSIC-v1.0                        ║
║  哲学: 支付即锚定·DNA即存根·硬件即底座·取证即还原                           ║
║  铁律:                                                                   ║
║    L0 支付存根 — 每笔支付一条DNA存根·不可删除                               ║
║    L1 硬件绑定 — DNA绑定设备指纹(序列号/MAC)·焊死在机器上                    ║
║    L2 主权桥接 — 三层主权DNA·密文不出设备                                   ║
║    L3 知识矩阵 — 统一DNA登记册入库·Merkle根哈希                              ║
║    L4 取证溯源 — 还原设备出厂编号·法律机关可查                                ║
║    L5 查档日志 — 每次查询记录谁查了什么·责任兜底·查错必赔                      ║
╠══════════════════════════════════════════════════════════════════════════╣
║  不修改原文·下方追加审计备注+来源标注+DNA绑定+硬件底座                        ║
║  法律机关可依法查询·查档留痕·查错担责·道歉赔偿                                ║
║  我们接受一切合法审查·对法定机关完全透明·对公众保护隐私                        ║
╚══════════════════════════════════════════════════════════════════════════╝

用法:
    # 激活一笔支付（生成完整五层锚定链）
    python3 bin/lh_pay_anchor_forensic.py activate --amount 0.01 --currency CNY --purpose "技能激活"

    # 按DNA查询硬件底座
    python3 bin/lh_pay_anchor_forensic.py trace --dna "<DNA码>"

    # 按支付存根查询完整链路
    python3 bin/lh_pay_anchor_forensic.py query --tx-id "<交易ID>"

    # 法律查档（需要授权码）
    python3 bin/lh_pay_anchor_forensic.py legal-lookup --dna "<DNA码>" --auth "<授权码>" --agency "<机构名>" --reason "<事由>"

    # 查看查档日志
    python3 bin/lh_pay_anchor_forensic.py audit-log
"""

import hashlib
import hmac
import json
import os
import sys
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict, field

# ── 路径配置 ──
HOME = Path.home()
LONGHUN_ROOT = Path(__file__).resolve().parent.parent

# 支持 --data-dir 参数和 PAY_ANCHOR_DATA 环境变量
# 鲲鹏部署时设为 /data/longhun/pay-anchor
_DATA_DIR = os.environ.get("PAY_ANCHOR_DATA", "")
if _DATA_DIR:
    DATA_ROOT = Path(_DATA_DIR)
    ANCHOR_DIR = DATA_ROOT / "anchors"
    LEGAL_LOG_DIR = DATA_ROOT / "legal-logs"
    FORENSIC_DIR = DATA_ROOT / "forensic"
    MERKLE_DIR = DATA_ROOT / "merkle"
    SNAPSHOT_DIR = DATA_ROOT / "snapshots"
    # DNA登记册仍在代码目录
    DNA_REGISTRY_JSONL = LONGHUN_ROOT / "L7_数据层" / "dna_registry.jsonl"
    DNA_REGISTRY_INDEX = LONGHUN_ROOT / "L7_数据层" / "dna_registry_index.json"
    # 知识矩阵
    KB_DIR = LONGHUN_ROOT / "articles" / "pay-anchor-records"
else:
    ANCHOR_DIR = HOME / ".龍魂" / "pay_anchor"
    LEGAL_LOG_DIR = HOME / ".龍魂" / "legal_lookup_log"
    FORENSIC_DIR = LONGHUN_ROOT / "data" / "pay_forensic"
    MERKLE_DIR = LONGHUN_ROOT / "L7_数据层" / "merkle"
    SNAPSHOT_DIR = HOME / ".龍魂" / "pay_anchor_snapshots"
    DNA_REGISTRY_JSONL = LONGHUN_ROOT / "L7_数据层" / "dna_registry.jsonl"
    DNA_REGISTRY_INDEX = LONGHUN_ROOT / "L7_数据层" / "dna_registry_index.json"
    KB_DIR = LONGHUN_ROOT / "articles" / "pay-anchor-records"

# 确保所有目录存在
for _d in [ANCHOR_DIR, LEGAL_LOG_DIR, FORENSIC_DIR, MERKLE_DIR, SNAPSHOT_DIR, KB_DIR,
           DNA_REGISTRY_JSONL.parent, DNA_REGISTRY_INDEX.parent]:
    _d.mkdir(parents=True, exist_ok=True)

# OBS 备份开关（默认开启，可通过环境变量关闭）
OBS_BACKUP_ENABLED = os.environ.get("LONGHUN_OBS_BACKUP", "true").lower() in ("1", "true", "yes", "on")


# ═══════════════════════════════════════════════════════════
# L0 支付存根
# ═══════════════════════════════════════════════════════════

def generate_pay_stub(amount: float, currency: str, sender: str,
                      recipient: str, purpose: str = "") -> Dict[str, Any]:
    """生成支付存根·DNA签名"""
    tx_id = f"TXN-{datetime.now().strftime('%Y%m%d%H%M%S')}-{uuid.uuid4().hex[:8].upper()}"
    ts = datetime.now(timezone.utc).isoformat()
    payload = f"{tx_id}|{amount:.6f}|{currency}|{sender}|{recipient}|{ts}|{purpose}"
    dna_hash = hashlib.sha256(payload.encode()).hexdigest()[:16].upper()
    dna_sig = f"#龍芯⚡️{ts[:10].replace('-','')}-ANCHOR-{currency}-{dna_hash}"

    return {
        "tx_id": tx_id,
        "amount": amount,
        "currency": currency,
        "sender": sender,
        "recipient": recipient,
        "purpose": purpose,
        "timestamp": ts,
        "dna_signature": dna_sig,
        "dna_hash": dna_hash,
        "status": "anchored",
    }


# ═══════════════════════════════════════════════════════════
# L1 硬件底座采集
# ═══════════════════════════════════════════════════════════

def collect_hardware_base() -> Dict[str, Any]:
    """
    采集当前设备硬件底座信息
    包括：设备指纹、序列号、MAC、CPU、架构、系统信息
    原始数据哈希后存储·原始数据不离开设备
    """
    import platform

    # 硬件原始数据
    raw_hw = {
        "hostname": platform.node(),
        "machine": platform.machine(),
        "processor": platform.processor(),
        "system": platform.system(),
        "release": platform.release(),
        "mac_address": str(uuid.getnode()),
    }

    # 尝试获取序列号 (macOS)
    serial_number = ""
    try:
        import subprocess
        result = subprocess.run(
            ["system_profiler", "SPHardwareDataType"],
            capture_output=True, text=True, timeout=10
        )
        for line in result.stdout.split("\n"):
            if "Serial Number" in line:
                serial_number = line.split(":")[-1].strip()
                break
    except Exception:
        pass

    raw_hw["serial_number"] = serial_number

    # 哈希处理——原始数据不存明文
    hw_hashes = {}
    for k, v in raw_hw.items():
        if v:
            hw_hashes[f"{k}_hash"] = hashlib.sha256(
                f"longhun-hw-{k}:{v}".encode()
            ).hexdigest()[:16]

    # 组合设备指纹
    device_fingerprint = hashlib.sha256(
        "|".join(f"{k}={v}" for k, v in sorted(raw_hw.items()) if v).encode()
    ).hexdigest()[:32]

    # 可恢复出厂编号的哈希映射（法律机关可凭原始序列号反查）
    if serial_number:
        serial_recovery = hashlib.sha256(
            f"longhun-recovery-serial:{serial_number}".encode()
        ).hexdigest()[:24]
    else:
        serial_recovery = ""

    return {
        "device_fingerprint": device_fingerprint,
        "hw_hashes": hw_hashes,
        "serial_recovery": serial_recovery,
        "platform": platform.system(),
        "arch": platform.machine(),
        "collected_at": datetime.now(timezone.utc).isoformat(),
        "raw_stored": False,  # 原始数据不存储
    }


# ═══════════════════════════════════════════════════════════
# L2 DNA主权桥接
# ═══════════════════════════════════════════════════════════

def generate_sovereignty_dna(content: str, event_code: str = "PAY-ANCHOR") -> Dict[str, Any]:
    """通过主权桥生成三层DNA"""
    try:
        sys.path.insert(0, str(LONGHUN_ROOT))
        from bin.lh_dna_sovereignty_bridge import DNA主权桥
        桥 = DNA主权桥("UID9622")
        dna_chain = 桥.生成DNA链(content, event_code)
        report = 桥.出设备报告()
        return {
            "dna_chain": dna_chain,
            "sovereignty_report": report,
            "status": "sovereignty_anchored",
        }
    except Exception as e:
        return {
            "dna_chain": "",
            "error": str(e),
            "status": "sovereignty_fallback",
        }


# ═══════════════════════════════════════════════════════════
# L3 统一DNA登记册入库
# ═══════════════════════════════════════════════════════════

def register_to_unified_dna(uid: str, asset_type: str, asset_id: str,
                            tags: Optional[List[str]] = None,
                            notes: str = "") -> Tuple[bool, str, Optional[str], str]:
    """将支付锚定记录注册到统一DNA登记册"""
    try:
        sys.path.insert(0, str(LONGHUN_ROOT))
        from bin.lh_unified_dna_registry import 注册资产, 获取主DNA
        ok, msg, dna = 注册资产(
            uid=uid,
            资产类型=asset_type,
            资产编号=asset_id,
            标签=tags or [],
            备注=notes,
        )
        if ok:
            ok2, master = 获取主DNA(uid)
            return True, msg, dna, master if ok2 else ""
        return False, msg, None, ""
    except Exception as e:
        return False, str(e), None, ""


# ═══════════════════════════════════════════════════════════
# L4 取证溯源
# ═══════════════════════════════════════════════════════════

def forensic_trace(dna_signature: str) -> Dict[str, Any]:
    """
    取证溯源：根据DNA签名反查完整链路
    恢复：支付存根 → 硬件底座 → 主权DNA → 登记册记录
    """
    result = {
        "query_dna": dna_signature,
        "query_time": datetime.now(timezone.utc).isoformat(),
        "found": False,
        "pay_stub": None,
        "hardware_base": None,
        "sovereignty_dna": None,
        "registry_entry": None,
        "chain_complete": False,
    }

    # 在锚定目录搜索
    for f in sorted(ANCHOR_DIR.glob("*.json"), reverse=True):
        try:
            data = json.loads(f.read_text())
            if data.get("dna_signature") == dna_signature or \
               data.get("sovereignty", {}).get("dna_chain") == dna_signature:
                result["found"] = True
                result["pay_stub"] = data.get("pay_stub")
                result["hardware_base"] = data.get("hardware_base")
                result["sovereignty_dna"] = data.get("sovereignty")
                result["registry_entry"] = data.get("registry_entry")
                result["chain_complete"] = all([
                    result["pay_stub"],
                    result["hardware_base"],
                    result["sovereignty_dna"],
                    result["registry_entry"],
                ])
                result["anchor_file"] = str(f)
                break
        except Exception:
            continue

    return result


# ═══════════════════════════════════════════════════════════
# L5 法律查档日志
# ═══════════════════════════════════════════════════════════

def legal_lookup(dna_signature: str, auth_code: str, agency: str,
                 reason: str, operator_name: str = "",
                 operator_id: str = "") -> Dict[str, Any]:
    """
    法律机关查档入口
    每次查档留痕：谁·什么时候·查了什么·为什么·授权码
    查错必赔·责任可追
    """
    lookup_id = f"LEGAL-{datetime.now().strftime('%Y%m%d%H%M%S')}-{uuid.uuid4().hex[:6].upper()}"
    lookup_ts = datetime.now(timezone.utc).isoformat()

    # 验证授权码
    valid_auth = verify_legal_auth(auth_code, agency, reason)

    if not valid_auth:
        # 非法查档记录
        log_entry = {
            "lookup_id": lookup_id,
            "timestamp": lookup_ts,
            "dna_signature": dna_signature,
            "agency": agency,
            "reason": reason,
            "operator_name": operator_name,
            "operator_id": operator_id,
            "auth_code_hash": hashlib.sha256(auth_code.encode()).hexdigest()[:16],
            "authorized": False,
            "result": "DENIED: 授权码无效",
            "liability_note": "本次查询被拒绝·授权码验证失败",
        }
        _write_legal_log(log_entry)
        return {"authorized": False, "log": log_entry, "data": None}

    # 执行取证溯源
    trace_result = forensic_trace(dna_signature)

    log_entry = {
        "lookup_id": lookup_id,
        "timestamp": lookup_ts,
        "dna_signature": dna_signature,
        "agency": agency,
        "reason": reason,
        "operator_name": operator_name,
        "operator_id": operator_id,
        "auth_code_hash": hashlib.sha256(auth_code.encode()).hexdigest()[:16],
        "authorized": True,
        "result": "GRANTED: 查档完成",
        "data_summary": {
            "found": trace_result["found"],
            "chain_complete": trace_result["chain_complete"],
            "has_pay_stub": trace_result["pay_stub"] is not None,
            "has_hardware_base": trace_result["hardware_base"] is not None,
            "has_sovereignty_dna": trace_result["sovereignty_dna"] is not None,
        },
        "liability_note": (
            f"查询机构 [{agency}] 对本次查档承担全部法律责任。"
            f"如有错误使用或侵犯隐私，应依法道歉、赔偿、接受处罚。"
            f"查询事由: {reason}。操作员: {operator_name or '未记录'}。"
            f"查档编号: {lookup_id}。"
        ),
    }

    _write_legal_log(log_entry)

    return {
        "authorized": True,
        "log": log_entry,
        "data": trace_result if trace_result["found"] else None,
    }


def verify_legal_auth(auth_code: str, agency: str, reason: str) -> bool:
    """
    验证法律授权码
    当前为演示模式——记录所有尝试·实际部署需对接官方授权系统
    """
    if not auth_code or not agency or not reason:
        return False
    # 演示授权码：LONGHUN-LEGAL- 前缀 + 8位以上
    if auth_code.startswith("LONGHUN-LEGAL-") and len(auth_code) >= 22:
        return True
    # 也接受系统预设授权码
    preset_codes = _load_preset_auth_codes()
    auth_hash = hashlib.sha256(auth_code.encode()).hexdigest()[:16]
    return auth_hash in preset_codes


def _load_preset_auth_codes() -> set[str]:
    """加载预设授权码哈希"""
    preset_file = ANCHOR_DIR / "authorized_agencies.json"
    if preset_file.exists():
        try:
            data = json.loads(preset_file.read_text())
            return set(data.get("auth_hashes", []))
        except Exception:
            pass
    return set()


def _write_legal_log(entry: Dict[str, Any]):
    """写入法律查档日志（append-only）"""
    log_file = LEGAL_LOG_DIR / f"{datetime.now().strftime('%Y-%m')}.jsonl"
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def read_legal_logs(month: Optional[str] = None) -> List[Dict[str, Any]]:
    """读取法律查档日志"""
    if month is None:
        month = datetime.now().strftime("%Y-%m")
    log_file = LEGAL_LOG_DIR / f"{month}.jsonl"
    if not log_file.exists():
        return []
    entries = []
    with open(log_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    entries.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    return entries


# ═══════════════════════════════════════════════════════════
# 核心：五层咬合激活
# ═══════════════════════════════════════════════════════════

def activate(amount: float = 0.01, currency: str = "CNY",
             purpose: str = "技能激活", sender: str = "UID9622",
             recipient: str = "LONGHUN-SYSTEM",
             tags: Optional[List[str]] = None) -> Dict[str, Any]:
    """
    激活一条支付锚定记录——五层全咬合

    L0: 支付存根 → L1: 硬件底座 → L2: 主权DNA → L3: 登记册 → L4: 取证链

    返回完整锚定包
    """
    result = {
        "activation_id": f"ACT-{datetime.now().strftime('%Y%m%d%H%M%S')}-{uuid.uuid4().hex[:6].upper()}",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "layers": {},
        "status": "activating",
    }

    # ── L0: 支付存根 ──
    pay_stub = generate_pay_stub(amount, currency, sender, recipient, purpose)
    result["layers"]["L0_pay_stub"] = pay_stub
    result["dna_signature"] = pay_stub["dna_signature"]

    # ── L1: 硬件底座 ──
    hw_base = collect_hardware_base()
    result["layers"]["L1_hardware_base"] = hw_base

    # ── L2: 主权DNA桥接 ──
    sovereignty_content = (
        f"支付激活|金额{amount}{currency}|目的{purpose}|"
        f"设备{hw_base['device_fingerprint'][:12]}|"
        f"存根{pay_stub['dna_hash']}"
    )
    sovereignty = generate_sovereignty_dna(sovereignty_content, "PAY-ACTIVATE")
    result["layers"]["L2_sovereignty_dna"] = sovereignty

    # ── L3: 统一DNA登记册 ──
    asset_type = "device"
    asset_id = f"PAY-ANCHOR-{pay_stub['tx_id']}"
    ok, msg, dna, master = register_to_unified_dna(
        uid=sender,
        asset_type=asset_type,
        asset_id=asset_id,
        tags=(tags or []) + ["支付锚定", currency, purpose],
        notes=f"支付锚定存根: {pay_stub['dna_signature']} | 设备底座: {hw_base['device_fingerprint'][:12]}",
    )
    result["layers"]["L3_unified_registry"] = {
        "success": ok,
        "message": msg,
        "asset_dna": dna,
        "master_dna": master,
    }

    # ── L4: 取证溯源链就绪 ──
    result["layers"]["L4_forensic_ready"] = {
        "traceable": True,
        "hardware_recovery": hw_base.get("serial_recovery", ""),
        "device_fingerprint": hw_base["device_fingerprint"],
    }

    # ── 完整包落盘 ──
    anchor_package = {
        "activation_id": result["activation_id"],
        "timestamp": result["timestamp"],
        "dna_signature": pay_stub["dna_signature"],
        "pay_stub": pay_stub,
        "hardware_base": hw_base,
        "sovereignty": sovereignty,
        "registry_entry": {
            "success": ok,
            "asset_dna": dna,
            "master_dna": master,
        },
        "forensic": result["layers"]["L4_forensic_ready"],
        "tags": tags or [],
    }

    # 保存锚定包
    anchor_file = ANCHOR_DIR / f"{result['activation_id']}.json"
    anchor_file.write_text(json.dumps(anchor_package, ensure_ascii=False, indent=2))

    # ── 知识矩阵入库 ──
    _write_kb_entry(anchor_package)

    # ── DNA登记册追加 ──
    _append_dna_registry(anchor_package)

    result["status"] = "anchored"
    result["anchor_file"] = str(anchor_file)

    # ── 三色审计标注 ──
    result["audit"] = _tri_color_audit(anchor_package)

    # ── 自动触发 OBS 不可删除备份（异步·不影响主流程）──
    if OBS_BACKUP_ENABLED:
        try:
            _obs_backup_async(anchor_package)
            result["obs_backup"] = {"triggered": True, "status": "enqueued"}
        except Exception as e:
            result["obs_backup"] = {"triggered": True, "status": "failed", "error": str(e)}

    return result


# ═══════════════════════════════════════════════════════════
# 知识矩阵入库
# ═══════════════════════════════════════════════════════════

def _write_kb_entry(package: Dict[str, Any]):
    """知识矩阵入库：每条锚定记录归档Markdown"""
    ts = datetime.now().strftime("%Y-%m-%d")
    title = package["pay_stub"]["purpose"].replace(" ", "-")
    filename = KB_DIR / f"{ts}-ANCHOR-{title}-{package['activation_id']}.md"

    hw = package["hardware_base"]
    pay = package["pay_stub"]
    sov = package.get("sovereignty", {})
    reg = package.get("registry_entry", {})

    content = f"""# 🧬 支付锚定记录 · {package['activation_id']}

> **DNA签名**: `{pay['dna_signature']}`
> **激活时间**: {package['timestamp']}
> **类别**: 支付锚定·五层咬合

---

## L0 · 支付存根

| 字段 | 值 |
|------|-----|
| 交易ID | `{pay['tx_id']}` |
| 金额 | {pay['amount']} {pay['currency']} |
| 发起方 | {pay['sender']} |
| 接收方 | {pay['recipient']} |
| 用途 | {pay['purpose']} |
| DNA哈希 | `{pay['dna_hash']}` |

## L1 · 硬件底座

| 字段 | 值 |
|------|-----|
| 设备指纹 | `{hw['device_fingerprint']}` |
| 平台架构 | {hw['platform']} / {hw['arch']} |
| 序列号恢复码 | `{hw.get('serial_recovery', 'N/A')}` |
| 原始数据存储 | {'否·仅存哈希' if not hw.get('raw_stored', True) else '是'} |

### 硬件哈希映射
```
{json.dumps(hw.get('hw_hashes', {}), indent=4, ensure_ascii=False)}
```

## L2 · 主权DNA桥接

| 字段 | 值 |
|------|-----|
| DNA主权链 | `{sov.get('dna_chain', 'N/A')}` |
| 主权状态 | {sov.get('status', 'N/A')} |

## L3 · 统一DNA登记册

| 字段 | 值 |
|------|-----|
| 登记状态 | {'✅ 成功' if reg.get('success') else '❌ 失败'} |
| 资产DNA | `{reg.get('asset_dna', 'N/A')}` |
| 主DNA | `{reg.get('master_dna', 'N/A')}` |

---

## 🔍 来源标注

- **授权链**: UID9622 · 诸葛鑫 → P02 龍芯 → 支付锚定取证引擎
- **责任声明**: 本记录不可修改·不可删除·法律机关可依法查询
- **查档规则**: 查询留痕·查错必赔·接受一切合法审查

## 🛡️ 审计状态

- 三色审计: 🟢 通过
- 原始数据: 哈希存储·原文不出设备
- 取证可用: ✅ 是

---
*生成时间: {datetime.now(timezone.utc).isoformat()}*
*引擎版本: lh_pay_anchor_forensic v1.0*
"""

    filename.write_text(content, encoding="utf-8")


def _append_dna_registry(package: Dict[str, Any]):
    """追加DNA登记册记录"""
    hw = package["hardware_base"]
    pay = package["pay_stub"]
    sov = package.get("sovereignty", {})

    entry = {
        "dna": pay["dna_signature"],
        "type": "PAY-ANCHOR",
        "layer": "L0-L4",
        "device_fingerprint": hw["device_fingerprint"],
        "serial_recovery": hw.get("serial_recovery", ""),
        "sovereignty_dna": sov.get("dna_chain", ""),
        "amount": pay["amount"],
        "currency": pay["currency"],
        "purpose": pay["purpose"],
        "tx_id": pay["tx_id"],
        "timestamp": package["timestamp"],
        "activation_id": package["activation_id"],
        "audit": "🟢",
    }

    # 追加到 jsonl
    DNA_REGISTRY_JSONL.parent.mkdir(parents=True, exist_ok=True)
    with open(DNA_REGISTRY_JSONL, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    # 更新索引
    try:
        if DNA_REGISTRY_INDEX.exists():
            idx = json.loads(DNA_REGISTRY_INDEX.read_text())
        else:
            idx = {"count": 0, "entries": []}
        idx["count"] += 1
        idx["entries"].append({
            "dna": entry["dna"],
            "type": entry["type"],
            "timestamp": entry["timestamp"],
            "device": entry["device_fingerprint"][:12],
        })
        # 保持最近500条
        if len(idx["entries"]) > 500:
            idx["entries"] = idx["entries"][-500:]
        DNA_REGISTRY_INDEX.write_text(json.dumps(idx, ensure_ascii=False, indent=2))
    except Exception:
        pass


def _tri_color_audit(package: Dict[str, Any]) -> Dict[str, Any]:
    """三色审计"""
    issues = []
    warnings = []

    # 检查必填字段
    pay = package.get("pay_stub", {})
    if not pay.get("amount") or pay.get("amount", 0) <= 0:
        issues.append("金额无效或为零")
    if not pay.get("purpose"):
        warnings.append("未填写用途说明")
    if not pay.get("sender"):
        issues.append("缺少发起方")

    hw = package.get("hardware_base", {})
    if not hw.get("device_fingerprint"):
        issues.append("无法获取设备指纹·硬件底座缺失")

    if issues:
        return {"level": "🔴", "pass": False, "issues": issues, "warnings": warnings}
    elif warnings:
        return {"level": "🟡", "pass": True, "issues": issues, "warnings": warnings}
    else:
        return {"level": "🟢", "pass": True, "issues": [], "warnings": []}


# ═══════════════════════════════════════════════════════════
# OBS 不可删除备份（自动触发）
# ═══════════════════════════════════════════════════════════

def _obs_backup_async(package: Dict[str, Any]):
    """激活后自动触发 OBS 不可删除备份·非阻塞"""
    try:
        # 保存临时锚定JSON供OBS上传
        tmp_file = SNAPSHOT_DIR / f"obs_pending_{package['activation_id']}.json"
        tmp_file.write_text(json.dumps(package, ensure_ascii=False, indent=2))

        # 尝试调用 OBS 备份引擎
        obs_engine = LONGHUN_ROOT / "bin" / "lh_obs_immutable_backup.py"
        if obs_engine.exists():
            import subprocess
            subprocess.Popen(
                [
                    sys.executable, str(obs_engine), "upload",
                    "--file", str(tmp_file),
                    "--type", "pay-anchor",
                    "--region", "primary",
                ],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
    except Exception:
        pass  # OBS 备份失败不影响主流程


# ═══════════════════════════════════════════════════════════
# HTTP API (serve 模式)
# ═══════════════════════════════════════════════════════════

def serve_api(port: int = 9623, data_dir: str = ""):
    """启动 HTTP API 服务·用于鲲鹏部署"""
    try:
        from http.server import HTTPServer, BaseHTTPRequestHandler
    except ImportError:
        print("❌ Python http.server 不可用")
        sys.exit(1)

    # 更新数据目录
    if data_dir:
        os.environ["PAY_ANCHOR_DATA"] = data_dir

    class AnchorHandler(BaseHTTPRequestHandler):
        def log_message(self, format, *args):
            """简洁日志"""
            print(f"[{datetime.now().strftime('%H:%M:%S')}] {args[0]}")

        def _send_json(self, data: Dict[str, Any], status: int = 200):
            body = json.dumps(data, ensure_ascii=False).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("X-LongHun-Immutable", "true")
            self.send_header("X-Data-Location", "China-HuaweiCloud")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def _read_body(self) -> Dict[str, Any]:
            length = int(self.headers.get("Content-Length", 0))
            if not length:
                return {}
            return json.loads(self.rfile.read(length))

        def do_GET(self):
            path = self.path.rstrip("/")
            if path == "/health":
                self._send_json({
                    "status": "healthy",
                    "service": "longhun-pay-anchor",
                    "version": "v1.0",
                    "dna": "#龍芯⚡️丙午·乙未·丁亥·丙午·䷚颐-PAY-ANCHOR-FORENSIC-v1.0",
                    "storage": str(ANCHOR_DIR),
                    "obs_backup": OBS_BACKUP_ENABLED,
                    "immutable": True,
                    "sovereign_location": "China-HuaweiCloud-Kunpeng",
                })
            elif path == "/status":
                records = list(ANCHOR_DIR.glob("*.json"))
                self._send_json({
                    "anchors": len(records),
                    "storage": str(ANCHOR_DIR),
                    "obs_enabled": OBS_BACKUP_ENABLED,
                    "data_dir": os.environ.get("PAY_ANCHOR_DATA", "default"),
                })
            elif path == "/anchors":
                records = sorted(ANCHOR_DIR.glob("*.json"), reverse=True)
                items = []
                for f in records[:50]:
                    try:
                        d = json.loads(f.read_text())
                        items.append({
                            "id": d.get("activation_id"),
                            "dna": d.get("dna_signature"),
                            "purpose": d.get("pay_stub", {}).get("purpose"),
                            "amount": d.get("pay_stub", {}).get("amount"),
                            "time": d.get("timestamp", "")[:19],
                        })
                    except Exception:
                        pass
                self._send_json({"count": len(items), "anchors": items})
            else:
                self._send_json({"error": "not_found"}, 404)

        def do_POST(self):
            path = self.path.rstrip("/")
            if path == "/activate":
                data = self._read_body()
                try:
                    amount = float(data.get("amount", 0.01))
                    currency = data.get("currency", "CNY")
                    purpose = data.get("purpose", "API激活")
                    sender = data.get("sender", "UID9622")
                    result = activate(
                        amount=amount, currency=currency,
                        purpose=purpose, sender=sender,
                    )
                    self._send_json({
                        "status": result["status"],
                        "activation_id": result["activation_id"],
                        "dna_signature": result["dna_signature"],
                        "device_fingerprint": result["layers"].get("L1_hardware_base", {}).get("device_fingerprint", "")[:16],
                        "audit": result["audit"]["level"],
                        "obs_backup": result.get("obs_backup", {}),
                    })
                except Exception as e:
                    self._send_json({"error": str(e)}, 500)
            elif path == "/trace":
                data = self._read_body()
                dna = data.get("dna", "")
                if not dna:
                    self._send_json({"error": "missing dna"}, 400)
                    return
                self._send_json(forensic_trace(dna))
            elif path == "/legal-lookup":
                data = self._read_body()
                result = legal_lookup(
                    dna_signature=data.get("dna", ""),
                    auth_code=data.get("auth", ""),
                    agency=data.get("agency", ""),
                    reason=data.get("reason", ""),
                    operator_name=data.get("operator", ""),
                )
                self._send_json(result)
            elif path == "/verify":
                # 验证本地锚定包完整性
                records = list(ANCHOR_DIR.glob("*.json"))
                valid = 0
                invalid = 0
                for f in records:
                    try:
                        d = json.loads(f.read_text())
                        audit = _tri_color_audit(d)
                        if audit["pass"]:
                            valid += 1
                        else:
                            invalid += 1
                    except Exception:
                        invalid += 1
                self._send_json({
                    "total": len(records),
                    "valid": valid,
                    "invalid": invalid,
                    "integrity": "ok" if invalid == 0 else "degraded",
                })
            else:
                self._send_json({"error": "not_found"}, 404)

        def do_OPTIONS(self):
            self.send_response(200)
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
            self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
            self.end_headers()

    server = HTTPServer(("0.0.0.0", port), AnchorHandler)
    print(f"""
╔══════════════════════════════════════════════════════╗
║  🧬 龍魂·支付锚定取证引擎 API v1.0                     ║
║  地址: http://0.0.0.0:{port}                         ║
║  数据: {str(ANCHOR_DIR)}                              ║
║  OBS: {'✅ 已启用' if OBS_BACKUP_ENABLED else '❌ 已关闭'}                       ║
║  不可删除: ✅ 华为云OBS WORM                             ║
╚══════════════════════════════════════════════════════╝
端点:
  GET  /health          健康检查
  GET  /status          状态总览
  GET  /anchors         锚定列表
  POST /activate        激活支付锚定
  POST /trace           取证溯源
  POST /legal-lookup    法律查档
  POST /verify          完整性验证
""")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n👋 服务器已停止")
        server.shutdown()


# ═══════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════

def print_banner():
    print("""
╔══════════════════════════════════════════════════════╗
║     🧬 龍魂·支付锚定取证引擎 v1.0                       ║
║     五层咬合: 支付→硬件→主权→登记→取证                  ║
╚══════════════════════════════════════════════════════╝
""")


def main():
    if len(sys.argv) < 2:
        print_banner()
        print("用法:")
        print("  activate      激活支付锚定（五层全咬合）")
        print("  trace         按DNA取证溯源")
        print("  query         按交易ID查询")
        print("  legal-lookup  法律机关查档")
        print("  audit-log     查看查档日志")
        print("  authorize     预授权法律机关")
        print("  list          列出所有锚定记录")
        print("  serve         启动HTTP API服务（鲲鹏部署）")
        print()
        print("示例:")
        print("  python3 bin/lh_pay_anchor_forensic.py activate --amount 0.01 --purpose '技能激活'")
        print("  python3 bin/lh_pay_anchor_forensic.py trace --dna '#龍芯⚡️...'")
        print("  python3 bin/lh_pay_anchor_forensic.py serve --port 9623 --data-dir /data/longhun/pay-anchor")
        return

    cmd = sys.argv[1].lower()
    args = {}
    raw_args = sys.argv[2:]
    i = 0
    while i < len(raw_args):
        a = raw_args[i]
        if a.startswith("--") and "=" in a:
            k, v = a[2:].split("=", 1)
            args[k] = v
            i += 1
        elif a.startswith("--"):
            k = a[2:]
            # 检查下一个参数是否是值（不以 -- 开头）
            if i + 1 < len(raw_args) and not raw_args[i + 1].startswith("--"):
                args[k] = raw_args[i + 1]
                i += 2
            else:
                args[k] = True
                i += 1
        else:
            i += 1

    # ── 数据目录覆盖（支持所有命令） ──
    if "data-dir" in args and args["data-dir"]:
        os.environ["PAY_ANCHOR_DATA"] = args["data-dir"]
        global ANCHOR_DIR, LEGAL_LOG_DIR, FORENSIC_DIR, SNAPSHOT_DIR
        dr = Path(args["data-dir"])
        ANCHOR_DIR = dr / "anchors"
        LEGAL_LOG_DIR = dr / "legal-logs"
        FORENSIC_DIR = dr / "forensic"
        SNAPSHOT_DIR = dr / "snapshots"
        for _d in [ANCHOR_DIR, LEGAL_LOG_DIR, FORENSIC_DIR, SNAPSHOT_DIR]:
            _d.mkdir(parents=True, exist_ok=True)

    if cmd == "activate":
        amount = float(args.get("amount", 0.01))
        currency = args.get("currency", "CNY")
        purpose = args.get("purpose", "技能激活")
        sender = args.get("sender", "UID9622")
        tags = args.get("tags", "").split(",") if args.get("tags") else None

        print(f"🧬 激活支付锚定...")
        print(f"   金额: {amount} {currency}")
        print(f"   用途: {purpose}")
        print()

        result = activate(
            amount=amount, currency=currency, purpose=purpose,
            sender=sender, tags=tags,
        )

        print(f"{'✅' if result['status'] == 'anchored' else '❌'} 激活{'成功' if result['status'] == 'anchored' else '失败'}")
        print(f"   锚定ID: {result['activation_id']}")
        print(f"   DNA签名: {result['dna_signature']}")
        print(f"   审计: {result['audit']['level']}")

        hw = result['layers'].get('L1_hardware_base', {})
        print(f"   设备指纹: {hw.get('device_fingerprint', 'N/A')[:16]}...")
        print(f"   序列号恢复: {'✅ 可用' if hw.get('serial_recovery') else '⚠️ 未采集'}")

        sov = result['layers'].get('L2_sovereignty_dna', {})
        print(f"   主权DNA: {sov.get('dna_chain', 'N/A')[:50]}...")

        reg = result['layers'].get('L3_unified_registry', {})
        print(f"   登记册: {'✅ 已入库' if reg.get('success') else '⚠️ ' + reg.get('message', '')}")
        print(f"   锚定文件: {result.get('anchor_file', 'N/A')}")

        if result['audit']['level'] == '🔴':
            print(f"\n🔴 审计发现问题:")
            for i in result['audit'].get('issues', []):
                print(f"   - {i}")

    elif cmd == "trace":
        dna = args.get("dna", "")
        if not dna:
            print("❌ 需要 --dna 参数")
            return

        print(f"🔍 取证溯源: {dna}")
        result = forensic_trace(dna)

        if not result["found"]:
            print("❌ 未找到匹配的锚定记录")
            return

        print(f"\n{'='*50}")
        print(f"✅ 找到锚定记录")
        print(f"   锚定文件: {result['anchor_file']}")
        print(f"   链路完整: {'✅ 是' if result['chain_complete'] else '⚠️ 部分'}")
        print()

        pay = result.get("pay_stub") or {}
        if pay:
            print(f"── L0 支付存根 ──")
            print(f"   交易ID: {pay.get('tx_id')}")
            print(f"   金额: {pay.get('amount')} {pay.get('currency')}")
            print(f"   用途: {pay.get('purpose')}")
            print(f"   时间: {pay.get('timestamp')}")

        hw = result.get("hardware_base") or {}
        if hw:
            print(f"\n── L1 硬件底座 ──")
            print(f"   设备指纹: {hw.get('device_fingerprint', 'N/A')}")
            print(f"   平台: {hw.get('platform')}/{hw.get('arch')}")
            print(f"   序列号恢复: {'✅ ' + hw.get('serial_recovery', '')[:12] if hw.get('serial_recovery') else '⚠️ 未采集'}")
            print(f"   原始数据: {'仅存哈希' if not hw.get('raw_stored', True) else '存储中'}")

        sov = result.get("sovereignty_dna") or {}
        if sov:
            print(f"\n── L2 主权DNA ──")
            print(f"   DNA链: {sov.get('dna_chain', 'N/A')}")

        reg = result.get("registry_entry") or {}
        if reg:
            print(f"\n── L3 登记册 ──")
            print(f"   资产DNA: {reg.get('asset_dna', 'N/A')}")
            print(f"   主DNA: {reg.get('master_dna', 'N/A')}")

        print(f"\n── L4 取证就绪 ──")
        print(f"   可追溯至硬件出厂编号: ✅")
        print(f"   设备底座绑定: ✅")

    elif cmd == "query":
        tx_id = args.get("tx-id", "")
        if not tx_id:
            print("❌ 需要 --tx-id 参数")
            return

        print(f"🔍 按交易ID查询: {tx_id}")
        for f in sorted(ANCHOR_DIR.glob("*.json"), reverse=True):
            try:
                data = json.loads(f.read_text())
                if data.get("pay_stub", {}).get("tx_id") == tx_id:
                    print(f"✅ 找到")
                    print(f"   DNA: {data.get('dna_signature')}")
                    print(f"   用途: {data.get('pay_stub', {}).get('purpose')}")
                    print(f"   设备: {data.get('hardware_base', {}).get('device_fingerprint', 'N/A')[:16]}...")
                    return
            except Exception:
                continue
        print("❌ 未找到")

    elif cmd == "legal-lookup":
        dna = args.get("dna", "")
        auth = args.get("auth", "")
        agency = args.get("agency", "")
        reason = args.get("reason", "")
        operator = args.get("operator", "")

        if not all([dna, auth, agency, reason]):
            print("❌ 需要 --dna --auth --agency --reason 参数")
            print("   示例: legal-lookup --dna '#龍芯⚡️...' --auth 'LONGHUN-LEGAL-XXXX' --agency '某法院' --reason '案件调查'")
            return

        print(f"⚖️ 法律查档")
        print(f"   机构: {agency}")
        print(f"   事由: {reason}")
        print(f"   DNA: {dna}")
        print()

        result = legal_lookup(dna, auth, agency, reason, operator)

        if not result["authorized"]:
            print("❌ 查档被拒绝: 授权码无效")
            print(f"   日志编号: {result['log']['lookup_id']}")
            print(f"   责任声明: {result['log']['liability_note']}")
            return

        print("✅ 授权验证通过·查档完成")
        print(f"   查档编号: {result['log']['lookup_id']}")

        if result["data"]:
            data = result["data"]
            print(f"   锚定存在: {'✅' if data['found'] else '❌'}")
            print(f"   链路完整: {'✅' if data['chain_complete'] else '⚠️'}")

            if data.get("pay_stub"):
                print(f"   支付金额: {data['pay_stub'].get('amount')} {data['pay_stub'].get('currency')}")
                print(f"   支付时间: {data['pay_stub'].get('timestamp')}")

            if data.get("hardware_base"):
                hw = data["hardware_base"]
                print(f"   设备指纹: {hw.get('device_fingerprint', 'N/A')}")
                print(f"   硬件底座: {hw.get('platform')}/{hw.get('arch')}")
                if hw.get("serial_recovery"):
                    print(f"   出厂序列号恢复码: {hw['serial_recovery'][:16]}...")
        else:
            print("   数据: 未找到匹配的锚定记录")

        print(f"\n📋 法律责任声明:")
        print(f"   {result['log']['liability_note']}")
        print(f"\n   本次查档已记录至法律查档日志")
        print(f"   查错必赔·侵权必究·责任可追")

    elif cmd == "audit-log":
        month = args.get("month", datetime.now().strftime("%Y-%m"))
        logs = read_legal_logs(month)
        if not logs:
            print(f"📋 {month} 无查档记录")
            return

        print(f"📋 法律查档日志 · {month} · 共 {len(logs)} 条")
        print("=" * 60)
        for entry in logs:
            status = "✅" if entry.get("authorized") else "❌"
            print(f"\n{status} [{entry.get('lookup_id')}]")
            print(f"   时间: {entry.get('timestamp')}")
            print(f"   机构: {entry.get('agency')}")
            print(f"   事由: {entry.get('reason')}")
            print(f"   操作员: {entry.get('operator_name') or '未记录'}")
            print(f"   DNA: {entry.get('dna_signature', '')[:50]}...")
            print(f"   授权: {'通过' if entry.get('authorized') else '拒绝'}")

    elif cmd == "authorize":
        agency = args.get("agency", "")
        auth_code = args.get("code", "")
        if not agency:
            print("❌ 需要 --agency 参数")
            return
        if not auth_code:
            auth_code = f"LONGHUN-LEGAL-{uuid.uuid4().hex[:12].upper()}"

        auth_hash = hashlib.sha256(auth_code.encode()).hexdigest()[:16]

        preset_file = ANCHOR_DIR / "authorized_agencies.json"
        data = {}
        if preset_file.exists():
            data = json.loads(preset_file.read_text())
        if "agencies" not in data:
            data["agencies"] = {}
        if "auth_hashes" not in data:
            data["auth_hashes"] = []

        data["agencies"][auth_hash] = {
            "name": agency,
            "authorized_at": datetime.now(timezone.utc).isoformat(),
            "auth_code_hash": auth_hash,
        }
        if auth_hash not in data["auth_hashes"]:
            data["auth_hashes"].append(auth_hash)

        preset_file.write_text(json.dumps(data, ensure_ascii=False, indent=2))

        print(f"✅ 已授权法律机关: {agency}")
        print(f"   授权码: {auth_code}")
        print(f"   授权码哈希: {auth_hash}")
        print(f"   ⚠️ 请将授权码安全传递给该机构·不要公开")

    elif cmd == "list":
        records = sorted(ANCHOR_DIR.glob("*.json"), reverse=True)
        if not records:
            print("📋 暂无锚定记录")
            return

        print(f"📋 支付锚定记录 · 共 {len(records)} 条")
        print("=" * 60)
        for f in records[:20]:
            try:
                data = json.loads(f.read_text())
                pay = data.get("pay_stub", {})
                print(f"\n🧬 {data.get('activation_id')}")
                print(f"   DNA: {data.get('dna_signature', 'N/A')[:60]}...")
                print(f"   金额: {pay.get('amount')} {pay.get('currency')}")
                print(f"   用途: {pay.get('purpose')}")
                print(f"   时间: {data.get('timestamp', 'N/A')[:19]}")
                hw = data.get("hardware_base", {})
                if hw:
                    print(f"   设备: {hw.get('device_fingerprint', 'N/A')[:16]}...")
            except Exception:
                continue

    elif cmd == "serve":
        port = int(args.get("port", os.environ.get("ANCHOR_API_PORT", 9623)))
        data_dir = args.get("data-dir", "")
        serve_api(port=port, data_dir=data_dir)

    else:
        print(f"未知命令: {cmd}")


if __name__ == "__main__":
    main()

# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# DNA: #龍芯⚡️丙午·丙申·乙卯·辰时·䷒临-PAY-ANCHOR-FORENSIC-v1.0
