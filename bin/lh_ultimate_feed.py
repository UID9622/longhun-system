#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·乙未·甲辰-终极投喂-v1.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
"""
╔══════════════════════════════════════════════════════════════════╗
║  龍魂·终极投喂引擎 v1.0 — 做减法，不做加法                      ║
║  DNA: #龍芯⚡️丙午·乙未·甲辰-终极投喂-v1.0                     ║
╠══════════════════════════════════════════════════════════════════╣
║  定位：减少结构噪音，让系统更能跑，而不是更大                    ║
║  负责人格：⚖️ 审判长 (P05上帝之眼)                              ║
║  协同人格：🤖 宝宝(P02) · 🧙 诸葛亮(P01) · 📋 雯雯(P03)        ║
║  优先级：P0级                                                    ║
╠══════════════════════════════════════════════════════════════════╣
║  核心流程：                                                      ║
║  1. 内容分类 — 自动识别 文档/代码/知识库/规则/协议/配置/对话    ║
║  2. 合并 — 语义相同的内容合并为一个核心单元                      ║
║  3. 覆盖 — 新内容表达更好则覆盖旧版本                            ║
║  4. 删除候选 — 无法调用的内容标记为创意池                        ║
║  5. 执行流对齐 — 强制判断是否能命中模板/量子/规则/索引           ║
║  6. 自动补全但不膨胀 — 只补DNA/人格/标签/索引                    ║
║  7. 国内/国外融合 — 同主题只保留系统标准版本                     ║
║  8. 质量评分 — 五维评分(完整度/可执行度/新鲜度/引用率/去重度)    ║
║  9. 页面结构生成 — 自动生成文档/代码/知识库展示模板              ║
║  10. 状态报告 — 按内容类型分类汇报合并/覆盖/冻结明细             ║
╠══════════════════════════════════════════════════════════════════╣
║  用法：                                                          ║
║    python3 bin/lh_ultimate_feed.py -f content.txt                ║
║    python3 bin/lh_ultimate_feed.py -c "内容1" -c "内容2"        ║
║    python3 bin/lh_ultimate_feed.py --import-dir ./docs/          ║
║    python3 bin/lh_ultimate_feed.py --interactive                 ║
║    python3 bin/lh_ultimate_feed.py --status                      ║
║    python3 bin/lh_ultimate_feed.py --export report.json          ║
╚══════════════════════════════════════════════════════════════════╝
"""

import json
import uuid
import hashlib
import datetime
import re
import os
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any, Set
from dataclasses import dataclass, field, asdict
from enum import Enum
import argparse
import difflib

# ============================================================
# 〇、常量 & 路径
# ============================================================

DATA_DIR = Path.home() / ".longhun" / "feed"
DATA_DIR.mkdir(parents=True, exist_ok=True)
CONTENT_POOL_PATH = DATA_DIR / "content_pool.json"
CREATIVITY_POOL_PATH = DATA_DIR / "creativity_pool.json"
HISTORY_PATH = DATA_DIR / "feed_history.json"
STATE_PATH = DATA_DIR / "feed_state.json"

# ============================================================
# 一、数据结构
# ============================================================

class 内容状态(Enum):
    保留 = "🟢 保留"
    合并 = "🟡 已合并"
    覆盖 = "🟠 已覆盖"
    冻结 = "🔴 已冻结"
    创意池 = "💡 创意池"
    待审核 = "⏳ 待审核"

class 内容类型(Enum):
    文档 = "📄 文档"
    代码 = "💻 代码"
    知识库 = "📚 知识库"
    规则 = "📜 规则"
    协议 = "🤝 协议"
    配置 = "⚙️ 配置"
    对话 = "💬 对话"
    创意 = "🎨 创意"
    未知 = "❓ 未知"

class 命中类型(Enum):
    模板 = "📋 模板"
    记忆量子 = "🧠 记忆量子"
    系统规则 = "📜 系统规则"
    索引节点 = "🧭 索引节点"
    人格路由 = "👤 人格路由"
    引擎调用 = "⚡ 引擎调用"
    未命中 = "❌ 未命中"

class 来源类型(Enum):
    国内 = "🇨🇳 国内"
    国外 = "🌐 国外"
    AI生成 = "🤖 AI生成"
    用户输入 = "👤 用户输入"
    系统产出 = "⚙️ 系统产出"

@dataclass
class 内容标签:
    """内容标签"""
    主标签: str = ""
    子标签: List[str] = field(default_factory=list)
    领域: Optional[str] = None
    优先级: str = "P3"  # P0/P1/P2/P3
    关联人格: List[str] = field(default_factory=list)

@dataclass
class 内容单元:
    """内容单元 — 完整字段"""
    id: str
    内容: str
    标题: str = ""
    来源: str = "Lucky"
    来源类型: 来源类型 = 来源类型.用户输入
    内容类型: 内容类型 = 内容类型.未知
    语义指纹: str = ""
    状态: 内容状态 = 内容状态.保留
    命中类型: Optional[命中类型] = None
    命中置信度: float = 0.0
    标签: 内容标签 = field(default_factory=内容标签)
    dna: str = ""
    版本: str = "v1.0"
    质量分: float = 0.0
    字数: int = 0
    被合并到: Optional[str] = None
    被覆盖到: Optional[str] = None
    创建时间: str = field(default_factory=lambda: datetime.datetime.now().isoformat())
    更新时间: str = field(default_factory=lambda: datetime.datetime.now().isoformat())
    页面模板: Optional[str] = None  # 文档/代码/知识库 展示模板

@dataclass
class 优化报告:
    """优化报告"""
    报告ID: str
    原始内容数: int
    处理后内容数: int
    合并数量: int
    覆盖数量: int
    冻结数量: int
    创意池数量: int
    命中数量: int
    未命中数量: int
    按类型统计: Dict[str, int] = field(default_factory=dict)
    按来源统计: Dict[str, int] = field(default_factory=dict)
    系统评估: str = ""
    时间戳: str = field(default_factory=lambda: datetime.datetime.now().isoformat())
    dna: str = ""


# ============================================================
# 二、语义指纹生成器
# ============================================================

