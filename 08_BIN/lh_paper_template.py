#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
龍魂 · 论文模板自动优化引擎 v1.0
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
多元化论文排版: 模板选择→结构填充→排版优化→HTML渲染

DNA: #龍芯⚡️丙午·甲申·戊戌·䷁坤-PAPER-TEMPLATE-ENGINE-v1.0-f3b8c2d1
创建者: 诸葛鑫（UID9622）
协议: 工程层 MulanPSL v2

用法:
  python3 bin/lh_paper_template.py --list                      # 列出模板
  python3 bin/lh_paper_template.py --auto input.md              # 自动匹配
  python3 bin/lh_paper_template.py --template P3 --skeleton     # 生成骨架
  python3 bin/lh_paper_template.py --optimize paper.md          # 排版优化
  python3 bin/lh_paper_template.py --render paper.md            # HTML渲染
"""

import sys
import os
import re
import argparse
import datetime
import textwrap
from pathlib import Path
from collections import Counter

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "bin"))

DNA = "#龍芯⚡️丙午·甲申·戊戌·䷁坤-PAPER-TEMPLATE-ENGINE-v1.0-f3b8c2d1"
VERSION = "1.0.0"

# ═══════════════════════════════════════════════
# 数字根 + 五行
# ═══════════════════════════════════════════════

def digital_root(s: str = None) -> int:
    """计算数字根"""
    if s is None:
        s = datetime.datetime.now().strftime("%Y%m%d")
    digits = [int(c) for c in s if c.isdigit()]
    if not digits:
        return 0
    total = sum(digits)
    while total > 9:
        total = sum(int(d) for d in str(total))
    return total

def wuxing_from_root(dr: int) -> str:
    wm = {1: "水", 2: "火", 3: "木", 4: "金", 5: "土", 6: "水", 7: "火", 8: "木", 9: "金"}
    return wm.get(dr, "土")

# ═══════════════════════════════════════════════
# 模板定义（6套）
# ═══════════════════════════════════════════════

PAPER_TEMPLATES = {
    "P1": {
        "name": "🎓 学术研究论文型",
        "emoji": "📄",
        "keywords": ["论文", "研究", "定理", "证明", "算法", "模型", "对比实验", "文献综述",
                      "摘要", "引言", "方法", "实验", "结论", "参考文献", "引用", "期刊", "arXiv"],
        "tricolor": "🟡",
        "tricolor_reason": "学术分析·含推演论断·建议同行评审后引用",
        "persona": "P01诸葛亮·P06数学大师·P05上帝之眼",
        "sections": [
            "## 🏷️ 论文元信息",
            "## 📋 摘要",
            "## 1. 引言",
            "## 2. 相关工作",
            "## 3. 数学模型",
            "## 4. 工程实现",
            "## 5. 实验验证",
            "## 6. 讨论",
            "## 7. 结论与未来工作",
            "## 📚 参考文献",
            "## 附录",
            "## 协议声明",
            "## 📋 ROOT_CARD",
        ]
    },
    "P2": {
        "name": "🔧 工程技术报告型",
        "emoji": "🔩",
        "keywords": ["系统", "架构", "API", "部署", "性能", "优化", "工程", "配置",
                      "端口", "命令行", "安装", "Docker", "运维", "监控", "日志"],
        "tricolor": "🟢",
        "tricolor_reason": "工程实测·可部署验证·代码可直接运行",
        "persona": "P04鲁班·P14吕蒙·P15乔前辈",
        "sections": [
            "## 🏷️ 报告元信息",
            "## 📦 交付物清单",
            "## 📂 系统架构",
            "## 🔌 API/接口说明",
            "## 🚀 部署方案",
            "## 📊 性能指标",
            "## 🔒 安全审计",
            "## ✅ 验收清单",
            "## 🔴 一票否决",
            "## 协议声明",
            "## 📋 ROOT_CARD",
        ]
    },
    "P3": {
        "name": "☯️ 哲学-数学交叉型",
        "emoji": "☯️",
        "keywords": ["道德经", "易经", "五行", "八卦", "洛书", "河图", "形式化", "哲学",
                      "天道", "无为", "阴阳", "太极", "中庸", "相生相克", "六十四卦"],
        "tricolor": "🟡",
        "tricolor_reason": "哲学推演+数学形式化·跨学科交叉·建议复核",
        "persona": "P06数学大师·P08仓颉·P12屈原·P00文心",
        "sections": [
            "## 🏷️ 论文元信息",
            "## 📋 摘要",
            "## 一、哲学源头",
            "## 二、数学形式化",
            "## 三、证明",
            "## 四、工程映射",
            "## 五、三层统一",
            "## 六、结论",
            "## 📚 参考文献",
            "## 协议声明",
            "## 📋 ROOT_CARD",
        ]
    },
    "P4": {
        "name": "🏗️ 系统架构设计型",
        "emoji": "🏗️",
        "keywords": ["架构设计", "拓扑", "层级", "引擎", "模块", "分布式", "微服务",
                      "通信协议", "数据流", "扩展", "插件", "接口", "端口分配"],
        "tricolor": "🟢",
        "tricolor_reason": "架构设计·结构清晰·可落地实施",
        "persona": "P04鲁班·P13姜子牙·P01诸葛亮",
        "sections": [
            "## 🏷️ 文档元信息",
            "## 一、设计目标与约束",
            "## 二、总体架构",
            "## 三、核心引擎/模块详解",
            "## 四、数据流",
            "## 五、端口与配置",
            "## 六、扩展性设计",
            "## 七、安全设计",
            "## 协议声明",
            "## 📋 ROOT_CARD",
        ]
    },
    "P5": {
        "name": "🧪 实证实验报告型",
        "emoji": "🧪",
        "keywords": ["实验", "测试", "验证", "基准", "对比", "性能", "数据集", "指标",
                      "准确率", "F1", "召回率", "收敛", "消融", "对照组", "统计"],
        "tricolor": "🟢",
        "tricolor_reason": "实验数据可复现·结果可验证",
        "persona": "P06数学大师·P04鲁班·P05上帝之眼",
        "sections": [
            "## 🏷️ 报告元信息",
            "## 一、实验目标与假设",
            "## 二、实验设置",
            "## 三、实验设计",
            "## 四、结果",
            "## 五、分析",
            "## 六、复现指南",
            "## 七、结论",
            "## 协议声明",
            "## 📋 ROOT_CARD",
        ]
    },
    "P6": {
        "name": "📋 总览/规划文档型",
        "emoji": "📋",
        "keywords": ["总览", "规划", "系列", "路线图", "矩阵", "概览", "目录", "大全",
                      "体系", "全景", "蓝图", "Roadmap", "索引", "规划文档"],
        "tricolor": "🟢",
        "tricolor_reason": "规划文档·框架完整·待逐项落地",
        "persona": "P01诸葛亮·P00文心·P03雯雯",
        "sections": [
            "## 🏷️ 文档元信息",
            "## 📋 摘要",
            "## 📑 目录",
            "## 一、矩阵总览",
            "## 二、逐项详解",
            "## 三、关系拓扑图",
            "## 四、与现有方案对比",
            "## 五、执行路线图",
            "## 六、FAQ",
            "## 七、版本历史",
            "## 附录",
            "## 协议声明",
            "## 📋 ROOT_CARD",
        ]
    },
}

# ═══════════════════════════════════════════════
# 模板自动选择
# ═══════════════════════════════════════════════

def tokenize(text: str) -> list:
    """简单分词（无jieba依赖）"""
    # 中文按标点和空格切分
    _DELIM = r'[\s,，。！？、；：""''（）()\[\]{}《》\-+]+'
    tokens = re.split(_DELIM, text)
    return [t for t in tokens if len(t) >= 2]

def auto_select_template(text: str, top_k: int = 2) -> list:
    """
    自动匹配最佳模板
    返回: [(模板ID, 模板名, 分数, 命中关键词), ...]
    """
    tokens = tokenize(text)
    token_set = set(tokens)
    
    scores = {}
    details = {}
    
    for tid, tmpl in PAPER_TEMPLATES.items():
        matched = [kw for kw in tmpl["keywords"] if kw in text or kw in token_set]
        score = len(matched)
        # 关键词密度加成
        if len(matched) > 0:
            density = len(matched) / len(tmpl["keywords"])
            score += density * 10
        scores[tid] = score
        details[tid] = matched
    
    # 排序
    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    results = []
    for tid, score in ranked[:top_k]:
        if score > 0:
            tmpl = PAPER_TEMPLATES[tid]
            results.append((tid, tmpl["name"], score, details[tid]))
    
    return results

# ═══════════════════════════════════════════════
# 骨架生成
# ═══════════════════════════════════════════════

def generate_skeleton(template_id: str, title: str = "", author: str = "诸葛鑫（UID9622）") -> str:
    """生成论文骨架"""
    tmpl = PAPER_TEMPLATES.get(template_id)
    if not tmpl:
        return f"❌ 未知模板: {template_id}"
    
    now = datetime.datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%Y-%m-%d %H:%M:%S CST")
    dna = f"#龍芯⚡️{date_str}-PAPER-{template_id}-v1.0-UID9622"
    dr = digital_root(date_str)
    wx = wuxing_from_root(dr)
    
    lines = []
    lines.append(f"# 🐉 {title or '[论文标题]'}")
    lines.append("")
    
    # 元信息区
    lines.append("## 🏷️ 论文元信息")
    lines.append("")
    lines.append(f"**模板类型**: {tmpl['name']}")
    lines.append(f"**作者**: {author}")
    lines.append(f"**生成时间**: {time_str}")
    lines.append(f"**三色审计**: {tmpl['tricolor']}（{tmpl['tricolor_reason']}）")
    lines.append(f"**关联人格**: {tmpl['persona']}")
    lines.append(f"**DNA签名**: {dna}")
    lines.append(f"**GPG**: A2D0092CEE2E5BA87035600924C3704A8CC26D5F")
    lines.append(f"**许可**: 思想层 CC BY-NC-SA 4.0 · 工程层 MulanPSL v2")
    lines.append(f"**生效时间**: {time_str}")
    lines.append("")
    lines.append("---")
    lines.append("")
    
    # 章节骨架
    for section in tmpl["sections"]:
        if section == "## 🏷️ 论文元信息" or section == "## 🏷️ 报告元信息" or section == "## 🏷️ 文档元信息":
            continue  # 已在上方
        lines.append(section)
        lines.append("")
        lines.append("[待填充]")
        lines.append("")
    
    # ROOT_CARD
    lines.append("---")
    lines.append("")
    lines.append("## 📋 ROOT_CARD")
    lines.append("")
    lines.append("```")
    lines.append("【ROOT_CARD｜数学根审计】")
    lines.append(f"Root: dr={dr}")
    lines.append(f"Wuxing: {wx}")
    lines.append(f"TriColor: {tmpl['tricolor']}")
    lines.append(f"Type: paper-{template_id.lower()}")
    lines.append(f"DNA: {dna}")
    lines.append("```")
    lines.append("")
    
    # DNA签名区
    lines.append("---")
    lines.append("")
    lines.append("```")
    lines.append("════════════════════════════════════════")
    lines.append(f"DNA: {dna}")
    lines.append("确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z")
    lines.append("GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F")
    lines.append(f"三色: {tmpl['tricolor']}")
    lines.append(f"生成时间: {time_str}")
    lines.append(f"作者: {author}")
    lines.append("════════════════════════════════════════")
    lines.append("```")
    
    return "\n".join(lines)

# ═══════════════════════════════════════════════
# 排版优化引擎
# ═══════════════════════════════════════════════

def optimize_typography(text: str) -> tuple:
    """
    排版自动优化
    返回: (优化后文本, 优化报告)
    """
    lines = text.split("\n")
    report = []
    optimized = []
    
    heading_pattern = re.compile(r'^(#{1,6})\s+(.*)')
    prev_h_level = 0
    table_lines = []
    in_table = False
    code_lang_pattern = re.compile(r'^```(\w*)$')
    math_count = 0
    
    for i, line in enumerate(lines):
        line_num = i + 1
        
        # --- 标题层级检查 ---
        m = heading_pattern.match(line)
        if m:
            level = len(m.group(1))
            title_text = m.group(2)
            
            # 跳级检测
            if prev_h_level > 0 and level > prev_h_level + 1:
                report.append(f"⚠️  L{line_num}: 标题跳级 h{prev_h_level}→h{level}「{title_text[:30]}」")
            
            # 标题过长
            if len(title_text) > 60:
                report.append(f"💡 L{line_num}: 标题过长({len(title_text)}字)「{title_text[:30]}...」建议精简")
            
            prev_h_level = level
            optimized.append(line)
            continue
        
        # --- 表格处理 ---
        if line.strip().startswith("|") and line.strip().endswith("|"):
            if not in_table:
                in_table = True
                table_lines = []
            table_lines.append(line)
            optimized.append(line)
            continue
        elif in_table:
            in_table = False
            # 检查表格是否缺少分隔行
            has_separator = any(re.match(r'^\|[\s:\-]+\|', tl) for tl in table_lines)
            if not has_separator and len(table_lines) > 1:
                report.append(f"⚠️  L{line_num - len(table_lines)}: 表格缺少分隔行")
        
        # --- 代码块语言标记 ---
        m = code_lang_pattern.match(line.strip())
        if m:
            lang = m.group(1)
            if not lang:
                report.append(f"💡 L{line_num}: 代码块缺少语言标记，建议添加（如 ```python）")
        
        # --- 公式 $ 配对检查 ---
        dollar_count = line.count("$") - line.count("$$") * 2  # 粗略计数
        math_count += dollar_count
        
        optimized.append(line)
    
    # 最终 $ 配对
    if math_count % 2 != 0:
        report.append(f"🔴 全文 $ 符号不配对（共{math_count}个），可能公式格式错误")
    
    if not report:
        report.append("✅ 排版检查通过，无需优化")
    
    return "\n".join(optimized), report

# ═══════════════════════════════════════════════
# HTML渲染
# ═══════════════════════════════════════════════

PAPER_CSS = """
/* ═══════════════════════════════════════════════
   龍魂论文渲染样式 v1.0
   DNA: #龍芯⚡️丙午·甲申·戊戌·䷁坤-PAPER-CSS-v1.0
   ═══════════════════════════════════════════════ */

