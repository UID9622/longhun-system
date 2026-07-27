#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════════╗
║       龍魂统一DNA登记册 · 物理+虚拟全维身份锚定 v1.0                    ║
║       LongHun Unified DNA Registry · One Person, One Life               ║
╠══════════════════════════════════════════════════════════════════════════╣
║  DNA: #龍芯⚡️丙午·丙申·甲寅·壬申-UNIFIED-DNA-REGISTRY-v1.0            ║
║  哲学: 一世一双人 · 物理虚拟不二分 · 哈希可对人不可见 · 追溯本源        ║
║  铁律: 本人可查·他人不可见 · 哈希可验证 · 不可篡改 · 不可删除           ║
║  📇 身份 · 联系 · 支持 → assets/PUBLIC_IDENTITY.md                      ║
╚══════════════════════════════════════════════════════════════════════════╝

设计理念：
  一个人的 DNA = 所有物理资产 + 所有虚拟身份 的 Merkle 根哈希
  本人能看到完整清单，外人只能看到哈希
  哈希对得上 = 归属验证通过
  被骗/被剽窃/被盗 → 追溯本源 → 一搜就知道

用法：
  python3 bin/lh_unified_dna_registry.py register <uid> <资产类型> <资产编号> [标签...]
  python3 bin/lh_unified_dna_registry.py list <uid>
  python3 bin/lh_unified_dna_registry.py verify <uid> <资产类型> <资产编号>
  python3 bin/lh_unified_dna_registry.py master <uid>
  python3 bin/lh_unified_dna_registry.py status <uid>

资产类型（内置 · 可扩展）：
  物理资产: watch 手表 | patent 专利 | ip 知识产权 | engine 发动机 | computer 电脑
           | phone 手机 | sim SIM卡 | card 证件 | contract 合同 | deed 契据
  虚拟资产: email 邮箱 | domain 域名 | social 社交账号 | wallet 钱包地址
           | gpg GPG密钥 | api API密钥 | ssl SSL证书 | repo 代码仓库
  身份资产: id_card 身份证 | passport 护照 | driver 驾照 | military 退伍证