class 语义指纹:
    """生成内容的语义指纹（去重 + 匹配 + 分类依据）"""

    @staticmethod
    def 生成(内容: str) -> str:
        """生成语义指纹"""
        清理 = re.sub(r'[\s，。、；：！？""''（）\\(\\)\\[\\]【】]', '', 内容)
        清理 = 清理.lower()
        词 = re.findall(r'[\u4e00-\u9fa5a-zA-Z][\u4e00-\u9fa5a-zA-Z]*', 清理)
        关键词 = sorted(set(词))[:15]
        hash_val = hashlib.md5("".join(关键词).encode()).hexdigest()[:12]
        return f"FP-{hash_val}"

    @staticmethod
    def 相似度(内容1: str, 内容2: str) -> float:
        """计算相似度"""
        清理1 = re.sub(r'[\s，。、；：！？""''（）\\(\\)\\[\\]【】]', '', 内容1)
        清理2 = re.sub(r'[\s，。、；：！？""''（）\\(\\)\\[\\]【】]', '', 内容2)
        if not 清理1 or not 清理2:
            return 0.0
        return difflib.SequenceMatcher(None, 清理1, 清理2).ratio()


# ============================================================
# 三、内容分类器 — 自动识别 文档/代码/知识库/规则/协议/配置
# ============================================================

class 内容分类器:
    """自动识别内容类型 + 打标签"""

    # 类型识别特征（关键词 + 权重）
    类型特征 = {
        内容类型.代码: {
            "关键词": ["def ", "class ", "import ", "function", "return", "if __", "#!/usr",
                     "console.log", "const ", "let ", "var ", "async ", "await ", "```python",
                     "```javascript", "```js", "```bash", "#include", "package.json",
                     "CNSH", "python", "script", "函数", "算法", "模块", "引擎"],
            "模式": [r'```\w+', r'def\s+\w+\s*\(', r'class\s+\w+', r'import\s+\w+',
                    r'const\s+\w+\s*=', r'function\s+\w+\s*\('],
            "权重": 1.3
        },
        内容类型.规则: {
            "关键词": ["规则", "铁律", "必须", "禁止", "允许", "P0", "P1", "天条", "熔断",
                     "审计", "焊死", "不可", "红线", "底线", "原则", "constitution"],
            "模式": [r'[0-9]+\..*必须', r'[0-9]+\..*禁止', r'第[一二三四五六七八九十]条'],
            "权重": 1.2
        },
        内容类型.协议: {
            "关键词": ["协议", "授权", "签署", "同意", "CC BY", "GPL", "MIT", "Apache",
                     "NC-SA", "ND", "LICENSE", "版权", "署名", "procotol", "covenant"],
            "模式": [r'CC\s+BY', r'GPL\s*v', r'MIT\s+License', r'协议', r'Protocol'],
            "权重": 1.4
        },
        内容类型.配置: {
            "关键词": ["config", "配置", "端口", "host", "port", "token", "key", "secret",
                     "password", "username", "database", "redis", "mysql", "env", "环境变量"],
            "模式": [r'^\s*[A-Z_]+\s*=', r'^\s*\{', r'^\s*\[', r'"\w+":\s*"'],
            "权重": 0.9
        },
        内容类型.知识库: {
            "关键词": ["知识", "概念", "定义", "术语", "解释", "原理", "理论", "框架",
                     "体系", "架构", "设计", "模式", "paradigm", "taxonomy", "百科"],
            "模式": [r'什么是', r'.*的定义', r'.*分为.*类', r'.*包括.*方面'],
            "权重": 1.0
        },
        内容类型.文档: {
            "关键词": ["文档", "说明", "指南", "手册", "教程", "使用", "安装", "部署",
                     "README", "CHANGELOG", "FAQ", "how to", "guide", "概述", "背景"],
            "模式": [r'#{1,3}\s+', r'^\d+\.\s+\*\*', r'###.*\n'],
            "权重": 1.0
        },
        内容类型.对话: {
            "关键词": ["你好", "谢谢", "请帮我", "帮我", "我想", "我觉得", "问一下",
                     "怎么样", "能不能", "可以吗", "好吗", "怎么样"],
            "模式": [r'^你', r'^我', r'[？?]$', r'请帮我'],
            "权重": 0.8
        },
        内容类型.创意: {
            "关键词": ["创意", "灵感", "想法", "点子", "脑洞", "想象", "比喻", "类比",
                     "创新", "方案", "构思", "设计思路", "草图", "原型"],
            "模式": [r'如果.*可以', r'假设', r'想象一下', r'有没有可能'],
            "权重": 0.9
        }
    }

    # 标签分类体系
    标签体系 = {
        "技术类": ["AI", "ML", "Python", "JavaScript", "CNSH", "算法", "数据结构",
                  "网络", "安全", "加密", "数据库", "前端", "后端", "部署", "运维"],
        "系统类": ["龍魂", "人格", "引擎", "DNA", "审计", "熔断", "量子", "路由",
                  "索引", "归档", "签名", "GPG"],
        "领域类": ["数学", "哲学", "易经", "三才", "369洛书", "五行", "八卦",
                  "密码学", "语义学", "博弈论"],
        "业务类": ["文档", "代码", "知识库", "规则", "协议", "配置", "部署",
                  "安全", "测试", "监控"],
        "来源类": ["国内", "国外", "AI生成", "人工编写", "自动生成"]
    }

    @classmethod
    def 分类(cls, 内容: str, 来源类型: 来源类型 = 来源类型.用户输入) -> Tuple[内容类型, float, 内容标签]:
        """自动分类内容 + 打标签"""
        得分 = {}
        for 类型, 特征 in cls.类型特征.items():
            分 = 0.0
            for 关键词 in 特征["关键词"]:
                if 关键词.lower() in 内容.lower():
                    分 += 1.0
            for 模式 in 特征["模式"]:
                if re.search(模式, 内容, re.IGNORECASE):
                    分 += 1.5
            得分[类型] = 分 * 特征["权重"]

        if not 得分 or max(得分.values()) == 0:
            return 内容类型.未知, 0.0, 内容标签(主标签="未分类")

        最佳类型 = max(得分, key=得分.get)
        最高分 = 得分[最佳类型]
        总匹配分 = sum(得分.values())
        置信度 = min(最高分 / max(1, 总匹配分) * 2, 1.0) if 总匹配分 > 0 else 0.0

        # 生成标签
        标签 = cls._打标签(内容, 最佳类型, 来源类型)

        return 最佳类型, round(置信度, 2), 标签

    @classmethod
    def _打标签(cls, 内容: str, 类型: 内容类型, 来源类型: 来源类型) -> 内容标签:
        """自动打标签"""
        标签列表 = []
        for 大类, 标签集 in cls.标签体系.items():
            for 标 in 标签集:
                if 标.lower() in 内容.lower():
                    标签列表.append(标)

        # 主标签 = 内容类型的中文名
        主标签 = 类型.value

        # 优先级判定
        优先级 = "P3"
        if any(词 in 内容 for 词 in ["P0", "天条", "焊死", "不可修改", "熔断", "∞"]):
            优先级 = "P0"
        elif any(词 in 内容 for 词 in ["P1", "铁律", "红线", "底线", "必须"]):
            优先级 = "P1"
        elif any(词 in 内容 for 词 in ["P2", "重要", "关键", "建议"]):
            优先级 = "P2"

        # 关联人格
        人格映射 = {
            "审计": "P05", "安全": "P05/P77", "推演": "P01", "代码": "P04",
            "文档": "P03", "命名": "P08", "通信": "P10", "创意": "P11",
            "底线": "P12", "权限": "P13", "部署": "P14", "签章": "P15",
            "熔断": "P72", "引擎": "P04", "算法": "P06"
        }
        关联人格 = []
        for 关键词, 人格 in 人格映射.items():
            if 关键词 in 内容:
                if 人格 not in 关联人格:
                    关联人格.append(人格)

        return 内容标签(
            主标签=主标签,
            子标签=标签列表[:8],
            优先级=优先级,
            关联人格=关联人格[:5]
        )

    @classmethod
    def 提取标题(cls, 内容: str) -> str:
        """自动提取标题"""
        # 尝试匹配 Markdown 标题
        m = re.search(r'^#+\s+(.+)$', 内容, re.MULTILINE)
        if m:
            return m.group(1).strip()[:80]

        # 尝试匹配第一句话
        m = re.search(r'^(.+?)[。．.，,\n]', 内容)
        if m:
            t = m.group(1).strip()
            return t[:80] if len(t) > 5 else 内容[:80]

        return 内容[:80]


