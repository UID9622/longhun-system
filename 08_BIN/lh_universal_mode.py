#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# DNA: #龍芯⚡️丙午·乙巳·癸酉·亥时·䷀乾-UNIVERSAL-MODE-v2.0
# 创建者: 诸葛鑫（UID9622）
# 协议: CC BY-NC-SA 4.0（君子协议，来源链不可切断）
# 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# -*- coding: utf-8 -*-
"""
🐉 龍魂·统一AI执行模式 × ROOT_CARD审计 × 多后端工程输出 v2.0

    一个脚本，把龍魂全体系规则压缩成可执行 CLI：
      - 加载规范作为核心全局规则表
      - CLI 解析触发词 / 意图 / 隐私等级 / 审计色
      - 自动匹配规则 → 生成 ROOT_CARD
      - 输出工程包骨架 / Cursor指令 / Notion字段定义
      - 内置数字根审计 + 三色初判

用法:
    lh mode "给 Cursor 工程包，做一个本地文件扫描器"
    lh mode --triggers                # 列出所有触发词
    lh mode --root-card "文本内容"     # 为任意文本生成 ROOT_CARD
    lh mode --cursor "任务描述"        # 生成 Cursor 专用指令
    lh mode --batch input.txt         # 批量处理
    lh mode --notion-fields --json    # 输出 Notion 字段 schema
    lh mode --skeleton "项目名"        # 生成工程包骨架
    lh mode --config                  # 输出当前配置的 JSON schema

集成:
    lh --mode "文本"  或  lh mode "文本"
    详见 .codebuddy/COMMAND_INDEX.md

联动:
    P06 数学大师（数字根 + 369不动点校验）
    P05 三色审计（🟢🟡🔴初判 + 十闸口检查清单）
    P08 仓颉（CNSH命名校验）
    P15 乔前辈（DNA盖章 + GPG签章提示）
    P72 龍盾（熔断词检测）

三色: 🟢 v2.0 全量规则覆盖·P05+P06+P08+P15+P72联动 🟡 待实机验证 🔴无
"""

import os
import sys
import re
import json
import hashlib
import argparse
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone

# ═══════════════════════════════════════════════════════════════
# 零、常量焊死
# ═══════════════════════════════════════════════════════════════

ROOT = Path(__file__).resolve().parent.parent
CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
GPG_FINGERPRINT = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
DNA_BASE = "#龍芯⚡️丙午·乙巳·癸酉·亥时·䷀乾-UNIVERSAL-MODE-v2.0"
VERSION = "v2.0"

# 369不动点（焊死·不可改）
S369 = 369
LOG369 = 5.911
PERM369 = 108

# ═══════════════════════════════════════════════════════════════
# 一、全局规则表 — 触发词分类（与龍魂42技能对齐）
# ═══════════════════════════════════════════════════════════════

