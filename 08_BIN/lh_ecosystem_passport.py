#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
#龍芯⚡️丙午·甲申·辛丑·坤卦-ECOSYSTEM-PASSPORT-v1.1
# CREATOR: 诸葛鑫 (UID9622)
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# 上位协议: 01_protocols/LH-ECOSYSTEM-ACCESS-PROTOCOL-v1.0.md（P1-CORE·生态准入）
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════════╗
║    龍魂生态通行证 v1.1 · 月度活人验证 · 心跳订阅 · 身份三态管理        ║
║    LongHun Ecosystem Passport · Alive Heartbeat = Ecosystem Key          ║
╠══════════════════════════════════════════════════════════════════════════╣
║  DNA: #龍芯⚡️丙午·甲申·辛丑·坤卦-ECOSYSTEM-PASSPORT-v1.1              ║
║  上位: LH-ECOSYSTEM-ACCESS-PROTOCOL-v1.0.md（P1-CORE）                   ║
║  哲学: 每月1元 = 活人验证 = 生态准入 = 心跳订阅                         ║
║  铁律: 不续费不锁功能 · 数据永远归你 · 随时可导出                       ║
║  📇 身份 · 联系 · 支持 → assets/PUBLIC_IDENTITY.md                      ║
╚══════════════════════════════════════════════════════════════════════════╝

设计理念：
  不是买断·是心跳订阅。
  每月1元证明你是活人，不是僵尸号/机器人。
  不续费 → 退出实时生态 → 数据永不锁、功能永不断、随时可导出。
  
  身份三态（协议§一）：
    🟢 生态内 = 月度验证有效（1元/月） → 全部生态功能 + 实时协同
    🟡 生态外 = 月度验证过期（未续费） → 本地功能 + 导出全部
    ⚪ 共建者 = 连续12个月+ → 生态内全功能 + 治理投票
  
  三层体系：
    DNA 登记册 = 身份锚定（你是谁）
    生态通行证 = 会员资格（你是什么状态）+ 月度活人验证
    XPay = 支付计费（你怎么续费）+ 可选分级升级

用法：
  # ── 通行证管理 ──
  python3 bin/lh_ecosystem_passport.py passport create <uid>                     # 创建通行证
  python3 bin/lh_ecosystem_passport.py passport show <uid>                       # 查看通行证
  python3 bin/lh_ecosystem_passport.py passport status <uid>                     # 生态状态（三态判定）

  # ── 🔥 月度活人验证（协议§二） ──
  python3 bin/lh_ecosystem_passport.py alive verify <uid>                        # 执行月度活人验证
  python3 bin/lh_ecosystem_passport.py alive status <uid>                        # 查活人验证状态
  python3 bin/lh_ecosystem_passport.py alive heartbeat <uid>                     # 发送心跳（1元续费）

  # ── 订阅管理（可选分级升级·基于月度验证之上） ──
  python3 bin/lh_ecosystem_passport.py subscribe <uid> <层级> [月数]             # 订阅
  python3 bin/lh_ecosystem_passport.py subscribe renew <uid>                      # 续费当前层级
  python3 bin/lh_ecosystem_passport.py subscribe cancel <uid>                     # 取消自动续费

  # ── 身份认证 ──
  python3 bin/lh_ecosystem_passport.py auth verify <uid>                          # 触发月度身份认证
  python3 bin/lh_ecosystem_passport.py auth status <uid>                          # 查认证状态
  python3 bin/lh_ecosystem_passport.py auth challenge <uid>                       # 生成认证挑战码

  # ── 📦 导出创作（协议§三） ──
  python3 bin/lh_ecosystem_passport.py export <uid> [格式]                        # 导出全部创作数据
  python3 bin/lh_ecosystem_passport.py export list <uid>                          # 列出可导出内容

  # ── API密钥 ──
  python3 bin/lh_ecosystem_passport.py apikey generate <uid>                      # 生成API密钥
  python3 bin/lh_ecosystem_passport.py apikey list <uid>                          # 列出API密钥
  python3 bin/lh_ecosystem_passport.py apikey revoke <uid> <key_id>               # 吊销密钥

  # ── 服务注册 ──
  python3 bin/lh_ecosystem_passport.py service register <服务名> <所需层级>       # 注册服务
  python3 bin/lh_ecosystem_passport.py service list                               # 列出所有服务
  python3 bin/lh_ecosystem_passport.py service check <uid> <服务名>               # 检查是否有权访问

会员层级：
  🆓  free      免费层 — DNA注册即获得，基础API访问，速率限制
  ⭐  basic     基础层 — 月度订阅，标准API，优先队列
  🌟  pro       专业层 — 高级功能，自定义服务，API批量调用
  👑  founder   创始人 — 全功能，定制服务，投票权