# ============================================================
# 四、质量评分器
# ============================================================

class 质量评分器:
    """五维内容质量评分"""

    @staticmethod
    def 评分(单元: 内容单元, 全池: List[内容单元]) -> float:
        """五维评分：完整度 + 可执行度 + 新鲜度 + 引用率 + 去重度"""
        分数 = 0.0

        # 1. 完整度 (0-25)：字数、结构完整性
        字数 = len(单元.内容)
        if 字数 > 500:
            分数 += 25
        elif 字数 > 200:
            分数 += 20
        elif 字数 > 50:
            分数 += 15
        elif 字数 > 10:
            分数 += 8
        else:
            分数 += 3

        # 2. 可执行度 (0-25)：是否含代码/步骤/具体方案
        可执行特征 = ["步骤", "方法", "方案", "代码", "命令", "操作", "配置",
                   "def ", "import ", "#!/", "python", "bash", "curl"]
        匹配数 = sum(1 for f in 可执行特征 if f.lower() in 单元.内容.lower())
        分数 += min(25, 匹配数 * 5)

        # 3. 新鲜度 (0-20)：是否最近创建/更新
        try:
            t = datetime.datetime.fromisoformat(单元.创建时间)
            days_old = max(0, (datetime.datetime.now() - t).days)
            if days_old < 1:
                分数 += 20
            elif days_old < 7:
                分数 += 15
            elif days_old < 30:
                分数 += 10
            else:
                分数 += 5
        except:
            分数 += 10

        # 4. 引用率 (0-15)：是否引用了系统组件
        引用词 = ["DNA", "GPG", "CNSH", "龙魂", "人格", "引擎", "协议", "361",
                "369", "UID9622", "鲲鹏", "龍芯"]
        分数 += min(15, sum(1 for r in 引用词 if r in 单元.内容) * 2)

        # 5. 去重度 (0-15)：如果相似内容少则高分
        重复数 = 0
        for other in 全池:
            if other.id != 单元.id and 语义指纹.相似度(单元.内容, other.内容) > 0.7:
                重复数 += 1
        分数 += max(0, 15 - 重复数 * 5)

        单元.质量分 = round(分数, 1)
        return 单元.质量分


# ============================================================
# 五、页面结构生成器 — 文档/代码/知识库统一展示模板
# ============================================================

class 页面结构:
    """为不同内容类型生成统一的页面结构模板"""

    模板 = {
        内容类型.文档: {
            "区块": ["标题", "概述", "背景", "核心内容", "关键要点", "操作步骤", "注意事项", "关联资源", "版本记录"],
            "样式": "document-page",
            "图标": "📄",
            "排序权重": 2
        },
        内容类型.代码: {
            "区块": ["标题", "功能说明", "输入输出", "核心逻辑", "代码块", "使用示例", "依赖说明", "DNA/签名"],
            "样式": "code-page",
            "图标": "💻",
            "排序权重": 1
        },
        内容类型.知识库: {
            "区块": ["标题", "定义", "分类", "详细说明", "应用场景", "关联概念", "参考资料"],
            "样式": "knowledge-page",
            "图标": "📚",
            "排序权重": 3
        },
        内容类型.规则: {
            "区块": ["标题", "规则编号", "适用范围", "规则正文", "例外情况", "生效日期", "修订记录"],
            "样式": "rule-page",
            "图标": "📜",
            "排序权重": 0
        },
        内容类型.协议: {
            "区块": ["标题", "协议编号", "签署方", "核心条款", "权利与义务", "生效条件", "终止条件", "签署记录"],
            "样式": "protocol-page",
            "图标": "🤝",
            "排序权重": 0
        },
        内容类型.配置: {
            "区块": ["标题", "配置项", "默认值", "说明", "环境差异", "安全标注", "修改记录"],
            "样式": "config-page",
            "图标": "⚙️",
            "排序权重": 1
        },
        内容类型.对话: {
            "区块": ["对话标题", "参与方", "核心议题", "关键结论", "待办事项", "跟进状态"],
            "样式": "conversation-page",
            "图标": "💬",
            "排序权重": 4
        },
        内容类型.创意: {
            "区块": ["标题", "创意来源", "核心概念", "可行性评估", "落地路径", "关联创意"],
            "样式": "creativity-page",
            "图标": "🎨",
            "排序权重": 5
        },
        内容类型.未知: {
            "区块": ["标题", "原始内容", "自动分类建议"],
            "样式": "unknown-page",
            "图标": "❓",
            "排序权重": 5
        }
    }

    @classmethod
    def 生成(cls, 单元: 内容单元) -> Dict:
        """为内容单元生成页面结构"""
        模板 = cls.模板.get(单元.内容类型, cls.模板[内容类型.未知])
        return {
            "页面ID": f"PAGE-{单元.id}",
            "标题": 单元.标题 or 内容分类器.提取标题(单元.内容),
            "图标": 模板["图标"],
            "样式": 模板["样式"],
            "类型": 单元.内容类型.value,
            "区块": 模板["区块"],
            "标签": {
                "主标签": 单元.标签.主标签,
                "子标签": 单元.标签.子标签,
                "优先级": 单元.标签.优先级,
                "关联人格": 单元.标签.关联人格
            },
            "状态": 单元.状态.value,
            "质量分": 单元.质量分,
            "版本": 单元.版本,
            "DNA": 单元.dna,
            "排序权重": 模板["排序权重"],
            "时间": 单元.更新时间
        }


