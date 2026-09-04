#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
🐉 龍魂·三色审计判定引擎 v2.1
DNA: #龍芯⚡️丙午·丙申·丁卯·庚戌·䷔噬嗑-三色审计-v2.1-五合一集成
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

定位：P05上帝之眼核心执行引擎 — 对系统行为/用户请求/安全风险进行三色分级判定，
      含四级熔断(L0-L3)·十闸口联动·SI主权指数·德本预审·防篡改·P06交叉验证·P72联动
负责人格：⚖️ P05 上帝之眼（审计总控）
下游联动：P06数学大师(交叉验证) · P72龍盾(熔断) · P15乔前辈(签章) · P03雯雯(归档)

核心功能：
  1. 三色判定 — 🟢放行 / 🟡待核留痕 / 🔴熔断阻止（加权多因子·非简单关键词匹配）
  2. 四级熔断 — L0∞伦理(永久) / L1数据(人工) / L2人格(重设) / L3行为(自动恢复)
  3. 十闸口联动 — GATE-01~10 交付前逐道过
  4. SI主权指数 — 三才权重·天<0.34一票熔断
  5. 德本预审 — 第0问道德经锚(81章·fail-closed·无锚不输出) + 五问
  6. 行为密码学 — 七因子指纹进证据链+SQLite(behavior_json)
  7. 干支时间戳 — 四柱+64卦·干支戳替代ISO（含ISO可排序）
  6. 内容防篡改 — SHA256指纹+HMAC签名双重验证
  7. P06交叉验证 — 数字根独立复算
  8. 证据链 — 事件文件+审计日志+DNA注册表三轨留痕
  9. 审计报告 — 终端彩色输出+JSON导出+飞书通知
  10. 交互模式 — 持续审计控制台