:root {
    --lh-bg: #0a0a0f;
    --lh-surface: #12121a;
    --lh-card: #1a1a28;
    --lh-border: #2a2a3a;
    --lh-text: #e0e0e8;
    --lh-text-dim: #8888a0;
    --lh-gold: #c9a227;
    --lh-gold-dim: #8a6d1b;
    --lh-red: #b93232;
    --lh-red-glow: rgba(185,50,50,0.15);
    --lh-green: #2ea84c;
    --lh-yellow: #c9a227;
    --lh-accent: #4a90d9;
    --lh-code-bg: #0d0d18;
    --lh-table-stripe: rgba(201,162,39,0.05);
    --lh-mermaid-bg: #0f0f1a;
    --font-cn: "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
    --font-mono: "SF Mono", "Cascadia Code", "Fira Code", monospace;
    --radius: 8px;
    --shadow: 0 2px 16px rgba(0,0,0,0.4);
}

* { margin: 0; padding: 0; box-sizing: border-box; }

body {
    background: var(--lh-bg);
    color: var(--lh-text);
    font-family: var(--font-cn);
    line-height: 1.8;
    font-size: 16px;
}

.paper-container {
    max-width: 860px;
    margin: 0 auto;
    padding: 48px 24px 80px;
}

/* ── 标题层级 ── */