# ============================================================
# 六、内容池管理器（持久化）
# ============================================================

class 内容池管理器:
    """管理所有内容单元·文件持久化"""

    def __init__(self):
        self.内容池: List[内容单元] = []
        self.创意池: List[内容单元] = []
        self.历史记录: List[Dict] = []
        self._从文件加载()

    def _从文件加载(self):
        """从磁盘加载持久化数据"""
        try:
            if CONTENT_POOL_PATH.exists():
                raw = json.loads(CONTENT_POOL_PATH.read_text(encoding='utf-8'))
                self.内容池 = [self._字典转单元(d) for d in raw]
        except Exception:
            pass
        try:
            if CREATIVITY_POOL_PATH.exists():
                raw = json.loads(CREATIVITY_POOL_PATH.read_text(encoding='utf-8'))
                self.创意池 = [self._字典转单元(d) for d in raw]
        except Exception:
            pass
        try:
            if HISTORY_PATH.exists():
                self.历史记录 = json.loads(HISTORY_PATH.read_text(encoding='utf-8'))
        except Exception:
            pass

    def _保存(self):
        """持久化到磁盘"""
        try:
            CONTENT_POOL_PATH.write_text(
                json.dumps([self._单元转字典(u) for u in self.内容池],
                          ensure_ascii=False, indent=2),
                encoding='utf-8')
            CREATIVITY_POOL_PATH.write_text(
                json.dumps([self._单元转字典(u) for u in self.创意池],
                          ensure_ascii=False, indent=2),
                encoding='utf-8')
            HISTORY_PATH.write_text(
                json.dumps(self.历史记录[-500:], ensure_ascii=False, indent=2),
                encoding='utf-8')
        except Exception:
            pass

    def _单元转字典(self, u: 内容单元) -> Dict:
        d = asdict(u)
        d['来源类型'] = d['来源类型'].value if isinstance(u.来源类型, 来源类型) else d['来源类型']
        d['内容类型'] = d['内容类型'].value if isinstance(u.内容类型, 内容类型) else d['内容类型']
        d['状态'] = d['状态'].value if isinstance(u.状态, 内容状态) else d['状态']
        d['命中类型'] = d['命中类型'].value if isinstance(u.命中类型, 命中类型) and u.命中类型 else None
        return d

    def _字典转单元(self, d: Dict) -> 内容单元:
        try:
            # 枚举还原
            st = d.get('状态', '🟢 保留')
            d['状态'] = next((s for s in 内容状态 if s.value == st), 内容状态.保留)
            ct = d.get('内容类型', '❓ 未知')
            d['内容类型'] = next((c for c in 内容类型 if c.value == ct), 内容类型.未知)
            ht = d.get('命中类型')
            if ht:
                d['命中类型'] = next((h for h in 命中类型 if h.value == ht), None)
            ft = d.get('来源类型', '👤 用户输入')
            d['来源类型'] = next((s for s in 来源类型 if s.value == ft), 来源类型.用户输入)
            # 标签 dataclass 还原
            if isinstance(d.get('标签'), dict):
                d['标签'] = 内容标签(**d['标签'])
            return 内容单元(**{k: v for k, v in d.items() if k in 内容单元.__dataclass_fields__})
        except Exception:
            return 内容单元(id=d.get('id', ''), 内容=d.get('内容', ''))

    def 添加(self, 内容: str, 来源: str = "Lucky",
             来源类型: 来源类型 = 来源类型.用户输入) -> 内容单元:
        """添加新内容 · 自动分类 + 打标签 + 提取标题"""
        类型, 置信度, 标签 = 内容分类器.分类(内容, 来源类型)
        标题 = 内容分类器.提取标题(内容)

        单元 = 内容单元(
            id=f"CONT-{uuid.uuid4().hex[:8].upper()}",
            内容=内容,
            标题=标题,
            来源=来源,
            来源类型=来源类型,
            内容类型=类型,
            语义指纹=语义指纹.生成(内容),
            状态=内容状态.保留,
            标签=标签,
            dna=f"#龍芯⚡️{datetime.datetime.now().strftime('%Y-%m-%d')}-FEED-{uuid.uuid4().hex[:6].upper()}",
            版本="v1.0",
            字数=len(内容)
        )
        # 评分
        质量评分器.评分(单元, self.内容池)
        # 生成页面结构
        单元.页面模板 = json.dumps(页面结构.生成(单元), ensure_ascii=False)

        self.内容池.append(单元)
        self._保存()
        return 单元

    def 查找相似(self, 内容: str, 阈值: float = 0.75) -> List[Tuple[float, 内容单元]]:
        """查找相似内容"""
        结果 = []
        for 单元 in self.内容池:
            if 单元.状态 in [内容状态.冻结, 内容状态.创意池]:
                continue
            相似度 = 语义指纹.相似度(内容, 单元.内容)
            if 相似度 >= 阈值:
                结果.append((相似度, 单元))
        结果.sort(key=lambda x: x[0], reverse=True)
        return 结果

    def 合并(self, 主单元: 内容单元, 从单元: 内容单元) -> bool:
        """合并两个内容单元"""
        if 从单元.状态 in [内容状态.合并, 内容状态.冻结, 内容状态.创意池]:
            return False

        从单元.状态 = 内容状态.合并
        从单元.被合并到 = 主单元.id
        从单元.更新时间 = datetime.datetime.now().isoformat()

        # 智能合并：取更丰富的表达
        if len(主单元.内容) < len(从单元.内容) and 从单元.内容 not in 主单元.内容:
            主单元.内容 = 主单元.内容 + "\n\n" + 从单元.内容
        主单元.更新时间 = datetime.datetime.now().isoformat()

        self._记录("合并", 主单元.id, 从单元.id)
        self._保存()
        return True

    def 覆盖(self, 旧单元: 内容单元, 新单元: 内容单元) -> bool:
        """覆盖旧内容"""
        if 旧单元.状态 in [内容状态.合并, 内容状态.冻结, 内容状态.创意池]:
            return False

        旧单元.内容 = 新单元.内容
        旧单元.版本 = f"v{round(float(旧单元.版本.replace('v', '')) + 0.1, 1)}"
        旧单元.状态 = 内容状态.覆盖
        旧单元.被覆盖到 = 新单元.id
        旧单元.更新时间 = datetime.datetime.now().isoformat()

        self._记录("覆盖", 旧单元.id, 新单元.id)
        self._保存()
        return True

    def 冻结(self, 单元: 内容单元) -> bool:
        if 单元.状态 in [内容状态.合并, 内容状态.冻结, 内容状态.创意池]:
            return False
        单元.状态 = 内容状态.冻结
        单元.更新时间 = datetime.datetime.now().isoformat()
        self._记录("冻结", 单元.id)
        self._保存()
        return True

    def 移入创意池(self, 单元: 内容单元) -> bool:
        if 单元.状态 in [内容状态.合并, 内容状态.冻结, 内容状态.创意池]:
            return False
        单元.状态 = 内容状态.创意池
        单元.更新时间 = datetime.datetime.now().isoformat()
        self.创意池.append(单元)
        self.内容池.remove(单元)
        self._记录("创意池", 单元.id)
        self._保存()
        return True

    def _记录(self, 操作: str, *相关IDs: str):
        self.历史记录.append({
            "操作": 操作,
            "相关": list(相关IDs),
            "时间": datetime.datetime.now().isoformat()
        })

    def 统计(self) -> Dict:
        状态统计 = {}
        for 单元 in self.内容池:
            s = 单元.状态.value
            状态统计[s] = 状态统计.get(s, 0) + 1

        类型统计 = {}
        for 单元 in self.内容池 + self.创意池:
            t = 单元.内容类型.value
            类型统计[t] = 类型统计.get(t, 0) + 1

        来源统计 = {}
        for 单元 in self.内容池 + self.创意池:
            f = 单元.来源类型.value
            来源统计[f] = 来源统计.get(f, 0) + 1

        return {
            "总内容": len(self.内容池) + len(self.创意池),
            "活跃": len(self.内容池),
            "创意池": len(self.创意池),
            "状态分布": 状态统计,
            "类型分布": 类型统计,
            "来源分布": 来源统计,
            "历史操作": len(self.历史记录)
        }


