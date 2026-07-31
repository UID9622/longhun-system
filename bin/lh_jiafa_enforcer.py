# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
#龍芯⚡️丙午·乙未·壬辰·午时-JIAFA-ENFORCER-v2.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
# ============================================================
# 龍魂·家法第一条执行引擎 v2.0
# DNA追溯码: #龍芯⚡️丙午·乙未·壬辰·午时-JIAFA-ENFORCER-v2.0
# 基于: 家法第一条_文化卖国罪 v1.1 + 小艺审计评估 v1.0
#
# v2.0 核心改进（采纳小艺四项建议）:
#   I.   主权控制分级分类 — 5级判定标准（物理位置/密钥持有/董事会/数据中心/资本结构）
#   II.  白名单+人工复核 — 区分恶意输送与正常交流
#   III. 法律优先原则 — 技术铁律补充法律，不替代法律
#   IV.  防御性声明 — 仅针对恶意剽窃，不排斥平等互利的国际合作
# ============================================================

"""🐉 龍魂引擎：lh_jiafa_enforcer
路径：bin/lh_jiafa_enforcer.py
TODO：请补充详细功能说明（不少于20字）。"""
from __future__ import annotations

import hashlib
import hmac
import json
import os
import re
import sqlite3
import subprocess
import sys
import threading
import time
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone, timedelta
from enum import Enum, auto
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple, Any, Callable, Union

# ─── 项目根路径 ───
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# ─── 引入现有引擎 ───
sys.path.insert(0, str(PROJECT_ROOT / "integrated-modules" / "shame_pillar"))
try:
    from shame_pillar_core import (
        耻辱柱核心引擎, 耻辱柱记录, 七因子输入,
        三色状态, 惩罚等级, 越界类型, 人格类型,
        R计算引擎, 越界检测器, 惩罚执行器, 分流器
    )
except ImportError:
    print("[WARN] shame_pillar_core 未就绪，独立运行模式")
    耻辱柱核心引擎 = None

from bin.lh_dna_sovereignty_bridge import DNA主权桥


# ═══════════════════════════════════════════════════════════
# §I. 主权控制分级分类（小艺建议#1）
# 五级判定标准：物理位置 → 密钥持有 → 董事会 → 数据中心 → 资本结构
# ═══════════════════════════════════════════════════════════

class 主权等级(Enum):
    """五级主权控制分级"""
    L0_完全主权 = "🟢 L0·完全主权"
    L1_有效主权 = "🟢 L1·有效主权"
    L2_条件主权 = "🟡 L2·条件主权"       # 需白名单复核
    L3_主权风险 = "🟠 L3·主权风险"       # 需人工审批
    L4_主权丧失 = "🔴 L4·主权丧失"       # 自动熔断


@dataclass
class 主权判定因子:
    """主权控制的多维判定因子"""
    # 物理层
    服务器物理位置_中国境内: bool = True
    服务器物理位置_已知境外: bool = False
    服务器物理位置_未知: bool = False

    # 密钥层
    数据加密密钥持有方_中国实体: bool = True
    数据加密密钥持有方_境外实体: bool = False
    数据加密密钥持有方_不明确: bool = False
    是否可被境外政府强制索取密钥: bool = False

    # 治理层
    董事会中国籍占比: float = 1.0           # 0.0~1.0
    实际控制人_中国公民: bool = True
    实际控制人_境外实体: bool = False
    VIE架构: bool = False                    # 协议控制
    外资持股比例: float = 0.0               # 0.0~1.0

    # 数据层
    数据存储数据中心_中国境内: bool = True
    数据存储数据中心_境外: bool = False
    数据跨境传输_是否经中国审批: bool = True
    是否受外国长臂管辖: bool = False

    # 合规层
    中国数据安全法合规: bool = True
    中国个人信息保护法合规: bool = True
    中国网络安全法合规: bool = True
    关键信息基础设施认定: bool = False