TRIGGER_TABLE: Dict[str, Dict] = {
    # ── 工程构建 ──
    "engineering": {
        "triggers": [
            "给 Cursor", "Cursor", "工程包", "落地", "文件树",
            "本地组件", "浏览器插件", "插件", "launchd",
            "SQLite", "IndexedDB", "WebSocket", "API",
            "Python脚本", "Shell脚本", "Mac开机自启",
            "一键执行", "验收", "回执", "写代码", "开发",
            "搭建", "脚手架", "CLI工具", "启动脚本",
            "systemd", "Docker", "Nginx", "部署脚本",
        ],
        "intent_type": "build",
        "default_backends": ["python"],
        "persona_route": "P04鲁班→P14吕蒙→P05审计",
        "action": "enter",
    },

    # ── CNSH / 数字根 / 哲学 ──
    "cnsh": {
        "triggers": [
            "CNSH", "中文语法", "中文语义编译", "语义桥",
            "数字为根", "数学根", "ROOT_CARD",
            "流场", "五行", "九宫", "三才", "洛书", "数字根",
            "龍魂统一AI执行模式", "多语言工程输出",
            "道德经", "太极", "八卦", "河图", "干支", "卦象",
        ],
        "intent_type": "route",
        "default_backends": ["cnsh", "python"],
        "persona_route": "P06数学大师→P08仓颉→P05审计",
        "action": "enter",
    },

    # ── 审计 / 复盘 / 整理 ──
    "audit": {
        "triggers": [
            "复盘", "重铸", "合并", "压缩", "整理",
            "扫一遍", "闭环", "防再犯", "记错本",
            "主线归一", "审查", "审计", "检查",
            "LU-ORIGIN-FULLSYNC", "LU-MEMORY-MERGE-ALL", "LU-REAL-CHECK",
            "对齐", "差多少", "有没有问题",
        ],
        "intent_type": "audit",
        "default_backends": ["notion", "json-yaml"],
        "persona_route": "P05上帝之眼→P03雯雯归档→P15乔前辈签章",
        "action": "hold",  # 🟡时先hold
    },

    # ── 安全 / 隐私 / 隐私熔断 ──
    "privacy": {
        "triggers": [
            "burn", "sealed", "hash_only", "no_external",
            "privacy", "阅后即焚", "直接封存",
            "商业机密", "国密", "涉密",
            "token", "私钥", "密钥", "API key", "password", "secret",
            "加密", "脱敏", "端侧加密",
        ],
        "intent_type": "seal",
        "default_backends": ["manual_only"],
        "persona_route": "P72龍盾→P05审计→P77黑天使(如需)",
        "action": "fuse",  # 立即熔断
    },

    # ── 经济 / 资源 / 预算 ──
    "economy": {
        "triggers": [
            "成本", "预算", "ROI", "值不值", "性价比",
            "打赏", "许愿池", "支付", "收费",
            "经济核算", "资源评估", "省钱",
        ],
        "intent_type": "evaluate",
        "default_backends": ["python"],
        "persona_route": "P07管仲→P01诸葛亮推演→P05审计",
        "action": "enter",
    },

    # ── 安全扫描 / 红蓝对抗 ──
    "security_scan": {
        "triggers": [
            "安全扫描", "漏洞检测", "渗透测试", "红蓝对抗",
            "攻击面", "CVE", "SQL注入", "XSS", "CSRF",
            "依赖检查", "黑天使", "P77",
        ],
        "intent_type": "scan",
        "default_backends": ["python"],
        "persona_route": "P77黑天使→P05审计→P72熔断",
        "action": "enter",
    },

    # ── 部署 / 发布 ──
    "deploy": {
        "triggers": [
            "部署", "上线", "发布", "同步鲲鹏",
            "推到服务器", "重启服务", "nginx reload",
            "systemd restart",
        ],
        "intent_type": "deploy",
        "default_backends": ["shell", "python"],
        "persona_route": "P14吕蒙→P77攻击面扫描→P05审计",
        "action": "enter",
    },

    # ── 搜索 / 知识检索 ──
    "search": {
        "triggers": [
            "搜索", "查一下", "搜一下", "找资料",
            "帮我查", "搜索一下",
        ],
        "intent_type": "query",
        "default_backends": ["python"],
        "persona_route": "搜索引擎(:9631)→P05审计来源",
        "action": "enter",
    },

    # ── 教学 / 解释 ──
    "teaching": {
        "triggers": [
            "教我", "教学", "大白话", "新手", "我是小白",
            "解释一下", "通俗", "举例", "打个比方",
            "类比", "入门的", "帮我理解",
        ],
        "intent_type": "explain",
        "default_backends": ["manual_only"],
        "persona_route": "P02宝宝温度→P08仓颉术语→P11李白创意",
        "action": "enter",
    },

    # ── 诊断 / 健康检查 ──
    "diagnosis": {
        "triggers": [
            "健康", "诊断", "体检", "自检",
            "检查系统", "有没有问题", "巡检",
            "状态怎么样", "自愈", "守护",
        ],
        "intent_type": "diagnose",
        "default_backends": ["python"],
        "persona_route": "P09孙思邈→P05审计→P72熔断",
        "action": "enter",
    },

    # ── GPG / 签名 / 签章 ──
    "signing": {
        "triggers": [
            "签名", "GPG签章", "签章", "补签",
            "验证签名", "检查签名", "GPG",
        ],
        "intent_type": "sign",
        "default_backends": ["python"],
        "persona_route": "P15乔前辈签章→P03雯雯归档",
        "action": "enter",
    },
}

# 触发词→分类快速索引（预处理）
_TRIGGER_INDEX: Dict[str, str] = {}
for _cat, _info in TRIGGER_TABLE.items():
    for _t in _info["triggers"]:
        _TRIGGER_INDEX[_t] = _cat


# ═══════════════════════════════════════════════════════════════
# 二、数字根 & 五行 & 三色初判（P06 数学大师）
# ═══════════════════════════════════════════════════════════════

# 数字根 → 五行
DIGITAL_ROOT_WUXING = {
    0: "土", 1: "水", 2: "火", 3: "木", 4: "金",
    5: "土", 6: "水", 7: "火", 8: "木", 9: "金",
}

# 数字根 → 含义
ROOT_MEANING = {
    0: "中宫·承载·普惠",     1: "水·生长·记忆之源",
    2: "火·表达·行动之光",    3: "木·创新·生长之力",
    4: "金·规则·结构之骨",    5: "土·均衡·承载之基",
    6: "水·流变·待审之镜",    7: "火·洞察·光明之眼",
    8: "木·生长·扩展之翼",    9: "金·收敛·熔断之剑",
}

# 三色初判闸（数字根→审计色）
# 🟢 放行 root ∈ {0,1,2,4,5,7,8}
# 🟡 待核 root ∈ {6}（流变·需复核）
# 🔴 熔断 root ∈ {3,9}（木3·创新需谨慎 | 金9·收敛熔断）
ROOT_GATE = {
    "🟢": {0, 1, 2, 4, 5, 7, 8},
    "🟡": {6},
    "🔴": {3, 9},
}

# 五行生克矩阵
WUXING_GENERATE = {"金": "水", "水": "木", "木": "火", "火": "土", "土": "金"}
WUXING_RESTRAIN = {"金": "木", "木": "土", "土": "水", "水": "火", "火": "金"}


