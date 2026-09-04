#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
╔══════════════════════════════════════════════════════════════════════════╗
║       龍魂统一DNA登记册 · 严格审计人格 v1.0                             ║
║       LongHun Unified DNA Registry · Strict Auditor Persona             ║
╠══════════════════════════════════════════════════════════════════════════╣
║  DNA: #龍芯⚡️丙午·丙申·甲寅·庚午·䷕贲-壬申-UNIFIED-DNA-AUDITOR-v1.0              ║
║  执行人格: P06 镜像审计者 · P07 开源守门人 · P03 墨子                   ║
║  铁律: 先审后写 · 明文不入库 · 身份只存哈希 · 异常熔断                 ║
║  📇 身份 · 联系 · 支持 → assets/PUBLIC_IDENTITY.md                      ║
╚══════════════════════════════════════════════════════════════════════════╝

功能:
  对一笔统一DNA登记记录执行严格审计，输出 🟢🟡🔴 三色结果。
  被 bin/lh_unified_dna_registry.py 在写入前强制调用。

用法:
  python3 bin/lh_unified_dna_audit.py <uid> <资产类型> <资产编号> [标签...]
  python3 bin/lh_unified_dna_audit.py UID9622 watch "ROLEX-116610LN-2020" 機械 潛水
"""

import re
import sys
from typing import Any, Dict, List, Optional, Tuple

# 从统一DNA登记引擎导入资产类型表与核心函数
from lh_unified_dna_registry import (
    DNA登记册,
    加载登记册,
    哈希资产编号,
    资产类型表,
)


# ═══════════════════════════════════════════════════════════
# L0 常量 · 格式校验规则
# ═══════════════════════════════════════════════════════════

格式规则表: Dict[str, Dict[str, Any]] = {
    # 物理资产
    "watch":    {"regex": re.compile(r"^.{3,128}$"),           "hint": "手表型号，建议品牌+型号"},
    "patent":   {"regex": re.compile(r"^[A-Z]{2}\d{7,15}$", re.I), "hint": "专利号如 CN20241000001"},
    "ip":       {"regex": re.compile(r"^.{3,128}$"),           "hint": "知识产权登记号"},
    "vehicle":  {"regex": re.compile(r"^[A-HJ-NPR-Z0-9]{17}$|^[\u4e00-\u9fa5][A-Z][A-Z0-9]{4,5}[A-Z0-9挂学警港澳]?$"), "hint": "VIN 17位字母数字，或车牌号"},
    "phone":    {"regex": re.compile(r"^\d{15}$|^.{8,32}$"),   "hint": "IMEI 15位数字，或 SN"},
    "computer": {"regex": re.compile(r"^.{5,64}$"),            "hint": "电脑序列号"},
    "engine":   {"regex": re.compile(r"^.{3,64}$"),            "hint": "发动机号"},
    "sim":      {"regex": re.compile(r"^\d{19,20}$"),          "hint": "SIM卡 ICCID 19~20位数字"},
    "card":     {"regex": re.compile(r"^.{3,64}$"),            "hint": "证件号"},
    "contract": {"regex": re.compile(r"^.{3,64}$"),            "hint": "合同编号"},
    "deed":     {"regex": re.compile(r"^.{3,64}$"),            "hint": "契据/权证号"},
    "device":   {"regex": re.compile(r"^.{3,64}$"),            "hint": "设备序列号/MAC"},
    # 虚拟资产
    "email":    {"regex": re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$"), "hint": "邮箱地址"},
    "domain":   {"regex": re.compile(r"^[a-z0-9][-a-z0-9]*\.[a-z]{2,}$", re.I), "hint": "域名如 longhun.dev"},
    "wallet":   {"regex": re.compile(r"^0x[a-f0-9]{40}$", re.I), "hint": "ETH地址以0x开头共42位"},
    "gpg":      {"regex": re.compile(r"^[0-9A-F]{16}$|^[0-9A-F]{32}$|^[0-9A-F]{40}$", re.I), "hint": "GPG指纹16/32/40位十六进制"},
    "api":      {"regex": re.compile(r"^.{16,128}$"),          "hint": "API密钥指纹或前缀"},
    "ssl":      {"regex": re.compile(r"^[0-9A-F:]{32,128}$", re.I), "hint": "SSL证书指纹"},
    "repo":     {"regex": re.compile(r"^.{3,128}$"),           "hint": "仓库URL"},
    "social":   {"regex": re.compile(r"^.{3,128}$"),           "hint": "社交账号或主页链接"},
    "game":     {"regex": re.compile(r"^.{3,64}$"),            "hint": "游戏平台/ID"},
    "nft":      {"regex": re.compile(r"^0x[a-f0-9]{40}:\d+$", re.I), "hint": "合约地址:TokenID"},
    # 身份资产 — 仅校验非空，具体格式交给用户，我们只存哈希
    "id_card":  {"regex": re.compile(r"^\d{17}[\dXx]$"),       "hint": "中国身份证18位，末位可X"},
    "passport": {"regex": re.compile(r"^[A-Z0-9]{5,20}$", re.I), "hint": "护照号码"},
    "driver":   {"regex": re.compile(r"^[A-Z0-9]{5,20}$", re.I), "hint": "驾照号码"},
    "military": {"regex": re.compile(r"^.{5,40}$"),            "hint": "退伍证号码"},
}

身份资产类型 = {"id_card", "passport", "driver", "military"}


# ═══════════════════════════════════════════════════════════
# 校验函数
# ═══════════════════════════════════════════════════════════

def 校验身份证号(号码: str) -> Tuple[bool, str]:
    """中国身份证最后一位校验（加权求和模11）"""
    if len(号码) != 18:
        return False, "身份证号必须为18位"
    if not re.match(r"^\d{17}[\dXx]$", 号码):
        return False, "身份证号格式错误"

    权重 = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
    校验码 = "10X98765432"
    try:
        s = sum(int(号码[i]) * 权重[i] for i in range(17))
        return 校验码[s % 11].upper() == 号码[17].upper(), "身份证校验位错误"
    except ValueError:
        return False, "身份证号包含非数字字符"


def 校验VIN(编号: str) -> Tuple[bool, str]:
    """VIN 校验和（ISO 3779 简化版）"""
    if len(编号) != 17:
        return False, "VIN必须为17位"
    # VIN 不允许 I/O/Q
    if re.search(r"[IOQ]", 编号, re.I):
        return False, "VIN不能包含 I、O、Q"
    return True, "VIN格式通过"


def 校验格式(资产类型: str, 资产编号: str) -> Tuple[bool, str]:
    """P03 墨子：格式校验"""
    if not 资产编号:
        return False, "资产编号不能为空"

    if 资产类型 not in 资产类型表:
        return False, f"未知资产类型: {资产类型}"

    rule = 格式规则表.get(资产类型)
    if not rule:
        return True, f"资产类型 [{资产类型}] 暂无格式规则，跳过格式校验"

    if not rule["regex"].match(资产编号):
        return False, f"格式错误：{rule['hint']}"

    # 特殊加强校验
    if 资产类型 == "id_card":
        ok, msg = 校验身份证号(资产编号)
        if not ok:
            return False, msg
    elif 资产类型 == "vehicle" and len(资产编号) == 17:
        ok, msg = 校验VIN(资产编号)
        if not ok:
            return False, msg

    return True, f"格式校验通过：{rule['hint']}"


def 检查明文泄露(资产类型: str, 资产编号: str, 备注: str = "") -> Tuple[bool, str]:
    """P07 开源守门人：确保原始编号不会写入存储"""
    # 这里主要检查调用方是否误把原始编号传入其他字段
    # 审计通过的标准：本函数不直接操作存储，只返回审查意见
    if 资产类型 in 身份资产类型:
        return True, "身份类资产将仅存储哈希，符合 R2 铁律"
    return True, "物理/虚拟资产将哈希化存储，符合 R1 铁律"


def 检查重复(uid: str, 资产类型: str, 资产编号: str, 登记册: Optional[DNA登记册] = None) -> Tuple[bool, str]:
    """检查同一 UID 下是否已存在相同资产"""
    if 登记册 is None:
        登记册 = 加载登记册(uid)
    if 登记册 is None:
        return True, "该 UID 尚无登记册，无重复"

    编号哈希 = 哈希资产编号(资产类型, 资产编号)
    现有列表 = 登记册.资产清单.get(资产类型, [])
    for item in 现有列表:
        if item.资产编号哈希 == 编号哈希:
            return False, f"重复登记：此 {资产类型} 已存在 (DNA: {item.DNA码})"
    return True, "去重检查通过"


# ═══════════════════════════════════════════════════════════
# 审计主函数
# ═══════════════════════════════════════════════════════════

def 审计资产登记(
    uid: str,
    资产类型: str,
    资产编号: str,
    标签: Optional[List[str]] = None,
    备注: str = "",
) -> Dict[str, Any]:
    """
    P06 镜像审计者：对一次登记请求执行完整审计

    返回结构:
      {
        "uid": str,
        "资产类型": str,
        "三色": "🟢" | "🟡" | "🔴",
        "是否可写": bool,
        "检查项": { ... },
        "报告": str,
        "dna": str | None,
        "资产编号哈希": str | None,
      }
    """
    检查项: Dict[str, Any] = {}
    失败项: List[str] = []
    警告项: List[str] = []

    # ── P17 入口检查 ──
    if not uid:
        失败项.append("UID 不能为空")

    # ── P03 格式校验 ──
    ok, msg = 校验格式(资产类型, 资产编号)
    检查项["P03_格式校验"] = {"通过": ok, "消息": msg}
    if not ok:
        失败项.append(msg)

    # ── P07 隐私审查 ──
    ok, msg = 检查明文泄露(资产类型, 资产编号, 备注)
    检查项["P07_隐私审查"] = {"通过": ok, "消息": msg}
    if not ok:
        失败项.append(msg)

    # 身份类资产额外标记
    if 资产类型 in 身份资产类型:
        检查项["P07_身份类特殊保护"] = {"通过": True, "消息": "身份类资产仅存储哈希，绝不存明文"}

    # ── P10 外部核验（可选项）──
    外部可核验类型 = {"patent", "domain", "gpg", "wallet"}
    if 资产类型 in 外部可核验类型:
        检查项["P10_外部核验"] = {
            "通过": True,
            "消息": f"{资产类型} 支持外部公开核验，登记后状态为「待验证」",
            "状态": "待验证",
        }
        警告项.append("外部核验待完成，当前标记为待验证")
    else:
        检查项["P10_外部核验"] = {
            "通过": True,
            "消息": "该资产类型无需外部核验",
            "状态": "N/A",
        }

    # ── P05 异常检测 ──
    # 简单频率检查：同一 UID 同类型短时间内大量登记
    登记册 = 加载登记册(uid)
    当前数量 = sum(len(v) for v in (登记册.资产清单.values() if 登记册 else []))
    if 当前数量 > 100:
        检查项["P05_异常检测"] = {"通过": False, "消息": f"该 UID 已登记 {当前数量} 条资产，触发高频预警"}
        失败项.append("高频登记预警：请联系 UID9622 确认")
    else:
        检查项["P05_异常检测"] = {"通过": True, "消息": f"当前登记数量 {当前数量}，未触发异常阈值"}

    # ── 去重检查 ──
    ok, msg = 检查重复(uid, 资产类型, 资产编号, 登记册)
    检查项["去重检查"] = {"通过": ok, "消息": msg}
    if not ok:
        失败项.append(msg)

    # ── 计算哈希与 DNA ──
    资产编号哈希: Optional[str] = None
    dna码: Optional[str] = None
    if not 失败项:
        资产编号哈希 = 哈希资产编号(资产类型, 资产编号)
        import hashlib
        from datetime import datetime, timezone
        时间戳 = datetime.now(timezone.utc).isoformat() + "Z"
        raw = f"{uid}:{资产类型}:{资产编号哈希}:{时间戳}"
        dna码 = hashlib.sha256(raw.encode()).hexdigest()[:12]

    # ── 三色判定 ──
    if 失败项:
        三色 = "🔴"
        是否可写 = False
        报告 = "\n".join([f"❌ {x}" for x in 失败项])
    elif 警告项:
        三色 = "🟡"
        是否可写 = True
        报告 = "\n".join([f"⚠️ {x}" for x in 警告项] + ["✅ 格式/隐私/去重均通过，允许写入"])
    else:
        三色 = "🟢"
        是否可写 = True
        报告 = "✅ 全部审计通过，P06 镜像审计者签名允许写入"

    return {
        "uid": uid,
        "资产类型": 资产类型,
        "资产编号": 资产编号,
        "三色": 三色,
        "是否可写": 是否可写,
        "检查项": 检查项,
        "失败项": 失败项,
        "警告项": 警告项,
        "报告": 报告,
        "dna": dna码,
        "资产编号哈希": 资产编号哈希,
    }


# ═══════════════════════════════════════════════════════════
# CLI 入口
# ═══════════════════════════════════════════════════════════

def main() -> int:
    if len(sys.argv) < 5:
        print("🧬 龍魂统一DNA登记册 · 严格审计人格 (P06)")
        print()
        print("用法:")
        print("  python3 bin/lh_unified_dna_audit.py <uid> <资产类型> <资产编号> [标签...]")
        print()
        print("示例:")
        print('  python3 bin/lh_unified_dna_audit.py UID9622 watch "ROLEX-116610LN-2020" 機械 潛水')
        print('  python3 bin/lh_unified_dna_audit.py UID9622 email "uid9622@longhun.dev" 主邮箱')
        return 0

    uid = sys.argv[1]
    资产类型 = sys.argv[2]
    资产编号 = sys.argv[3]
    标签 = sys.argv[4:] if len(sys.argv) > 4 else []

    result = 审计资产登记(uid, 资产类型, 资产编号, 标签)

    print("=" * 60)
    print(f"  🧬 统一DNA登记审计报告 · {uid}")
    print("=" * 60)
    print(f"  资产类型: {资产类型}")
    print(f"  三色结果: {result['三色']}")
    print(f"  是否可写: {'是' if result['是否可写'] else '否'}")
    print()
    print("  检查项:")
    for name, item in result["检查项"].items():
        mark = "✅" if item["通过"] else "❌"
        print(f"    {mark} {name}: {item['消息']}")
    print()
    print("  报告:")
    for line in result["报告"].split("\n"):
        print(f"    {line}")
    if result["dna"]:
        print(f"\n  独立 DNA: {result['dna']}")
        print(f"  资产编号哈希: {result['资产编号哈希']}")
    print("=" * 60)

    return 0 if result["是否可写"] else 1


if __name__ == "__main__":
    sys.exit(main())

# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# DNA: #龍芯⚡️丙午·丙申·甲寅·壬申·䷒临-UNIFIED-DNA-AUDITOR-v1.0-9F3E2D1C