.paper-container h1 {
    font-size: 2.2em;
    color: var(--lh-gold);
    text-align: center;
    padding: 32px 0 16px;
    border-bottom: 2px solid var(--lh-gold-dim);
    margin-bottom: 32px;
    letter-spacing: 0.05em;
}

.paper-container h2 {
    font-size: 1.5em;
    color: var(--lh-gold);
    margin: 48px 0 20px;
    padding-left: 12px;
    border-left: 4px solid var(--lh-gold);
    line-height: 1.4;
}

.paper-container h3 {
    font-size: 1.2em;
    color: #d4c080;
    margin: 32px 0 12px;
}

.paper-container h4 {
    font-size: 1.05em;
    color: var(--lh-text-dim);
    margin: 24px 0 8px;
}

/* ── 段落与文本 ── */

.paper-container p {
    margin: 12px 0;
    text-align: justify;
}

.paper-container strong {
    color: var(--lh-gold);
    font-weight: 700;
}

.paper-container em {
    color: #c0b880;
}

.paper-container a {
    color: var(--lh-accent);
    text-decoration: none;
    border-bottom: 1px dotted var(--lh-accent);
}

.paper-container a:hover {
    color: var(--lh-gold);
    border-bottom-color: var(--lh-gold);
}

/* ── 摘要框 ── */