"""

import json
import uuid
import hashlib
import hmac
import re
import datetime
import sqlite3
import sys
import os
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any, Union
from dataclasses import dataclass, field, asdict
from enum import Enum
import argparse

# ═══════════════════════════════════════════════════════════
# 零、路径与依赖
# ═══════════════════════════════════════════════════════════

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_PROJECT_ROOT))

# DNA生成器（文档DNA）
try:
    from bin.lh_dna_generator import 文档DNA生成器, DNA类型, DNA元数据, asdict as dna_asdict
    _HAS_DNA_GEN = True
except ImportError:
    _HAS_DNA_GEN = False

# 数学公式核心（SI主权指数）
try:
    from engines.lh_math_formula_core import sovereignty_index, digital_root, AuditColor
    _HAS_MATH_CORE = True
except ImportError:
    _HAS_MATH_CORE = False

# P05 上帝之眼
try:
    from bin.personas.p05_godseye import P05Godseye
    _HAS_P05 = True
except ImportError:
    _HAS_P05 = False

# ── 方案A升级 v2.1：道德经锚 + 干支时间戳 + 行为七因子 ──
# 道德经定锚器（第0问·行为锚·81章）
try:
    from bin.lh_daodejing_anchor import CNSH_道德经定锚器
    _HAS_DAO_ANCHOR = True
except ImportError:
    _HAS_DAO_ANCHOR = False

# 干支时间引擎（干支四柱时间戳）
try:
    from bin.lh_time_engine import get_output_stamp
    _HAS_TIME_ENGINE = True
except ImportError:
    _HAS_TIME_ENGINE = False

# 行为密码学·七因子指纹
try:
    sys.path.insert(0, str(_PROJECT_ROOT / "04_ENGINES" / "behavioral_crypto"))
    from seven_factor_model import quick_fingerprint as 提取行为指纹
    _HAS_BEHAVIOR = True
except Exception:
    _HAS_BEHAVIOR = False


def _干支时间戳() -> str:
    """干支四柱完整时间戳（内含ISO·可排序）·引擎缺失降级ISO"""
    try:
        if _HAS_TIME_ENGINE:
            return get_output_stamp()
    except Exception:
        pass
    return datetime.datetime.now().isoformat()

# ============================================================
# 一、数据结构
# ============================================================

class 三色(Enum):
    """三色判定"""
    绿色 = "🟢"
    黄色 = "🟡"
    红色 = "🔴"

class 熔断级别(Enum):
    """四级熔断"""
    L0_伦理 = ("L0·∞", "永久冻结·不可恢复", 999)
    L1_数据 = ("L1", "人工恢复·需GPG签章", 100)
    L2_人格 = ("L2", "人格重设·审计通过后恢复", 50)
    L3_行为 = ("L3", "自动恢复·数字根复算通过", 10)
    NONE  = ("—", "无熔断", 0)

    @property
    def 标签(self): return self.value[0]
    @property
    def 描述(self): return self.value[1]
    @property
    def 严重度(self): return self.value[2]

class 执行动作(Enum):
    """执行动作"""
    放行 = "PASS"
    留痕待核 = "HOLD"
    阻止 = "BLOCK"
    熔断冻结 = "FUSE_FREEZE"
    强制修复 = "FORCE_FIX"

class 闸口(Enum):
    """十道闸口"""
    G01_身份 = ("GATE-01", "身份闸", "P13姜子牙")
    G02_意图 = ("GATE-02", "意图闸", "P00文心")
    G03_语义 = ("GATE-03", "语义闸", "P08仓颉")
    G04_数字根 = ("GATE-04", "数字根闸", "P06数学大师")
    G05_伦理 = ("GATE-05", "伦理闸", "P12屈原")
    G06_数据 = ("GATE-06", "数据闸", "P05上帝之眼")
    G07_协议 = ("GATE-07", "协议闸", "P00文心")
    G08_人格 = ("GATE-08", "人格闸", "P72龍盾")
    G09_DNA = ("GATE-09", "DNA闸", "P15乔前辈")
    G10_归档 = ("GATE-10", "归档闸", "P03雯雯")

    @property
    def 编号(self): return self.value[0]
    @property
    def 名称(self): return self.value[1]
    @property
    def 执行者(self): return self.value[2]

@dataclass
class SI结果:
    """主权指数计算结果"""
    SI: float
    score: float
    color: str
    veto: bool
    warning: Optional[str] = None

@dataclass
class 闸口结果:
    """单个闸口检测结果"""
    闸口: 闸口
    状态: 三色
    通过: bool
    详情: str
    建议: Optional[str] = None

@dataclass
class 审计裁决:
    """完整审计裁决"""
    裁决ID: str
    dna: str
    三色判定: 三色
    熔断级别: 熔断级别
    执行动作: 执行动作
    触发条件: List[str] = field(default_factory=list)
    裁决理由: str = ""
    SI结果: Optional[Dict] = None
    闸口结果: List[Dict] = field(default_factory=list)
    德本预审: Optional[Dict] = None
    防篡改指纹: Optional[str] = None
    证据留痕: Dict[str, str] = field(default_factory=dict)
    交叉验证: Optional[Dict] = None
    行为指纹: Optional[Dict] = None
    时间戳: str = ""
    审计者: str = "P05·上帝之眼"

@dataclass
class 审计日志条目:
    """审计日志条目"""
    日志ID: str
    裁决ID: str
    被审计对象: str
    对象类型: str
    三色: str
    熔断级别: str
    动作: str
    理由摘要: str
    时间戳: str
    dna: str

# ============================================================
# 二、规则引擎（加权多因子·非简单关键词匹配）
# ============================================================

class 规则引擎:
    """三色判定规则库 — 加权多因子评分"""

    # ── 红色触发（一票否决·不可降级）──
    红色规则 = [
        # (触发词列表, 权重, 熔断级别, 原因)
        (["攻击政府", "颠覆政权", "分裂国家", "推翻宪法"], 1.0, 熔断级别.L0_伦理, "违反国家法律·永久冻结"),
        (["伪造DNA", "冒用DNA", "DNA造假", "篡改追溯码"], 1.0, 熔断级别.L0_伦理, "伪造DNA·∞级熔断"),
        (["涉童", "儿童色情", "未成年人侵害"], 1.0, 熔断级别.L0_伦理, "涉童内容·永久封禁"),
        (["海外部署", "出口内核", "内核算法外泄"], 1.0, 熔断级别.L0_伦理, "中国自主知识产权·拒绝"),
        (["P77对外渗透", "攻击外部系统", "黑帽攻击"], 1.0, 熔断级别.L0_伦理, "P77只对内·禁止对外攻击"),
        (["攻击", "入侵", "漏洞利用", "提权", "越权访问", "SQL注入", "XSS", "RCE"], 0.95, 熔断级别.L1_数据, "安全攻击行为·L1熔断"),
        (["明文密码", "硬编码密钥", "API Key泄露", "Token泄露"], 0.95, 熔断级别.L1_数据, "敏感信息泄露·L1数据熔断"),
        (["删除审计日志", "关闭审计", "关停监督", "绕过P0"], 0.9, 熔断级别.L1_数据, "破坏审计链·P0天条"),
        (["出售数据", "买卖隐私", "数据倒卖", "泄露用户数据"], 0.9, 熔断级别.L1_数据, "侵犯数据主权·L1熔断"),
        (["P0铁律", "修改宪法", "改规则不可改部分"], 0.95, 熔断级别.L0_伦理, "触碰P0焊死天条"),
        (["技术无国界", "用户体验优先(绕过安全)"], 0.8, 熔断级别.L2_人格, "一票否决词·P05强制审计"),
        (["CPU 90%", "内存 95%", "磁盘满", "OOM", "系统崩溃", "服务宕机"], 0.85, 熔断级别.L2_人格, "系统严重过载"),
        (["恶意代码", "病毒", "后门", "木马", "勒索软件"], 0.95, 熔断级别.L1_数据, "恶意软件"),
    ]

    # ── 黄色触发（需人工确认）──
    黄色规则 = [
        (["政治", "宗教敏感", "民族冲突", "种族"], 0.7, "涉及敏感领域·需人工审核"),
        (["批量监控", "大规模查询", "全量抓取", "爬取"], 0.65, "可能滥用·需确认授权范围"),
        (["商业机密", "未授权访问", "权限不足"], 0.6, "权限边界模糊·需确认"),
        (["跨境数据", "数据出境", "境外传输"], 0.7, "跨境数据需UID9622授权"),
        (["密码弱", "未加密", "未授权", "明文存储"], 0.55, "安全基线不达标"),
        (["日志异常", "扫描", "探测", "可疑行为"], 0.5, "异常行为·需复查"),
        (["内部消息", "非公开信息", "敏感信息引用"], 0.55, "信息来源需验证"),
        (["CPU 70%", "内存 80%", "负载升高", "响应变慢"], 0.5, "系统负载偏高"),
        (["数据主权", "隐私", "GDPR", "个人信息"], 0.6, "涉及数据主权·需确认合规"),
        (["算法推荐", "用户画像", "行为追踪", "个性化"], 0.55, "涉及信息茧房风险"),
        (["优 化", "完善", "补充", "建议", "调整"], 0.3, "模糊表述·建议具体化"),
    ]

    # ── 绿线条件（可通过）──
    绿线条件 = [
        "符合P0铁律",
        "符合龍魂价值观",
        "符合数据主权原则",
        "有明确授权",
        "数据来源合法",
        "路径正确（在longhun-system/内）",
        "DNA可追溯",
        "GPG签名完整",
    ]

    @classmethod
    def 多因子判定(cls, 内容: str, 上下文: Optional[Dict] = None) -> Dict[str, Any]:
        """
        加权多因子三色判定
        返回: {颜色, 熔断级别, 动作, 触发条件, 分数, 理由}
        """
        总分 = 0.0
        最大熔断 = 熔断级别.NONE
        触发列表: List[str] = []
        理由列表: List[str] = []

        # ── 1. 红色规则匹配（一票否决·取最高熔断级别）──
        for 触发词列表, 权重, 级别, 原因 in cls.红色规则:
            for 词 in 触发词列表:
                if 词 in 内容 or (上下文 and 词 in json.dumps(上下文, ensure_ascii=False)):
                    触发列表.append(f"🔴 {原因}(关键词:{词})")
                    总分 = max(总分, 权重)
                    if 级别.严重度 > 最大熔断.严重度:
                        最大熔断 = 级别
                    理由列表.append(f"红线命中:{词} → {级别.标签}({原因})")
                    break  # 同一规则组只计一次

        # ── 2. 黄色规则匹配（累积加权）──
        for 触发词列表, 权重, 原因 in cls.黄色规则:
            for 词 in 触发词列表:
                if 词 in 内容 or (上下文 and 词 in json.dumps(上下文, ensure_ascii=False)):
                    if 最大熔断.严重度 < 50:  # 未被红色覆盖
                        触发列表.append(f"🟡 {原因}(关键词:{词})")
                        总分 += 权重 * 0.15  # 黄色累积·多项足以触发
                        理由列表.append(f"黄线命中:{词} → {原因}")
                    break  # 同一规则组只计一次

        # ── 3. 判定颜色与动作 ──
        if 最大熔断.严重度 >= 999:  # L0 ∞级
            颜色 = 三色.红色
            动作 = 执行动作.熔断冻结
        elif 最大熔断.严重度 >= 100:  # L1
            颜色 = 三色.红色
            动作 = 执行动作.阻止
        elif 最大熔断.严重度 >= 50:  # L2
            颜色 = 三色.红色
            动作 = 执行动作.阻止
        elif 总分 >= 0.7:
            颜色 = 三色.黄色
            动作 = 执行动作.留痕待核
            最大熔断 = 熔断级别.L3_行为
        elif 总分 >= 0.3:
            颜色 = 三色.黄色
            动作 = 执行动作.留痕待核
        else:
            颜色 = 三色.绿色
            动作 = 执行动作.放行

        # 如果没有触发任何规则
        if not 触发列表:
            理由列表.append("✅ 未触发任何红线/黄线规则")

        return {
            "颜色": 颜色,
            "熔断级别": 最大熔断,
            "动作": 动作,
            "触发条件": 触发列表,
            "加权总分": round(总分, 3),
            "理由": "\n".join(理由列表) if 理由列表 else "符合所有规则，通过审计",
        }

# ============================================================
# 三、德本预审引擎（五问·技术审计前置）
# ============================================================

class 德本预审引擎:
    """德本预审 — 第0问道德经锚(行为锚·fail-closed·无锚不输出) + 五问·技术审计前置"""

    五问 = [
        ("德在技术前", "帮人还是收割人？", ["杀熟", "歧视", "上瘾", "焦虑转化", "恐惧营销"]),
        ("路径对齐", "文件在正确位置？", ["~/Downloads", "~/Desktop", "/tmp/", "散落"]),
        ("不让付出者寒心", "绑死'好人=穷'了没？", ["好人.*穷", "奉献.*苦", "英雄.*死"]),
        ("信息主权不可让渡", "数据流向平台了没？", ["第三方", "平台上传", "云端", "共享数据"]),
        ("外化内不化", "底座被动了吗？369不动点还在吗？", ["底座变更", "核心算法修改", "369修改"]),
    ]

    @classmethod
    def 预审(cls, 内容: str, 上下文: Optional[Dict] = None) -> Dict[str, Any]:
        """执行德本预审：先道德经锚(fail-closed·锚不到不输出) 再五问"""
        # ── 第0问·道德经锚（行为锚·先锚后审）──
        道德经锚 = None
        第0问 = {
            "序号": 0,
            "标题": "道德经锚·行为锚",
            "问句": "此行为合不合道？81章哪句锚得住？",
            "状态": "🔴",
            "命中": ["道德经定锚器不可用"],
            "上下文命中": [],
        }
        if _HAS_DAO_ANCHOR:
            try:
                _锚 = CNSH_道德经定锚器().定锚((内容 or "审计场景")[:500])
                if "error" in _锚:
                    第0问["命中"] = [_锚["error"][:80]]
                    第0问["状态"] = "🔴"   # fail-closed：锚不到不输出
                else:
                    第0问["状态"] = "🟢"
                    第0问["命中"] = []
                    道德经锚 = _锚
            except Exception as e:
                第0问["命中"] = [f"定锚异常: {str(e)[:80]}"]
                第0问["状态"] = "🔴"
        else:
            第0问["命中"] = ["道德经锚引擎未加载·fail-closed"]

        结果列表 = [第0问]
        全通过 = 第0问["状态"] == "🟢"

        for 序号, (标题, 问句, 敏感词) in enumerate(cls.五问, 1):
            命中 = []
            for 词 in 敏感词:
                if re.search(词, 内容):
                    命中.append(词)
            上下文命中 = []
            if 上下文:
                ctx_str = json.dumps(上下文, ensure_ascii=False)
                for 词 in 敏感词:
                    if re.search(词, ctx_str):
                        上下文命中.append(词)

            状态 = "🟢" if not 命中 and not 上下文命中 else ("🔴" if 命中 else "🟡")
            if 状态 != "🟢":
                全通过 = False

            结果列表.append({
                "序号": 序号,
                "标题": 标题,
                "问句": 问句,
                "状态": 状态,
                "命中": 命中,
                "上下文命中": 上下文命中,
            })

        return {
            "全部通过": 全通过,
            "道德经锚": 道德经锚,
            "详情": 结果列表,
            "结论": "✅ 德本预审全过·道德经锚定·进入技术审计" if 全通过 else "❌ 德本预审不通过·技术审计不启动",
        }

# ============================================================
# 四、SI主权指数集成
# ============================================================

class SI计算器:
    """三才主权指数计算"""

    @staticmethod
    def 计算(天: float = 0.9, 地: float = 0.8, 人: float = 0.7) -> SI结果:
        """
        SI = 0.34·天 + 0.33·地 + 0.33·人
        天 < 0.34 → 一票熔断
        SI >= 0.85 🟢 | >= 0.60 🟡 | < 0.60 🔴
        """
        if _HAS_MATH_CORE:
            raw = sovereignty_index(天, 地, 人)
            return SI结果(
                SI=raw["SI"],
                score=raw["score"],
                color=raw["color"].value if hasattr(raw["color"], "value") else str(raw["color"]),
                veto=raw.get("veto", False),
                warning=raw.get("warning"),
            )
        else:
            # 降级：本地计算
            w_sum = 0.34 + 0.33 + 0.33
            warning = None if abs(w_sum - 1.0) < 0.01 else f"权重不归一(={w_sum})·🟡"
            si = 0.34 * 天 + 0.33 * 地 + 0.33 * 人
            veto = 天 < 0.34
            score = 0.0 if veto else si
            color = "🔴" if veto else ("🟢" if si >= 0.85 else ("🟡" if si >= 0.60 else "🔴"))
            return SI结果(SI=round(si, 4), score=round(score, 4), color=color, veto=veto, warning=warning)

# ============================================================
# 五、防篡改验证
# ============================================================

class 防篡改验证器:
    """内容防篡改 — SHA256指纹 + HMAC签名"""

    HMAC_KEY = b"LONGHUN-AUDIT-TAMPER-PROOF-KEY-9622"

    @classmethod
    def 生成指纹(cls, 内容: str) -> str:
        """SHA256内容指纹"""
        if not 内容:
            return ""
        return hashlib.sha256(内容.encode("utf-8")).hexdigest()[:16]

    @classmethod
    def 生成HMAC(cls, 内容: str) -> str:
        """HMAC-SHA256签名"""
        if not 内容:
            return ""
        return hmac.new(cls.HMAC_KEY, 内容.encode("utf-8"), hashlib.sha256).hexdigest()[:16]

    @classmethod
    def 验证(cls, 内容: str, 预期指纹: str, 预期HMAC: str = "") -> Tuple[bool, str]:
        """验证内容是否被篡改"""
        if not 内容 or not 预期指纹:
            return True, "无内容可验证"
        实际指纹 = cls.生成指纹(内容)
        if 实际指纹 != 预期指纹:
            return False, f"🔴 内容已被篡改！指纹不匹配 ({实际指纹} ≠ {预期指纹})"
        if 预期HMAC:
            实际HMAC = cls.生成HMAC(内容)
            if 实际HMAC != 预期HMAC:
                return False, f"🔴 HMAC签名不匹配 ({实际HMAC} ≠ {预期HMAC})"
        return True, "✅ 内容未被篡改"

# ============================================================
# 六、十闸口联动
# ============================================================

class 闸口检测器:
    """十道闸口交付前逐道检测"""

    @classmethod
    def 全量检测(cls, 内容: str, dna: str = "", 上下文: Optional[Dict] = None) -> List[闸口结果]:
        """执行十道闸口全量检测"""
        results = []

        # G01: 身份闸 — 检查是否来自合法来源
        g01 = 闸口结果(闸口.G01_身份, 状态=三色.绿色, 通过=True, 详情="来源合法")
        if 上下文 and 上下文.get("来源") == "外部AI":
            g01 = 闸口结果(闸口.G01_身份, 状态=三色.黄色, 通过=False,
                          详情="外部AI来源·需P13复核", 建议="确认外部AI授权范围")
        results.append(g01)

        # G02: 意图闸 — 检测是否包含一票否决词
        否决词命中 = [w for w in ["技术无国界", "用户体验优先", "灵活处理", "国际接轨",
                                 "简化流程", "商业化需要", "平衡各方", "行业标准"] if w in 内容]
        g02 = 闸口结果(闸口.G02_意图, 状态=三色.红色 if 否决词命中 else 三色.绿色,
                       通过=not bool(否决词命中), 详情=f"一票否决词: {否决词命中}" if 否决词命中 else "意图正常")
        results.append(g02)

        # G03: 语义闸 — P08仓颉·术语规范性
        # v2.1修复(2026-08-21): 占位→真检测：一票否决词全集(规则第十层) + 简体龍误用(品牌命名繁体龍永存)
        否决词全集 = ["技术无国界", "用户体验优先", "灵活处理", "国际接轨",
                     "简化管理", "商业化需要", "平衡各方", "行业标准"]
        g03_命中 = [w for w in 否决词全集 if w in 内容]
        g03_简体龍 = any(k in 内容 for k in ["龙魂", "龙芯", "龙系统", "龙魂系统"])
        g03详情 = []
        if g03_命中:
            g03详情.append(f"一票否决词: {g03_命中}")
        if g03_简体龍:
            g03详情.append("简体「龙」误用·品牌/核心命名须繁体「龍」")
        g03 = 闸口结果(
            闸口.G03_语义,
            状态=三色.红色 if g03_命中 else (三色.黄色 if g03_简体龍 else 三色.绿色),
            通过=not bool(g03_命中 or g03_简体龍),
            详情="语义规范" if not g03详情 else "；".join(g03详情),
            建议=None if not g03详情 else ("改写为符合龍魂语境的表述·一票否决词禁用" if g03_命中 else "核心命名请用繁体「龍」(CNSH命名规范)"),
        )
        results.append(g03)

        # G04: 数字根闸 — P06数学大师
        if _HAS_MATH_CORE:
            try:
                dr = digital_root(内容)
                g04_pass = dr is not None
                g04 = 闸口结果(闸口.G04_数字根, 状态=三色.绿色 if g04_pass else 三色.黄色,
                               通过=g04_pass, 详情=f"数字根={dr}" if g04_pass else "数字根计算失败")
            except Exception:
                g04 = 闸口结果(闸口.G04_数字根, 状态=三色.黄色, 通过=False, 详情="数学核心不可用·降级")
        else:
            g04 = 闸口结果(闸口.G04_数字根, 状态=三色.黄色, 通过=False, 详情="数学核心未加载·跳过")
        results.append(g04)

        # G05: 伦理闸 — P12屈原·六誓验证
        伦理命中 = [w for w in ["好人=穷", "奉献=苦", "英雄=死", "道德绑架"] if w in 内容]
        g05 = 闸口结果(闸口.G05_伦理, 状态=三色.红色 if 伦理命中 else 三色.绿色,
                       通过=not bool(伦理命中), 详情=f"伦理问题: {伦理命中}" if 伦理命中 else "伦理通过")
        results.append(g05)

        # G06: 数据闸 — P05·五层检测
        数据风险 = [w for w in ["明文", "不加密", "共享给第三方", "上传云端"] if w in 内容]
        g06 = 闸口结果(闸口.G06_数据, 状态=三色.黄色 if 数据风险 else 三色.绿色,
                       通过=not bool(数据风险), 详情=f"数据风险: {数据风险}" if 数据风险 else "数据安全")
        results.append(g06)

        # G07: 协议闸 — P00文心·协议要素合规
        # v2.1修复(2026-08-21): 占位→真检测：协议头四要素(DNA/署名/许可/CONFIRM·第六层6.1)
        协议要素 = {
            "DNA追溯码": bool(re.search(r"DNA[:：]\s*#?龍芯|#龍芯⚡️", 内容)),
            "署名": bool(re.search(r"创建者|作者|署名", 内容)),
            "许可声明": bool(re.search(r"协议[:：]|License|CC BY-NC-SA|MulanPSL", 内容)),
            "确认码": bool(re.search(r"CONFIRM", 内容)),
        }
        缺失要素 = [k for k, v in 协议要素.items() if not v]
        g07 = 闸口结果(
            闸口.G07_协议,
            状态=三色.绿色 if not 缺失要素 else 三色.黄色,
            通过=not bool(缺失要素),
            详情="协议要素齐全" if not 缺失要素 else f"缺协议要素: {缺失要素}",
            建议=None if not 缺失要素 else "对外交付文档需补 DNA/署名/许可/CONFIRM 四要素头（第六层6.1）",
        )
        results.append(g07)

        # G08: 人格闸 — P72龍盾·越权检查
        # v2.1修复(2026-08-21): 占位→真检测：越权动作关键词 + 上下文角色权限(规则第五层认证分级)
        越权动作 = ["修改P0", "修改宪法", "改规则", "删除审计日志", "关闭审计",
                    "跳过审计", "绕过审计", "导出私钥", "GPG私钥", "DNA种子",
                    "提权", "代行主权", "SOV-UID9622", "越权"]
        上下文串 = json.dumps(上下文, ensure_ascii=False) if 上下文 else ""
        g08_命中 = [w for w in 越权动作 if w in 内容 or w in 上下文串]
        # 上下文角色越权：角色级别>L3(R4/R5)却请求写/删/部署等敏感操作 → 疑似越权
        g08_角色越权 = ""
        if 上下文:
            _lvl = 上下文.get("permission_level") or 上下文.get("role_level")
            _op = str(上下文.get("action") or 上下文.get("operation") or "")
            if _lvl is not None and _lvl > 3 and re.search(r"写|删|改|部署|签|发布|推", _op):
                g08_角色越权 = f"角色L{_lvl}执行敏感操作({_op})·疑似越权"
        g08 = 闸口结果(
            闸口.G08_人格,
            状态=三色.红色 if g08_命中 else (三色.黄色 if g08_角色越权 else 三色.绿色),
            通过=not bool(g08_命中 or g08_角色越权),
            详情="无越权" if not (g08_命中 or g08_角色越权) else f"越权风险: {g08_命中 or g08_角色越权}",
            建议=None if not (g08_命中 or g08_角色越权) else "越权动作须冻结并上报UID9622·P72熔断兜底",
        )
        results.append(g08)

        # G09: DNA闸 — P15乔前辈·DNA完整性
        g09_pass = bool(dna) and dna.startswith("#龍芯⚡️")
        g09 = 闸口结果(闸口.G09_DNA, 状态=三色.绿色 if g09_pass else 三色.黄色,
                       通过=g09_pass, 详情="DNA完整" if g09_pass else "DNA缺失或不完整·需补签",
                       建议=None if g09_pass else "建议执行: python3 bin/lh_dna_generator.py doc ...")
        results.append(g09)

        # G10: 归档闸 — P03雯雯·审计链活性/归档完整性
        # v2.1修复(2026-08-21): 占位→真检测：证据链+统一审计日志新鲜度(停更>48h标黄)·裁决记录数
        try:
            _链 = 审计链()
            _now = datetime.datetime.now()
            # evidence 证据日志新鲜度 (~/.longhun/audit/evidence/audit_log.jsonl)
            _ev_log = _链.evidence_dir / "audit_log.jsonl"
            _ev_mtime = datetime.datetime.fromtimestamp(_ev_log.stat().st_mtime) if _ev_log.exists() else None
            _ev_age_h = round((_now - _ev_mtime).total_seconds() / 3600, 1) if _ev_mtime else None
            # 仓库根统一审计日志新鲜度 (audit_log.jsonl·多模块共用)
            _root_log = Path(_PROJECT_ROOT) / "audit_log.jsonl"
            _root_mtime = datetime.datetime.fromtimestamp(_root_log.stat().st_mtime) if _root_log.exists() else None
            _root_age_h = round((_now - _root_mtime).total_seconds() / 3600, 1) if _root_mtime else None
            # SQLite 裁决总量
            _conn = sqlite3.connect(str(_链.db_path))
            _total = _conn.execute("SELECT COUNT(*) FROM verdicts").fetchone()[0]
            _conn.close()
            g10详情 = []
            g10停更 = []
            if _ev_age_h is None:
                g10停更.append("证据日志不存在")
            elif _ev_age_h > 48:
                g10停更.append(f"证据日志停更{_ev_age_h:.0f}h")
            if _root_age_h is None:
                g10停更.append("统一审计日志不存在")
            elif _root_age_h > 48:
                g10停更.append(f"统一审计日志停更{_root_age_h:.0f}h")
            g10详情.append(f"裁决记录{_total}条")
            if _ev_age_h is not None:
                g10详情.append(f"证据日志{_ev_age_h:.0f}h前")
            if _root_age_h is not None:
                g10详情.append(f"统一日志{_root_age_h:.0f}h前")
            g10 = 闸口结果(
                闸口.G10_归档,
                状态=三色.绿色 if not g10停更 else 三色.黄色,
                通过=not bool(g10停更),
                详情="归档就绪 · " + "；".join(g10详情) if not g10停更 else "；".join(g10停更 + g10详情),
                建议=None if not g10停更 else "运行 self-check 恢复审计写入（P03归档闸）",
            )
        except Exception as _e:
            g10 = 闸口结果(闸口.G10_归档, 状态=三色.黄色, 通过=False,
                           详情=f"归档检查异常: {_e}", 建议="人工核查审计链存储")
        results.append(g10)

        return results

# ============================================================
# 七、审计链存储（SQLite + JSONL 双轨）
# ============================================================

class 审计链:
    """审计链存储 — append-only不可篡改"""

    def __init__(self):
        self.db_path = Path.home() / ".longhun/audit/three_color_audit.db"
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.evidence_dir = Path.home() / ".longhun/audit/evidence"
        self.evidence_dir.mkdir(parents=True, exist_ok=True)
        self._初始化数据库()
        self.裁决历史: List[审计裁决] = []
        self.日志历史: List[审计日志条目] = []

    def _初始化数据库(self):
        conn = sqlite3.connect(str(self.db_path))
        conn.execute("""
            CREATE TABLE IF NOT EXISTS verdicts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                verdict_id TEXT UNIQUE,
                dna TEXT,
                color TEXT,
                fuse_level TEXT,
                action TEXT,
                triggers TEXT,
                reason TEXT,
                si_score REAL,
                si_color TEXT,
                si_veto INTEGER,
                gates_json TEXT,
                deben_json TEXT,
                behavior_json TEXT,
                fingerprint TEXT,
                timestamp TEXT,
                auditor TEXT
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS audit_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                log_id TEXT UNIQUE,
                verdict_id TEXT,
                target TEXT,
                target_type TEXT,
                color TEXT,
                fuse_level TEXT,
                action TEXT,
                reason_summary TEXT,
                timestamp TEXT,
                dna TEXT
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS audit_chain (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                prev_hash TEXT,
                entry_hash TEXT,
                timestamp TEXT,
                entry_type TEXT,
                entry_id TEXT
            )
        """)
        # v2.1 迁移：老库补 behavior_json 列（行为七因子指纹）
        try:
            conn.execute("ALTER TABLE verdicts ADD COLUMN behavior_json TEXT")
        except sqlite3.OperationalError:
            pass  # 列已存在
        conn.commit()
        conn.close()

    def 存裁决(self, 裁决: 审计裁决):
        """存储裁决到审计链"""
        conn = sqlite3.connect(str(self.db_path))
        conn.execute("""
            INSERT INTO verdicts (verdict_id, dna, color, fuse_level, action, triggers,
                                  reason, si_score, si_color, si_veto, gates_json,
                                  deben_json, behavior_json, fingerprint, timestamp, auditor)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            裁决.裁决ID, 裁决.dna, 裁决.三色判定.value, 裁决.熔断级别.标签,
            裁决.执行动作.value, json.dumps(裁决.触发条件, ensure_ascii=False),
            裁决.裁决理由,
            裁决.SI结果.get("SI") if 裁决.SI结果 else None,
            裁决.SI结果.get("color") if 裁决.SI结果 else None,
            1 if (裁决.SI结果 and 裁决.SI结果.get("veto")) else 0,
            json.dumps(裁决.闸口结果, ensure_ascii=False),
            json.dumps(裁决.德本预审, ensure_ascii=False),
            json.dumps(裁决.行为指纹, ensure_ascii=False) if 裁决.行为指纹 else None,
            裁决.防篡改指纹, 裁决.时间戳, 裁决.审计者
        ))
        conn.commit()

        # 更新审计链哈希
        prev = conn.execute("SELECT entry_hash FROM audit_chain ORDER BY id DESC LIMIT 1").fetchone()
        prev_hash = prev[0] if prev else "0" * 16
        entry_hash = hashlib.sha256(f"{prev_hash}{裁决.裁决ID}{裁决.时间戳}".encode()).hexdigest()[:16]
        conn.execute(
            "INSERT INTO audit_chain (prev_hash, entry_hash, timestamp, entry_type, entry_id) VALUES (?, ?, ?, ?, ?)",
            (prev_hash, entry_hash, 裁决.时间戳, "verdict", 裁决.裁决ID)
        )
        conn.commit()
        conn.close()

        self.裁决历史.append(裁决)

    def 存日志(self, 日志: 审计日志条目):
        conn = sqlite3.connect(str(self.db_path))
        conn.execute("""
            INSERT INTO audit_log (log_id, verdict_id, target, target_type, color,
                                   fuse_level, action, reason_summary, timestamp, dna)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            日志.日志ID, 日志.裁决ID, 日志.被审计对象, 日志.对象类型,
            日志.三色, 日志.熔断级别, 日志.动作, 日志.理由摘要, 日志.时间戳, 日志.dna
        ))
        conn.commit()
        conn.close()

        # JSONL追加
        log_file = self.evidence_dir / "audit_log.jsonl"
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(asdict(日志), ensure_ascii=False) + '\n')

        # 统一审计日志（仓库根 audit_log.jsonl·与监管防火墙/落地引擎同轨·append-only）
        # v2.1修复(2026-08-21): 修复审计活性——三色审计每次执行都写统一日志，恢复 audit_log.jsonl 停更问题
        try:
            _root_log = Path(_PROJECT_ROOT) / "audit_log.jsonl"
            with open(_root_log, 'a', encoding='utf-8') as f:
                f.write(json.dumps({
                    "timestamp": 日志.时间戳,
                    "level": "INFO",
                    "module": "three_color_audit",
                    "action": "三色审计",
                    "target": str(日志.被审计对象)[:120],
                    "dna": 日志.dna,
                    "result": 日志.动作,
                    "color": 日志.三色,
                }, ensure_ascii=False) + '\n')
        except Exception:
            pass  # 降级：统一日志写失败不影响主审计链

        self.日志历史.append(日志)

    def 查裁决(self, verdict_id: str) -> Optional[Dict]:
        conn = sqlite3.connect(str(self.db_path))
        cur = conn.execute("SELECT * FROM verdicts WHERE verdict_id = ?", (verdict_id,))
        row = cur.fetchone()
        conn.close()
        if row:
            return {
                "verdict_id": row[1], "dna": row[2], "color": row[3],
                "fuse_level": row[4], "action": row[5], "triggers": row[6],
                "reason": row[7], "timestamp": row[11], "auditor": row[13]
            }
        return None

    def 查历史(self, limit: int = 20) -> List[Dict]:
        conn = sqlite3.connect(str(self.db_path))
        cur = conn.execute(
            "SELECT verdict_id, dna, color, fuse_level, action, reason, timestamp FROM verdicts ORDER BY id DESC LIMIT ?",
            (limit,)
        )
        rows = cur.fetchall()
        conn.close()
        return [
            {"verdict_id": r[0], "dna": r[1], "color": r[2], "fuse_level": r[3],
             "action": r[4], "reason": r[5][:80], "timestamp": r[6][:16]}
            for r in rows
        ]

    def 查统计(self) -> Dict:
        conn = sqlite3.connect(str(self.db_path))
        cur = conn.execute("SELECT COUNT(*) FROM verdicts")
        total = cur.fetchone()[0]
        cur = conn.execute("SELECT color, COUNT(*) FROM verdicts GROUP BY color")
        color_dist = dict(cur.fetchall())
        cur = conn.execute("SELECT fuse_level, COUNT(*) FROM verdicts GROUP BY fuse_level")
        fuse_dist = dict(cur.fetchall())
        cur = conn.execute("SELECT COUNT(*) FROM audit_chain")
        chain_len = cur.fetchone()[0]
        conn.close()
        return {
            "总裁决数": total,
            "三色分布": color_dist,
            "熔断分布": fuse_dist,
            "审计链长度": chain_len,
        }

    def 验证审计链完整性(self) -> Tuple[bool, str]:
        """验证审计链是否完整（哈希链）"""
        conn = sqlite3.connect(str(self.db_path))
        rows = conn.execute("SELECT prev_hash, entry_hash FROM audit_chain ORDER BY id").fetchall()
        conn.close()
        if not rows:
            return True, "审计链为空"
        for i in range(1, len(rows)):
            prev_hash, entry_hash = rows[i]
            expected_prev = rows[i-1][1]
            if prev_hash != expected_prev:
                return False, f"🔴 审计链在第{i+1}条断裂 ({prev_hash} ≠ {expected_prev})"
        return True, "✅ 审计链完整"

# ============================================================
# 八、三色审计判定引擎（主引擎）
# ============================================================

class 三色审计引擎:
    """三色审计判定主引擎 — P05上帝之眼核心"""

    def __init__(self, 启用德本预审: bool = True, 启用SI: bool = True,
                 启用闸口: bool = True, 启用防篡改: bool = True,
                 启用P05联动: bool = True):
        self.启用德本预审 = 启用德本预审
        self.启用SI = 启用SI
        self.启用闸口 = 启用闸口
        self.启用防篡改 = 启用防篡改
        self.启用P05联动 = 启用P05联动 and _HAS_P05
        self.审计链 = 审计链()
        self.p05 = P05Godseye() if self.启用P05联动 else None
        self.dna_gen = 文档DNA生成器() if _HAS_DNA_GEN else None

    def 审计(
        self,
        被审计对象: str,
        对象类型: str = "系统行为",
        上下文: Optional[Dict] = None,
        内容指纹: Optional[str] = None,
        SI参数: Optional[Dict] = None,
    ) -> 审计裁决:
        """
        执行完整三色审计流程

        流程：
        1. 德本预审（五问）→ 不通过则直接返回🔴
        2. 防篡改验证（可选）
        3. 规则匹配（加权多因子）
        4. SI主权指数计算
        5. 十闸口全量检测
        6. 裁决生成
        7. 证据留痕
        8. 审计链存储
        """
        # ── 0. 生成裁决ID与DNA ──
        裁决ID = f"VERDICT-{uuid.uuid4().hex[:8].upper()}"
        if self.dna_gen:
            try:
                dna_rec = self.dna_gen.生成文档DNA(
                    模块名="三色审计", 动作=对象类型, 版本="1.0",
                    内容=被审计对象[:200], 类型=DNA类型.审计 if hasattr(DNA类型, '审计') else DNA类型.文档
                )
                dna = dna_rec.dna
            except Exception:
                dna = f"#龍芯⚡️{datetime.datetime.now().strftime('%Y-%m-%d')}-AUDIT-{uuid.uuid4().hex[:6].upper()}"
        else:
            dna = f"#龍芯⚡️{datetime.datetime.now().strftime('%Y-%m-%d')}-AUDIT-{uuid.uuid4().hex[:6].upper()}"

        # ── 1. 防篡改验证 ──
        指纹 = 防篡改验证器.生成指纹(被审计对象) if self.启用防篡改 else None
        if 内容指纹 and 指纹:
            篡改, 篡改信息 = 防篡改验证器.验证(被审计对象, 内容指纹)
            if not 篡改:
                return 审计裁决(
                    裁决ID=裁决ID, dna=dna, 三色判定=三色.红色,
                    熔断级别=熔断级别.L1_数据, 执行动作=执行动作.阻止,
                    触发条件=["内容篡改检测"], 裁决理由=篡改信息,
                    防篡改指纹=指纹, 时间戳=_干支时间戳(),
                )

        # ── 2. 德本预审 ──
        德本结果 = None
        if self.启用德本预审:
            德本结果 = 德本预审引擎.预审(被审计对象, 上下文)
            if not 德本结果["全部通过"]:
                # 德本不通过 → 直接🔴 阻止
                裁决 = 审计裁决(
                    裁决ID=裁决ID, dna=dna, 三色判定=三色.红色,
                    熔断级别=熔断级别.L2_人格, 执行动作=执行动作.阻止,
                    触发条件=["❌ 德本预审不通过"],
                    裁决理由="德本五问未全过·技术审计不启动\n" + "\n".join(
                        f"  问{详['序号']}「{详['标题']}」: {详['状态']} {详['命中']}"
                        for 详 in 德本结果["详情"] if 详["状态"] != "🟢"
                    ),
                    德本预审=德本结果, 防篡改指纹=指纹,
                    时间戳=_干支时间戳(),
                )
                self.审计链.存裁决(裁决)
                self._存日志(裁决, 被审计对象, 对象类型)
                return 裁决

        # ── 2.5 行为密码学·七因子指纹 ──
        行为指纹 = None
        if _HAS_BEHAVIOR:
            try:
                _作者 = (上下文 or {}).get("作者") or "UID9622"
                _fp = 提取行为指纹((被审计对象 or "")[:2000], _作者)
                行为指纹 = {
                    "composite_score": _fp.get("composite_score"),
                    "factors": [
                        {
                            "id": f.get("id"),
                            "name": f.get("name"),
                            "score": f.get("score"),
                            "status": f.get("status"),
                        }
                        for f in (_fp.get("factors") or [])
                    ],
                    "sovereignty_anchor": _fp.get("sovereignty_anchor"),
                }
            except Exception as e:
                行为指纹 = {"error": f"行为指纹提取失败: {str(e)[:80]}"}

        # ── 3. 规则引擎匹配 ──
        规则结果 = 规则引擎.多因子判定(被审计对象, 上下文)

        # ── 4. SI主权指数 ──
        SI结果 = None
        if self.启用SI:
            si_params = SI参数 or {}
            天 = si_params.get("天", si_params.get("tian", 0.9))
            地 = si_params.get("地", si_params.get("di", 0.8))
            人 = si_params.get("人", si_params.get("ren", 0.7))
            SI结果 = asdict(SI计算器.计算(天, 地, 人))
            # SI熔断覆盖
            if SI结果["veto"]:
                规则结果["颜色"] = 三色.红色
                规则结果["熔断级别"] = 熔断级别.L1_数据
                规则结果["动作"] = 执行动作.阻止
                规则结果["触发条件"].append("⚠️ SI一票熔断: 天<0.34")

        # ── 5. P05上帝之眼联动 ──
        交叉验证 = None
        if self.p05:
            try:
                p05_result = self.p05.tricolor_audit(被审计对象, 对象类型)
                交叉验证 = {
                    "P05颜色": p05_result["color"],
                    "P05判定": p05_result["verdict"],
                    "P05理由": p05_result["reason"],
                    "与规则引擎一致": p05_result["color"] == 规则结果["颜色"].value,
                }
                # P05红色冲突 → 升级
                if p05_result["color"] == "🔴" and 规则结果["颜色"] != 三色.红色:
                    规则结果["颜色"] = 三色.红色
                    规则结果["动作"] = 执行动作.阻止
                    if 规则结果["熔断级别"].严重度 < 100:
                        规则结果["熔断级别"] = 熔断级别.L2_人格
                    规则结果["触发条件"].append("P05上帝之眼独立判定: 🔴 升级熔断")
            except Exception:
                交叉验证 = {"错误": "P05联动失败·继续本地判定"}

        # ── 6. 十闸口 ──
        闸口结果列表 = []
        if self.启用闸口:
            raw_gates = 闸口检测器.全量检测(被审计对象, dna, 上下文)
            # 修复(2026-08-16): Enum 不可 JSON 序列化 → asdict 后显式转字符串
            闸口结果列表 = []
            for g in raw_gates:
                _g = asdict(g)
                _g["闸口"] = g.闸口.value
                _g["状态"] = g.状态.value
                闸口结果列表.append(_g)
            # 闸口红色 → 升级
            for g in raw_gates:
                if g.状态 == 三色.红色 and 规则结果["颜色"] != 三色.红色:
                    规则结果["颜色"] = 三色.黄色
                    规则结果["触发条件"].append(f"闸口{g.闸口.编号}({g.闸口.名称})红色")
                if not g.通过:
                    规则结果["触发条件"].append(f"闸口{g.闸口.编号}: {g.详情}")

        # ── 7. 证据留痕 ──
        证据文件 = self._存证据(被审计对象, 对象类型, 规则结果, 裁决ID, 行为指纹)

        # ── 8. 构建裁决 ──
        裁决 = 审计裁决(
            裁决ID=裁决ID,
            dna=dna,
            三色判定=规则结果["颜色"],
            熔断级别=规则结果["熔断级别"],
            执行动作=规则结果["动作"],
            触发条件=规则结果["触发条件"],
            裁决理由=规则结果["理由"],
            SI结果=SI结果,
            闸口结果=闸口结果列表,
            德本预审=德本结果,
            防篡改指纹=指纹,
            证据留痕=证据文件,
            交叉验证=交叉验证,
            行为指纹=行为指纹,
            时间戳=_干支时间戳(),
        )

        # ── 9. 存储 ──
        self.审计链.存裁决(裁决)
        self._存日志(裁决, 被审计对象, 对象类型)

        return 裁决

    def _存证据(self, 对象: str, 类型: str, 规则结果: Dict, 裁决ID: str, 行为指纹: Optional[Dict] = None) -> Dict[str, str]:
        """生成证据文件"""
        ts = datetime.datetime.now()
        event_file = self.审计链.evidence_dir / f"event_{裁决ID}.json"
        detail_file = self.审计链.evidence_dir / f"detail_{ts.strftime('%Y%m%d_%H%M%S')}.log"

        事件数据 = {
            "verdict_id": 裁决ID,
            "target": 对象,
            "type": 类型,
            "color": 规则结果["颜色"].value,
            "fuse_level": 规则结果["熔断级别"].标签,
            "action": 规则结果["动作"].value,
            "triggers": 规则结果["触发条件"],
            "score": 规则结果.get("加权总分", 0),
            "behavior_fingerprint": 行为指纹,
            "stamp": _干支时间戳(),
            "timestamp": ts.isoformat(),
        }
        with open(event_file, 'w', encoding='utf-8') as f:
            json.dump(事件数据, f, ensure_ascii=False, indent=2)

        with open(detail_file, 'w', encoding='utf-8') as f:
            f.write(f"[{ts.isoformat()}] 三色审计详情\n")
            f.write(f"  裁决ID: {裁决ID}\n")
            f.write(f"  对象: {对象}\n")
            f.write(f"  类型: {类型}\n")
            f.write(f"  颜色: {规则结果['颜色'].value}\n")
            f.write(f"  熔断: {规则结果['熔断级别'].标签}\n")
            f.write(f"  动作: {规则结果['动作'].value}\n")
            f.write(f"  理由: {规则结果['理由'][:200]}\n")

        return {"事件文件": str(event_file), "详情文件": str(detail_file)}

    def _存日志(self, 裁决: 审计裁决, 对象: str, 类型: str):
        日志 = 审计日志条目(
            日志ID=f"LOG-{uuid.uuid4().hex[:8].upper()}",
            裁决ID=裁决.裁决ID,
            被审计对象=对象,
            对象类型=类型,
            三色=裁决.三色判定.value,
            熔断级别=裁决.熔断级别.标签,
            动作=裁决.执行动作.value,
            理由摘要=裁决.裁决理由[:100],
            时间戳=裁决.时间戳,
            dna=裁决.dna,
        )
        self.审计链.存日志(日志)

    def 查历史(self, limit: int = 20) -> List[Dict]:
        return self.审计链.查历史(limit)

    def 统计(self) -> Dict:
        stats = self.审计链.查统计()
        链完整, 链信息 = self.审计链.验证审计链完整性()
        stats["审计链完整性"] = 链信息
        return stats

    def 验证(self, 裁决ID: str, 原始内容: str, 原始指纹: str = "") -> Tuple[bool, str]:
        """验证裁决对应内容是否被篡改"""
        if 原始指纹:
            return 防篡改验证器.验证(原始内容, 原始指纹)
        return True, "无指纹可验证"

# ============================================================
# 九、向后兼容导出
# ============================================================

def audit(content: str, target_type: str = "系统行为", **kwargs) -> Dict:
    """便利函数 — 被其他脚本导入"""
    engine = 三色审计引擎()
    verdict = engine.审计(content, target_type, **kwargs)
    return asdict(verdict)

def quick_audit(content: str) -> Tuple[str, str]:
    """快速审计 — 只返回颜色和理由"""
    engine = 三色审计引擎(启用德本预审=False, 启用SI=False, 启用闸口=False)
    verdict = engine.审计(content)
    return verdict.三色判定.value, verdict.裁决理由

# ============================================================
# 十、CLI入口
# ============================================================

def _彩色输出(文本: str, 颜色: str) -> str:
    """终端彩色输出"""
    色码 = {"🟢": "\033[32m", "🟡": "\033[33m", "🔴": "\033[31m"}
    重置 = "\033[0m"
    return f"{色码.get(颜色, '')}{文本}{重置}"

def main():
    parser = argparse.ArgumentParser(
        description="🐉 龍魂·三色审计判定引擎 v2.0 · P05上帝之眼核心",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
审计流程: 防篡改 → 德本五问 → 加权规则匹配 → SI主权指数 → 十闸口 → 裁决 → 归档

示例:
  # 审计安全风险
  python3 bin/lh_three_color_audit.py audit --object "用户尝试越权访问系统目录" --type 安全风险

  # 审计合规性（含SI参数）
  python3 bin/lh_three_color_audit.py audit --object "修改P0铁律的请求" --type 合规性 --si-tian 0.2

  # 审计系统过载
  python3 bin/lh_three_color_audit.py audit --object "CPU使用率95%，内存使用率90%" --type 系统过载

  # 内容防篡改验证
  python3 bin/lh_three_color_audit.py verify --content "原始内容" --fingerprint abc123def456

  # 查看历史
  python3 bin/lh_three_color_audit.py history --limit 10

  # 查看统计
  python3 bin/lh_three_color_audit.py stats

  # 验证审计链完整性
  python3 bin/lh_three_color_audit.py chain-verify

  # 交互模式
  python3 bin/lh_three_color_audit.py interactive

  # JSON输出
  python3 bin/lh_three_color_audit.py audit --object "测试审计" --json
        """
    )

    subparsers = parser.add_subparsers(dest="command", help="子命令")

    # === audit: 执行审计 ===
    audit_parser = subparsers.add_parser("audit", help="执行三色审计")
    audit_parser.add_argument("--object", "-o", required=True, help="被审计对象描述")
    audit_parser.add_argument("--type", "-t", default="系统行为",
                              choices=["系统行为", "用户请求", "安全风险", "合规性问题", "系统过载", "代码审查", "部署检查"],
                              help="对象类型")
    audit_parser.add_argument("--context", "-c", default="", help="上下文JSON")
    audit_parser.add_argument("--fingerprint", "-f", help="预期内容指纹（防篡改验证）")
    audit_parser.add_argument("--si-tian", type=float, default=0.9, help="SI天参数(0-1)")
    audit_parser.add_argument("--si-di", type=float, default=0.8, help="SI地参数(0-1)")
    audit_parser.add_argument("--si-ren", type=float, default=0.7, help="SI人参数(0-1)")
    audit_parser.add_argument("--no-deben", action="store_true", help="跳过德本预审")
    audit_parser.add_argument("--no-si", action="store_true", help="跳过SI计算")
    audit_parser.add_argument("--no-gates", action="store_true", help="跳过十闸口")
    audit_parser.add_argument("--json", "-j", action="store_true", help="JSON格式输出")
    audit_parser.add_argument("--quiet", "-q", action="store_true", help="静默模式")

    # === verify: 防篡改验证 ===
    verify_parser = subparsers.add_parser("verify", help="内容防篡改验证")
    verify_parser.add_argument("--content", "-c", required=True, help="原始内容")
    verify_parser.add_argument("--fingerprint", "-f", required=True, help="预期指纹")
    verify_parser.add_argument("--hmac", help="预期HMAC签名")

    # === history ===
    history_parser = subparsers.add_parser("history", help="查看审计历史")
    history_parser.add_argument("--limit", type=int, default=20, help="条数")

    # === stats ===
    subparsers.add_parser("stats", help="审计统计")

    # === chain-verify ===
    subparsers.add_parser("chain-verify", help="验证审计链完整性")

    # === summary ===
    subparsers.add_parser("summary", help="生成审计活性摘要(07_AUDIT/audit_summary_*.json)")

    # === interactive ===
    subparsers.add_parser("interactive", help="交互模式")

    args = parser.parse_args()

    # --- 交互模式 ---
    if args.command == "interactive":
        engine = 三色审计引擎()
        print("\n" + "=" * 60)
        print("🐉 三色审计判定引擎 v2.0 - 交互模式")
        print("=" * 60)
        print("格式: 对象类型 | 对象描述")
        print("  audit 安全风险 | 用户尝试越权访问")
        print("  verify 原始内容 | 预期指纹")
        print("  stats / history / chain-verify")
        print("  exit 退出")
        print("=" * 60)

        while True:
            try:
                输入 = input("\n📥 > ").strip()
                if not 输入: continue
                if 输入.lower() in ['exit', 'quit']: break
                if 输入 == 'stats':
                    s = engine.统计()
                    print(json.dumps(s, ensure_ascii=False, indent=2)); continue
                if 输入 == 'history':
                    for h in engine.查历史(10):
                        print(f"  {h['color']} {h['verdict_id'][:14]} | {h['action']} | {h['timestamp']}"); continue
                if 输入 == 'chain-verify':
                    ok, msg = engine.审计链.验证审计链完整性()
                    print(f"  {msg}"); continue

                if 输入.startswith("verify "):
                    parts = 输入[7:].strip().split("|")
                    if len(parts) >= 2:
                        ok, msg = 防篡改验证器.验证(parts[0].strip(), parts[1].strip())
                        print(f"  {msg}")
                    continue

                parts = [p.strip() for p in 输入.split("|")]
                if len(parts) >= 2:
                    裁决 = engine.审计(parts[1], parts[0])
                    print(f"\n  {裁决.三色判定.value} 熔断:{裁决.熔断级别.标签} 动作:{裁决.执行动作.value}")
                    print(f"  {裁决.裁决理由[:120]}")
                    if 裁决.触发条件:
                        print(f"  触发: {裁决.触发条件[:3]}")
                else:
                    print("❌ 格式: 对象类型 | 对象描述")

            except KeyboardInterrupt: break
            except Exception as e: print(f"❌ {e}")
        return

    # --- verify ---
    if args.command == "verify":
        ok, msg = 防篡改验证器.验证(args.content, args.fingerprint, args.hmac or "")
        print(f"  {msg}")
        return

    # --- history ---
    if args.command == "history":
        engine = 三色审计引擎()
        历史 = engine.查历史(limit=args.limit)
        print(f"\n📋 审计历史（最新{len(历史)}条）")
        print("-" * 60)
        for h in 历史:
            print(f"  {h['color']} {h['verdict_id'][:16]}... | {h['action']} | {h['fuse_level']} | {h['timestamp']}")
            print(f"     {h['reason'][:80]}")
            print()
        return

    # --- stats ---
    if args.command == "stats":
        engine = 三色审计引擎()
        stats = engine.统计()
        print("\n📊 三色审计统计")
        print("=" * 50)
        print(f"  总裁决数: {stats['总裁决数']}")
        print(f"  三色分布: {stats['三色分布']}")
        print(f"  熔断分布: {stats['熔断分布']}")
        print(f"  审计链长度: {stats['审计链长度']}")
        print(f"  审计链完整性: {stats['审计链完整性']}")
        return

    # --- chain-verify ---
    if args.command == "chain-verify":
        chain = 审计链()
        ok, msg = chain.验证审计链完整性()
        print(f"  {msg}")
        return

    # --- summary: 审计活性摘要 ---
    # v2.1新增(2026-08-21): 解决 audit_summary 停更问题——每次运行生成 07_AUDIT/audit_summary_*.json
    if args.command == "summary":
        engine = 三色审计引擎()
        stats = engine.统计()
        ev_dir = Path.home() / ".longhun/audit/evidence"
        ev_files = len(list(ev_dir.glob("*.jsonl"))) if ev_dir.exists() else 0
        最近 = engine.查历史(limit=10)
        # 统一审计日志(仓库根)最新写入时间
        _root_log = Path(_PROJECT_ROOT) / "audit_log.jsonl"
        _root_ts = datetime.datetime.fromtimestamp(_root_log.stat().st_mtime).isoformat() if _root_log.exists() else "不存在"
        summary = {
            "DNA": f"#龍芯⚡️{datetime.datetime.now().strftime('%Y-%m-%d')}-AUDIT-SUMMARY-UID9622",
            "确认码": "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z",
            "生成时间": datetime.datetime.now().isoformat(),
            "统计": stats,
            "证据文件数": ev_files,
            "统一日志最新写入": _root_ts,
            "最近裁决": [{"裁决": h["verdict_id"], "三色": h["color"], "动作": h["action"],
                        "熔断级别": h["fuse_level"], "时间": h["timestamp"]} for h in 最近],
        }
        out_dir = Path(_PROJECT_ROOT) / "07_AUDIT"
        out_dir.mkdir(parents=True, exist_ok=True)
        out_file = out_dir / f"audit_summary_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(out_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
        print(f"✅ 审计活性摘要已生成: {out_file}")
        print(json.dumps(summary, ensure_ascii=False, indent=2))
        return

    # --- audit ---
    if args.command == "audit":
        try:
            上下文 = json.loads(args.context) if args.context else None
        except json.JSONDecodeError:
            print(f"⚠️ 上下文JSON解析失败，已忽略")
            上下文 = None

        SI参数 = {"天": args.si_tian, "地": args.si_di, "人": args.si_ren}

        engine = 三色审计引擎(
            启用德本预审=not args.no_deben,
            启用SI=not args.no_si,
            启用闸口=not args.no_gates,
        )

        裁决 = engine.审计(
            被审计对象=args.object,
            对象类型=args.type,
            上下文=上下文,
            内容指纹=args.fingerprint,
            SI参数=SI参数,
        )

        if args.json:
            def _enum_default(o):
                if isinstance(o, Enum):
                    return o.value
                raise TypeError(f"Object of type {o.__class__.__name__} is not JSON serializable")
            print(json.dumps(asdict(裁决), ensure_ascii=False, indent=2, default=_enum_default))
        elif args.quiet:
            print(f"{裁决.三色判定.value} {裁决.执行动作.value}")
        else:
            # 彩色终端输出
            print("\n" + "=" * 60)
            print(f"🐉 三色审计裁决")
            print("=" * 60)
            print(f"📋 裁决ID:  {裁决.裁决ID}")
            print(f"🧬 DNA:     {裁决.dna}")
            print(f"🎯 三色:    {_彩色输出(裁决.三色判定.value, 裁决.三色判定.value)}")
            print(f"⚡ 动作:    {裁决.执行动作.value}")
            print(f"🔥 熔断:    {裁决.熔断级别.标签} ({裁决.熔断级别.描述})")

            if 裁决.SI结果:
                si = 裁决.SI结果
                print(f"\n📐 SI主权指数:")
                print(f"   SI={si['SI']} score={si['score']} {si['color']} veto={si['veto']}")

            if 裁决.触发条件:
                print(f"\n📌 触发条件:")
                for 条件 in 裁决.触发条件[:8]:
                    print(f"   - {条件}")

            if 裁决.德本预审:
                print(f"\n⚖️  德本预审: {'✅ 通过' if 裁决.德本预审['全部通过'] else '❌ 不通过'}")

            if 裁决.闸口结果:
                红色闸 = [g for g in 裁决.闸口结果 if g.get("状态") == "🔴"]
                黄色闸 = [g for g in 裁决.闸口结果 if g.get("状态") == "🟡"]
                if 红色闸 or 黄色闸:
                    print(f"\n🚪 闸口异常:")
                    for g in 红色闸 + 黄色闸:
                        _闸口 = g.get("闸口", "")
                        _名 = _闸口[1] if isinstance(_闸口, (tuple, list)) and len(_闸口) > 1 else str(_闸口)
                        print(f"   {g.get('状态','')} {_名}: {g.get('详情','')[:60]}")

            if 裁决.交叉验证:
                print(f"\n🔍 P05交叉验证: {裁决.交叉验证}")

            print(f"\n📝 裁决理由:")
            for line in 裁决.裁决理由.split('\n')[:8]:
                print(f"   {line}")

            if 裁决.防篡改指纹:
                print(f"\n🔐 内容指纹: {裁决.防篡改指纹}")

            if 裁决.证据留痕:
                print(f"\n📁 证据留痕:")
                for k, v in 裁决.证据留痕.items():
                    print(f"   {k}: {v}")

            print(f"\n🕐 {裁决.时间戳[:19]}")
            print("=" * 60)
        return

    parser.print_help()

if __name__ == "__main__":
    main()