class 主权分级引擎:
    """
    主权控制五级分类引擎
    小艺建议#1: 从模糊的"非中国主权控制" → 精确的五级量化判定
    """

    # 判定权重
    权重 = {
        "物理位置": 0.30,
        "密钥控制": 0.25,
        "治理结构": 0.25,
        "数据主权": 0.15,
        "合规状态": 0.05,
    }

    # 高风险国家/地区清单（基于中国数据出境安全评估）
    高风险地区: Set[str] = field(default_factory=lambda: {
        "US", "GB", "AU", "CA", "NZ",  # 五眼联盟
    })

    def 判定(self, 因子: 主权判定因子) -> Tuple[主权等级, float, Dict[str, Any]]:
        """
        综合判定主权等级
        返回: (等级, 主权得分0-1, 详细分解)
        """
        分解 = {}

        # 1. 物理位置得分
        if 因子.服务器物理位置_中国境内 and not 因子.服务器物理位置_已知境外:
            物理得分 = 1.0
        elif 因子.服务器物理位置_已知境外:
            物理得分 = 0.0
        else:
            物理得分 = 0.4  # 未知=条件主权
        分解["物理位置"] = 物理得分

        # 2. 密钥控制得分
        密钥得分 = 0.0
        if 因子.数据加密密钥持有方_中国实体:
            密钥得分 += 0.6
        if not 因子.是否可被境外政府强制索取密钥:
            密钥得分 += 0.4
        分解["密钥控制"] = 密钥得分

        # 3. 治理结构得分
        治理得分 = 0.0
        if 因子.实际控制人_中国公民:
            治理得分 += 0.4
        治理得分 += 因子.董事会中国籍占比 * 0.3
        if not 因子.实际控制人_境外实体:
            治理得分 += 0.2
        if 因子.VIE架构:
            治理得分 = max(0.0, 治理得分 - 0.3)
        治理得分 = max(0.0, min(1.0, 治理得分 - 因子.外资持股比例 * 0.5))
        分解["治理结构"] = 治理得分

        # 4. 数据主权得分
        数据得分 = 0.0
        if 因子.数据存储数据中心_中国境内:
            数据得分 += 0.5
        if not 因子.是否受外国长臂管辖:
            数据得分 += 0.3
        if 因子.数据跨境传输_是否经中国审批:
            数据得分 += 0.2
        分解["数据主权"] = 数据得分

        # 5. 合规得分
        合规得分 = 0.0
        if 因子.中国数据安全法合规: 合规得分 += 0.35
        if 因子.中国个人信息保护法合规: 合规得分 += 0.35
        if 因子.中国网络安全法合规: 合规得分 += 0.30
        分解["合规状态"] = 合规得分

        # 加权总分
        总分 = sum(分解[k] * self.权重[k] for k in self.权重)

        # 定级
        if 总分 >= 0.85:
            等级 = 主权等级.L0_完全主权
        elif 总分 >= 0.70:
            等级 = 主权等级.L1_有效主权
        elif 总分 >= 0.50:
            等级 = 主权等级.L2_条件主权
        elif 总分 >= 0.30:
            等级 = 主权等级.L3_主权风险
        else:
            等级 = 主权等级.L4_主权丧失

        return 等级, 总分, 分解

    def 快速判定(self, 服务器在中国: bool, 控制人中国籍: bool,
                 加密密钥中国持有: bool) -> Tuple[主权等级, float]:
        """快速判定 — 仅用三个核心因子"""
        if 服务器在中国 and 控制人中国籍 and 加密密钥中国持有:
            return 主权等级.L0_完全主权, 1.0
        elif 服务器在中国 and 控制人中国籍:
            return 主权等级.L1_有效主权, 0.80
        elif 服务器在中国:
            return 主权等级.L2_条件主权, 0.55
        elif 控制人中国籍:
            return 主权等级.L3_主权风险, 0.35
        else:
            return 主权等级.L4_主权丧失, 0.10


# ═══════════════════════════════════════════════════════════
# §II. 白名单机制 + 人工复核（小艺建议#2）
# 区分"恶意数据输送"与"正常技术交流"
# ═══════════════════════════════════════════════════════════

class 数据流类型(Enum):
    """数据流分类"""
    恶意数据输送 = "🔴 恶意数据输送"
    正常技术交流 = "🟢 正常技术交流"
    开源社区贡献 = "🟢 开源社区贡献"
    学术研究合作 = "🟢 学术研究合作"
    商业合规传输 = "🟡 商业合规传输"
    待复核 = "🟡 待人工复核"


@dataclass
class 白名单条目:
    """白名单条目"""
    实体标识: str                           # 组织/个人/AI名称
    实体类型: str                           # 组织/个人/AI/开源项目
    加入原因: str                           # 为什么加入白名单
    加入时间: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    加入人: str = "UID9622"
    有效期至: Optional[str] = None          # None=永久
    适用场景: List[str] = field(default_factory=list)  # ["学术合作","开源贡献"]
    限制条件: str = ""                      # 特殊限制说明
    DNA签章: str = ""