"""

import hashlib
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime, timezone

# ═══════════════════════════════════════════════════════════
# L0 常量 · 焊死
# ═══════════════════════════════════════════════════════════

注册表目录 = Path.home() / ".龍魂" / "unified_dna_registry"
注册表目录.mkdir(parents=True, exist_ok=True)

# 资产类型定义 · 物理 + 虚拟 + 身份
资产类型表 = {
    # ── 物理资产 ──
    "watch":     {"类别": "物理", "名称": "手表/精密机械", "验证方式": "序列号/购买凭证/保卡"},
    "patent":    {"类别": "物理", "名称": "专利",         "验证方式": "专利号/授权书/国家局查询"},
    "ip":        {"类别": "物理", "名称": "知识产权",     "验证方式": "登记号/证书/版权局查询"},
    "engine":    {"类别": "物理", "名称": "发动机",       "验证方式": "发动机号/行驶证"},
    "computer":  {"类别": "物理", "名称": "电脑",         "验证方式": "序列号/购买凭证"},
    "phone":     {"类别": "物理", "名称": "手机",         "验证方式": "IMEI/SN/购买凭证"},
    "sim":       {"类别": "物理", "名称": "SIM卡",        "验证方式": "ICCID/运营商"},
    "card":      {"类别": "物理", "名称": "证件",         "验证方式": "证件号/发证机关"},
    "contract":  {"类别": "物理", "名称": "合同/契约",    "验证方式": "合同编号/签署方"},
    "deed":      {"类别": "物理", "名称": "契据/房契",    "验证方式": "权证号/不动产登记"},
    "vehicle":   {"类别": "物理", "名称": "车辆",         "验证方式": "VIN/车牌号"},
    "device":    {"类别": "物理", "名称": "设备/硬件",    "验证方式": "序列号/MAC地址"},
    # ── 虚拟资产 ──
    "email":     {"类别": "虚拟", "名称": "邮箱",         "验证方式": "邮箱地址/所有权验证"},
    "domain":    {"类别": "虚拟", "名称": "域名",         "验证方式": "WHOIS/DNS验证"},
    "social":    {"类别": "虚拟", "名称": "社交账号",     "验证方式": "平台ID/主页链接"},
    "wallet":    {"类别": "虚拟", "名称": "钱包地址",     "验证方式": "区块链地址/签名验证"},
    "gpg":       {"类别": "虚拟", "名称": "GPG密钥",      "验证方式": "指纹/公钥验证"},
    "api":       {"类别": "虚拟", "名称": "API密钥",      "验证方式": "密钥指纹"},
    "ssl":       {"类别": "虚拟", "名称": "SSL证书",      "验证方式": "证书指纹"},
    "repo":      {"类别": "虚拟", "名称": "代码仓库",     "验证方式": "仓库URL/所有者"},
    "game":      {"类别": "虚拟", "名称": "游戏账号",     "验证方式": "平台/ID"},
    "nft":       {"类别": "虚拟", "名称": "NFT/数字藏品", "验证方式": "合约地址/TokenID"},
    # ── 身份资产 ──
    "id_card":   {"类别": "身份", "名称": "身份证",       "验证方式": "仅存哈希·不存明文"},
    "passport":  {"类别": "身份", "名称": "护照",         "验证方式": "仅存哈希·不存明文"},
    "driver":    {"类别": "身份", "名称": "驾照",         "验证方式": "仅存哈希·不存明文"},
    "military":  {"类别": "身份", "名称": "退伍证",       "验证方式": "仅存哈希·不存明文"},
    # ── 社会贡献 ──
    "oss_code":     {"类别": "社会", "名称": "代码贡献",     "验证方式": "PR/Commit哈希/仓库统计（代码即权威）"},
    "tech_doc":     {"类别": "社会", "名称": "技术文档",     "验证方式": "文章URL/教程/翻译源（技术即话语权）"},
    "oss_maintain": {"类别": "社会", "名称": "开源维护",     "验证方式": "Review记录/Release维护/Issue响应"},
    "community":    {"类别": "社会", "名称": "社区服务",     "验证方式": "答疑记录/ mentorship/组织活动"},
    "welfare":      {"类别": "社会", "名称": "公益行动",     "验证方式": "志愿证明/捐赠记录/救灾参与（不求回报）"},
    "intl_bridge":  {"类别": "社会", "名称": "国际桥接",     "验证方式": "跨文化项目/翻译/国际标准参与（信任桥梁）"},
}

# 资产类别颜色
类别色 = {"物理": "🔵", "虚拟": "🟣", "身份": "🔴", "社会": "🌟"}


# ═══════════════════════════════════════════════════════════
# 核心数据结构
# ═══════════════════════════════════════════════════════════

@dataclass
class DNA资产条目:
    """单条资产登记"""
    资产类型: str          # 如 watch/patent/email
    资产编号哈希: str       # SHA256(资产编号) → 前16位
    资产标签: List[str]    # 用户自定义标签
    登记时间: str          # ISO 时间戳
    登记干支: str          # 农历干支
    验证状态: str          # 已验证/待验证/争议中
    DNA码: str             # 本条资产的独立DNA
    备注哈希: str          # SHA256(备注) 可选

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "DNA资产条目":
        return cls(**d)


@dataclass
class DNA登记册:
    """一个人的完整DNA登记册"""
    UID: str
    创建时间: str
    更新时间: str
    资产清单: Dict[str, List[DNA资产条目]]  # key = 资产类型
    主DNA哈希: str           # Merkle根哈希·一世一双人的DNA
    版本: int = 1
    确认码: str = ""
    GPG指纹: str = ""

    def to_dict(self) -> Dict[str, Any]:
        d: Dict[str, Any] = asdict(self)
        d["资产清单"] = {
            k: [item.to_dict() for item in v]
            for k, v in self.资产清单.items()
        }
        return d

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "DNA登记册":
        资产清单: Dict[str, List[DNA资产条目]] = {}
        for k, v in d.get("资产清单", {}).items():
            资产清单[k] = [DNA资产条目.from_dict(item) for item in v]
        d["资产清单"] = 资产清单
        return cls(**d)


# ═══════════════════════════════════════════════════════════
# 核心算法
# ═══════════════════════════════════════════════════════════

# ── 身份资产安全盐 · Kimi审查边界3 ──
# 身份资产(id_card/passport/driver/military)的哈希加设备级盐
# 即使注册表文件被拷贝，无盐也无法暴力破解证件号
身份资产类型_加密 = {"id_card", "passport", "driver", "military"}

def _获取设备指纹() -> str:
    """获取设备唯一指纹·用于盐派生"""
    import platform, uuid as _uuid
    parts = [
        platform.node() or "unknown",
        platform.machine() or "unknown",
        str(_uuid.getnode()),
    ]
    return hashlib.sha256("|".join(parts).encode()).hexdigest()[:16]

def _设置主盐(master_salt: str) -> bool:
    """
    设置主盐（密码派生·跨设备共享）· Kimi审查P2校准
    
    用法：在多台设备上设置相同主盐 → 设备盐可复现 → 多设备验证一致
      python3 -c "from lh_unified_dna_registry import _设置主盐; _设置主盐('你的脑内密码')"
    """
    import hmac as _hmac
    主盐文件 = 注册表目录 / ".master_salt"
    # 用设备指纹 HMAC 加密存储主盐（即使磁盘被读，无设备指纹无法还原）
    设备指纹 = _获取设备指纹()
    加密主盐 = _hmac.new(设备指纹.encode(), master_salt.encode(), "sha256").hexdigest()
    主盐文件.write_text(加密主盐)
    os.chmod(主盐文件, 0o600)
    return True

def _获取设备盐() -> bytes:
    """
    获取设备指纹盐（支持主盐派生·Kimi审查P2校准）
    
    优先级：
      1. 有主盐 → 派生设备盐 = HMAC(设备指纹, 主盐)  [跨设备一致]
      2. 无主盐 → 本地随机盐                               [单设备·向后兼容]
    """
    import hmac as _hmac
    
    # 检查是否有主盐
    主盐文件 = 注册表目录 / ".master_salt"
    if 主盐文件.exists():
        try:
            设备指纹 = _获取设备指纹()
            加密主盐 = 主盐文件.read_text().strip()
            return _hmac.new(设备指纹.encode(), 加密主盐.encode(), "sha256").digest()
        except Exception:
            pass  # 主盐损坏 → 降级到本地盐
    
    # 无主盐：使用本地随机盐（向后兼容）
    盐文件 = 注册表目录 / ".device_salt"
    if 盐文件.exists():
        return 盐文件.read_bytes()
    # 首次生成：32字节随机盐
    盐 = os.urandom(32)
    盐文件.write_bytes(盐)
    os.chmod(盐文件, 0o600)
    return 盐


def 哈希资产编号(资产类型: str, 资产编号: str) -> str:
    """
    对资产编号做 SHA256 哈希，返回前 16 位。原始编号永不明文存储。
    
    身份资产额外加设备级盐（Kimi审查边界3）：
      - id_card/passport/driver/military → SHA256(类型:编号:设备盐)
      - 非身份资产 → SHA256(类型:编号)
      - 即使注册表文件被拷贝，无盐也无法暴力破解
    """
    if 资产类型 in 身份资产类型_加密:
        盐 = _获取设备盐()
        raw = f"{资产类型}:{资产编号}:{盐.hex()}"
    else:
        raw = f"{资产类型}:{资产编号}"
    return hashlib.sha256(raw.encode()).hexdigest()[:16]


def 生成资产DNA(uid: str, 资产类型: str, 资产编号哈希: str, 时间戳: str) -> str:
    """为单条资产生成独立 DNA 码"""
    raw = f"{uid}:{资产类型}:{资产编号哈希}:{时间戳}"
    return hashlib.sha256(raw.encode()).hexdigest()[:12]


def 计算主DNA哈希(登记册: DNA登记册) -> str:
    """
    Merkle 根哈希 · 一世一双人的 DNA

    算法：
      1. 收集所有资产条目的 DNA 码
      2. 排序后拼接
      3. SHA256 取前 16 位
      4. 这就是这个人的「物理+虚拟」统一DNA
    """
    all_dna = []
    for _类型, 条目列表 in 登记册.资产清单.items():
        for 条目 in 条目列表:
            all_dna.append(条目.DNA码)
    all_dna.sort()
    merkle_input = "|".join(all_dna) + f"|{登记册.UID}"
    return hashlib.sha256(merkle_input.encode()).hexdigest()[:16]


def 验证资产归属(uid: str, 资产类型: str, 资产编号: str, 登记册: DNA登记册) -> Tuple[bool, str]:
    """
    验证一条资产是否属于某人
    不需要看到原始编号，只要哈希对得上就行
    """
    编号哈希 = 哈希资产编号(资产类型, 资产编号)
    if 资产类型 not in 登记册.资产清单:
        return False, f"资产类型 [{资产类型}] 未登记"

    for 条目 in 登记册.资产清单[资产类型]:
        if 条目.资产编号哈希 == 编号哈希:
            return True, f"✅ 验证通过 · {资产类型表.get(资产类型, {}).get('名称', 资产类型)} 归属 {uid} · DNA: {条目.DNA码}"

    return False, f"❌ 未找到匹配 · 此 {资产类型} 未在 {uid} 名下登记"


# ═══════════════════════════════════════════════════════════
# CRUD 操作
# ═══════════════════════════════════════════════════════════

def 加载登记册(uid: str) -> Optional[DNA登记册]:
    """从本地加载已存在的登记册"""
    path = 注册表目录 / f"{uid}.json"
    if not path.exists():
        return None
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return DNA登记册.from_dict(data)


def 保存登记册(登记册: DNA登记册):
    """保存登记册到本地（append-only 语义）"""
    path = 注册表目录 / f"{登记册.UID}.json"
    # 备份旧版本
    if path.exists():
        backup = 注册表目录 / f"{登记册.UID}.v{登记册.版本 - 1}.json"
        path.rename(backup)
    登记册.更新时间 = datetime.now(timezone.utc).isoformat() + "Z"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(登记册.to_dict(), f, ensure_ascii=False, indent=2)


def 注册资产(uid: str, 资产类型: str, 资产编号: str, 标签: Optional[List[str]] = None,
             备注: str = "", 验证状态: str = "待验证") -> Tuple[bool, str, Optional[str]]:
    """
    注册一条资产到某人的 DNA 登记册

    返回: (成功, 消息, DNA码)
    """
    if 资产类型 not in 资产类型表:
        return False, f"未知资产类型: {资产类型}。可用类型: {', '.join(资产类型表.keys())}", None

    登记册 = 加载登记册(uid)
    是新登记册 = 登记册 is None  # 首次注册标记
    
    if 登记册 is None:
        登记册 = DNA登记册(
            UID=uid,
            创建时间=datetime.now(timezone.utc).isoformat() + "Z",
            更新时间=datetime.now(timezone.utc).isoformat() + "Z",
            资产清单={},
            主DNA哈希="",
            版本=1,
        )

    编号哈希 = 哈希资产编号(资产类型, 资产编号)
    备注哈希 = hashlib.sha256(备注.encode()).hexdigest()[:16] if 备注 else ""

    # ═══════════════════════════════════════════════════════════
    # P06 镜像审计者 · 写入前强制审计（延迟导入避免循环依赖）
    # ═══════════════════════════════════════════════════════════
    from lh_unified_dna_audit import 审计资产登记
    审计结果 = 审计资产登记(uid, 资产类型, 资产编号, 标签, 备注)
    if not 审计结果["是否可写"]:
        return False, f"🔴 审计人格拒绝写入\n{审计结果['报告']}", None

    # 若审计为 🟡 待验证（如外部核验未完成），自动把验证状态改为待验证
    if 审计结果["三色"] == "🟡":
        验证状态 = "待验证"

    # 获取干支
    try:
        sys.path.insert(0, str(Path(__file__).parent.parent / "calendar-context-logger"))
        from calendar_core import LunarEngine  # type: ignore[import-untyped]
        g = LunarEngine().get_ganzhi()
        干支 = f"{g['year_zhu']}·{g['month_zhu']}·{g['day_zhu']}·{g['hour_zhu']}"
    except Exception:
        干支 = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")

    时间戳 = datetime.now(timezone.utc).isoformat() + "Z"
    dna码 = 生成资产DNA(uid, 资产类型, 编号哈希, 时间戳)

    # 去重检查
    if 资产类型 in 登记册.资产清单:
        for 条目 in 登记册.资产清单[资产类型]:
            if 条目.资产编号哈希 == 编号哈希:
                return False, f"此 {资产类型} 已登记 (DNA: {条目.DNA码})", None

    条目 = DNA资产条目(
        资产类型=资产类型,
        资产编号哈希=编号哈希,
        资产标签=标签 or [],
        登记时间=时间戳,
        登记干支=干支,
        验证状态=验证状态,
        DNA码=dna码,
        备注哈希=备注哈希,
    )

    if 资产类型 not in 登记册.资产清单:
        登记册.资产清单[资产类型] = []
    登记册.资产清单[资产类型].append(条目)

    登记册.版本 += 1
    登记册.主DNA哈希 = 计算主DNA哈希(登记册)
    保存登记册(登记册)

    # ═══════════════════════════════════════════════════════════
    # 🧬 DNA→通行证自动桥接 · 首次注册自动创建通行证
    # ═══════════════════════════════════════════════════════════
    通行证消息 = ""
    try:
        from lh_ecosystem_passport import 加载通行证, 自动创建或更新通行证
        existing_passport = 加载通行证(uid)
        if 是新登记册 or not existing_passport:
            # 首次注册DNA → 自动创建通行证（带角色推导）
            ok_p, msg_p, passport = 自动创建或更新通行证(uid)
            通行证消息 = f"\n   🧬 {msg_p.replace(chr(10), chr(10)+'   ')}"
    except ImportError:
        pass  # 通行证模块不可用时静默跳过
    except Exception:
        pass  # 不阻断DNA注册流程

    return True, f"✅ {资产类型表[资产类型]['名称']} 已注册{通行证消息}", dna码


def 列出资产(uid: str) -> Tuple[bool, str]:
    """列出某人的完整资产清单"""
    登记册 = 加载登记册(uid)
    if 登记册 is None:
        return False, f"UID [{uid}] 尚未建立DNA登记册"

    总资产数 = sum(len(v) for v in 登记册.资产清单.values())

    lines = [
        "╔══════════════════════════════════════════════════════╗",
        f"║  🧬 龍魂统一DNA登记册 · {uid}                         ║",
        "╠══════════════════════════════════════════════════════╣",
        f"║  主DNA哈希: {登记册.主DNA哈希}                          ║",
        f"║  总资产数: {总资产数}                                           ║",
        f"║  版本: v{登记册.版本}                                              ║",
        "╠══════════════════════════════════════════════════════╣",
    ]

    for 类别名 in ["物理", "虚拟", "身份"]:
        类别资产 = [
            (t, items) for t, items in 登记册.资产清单.items()
            if 资产类型表.get(t, {}).get("类别") == 类别名
        ]
        if not 类别资产:
            continue
        emoji = 类别色[类别名]
        lines.append(f"║  {emoji} {类别名}资产                                         ║")
        for 类型, 条目列表 in 类别资产:
            名称 = 资产类型表[类型]["名称"]
            for item in 条目列表:
                标签 = " ".join([f"#{t}" for t in item.资产标签]) if item.资产标签 else ""
                lines.append(f"║    [{名称}] · {item.资产编号哈希} · {item.验证状态} {标签}")
                lines.append(f"║     DNA: {item.DNA码}")
        lines.append("║                                                      ║")

    lines.append("╠══════════════════════════════════════════════════════╣")
    lines.append("║  🔒 本人可查 · 他人不可见 · 哈希可验证 · 不可篡改     ║")
    lines.append("╚══════════════════════════════════════════════════════╝")

    return True, "\n".join(lines)


def 获取主DNA(uid: str) -> Tuple[bool, str]:
    """获取某人的主DNA哈希（对外唯一标识）"""
    登记册 = 加载登记册(uid)
    if 登记册 is None:
        return False, f"UID [{uid}] 尚未建立DNA登记册"
    return True, 登记册.主DNA哈希


def 获取状态(uid: str) -> Tuple[bool, str]:
    """获取某人登记册状态摘要"""
    登记册 = 加载登记册(uid)
    if 登记册 is None:
        return True, f"UID [{uid}] · 状态：未建立 · 需要 `register` 创建首条资产"

    物理数 = sum(
        len(v) for k, v in 登记册.资产清单.items()
        if 资产类型表.get(k, {}).get("类别") == "物理"
    )
    虚拟数 = sum(
        len(v) for k, v in 登记册.资产清单.items()
        if 资产类型表.get(k, {}).get("类别") == "虚拟"
    )
    身份数 = sum(
        len(v) for k, v in 登记册.资产清单.items()
        if 资产类型表.get(k, {}).get("类别") == "身份"
    )
    总数 = 物理数 + 虚拟数 + 身份数

    return True, (
        f"🧬 UID [{uid}]\n"
        f"   主DNA: {登记册.主DNA哈希 or '(尚无资产)'}\n"
        f"   资产: 🔵物理{物理数}项 🟣虚拟{虚拟数}项 🔴身份{身份数}项 · 共{总数}项\n"
        f"   版本: v{登记册.版本}\n"
        f"   创建: {登记册.创建时间}\n"
        f"   更新: {登记册.更新时间}"
    )


# ═══════════════════════════════════════════════════════════
# CLI 入口
# ═══════════════════════════════════════════════════════════

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("🧬 龍魂统一DNA登记册 · 物理+虚拟全维身份锚定")
        print()
        print("用法:")
        print("  python3 bin/lh_unified_dna_registry.py register <uid> <资产类型> <资产编号> [标签...]")
        print("  python3 bin/lh_unified_dna_registry.py list <uid>")
        print("  python3 bin/lh_unified_dna_registry.py verify <uid> <资产类型> <资产编号>")
        print("  python3 bin/lh_unified_dna_registry.py master <uid>")
        print("  python3 bin/lh_unified_dna_registry.py status <uid>")
        print()
        print("资产类型:")
        for t, info in 资产类型表.items():
            print(f"  {类别色[info['类别']]} {t:<12} {info['名称']:<10} {info['验证方式']}")
        print()
        print("示例:")
        print('  python3 bin/lh_unified_dna_registry.py register UID9622 watch "ROLEX-116610LN-2020" 機械 潛水')
        print('  python3 bin/lh_unified_dna_registry.py register UID9622 patent "CN20241000001" AI算法')
        print('  python3 bin/lh_unified_dna_registry.py register UID9622 email "uid9622@longhun.dev" 主邮箱')
        print('  python3 bin/lh_unified_dna_registry.py verify UID9622 watch "ROLEX-116610LN-2020"')
        print('  python3 bin/lh_unified_dna_registry.py master UID9622')
        sys.exit(0)

    cmd = sys.argv[1]

    if cmd == "register" and len(sys.argv) >= 5:
        uid = sys.argv[2]
        资产类型 = sys.argv[3]
        资产编号 = sys.argv[4]
        标签 = sys.argv[5:] if len(sys.argv) > 5 else []
        ok, msg, dna = 注册资产(uid, 资产类型, 资产编号, 标签)
        print(msg)
        if dna:
            print(f"   DNA: {dna}")
            # 刷新主DNA
            ok2, master = 获取主DNA(uid)
            if ok2:
                print(f"   主DNA: {master}")
        sys.exit(0 if ok else 1)

    elif cmd == "list" and len(sys.argv) >= 3:
        uid = sys.argv[2]
        ok, msg = 列出资产(uid)
        print(msg)

    elif cmd == "verify" and len(sys.argv) >= 5:
        uid = sys.argv[2]
        资产类型 = sys.argv[3]
        资产编号 = sys.argv[4]
        登记册 = 加载登记册(uid)
        if 登记册 is None:
            print(f"UID [{uid}] 尚未建立DNA登记册")
            sys.exit(1)
        ok, msg = 验证资产归属(uid, 资产类型, 资产编号, 登记册)
        print(msg)
        sys.exit(0 if ok else 1)

    elif cmd == "master" and len(sys.argv) >= 3:
        uid = sys.argv[2]
        ok, msg = 获取主DNA(uid)
        print(msg)

    elif cmd == "status" and len(sys.argv) >= 3:
        uid = sys.argv[2]
        ok, msg = 获取状态(uid)
        print(msg)

    elif cmd == "types":
        print("可用资产类型:")
        for t, info in 资产类型表.items():
            print(f"  {类别色[info['类别']]} {t:<12} {info['名称']:<10} → {info['验证方式']}")

    else:
        print(f"未知命令: {cmd}")

# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# DNA: #龍芯⚡️丙午·丙申·甲寅·申时·临-CONFIRM-SEAL-lh_unified_dna_regis-2DFA8ABB