.abstract-box {
    background: linear-gradient(135deg, rgba(201,162,39,0.08), rgba(201,162,39,0.02));
    border: 1px solid var(--lh-gold-dim);
    border-radius: var(--radius);
    padding: 24px 28px;
    margin: 24px 0;
}

.abstract-box h3 {
    color: var(--lh-gold);
    margin-top: 0;
    font-size: 1.1em;
}

.abstract-box p {
    color: var(--lh-text);
    font-size: 0.95em;
    margin: 8px 0;
}

/* ── 表格 ── */

.paper-container table {
    width: 100%;
    border-collapse: collapse;
    margin: 20px 0;
    font-size: 0.92em;
    border-radius: var(--radius);
    overflow: hidden;
}

.paper-container thead th {
    background: linear-gradient(180deg, rgba(201,162,39,0.15), rgba(201,162,39,0.08));
    color: var(--lh-gold);
    font-weight: 700;
    padding: 12px 16px;
    text-align: left;
    border-bottom: 2px solid var(--lh-gold-dim);
    white-space: nowrap;
}

.paper-container tbody td {
    padding: 10px 16px;
    border-bottom: 1px solid var(--lh-border);
    color: var(--lh-text);
}

.paper-container tbody tr:nth-child(even) {
    background: var(--lh-table-stripe);
}