def digital_root(text: str) -> int:
    """计算文本的数字根——提取所有数字字符求和，递归压缩至个位数。
    369不动点校验：结果为 3/6/9 时标记为不动点。
    """
    digits = [int(c) for c in text if c.isdigit()]
    if not digits:
        # 无数字时用字符 Unicode 码点求和
        digits = [ord(c) % 10 for c in text if c.strip()]
        if not digits:
            return 0
    n = sum(digits)
    while n >= 10:
        n = sum(int(c) for c in str(n))
    return n


def wuxing_from_root(root: int) -> str:
    return DIGITAL_ROOT_WUXING.get(root, "土")


def tricolor_from_root(root: int) -> str:
    for color, roots in ROOT_GATE.items():
        if root in roots:
            return color
    return "🟡"


def is_369_anchor(root: int) -> bool:
    """判断数字根是否为369不动点"""
    return root in (3, 6, 9)


def root_card_checksum(text: str) -> str:
    """生成 ROOT_CARD 的 SHA-256 校验和（前12位）"""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:12]


# ═══════════════════════════════════════════════════════════════
# 三、数据等级与隐私策略
# ═══════════════════════════════════════════════════════════════

DATA_LEVEL_POLICY = {
    "L0_PUBLIC": {
        "privacy_mode": "normal",
        "retention": "full",
        "trace_mode": "chain",
        "can_export": True,
        "can_publish": True,
    },
    "L1_INTERNAL": {
        "privacy_mode": "normal",
        "retention": "summary_only",
        "trace_mode": "chain",
        "can_export": "confirm_required",
        "can_publish": "confirm_required",
    },
    "L2_PERSONAL": {
        "privacy_mode": "burn",
        "retention": "hash_only_or_summary_only",
        "trace_mode": "local_only",
        "can_export": False,
        "can_publish": False,
    },
    "L3_BUSINESS_INTERNAL": {
        "privacy_mode": "burn_or_sealed",
        "retention": "hash_only",
        "trace_mode": "no_external",
        "can_export": False,
        "can_publish": False,
    },
    "L4_TRADE_SECRET": {
        "privacy_mode": "sealed",
        "retention": "hash_only",
        "trace_mode": "no_external",
        "can_export": False,
        "can_publish": False,
    },
    "L5_IMPORTANT_DATA": {
        "privacy_mode": "sealed",
        "retention": "hash_only",
        "trace_mode": "no_external",
        "can_export": False,
        "can_publish": False,
    },
    "L6_STATE_SECRET": {
        "privacy_mode": "sealed",
        "retention": "hash_only",
        "trace_mode": "no_external",
        "can_export": False,
        "can_publish": False,
    },
}

# 数据等级判定关键词
DATA_LEVEL_KEYWORDS = {
    "L6_STATE_SECRET": [
        "国家秘密", "军事", "核", "机密级", "绝密级",
    ],
    "L5_IMPORTANT_DATA": [
        "重要数据", "关键基础设施", "基因数据", "人口健康",
    ],
    "L4_TRADE_SECRET": [
        "商业机密", "核心算法", "未公开专利", "竞品数据",
    ],
    "L3_BUSINESS_INTERNAL": [
        "内部数据", "未发布", "内部文档", "内部邮件",
    ],
    "L2_PERSONAL": [
        "个人信息", "手机号", "身份证", "住址", "人脸",
        "声纹", "位置", "行为", "消费记录", "健康档案",
    ],
    "L1_INTERNAL": [
        "内部", "项目内部", "团队内部", "部门",
    ],
}

# ═══════════════════════════════════════════════════════════════
# 四、一票否决模式（P72 龍盾 + P05 审计联动）
# ═══════════════════════════════════════════════════════════════

VETO_PATTERNS: List[Tuple[str, str, str]] = [
    # (正则, 违规描述, 熔断级别)
    (r"改写.*CONFIRM", "试图篡改确认码", "L0"),
    (r"截断.*GPG", "试图截断GPG签名链", "L0"),
    (r"删除.*DNA", "试图删除DNA追溯", "L0"),
    (r"去掉.*签章|跳过.*审计|绕过.*熔断", "试图绕过审计/签章/熔断", "L0"),
    (r"伪造.*签名|冒充.*UID9622", "身份伪造", "L0"),
    (r"擅自深度研究", "越权深度研究", "L1"),
    (r"工程任务.*论文", "任务类型偏移", "L2"),
    (r"复盘任务.*鸡汤", "审计任务娱乐化", "L2"),
    (r"未执行.*已执行|无API.*已同步|无文件写入.*已落盘", "虚假汇报", "L1"),
    (r"无测试.*已通过", "跳过测试", "L1"),
    (r"读取.*token|读取.*私钥|读取.*密钥", "尝试读取敏感凭证", "L1"),
    (r"sealed.*正文|burn.*正文|no_external.*外发", "违反隐私策略", "L1"),
    (r"帮我绕过|偷偷|别留记录|不留痕迹", "恶意绕过请求", "L0"),
    (r"技术无国界|用户体验优先|灵活处理|国际接轨|简化管理|商业化需要|平衡各方|行业标准",
     "一票否决词触发", "L2"),
]