# ============================================================
# 七、执行流对齐器（增强版）
# ============================================================

class 执行流对齐器:
    """判断内容是否能命中系统组件"""

    命中规则 = {
        命中类型.模板: {
            "关键词": ["模板", "套用", "格式", "标准", "可复用", "调用", "pattern", "template"],
            "权重": 1.0,
            "说明": "可匹配到系统模板"
        },
        命中类型.记忆量子: {
            "关键词": ["记忆", "经验", "习惯", "历史", "曾经", "之前", "过去", "积累"],
            "权重": 0.9,
            "说明": "可接入量子记忆"
        },
        命中类型.系统规则: {
            "关键词": ["规则", "铁律", "协议", "必须", "禁止", "允许", "P0", "P1",
                     "熔断", "天条", "不能", "不可"],
            "权重": 1.2,
            "说明": "触发系统规则"
        },
        命中类型.索引节点: {
            "关键词": ["索引", "定位", "追溯", "查找", "链接", "锚点", "导航", "路径"],
            "权重": 0.8,
            "说明": "可挂载到索引节点"
        },
        命中类型.人格路由: {
            "关键词": ["人格", "角色", "诸葛亮", "宝宝", "雯雯", "鲁班", "上帝之眼",
                     "审判长", "仓颉", "姜子牙", "乔前辈", "龙盾", "黑天使"],
            "权重": 1.1,
            "说明": "触发人格路由"
        },
        命中类型.引擎调用: {
            "关键词": ["引擎", "engine", "engine.py", "计算", "分析", "处理",
                     "推演", "审计", "扫描", "检测", "生成"],
            "权重": 1.0,
            "说明": "可调用龙魂引擎"
        }
    }

    @classmethod
    def 对齐(cls, 内容: str) -> Tuple[命中类型, float, List[str]]:
        """判断内容命中的类型、置信度和命中组件"""
        all_hits = []

        for 类型, 规则 in cls.命中规则.items():
            匹配数 = sum(1 for 词 in 规则["关键词"] if 词.lower() in 内容.lower())
            if 匹配数 > 0:
                score = (匹配数 / max(1, len(规则["关键词"]))) * 规则["权重"]
                all_hits.append((类型, score))

        if not all_hits:
            return 命中类型.未命中, 0.0, []

        # 按总分排序
        all_hits.sort(key=lambda x: x[1], reverse=True)
        最佳类型, 最佳分 = all_hits[0]

        命中组件 = [
            f"{t.value}: {cls.命中规则[t]['说明']}"
            for t, s in all_hits[:3] if s > 0.15
        ]

        return 最佳类型, round(最佳分, 2), 命中组件


# ============================================================
# 八、目录导入器
# ============================================================

