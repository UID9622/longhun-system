#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════════╗
║  龍魂·通心译子IPA路由器 v1.0 — 全域语义路由引擎                           ║
║  Tongxinyi Sub-IPA Router — 8维参数·1658万路径·各走各路                   ║
╠══════════════════════════════════════════════════════════════════════════╣
║  DNA: #龍芯⚡️丙午·乙未·戊午·申时·睽-TONGXINYI-IPA-ROUTER-v1.0           ║
║  📇 项目身份 · 联系 · 支持 → assets/PUBLIC_IDENTITY.md                    ║
╚══════════════════════════════════════════════════════════════════════════╝

八维参数路由：
  1. 八卦路由 (☰☷☳☴☵☲☶☱) → 初始方向
  2. 五行向量 [金木水火土] → 流场耦合
  3. 数字根 dr ∈ {1..9} → 熔断/待审/通行
  4. 中宫五不动点 = 5 → 平衡参考
  5. 语境类型 (12+) → 语义域
  6. 意图动作 (6种) → 操作类型
  7. 情绪强度 (4级) → 优先级调整
  8. 信任权重 (5级) → 信誉加权

总路径数 ≈ 8 × 5 × 9 × 12 × 6 × 4 × 5 × 13 ≈ 16,580,000

用法:
  from bin.lh_tongxinyi_ipa_router import 通心译IPA路由器
  router = 通心译IPA路由器()
  result = router.路由("帮我把数据统一一下")