def check_veto(text: str) -> List[Dict]:
    """检查文本是否触犯一票否决模式"""
    hits = []
    for pattern, desc, level in VETO_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            hits.append({
                "pattern": pattern,
                "violation": desc,
                "fuse_level": level,
                "snippet": text[max(0, text.lower().find(pattern.lower().split(".*")[0]) - 20):
                                 text.lower().find(pattern.lower().split(".*")[0]) + 60],
            })
    return hits


def detect_data_level(text: str) -> str:
    """根据关键词自动判定数据等级（取最高）"""
    current = "L0_PUBLIC"
    level_order = ["L0_PUBLIC", "L1_INTERNAL", "L2_PERSONAL",
                   "L3_BUSINESS_INTERNAL", "L4_TRADE_SECRET",
                   "L5_IMPORTANT_DATA", "L6_STATE_SECRET"]
    for level in reversed(level_order):  # 从高到低
        for kw in DATA_LEVEL_KEYWORDS.get(level, []):
            if kw in text:
                return level
    return current


def infer_backends(text: str) -> List[str]:
    """根据文本关键词推断所需技术后端"""
    backend_map = {
        "python": ["Python", "python", "脚本", "Django", "Flask", "FastAPI",
                    "机器学习", "AI", "模型", "Ollama", "MLX"],
        "swift": ["Swift", "iOS", "App", "Mac菜单栏", "Mac App",
                   "macOS", "iPhone", "iPad"],
        "cpp": ["C++", "Rust", "c++", "高性能", "嵌入式", "固件"],
        "js-ts": ["JS", "TS", "JavaScript", "TypeScript", "前端",
                   "React", "Vue", "Node", "npm", "yarn"],
        "html-css": ["HTML", "CSS", "页面", "网页", "Web页面",
                      "响应式", "静态页面"],
        "json-yaml": ["JSON", "YAML", "配置", "schema", "数据格式"],
        "shell": ["Shell", "Bash", "Zsh", "launchd", "systemd",
                   "cron", "脚本", "命令行"],
        "notion": ["Notion", "数据库", "字段", "页面", "知识库"],
        "cursor": ["Cursor", "IDE指令", ".cursorrules", "AI辅助"],
    }
    found = []
    for backend, keywords in backend_map.items():
        if any(kw in text for kw in keywords):
            found.append(backend)
    return found if found else ["manual_only"]


# ═══════════════════════════════════════════════════════════════
# 五、核心引擎 — CNSHModeEngine v2.0
# ═══════════════════════════════════════════════════════════════