.paper-container tbody tr:hover {
    background: rgba(201,162,39,0.08);
}

/* ── 代码块 ── */

.paper-container pre {
    background: var(--lh-code-bg);
    border: 1px solid var(--lh-border);
    border-radius: var(--radius);
    padding: 20px;
    overflow-x: auto;
    margin: 16px 0;
    font-family: var(--font-mono);
    font-size: 0.88em;
    line-height: 1.6;
}

.paper-container pre code {
    color: #d4d4e8;
}

.paper-container code {
    font-family: var(--font-mono);
    background: rgba(201,162,39,0.08);
    color: var(--lh-gold);
    padding: 2px 6px;
    border-radius: 3px;
    font-size: 0.9em;
}

.paper-container pre code {
    background: none;
    padding: 0;
    color: #d4d4e8;
}

/* ── 引用 ── */

.paper-container blockquote {
    border-left: 4px solid var(--lh-gold);
    background: rgba(201,162,39,0.04);
    margin: 16px 0;
    padding: 12px 20px;
    color: var(--lh-text-dim);
    font-style: italic;
    border-radius: 0 var(--radius) var(--radius) 0;
}

/* ── 定理/证明框 ── */

.theorem-box {
    border: 1px solid var(--lh-gold-dim);
    border-left: 4px solid var(--lh-gold);
    background: rgba(201,162,39,0.04);
    border-radius: 0 var(--radius) var(--radius) 0;
    padding: 16px 20px;
    margin: 16px 0;
}