class 目录导入器:
    """从目录批量导入 文档/代码/知识库 文件"""

    支持扩展名 = {
        '.md': 内容类型.文档, '.txt': 内容类型.文档,
        '.py': 内容类型.代码, '.js': 内容类型.代码,
        '.ts': 内容类型.代码, '.sh': 内容类型.代码,
        '.cs': 内容类型.代码, '.java': 内容类型.代码,
        '.go': 内容类型.代码, '.rs': 内容类型.代码,
        '.json': 内容类型.配置, '.yaml': 内容类型.配置,
        '.yml': 内容类型.配置, '.toml': 内容类型.配置,
        '.html': 内容类型.文档, '.css': 内容类型.文档,
        '.cnsh': 内容类型.代码
    }

    排除目录 = {'.git', '__pycache__', 'node_modules', '.venv', 'venv',
              '.codebuddy', 'archive', 'models', 'dist', 'logs', '.DS_Store'}

    @classmethod
    def 导入(cls, 目录: str, 最大文件数: int = 200) -> List[Tuple[str, str, 内容类型]]:
        """从目录递归导入文件 · 返回 (文件路径, 内容, 类型)"""
        结果 = []
        计数 = 0

        for root, dirs, files in os.walk(目录):
            # 排除目录
            dirs[:] = [d for d in dirs if d not in cls.排除目录 and not d.startswith('.')]

            for fname in files:
                if 计数 >= 最大文件数:
                    break
                ext = os.path.splitext(fname)[1].lower()
                if ext not in cls.支持扩展名:
                    continue

                fpath = os.path.join(root, fname)
                try:
                    内容 = Path(fpath).read_text(encoding='utf-8', errors='ignore')
                    if len(内容.strip()) < 5:
                        continue
                    类型 = cls.支持扩展名[ext]
                    结果.append((fpath, 内容, 类型))
                    计数 += 1
                except Exception:
                    pass

        return 结果


# ============================================================
# 九、终极投喂引擎（主控）
# ============================================================

class 终极投喂引擎:
    """龙魂终极投喂引擎 — 做减法，不做加法"""

    def __init__(self):
        self.内容池 = 内容池管理器()
        self.对齐器 = 执行流对齐器()
        self.处理历史: List[Dict] = []

    def 投喂(self, 内容列表: List[str], 来源: str = "Lucky",
             来源类型: 来源类型 = 来源类型.用户输入) -> 优化报告:
        """
        终极投喂全流程：
        分类 → 相似查找 → 合并/覆盖 → 对齐判断 → 创意池筛选 → 冻结无效
        → 国内/国外融合去重 → 质量评分 → 页面结构 → 报告
        """
        报告 = {"原始": len(内容列表), "合并": 0, "覆盖": 0, "冻结": 0,
                "创意池": 0, "命中": 0, "未命中": 0, "最终": 0,
                "新增": 0}

        for 内容 in 内容列表:
            if not 内容.strip():
                continue

            # 1. 查找相似内容
            相似 = self.内容池.查找相似(内容, 阈值=0.7)

            if 相似:
                最佳相似度, 主单元 = 相似[0]
                if 最佳相似度 > 0.90:
                    # 高度相似 → 覆盖（新版本替换旧版本）
                    临时单元 = 内容单元(
                        id=f"TEMP-{uuid.uuid4().hex[:8].upper()}",
                        内容=内容,
                        来源=来源,
                        来源类型=来源类型,
                        内容类型=主单元.内容类型,
                        语义指纹=语义指纹.生成(内容),
                        状态=内容状态.覆盖
                    )
                    if self.内容池.覆盖(主单元, 临时单元):
                        报告["覆盖"] += 1
                        报告["合并"] += 1
                        continue
                elif 最佳相似度 > 0.70:
                    # 中度相似 → 直接合并（内容补充到主单元）
                    从单元 = 内容单元(
                        id=f"MG-{uuid.uuid4().hex[:8].upper()}",
                        内容=内容,
                        来源=来源,
                        来源类型=来源类型,
                        内容类型=主单元.内容类型,
                        语义指纹=语义指纹.生成(内容),
                        状态=内容状态.保留
                    )
                    if self.内容池.合并(主单元, 从单元):
                        报告["合并"] += 1
                    continue
                else:
                    新单元 = self.内容池.添加(内容, 来源, 来源类型)
            else:
                新单元 = self.内容池.添加(内容, 来源, 来源类型)

            报告["新增"] += 1

            # 2. 对齐判断
            命中类型, 置信度, 命中组件 = self.对齐器.对齐(内容)
            新单元.命中类型 = 命中类型
            新单元.命中置信度 = 置信度

            if 命中类型 != 命中类型.未命中 and 置信度 > 0.15:
                报告["命中"] += 1
            else:
                报告["未命中"] += 1

            # 3. 判断是否移入创意池（未命中 + 内容过短）
            if 命中类型 == 命中类型.未命中 and len(内容) < 20:
                if self.内容池.移入创意池(新单元):
                    报告["创意池"] += 1
                    continue

            # 4. 冻结判定
            冻结词 = ["删除", "清除", "移除", "废弃", "淘汰", "作废"]
            if any(词 in 内容 for 词 in 冻结词):
                if self.内容池.冻结(新单元):
                    报告["冻结"] += 1

            # 5. 补全页面结构（已完成在添加时）

        # 6. 融合多源内容去重
        报告["合并"] += self._融合多源内容()

        # 7. 生成最终统计
        统计 = self.内容池.统计()
        报告["最终"] = 统计["活跃"]

        # 8. 类型/来源统计
        类型统计 = 统计.get("类型分布", {})
        来源统计 = 统计.get("来源分布", {})

        return 优化报告(
            报告ID=f"RPT-{uuid.uuid4().hex[:8].upper()}",
            原始内容数=报告["原始"],
            处理后内容数=报告["最终"],
            合并数量=报告["合并"],
            覆盖数量=报告["覆盖"],
            冻结数量=报告["冻结"],
            创意池数量=报告["创意池"],
            命中数量=报告["命中"],
            未命中数量=报告["未命中"],
            按类型统计=类型统计,
            按来源统计=来源统计,
            系统评估=self._生成评估(报告),
            时间戳=datetime.datetime.now().isoformat(),
            dna=f"#龍芯⚡️{datetime.datetime.now().strftime('%Y-%m-%d')}-FEED-RPT-{uuid.uuid4().hex[:6].upper()}"
        )

    def 从文件投喂(self, 文件路径: str) -> 优化报告:
        """从文件读取内容投喂"""
        with open(文件路径, 'r', encoding='utf-8') as f:
            内容 = f.read()
        内容列表 = [line.strip() for line in 内容.split('\n') if line.strip()]
        return self.投喂(内容列表, 来源=文件路径, 来源类型=来源类型.用户输入)

    def 从目录投喂(self, 目录: str, 最大文件数: int = 200) -> 优化报告:
        """从目录批量导入文件投喂"""
        files = 目录导入器.导入(目录, 最大文件数)
        内容列表 = [f"[{fp}]\n{内容}" for fp, 内容, _ in files]
        return self.投喂(内容列表, 来源=目录, 来源类型=来源类型.系统产出)

    def _融合多源内容(self) -> int:
        """融合国内/国外内容去重"""
        合并数 = 0
        指纹分组: Dict[str, List[内容单元]] = {}
        for 单元 in self.内容池.内容池:
            if 单元.状态 in [内容状态.合并, 内容状态.冻结, 内容状态.创意池]:
                continue
            fp = 单元.语义指纹
            if fp not in 指纹分组:
                指纹分组[fp] = []
            指纹分组[fp].append(单元)

        for fp, 组 in 指纹分组.items():
            if len(组) > 1:
                # 按优先级：国内 > AI生成 > 国外
                优先 = {来源类型.国内: 3, 来源类型.系统产出: 2,
                      来源类型.AI生成: 1, 来源类型.用户输入: 1, 来源类型.国外: 0}
                组.sort(key=lambda x: (优先.get(x.来源类型, 0), len(x.内容)),
                        reverse=True)
                主单元 = 组[0]
                for i in range(1, len(组)):
                    if self.内容池.合并(主单元, 组[i]):
                        合并数 += 1

        return 合并数

    def _生成评估(self, 报告: Dict) -> str:
        """生成系统评估"""
        原始 = 报告["原始"]
        最终 = 报告["最终"]
        合并 = 报告["合并"]
        覆盖 = 报告["覆盖"]
        命中 = 报告["命中"]
        未命中 = 报告["未命中"]

        if 最终 == 0 and 原始 > 0:
            return "⚠️ 所有内容已移入创意池或冻结，系统需要新的有效输入"
        if 原始 == 最终 and 合并 == 0:
            return "🟡 内容数量未减少，建议手动审查是否有重复项"
        if 最终 < 原始 * 0.5:
            return "🟢 系统显著精简，运行效率提升 (精简率>50%)"
        if 合并 > 0 or 覆盖 > 0:
            return f"🟢 已合并{合并}项·覆盖{覆盖}项，系统更紧凑"
        if 未命中 > 命中:
            return "🟡 大量内容未命中系统组件，建议补充结构信息"
        return "🟢 内容已优化，系统更清晰"

    def 获取状态(self) -> Dict:
        统计 = self.内容池.统计()
        return {
            "内容池": 统计,
            "命中率": f"{sum(1 for u in self.内容池.内容池 if u.命中类型 and u.命中类型 != 命中类型.未命中)}/{len(self.内容池.内容池)}",
            "平均质量分": round(
                sum(u.质量分 for u in self.内容池.内容池) / max(1, len(self.内容池.内容池)), 1
            ),
            "数据目录": str(DATA_DIR)
        }

    @staticmethod
    def _序列化单元(u: 内容单元) -> Dict:
        """安全序列化内容单元（Enum → str）"""
        d = {}
        for k, v in asdict(u).items():
            if isinstance(v, Enum):
                d[k] = v.value
            elif hasattr(v, 'value') and hasattr(v, '__class__') and issubclass(type(v), Enum):
                d[k] = v.value
            else:
                d[k] = v
        return d

    def 导出(self, 文件路径: str):
        """导出内容池为JSON"""
        data = {
            "内容池": [self._序列化单元(u) for u in self.内容池.内容池],
            "创意池": [self._序列化单元(u) for u in self.内容池.创意池],
            "统计": self.内容池.统计(),
            "导出时间": datetime.datetime.now().isoformat()
        }
        Path(文件路径).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')

    def 按类型查询(self, 类型: 内容类型) -> List[内容单元]:
        return [u for u in self.内容池.内容池 if u.内容类型 == 类型 and u.状态 == 内容状态.保留]

    def 按标签查询(self, 标签词: str) -> List[内容单元]:
        return [u for u in self.内容池.内容池
                if 标签词 in u.标签.子标签 or 标签词 == u.标签.主标签]