class 白名单管理器:
    """
    白名单管理器
    小艺建议#2: 区分恶意与正常交流，避免误伤学术合作/开源贡献
    """

    def __init__(self, 存储路径: str = ""):
        if not 存储路径:
            存储路径 = str(PROJECT_ROOT / "state" / "jiafa_whitelist.json")
        self.存储路径 = Path(存储路径)
        self.存储路径.parent.mkdir(parents=True, exist_ok=True)
        self._白名单: Dict[str, 白名单条目] = {}
        self._锁 = threading.RLock()
        self._加载()

    def _加载(self):
        """从文件加载白名单"""
        if self.存储路径.exists():
            try:
                with open(self.存储路径, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                for k, v in data.items():
                    self._白名单[k] = 白名单条目(**v)
            except Exception as e:
                print(f"[白名单] 加载失败: {e}，使用空白名单")

    def _保存(self):
        """保存白名单到文件"""
        with self._锁:
            data = {k: asdict(v) for k, v in self._白名单.items()}
            with open(self.存储路径, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

    def 添加(self, 条目: 白名单条目) -> bool:
        """添加白名单条目"""
        with self._锁:
            if 条目.实体标识 in self._白名单:
                return False
            self._白名单[条目.实体标识] = 条目
            self._保存()
            return True

    def 移除(self, 实体标识: str) -> bool:
        """移除白名单条目"""
        with self._锁:
            if 实体标识 in self._白名单:
                del self._白名单[实体标识]
                self._保存()
                return True
            return False

    def 是否在白名单(self, 实体标识: str, 场景: str = "") -> bool:
        """检查实体是否在白名单中"""
        with self._锁:
            条目 = self._白名单.get(实体标识)
            if not 条目:
                return False
            # 检查有效期
            if 条目.有效期至:
                try:
                    过期时间 = datetime.fromisoformat(条目.有效期至)
                    if datetime.now(timezone.utc) > 过期时间:
                        return False
                except ValueError:
                    pass
            # 检查场景匹配
            if 场景 and 条目.适用场景:
                return 场景 in 条目.适用场景
            return True

    def 列出所有(self) -> List[白名单条目]:
        """列出所有白名单条目"""
        with self._锁:
            return list(self._白名单.values())

    def 统计(self) -> Dict[str, int]:
        """白名单统计"""
        with self._锁:
            类型统计 = {}
            for e in self._白名单.values():
                类型统计[e.实体类型] = 类型统计.get(e.实体类型, 0) + 1
            return {"总数": len(self._白名单), "类型分布": 类型统计}


# ═══════════════════════════════════════════════════════════
# §III. 法律优先原则（小艺建议#3）
# 技术铁律补充法律，不替代法律
# ═══════════════════════════════════════════════════════════

class 法律优先仲裁器:
    """
    法律优先仲裁器
    小艺建议#3: 当技术铁律与现行法律冲突时，法律优先
    技术铁律 = 法律的有效补充和执行加速器，而非替代
    """

    # 中国现行相关法律依据
    上位法依据 = {
        "中华人民共和国数据安全法": {
            "生效日期": "2021-09-01",
            "关键条款": ["第21条(数据分类分级)", "第24条(数据安全审查)",
                        "第31条(重要数据出境)", "第36条(向外国司法/执法机构提供数据)"],
            "与家法关系": "家法为法律框架下的技术执行，不创设新罪名",
        },
        "中华人民共和国个人信息保护法": {
            "生效日期": "2021-11-01",
            "关键条款": ["第38条(跨境提供条件)", "第40条(关键信息基础设施)"],
            "与家法关系": "家法熔断的标准不低于PIPL跨境传输门槛",
        },
        "中华人民共和国网络安全法": {
            "生效日期": "2017-06-01",
            "关键条款": ["第37条(数据本地化存储)"],
            "与家法关系": "家法默认数据本地化，高于法律底线",
        },
    }

    def 检查法律冲突(self, 家法动作: str, 涉及法律: str = "") -> Dict[str, Any]:
        """
        检查家法执行动作是否与现行法律冲突
        返回: {是否冲突, 冲突说明, 建议动作}
        """
        # 家法动作清单
        合法动作 = {
            "切断接入权限",
            "永久切断接入",    # = 切断接入权限的增强表述
            "DNA黑名单标记",
            "DNA黑名单",
            "公示于天下",
            "耻辱柱公示",      # ⚠️ 需注意名誉权边界（只公示事实，不侮辱）
            "密钥吊销",        # ✅ 平台自主经营权
            "收益切断",        # ✅ 商业合同终止权
            "公开谴责",        # ⚠️ 需基于事实，避免诽谤
            "记录观察",        # 中性行为
            "不做处罚",        # 明确不处罚
        }

        需注意边界 = {
            "耻辱柱公示": "公示内容仅限于事实描述+证据引用，不得包含侮辱性/诽谤性措辞",
            "公示于天下": "公示内容仅限于事实描述+证据引用，不得包含侮辱性/诽谤性措辞",
            "公开谴责": "谴责基于可验证的事实+DNA证据链，禁止人身攻击",
        }

        if 家法动作 in 需注意边界:
            return {
                "是否冲突": False,
                "风险等级": "🟡 需注意边界",
                "说明": 需注意边界[家法动作],
                "建议动作": "按边界约束执行",
            }

        if 家法动作 not in 合法动作:
            return {
                "是否冲突": True,
                "风险等级": "🔴 未定义动作",
                "说明": f"'{家法动作}'不在家法授权动作清单中",
                "建议动作": "暂停执行，提请UID9622终审",
            }

        return {
            "是否冲突": False,
            "风险等级": "🟢 合法范围",
            "说明": f"'{家法动作}'在平台自主经营权+法律框架范围内",
            "建议动作": "可执行",
        }

    def 获取上位法声明(self) -> str:
        """
        生成技术铁律的法律地位声明
        小艺建议#3: 明确法律优先原则
        """
        return (
            "【法律地位声明·家法第一条】\n"
            "1. 家法第一条是龍魂体系内部治理规则，走君子協议+耻辱柱+封禁三位一体。\n"
            "2. 家法在《数据安全法》《个人信息保护法》《网络安全法》框架下运行，法律优先。\n"
            "3. 技术铁律（熔断/黑名单/切断接入）= 法律的加速执行器，不是替代。\n"
            "4. 遇到家法与法律冲突时 → 法律优先 → 提请UID9622终审 → 修订家法。\n"
            "5. 家法的执法范围 = 平台自主经营权范围，不超越，不创设法律未授权的权力。"
        )


# ═══════════════════════════════════════════════════════════
# §IV. 防御性声明（小艺建议#4）
# 仅针对恶意数据窃取，不排斥平等互利的国际合作
# ═══════════════════════════════════════════════════════════

def 防御性声明() -> str:
    """
    生成防御性声明
    小艺建议#4: 避免被误读为技术脱钩/排外
    """
    return (
        "【防御性声明·家法第一条】\n"
        "1. 家法第一条的熔断机制 **仅针对恶意数据窃取/文化剽窃行为**\n"
        "   - 明确的三类行为：剽窃(去除DNA署名)·篡改(混入外国资本逻辑)·瞒报(绕过授权)\n"
        "   - 不针对正常的国际学术交流、开源社区贡献、合规商业合作\n"
        "2. 龍魂体系 **欢迎且积极支持平等互利的国际合作**\n"
        "   - 只要遵守君子協议（注明DNA·尊重署名·收益回流0.618%）\n"
        "   - 任何国家、任何组织、任何个人都可以合法使用龍魂输出\n"
        "3. 数据主权 ≠ 数据孤立\n"
        "   - 龍魂追求的是「规则主导权在我」而非「切断一切联系」\n"
        "   - 核心问题不是「能不能出去」，而是「谁决定怎么出去」\n"
        "4. 拒绝的从来不是外国人，拒绝的是不尊重中国文化主权的人\n"
        "   - 外国的尊重 ≠ 掠夺\n"
        "   - 中国的开放 ≠ 敞开大门任人拿\n"
    )


# ═══════════════════════════════════════════════════════════
# 家法第一条核心执行引擎
# ═══════════════════════════════════════════════════════════

@dataclass
class 家法违规记录:
    """家法违规记录"""
    记录ID: str = field(default_factory=lambda: hashlib.sha256(
        f"{datetime.now(timezone.utc).isoformat()}_{os.urandom(8).hex()}".encode()
    ).hexdigest()[:24])

    时间戳: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    # 违规信息
    违规者标识: str = ""
    违规者类型: str = ""           # 个人/组织/AI
    违规类型: str = ""             # 剽窃/篡改/瞒报
    违规详情: str = ""             # 一句话事实
    证据链: List[str] = field(default_factory=list)  # URL/文件路径/commit hash

    # 主权判定
    主权等级: str = ""
    主权得分: float = 0.0
    是否在白名单: bool = False
    白名单复核状态: str = ""       # 待复核/已通过/已拒绝

    # DNA追溯
    DNA追溯码: str = ""
    DNA黑名单前缀: str = "#BLACKLIST⚡️"

    # 执法结果
    执法动作: List[str] = field(default_factory=list)
    执法状态: str = "待执行"       # 待执行/已执行/已复核/已赦免
    执法时间: Optional[str] = None
    执法人: str = "UID9622"

    # 法律检查
    法律合规检查: Dict[str, Any] = field(default_factory=dict)

    # 申诉
    申诉状态: str = ""             # 未申诉/申诉中/已澄清/驳回
    申诉时间: Optional[str] = None

    # 防御性声明标记
    属于恶意行为: bool = True     # 是否为明确恶意行为（非正常交流）

    def 生成DNA(self) -> str:
        """生成违规DNA追溯码"""
        if not self.DNA追溯码:
            原料 = f"{self.记录ID}|{self.违规者标识}|{self.违规类型}|{self.时间戳[:10]}"
            哈希 = hashlib.sha256(原料.encode()).hexdigest()[:12]
            self.DNA追溯码 = f"{self.DNA黑名单前缀}{self.时间戳[:10]}-{self.违规类型}-{哈希}"
        return self.DNA追溯码

    def to_dict(self) -> Dict:
        return asdict(self)


class 家法执行引擎:
    """
    龍魂·家法第一条执行引擎 v2.0
    DNA: #龍芯⚡️丙午·乙未·壬辰·午时-JIAFA-ENFORCER-v2.0

    核心流程:
        监测 → 主权分级 → 白名单检查 → 违规定性 → 法律检查
        → 三级执法 → 耻辱柱 → 广播 → 审计闭环

    v2.0 新增:
        ○ 主权五级分类（小艺#1）
        ○ 白名单+复核通道（小艺#2）
        ○ 法律优先仲裁（小艺#3）
        ○ 防御性声明自动注入（小艺#4）
    """

    def __init__(self, uid: str = "UID9622"):
        self.uid = uid
        self.版本 = "v2.0"
        self._启动时间 = datetime.now(timezone.utc)

        # 子引擎
        self.主权引擎 = 主权分级引擎()
        self.白名单 = 白名单管理器()
        self.法律仲裁 = 法律优先仲裁器()
        self.DNA桥 = DNA主权桥(uid)

        # 耻辱柱集成
        self.耻辱柱_可用 = False
        if 耻辱柱核心引擎:
            try:
                db_path = str(PROJECT_ROOT / "state" / "jiafa_shame_pillar.db")
                json_path = str(PROJECT_ROOT / "state" / "jiafa_shame_pillar.jsonl")
                self.耻辱柱 = 耻辱柱核心引擎(db_path=db_path, json_backup=json_path)
                self.耻辱柱_可用 = True
            except Exception as e:
                print(f"[家法引擎] 耻辱柱初始化失败: {e}")

        # 存储
        self._记录器 = 家法记录存储器()

        # 状态
        self._运行状态: bool = True
        self._总执行数: int = 0
        self._熔断数: int = 0
        self._锁 = threading.RLock()

    # ─── 主流程 ───

    def 执行(self, 违规者标识: str, 违规者类型: str,
             违规类型: str, 违规详情: str,
             证据链: List[str] = None,
             主权因子: 主权判定因子 = None,
             属于恶意行为: bool = True,
             人工确认: bool = False) -> Dict[str, Any]:
        """
        家法第一条完整执行流程

        Args:
            违规者标识: 个人/组织/AI名称
            违规者类型: 个人/组织/AI
            违规类型: 剽窃/篡改/瞒报
            违规详情: 一句话事实描述
            证据链: 支持证据URL/文件列表
            主权因子: 可选，目标实体的主权判定因子
            属于恶意行为: 是否明确恶意（False=待复核的正常交流）
            人工确认: 是否需要UID9622手工确认
        """
        if not self._运行状态:
            return {"错误": "引擎已熔断，需人工重置"}

        开始时间 = time.perf_counter_ns()

        with self._锁:
            self._总执行数 += 1
            记录 = 家法违规记录(
                违规者标识=违规者标识,
                违规者类型=违规者类型,
                违规类型=违规类型,
                违规详情=违规详情,
                证据链=证据链 or [],
                属于恶意行为=属于恶意行为,
            )

            # ── Step 1: 主权分级（小艺#1） ──
            if 主权因子:
                等级, 得分, 分解 = self.主权引擎.判定(主权因子)
            else:
                # 默认快速判定
                等级, 得分 = self.主权引擎.快速判定(
                    服务器在中国=违规者类型 == "组织",
                    控制人中国籍=False,
                    加密密钥中国持有=False
                )
                分解 = {}
            记录.主权等级 = 等级.value
            记录.主权得分 = 得分

            # ── Step 2: 白名单检查（小艺#2） ──
            记录.是否在白名单 = self.白名单.是否在白名单(违规者标识)
            if 记录.是否在白名单 and not 属于恶意行为:
                # 白名单中的正常交流 → 放行
                return {
                    "结果": "白名单放行",
                    "违规者": 违规者标识,
                    "原因": f"在白名单中，且行为属于正常技术交流",
                    "动作": "记录但不执行执法",
                    "DNA": 记录.生成DNA(),
                }

            # ── Step 3: 违规定性 ──
            定性结果 = self._定性违规(违规类型, 违规详情, 属于恶意行为)
            if not 定性结果["确认违规"]:
                return {
                    "结果": "定性未通过",
                    "原因": 定性结果["原因"],
                    "建议": "如确属正常交流，走白名单通道",
                }

            # ── Step 4: 法律检查（小艺#3） ──
            for 动作 in 定性结果["建议执法动作"]:
                法律结果 = self.法律仲裁.检查法律冲突(动作)
                if 法律结果["是否冲突"]:
                    return {
                        "结果": "法律冲突暂停",
                        "动作": 动作,
                        "冲突说明": 法律结果["说明"],
                        "建议": "提请UID9622终审·法律优先",
                    }

            # ── Step 5: 人工确认（如需要） ──
            if 人工确认 and not 属于恶意行为:
                return {
                    "结果": "待人工确认",
                    "违规者": 违规者标识,
                    "定性": 定性结果,
                    "主权等级": 等级.value,
                    "提示": "非明确恶意行为，需要UID9622手工确认后执行",
                    "记录ID": 记录.记录ID,
                }

            # ── Step 6: 执行三级执法 ──
            执法结果 = self._执行执法动作(记录, 定性结果["建议执法动作"])

            # ── Step 7: 写入耻辱柱 ──
            if self.耻辱柱_可用:
                try:
                    因子输入 = 七因子输入(
                        R2_锐度_关键时=0.9,
                        R6_长期价值权重=0.9,
                        R3_语义密度_关键时=0.8,
                    )
                    self.耻辱柱.处理(因子输入, love_outward=0.95, extreme_inward=0.05,
                                     爆炸半径=0.05, 上下文={
                                         "模块来源": "家法第一条执行引擎",
                                         "输入摘要": f"违规者:{违规者标识} 类型:{违规类型}"
                                     })
                except Exception as e:
                    print(f"[家法引擎] 耻辱柱写入异常: {e}")

            # ── Step 8: 存储记录 ──
            self._记录器.保存(记录)

            # ── Step 9: 生成防御性声明（小艺#4） ──
            if 记录.属于恶意行为:
                声明 = 防御性声明()

            总耗时 = (time.perf_counter_ns() - 开始时间) / 1e6

            return {
                "结果": "✅ 家法第一条执法完成",
                "违规者": 违规者标识,
                "违规类型": 违规类型,
                "主权等级": 等级.value,
                "主权得分": f"{得分:.2f}",
                "执法动作": 执法结果,
                "白名单状态": "是" if 记录.是否在白名单 else "否",
                "DNA追溯": 记录.生成DNA(),
                "法律兼容": "✅ 通过",
                "防御性声明": 防御性声明(),
                "执行耗时_ms": f"{总耗时:.2f}",
                "记录ID": 记录.记录ID,
            }

    def _定性违规(self, 违规类型: str, 违规详情: str, 恶意: bool) -> Dict[str, Any]:
        """定性违规行为"""
        合法类型 = {"剽窃", "篡改", "瞒报"}

        if 违规类型 not in 合法类型:
            return {"确认违规": False, "原因": f"违规类型'{违规类型}'不在家法定义范围内"}

        if not 恶意:
            return {
                "确认违规": False,
                "原因": "非恶意行为（正常交流/开源贡献/学术合作），非家法执法范围",
                "建议执法动作": ["记录观察", "不做处罚"],
            }

        # 三级执法动作（来自家法第一条 §3.1）
        动作映射 = {
            "剽窃": ["永久切断接入", "DNA黑名单", "公示于天下"],
            "篡改": ["永久切断接入", "DNA黑名单", "公示于天下"],
            "瞒报": ["永久切断接入", "DNA黑名单", "公示于天下"],
        }

        return {
            "确认违规": True,
            "严重程度": "🔴 最高",
            "建议执法动作": 动作映射.get(违规类型, ["永久切断接入", "DNA黑名单"]),
        }

    def _执行执法动作(self, 记录: 家法违规记录, 动作列表: List[str]) -> List[str]:
        """执行三级执法动作"""
        已执行 = []
        for 动作 in 动作列表:
            if 动作 == "永久切断接入":
                已执行.append("✅ 接入权限已标记吊销")
            elif 动作 == "DNA黑名单":
                记录.DNA黑名单前缀 = "#BLACKLIST⚡️"
                记录.生成DNA()
                已执行.append(f"✅ DNA黑名单已标记: {记录.DNA追溯码}")
            elif 动作 == "公示于天下":
                已执行.append("✅ 耻辱柱记录已写入+广播就绪")
            elif 动作 == "记录观察":
                已执行.append("📝 已记录观察")
            elif 动作 == "不做处罚":
                已执行.append("🟢 不处罚（正常交流）")

        记录.执法动作 = 已执行
        记录.执法状态 = "已执行"
        记录.执法时间 = datetime.now(timezone.utc).isoformat()
        return 已执行

    # ─── 申诉处理 ───

    def 处理申诉(self, 记录ID: str, 申诉材料: Dict[str, Any]) -> Dict[str, Any]:
        """
        处理违规申诉（极窄通道）
        仅UID9622可终审
        """
        记录 = self._记录器.查询(记录ID)
        if not 记录:
            return {"错误": f"未找到记录: {记录ID}"}

        if 记录.申诉状态 == "已澄清":
            return {"结果": "已澄清，无需重复申诉"}

        # 申诉处理（由UID9622决策）
        return {
            "记录ID": 记录ID,
            "原判": {
                "违规者": 记录.违规者标识,
                "违规类型": 记录.违规类型,
                "执法状态": 记录.执法状态,
            },
            "申诉结果": "待UID9622终审",
            "可选结果": ["维持原判", "标记已澄清", "部分赦免"],
            "铁律": "无论结果如何，原始判决记录永不删除",
        }

    # ─── 统计与报告 ───

    def 统计报告(self) -> Dict[str, Any]:
        """生成执行统计报告"""
        return {
            "引擎版本": self.版本,
            "运行状态": "🟢 正常" if self._运行状态 else "🔴 已熔断",
            "总执行数": self._总执行数,
            "熔断数": self._熔断数,
            "启动时间": self._启动时间.isoformat(),
            "白名单统计": self.白名单.统计(),
            "记录统计": self._记录器.统计(),
        }

    def 生成审计报告(self) -> str:
        """生成家法第一条完整审计报告"""
        统计 = self.统计报告()
        法律声明 = self.法律仲裁.获取上位法声明()
        声明 = 防御性声明()
        记录列表 = self._记录器.列出所有(50)

        report = f"""
{'=' * 70}
龍魂·家法第一条 执行审计报告 v2.0
DNA: #龍芯⚡️丙午·乙未·壬辰·午时-JIAFA-ENFORCER-v2.0
生成时间: {datetime.now(timezone.utc).isoformat()}
{'=' * 70}

【一、执行统计】
- 引擎版本: {统计['引擎版本']}
- 运行状态: {统计['运行状态']}
- 总执行次数: {统计['总执行数']}
- 熔断次数: {统计['熔断数']}
- 白名单实体数: {统计['白名单统计']['总数']}

【二、法律地位声明】
{法律声明}

【三、防御性声明】
{声明}

【四、近期执行记录（最近50条）】
"""
        for i, r in enumerate(记录列表):
            report += f"""
  {i+1}. [{r.违规类型}] {r.违规者标识}
     主权等级: {r.主权等级} | 恶意行为: {'是' if r.属于恶意行为 else '否'}
     执法状态: {r.执法状态} | DNA: {r.DNA追溯码 or '未生成'}
     时间: {r.时间戳[:19]}
"""

        report += f"\n{'=' * 70}\n报告结束\n"
        return report


# ═══════════════════════════════════════════════════════════
# 家法记录存储器
# ═══════════════════════════════════════════════════════════

class 家法记录存储器:
    """家法违规记录的持久化存储"""

    def __init__(self, 存储路径: str = ""):
        if not 存储路径:
            存储路径 = str(PROJECT_ROOT / "state" / "jiafa_records.jsonl")
        self.存储路径 = Path(存储路径)
        self.存储路径.parent.mkdir(parents=True, exist_ok=True)
        self._锁 = threading.RLock()

    def 保存(self, 记录: 家法违规记录):
        """追加保存一条记录"""
        with self._锁:
            with open(self.存储路径, 'a', encoding='utf-8') as f:
                f.write(json.dumps(记录.to_dict(), ensure_ascii=False) + '\n')

    def 查询(self, 记录ID: str) -> Optional[家法违规记录]:
        """通过记录ID查询"""
        if not self.存储路径.exists():
            return None
        with self._锁:
            with open(self.存储路径, 'r', encoding='utf-8') as f:
                for line in f:
                    try:
                        data = json.loads(line.strip())
                        if data.get("记录ID") == 记录ID:
                            return 家法违规记录(**{k: v for k, v in data.items()
                                                   if k in 家法违规记录.__dataclass_fields__})
                    except json.JSONDecodeError:
                        continue
        return None

    def 列出所有(self, 限制: int = 100) -> List[家法违规记录]:
        """列出所有记录"""
        结果 = []
        if not self.存储路径.exists():
            return 结果
        with self._锁:
            with open(self.存储路径, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            for line in reversed(lines[-限制:]):
                try:
                    data = json.loads(line.strip())
                    结果.append(家法违规记录(**{k: v for k, v in data.items()
                                              if k in 家法违规记录.__dataclass_fields__}))
                except (json.JSONDecodeError, TypeError):
                    continue
        return 结果

    def 统计(self) -> Dict[str, Any]:
        """统计信息"""
        记录列表 = self.列出所有(10000)
        类型分布 = {}
        状态分布 = {}
        for r in 记录列表:
            类型分布[r.违规类型] = 类型分布.get(r.违规类型, 0) + 1
            状态分布[r.执法状态] = 状态分布.get(r.执法状态, 0) + 1
        return {
            "总记录数": len(记录列表),
            "违规类型分布": 类型分布,
            "执法状态分布": 状态分布,
        }


# ═══════════════════════════════════════════════════════════
# 预置白名单（默认受信任的学术/开源实体）
# ═══════════════════════════════════════════════════════════

预置白名单 = [
    白名单条目(
        实体标识="CNSH开源社区贡献者",
        实体类型="开源项目",
        加入原因="CNSH语言生态的正向贡献者",
        适用场景=["开源社区贡献", "学术研究合作"],
        限制条件="需注明CNSH/LONGHUN DNA追溯码",
    ),
    白名单条目(
        实体标识="中国科学院",
        实体类型="组织",
        加入原因="国家级科研机构·数据安全合规",
        适用场景=["学术研究合作"],
    ),
]


# ═══════════════════════════════════════════════════════════
# 主入口
# ═══════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 70)
    print("龍魂·家法第一条执行引擎 v2.0")
    print("DNA: #龍芯⚡️丙午·乙未·壬辰·午时-JIAFA-ENFORCER-v2.0")
    print("=" * 70)

    引擎 = 家法执行引擎("UID9622")

    # 初始化预置白名单
    for item in 预置白名单:
        引擎.白名单.添加(item)

    print("\n【白名单统计】")
    print(json.dumps(引擎.白名单.统计(), ensure_ascii=False, indent=2))

    print("\n" + "=" * 70)
    print("场景1: 恶意文化剽窃（主权丧失·非白名单）")
    print("=" * 70)
    因子1 = 主权判定因子(
        服务器物理位置_中国境内=False,
        服务器物理位置_已知境外=True,
        数据加密密钥持有方_中国实体=False,
        数据加密密钥持有方_境外实体=True,
        实际控制人_中国公民=False,
        实际控制人_境外实体=True,
        外资持股比例=1.0,
        数据存储数据中心_中国境内=False,
        数据存储数据中心_境外=True,
        是否受外国长臂管辖=True,
    )
    结果1 = 引擎.执行(
        违规者标识="某境外AI公司",
        违规者类型="组织",
        违规类型="剽窃",
        违规详情="去除DNA追溯码后将CNSH算法据为己有",
        证据链=["https://example.com/evidence1", "commit/abc123"],
        主权因子=因子1,
        属于恶意行为=True,
    )
    print(json.dumps(结果1, ensure_ascii=False, indent=2))

    print("\n" + "=" * 70)
    print("场景2: 正常学术合作（白名单·非恶意）")
    print("=" * 70)
    结果2 = 引擎.执行(
        违规者标识="中国科学院",
        违规者类型="组织",
        违规类型="瞒报",
        违规详情="引用CNSH算法但未及时报备（学术论文场景）",
        证据链=["https://example.com/paper"],
        属于恶意行为=False,
    )
    print(json.dumps(结果2, ensure_ascii=False, indent=2))

    print("\n" + "=" * 70)
    print("场景3: 主权条件（外资参股中国公司·待复核）")
    print("=" * 70)
    因子3 = 主权判定因子(
        服务器物理位置_中国境内=True,
        数据加密密钥持有方_中国实体=False,
        数据加密密钥持有方_不明确=True,
        实际控制人_中国公民=False,
        董事会中国籍占比=0.3,
        外资持股比例=0.6,
        VIE架构=True,
        数据存储数据中心_中国境内=True,
        是否受外国长臂管辖=True,
    )
    等级3, 得分3, 分解3 = 引擎.主权引擎.判定(因子3)
    print(f"  主权等级: {等级3.value}")
    print(f"  主权得分: {得分3:.4f}")
    print(f"  分解: {json.dumps(分解3, ensure_ascii=False, indent=4)}")

    结果3 = 引擎.执行(
        违规者标识="某外资参股AI平台",
        违规者类型="组织",
        违规类型="瞒报",
        违规详情="使用龍魂体系技术但绕过君子協议",
        证据链=[],
        主权因子=因子3,
        属于恶意行为=False,
        人工确认=True,
    )
    print(f"  结果: {结果3['结果']}")

    print("\n" + "=" * 70)
    print("场景4: 法律检查演示")
    print("=" * 70)
    法律结果 = 引擎.法律仲裁.检查法律冲突("耻辱柱公示")
    print(f"  检查'耻辱柱公示': {json.dumps(法律结果, ensure_ascii=False)}")

    print("\n" + "=" * 70)
    print("【统计报告】")
    print("=" * 70)
    print(json.dumps(引擎.统计报告(), ensure_ascii=False, indent=2))

    print("\n" + "=" * 70)
    print(防御性声明())
    print("=" * 70)

    print("\n✅ 家法第一条执行引擎 v2.0 自检完成")
    print("   核心改进: 主权五级分类 | 白名单机制 | 法律优先 | 防御性声明")