.theorem-box .theorem-title {
    color: var(--lh-gold);
    font-weight: bold;
    margin-bottom: 8px;
}

.proof-box {
    border: 1px solid var(--lh-border);
    border-left: 4px solid var(--lh-accent);
    background: rgba(74,144,217,0.04);
    border-radius: 0 var(--radius) var(--radius) 0;
    padding: 16px 20px;
    margin: 16px 0;
}

/* ── Mermaid图表 ── */

.mermaid-container {
    background: var(--lh-mermaid-bg);
    border: 1px solid var(--lh-border);
    border-radius: var(--radius);
    padding: 24px;
    margin: 20px 0;
    text-align: center;
    overflow-x: auto;
}

/* ── 分隔线 ── */

.paper-container hr {
    border: none;
    border-top: 1px solid var(--lh-border);
    margin: 40px 0;
}

/* ── 列表 ── */

.paper-container ul, .paper-container ol {
    margin: 12px 0;
    padding-left: 24px;
}

.paper-container li {
    margin: 6px 0;
    line-height: 1.7;
}

/* ── ROOT_CARD ├── */

.root-card {
    background: linear-gradient(135deg, rgba(201,162,39,0.06), rgba(185,50,50,0.04));
    border: 1px solid var(--lh-gold-dim);
    border-radius: var(--radius);
    padding: 20px 24px;
    margin: 32px 0;
}

.root-card h3 { color: var(--lh-gold); margin-top: 0; }

/* ── 签名区 ── */

.signature-zone {
    background: var(--lh-card);
    border: 1px solid var(--lh-border);
    border-radius: var(--radius);
    padding: 24px;
    margin: 32px 0;
    font-family: var(--font-mono);
    font-size: 0.85em;
    color: var(--lh-text-dim);
    white-space: pre-wrap;
}

/* ── 移动端适配 ── */

@media (max-width: 768px) {
    .paper-container {
        padding: 24px 16px 60px;
    }
    .paper-container h1 { font-size: 1.6em; }
    .paper-container h2 { font-size: 1.25em; }
    .paper-container table { font-size: 0.82em; }
    .paper-container thead th,
    .paper-container tbody td { padding: 8px 10px; }
}
"""

def render_html(md_text: str, title: str = "龍魂论文") -> str:
    """将Markdown论文渲染为带CSS的HTML"""
    
    # 简单Markdown→HTML转换
    html_body = _simple_md_to_html(md_text)
    
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} · 龍魂系统</title>
<style>
{PAPER_CSS}
</style>
</head>
<body>
<div class="paper-container">
{html_body}
</div>
<footer style="text-align:center;padding:40px;color:var(--lh-text-dim);font-size:0.85em;">
🐉 龍魂出品 · 透明可审 · <span style="color:var(--lh-gold)">UID9622</span>
</footer>
</body>
</html>"""
    return html