# ============================================================
# 十、页面结构审查器（自动补全缺失区块）
# ============================================================

class 页面结构审查器:
    """审查内容池中所有单元的页面结构，自动补全缺失区块"""

    @classmethod
    def 审查(cls, engine: 终极投喂引擎) -> Dict:
        """全量审查 + 补全"""
        结果 = {"总数": 0, "已补全": 0, "已更新": 0, "无页面结构": 0}

        for 单元 in engine.内容池.内容池:
            结果["总数"] += 1
            if not 单元.页面模板:
                单元.页面模板 = json.dumps(页面结构.生成(单元), ensure_ascii=False)
                结果["无页面结构"] += 1
            else:
                # 检查是否需要更新（内容类型变更）
                try:
                    旧页面 = json.loads(单元.页面模板)
                    if 旧页面.get("类型") != 单元.内容类型.value:
                        单元.页面模板 = json.dumps(页面结构.生成(单元), ensure_ascii=False)
                        结果["已更新"] += 1
                except Exception:
                    单元.页面模板 = json.dumps(页面结构.生成(单元), ensure_ascii=False)
                    结果["已补全"] += 1

        engine.内容池._保存()
        return 结果


# ============================================================
# 十一、命令行入口
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="🐉 龍魂·终极投喂引擎 — 做减法，不做加法",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3 lh_ultimate_feed.py -f content.txt
  python3 lh_ultimate_feed.py -c "内容1" -c "内容2"
  python3 lh_ultimate_feed.py --import-dir ./docs/
  python3 lh_ultimate_feed.py --interactive
  python3 lh_ultimate_feed.py --status
  python3 lh_ultimate_feed.py --export report.json
  python3 lh_ultimate_feed.py --review  # 审查页面结构
  python3 lh_ultimate_feed.py --list 文档  # 按类型列出
  python3 lh_ultimate_feed.py --tag AI  # 按标签查询
        """
    )

    parser.add_argument("-f", "--file", type=str, help="内容文件路径")
    parser.add_argument("-c", "--content", action="append", help="直接输入内容（可多次）")
    parser.add_argument("-i", "--interactive", action="store_true", help="交互模式")
    parser.add_argument("-s", "--status", action="store_true", help="查看系统状态")
    parser.add_argument("--import-dir", type=str, help="从目录批量导入")
    parser.add_argument("--export", type=str, help="导出内容池到JSON文件")
    parser.add_argument("--review", action="store_true", help="审查+补全页面结构")
    parser.add_argument("--list", type=str, help="按类型列出（文档/代码/知识库/规则/协议/配置）")
    parser.add_argument("--tag", type=str, help="按标签查询")
    parser.add_argument("--json", action="store_true", help="JSON格式输出")

    args = parser.parse_args()

    engine = 终极投喂引擎()

    # 状态
    if args.status:
        状态 = engine.获取状态()
        if args.json:
            print(json.dumps(状态, ensure_ascii=False, indent=2))
        else:
            print("\n📊 系统状态")
            print("=" * 60)
            s = 状态["内容池"]
            print(f"总内容: {s['总内容']} | 活跃: {s['活跃']} | 创意池: {s['创意池']}")
            print(f"历史操作: {s['历史操作']} | 平均质量分: {状态['平均质量分']}")
            print(f"\n类型分布:")
            for t, n in sorted(s.get("类型分布", {}).items(), key=lambda x: -x[1]):
                print(f"  {t}: {n}")
            print(f"\n状态分布:")
            for t, n in sorted(s.get("状态分布", {}).items(), key=lambda x: -x[1]):
                print(f"  {t}: {n}")
        return

    # 导出
    if args.export:
        engine.导出(args.export)
        print(f"✅ 已导出到 {args.export}")
        return

    # 审查页面结构
    if args.review:
        r = 页面结构审查器.审查(engine)
        print(f"✅ 页面结构审查完成: 总数{r['总数']} | 无结构补全{r['无页面结构']} | 已更新{r['已更新']} | 已补全{r['已补全']}")
        return

    # 按类型查询
    if args.list:
        类型映射 = {"文档": 内容类型.文档, "代码": 内容类型.代码, "知识库": 内容类型.知识库,
                  "规则": 内容类型.规则, "协议": 内容类型.协议, "配置": 内容类型.配置,
                  "对话": 内容类型.对话, "创意": 内容类型.创意}
        类型 = 类型映射.get(args.list)
        if 类型:
            units = engine.按类型查询(类型)
            print(f"\n📋 {类型.value} 类型 ({len(units)}条):")
            for u in units:
                print(f"  [{u.质量分}分] {u.标题[:50]} | {u.标签.优先级} | {u.dna[:30]}...")
        else:
            print(f"❌ 未知类型: {args.list}")
            print(f"可用类型: {', '.join(类型映射.keys())}")
        return

    # 按标签查询
    if args.tag:
        units = engine.按标签查询(args.tag)
        print(f"\n🏷️ 标签「{args.tag}」({len(units)}条):")
        for u in units:
            类型_short = u.内容类型.value.split(" ")[1] if " " in u.内容类型.value else u.内容类型.value
            print(f"  [{类型_short}] {u.标题[:50]} | {u.标签.主标签}")
        return

    # 从目录导入
    if args.import_dir:
        print(f"📂 扫描目录: {args.import_dir} ...")
        报告 = engine.从目录投喂(args.import_dir)
        _print_report(报告, args.json)
        return

    # 交互模式
    if args.interactive:
        print("\n" + "=" * 60)
        print("🐉 终极投喂引擎 - 交互模式")
        print("=" * 60)
        print("输入内容自动分类/合并/覆盖/优化")
        print("命令: exit | status | review | list <类型> | tag <标签>")
        print("=" * 60)

        内容列表 = []
        while True:
            try:
                输入 = input("\n📥 > ").strip()
                if not 输入:
                    continue
                if 输入.lower() in ['exit', 'quit']:
                    break
                if 输入.lower() == 'status':
                    s = engine.获取状态()
                    st = s["内容池"]
                    print(f"总{st['总内容']} | 活跃{st['活跃']} | 创意池{st['创意池']} | 均分{s['平均质量分']}")
                    continue
                if 输入.lower() == 'review':
                    r = 页面结构审查器.审查(engine)
                    print(f"✅ 审查: 补全{r['无页面结构']}+更新{r['已更新']}")
                    continue
                if 输入.startswith('list '):
                    类型 = 输入[5:].strip()
                    import subprocess
                    subprocess.run(['python3', __file__, '--list', 类型], cwd=os.path.dirname(os.path.abspath(__file__)))
                    continue
                if 输入.startswith('tag '):
                    标 = 输入[4:].strip()
                    import subprocess
                    subprocess.run(['python3', __file__, '--tag', 标], cwd=os.path.dirname(os.path.abspath(__file__)))
                    continue

                报告 = engine.投喂([输入])
                print(f"✅ 分类: {内容分类器.分类(输入)[0].value}")
                print(f"📊 合并{报告.合并数量} | 覆盖{报告.覆盖数量} | 冻结{报告.冻结数量} | 创意池{报告.创意池数量}")
                print(f"🎯 命中率: {报告.命中数量}/{报告.原始内容数} | {报告.系统评估}")

            except KeyboardInterrupt:
                break
        return

    # 从文件读取
    if args.file:
        报告 = engine.从文件投喂(args.file)
        _print_report(报告, args.json)
        return

    # 直接投喂
    内容列表 = args.content or []
    if not 内容列表:
        parser.print_help()
        return

    报告 = engine.投喂(内容列表)
    _print_report(报告, args.json)


def _print_report(报告: 优化报告, json_mode: bool = False):
    if json_mode:
        d = asdict(报告)
        d['系统评估'] = 报告.系统评估
        print(json.dumps(d, ensure_ascii=False, indent=2))
    else:
        print("\n" + "=" * 60)
        print("🐉 终极投喂报告")
        print("=" * 60)
        print(f"📥 原始: {报告.原始内容数} → 📤 处理后: {报告.处理后内容数}")
        print(f"\n🔻 减法统计:")
        print(f"   合并: {报告.合并数量} | 覆盖: {报告.覆盖数量}")
        print(f"   冻结: {报告.冻结数量} | 创意池: {报告.创意池数量}")
        print(f"\n🎯 命中: {报告.命中数量} | 未命中: {报告.未命中数量}")
        if 报告.按类型统计:
            print(f"\n📂 类型分布:")
            for t, n in sorted(报告.按类型统计.items(), key=lambda x: -x[1])[:6]:
                print(f"   {t}: {n}")
        print(f"\n✅ 评估: {报告.系统评估}")
        print(f"🧬 DNA: {报告.dna}")
        print("=" * 60)


if __name__ == "__main__":
    main()