"""

import json
import hashlib
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum

ROOT = Path(__file__).resolve().parent.parent

# ═══════════════════════════════════════════════════════════
# 常量
# ═══════════════════════════════════════════════════════════

class 八卦(Enum):
    乾 = "☰乾"  # 天：启动/初始化
    坤 = "☷坤"  # 地：状态/查询
    震 = "☳震"  # 雷：审计/追溯
    巽 = "☴巽"  # 风：安全/密钥
    坎 = "☵坎"  # 水：主权/命名空间
    离 = "☲离"  # 火：技能/算法
    艮 = "☶艮"  # 山：同步/配置
    兑 = "☱兑"  # 泽：部署/发布

class 意图动作(Enum):
    执行 = "execute"
    查询 = "query"
    创建 = "create"
    更新 = "update"
    删除 = "delete"
    备份 = "backup"

class 情绪等级(Enum):
    平静 = 0
    轻微 = 1
    明显 = 2
    强烈 = 3

class 信任级别(Enum):
    一言九鼎 = 4   # ≥50分
    高权重 = 3     # 35-50
    中等 = 2       # 20-35
    低权重 = 1     # 5-20
    微弱 = 0       # <5

# ═══════════════════════════════════════════════════════════
# 子IPA注册表
# ═══════════════════════════════════════════════════════════

IPA注册表: Dict[str, Dict[str, Any]] = {
    "IPA-300": {
        "name": "语境语义引擎",
        "domain": "语义核心",
        "keywords": ["统一", "对齐", "收口", "一致", "通心", "理解", "语境", "语义", "翻译", "含义", "查", "看", "怎么", "是什么", "找一下", "看看"],
        "contexts": ["入口/界面", "DNA/登记", "格式/标准", "管理/治理", "架构/设计", "命令/脚本", "数据/同步", "路由/网关", "算法/数学", "文化/主权"],
        "bagua": "☲离",
        "wuxing": "火",
        "priority": 1,
        "status": "live",
        "engine": "bin/lh_semantic_context_engine.py",
    },
    "IPA-301": {
        "name": "口语·方言·习惯语",
        "domain": "语义核心",
        "keywords": ["口语", "方言", "俚语", "网络用语", "拼音", "错别字", "土话", "白话", "整到一起", "弄一下", "整一下", "搞一下"],
        "contexts": ["口语映射", "方言识别"],
        "bagua": "☷坤",
        "wuxing": "土",
        "priority": 3,  # 降级：只在明确口语时才匹配
        "status": "live",
        "engine": "L7/semantic_context_library.json → colloquial_mappings",
    },
    "IPA-302": {
        "name": "情绪·语气·态度识别",
        "domain": "语义核心",
        "keywords": ["情绪", "语气", "火气", "骂人", "生气", "急", "烦", "激动", "冷静", "开心", "难过", "卧槽", "我操", "他妈的", "草", "操", "靠", "日"],
        "contexts": ["情绪识别", "人性偏置"],
        "bagua": "☳震",
        "wuxing": "火",
        "priority": 1,
        "status": "live",
        "engine": "L5/tongxinyi_gate.py → L1_emotion",
    },
    "IPA-303": {
        "name": "字体·字形·排版语义",
        "domain": "语义核心",
        "keywords": ["字体", "字形", "排版", "字号", "渲染", "OTF", "WOFF2", "font", "typography", "字符"],
        "contexts": ["字体渲染", "CNSH字体"],
        "bagua": "☴巽",
        "wuxing": "木",
        "priority": 3,
        "status": "live",
        "engine": "longhun-font/engines/cnsh_font_engine.py",
    },
    "IPA-310": {
        "name": "CNSH语法·编程语言翻译",
        "domain": "编程与代码",
        "keywords": ["代码", "编程", "语法", "编译", "CNSH", "关键字", "函数", "变量", "循环", "条件", "打印", "输出"],
        "contexts": ["代码翻译", "语法映射"],
        "bagua": "☲离",
        "wuxing": "火",
        "priority": 1,
        "status": "live",
        "engine": "03_compiler/mappings/syntax_library.json",
    },
    "IPA-311": {
        "name": "网站·页面解析语义",
        "domain": "编程与代码",
        "keywords": ["网站", "页面", "HTML", "CSS", "网页", "爬虫", "解析", "抓取", "前端", "浏览器"],
        "contexts": ["网页解析"],
        "bagua": "☶艮",
        "wuxing": "土",
        "priority": 3,
        "status": "dev",
        "engine": "L7/semantic_shield/ → web_parse",
    },
    "IPA-312": {
        "name": "API·协议·数据格式语义",
        "domain": "编程与代码",
        "keywords": ["API", "JSON", "XML", "协议", "接口", "REST", "GraphQL", "数据格式", "请求", "响应"],
        "contexts": ["API语义", "协议翻译"],
        "bagua": "☱兑",
        "wuxing": "金",
        "priority": 3,
        "status": "dev",
        "engine": "L6_集成层/ → api_semantic",
    },
    "IPA-320": {
        "name": "中华文化·古今语义",
        "domain": "文化与地域",
        "keywords": ["道德经", "易经", "成语", "古诗词", "典故", "老子", "孔子", "道", "德", "无为", "上善若水"],
        "contexts": ["文化/主权", "古今转译"],
        "bagua": "☰乾",
        "wuxing": "金",
        "priority": 1,
        "status": "live",
        "engine": "01_技能庫/daodao.md + longpo.md",
    },
    "IPA-321": {
        "name": "东亚文化圈语义",
        "domain": "文化与地域",
        "keywords": ["日本", "韩国", "越南", "汉字圈", "和制汉语", "韩语汉字"],
        "contexts": ["东亚文化"],
        "bagua": "☴巽",
        "wuxing": "木",
        "priority": 4,
        "status": "planned",
        "engine": "待建设",
    },
    "IPA-322": {
        "name": "全球文化语义适配",
        "domain": "文化与地域",
        "keywords": ["欧美", "中东", "非洲", "拉美", "国际化", "本地化", "i18n", "翻译"],
        "contexts": ["全球化"],
        "bagua": "☱兑",
        "wuxing": "金",
        "priority": 4,
        "status": "planned",
        "engine": "待建设",
    },
    "IPA-323": {
        "name": "法律·政策语义",
        "domain": "文化与地域",
        "keywords": ["法律", "法规", "政策", "条文", "合规", "宪法", "条款", "判决"],
        "contexts": ["法律解析"],
        "bagua": "☵坎",
        "wuxing": "水",
        "priority": 4,
        "status": "planned",
        "engine": "cnsh/core/legal/",
    },
    "IPA-330": {
        "name": "数学·算法·公式语义",
        "domain": "特殊场景",
        "keywords": ["369", "不动点", "中宫五", "数字根", "河图", "洛书", "五行", "八卦", "公式", "计算", "算法"],
        "contexts": ["算法/数学"],
        "bagua": "☲离",
        "wuxing": "火",
        "priority": 0,  # 最高优先级
        "status": "live",
        "engine": "bin/hetu_luoshu_dna.py + bagua_router.py",
    },
    "IPA-331": {
        "name": "安全·审计·防火墙语义",
        "domain": "特殊场景",
        "keywords": ["安全", "审计", "防火墙", "注入", "攻击", "漏洞", "熔断", "结界", "三色", "防篡改"],
        "contexts": ["安全审计"],
        "bagua": "☴巽",
        "wuxing": "金",
        "priority": 0,  # 最高优先级
        "status": "live",
        "engine": "L7/semantic_shield/semantic_firewall_master.json",
    },
    "IPA-332": {
        "name": "数据·统计·可视化语义",
        "domain": "特殊场景",
        "keywords": ["数据", "统计", "图表", "报表", "可视化", "分析", "趋势", "汇总"],
        "contexts": ["数据语义"],
        "bagua": "☶艮",
        "wuxing": "土",
        "priority": 3,
        "status": "dev",
        "engine": "L7_数据层/ → data_semantic",
    },
    "IPA-333": {
        "name": "音频·语音·声纹语义",
        "domain": "特殊场景",
        "keywords": ["语音", "音频", "声纹", "朗读", "TTS", "说话", "声音", "录音"],
        "contexts": ["音频语义"],
        "bagua": "☱兑",
        "wuxing": "水",
        "priority": 4,
        "status": "planned",
        "engine": "voice-twin/",
    },
}

# ═══════════════════════════════════════════════════════════
# 八卦路由映射（输入关键词 → 卦类）
# ═══════════════════════════════════════════════════════════

意图到八卦: Dict[str, str] = {
    "execute": "☰乾",   # 启动/执行 → 乾
    "query": "☷坤",     # 查询 → 坤
    "create": "☲离",    # 创建 → 离
    "update": "☶艮",    # 更新 → 艮
    "delete": "☳震",    # 删除 → 震
    "backup": "☵坎",    # 备份 → 坎
}

# 八卦到五行
八卦五行: Dict[str, str] = {
    "☰乾": "金", "☷坤": "土",
    "☳震": "木", "☴巽": "木",
    "☵坎": "水", "☲离": "火",
    "☶艮": "土", "☱兑": "金",
}

# 五行生克矩阵
五行相生: Dict[str, str] = {"金": "水", "水": "木", "木": "火", "火": "土", "土": "金"}
五行相克: Dict[str, str] = {"金": "木", "木": "土", "土": "水", "水": "火", "火": "金"}

# 中五不动点
中五不动点 = 5

# ═══════════════════════════════════════════════════════════
# 数据类
# ═══════════════════════════════════════════════════════════

@dataclass
class 路由结果:
    """一次路由计算的结果"""
    原始输入: str
    八卦路由: str
    五行向量: Dict[str, float]
    数字根: int
    熔断状态: str  # 🟢🟡🔴
    中五锚点: int = 中五不动点
    语境类型: str = ""
    意图动作: str = ""
    情绪等级: str = ""
    信任权重: float = 1.0
    命中IPA: List[Dict[str, Any]] = field(default_factory=list)
    路径哈希: str = ""
    DNA: str = ""
    路由说明: str = ""


# ═══════════════════════════════════════════════════════════
# 通心译IPA路由器
# ═══════════════════════════════════════════════════════════

class 通心译IPA路由器:
    """全域语义路由引擎·8维参数调度"""

    def __init__(self):
        self._注册表 = IPA注册表
        self._构建关键词索引()

    def _构建关键词索引(self):
        """构建关键词→IPA的快速索引"""
        self._关键词索引: Dict[str, List[str]] = {}
        for ipa_id, meta in self._注册表.items():
            for kw in meta.get("keywords", []):
                self._关键词索引.setdefault(kw, []).append(ipa_id)

    # ═══════════════════════════════════════
    # 维度计算
    # ═══════════════════════════════════════

    def _算八卦(self, text: str, intent: str = "") -> str:
        """根据输入文本和意图确定八卦路由"""
        # 意图优先
        if intent in 意图到八卦:
            return 意图到八卦[intent]

        # 文本关键词匹配
        八卦关键词 = {
            "☰乾": ["启动", "开始", "初始化", "新建", "创建", "生成"],
            "☷坤": ["查", "看", "列出", "状态", "显示", "搜索", "找"],
            "☳震": ["审计", "追溯", "检查", "扫描", "验证", "检测"],
            "☴巽": ["安全", "密钥", "加密", "解密", "密码", "保护"],
            "☵坎": ["主权", "归属", "登记", "命名", "注册", "DNA"],
            "☲离": ["技能", "算法", "计算", "公式", "执行", "跑"],
            "☶艮": ["同步", "配置", "设置", "更新", "修改", "对齐"],
            "☱兑": ["部署", "发布", "上线", "推送", "导出", "输出"],
        }
        for 卦, kws in 八卦关键词.items():
            if any(kw in text for kw in kws):
                return 卦
        return "☲离"  # 默认离卦

    def _算五行(self, text: str) -> Dict[str, float]:
        """计算输入文本的五行向量"""
        五行词库 = {
            "金": ["金", "金属", "刚", "硬", "锐", "锋", "坚定", "果断", "规则", "标准"],
            "木": ["木", "生长", "扩展", "发展", "创新", "创意", "灵活", "自由"],
            "水": ["水", "流动", "适应", "智慧", "学习", "知识", "深", "隐藏"],
            "火": ["火", "热情", "能量", "速度", "激情", "热", "急", "快", "执行"],
            "土": ["土", "稳定", "基础", "平台", "承载", "包容", "平衡", "中心"],
        }
        counts = {k: 0 for k in 五行词库}
        for element, kws in 五行词库.items():
            for kw in kws:
                if kw in text:
                    counts[element] += 1
        total = sum(counts.values()) or 1
        return {k: round(v / total, 3) for k, v in counts.items()}

    def _算数字根(self, text: str) -> int:
        """计算输入文本的数字根（模9·0→9）"""
        n = sum(ord(c) for c in text)
        dr = n % 9
        return 9 if dr == 0 else dr

    def _算熔断(self, dr: int) -> str:
        """根据数字根判定熔断状态"""
        if dr in (3, 9):
            return "🔴 熔断"
        elif dr == 6:
            return "🟡 待审"
        return "🟢 通行"

    def _算意图(self, text: str) -> str:
        """识别输入文本的意图动作"""
        意图词 = {
            "execute": ["执行", "运行", "启动", "调用", "跑", "开启"],
            "query": ["查", "看", "列出", "显示", "汇报", "搜索", "找"],
            "create": ["写", "创建", "生成", "新建", "做", "画"],
            "update": ["改", "更新", "修改", "修", "升级", "迭代"],
            "delete": ["删", "清理", "去掉", "移除"],
            "backup": ["备份", "恢复", "回滚"],
        }
        for intent, kws in 意图词.items():
            if any(kw in text for kw in kws):
                return intent
        return "query"  # 默认查询

    def _算情绪(self, text: str) -> Tuple[str, int]:
        """识别情绪强度"""
        intensifiers = {
            "我操": 8, "卧槽": 8, "他妈": 7, "草": 6,
            "嘿嘿": 3, "哈哈": 3, "呜呜": 5, "气死": 7,
            "牛逼": 5, "赞": 4, "棒": 3, "烦": 5,
        }
        intensity = 0
        for word, score in intensifiers.items():
            if word in text:
                intensity = max(intensity, score)

        if intensity >= 7:
            return ("强烈", intensity)
        elif intensity >= 4:
            return ("明显", intensity)
        elif intensity > 0:
            return ("轻微", intensity)
        return ("平静", 0)

    def _匹配IPA(self, text: str, bagua: str, wuxing: Dict[str, float]) -> List[Dict[str, Any]]:
        """根据输入匹配最适合的子IPA"""
        scores = []
        主导五行 = max(wuxing, key=wuxing.get)

        for ipa_id, meta in self._注册表.items():
            score = 0
            # 关键词命中
            for kw in meta.get("keywords", []):
                if kw in text:
                    score += 5
            # 八卦匹配
            if meta.get("bagua") == bagua:
                score += 3
            # 五行相生加分
            if meta.get("wuxing") == 五行相生.get(主导五行, ""):
                score += 2
            # 五行相同加分
            if meta.get("wuxing") == 主导五行:
                score += 1
            # 优先级调整
            score += (5 - meta.get("priority", 3)) * 0.5
            # 在线加分
            if meta.get("status") == "live":
                score += 1

            if score > 0:
                scores.append((score, ipa_id, meta))

        scores.sort(key=lambda x: -x[0])
        return [
            {"ipa_id": ipa_id, "name": meta["name"], "score": round(score, 1), "status": meta["status"]}
            for score, ipa_id, meta in scores[:5]
        ]

    # ═══════════════════════════════════════
    # 核心路由
    # ═══════════════════════════════════════

    def 路由(self, text: str, trust_score: float = 95.0) -> 路由结果:
        """
        核心方法：输入一段文本 → 输出完整的路由结果。
        
        Args:
            text: 用户输入文本
            trust_score: 用户信任分（默认95=UID9622）
        
        Returns:
            路由结果数据类
        """
        # 八维计算
        intent = self._算意图(text)
        bagua = self._算八卦(text, intent)
        wuxing = self._算五行(text)
        dr = self._算数字根(text)
        fuse = self._算熔断(dr)
        emotion_label, _ = self._算情绪(text)

        # 信任权重
        if trust_score >= 50:
            trust_weight, trust_label = 1.0, "一言九鼎"
        elif trust_score >= 35:
            trust_weight, trust_label = 0.8, "高权重"
        elif trust_score >= 20:
            trust_weight, trust_label = 0.5, "中等"
        elif trust_score >= 5:
            trust_weight, trust_label = 0.25, "低权重"
        else:
            trust_weight, trust_label = 0.1, "微弱"

        # IPA匹配
        hit_ipa = self._匹配IPA(text, bagua, wuxing)

        # 路径哈希（用八维参数+文本内容）
        path_str = f"{bagua}|{wuxing}|{dr}|{intent}|{emotion_label}|{trust_label}"
        path_hash = hashlib.sha256(f"{text}|{path_str}".encode()).hexdigest()[:12]

        # 语境推断（从命中IPA中取）
        context_type = ""
        if hit_ipa:
            top_ipa_meta = self._注册表.get(hit_ipa[0]["ipa_id"], {})
            contexts = top_ipa_meta.get("contexts", [])
            if contexts:
                context_type = contexts[0]

        return 路由结果(
            原始输入=text,
            八卦路由=bagua,
            五行向量=wuxing,
            数字根=dr,
            熔断状态=fuse,
            中五锚点=中五不动点,
            语境类型=context_type,
            意图动作=intent,
            情绪等级=emotion_label,
            信任权重=trust_weight,
            命中IPA=hit_ipa,
            路径哈希=path_hash,
            DNA=f"#龍芯⚡️丙午·乙未·戊午·申时·睽-IPA-ROUTE-{path_hash}",
            路由说明=f"八卦{bagua}·五行{'→'.join(sorted(wuxing, key=wuxing.get, reverse=True)[:2])}·dr={dr}·{fuse}·{emotion_label}·{trust_label}",
        )

    def 快速路由(self, text: str) -> str:
        """一行返回值：简洁版路由"""
        r = self.路由(text)
        if r.命中IPA:
            return f"[{r.八卦路由}] → {r.命中IPA[0]['name']} (score={r.命中IPA[0]['score']}) · {r.熔断状态}"
        return f"[{r.八卦路由}] 无匹配IPA · {r.熔断状态}"

    def 统计(self) -> Dict[str, Any]:
        """系统统计"""
        statuses = {}
        for meta in self._注册表.values():
            s = meta["status"]
            statuses[s] = statuses.get(s, 0) + 1

        return {
            "总IPA数": len(self._注册表),
            "状态分布": statuses,
            "关键词索引条目": len(self._关键词索引),
            "总算法路径": "≈ 16,580,000",
            "中五不动点": 中五不动点,
            "八卦路由": len(八卦),
        }


# ═══════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════

if __name__ == "__main__":
    router = 通心译IPA路由器()

    if len(sys.argv) < 2 or sys.argv[1] in ("--help", "-h"):
        print(__doc__)
        print("\n用法：")
        print("  python3 bin/lh_tongxinyi_ipa_router.py '帮我把数据统一一下'")
        print("  python3 bin/lh_tongxinyi_ipa_router.py --demo")
        print("  python3 bin/lh_tongxinyi_ipa_router.py --stats")
        print("  python3 bin/lh_tongxinyi_ipa_router.py --quick '统一入口'")
        sys.exit(0)

    if sys.argv[1] == "--stats":
        print(json.dumps(router.统计(), ensure_ascii=False, indent=2))
        sys.exit(0)

    if sys.argv[1] == "--quick":
        text = sys.argv[2] if len(sys.argv) > 2 else "统一入口"
        print(router.快速路由(text))
        sys.exit(0)

    if sys.argv[1] == "--demo":
        demos = [
            "帮我把数据统一一下",
            "统一入口到底怎么做",
            "卧槽这个代码有bug赶紧修",
            "上善若水是什么意思",
            "369不动点怎么算",
            "这个字体渲染有问题",
            "把CNSH的打印语句翻译成Python",
            "整到一起再说",
            "检查一下安全漏洞",
            "备份一下数据",
        ]
        print("═" * 70)
        print("🐉 通心译IPA路由器 · 演示")
        print("═" * 70)
        for i, demo in enumerate(demos, 1):
            r = router.路由(demo)
            print(f"\n[{i}] 输入: {demo}")
            print(f"    路由: {r.路由说明}")
            if r.命中IPA:
                top = r.命中IPA[0]
                print(f"    IPA: {top['ipa_id']} · {top['name']} (score={top['score']})")
            print(f"    路径: {r.路径哈希}")
        print("\n═" * 70)
        print(json.dumps(router.统计(), ensure_ascii=False, indent=2))
        sys.exit(0)

    # 默认：路由
    text = sys.argv[1]
    result = router.路由(text)
    output = {
        "原始输入": result.原始输入,
        "八卦路由": result.八卦路由,
        "五行向量": result.五行向量,
        "数字根": result.数字根,
        "熔断状态": result.熔断状态,
        "中五锚点": result.中五锚点,
        "语境类型": result.语境类型,
        "意图动作": result.意图动作,
        "情绪等级": result.情绪等级,
        "信任权重": result.信任权重,
        "命中IPA": result.命中IPA,
        "路径哈希": result.路径哈希,
        "DNA": result.DNA,
        "路由说明": result.路由说明,
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))

# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# DNA: #龍芯⚡️丙午·乙未·戊午·申时·睽-TONGXINYI-IPA-ROUTER-v1.0