def _simple_md_to_html(text: str) -> str:
    """简易Markdown→HTML（行级转换）"""
    lines = text.split("\n")
    out = []
    in_code = False
    in_table = False
    table_html = []
    
    for line in lines:
        # 代码块
        if line.strip().startswith("```"):
            if in_code:
                out.append("</code></pre>")
                in_code = False
            else:
                lang = line.strip()[3:].strip()
                cls = f' class="language-{lang}"' if lang else ""
                out.append(f"<pre><code{cls}>")
                in_code = True
            continue
        
        if in_code:
            out.append(_escape_html(line))
            continue
        
        # 表格
        if line.strip().startswith("|") and line.strip().endswith("|"):
            if not in_table:
                in_table = True
                table_html = []
            table_html.append(line)
            continue
        elif in_table:
            in_table = False
            out.append(_render_table(table_html))
            table_html = []
        
        # 标题
        m = re.match(r'^(#{1,6})\s+(.*)', line)
        if m:
            level = len(m.group(1))
            content = m.group(2)
            out.append(f"<h{level}>{content}</h{level}>")
            continue
        
        # 分隔线
        if re.match(r'^[-*_]{3,}$', line.strip()):
            out.append("<hr>")
            continue
        
        # 引用
        if line.startswith(">"):
            content = line[1:].strip()
            out.append(f"<blockquote><p>{content}</p></blockquote>")
            continue
        
        # 列表
        m = re.match(r'^(\s*)[-*+]\s+(.*)', line)
        if m:
            out.append(f"<li>{m.group(2)}</li>")
            continue
        
        m = re.match(r'^(\s*)\d+\.\s+(.*)', line)
        if m:
            out.append(f"<li>{m.group(2)}</li>")
            continue
        
        # 加粗/斜体
        line = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', line)
        line = re.sub(r'\*(.+?)\*', r'<em>\1</em>', line)
        
        # 行内代码
        line = re.sub(r'`([^`]+)`', r'<code>\1</code>', line)
        
        # 链接
        line = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', line)
        
        # 空行→段落
        if not line.strip():
            out.append("<br>")
        else:
            out.append(f"<p>{line}</p>")
    
    if in_table:
        out.append(_render_table(table_html))
    if in_code:
        out.append("</code></pre>")
    
    return "\n".join(out)


def _render_table(lines: list) -> str:
    """渲染Markdown表格为HTML"""
    if len(lines) < 2:
        return ""
    
    rows = []
    for line in lines:
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        rows.append(cells)
    
    # 跳过分隔行
    data_rows = [rows[0]]  # 表头
    for row in rows[1:]:
        if not all(re.match(r'^[\s:\-]+$', c) for c in row):
            data_rows.append(row)
    
    html = "<table><thead><tr>"
    for cell in data_rows[0]:
        html += f"<th>{cell}</th>"
    html += "</tr></thead><tbody>"
    
    for row in data_rows[1:]:
        html += "<tr>"
        for cell in row:
            html += f"<td>{cell}</td>"
        html += "</tr>"
    
    html += "</tbody></table>"
    return html


def _escape_html(text: str) -> str:
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