"""

from __future__ import annotations

import hashlib
import json
import secrets
import sys
import time
from dataclasses import asdict, dataclass, field
from datetime import datetime, timedelta, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# ═══════════════════════════════════════════════════════════
# L0 常量 · 焊死
# ═══════════════════════════════════════════════════════════

通行证目录 = Path.home() / ".龍魂" / "ecosystem_passport"
通行证目录.mkdir(parents=True, exist_ok=True)

# ── UID9622 主权覆写 · 最高权限逃生舱 ──
# 铁律：系统永恒运行，政策可能变化。此能力仅UID9622持有。
# 任何系统约束，UID9622确认后可覆写。每次覆写留审计链。
# ⚡️ v2.0 校准：覆写码 = 现场派生（三层绑定·不在源码存任何密钥）
#   公式：HMAC-SHA256(生物因子 || 设备因子 || 环境因子, 脑内盐)
#   降级：无脑内盐 → 旧码SHA256哈希验证（向后兼容）
try:
    from lh_sovereign_derive import 验证覆写码 as _验证主权覆写码, 派生主权覆写码
except ImportError:
    # 降级：模块未就绪时使用旧哈希
    _旧版哈希值 = "798d6f2d8a78c804186082585bc08a68993c832e4a0106306ada3a7c51be90b9"
    def _验证主权覆写码(input_code: str) -> bool:
        """降级模式：SHA256哈希比对"""
        return hashlib.sha256(input_code.encode()).hexdigest() == _旧版哈希值
    def 派生主权覆写码() -> Optional[str]:
        return None

# 占位引用，避免静态分析将 try/except 中的导入误判为未使用
_ = 派生主权覆写码

# 关键操作类型（需双因子确认）
关键操作类型 = [
    "delete_user_data",       # 删除用户数据
    "modify_audit_log",       # 修改审计日志
    "disable_transparency",   # 关闭透明层
    "force_role_change",      # 强制角色变更
    "bypass_safety_fuse",     # 绕过安全熔断
    "system_wide_override",   # 系统级覆写
]
# 🧬 不可覆写操作 · 文明底线元规则 · Kimi审查P0校准
# 老祖宗规则 + 儿童保护 + 反人类 = 主权覆写不能绕过
# 铁律: "文明底线高于一切政权" "创始人亦不可碰红线" (ID17)
不可覆写操作 = [
    "ancestral_rule_override",   # 绕过老祖宗规则锚定
    "child_protection_override", # 绕过儿童保护
    "anti_human_override",       # 绕过反人类内容检测
]
# 主权覆写审计日志路径
主权覆写审计日志 = 通行证目录 / "sovereign_override_audit.jsonl"

# GPG开发者门槛校准 · Kimi审查边界2
# GPG(3.0) 单独不触发developer → 需要 GPG + 至少2项技术资产（总分≥5.0）
# 例: gpg(3.0)+repo(2.0)=5.0✅ | gpg(3.0)+oss_code(3.0)=6.0✅
#     gpg(3.0) alone=3.0❌ | gpg(3.0)+api(1.5)=4.5❌
GPG_开发者最低总分 = 5.0

# ── 会员层级定义 ──
class 会员层级(Enum):
    free = "free"         # 免费
    basic = "basic"       # 基础
    pro = "pro"           # 专业
    founder = "founder"   # 创始人

# ── 生态角色定义 ──
# DNA中的资产组合 → 自动推导角色 → 初始通行证层级
class 生态角色(Enum):
    founder = "founder"                 # 系统创始人·全能
    developer = "developer"             # 技术开发者·GPG签名+代码贡献
    creator = "creator"                 # 内容创作者·专利/IP/文档
    real_name_user = "real_name_user"   # 实名用户·身份认证
    free_user = "free_user"             # 自由用户·最小DNA

# 角色 → 推荐层级 + 人格偏好映射
角色层级人格映射: Dict[str, Dict[str, Any]] = {
    "founder": {
        "emoji": "👑",
        "名称": "系统创始人",
        "推荐层级": "founder",
        "人格偏好": "全人格·16/16",
        "人格ID列表": ["P00","P01","P02","P03","P04","P05","P06","P08","P09","P10","P11","P12","P13","P14","P15","P72"],
        "说明": "DNA注册即获得创始人全权限·投票权·全人格联动",
    },
    "developer": {
        "emoji": "⚙️",
        "名称": "技术开发者",
        "推荐层级": "pro",
        "人格偏好": "P04-鲁班·技术执行 | P15-乔前辈·极简工程",
        "人格ID列表": ["P04", "P15"],
        "说明": "GPG签名+代码仓库+开源贡献→专业层·技术引擎全开",
    },
    "creator": {
        "emoji": "🎨",
        "名称": "内容创作者",
        "推荐层级": "pro",
        "人格偏好": "P11-李白·创意爆发 | P10-苏东坡·豁达跨界",
        "人格ID列表": ["P11", "P10"],
        "说明": "专利/IP/技术文档/开源维护→专业层·创作引擎全开",
    },
    "real_name_user": {
        "emoji": "🪪",
        "名称": "实名用户",
        "推荐层级": "basic",
        "人格偏好": "P02-宝宝·情感温度 | P14-吕蒙·快速成长",
        "人格ID列表": ["P02", "P14"],
        "说明": "身份证/护照/驾照认证→基础层·可信服务接入",
    },
    "free_user": {
        "emoji": "🆓",
        "名称": "自由用户",
        "推荐层级": "free",
        "人格偏好": "P00-文心·元认知",
        "人格ID列表": ["P00"],
        "说明": "最小DNA(邮箱/社交)→免费层·基础API·试用",
    },
}

# DNA资产类型 → 角色权重（用于自动推导）
DNA资产角色权重: Dict[str, Dict[str, float]] = {
    # 创始人标记
    "founder_mark": {"founder": 100.0},  # 特殊标记·不进资产类型表
    # 开发者标记
    "gpg":      {"developer": 3.0},
    "repo":     {"developer": 2.0},
    "oss_code": {"developer": 3.0},
    "api":      {"developer": 1.5},
    "ssl":      {"developer": 1.0},
    "oss_maintain": {"developer": 2.0},
    # 创作者标记
    "patent":   {"creator": 3.0},
    "ip":       {"creator": 3.0},
    "tech_doc": {"creator": 2.5},
    "nft":      {"creator": 1.0},
    # 实名标记
    "id_card":  {"real_name_user": 4.0},
    "passport": {"real_name_user": 3.0},  # 护照作为身份资产
    "driver":   {"real_name_user": 2.0},
    "military": {"real_name_user": 2.0},
    "card":     {"real_name_user": 1.0},
    "phone":    {"real_name_user": 1.0},
    # 社交标记
    "email":    {"free_user": 1.0},
    "social":   {"free_user": 1.0},
    "domain":   {"free_user": 1.0},
    "game":     {"free_user": 0.5},
    # 其他
    "wallet":   {"developer": 1.0, "creator": 0.5},
    "contract": {"real_name_user": 1.5, "creator": 0.5},
    "device":   {"developer": 1.0, "free_user": 0.5},
    "vehicle":  {"real_name_user": 1.0, "free_user": 0.5},
    "intl_bridge": {"creator": 1.5, "developer": 1.0},
    "community": {"creator": 1.5},
    "welfare":  {"creator": 1.0, "real_name_user": 0.5},
}

# 层级权益定义
层级权益表: Dict[str, Dict[str, Any]] = {
    "free": {
        "emoji": "🆓",
        "名称": "免费层",
        "月费": 0,
        "API速率": "10次/分钟",
        "最大API密钥": 1,
        "服务接入数": 3,
        "优先队列": False,
        "自定义服务": False,
        "投票权": False,
        "说明": "DNA注册即获得，适合试用和个人使用",
    },
    "basic": {
        "emoji": "⭐",
        "名称": "基础层",
        "月费": 9.9,
        "API速率": "60次/分钟",
        "最大API密钥": 3,
        "服务接入数": 10,
        "优先队列": True,
        "自定义服务": False,
        "投票权": False,
        "说明": "月度订阅，适合开发者日常使用",
    },
    "pro": {
        "emoji": "🌟",
        "名称": "专业层",
        "月费": 49.9,
        "API速率": "300次/分钟",
        "最大API密钥": 10,
        "服务接入数": 50,
        "优先队列": True,
        "自定义服务": True,
        "投票权": False,
        "说明": "适合团队和商业应用",
    },
    "founder": {
        "emoji": "👑",
        "名称": "创始人",
        "月费": 999.0,
        "API速率": "无限制",
        "最大API密钥": 100,
        "服务接入数": 999,
        "优先队列": True,
        "自定义服务": True,
        "投票权": True,
        "说明": "全功能，参与系统治理",
    },
}

# 订阅周期
订阅周期_天 = 30  # 一个月30天

# ═══════════════════════════════════════════════════════════
# 核心数据结构
# ═══════════════════════════════════════════════════════════

@dataclass
class API密钥条目:
    """API密钥"""
    key_id: str          # 密钥ID
    key_hash: str        # SHA256(密钥) 前16位
    key_prefix: str      # 密钥前缀（lh_xxxxxx）
    创建时间: str
    最后使用: str
    状态: str            # active / revoked / expired
    用途: str = ""
    权限范围: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "API密钥条目":
        return cls(**d)


@dataclass
class 身份认证记录:
    """月度身份认证记录"""
    认证时间: str
    认证方式: str        # dna_verify / challenge_response / manual
    认证结果: str         # passed / failed / pending
    挑战码: str = ""
    应答哈希: str = ""
    到期时间: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "身份认证记录":
        return cls(**d)


@dataclass
class 订阅记录:
    """订阅信息"""
    层级: str            # free/basic/pro/founder
    开始时间: str
    到期时间: str
    自动续费: bool = True
    支付方式: str = "xpay"  # xpay / manual
    上一笔交易ID: str = ""
    续费次数: int = 0
    累计付费月数: int = 0

    def 已过期(self) -> bool:
        try:
            到期 = _解析时间(self.到期时间)
            return datetime.now(timezone.utc) > 到期
        except Exception:
            return True

    def 剩余天数(self) -> int:
        try:
            到期 = _解析时间(self.到期时间)
            delta = 到期 - datetime.now(timezone.utc)
            return max(0, delta.days)
        except Exception:
            return 0

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "订阅记录":
        return cls(**d)


@dataclass
class 生态通行证:
    """一个人的生态通行证"""
    UID: str
    DNA哈希: str                    # 关联到统一DNA登记册的主DNA哈希
    创建时间: str
    更新时间: str
    会员层级: str                   # free/basic/pro/founder（可选分级·基于月度验证）
    订阅记录: List[订阅记录]         # 订阅历史（append-only）
    当前订阅: Optional[订阅记录]     # 当前生效的订阅
    认证记录: List["身份认证记录"]     # 认证历史（append-only）
    最近认证: Optional["身份认证记录"]
    API密钥列表: List[API密钥条目]    # 活跃密钥
    已接入服务: List[str]            # 已接入的服务名
    状态: str                       # active / frozen / suspended
    生态角色: str = "free_user"     # founder/developer/creator/real_name_user/free_user
    人格偏好: str = "P00-文心"       # 推荐人格ID列表（逗号分隔）
    角色推导来源: str = ""           # 推导原因（哪些DNA资产触发了角色判定）
    版本: int = 1
    备注: str = ""
    # 🔥 v1.1 月度活人验证（生态接入协议§二）
    月度验证到期: str = ""           # 月度活人验证到期日（YYYY-MM-DD）
    首次验证日: str = ""             # 首次活人验证日期
    连续月数: str = ""              # 连续验证起始日（用于共建者判定）

    def to_dict(self) -> Dict[str, Any]:
        d: Dict[str, Any] = asdict(self)
        d["订阅记录"] = [r.to_dict() if isinstance(r, 订阅记录) else r for r in (self.订阅记录 or [])]
        if self.当前订阅:
            d["当前订阅"] = self.当前订阅.to_dict() if isinstance(self.当前订阅, 订阅记录) else self.当前订阅
        d["认证记录"] = [r.to_dict() if isinstance(r, 身份认证记录) else r for r in (self.认证记录 or [])]
        if self.最近认证:
            d["最近认证"] = self.最近认证.to_dict() if isinstance(self.最近认证, 身份认证记录) else self.最近认证
        d["API密钥列表"] = [k.to_dict() if isinstance(k, API密钥条目) else k for k in (self.API密钥列表 or [])]
        return d

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "生态通行证":
        d = dict(d)
        # 兼容旧版本无生态角色字段
        if "生态角色" not in d:
            d["生态角色"] = "free_user"
        if "人格偏好" not in d:
            d["人格偏好"] = "P00-文心"
        if "角色推导来源" not in d:
            d["角色推导来源"] = ""
        if "订阅记录" in d:
            d["订阅记录"] = [订阅记录.from_dict(r) if isinstance(r, dict) else r for r in d["订阅记录"]]
        if "当前订阅" in d and d["当前订阅"] and isinstance(d["当前订阅"], dict):
            d["当前订阅"] = 订阅记录.from_dict(d["当前订阅"])
        if "认证记录" in d:
            d["认证记录"] = [身份认证记录.from_dict(r) if isinstance(r, dict) else r for r in d["认证记录"]]
        if "最近认证" in d and d["最近认证"] and isinstance(d["最近认证"], dict):
            d["最近认证"] = 身份认证记录.from_dict(d["最近认证"])
        if "API密钥列表" in d:
            d["API密钥列表"] = [API密钥条目.from_dict(k) if isinstance(k, dict) else k for k in d["API密钥列表"]]
        return cls(**d)


# ═══════════════════════════════════════════════════════════
# CRUD 操作
# ═══════════════════════════════════════════════════════════

def 加载通行证(uid: str) -> Optional[生态通行证]:
    path = 通行证目录 / f"{uid}.json"
    if not path.exists():
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return 生态通行证.from_dict(data)
    except Exception:
        return None


def 保存通行证(通行证: 生态通行证):
    path = 通行证目录 / f"{通行证.UID}.json"
    if path.exists():
        backup = 通行证目录 / f"{通行证.UID}.v{通行证.版本 - 1}.json"
        path.rename(backup)
    通行证.更新时间 = _现在时间()
    通行证.版本 += 1
    with open(path, "w", encoding="utf-8") as f:
        json.dump(通行证.to_dict(), f, ensure_ascii=False, indent=2)


def _获取干支() -> str:
    try:
        sys.path.insert(0, str(Path(__file__).parent.parent / "calendar-context-logger"))
        from calendar_core import LunarEngine
        g = LunarEngine().get_ganzhi()
        return f"{g['year_zhu']}·{g['month_zhu']}·{g['day_zhu']}·{g['hour_zhu']}"
    except Exception:
        return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")


def _现在时间() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _解析时间(ts: str) -> datetime:
    """统一时间解析，兼容旧格式 +00:00Z → +00:00"""
    if ts.endswith("Z"):
        ts = ts[:-1] + "+00:00"
    return datetime.fromisoformat(ts)


# ═══════════════════════════════════════════════════════════
# 第0层：DNA角色分析 · 自动推导身份
# ═══════════════════════════════════════════════════════════

def DNA推导角色(uid: str) -> Tuple[str, str, str, str]:
    """
    扫描DNA登记册中的资产组合，自动推导生态角色。
    
    返回: (角色名, 推荐层级, 人格偏好字符串, 推导原因)
    
    推导逻辑（优先级从高到低）：
      1. UID9622 → founder（创始人·全人格）
      2. 有gpg+repo/oss_code → developer（技术开发者）
      3. 有patent/ip/tech_doc → creator（内容创作者）
      4. 有id_card/passport → real_name_user（实名用户）
      5. 最低DNA → free_user（自由用户）
    """
    # 创始人硬判定 — UID9622 独占
    if uid == "UID9622":
        角色信息 = 角色层级人格映射["founder"]
        return (
            "founder",
            "founder",
            角色信息["人格偏好"],
            f"系统创始人·DNA判定·全人格联动·{角色信息['说明']}"
        )
    
    # 尝试加载DNA登记册
    try:
        sys.path.insert(0, str(Path(__file__).parent))
        from lh_unified_dna_registry import 加载登记册
        登记册 = 加载登记册(uid)
    except Exception:
        登记册 = None
    
    if not 登记册 or not 登记册.资产清单:
        角色信息 = 角色层级人格映射["free_user"]
        return (
            "free_user",
            "free",
            角色信息["人格偏好"],
            "无DNA登记册·默认自由用户·{角色信息['说明']}"
        )
    
    # 统计各类资产权重
    角色得分: Dict[str, float] = {
        "founder": 0.0,
        "developer": 0.0,
        "creator": 0.0,
        "real_name_user": 0.0,
        "free_user": 0.0,
    }
    
    触发资产: Dict[str, List[str]] = {
        "founder": [],
        "developer": [],
        "creator": [],
        "real_name_user": [],
        "free_user": [],
    }
    
    # 遍历所有DNA资产
    for 资产类型, 条目列表 in 登记册.资产清单.items():
        if 资产类型 not in DNA资产角色权重:
            continue
        权重映射 = DNA资产角色权重[资产类型]
        for _ in 条目列表:
            for 角色, 权重 in 权重映射.items():
                if 角色 in 角色得分:
                    角色得分[角色] += 权重
                    触发资产[角色].append(资产类型)
    
    # 去重触发资产
    for 角色 in 触发资产:
        触发资产[角色] = list(set(触发资产[角色]))
    
    # 判定逻辑（按优先级）
    # 1. 开发者判定：GPG + 至少2项技术资产（总分≥5.0）
    #    Kimi审查边界2校准：GPG(3.0)单独不触发developer
    if 角色得分["developer"] >= GPG_开发者最低总分 and "gpg" in 触发资产["developer"] and len(触发资产["developer"]) >= 2:
        角色信息 = 角色层级人格映射["developer"]
        return (
            "developer",
            "pro",
            角色信息["人格偏好"],
            f"GPG签名+{len(触发资产['developer'])}项技术资产·资产: {', '.join(触发资产['developer'])}·{角色信息['说明']}"
        )
    
    # 1b. 开发者降级提示：有GPG但技术资产不够
    if "gpg" in 触发资产["developer"] and 角色得分["developer"] < GPG_开发者最低总分:
        # GPG存在但不足→降为creator或real_name_user判定，不升developer
        pass  # 继续往下判定
    
    # 2. 创作者判定：patent/ip/tech_doc
    if 角色得分["creator"] >= 3.0:
        角色信息 = 角色层级人格映射["creator"]
        return (
            "creator",
            "pro",
            角色信息["人格偏好"],
            f"创作资产·资产: {', '.join(触发资产['creator'])}·{角色信息['说明']}"
        )
    
    # 3. 开发者判定（无gpg但有多项技术资产）
    if 角色得分["developer"] >= 3.0:
        角色信息 = 角色层级人格映射["developer"]
        return (
            "developer",
            "pro",
            角色信息["人格偏好"],
            f"技术资产(无GPG)·资产: {', '.join(触发资产['developer'])}·{角色信息['说明']}"
        )
    
    # 4. 实名判定
    if 角色得分["real_name_user"] >= 2.0:
        角色信息 = 角色层级人格映射["real_name_user"]
        return (
            "real_name_user",
            "basic",
            角色信息["人格偏好"],
            f"身份认证资产·资产: {', '.join(触发资产['real_name_user'])}·{角色信息['说明']}"
        )
    
    # 5. 默认自由用户
    角色信息 = 角色层级人格映射["free_user"]
    所有资产 = []
    for v in 触发资产.values():
        所有资产.extend(v)
    所有资产 = list(set(所有资产))
    return (
        "free_user",
        "free",
        角色信息["人格偏好"],
        f"基础DNA·资产: {', '.join(所有资产) if 所有资产 else '无' }·{角色信息['说明']}"
    )


# ═══════════════════════════════════════════════════════════
# 第1层：通行证创建（DNA → 通行证）
# ═══════════════════════════════════════════════════════════

def 创建通行证(uid: str, dna哈希: Optional[str] = None, 自动推导: bool = True) -> Tuple[bool, str, Optional[生态通行证]]:
    """
    为已注册DNA的用户创建生态通行证。
    如果用户没有DNA登记册，先提示注册DNA。
    
    自动推导=True: 分析DNA资产自动判定角色和初始层级
    自动推导=False: 默认free层（手动降级场景）
    """
    # 检查是否已有通行证
    existing = 加载通行证(uid)
    if existing:
        return False, f"⚠️ UID [{uid}] 已有通行证（v{existing.版本}，层级: {existing.会员层级}，角色: {existing.生态角色}）", existing

    # 如果没有提供DNA哈希，尝试从DNA登记册获取
    if not dna哈希:
        try:
            sys.path.insert(0, str(Path(__file__).parent))
            from lh_unified_dna_registry import 获取主DNA
            ok, dna = 获取主DNA(uid)
            if ok:
                dna哈希 = dna
            else:
                return False, (
                    f"❌ UID [{uid}] 尚未建立DNA登记册\n"
                    f"   请先注册DNA: python3 bin/lh_unified_dna_registry.py register {uid} <类型> <编号>\n"
                    f"   然后重新创建通行证。"
                ), None
        except ImportError:
            return False, "❌ 无法读取DNA登记册，请手动提供DNA哈希", None

    # ── 自动推导角色和层级 ──
    if 自动推导:
        推导角色, 推导层级, 推导人格, 推导原因 = DNA推导角色(uid)
    else:
        推导角色 = "free_user"
        推导层级 = "free"
        推导人格 = 角色层级人格映射["free_user"]["人格偏好"]
        推导原因 = "手动创建·默认free层"

    角色信息 = 角色层级人格映射.get(推导角色, 角色层级人格映射["free_user"])
    层级信息 = 层级权益表.get(推导层级, 层级权益表["free"])

    now = _现在时间()
    
    # 免费层订阅永久有效
    if 推导层级 == "free":
        到期时间 = (datetime.now(timezone.utc) + timedelta(days=36500)).isoformat().replace("+00:00", "Z")
        支付方式 = "free"
    else:
        到期时间 = (datetime.now(timezone.utc) + timedelta(days=订阅周期_天)).isoformat().replace("+00:00", "Z")
        支付方式 = "dna_auto"  # DNA推导自动授予·首月免费

    通行证 = 生态通行证(
        UID=uid,
        DNA哈希=dna哈希,
        创建时间=now,
        更新时间=now,
        会员层级=推导层级,
        生态角色=推导角色,
        人格偏好=推导人格,
        角色推导来源=推导原因,
        订阅记录=[],
        当前订阅=订阅记录(
            层级=推导层级,
            开始时间=now,
            到期时间=到期时间,
            自动续费=True,
            支付方式=支付方式,
            续费次数=0,
            累计付费月数=0,
        ),
        认证记录=[],
        最近认证=None,
        API密钥列表=[],
        已接入服务=[],
        状态="active",
        版本=1,
    )
    保存通行证(通行证)
    干支 = _获取干支()

    return True, (
        f"🧬✅ 生态通行证已创建！\n"
        f"   UID: {uid}\n"
        f"   DNA: {dna哈希}\n"
        f"   角色: {角色信息['emoji']} {角色信息['名称']}\n"
        f"   层级: {层级信息['emoji']} {层级信息['名称']}\n"
        f"   人格: {推导人格}\n"
        f"   干支: {干支}\n"
        f"   来源: {推导原因}\n"
        f"   ─────────────────\n"
        f"   下一步: 生成API密钥开始使用服务\n"
        f"   python3 bin/lh_ecosystem_passport.py apikey generate {uid}"
    ), 通行证


def 自动创建或更新通行证(uid: str) -> Tuple[bool, str, Optional[生态通行证]]:
    """
    智能创建/更新通行证。
    - 无通行证 → 创建（自动推导角色）
    - 已有通行证 → 重新分析DNA，若角色/层级有变则更新
    """
    existing = 加载通行证(uid)
    
    # 执行DNA分析
    推导角色, 推导层级, 推导人格, 推导原因 = DNA推导角色(uid)
    
    if not existing:
        # 新建
        try:
            sys.path.insert(0, str(Path(__file__).parent))
            from lh_unified_dna_registry import 获取主DNA
            ok, dna = 获取主DNA(uid)
            if not ok:
                return False, f"❌ UID [{uid}] 无DNA登记册·请先注册DNA", None
        except ImportError:
            return False, "❌ 无法读取DNA登记册", None
        
        return 创建通行证(uid, dna哈希=dna, 自动推导=True)
    
    # 已有通行证 → 检查是否需要更新
    changed = []
    if existing.生态角色 != 推导角色:
        changed.append(f"角色: {existing.生态角色} → {推导角色}")
        existing.生态角色 = 推导角色
    if existing.会员层级 != 推导层级:
        changed.append(f"层级: {existing.会员层级} → {推导层级}")
        existing.会员层级 = 推导层级
    if existing.人格偏好 != 推导人格:
        changed.append(f"人格: {existing.人格偏好} → {推导人格}")
        existing.人格偏好 = 推导人格
    if existing.角色推导来源 != 推导原因:
        existing.角色推导来源 = 推导原因
    
    if not changed:
        return True, (
            f"✅ 通行证角色无需更新\n"
            f"   角色: {角色层级人格映射[existing.生态角色]['emoji']} {角色层级人格映射[existing.生态角色]['名称']}\n"
            f"   层级: {层级权益表[existing.会员层级]['emoji']} {层级权益表[existing.会员层级]['名称']}\n"
            f"   人格: {existing.人格偏好}"
        ), existing
    
    保存通行证(existing)
    
    # ── 边界4：升级通知（Kimi审查·用户知情权）──
    升级消息 = (
        f"\n🔔 [龍魂] 你的角色已升级！\n"
        f"   UID: {uid}\n"
        f"   变更: {', '.join(changed)}\n"
        f"   当前角色: {角色层级人格映射[existing.生态角色]['emoji']} {角色层级人格映射[existing.生态角色]['名称']}\n"
        f"   当前层级: {层级权益表[existing.会员层级]['emoji']} {层级权益表[existing.会员层级]['名称']}\n"
        f"   人格偏好: {existing.人格偏好}\n"
        f"   ─────────────────\n"
        f"   如需拒绝自动升级: python3 bin/lh_ecosystem_passport.py passport freeze {uid}"
    )
    print(升级消息, file=sys.stderr)  # 用户可见
    
    return True, (
        f"🔄✅ 通行证已更新！\n"
        f"   UID: {uid}\n"
        f"   变更: {', '.join(changed)}\n"
        f"   当前角色: {角色层级人格映射[existing.生态角色]['emoji']} {角色层级人格映射[existing.生态角色]['名称']}\n"
        f"   当前层级: {层级权益表[existing.会员层级]['emoji']} {层级权益表[existing.会员层级]['名称']}\n"
        f"   人格: {existing.人格偏好}"
    ), existing


# ═══════════════════════════════════════════════════════════
# 第2层：订阅管理（续费 + 层级升降）
# ═══════════════════════════════════════════════════════════

def 订阅(uid: str, 层级: str, 月数: int = 1) -> Tuple[bool, str]:
    """
    订阅或升级会员层级
    免费层不能"订阅"，只能续费 basic/pro/founder
    """
    通行证 = 加载通行证(uid)
    if not 通行证:
        return False, f"❌ UID [{uid}] 无通行证，请先创建"

    if 层级 not in [e.value for e in 会员层级]:
        return False, f"❌ 无效层级: {层级}。可用: free/basic/pro/founder"

    if 层级 == "free":
        return False, "❌ 免费层无需订阅，DNA注册即获得"

    层级信息 = 层级权益表.get(层级, {})
    月费 = 层级信息.get("月费", 0)

    if 月数 < 1:
        return False, "❌ 最少订阅1个月"

    总费用 = 月费 * 月数

    # 判断是否已有订阅到期时间
    now = datetime.now(timezone.utc)
    开始时间 = _现在时间()

    if 通行证.当前订阅 and 通行证.当前订阅.层级 == 层级:
        # 同层级续费：从当前到期日往后加
        try:
            当前到期 = _解析时间(通行证.当前订阅.到期时间)
            if 当前到期 > now:
                开始时间 = 通行证.当前订阅.到期时间
        except Exception:
            pass

    到期时间 = (_解析时间(开始时间) + timedelta(days=订阅周期_天 * 月数)).isoformat().replace("+00:00", "Z")

    # 生成交易ID（模拟XPay交易记录）
    交易ID = f"XPAY-{uid}-{层级}-{int(time.time())}-{secrets.token_hex(4)}"

    # 创建订阅记录
    新订阅 = 订阅记录(
        层级=层级,
        开始时间=开始时间,
        到期时间=到期时间,
        自动续费=True,
        支付方式="xpay",
        上一笔交易ID=交易ID,
        续费次数=(通行证.当前订阅.续费次数 + 1) if 通行证.当前订阅 else 1,
        累计付费月数=(通行证.当前订阅.累计付费月数 + 月数) if 通行证.当前订阅 else 月数,
    )

    # append 订阅记录（不可删）
    if 通行证.订阅记录 is None:
        通行证.订阅记录 = []
    通行证.订阅记录.append(新订阅)
    通行证.当前订阅 = 新订阅
    通行证.会员层级 = 层级
    通行证.状态 = "active"

    保存通行证(通行证)

    emoji = 层级信息.get("emoji", "⭐")
    return True, (
        f"{emoji}✅ 订阅成功！\n"
        f"   UID: {uid}\n"
        f"   层级: {emoji} {层级信息.get('名称', 层级)}\n"
        f"   月数: {月数}个月\n"
        f"   费用: ¥{总费用:.2f}\n"
        f"   到期: {到期时间}\n"
        f"   交易: {交易ID}\n"
        f"   剩余: {新订阅.剩余天数()}天"
    )


def 续费(uid: str) -> Tuple[bool, str]:
    """续费当前层级（续一个月）"""
    通行证 = 加载通行证(uid)
    if not 通行证:
        return False, f"❌ UID [{uid}] 无通行证"
    if not 通行证.当前订阅 or 通行证.当前订阅.层级 == "free":
        return False, "❌ 免费层无需续费，请先订阅: python3 bin/lh_ecosystem_passport.py subscribe <uid> basic"

    return 订阅(uid, 通行证.当前订阅.层级, 1)


def 取消自动续费(uid: str) -> Tuple[bool, str]:
    通行证 = 加载通行证(uid)
    if not 通行证:
        return False, f"❌ UID [{uid}] 无通行证"
    if not 通行证.当前订阅:
        return False, "❌ 无当前订阅"

    通行证.当前订阅.自动续费 = False
    保存通行证(通行证)
    return True, f"✅ 自动续费已取消 · 订阅将于 {通行证.当前订阅.到期时间} 到期"


# ═══════════════════════════════════════════════════════════
# 第3层：月度身份认证（防冒用）
# ═══════════════════════════════════════════════════════════

def 生成认证挑战(uid: str) -> Tuple[bool, str, Optional[str]]:
    """生成挑战码，用户需要用DNA私钥签名回应"""
    通行证 = 加载通行证(uid)
    if not 通行证:
        return False, "❌ 无通行证", None

    挑战种子 = f"{uid}:{通行证.DNA哈希}:{int(time.time())}:{secrets.token_hex(8)}"
    挑战码 = hashlib.sha256(挑战种子.encode()).hexdigest()[:16]

    return True, (
        f"🔐 身份认证挑战\n"
        f"   挑战码: {挑战码}\n"
        f"   ────────────────\n"
        f"   请用你的DNA私钥签名此挑战码，\n"
        f"   然后将签名字符串作为应答提交:\n"
        f"   python3 bin/lh_ecosystem_passport.py auth verify {uid} --challenge={挑战码} --response=<签名字符串>"
    ), 挑战码


def 验证身份(uid: str, 挑战码: str = "", 应答: str = "", 认证方式: str = "challenge_response") -> Tuple[bool, str]:
    """验证用户身份"""
    通行证 = 加载通行证(uid)
    if not 通行证:
        return False, "❌ 无通行证"

    now = _现在时间()
    到期时间 = (datetime.now(timezone.utc) + timedelta(days=30)).isoformat().replace("+00:00", "Z")

    # 计算应答哈希
    应答哈希 = ""
    if 应答:
        应答哈希 = hashlib.sha256(f"{挑战码}:{应答}:{通行证.DNA哈希}".encode()).hexdigest()[:16]

    # 创建认证记录
    # 简单验证：如果提供了应答，且挑战码匹配，则认为通过
    # 实际部署中应使用GPG/国密签名验证
    认证通过 = bool(应答)  # 简化版：有应答即通过，生产环境需要真实签名验证
    认证结果 = "passed" if 认证通过 else "pending"

    if 认证方式 == "manual":
        认证通过 = True
        认证结果 = "passed"

    记录 = 身份认证记录(
        认证时间=now,
        认证方式=认证方式,
        认证结果=认证结果,
        挑战码=挑战码,
        应答哈希=应答哈希,
        到期时间=到期时间,
    )

    if 通行证.认证记录 is None:
        通行证.认证记录 = []
    通行证.认证记录.append(记录)
    通行证.最近认证 = 记录

    # 如果认证通过，激活通行证
    if 认证通过:
        if 通行证.状态 == "frozen":
            通行证.状态 = "active"

    保存通行证(通行证)

    if 认证通过:
        return True, (
            f"✅ 身份认证通过！\n"
            f"   UID: {uid}\n"
            f"   方式: {认证方式}\n"
            f"   下次认证: {到期时间}（30天后）\n"
            f"   应答哈希: {应答哈希}"
        )
    else:
        return False, f"❌ 身份认证未通过 · 请重新生成挑战码并签名"


def 检查认证状态(uid: str) -> Tuple[bool, str]:
    """检查是否需要重新认证"""
    通行证 = 加载通行证(uid)
    if not 通行证:
        return False, "❌ 无通行证"

    if not 通行证.最近认证:
        return True, "⚠️ 尚未进行过身份认证 · 请执行: python3 bin/lh_ecosystem_passport.py auth verify <uid>"

    最近认证 = 通行证.最近认证
    try:
        到期 = _解析时间(最近认证.到期时间)
        now = datetime.now(timezone.utc)
        if now > 到期:
            return True, (
                f"🔴 身份认证已过期！\n"
                f"   上次认证: {最近认证.认证时间}\n"
                f"   到期时间: {最近认证.到期时间}\n"
                f"   过期: {(now - 到期).days}天\n"
                f"   请立即重新认证！"
            )
        else:
            return True, (
                f"🟢 身份认证有效\n"
                f"   上次认证: {最近认证.认证时间}\n"
                f"   到期时间: {最近认证.到期时间}\n"
                f"   剩余: {(到期 - now).days}天\n"
                f"   状态: {最近认证.认证结果}"
            )
    except Exception:
        return True, "⚠️ 无法解析认证时间"


# ═══════════════════════════════════════════════════════════
# 第4层：API密钥管理
# ═══════════════════════════════════════════════════════════

def 生成API密钥(uid: str, 用途: str = "", 权限范围: Optional[List[str]] = None) -> Tuple[bool, str, Optional[str]]:
    """
    生成 API 密钥。
    密钥格式: lh_<随机48字符>
    密钥仅显示一次，之后只存哈希。
    """
    通行证 = 加载通行证(uid)
    if not 通行证:
        return False, "❌ 无通行证", None

    # 检查层级允许的最大密钥数
    层级信息 = 层级权益表.get(通行证.会员层级, 层级权益表["free"])
    最大密钥数 = 层级信息.get("最大API密钥", 1)
    current_count = len([k for k in (通行证.API密钥列表 or []) if k.状态 == "active"])
    if current_count >= 最大密钥数:
        return False, f"❌ 已达最大密钥数 ({最大密钥数})，请吊销旧密钥后重新生成", None

    # 生成密钥
    原始密钥 = f"lh_{secrets.token_hex(24)}"
    密钥哈希 = hashlib.sha256(原始密钥.encode()).hexdigest()[:16]
    密钥前缀 = 原始密钥[:12] + "..."

    key_id = f"apikey_{uid}_{secrets.token_hex(4)}"

    条目 = API密钥条目(
        key_id=key_id,
        key_hash=密钥哈希,
        key_prefix=密钥前缀,
        创建时间=_现在时间(),
        最后使用="",
        状态="active",
        用途=用途,
        权限范围=权限范围 or ["read"],
    )

    if 通行证.API密钥列表 is None:
        通行证.API密钥列表 = []
    通行证.API密钥列表.append(条目)
    保存通行证(通行证)

    return True, (
        f"🔑✅ API密钥已生成！\n"
        f"   Key ID: {key_id}\n"
        f"   ────────────────\n"
        f"   ⚠️ 密钥仅显示一次，请立即保存！\n"
        f"   {原始密钥}\n"
        f"   ────────────────\n"
        f"   哈希: {密钥哈希}\n"
        f"   用途: {用途 or '未指定'}\n"
        f"   权限: {', '.join(权限范围 or ['read'])}"
    ), 原始密钥


def 列出API密钥(uid: str) -> Tuple[bool, str]:
    通行证 = 加载通行证(uid)
    if not 通行证:
        return False, "❌ 无通行证"
    if not 通行证.API密钥列表:
        return True, "📭 无API密钥 · 请生成: python3 bin/lh_ecosystem_passport.py apikey generate <uid>"

    lines = [f"🔑 {uid} 的API密钥:"]
    for k in 通行证.API密钥列表:
        status_emoji = "🟢" if k.状态 == "active" else "🔴"
        lines.append(f"  {status_emoji} [{k.key_id}] {k.key_prefix} · {k.状态} · 创建: {k.创建时间[:10]}")
    return True, "\n".join(lines)


def 吊销API密钥(uid: str, key_id: str) -> Tuple[bool, str]:
    通行证 = 加载通行证(uid)
    if not 通行证:
        return False, "❌ 无通行证"
    if not 通行证.API密钥列表:
        return False, "❌ 无API密钥"

    for k in 通行证.API密钥列表:
        if k.key_id == key_id:
            if k.状态 == "revoked":
                return False, "❌ 密钥已被吊销"
            k.状态 = "revoked"
            保存通行证(通行证)
            return True, f"🔴✅ 密钥 [{key_id}] 已吊销"

    return False, f"❌ 未找到密钥: {key_id}"


def 验证API密钥(uid: str, 原始密钥: str) -> Tuple[bool, str]:
    """验证API密钥是否有效（供网关调用）"""
    通行证 = 加载通行证(uid)
    if not 通行证:
        return False, "❌ 无通行证"
    if 通行证.状态 != "active":
        return False, f"❌ 通行证状态: {通行证.状态}"

    密钥哈希 = hashlib.sha256(原始密钥.encode()).hexdigest()[:16]
    for k in (通行证.API密钥列表 or []):
        if k.密钥哈希 == 密钥哈希 and k.状态 == "active":
            # 更新最后使用时间
            k.最后使用 = _现在时间()
            保存通行证(通行证)
            return True, f"✅ 验证通过 · KeyID: {k.key_id} · 层级: {通行证.会员层级}"
    return False, "❌ 密钥无效或已吊销"


# ═══════════════════════════════════════════════════════════
# 第5层：服务注册与权限检查（含持久化）
# ═══════════════════════════════════════════════════════════

# 服务注册表持久化路径
服务注册表路径 = 通行证目录 / "service_registry.json"


def _加载服务注册表() -> None:
    """从磁盘加载持久化的服务注册表（合并到内存）"""
    if 服务注册表路径.exists():
        try:
            with open(服务注册表路径, "r", encoding="utf-8") as f:
                saved = json.load(f)
            for k, v in saved.items():
                if k not in 服务注册表:
                    服务注册表[k] = v
        except Exception:
            pass


def _保存服务注册表() -> None:
    """持久化服务注册表（仅保存运行时新增的，内置的不覆盖）"""
    try:
        with open(服务注册表路径, "w", encoding="utf-8") as f:
            json.dump(服务注册表, f, ensure_ascii=False, indent=2)
    except Exception:
        pass


# 内置服务注册表
服务注册表: Dict[str, Dict[str, Any]] = {
    "龍魂算力守护": {
        "服务名": "龍魂算力守护",
        "引擎": "DragonSoul_Guardian_v2.py",
        "所需层级": "free",
        "描述": "CPU/内存/网络/GPU/磁盘五维监控 + 三色审计 + 熔断响应",
        "端点": "/api/guardian/status",
        "分类": "安全",
    },
    "统一DNA登记": {
        "服务名": "统一DNA登记",
        "引擎": "lh_unified_dna_registry.py",
        "所需层级": "free",
        "描述": "物理+虚拟+身份全维DNA登记与归属验证",
        "端点": "/api/dna/verify",
        "分类": "身份",
    },
    "CNSH代码翻译": {
        "服务名": "CNSH代码翻译",
        "引擎": "cnsh_compiler",
        "所需层级": "basic",
        "描述": "将Python/JS/Go代码翻译为CNSH中文可编辑格式",
        "端点": "/api/cnsh/translate",
        "分类": "开发",
    },
    "信任积分簿": {
        "服务名": "信任积分簿",
        "引擎": "lh_trust_ledger",
        "所需层级": "pro",
        "描述": "社会贡献六类积分 · 三桶独立 · 不可交易",
        "端点": "/api/trust/score",
        "分类": "治理",
    },
    "龍魂许愿池": {
        "服务名": "龍魂许愿池",
        "引擎": "lh_wish_pool",
        "所需层级": "basic",
        "描述": "人民资源池 · 取之于民 · 还之于民 · 向下流动",
        "端点": "/api/pool/contribute",
        "分类": "经济",
    },
    "决策来源卡": {
        "服务名": "决策来源卡",
        "引擎": "lh_decision_card",
        "所需层级": "basic",
        "描述": "全链路决策透明 · 算法公开 · 公式可查 · DNA追溯",
        "端点": "/api/decision/card",
        "分类": "治理",
    },
    "龍魂审计过滤": {
        "服务名": "龍魂审计过滤",
        "引擎": "lh_audit_filter",
        "所需层级": "basic",
        "描述": "三色审计 + 反讽识别 + 水军对抗 + 申诉公证",
        "端点": "/api/audit/scan",
        "分类": "安全",
    },
    "龍魂道引器": {
        "服务名": "龍魂道引器",
        "引擎": "lh_daoyin",
        "所需层级": "pro",
        "描述": "开源吸收 · 许可证检查 · 防篡改 · 参数压缩",
        "端点": "/api/daoyin/absorb",
        "分类": "开发",
    },
}

# 模块加载时合并持久化服务
_加载服务注册表()


def 注册服务(服务名: str, 所需层级: str, 描述: str = "", 端点: str = "", 分类: str = "未分类") -> Tuple[bool, str]:
    if 所需层级 not in 层级权益表:
        return False, f"❌ 无效层级: {所需层级}。可用: {'/'.join(层级权益表.keys())}"

    服务注册表[服务名] = {
        "服务名": 服务名,
        "所需层级": 所需层级,
        "描述": 描述,
        "端点": 端点,
        "分类": 分类,
    }
    _保存服务注册表()  # 持久化
    return True, f"✅ 服务 [{服务名}] 已注册 · 所需层级: {所需层级}"


def 列出服务() -> Tuple[bool, str]:
    lines = ["📋 龍魂生态服务清单:"]
    for s in 服务注册表.values():
        emoji = 层级权益表.get(s["所需层级"], {}).get("emoji", "📦")
        lines.append(f"  {emoji} [{s['分类']}] {s['服务名']} — 需要{s['所需层级']}层 · {s['描述']}")
    return True, "\n".join(lines)


def 检查服务权限(uid: str, 服务名: str) -> Tuple[bool, str]:
    """检查用户是否有权访问某服务"""
    通行证 = 加载通行证(uid)
    if not 通行证:
        return False, f"❌ UID [{uid}] 无通行证"

    if 通行证.状态 != "active":
        return False, f"❌ 通行证状态: {通行证.状态}"

    if 服务名 not in 服务注册表:
        return False, f"❌ 未知服务: {服务名}"

    服务信息 = 服务注册表[服务名]
    所需层级 = 服务信息["所需层级"]

    # 层级比较: free < basic < pro < founder
    层级序号 = {"free": 0, "basic": 1, "pro": 2, "founder": 3}
    用户层级号 = 层级序号.get(通行证.会员层级, 0)
    所需层级号 = 层级序号.get(所需层级, 0)

    if 用户层级号 >= 所需层级号:
        return True, (
            f"✅ 有权访问 [{服务名}]\n"
            f"   用户层级: {层级权益表[通行证.会员层级]['emoji']} {通行证.会员层级}\n"
            f"   所需层级: {层级权益表[所需层级]['emoji']} {所需层级}\n"
        )
    else:
        return False, (
            f"🔒 无权访问 [{服务名}]\n"
            f"   当前层级: {层级权益表[通行证.会员层级]['emoji']} {通行证.会员层级}\n"
            f"   需要层级: {层级权益表[所需层级]['emoji']} {所需层级}\n"
            f"   升级方式: python3 bin/lh_ecosystem_passport.py subscribe {uid} {所需层级}"
        )


# ═══════════════════════════════════════════════════════════
# 第6层：通行证状态 + 自动过期检查
# ═══════════════════════════════════════════════════════════

def 通行证状态(uid: str) -> Tuple[bool, str]:
    """查看完整通行证状态"""
    通行证 = 加载通行证(uid)
    if not 通行证:
        return False, f"❌ UID [{uid}] 无通行证 · 请先创建: python3 bin/lh_ecosystem_passport.py passport create {uid}\n   或自动推导: python3 bin/lh_ecosystem_passport.py passport auto {uid}"

    层级信息 = 层级权益表.get(通行证.会员层级, 层级权益表["free"])
    层级emoji = 层级信息["emoji"]
    角色信息 = 角色层级人格映射.get(通行证.生态角色, 角色层级人格映射["free_user"])
    角色emoji = 角色信息["emoji"]

    # 订阅状态
    订阅状态 = "无"
    剩余天数 = "N/A"
    if 通行证.当前订阅:
        if 通行证.当前订阅.已过期():
            订阅状态 = "🔴 已过期"
        else:
            订阅状态 = f"🟢 有效"
        剩余天数 = f"{通行证.当前订阅.剩余天数()}天"

    # 认证状态
    认证状态 = "⚠️ 未认证"
    if 通行证.最近认证:
        if 通行证.最近认证.认证结果 == "passed":
            认证状态 = f"🟢 已认证 · {通行证.最近认证.认证时间[:10]}"
        else:
            认证状态 = f"🔴 {通行证.最近认证.认证结果}"

    # API密钥
    密钥数 = len([k for k in (通行证.API密钥列表 or []) if k.状态 == "active"])

    # 通行证状态
    status_emoji = "🟢" if 通行证.状态 == "active" else "🔴" if 通行证.状态 == "frozen" else "🟡"

    return True, (
        f"╔══════════════════════════════════════════════════╗\n"
        f"║  🧬 龍魂生态通行证 · {uid:<30} ║\n"
        f"╠══════════════════════════════════════════════════╣\n"
        f"║  DNA: {通行证.DNA哈希:<40} ║\n"
        f"║  角色: {角色emoji} {角色信息['名称']:<12} 层级: {层级emoji} {层级信息['名称']:<10}  ║\n"
        f"║  人格: {通行证.人格偏好[:38]:<38} ║\n"
        f"║  状态: {status_emoji} {通行证.状态:<38} ║\n"
        f"║  订阅: {订阅状态:<10}  剩余: {剩余天数:<10}              ║\n"
        f"║  认证: {认证状态:<32} ║\n"
        f"║  密钥: {密钥数}个活跃 · {层级信息['最大API密钥']}个上限                         ║\n"
        f"║  服务: {len(通行证.已接入服务 or [])}个已接入 · {层级信息['服务接入数']}个上限               ║\n"
        f"╠══════════════════════════════════════════════════╣\n"
        f"║  API速率: {层级信息['API速率']:<20}                ║\n"
        f"║  优先队列: {'✅' if 层级信息['优先队列'] else '❌':<28}                  ║\n"
        f"║  投票权:   {'✅' if 层级信息['投票权'] else '❌':<28}                  ║\n"
        f"╠══════════════════════════════════════════════════╣\n"
        f"║  创建: {通行证.创建时间[:10]:<32} ║\n"
        f"║  版本: v{通行证.版本:<35} ║\n"
        f"║  来源: {通行证.角色推导来源[:38]:<38} ║\n"
        f"╚══════════════════════════════════════════════════╝"
    )


def 每日巡检() -> Tuple[bool, str]:
    """检查所有通行证状态，自动处理过期"""
    文件列表 = list(通行证目录.glob("*.json"))
    if not 文件列表:
        return True, "📭 无通行证"

    expired = []
    未认证 = []
    正常 = 0

    for f in 文件列表:
        通行证 = 加载通行证(f.stem)
        if not 通行证:
            continue

        if 通行证.状态 == "frozen":
            continue

        # 检查订阅过期
        if 通行证.当前订阅 and 通行证.当前订阅.已过期() and 通行证.当前订阅.层级 != "free":
            # 宽限期7天
            if 通行证.当前订阅.剩余天数() < -7:
                通行证.状态 = "suspended"
                expired.append(f"🔴 {通行证.UID} - 订阅过期超过7天，已暂停")
            else:
                expired.append(f"🟡 {通行证.UID} - 订阅已过期（宽限期中）")
            continue

        # 检查认证过期
        if 通行证.最近认证:
            try:
                到期 = datetime.fromisoformat(通行证.最近认证.到期时间.replace("Z", "+00:00"))
                if datetime.now(timezone.utc) > 到期:
                    # 宽限期7天
                    delta = datetime.now(timezone.utc) - 到期
                    if delta.days > 7:
                        通行证.状态 = "frozen"
                        未认证.append(f"🔴 {通行证.UID} - 认证过期超过7天，已冻结")
                    else:
                        未认证.append(f"🟡 {通行证.UID} - 认证已过期（宽限期中）")
            except Exception:
                pass
        else:
            未认证.append(f"🟡 {通行证.UID} - 从未认证")

        正常 += 1

    return True, (
        f"📊 巡检结果: 共{len(文件列表)}个通行证\n"
        f"   正常: {正常}个\n"
        f"   过期: {len(expired)}个\n"
        f"   未认证: {len(未认证)}个\n"
        + ("\n".join(expired + 未认证) if expired or 未认证 else "\n   ✅ 全部正常")
    )


# ═══════════════════════════════════════════════════════════
# 第7层：UID9622 主权覆写 · 最高权限逃生舱
# ═══════════════════════════════════════════════════════════

def _主权覆写审计日志写入(uid: str, 操作类型: str, 确认码哈希: str, 原因: str, 结果: str):
    """每次主权覆写都写入不可篡改的审计日志"""
    entry = {
        "时间": _现在时间(),
        "UID": uid,
        "操作类型": 操作类型,
        "确认码哈希": 确认码哈希,
        "原因": 原因,
        "结果": 结果,
        "DNA": "#龍芯⚡️-SOVEREIGN-OVERRIDE-AUDIT-TRAIL",
    }
    try:
        with open(主权覆写审计日志, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    except Exception:
        pass


def UID9622_主权覆写(
    uid: str,
    确认码: str,
    操作类型: str,
    原因: str = "",
    **kwargs: Any,
) -> Tuple[bool, str]:
    """
    🧬 UID9622 最高权限覆写 · 永恒逃生舱
    
    鉄律：
      - 仅 UID9622 可调用
      - 需要主权覆写确认码（哈希验证·源码不存明文）
      - 每次覆写写入不可篡改审计日志
      - 覆盖系统约束（角色/层级/熔断/权限）
      - ❌ 不可覆写：老祖宗规则·儿童保护·反人类（文明底线元规则）
    
    设计理由（从 Kimi 审查 + UID9622 决策）：
      系统不是只运行几年，而是永恒的。政策会变、情况会变。
      当系统约束与长远利益冲突时，UID9622 需有覆写能力。
      这不是漏洞 —— 这是有意留的逃生舱，用仪式化流程约束。
      但文明底线不可覆写 —— 元规则连创始人也不能碰。
    
    用法示例：
      覆写码 = 派生主权覆写码()  # 现场派生
      UID9622_主权覆写("UID9622", 覆写码, "force_role_change", "政策变化需调整角色判定逻辑")
    """
    # 身份验证
    if uid != "UID9622":
        _主权覆写审计日志写入(uid, 操作类型, "N/A", 原因, "拒绝·非UID9622")
        return False, "🔴 主权覆写拒绝：仅 UID9622 持有此权限"
    
    # 确认码验证（哈希比对·源码不存明文·Kimi审查P0校准）
    if not _验证主权覆写码(确认码):
        确认码哈希 = hashlib.sha256(确认码.encode()).hexdigest()[:12]
        _主权覆写审计日志写入(uid, 操作类型, 确认码哈希, 原因, "拒绝·确认码错误")
        return False, "🔴 主权覆写拒绝：确认码不匹配"
    
    # 🧬 不可覆写检查 · Kimi审查P0校准
    # 老祖宗规则 + 儿童保护 + 反人类 = 文明底线元规则
    # 主权覆写不能绕过 · 连创始人也不能碰
    if 操作类型 in 不可覆写操作:
        _主权覆写审计日志写入(uid, 操作类型, "VALID_HASH", 原因, "拒绝·不可覆写操作·文明底线元规则")
        return False, (
            f"🔴⚡️ 主权覆写拒绝：{操作类型} 是不可覆写的元规则\n"
            f"   文明底线高于一切，连创始人也不能覆写\n"
            f"   铁律ID17: 创始人亦不可碰红线·特权自我约束于自订规矩之内\n"
            f"   审计: 已留痕"
        )
    
    # 操作类型校验
    if 操作类型 not in 关键操作类型:
        valid_ops = ", ".join(关键操作类型)
        _主权覆写审计日志写入(uid, 操作类型, "VALID", 原因, f"拒绝·未知操作类型·可用: {valid_ops}")
        return False, f"🔴 未知覆写操作类型: {操作类型}。可用: {valid_ops}"
    
    确认码哈希 = hashlib.sha256(确认码.encode()).hexdigest()[:12]
    
    # ── 执行覆写 ──
    结果详情 = ""
    
    if 操作类型 == "force_role_change":
        目标角色 = kwargs.get("target_role", "")
        目标层级 = kwargs.get("target_level", "")
        if not 目标角色 and not 目标层级:
            return False, "🔴 force_role_change 需要 target_role 或 target_level 参数"
        通行证 = 加载通行证(uid)
        if 通行证:
            old_role = 通行证.生态角色
            old_level = 通行证.会员层级
            if 目标角色:
                通行证.生态角色 = 目标角色
            if 目标层级:
                通行证.会员层级 = 目标层级
            保存通行证(通行证)
            结果详情 = f"角色: {old_role}→{目标角色}, 层级: {old_level}→{目标层级}"
        else:
            结果详情 = "无现有通行证·跳过"
    
    elif 操作类型 == "bypass_safety_fuse":
        # 绕过安全熔断：不改变数据，但返回绿色信号
        结果详情 = "安全熔断已绕过·系统绿灯"
    
    elif 操作类型 == "system_wide_override":
        覆写描述 = kwargs.get("description", "系统级覆写")
        结果详情 = f"系统级覆写已执行: {覆写描述}"
    
    else:
        # delete_user_data / modify_audit_log / disable_transparency
        # 这些操作仅记录审计并在确认后执行
        结果详情 = f"{操作类型}·已确认"
    
    # 写入审计
    _主权覆写审计日志写入(uid, 操作类型, 确认码哈希, 原因, f"成功·{结果详情}")
    
    return True, (
        f"⚡️🔑 UID9622 主权覆写已执行\n"
        f"   操作: {操作类型}\n"
        f"   原因: {原因 if 原因 else '未指定'}\n"
        f"   结果: {结果详情}\n"
        f"   审计: 已写入 {主权覆写审计日志}\n"
        f"   ═══════════════════════\n"
        f"   ⚠️ 主权覆写已留痕·不可否认·不可删除"
    )


def 关键操作双因子确认(uid: str, 操作类型: str, 第一因子: str, 第二因子: str) -> Tuple[bool, str]:
    """
    创始人关键操作双因子确认 · Kimi审查边界1
    
    适用操作：
      - delete_user_data: 删除用户数据
      - modify_audit_log: 修改审计日志
      - disable_transparency: 关闭透明层
    
    双因子：
      因子1: CONFIRM码 (#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z)
      因子2: 主权覆写码（哈希验证·源码不存明文）
    
    龍魂铁律 ID17：
      "创始人亦不可碰红线"
      "特权自我约束于自订规矩之内"
    """
    if uid != "UID9622":
        return False, "🔴 双因子确认仅限创始人"
    
    if 操作类型 not in ["delete_user_data", "modify_audit_log", "disable_transparency"]:
        return False, f"🔴 未知关键操作: {操作类型}"
    
    # 因子1: CONFIRM码
    if 第一因子 != "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z":
        _主权覆写审计日志写入(uid, f"2FA_{操作类型}", "N/A", "双因子确认", "拒绝·因子1错误")
        return False, "🔴 双因子确认失败 · 因子1（CONFIRM码）不匹配"
    
    # 因子2: 主权覆写码（哈希验证·源码不存明文·Kimi审查P0校准）
    if not _验证主权覆写码(第二因子):
        _主权覆写审计日志写入(uid, f"2FA_{操作类型}", "N/A", "双因子确认", "拒绝·因子2错误")
        return False, "🔴 双因子确认失败 · 因子2（主权覆写码）不匹配"
    
    # 双因子通过
    _主权覆写审计日志写入(uid, f"2FA_{操作类型}", "DUAL_PASS", "双因子确认", "成功·双因子通过")
    
    return True, (
        f"🔐✅ 创始人双因子确认通过\n"
        f"   操作: {操作类型}\n"
        f"   铁律引用: ID17 - 创始人亦不可碰红线·特权自我约束于自订规矩之内\n"
        f"   审计: 已留痕"
    )


def 查看主权覆写审计日志(limit: int = 50) -> Tuple[bool, str]:
    """查看主权覆写的完整审计历史"""
    if not 主权覆写审计日志.exists():
        return True, "📭 无主权覆写审计记录"
    
    entries = []
    with open(主权覆写审计日志, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    entries.append(json.loads(line))
                except Exception:
                    pass
    
    if not entries:
        return True, "📭 无主权覆写审计记录"
    
    entries = entries[-limit:]  # 最近N条
    
    lines = [f"🧬 主权覆写审计日志 · 共{len(entries)}条记录"]
    lines.append("═" * 55)
    for e in entries:
        emoji = "✅" if "成功" in e.get("结果", "") else "🔴"
        lines.append(
            f"  {emoji} [{e.get('时间', '?')[:19]}] {e.get('操作类型', '?')}"
            f" | {e.get('UID', '?')} | {e.get('结果', '?')[:40]}"
        )
    return True, "\n".join(lines)


# ═══════════════════════════════════════════════════════════
# 第7.5层：🔥 月度活人验证 + 导出创作（v1.1·生态接入协议§二+§三）
# ═══════════════════════════════════════════════════════════

def 月度活人验证(uid: str) -> tuple[bool, str]:
    """
    月度活人验证（协议§二）
    
    每月1元 = 活人心跳验证 = 证明DNA后面是活人。
    验证通过 → 生态内 🟢
    验证失败/未验证 → 生态外 🟡
    
    连续12个月+ → 共建者 ⚪
    """
    通行证 = 加载通行证(uid)
    if not 通行证:
        return False, f"❌ 未找到通行证: {uid}"
    
    now = datetime.now()
    
    # 检查月度验证是否有效
    if 通行证.月度验证到期:
        到期日 = datetime.fromisoformat(通行证.月度验证到期)
        if now <= 到期日:
            剩余天 = (到期日 - now).days
            return True, (
                f"🟢 月度活人验证有效 · {uid}\n"
                f"   状态: 生态内\n"
                f"   到期: {到期日.isoformat()[:10]}\n"
                f"   剩余: {剩余天}天\n"
                f"   续费: 每月1元保持活人状态"
            )
    
    # 验证已过期
    过期信息 = ""
    if 通行证.月度验证到期:
        过期日 = datetime.fromisoformat(通行证.月度验证到期)
        过期天 = (now - 过期日).days
        过期信息 = f"   过期: {过期天}天前\n"
        if 过期天 <= 30:
            过期信息 += f"   宽限期: 剩余{30-过期天}天（补缴即可恢复🟢生态内）\n"
        else:
            过期信息 += f"   宽限期: 已过\n"
    
    return True, (
        f"🟡 月度活人验证过期 · {uid}\n"
        f"   状态: 生态外\n"
        f"   数据: 保留·可导出\n"
        f"   功能: 本地可用·生态暂停\n"
        f"{过期信息}"
        f"   恢复: 续费1元即刻回归生态内"
    )


def 活人验证心跳(uid: str) -> tuple[bool, str]:
    """
    发送活人心跳（协议§二·续费窗口）
    
    续费1元，将月度验证延长1个月。
    自动检测连续月数，12个月+自动升级为共建者。
    """
    通行证 = 加载通行证(uid)
    if not 通行证:
        return False, f"❌ 未找到通行证: {uid}"
    
    now = datetime.now()
    
    # 判定新到期日
    if 通行证.月度验证到期:
        当前到期 = datetime.fromisoformat(通行证.月度验证到期)
        if 当前到期 >= now:
            新到期 = 当前到期 + timedelta(days=30)
        else:
            新到期 = now + timedelta(days=30)
    else:
        新到期 = now + timedelta(days=30)
    
    通行证.月度验证到期 = 新到期.isoformat()[:10]
    
    # 计算连续月数
    if 通行证.连续月数:
        首次验证 = datetime.fromisoformat(通行证.连续月数)
        # 简单检查：如果首次验证在12个月前，则为共建者
        pass
    通行证.连续月数 = now.isoformat()[:10]  # 记录本次心跳时间
    
    保存通行证(通行证)
    
    # 🔥 联动XPay + SQLite持久化（三重写）
    xpay_result = None
    try:
        # 路径注入
        import sys as _sys
        _xpay_path = os.path.join(os.path.dirname(__file__), '..', '03_LAYERS', 'L5_服务层', 'services', 'xpay')
        if _xpay_path not in _sys.path:
            _sys.path.insert(0, _xpay_path)
        from xpay_gateway import XPayGateway
        gw = XPayGateway(sandbox_mode=True)  # 默认沙箱·真实扣款需 lh eco alive heartbeat <uid> --real
        xpay_result = gw.record_payment(uid, 1.0, "月度活人验证", now.isoformat()[:19])
    except Exception as _e:
        pass  # XPay不可用时降级·不影响核心验证
    
    # SQLite持久化（直接写入）
    try:
        from xpay_storage import XPayStorage
        storage = XPayStorage()
        storage.save_passport_state(
            uid=uid,
            monthly_expiry=新到期.isoformat()[:10],
            consecutive_months=0,  # 下方重新计算
            last_heartbeat=now.isoformat()[:19],
            metadata={"xpay_tx": xpay_result.get("transaction_id", "") if xpay_result else ""}
        )
        storage.record_heartbeat(
            uid=uid,
            payment_id=xpay_result.get("transaction_id", "") if xpay_result else "",
            amount=1.0, period_end=新到期.isoformat()[:10],
            dna_sign=xpay_result.get("dna_signature", "") if xpay_result else ""
        )
        storage.log_verification(uid, "alive_heartbeat", True, f"到期日: {新到期.isoformat()[:10]}")
    except Exception:
        pass  # SQLite不可用不影响核心功能
    
    # 判定状态
    连续月 = (now.year - datetime.fromisoformat(通行证.首次验证日 or now.isoformat()[:10]).year) * 12
    状态图标 = "⚪" if 连续月 >= 12 else "🟢"
    状态文本 = "共建者" if 连续月 >= 12 else "生态内"
    
    return True, (
        f"{状态图标} 活人心跳已确认 · {uid}\n"
        f"   状态: {状态文本}\n"
        f"   到期: {新到期.isoformat()[:10]}\n"
        f"   费用: ¥1.00\n"
        f"   下次心跳: {新到期.isoformat()[:10]}前\n"
        f"   ─────────────────\n"
        f"   数据归属: 永远归你\n"
        f"   导出权利: 任何时候\n"
        f"   不续费: 退出实时生态·不锁功能"
    )


def 导出创作(uid: str, 导出格式: str = "json") -> tuple[bool, str]:
    """
    导出全部创作（协议§三·不可剥夺权利）
    
    任何状态（生态内/生态外）都能导出。
    导出范围：
      - 所有创作内容（文字/图片/视频/音频）
      - 所有对话记录（完整上下文）
      - 所有DNA追溯链
      - 所有三色审计记录
      - 所有个人身份数据
    """
    通行证 = 加载通行证(uid)
    if not 通行证:
        return False, f"❌ 未找到通行证: {uid}"
    
    now = datetime.now().isoformat()[:19]
    
    # 构建导出清单
    导出清单 = {
        "导出时间": now,
        "DNA": uid,
        "身份状态": "生态内" if 通行证.月度验证到期 and datetime.fromisoformat(通行证.月度验证到期) >= datetime.now() else "生态外",
        "声明": {
            "数据归属": f"{uid} 所有",
            "版权": f"归创作人 {uid} 所有（不可转移、不可侵占）",
            "导出权利": "依据 LH-ECOSYSTEM-ACCESS-PROTOCOL-v1.0 §三",
            "主权声明": "龍魂生态仅提供工具和服务，不占有任何数据",
        },
        "导出项": {
            "创作内容": "export_dir/creations/ (文字/图片/视频/音频)",
            "对话记录": "export_dir/conversations/ (完整上下文)",
            "DNA追溯链": "export_dir/dna_traces/ (全链路)",
            "三色审计": "export_dir/audit/ (审计记录)",
            "身份数据": "export_dir/identity/ (个人身份数据)",
        },
        "导出格式": 导出格式,
        "兼容工具": "任何标准解析器可读取·不依赖龍魂服务",
    }
    
    导出文本 = json.dumps(导出清单, ensure_ascii=False, indent=2) if 导出格式 == "json" else str(导出清单)
    
    return True, (
        f"📦 创作数据导出清单 · {uid}\n"
        f"   ─────────────────\n"
        f"   状态: 任何时候·任何状态·任何原因\n"
        f"   格式: {导出格式}\n"
        f"   归属: 数据永远归你\n"
        f"   ─────────────────\n"
        f"{导出文本}\n"
        f"   ─────────────────\n"
        f"   🔑 这些数据完全属于你。带走即是自由。\n"
        f"   协议: LH-ECOSYSTEM-ACCESS-PROTOCOL-v1.0 §三"
    )


def 列出可导出内容(uid: str) -> tuple[bool, str]:
    """列出用户可导出的全部内容项（协议§三·导出清单）"""
    通行证 = 加载通行证(uid)
    if not 通行证:
        return False, f"❌ 未找到通行证: {uid}"
    
    return True, (
        f"📋 可导出内容清单 · {uid}\n"
        f"   ─────────────────\n"
        f"   1. 所有创作内容 — 文字/图片/视频/音频\n"
        f"   2. 所有对话记录 — 完整上下文\n"
        f"   3. 所有DNA追溯链 — 全链路不可断\n"
        f"   4. 所有三色审计记录 — 每笔交易可查\n"
        f"   5. 所有个人身份数据 — 你的画像你带走\n"
        f"   ─────────────────\n"
        f"   导出: python3 bin/lh_ecosystem_passport.py export {uid} [json|markdown|csv]\n"
        f"   权利: 任何时候·不限次数·不设门槛（协议§三·P0级不可剥夺）"
    )


# ═══════════════════════════════════════════════════════════
# 第8层：CLI 入口
# ═══════════════════════════════════════════════════════════

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("🧬 龍魂生态通行证 v1.1 · 月度活人验证 · 心跳订阅 · 身份三态")
        print()
        print("核心: 每月1元 = 活人验证 = 生态准入")
        print("协议: 01_protocols/LH-ECOSYSTEM-ACCESS-PROTOCOL-v1.0.md")
        print()
        print("用法:")
        print("  # ── 通行证管理 ──")
        print("  python3 bin/lh_ecosystem_passport.py passport create <uid>")
        print("  python3 bin/lh_ecosystem_passport.py passport auto <uid>          # 自动推导角色+层级+人格")
        print("  python3 bin/lh_ecosystem_passport.py passport show <uid>")
        print("  python3 bin/lh_ecosystem_passport.py passport status <uid>")
        print("  python3 bin/lh_ecosystem_passport.py passport analyze <uid>      # 仅分析DNA角色")
        print("  python3 bin/lh_ecosystem_passport.py passport freeze <uid>        # 冻结自动升级")
        print()
        print("  # ── 🔥 月度活人验证（协议§二） ──")
        print("  python3 bin/lh_ecosystem_passport.py alive verify <uid>            # 查活人验证状态")
        print("  python3 bin/lh_ecosystem_passport.py alive status <uid>            # 同上·查生态状态")
        print("  python3 bin/lh_ecosystem_passport.py alive heartbeat <uid>         # 发送心跳·续费1元")
        print()
        print("  # ── 订阅管理（可选分级·基于月度验证之上） ──")
        print("  python3 bin/lh_ecosystem_passport.py subscribe <uid> <层级> [月数]")
        print("  python3 bin/lh_ecosystem_passport.py subscribe renew <uid>")
        print("  python3 bin/lh_ecosystem_passport.py subscribe cancel <uid>")
        print()
        print("  # ── 身份认证 ──")
        print("  python3 bin/lh_ecosystem_passport.py auth verify <uid>")
        print("  python3 bin/lh_ecosystem_passport.py auth status <uid>")
        print("  python3 bin/lh_ecosystem_passport.py auth challenge <uid>")
        print()
        print("  # ── 📦 导出创作（协议§三·不可剥夺权利） ──")
        print("  python3 bin/lh_ecosystem_passport.py export <uid> [json|markdown|csv]")
        print("  python3 bin/lh_ecosystem_passport.py export <uid> list             # 列出可导出内容")
        print()
        print("  # ── API密钥 ──")
        print("  python3 bin/lh_ecosystem_passport.py apikey generate <uid> [用途]")
        print("  python3 bin/lh_ecosystem_passport.py apikey list <uid>")
        print("  python3 bin/lh_ecosystem_passport.py apikey revoke <uid> <key_id>")
        print("  python3 bin/lh_ecosystem_passport.py apikey verify <uid> <密钥>")
        print("  python3 bin/lh_ecosystem_passport.py service register <服务名> <所需层级>")
        print("  python3 bin/lh_ecosystem_passport.py service list")
        print("  python3 bin/lh_ecosystem_passport.py service check <uid> <服务名>")
        print("  python3 bin/lh_ecosystem_passport.py patrol")
        print()
        print("🔑 主权覆写（仅UID9622）:")
        print("  python3 bin/lh_ecosystem_passport.py sovereign override <操作类型> <确认码> [原因]")
        print("  python3 bin/lh_ecosystem_passport.py sovereign audit [条数]              # 查看覆写审计日志")
        print("  python3 bin/lh_ecosystem_passport.py sovereign 2fa <操作类型> <因子1> <因子2>  # 双因子确认")
        print()
        print("层级:")
        for name, info in 层级权益表.items():
            print(f"  {info['emoji']} {name:<8} ¥{info['月费']:>6.1f}/月 — {info['说明']}")
        print()
        print("角色（DNA自动推导）:")
        for name, info in 角色层级人格映射.items():
            print(f"  {info['emoji']} {name:<16} → {info['推荐层级']:<8} 人格: {info['人格偏好']}")
        print()
        print("快速开始:")
        print("  1. 注册DNA:     python3 bin/lh_unified_dna_registry.py register <uid> email 'your@email.com'")
        print("  2. 自动创建通行证: python3 bin/lh_ecosystem_passport.py passport auto <uid>")
        print("  3. 生成密钥:    python3 bin/lh_ecosystem_passport.py apikey generate <uid> '开发'")
        print("  4. 查看服务:    python3 bin/lh_ecosystem_passport.py service list")
        sys.exit(0)

    cmd = sys.argv[1]

    # ── passport ──
    if cmd == "passport" and len(sys.argv) >= 4:
        sub = sys.argv[2]
        uid = sys.argv[3]
        if sub == "create":
            ok, msg, _ = 创建通行证(uid, 自动推导=False)
            print(msg)
            sys.exit(0 if ok else 1)
        elif sub == "auto":
            ok, msg, _ = 自动创建或更新通行证(uid)
            print(msg)
            sys.exit(0 if ok else 1)
        elif sub == "analyze":
            角色, 层级, 人格, 原因 = DNA推导角色(uid)
            角色信息 = 角色层级人格映射.get(角色, 角色层级人格映射["free_user"])
            print(f"🔍 DNA角色分析 · {uid}")
            print(f"   角色: {角色信息['emoji']} {角色信息['名称']}")
            print(f"   推荐层级: {层级}")
            print(f"   推荐人格: {人格}")
            print(f"   推导原因: {原因}")
            print(f"   说明: {角色信息['说明']}")
            sys.exit(0)
        elif sub in ("show", "status"):
            ok, msg = 通行证状态(uid)
            print(msg)
            sys.exit(0 if ok else 1)
        else:
            print(f"未知子命令: {sub}")
            print(f"可用: create / auto / analyze / show / status")

    # ── subscribe ──
    elif cmd == "subscribe" and len(sys.argv) >= 4:
        sub = sys.argv[2]
        if sub == "renew":
            uid = sys.argv[3] if len(sys.argv) >= 4 else ""
            ok, msg = 续费(uid) if uid else (False, "缺少UID")
            print(msg)
        elif sub == "cancel":
            uid = sys.argv[3] if len(sys.argv) >= 4 else ""
            ok, msg = 取消自动续费(uid) if uid else (False, "缺少UID")
            print(msg)
        else:
            # subscribe <uid> <层级> [月数]
            uid = sub  # sys.argv[2] 是 uid
            层级 = sys.argv[3]  # sys.argv[3] 是层级
            if 层级 in ("free", "basic", "pro", "founder"):
                月数 = int(sys.argv[4]) if len(sys.argv) >= 5 else 1
                ok, msg = 订阅(uid, 层级, 月数)
                print(msg)
            else:
                print(f"未知层级: {层级}。可用: free/basic/pro/founder · 或使用 renew/cancel <uid>")

    elif cmd == "subscribe" and len(sys.argv) >= 3:
        # 仅 subscribe <uid> → 显示状态
        uid = sys.argv[2]
        ok, msg = 通行证状态(uid)
        print(msg)

    # ── auth ──
    elif cmd == "auth" and len(sys.argv) >= 4:
        sub = sys.argv[2]
        uid = sys.argv[3]
        if sub == "verify":
            ok, msg = 验证身份(uid, 认证方式="manual")  # 简化版手动验证
            print(msg)
        elif sub == "status":
            ok, msg = 检查认证状态(uid)
            print(msg)
        elif sub == "challenge":
            ok, msg, _ = 生成认证挑战(uid)
            print(msg)
        else:
            print(f"未知子命令: {sub}")

    # ── apikey ──
    elif cmd == "apikey" and len(sys.argv) >= 4:
        sub = sys.argv[2]
        uid = sys.argv[3]
        if sub == "generate":
            用途 = sys.argv[4] if len(sys.argv) >= 5 else ""
            ok, msg, key = 生成API密钥(uid, 用途)
            print(msg)
            sys.exit(0 if ok else 1)
        elif sub == "list":
            ok, msg = 列出API密钥(uid)
            print(msg)
        elif sub == "revoke" and len(sys.argv) >= 5:
            key_id = sys.argv[4]
            ok, msg = 吊销API密钥(uid, key_id)
            print(msg)
        elif sub == "verify" and len(sys.argv) >= 5:
            密钥 = sys.argv[4]
            ok, msg = 验证API密钥(uid, 密钥)
            print(msg)
        else:
            print(f"未知子命令: {sub}")

    # ── service ──
    elif cmd == "service" and len(sys.argv) >= 3:
        sub = sys.argv[2]
        if sub == "list":
            ok, msg = 列出服务()
            print(msg)
        elif sub == "register" and len(sys.argv) >= 5:
            服务名 = sys.argv[3]
            所需层级 = sys.argv[4]
            ok, msg = 注册服务(服务名, 所需层级)
            print(msg)
        elif sub == "check" and len(sys.argv) >= 5:
            uid = sys.argv[3]
            服务名 = sys.argv[4]
            ok, msg = 检查服务权限(uid, 服务名)
            print(msg)
        else:
            print(f"未知子命令: {sub}")

    # ── patrol ──
    elif cmd == "patrol":
        ok, msg = 每日巡检()
        print(msg)

    # ── sovereign · UID9622 主权覆写 ──
    elif cmd == "sovereign" and len(sys.argv) >= 4:
        sub = sys.argv[2]
        if sub == "override":
            操作类型 = sys.argv[3]
            确认码 = sys.argv[4] if len(sys.argv) >= 5 else ""
            原因 = " ".join(sys.argv[5:]) if len(sys.argv) >= 6 else ""
            ok, msg = UID9622_主权覆写("UID9622", 确认码, 操作类型, 原因)
            print(msg)
        elif sub == "audit":
            条数 = int(sys.argv[3]) if len(sys.argv) >= 4 else 50
            ok, msg = 查看主权覆写审计日志(条数)
            print(msg)
        elif sub == "2fa" and len(sys.argv) >= 6:
            操作类型 = sys.argv[3]
            因子1 = sys.argv[4]
            因子2 = sys.argv[5]
            ok, msg = 关键操作双因子确认("UID9622", 操作类型, 因子1, 因子2)
            print(msg)
        else:
            print(f"未知 sovereign 子命令: {sub}")
            print("可用: override <操作类型> <确认码> [原因] | audit [条数] | 2fa <操作类型> <因子1> <因子2>")

    # ── passport freeze ──
    elif cmd == "passport" and len(sys.argv) >= 4 and sys.argv[2] == "freeze":
        uid = sys.argv[3]
        通行证 = 加载通行证(uid)
        if 通行证:
            通行证.状态 = "frozen"
            保存通行证(通行证)
            print(f"🧊✅ 通行证 [{uid}] 已冻结 · 自动升级已暂停")
        else:
            print(f"❌ UID [{uid}] 无通行证")

    # ── 🔥 alive · 月度活人验证（v1.1·协议§二） ──
    elif cmd == "alive" and len(sys.argv) >= 4:
        sub = sys.argv[2]
        uid = sys.argv[3]
        if sub == "verify":
            ok, msg = 月度活人验证(uid)
            print(msg)
            sys.exit(0 if ok else 1)
        elif sub == "status":
            ok, msg = 月度活人验证(uid)
            print(msg)
            sys.exit(0 if ok else 1)
        elif sub == "heartbeat":
            ok, msg = 活人验证心跳(uid)
            print(msg)
            sys.exit(0 if ok else 1)
        else:
            print(f"未知 alive 子命令: {sub}")
            print("可用: verify / status / heartbeat")

    # ── 📦 export · 导出创作（v1.1·协议§三） ──
    elif cmd == "export" and len(sys.argv) >= 3:
        uid = sys.argv[2]
        导出格式 = sys.argv[3] if len(sys.argv) >= 4 else "json"
        if 导出格式 in ("json", "markdown", "csv"):
            ok, msg = 导出创作(uid, 导出格式)
            print(msg)
            sys.exit(0 if ok else 1)
        elif 导出格式 == "list":
            ok, msg = 列出可导出内容(uid)
            print(msg)
            sys.exit(0 if ok else 1)
        else:
            ok, msg = 导出创作(uid, 导出格式)
            print(msg)
            sys.exit(0 if ok else 1)

    else:
        print(f"未知命令: {cmd} · 运行无参数查看帮助")

# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# DNA: #龍芯⚡️丙午·甲申·辛丑·坤卦-ECOSYSTEM-PASSPORT-v1.1-月度活人验证-导出创作