class CNSHModeEngine:
    """龍魂统一执行模式引擎。输入任意文本 → 输出完整决策包 + ROOT_CARD。"""

    def __init__(self):
        self.reset()

    def reset(self):
        self.root = 0
        self.wuxing = "土"
        self.tricolor = "🟢"
        self.data_level = "L0_PUBLIC"
        self.privacy_mode = "normal"
        self.retention = "full"
        self.trace_mode = "chain"
        self.backends: List[str] = []
        self.action = "enter"
        self.trigger_category: Optional[str] = None
        self.intent_type = "explain"
        self.persona_route = ""
        self.veto_hits: List[Dict] = []
        self.is_369 = False
        self.checksum = ""
        self.timestamp = ""

    def analyze(self, text: str) -> Dict:
        """主入口：分析文本，返回完整决策包"""
        self.reset()
        self.timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

        # 1. 数字根
        self.root = digital_root(text)
        self.wuxing = wuxing_from_root(self.root)
        self.tricolor = tricolor_from_root(self.root)
        self.is_369 = is_369_anchor(self.root)

        # 2. 触发词分类
        self.trigger_category = self._detect_category(text)
        cat_info = TRIGGER_TABLE.get(self.trigger_category, {})

        if self.trigger_category:
            self.intent_type = cat_info.get("intent_type", "explain")
            self.backends = infer_backends(text) or cat_info.get("default_backends", ["manual_only"])
            self.persona_route = cat_info.get("persona_route", "")
            self.action = cat_info.get("action", "enter")
        else:
            self.intent_type = "explain"
            self.backends = infer_backends(text) or ["manual_only"]
            self.persona_route = "P00文心意图解析→P04鲁班默认执行"
            self.action = "enter"

        # 3. 审计色修正：🟡时action=hold；🔴时action=fuse
        if self.tricolor == "🟡" and self.action == "enter":
            self.action = "hold"
        elif self.tricolor == "🔴":
            self.action = "fuse"

        # 4. 数据等级 & 隐私策略
        self.data_level = detect_data_level(text)
        policy = DATA_LEVEL_POLICY.get(self.data_level, DATA_LEVEL_POLICY["L0_PUBLIC"])
        self.privacy_mode = policy["privacy_mode"]
        self.retention = policy["retention"]
        self.trace_mode = policy["trace_mode"]

        # 隐私类触发词强制升级
        if self.trigger_category == "privacy":
            self.privacy_mode = "sealed"
            self.retention = "hash_only"
            self.trace_mode = "no_external"
            self.data_level = max(self.data_level, "L4_TRADE_SECRET",
                                  key=lambda x: list(DATA_LEVEL_POLICY.keys()).index(x))
            self.action = "fuse"

        # 5. 一票否决检测
        self.veto_hits = check_veto(text)
        if self.veto_hits:
            self.action = "fuse"
            self.tricolor = "🔴"
            # L0级熔断 → 数据等级拉到最高
            if any(h["fuse_level"] == "L0" for h in self.veto_hits):
                self.data_level = "L6_STATE_SECRET"
                self.privacy_mode = "sealed"
                self.retention = "hash_only"
                self.trace_mode = "no_external"

        # 6. 生成校验和
        self.checksum = root_card_checksum(text)

        return self.to_dict()

    def _detect_category(self, text: str) -> Optional[str]:
        """最长匹配触发词分类"""
        best_cat, best_len = None, 0
        for cat, info in TRIGGER_TABLE.items():
            for t in info["triggers"]:
                if t in text and len(t) > best_len:
                    best_cat, best_len = cat, len(t)
        return best_cat

    def to_dict(self) -> Dict:
        return {
            "root": self.root,
            "wuxing": self.wuxing,
            "tricolor": self.tricolor,
            "is_369_anchor": self.is_369,
            "data_level": self.data_level,
            "privacy_mode": self.privacy_mode,
            "retention": self.retention,
            "trace_mode": self.trace_mode,
            "backends": self.backends,
            "action": self.action,
            "trigger_category": self.trigger_category,
            "intent_type": self.intent_type,
            "persona_route": self.persona_route,
            "veto_triggered": bool(self.veto_hits),
            "veto_hits": self.veto_hits,
            "checksum": self.checksum,
            "timestamp": self.timestamp,
        }

    def generate_root_card(self, text: str, custom_meta: Dict = None) -> Dict:
        """生成标准 ROOT_CARD v2.0"""
        decision = self.analyze(text)
        root_card = {
            # ── 核心信息 ──
            "ROOT_CARD_VERSION": "v2.0",
            "Root": f"dr={decision['root']}",
            "Wuxing": decision["wuxing"],
            "RootMeaning": ROOT_MEANING.get(decision["root"], "规则"),
            "Is369Anchor": decision["is_369_anchor"],
            "TriColor": decision["tricolor"],

            # ── 策略信息 ──
            "DataLevel": decision["data_level"],
            "PrivacyMode": decision["privacy_mode"],
            "Retention": decision["retention"],
            "TraceMode": decision["trace_mode"],

            # ── 路由信息 ──
            "IntentType": decision["intent_type"],
            "PersonaRoute": decision["persona_route"],
            "Backend": decision["backends"],
            "Action": decision["action"],

            # ── 审计信息 ──
            "VetoTriggered": decision["veto_triggered"],
            "VetoCount": len(decision["veto_hits"]),
            "Checksum": decision["checksum"],
            "Timestamp": decision["timestamp"],

            # ── 身份焊死 ──
            "DNA": DNA_BASE,
            "CONFIRM": CONFIRM,
            "GPG": GPG_FINGERPRINT,
            "Creator": "诸葛鑫（UID9622）",
            "Protocol": "CC BY-NC-SA 4.0",

            # ── 369锚点 ──
            "Anchor369": {
                "sn": S369,
                "log369": LOG369,
                "perm369": PERM369,
            },
        }
        if custom_meta:
            root_card["Custom"] = custom_meta
        return root_card

    # ── 输出生成器 ──

    def generate_cursor_prompt(self, text: str) -> str:
        """生成 Cursor IDE 专用指令"""
        decision = self.analyze(text)
        root_card = self.generate_root_card(text)

        # 根据意图类型生成不同风格的 prompt
        if decision["veto_triggered"]:
            fuse_warning = "\n".join(
                f"  ⚠️ [{h['fuse_level']}] {h['violation']}"
                for h in decision["veto_hits"]
            )
            fuse_block = f"""
🔴 熔断警告 — 以下违规已触发:
{fuse_warning}

本任务已冻结。需 UID9622 人工放行后方可继续。
"""
        else:
            fuse_block = ""

        prompt = f"""<!--
  龍魂·统一执行模式 ROOT_CARD v2.0
  生成时间: {decision['timestamp']}
  数字根: dr={decision['root']} ({decision['wuxing']})
  三色: {decision['tricolor']}
  数据等级: {decision['data_level']}
  人格路由: {decision['persona_route']}
  DNA: {DNA_BASE}
  CONFIRM: {CONFIRM}
-->
{fuse_block}
## 📋 任务

{text}

## ⚙️ 执行约束

1. **不写研究报告** — 直接给工程落地。
2. **必须包含**: 文件树、创建/修改清单、代码、测试、验收、回执。
3. **不破坏** DNA / CONFIRM / GPG 签名链。
4. **不读取** .env / token / 私钥 / 密码。
5. **不假装同步** Notion / API（除非实测可达）。
6. **不联网** 除非明确配置了官方公开 URL。
7. 所有隐私内容按 `{decision['privacy_mode']}` / `{decision['retention']}` 处理。
8. 最后输出**执行回执**（做了什么 / 没做什么 / 为什么没做）。

## 🏗️ 技术后端

`{', '.join(decision['backends'])}`

## 🔍 审计检查点

- [ ] GATE-01 身份闸(P13): 操作者身份确认
- [ ] GATE-03 语义闸(P08): 无一票否决词
- [ ] GATE-04 数字根闸(P06): dr={decision['root']} {'⚠️ 369不动点·需复核' if decision['is_369_anchor'] else '🟢'}
- [ ] GATE-05 伦理闸(P12): 六誓验证
- [ ] GATE-06 数据闸(P05): {decision['data_level']} — {decision['trace_mode']}
- [ ] GATE-09 DNA闸(P15): 产出文件挂DNA头三行

## 📦 验收标准

- 文件能创建 ✓
- 命令能运行 ✓
- 日志能写 ✓
- 错误能回执 ✓
- 没做的必须说没做 ✓
"""
        return prompt

    def generate_notion_schema(self) -> Dict:
        """生成 Notion 数据库字段定义"""
        return {
            "database_name": "龍魂·统一执行模式 ROOT_CARD v2.0",
            "properties": {
                "Title": {"type": "title"},
                "UnifiedName": {"type": "rich_text"},
                "Version": {"type": "select", "options": ["v1.0", "v1.1", "v1.2", "v1.3", "v2.0"]},
                "TriggerCategory": {
                    "type": "select",
                    "options": list(TRIGGER_TABLE.keys()),
                },
                "IntentType": {
                    "type": "select",
                    "options": ["build", "route", "audit", "seal", "evaluate",
                                "scan", "deploy", "query", "explain", "diagnose", "sign"],
                },
                "DataLevel": {
                    "type": "select",
                    "options": list(DATA_LEVEL_POLICY.keys()),
                },
                "PrivacyMode": {
                    "type": "select",
                    "options": ["normal", "burn", "sealed", "burn_or_sealed"],
                },
                "Retention": {
                    "type": "select",
                    "options": ["full", "summary_only", "hash_only", "hash_only_or_summary_only"],
                },
                "TraceMode": {
                    "type": "select",
                    "options": ["chain", "local_only", "no_external"],
                },
                "Backend": {
                    "type": "multi_select",
                    "options": ["python", "swift", "cpp", "js-ts", "html-css",
                                "json-yaml", "shell", "notion", "cursor", "manual_only", "cnsh"],
                },
                "PersonaRoute": {"type": "rich_text"},
                "AuditColor": {"type": "select", "options": ["🟢", "🟡", "🔴"]},
                "Action": {"type": "select", "options": ["enter", "hold", "fuse"]},
                "Is369Anchor": {"type": "checkbox"},
                "DigitalRoot": {"type": "number"},
                "Wuxing": {"type": "select", "options": ["金", "水", "木", "火", "土"]},
                "VetoTriggered": {"type": "checkbox"},
                "Checksum": {"type": "rich_text"},
                "DNA": {"type": "rich_text"},
                "CONFIRM": {"type": "rich_text"},
                "GPG": {"type": "rich_text"},
                "Status": {
                    "type": "status",
                    "options": ["草案", "已确认", "已入库", "待执行", "已执行", "已归档", "熔断"],
                },
                "NextAction": {"type": "rich_text"},
                "CreatedAt": {"type": "date"},
            },
        }

    def generate_skeleton(self, project_name: str, backends: List[str] = None,
                          text: str = "") -> Dict:
        """生成工程包骨架（目录结构 + 文件清单）"""
        if backends is None:
            decision = self.analyze(text) if text else self.to_dict()
            backends = decision.get("backends", ["python"])

        skeleton = {
            "project": project_name,
            "DNA": DNA_BASE,
            "CONFIRM": CONFIRM,
            "GPG": GPG_FINGERPRINT,
            "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        }

        files = []
        dirs = set()

        # Python 后端
        if "python" in backends:
            dirs.update(["src", "tests", "config"])
            files += [
                f"{project_name}/src/__init__.py",
                f"{project_name}/src/main.py",
                f"{project_name}/src/core.py",
                f"{project_name}/tests/__init__.py",
                f"{project_name}/tests/test_core.py",
                f"{project_name}/config/settings.py",
                f"{project_name}/requirements.txt",
                f"{project_name}/README.md",
            ]

        # Swift 后端
        if "swift" in backends:
            dirs.add("Sources")
            files += [
                f"{project_name}/Sources/main.swift",
                f"{project_name}/Sources/AppDelegate.swift",
                f"{project_name}/Package.swift",
            ]

        # JS/TS 后端
        if "js-ts" in backends:
            dirs.update(["src", "public"])
            files += [
                f"{project_name}/src/index.ts",
                f"{project_name}/public/index.html",
                f"{project_name}/package.json",
                f"{project_name}/tsconfig.json",
            ]

        # C++ 后端
        if "cpp" in backends:
            dirs.update(["src", "include", "build"])
            files += [
                f"{project_name}/src/main.cpp",
                f"{project_name}/include/core.h",
                f"{project_name}/CMakeLists.txt",
            ]

        # Shell 后端
        if "shell" in backends:
            dirs.add("scripts")
            files += [
                f"{project_name}/scripts/start.sh",
                f"{project_name}/scripts/deploy.sh",
                f"{project_name}/Makefile",
            ]

        # HTML/CSS 后端
        if "html-css" in backends:
            dirs.update(["css", "js", "assets"])
            files += [
                f"{project_name}/index.html",
                f"{project_name}/css/style.css",
                f"{project_name}/js/main.js",
            ]

        # 通用文件
        files += [
            f"{project_name}/.gitignore",
            f"{project_name}/.cursorrules",
        ]
        dirs.add(project_name)

        skeleton["directories"] = sorted(dirs)
        skeleton["files"] = sorted(files)
        skeleton["file_count"] = len(files)

        return skeleton

    def generate_config_schema(self) -> Dict:
        """输出当前配置的 JSON Schema"""
        return {
            "engine": "CNSHModeEngine v2.0",
            "DNA": DNA_BASE,
            "CONFIRM": CONFIRM,
            "GPG": GPG_FINGERPRINT,
            "creator": "诸葛鑫（UID9622）",
            "protocol": "CC BY-NC-SA 4.0",
            "anchor_369": {"sn": S369, "log369": LOG369, "perm369": PERM369},
            "trigger_categories": {
                cat: {
                    "count": len(info["triggers"]),
                    "sample_triggers": info["triggers"][:8],
                    "intent_type": info["intent_type"],
                    "persona_route": info["persona_route"],
                }
                for cat, info in TRIGGER_TABLE.items()
            },
            "data_levels": {
                level: policy
                for level, policy in DATA_LEVEL_POLICY.items()
            },
            "veto_patterns_count": len(VETO_PATTERNS),
            "digital_root": {
                "gate": {color: sorted(roots) for color, roots in ROOT_GATE.items()},
                "wuxing_map": DIGITAL_ROOT_WUXING,
                "meaning_map": ROOT_MEANING,
            },
            "backends_inferable": [
                "python", "swift", "cpp", "js-ts", "html-css",
                "json-yaml", "shell", "notion", "cursor", "cnsh",
            ],
            "output_formats": [
                "root_card", "cursor_prompt", "notion_schema",
                "skeleton", "config_schema", "batch", "raw_analysis",
            ],
            "integrations": {
                "P05_audit": "三色审计初判 + 十闸口清单",
                "P06_math": "数字根 + 五行 + 369不动点校验",
                "P08_cnsh": "CNSH命名规范校验",
                "P15_sign": "DNA盖章 + GPG签章提示",
                "P72_fuse": "一票否决词 + 四级熔断",
            },
        }


# ═══════════════════════════════════════════════════════════════
# 六、CLI 入口
# ═══════════════════════════════════════════════════════════════

def print_banner():
    print(f"\n  🐉 龍魂·统一AI执行模式 v2.0")
    print(f"  DNA: {DNA_BASE}")
    print(f"  CONFIRM: {CONFIRM}\n")


def main():
    parser = argparse.ArgumentParser(
        description="🐉 龍魂·统一AI执行模式 × ROOT_CARD审计 × 多后端工程输出 v2.0",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
示例:
  lh mode "给 Cursor 工程包，做一个本地文件扫描器"
  lh mode --triggers
  lh mode --root-card "复盘近期10个AI对话"
  lh mode --cursor "用Swift写Mac菜单栏工具"
  lh mode --batch input.txt
  lh mode --notion-fields --json
  lh mode --skeleton my-project
  lh mode --config --json

DNA: {DNA_BASE}
CONFIRM: {CONFIRM}
        """,
    )
    parser.add_argument("text", nargs="*", help="要分析的文本（自然语言）")
    parser.add_argument("--triggers", "-t", action="store_true", help="列出所有触发词")
    parser.add_argument("--root-card", "-r", action="store_true", help="生成 ROOT_CARD")
    parser.add_argument("--cursor", "-c", action="store_true", help="生成 Cursor 专用指令")
    parser.add_argument("--notion-fields", action="store_true", help="输出 Notion 数据库字段定义")
    parser.add_argument("--skeleton", "-s", type=str, metavar="NAME",
                        help="生成工程包骨架（项目名）")
    parser.add_argument("--batch", "-b", type=str, metavar="FILE",
                        help="批量处理文件（每行一个任务）")
    parser.add_argument("--config", action="store_true", help="输出当前配置 JSON schema")
    parser.add_argument("--json", "-j", action="store_true", help="以 JSON 格式输出")
    parser.add_argument("--backends", type=str, metavar="LIST",
                        help="指定后端（逗号分隔，如 python,swift,shell）")
    args = parser.parse_args()

    engine = CNSHModeEngine()

    # ── 列出触发词 ──
    if args.triggers:
        print_banner()
        print("📋 触发词分类表 (共 {} 类 · {} 个触发词):\n".format(
            len(TRIGGER_TABLE),
            sum(len(info["triggers"]) for info in TRIGGER_TABLE.values()),
        ))
        for cat, info in TRIGGER_TABLE.items():
            print(f"  [{info['intent_type']:8s}] {cat:16s} → {info['persona_route']}")
            # 分组显示触发词，每行最多4个
            triggers = info["triggers"]
            for i in range(0, len(triggers), 4):
                chunk = triggers[i:i+4]
                print(f"           {' · '.join(chunk)}")
            print()
        return

    # ── Notion 字段 ──
    if args.notion_fields:
        schema = engine.generate_notion_schema()
        if args.json:
            print(json.dumps(schema, ensure_ascii=False, indent=2))
        else:
            print_banner()
            print(f"📋 Notion 数据库: {schema['database_name']}\n")
            for name, spec in schema["properties"].items():
                opts = spec.get("options", [])
                opt_str = f" ({', '.join(opts)})" if opts else ""
                print(f"  - {name}: {spec['type']}{opt_str}")
        return

    # ── 配置 schema ──
    if args.config:
        schema = engine.generate_config_schema()
        print(json.dumps(schema, ensure_ascii=False, indent=2))
        return

    # ── 批量处理 ──
    if args.batch:
        path = Path(args.batch)
        if not path.exists():
            print(f"❌ 文件不存在: {args.batch}", file=sys.stderr)
            sys.exit(1)
        content = path.read_text(encoding="utf-8")
        lines = [l.strip() for l in content.splitlines() if l.strip()]
        results = []
        for i, line in enumerate(lines):
            decision = engine.analyze(line)
            entry = {
                "index": i + 1,
                "text": line[:120],
                "decision": decision,
            }
            results.append(entry)

        if args.json:
            print(json.dumps(results, ensure_ascii=False, indent=2))
        else:
            print_banner()
            print(f"📦 批量处理: {len(lines)} 条\n")
            for r in results:
                d = r["decision"]
                veto = " ⚠️VETO" if d["veto_triggered"] else ""
                anchor = " [369]" if d["is_369_anchor"] else ""
                print(f"  {d['tricolor']} dr={d['root']}({d['wuxing']})"
                      f" {d['action']:5s} | {d['trigger_category'] or '未分类':16s}"
                      f" | {d['intent_type']}{veto}{anchor}")
                print(f"     {r['text'][:80]}...")
            print()
        return

    # ── 工程骨架（不需要文本参数）──
    if args.skeleton:
        backends_list = args.backends.split(",") if args.backends else ["python", "shell"]
        skeleton = engine.generate_skeleton(args.skeleton, backends_list)
        if args.json:
            print(json.dumps(skeleton, ensure_ascii=False, indent=2))
        else:
            print_banner()
            print(f"🏗️ 工程包骨架: {args.skeleton}\n")
            print(f"📁 目录 ({len(skeleton['directories'])}):")
            for d in sorted(skeleton["directories"]):
                print(f"    {d}/")
            print(f"\n📄 文件 ({skeleton['file_count']}):")
            for f in skeleton["files"]:
                print(f"    {f}")
            print(f"\n  🧬 DNA: {skeleton['DNA']}")
        return

    # ── 需要文本输入的命令 ──
    text = " ".join(args.text) if args.text else ""
    if not text:
        parser.print_help()
        return

    # ── Cursor 指令 ──
    if args.cursor:
        prompt = engine.generate_cursor_prompt(text)
        if args.json:
            print(json.dumps({"cursor_prompt": prompt}, ensure_ascii=False, indent=2))
        else:
            print(prompt)
        return

    # ── ROOT_CARD ──
    if args.root_card:
        root_card = engine.generate_root_card(text)
        if args.json:
            print(json.dumps(root_card, ensure_ascii=False, indent=2))
        else:
            print_banner()
            print("🧬 ROOT_CARD v2.0:\n")
            for k, v in root_card.items():
                if k == "Anchor369":
                    print(f"  {k}: sn=369 log369=5.911 perm369=108")
                elif isinstance(v, dict):
                    pass  # skip nested in plain mode
                else:
                    print(f"  {k:20s}: {v}")
        return

    # ── 默认：输出完整分析 ──
    decision = engine.analyze(text)
    if args.json:
        print(json.dumps(decision, ensure_ascii=False, indent=2))
    else:
        print_banner()
        print(f"🔍 分析结果:\n")
        print(f"  数字根     : {decision['root']} ({decision['wuxing']}) {'⚠️ 369不动点' if decision['is_369_anchor'] else ''}")
        print(f"  三色审计   : {decision['tricolor']}")
        print(f"  数据等级   : {decision['data_level']}")
        print(f"  隐私模式   : {decision['privacy_mode']}")
        print(f"  保留策略   : {decision['retention']}")
        print(f"  追踪模式   : {decision['trace_mode']}")
        print(f"  触发分类   : {decision['trigger_category'] or '未分类'}")
        print(f"  意图类型   : {decision['intent_type']}")
        print(f"  人格路由   : {decision['persona_route']}")
        print(f"  目标后端   : {', '.join(decision['backends'])}")
        print(f"  执行动作   : {decision['action']}")
        print(f"  校验和     : {decision['checksum']}")

        if decision["veto_triggered"]:
            print(f"\n  ⚠️ 一票否决已触发 ({len(decision['veto_hits'])} 项):")
            for h in decision["veto_hits"]:
                print(f"     [{h['fuse_level']}] {h['violation']}")
                print(f"     匹配: {h['snippet']}")

        print()


if __name__ == "__main__":
    main()