# ═══════════════════════════════════════════════
# 主入口
# ═══════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description="🐉 龍魂 · 论文模板自动优化引擎 v1.0",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""\
        示例:
          %(prog)s --list                       列出6套模板
          %(prog)s --auto paper.md               自动匹配最佳模板
          %(prog)s --template P3 --skeleton      生成哲学-数学交叉型骨架
          %(prog)s --optimize paper.md           排版优化
          %(prog)s --render paper.md             生成HTML渲染版
        """)
    )
    parser.add_argument("--list", action="store_true", help="列出所有模板")
    parser.add_argument("--template", "-t", choices=[f"P{i}" for i in range(1, 7)], help="指定模板ID")
    parser.add_argument("--auto", metavar="FILE", help="自动匹配模板（输入论文文件）")
    parser.add_argument("--skeleton", action="store_true", help="生成模板骨架")
    parser.add_argument("--title", default="", help="论文标题")
    parser.add_argument("--author", default="诸葛鑫（UID9622）", help="作者")
    parser.add_argument("--output", "-o", default="", help="输出文件")
    parser.add_argument("--optimize", metavar="FILE", help="排版优化（输入论文文件）")
    parser.add_argument("--render", metavar="FILE", help="HTML渲染（输入论文文件）")
    parser.add_argument("--fix", action="store_true", help="自动修复排版问题")
    
    args = parser.parse_args()
    
    # --- list ---
    if args.list:
        print("=" * 60)
        print("🐉 龍魂 · 论文多元化模板库 v1.0")
        print("=" * 60)
        for tid, tmpl in PAPER_TEMPLATES.items():
            print(f"\n  {tid}  {tmpl['name']}")
            print(f"      三色: {tmpl['tricolor']}  |  人格: {tmpl['persona']}")
            print(f"      关键词: {', '.join(tmpl['keywords'][:8])}...")
            print(f"      章节数: {len(tmpl['sections'])}")
        print("\n" + "=" * 60)
        print("用法: python3 bin/lh_paper_template.py --auto paper.md")
        print("=" * 60)
        return
    
    # --- auto ---
    if args.auto:
        path = Path(args.auto)
        if not path.exists():
            print(f"❌ 文件不存在: {args.auto}")
            sys.exit(1)
        text = path.read_text(encoding="utf-8")
        results = auto_select_template(text)
        
        print("\n" + "=" * 60)
        print(f"🔍 自动匹配结果: {path.name}")
        print("=" * 60)
        
        if not results:
            print("❌ 未匹配到合适模板，请手动指定 --template")
            sys.exit(1)
        
        for tid, name, score, keywords in results:
            bar = "█" * min(int(score), 40)
            print(f"\n  {tid}  {name}")
            print(f"  匹配分: {score:.1f}  {bar}")
            print(f"  命中词: {', '.join(keywords[:10])}")
            print(f"  章节预览:")
            for s in PAPER_TEMPLATES[tid]["sections"][:5]:
                print(f"    {s}")
            print()
        
        best_id = results[0][0]
        best_name = results[0][1]
        print(f"🏆 推荐: {best_id} {best_name}")
        print(f"   运行生成骨架: python3 bin/lh_paper_template.py --template {best_id} --skeleton --title \"论文标题\"")
        return
    
    # --- skeleton ---
    if args.skeleton and args.template:
        skeleton = generate_skeleton(args.template, args.title, args.author)
        if args.output:
            Path(args.output).write_text(skeleton, encoding="utf-8")
            print(f"✅ 骨架已生成: {args.output}")
        else:
            print(skeleton)
        return
    
    # --- optimize ---
    if args.optimize:
        path = Path(args.optimize)
        if not path.exists():
            print(f"❌ 文件不存在: {args.optimize}")
            sys.exit(1)
        text = path.read_text(encoding="utf-8")
        
        print("\n" + "=" * 60)
        print(f"🔧 排版优化: {path.name}")
        print("=" * 60)
        
        optimized, report = optimize_typography(text)
        
        for r in report:
            print(f"  {r}")
        
        if args.fix and report and report[0] != "✅ 排版检查通过，无需优化":
            output_path = args.output or path
            Path(output_path).write_text(optimized, encoding="utf-8")
            print(f"\n✅ 已修复并保存: {output_path}")
        
        print()
        return
    
    # --- render ---
    if args.render:
        path = Path(args.render)
        if not path.exists():
            print(f"❌ 文件不存在: {args.render}")
            sys.exit(1)
        text = path.read_text(encoding="utf-8")
        
        # 提取标题
        title_match = re.search(r'^#\s+(.+)', text, re.MULTILINE)
        title = title_match.group(1) if title_match else path.stem
        
        html = render_html(text, title)
        output_path = args.output or path.with_suffix(".html")
        Path(output_path).write_text(html, encoding="utf-8")
        print(f"✅ HTML已生成: {output_path}")
        return
    
    # --- 无参数 ---
    parser.print_help()


if __name__ == "__main__":
    main()
