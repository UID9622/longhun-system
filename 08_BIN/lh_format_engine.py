#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
🐉 龍魂智能排版引擎 v1.0 — Smart Formatting Engine
让系统输出自动兼容: Mermaid流程图 · Markdown · Python/CNSH代码 · 表格 · 时间线

DNA: #龍芯⚡️丙午·丙申·庚戌·午时·䷙大畜-FORMAT-ENGINE-v1.0
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

功能:
  1. 自动识别输入内容类型（代码/流程图/表格/列表/普通文本）
  2. 自动选择输出模板（Mermaid/Python/Markdown/CNSH）
  3. 统一添加DNA追溯、时间戳、主权锚定
  4. 支持终端彩色输出、HTML网页嵌入、Markdown导出

用法:
  作为库: from lh_format_engine import format_output
  命令行: python lh_format_engine.py --input "输入文本" --type auto
  lh命令: lh --format "开始→处理→结束" --type flowchart
"""

import re
import json
import hashlib
from datetime import datetime
from typing import Dict, Optional, Any
from enum import Enum
import sys
import os

# ============================================================
# 时间戳焊死
# ============================================================
try:
    # 尝试导入时间引擎获取干支+卦象
    ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, os.path.join(ROOT, "bin"))
    from lh_time_engine import get_output_stamp
    TIME_STAMP = get_output_stamp(format_type="simple")
except Exception:
    TIME_STAMP = "🐉丙午·庚戌·䷙大畜"

# ============================================================
# DNA追溯
# ============================================================
DNA_PREFIX = "#龍芯⚡️丙午·丙申·庚戌·午时·䷙大畜"

def generate_dna(module: str = "FORMAT") -> str:
    h = hashlib.sha256(f"{module}{datetime.now().isoformat()}".encode()).hexdigest()[:8].upper()
    return f"{DNA_PREFIX}-{module}-UID9622-{h}"

# ============================================================
# 格式类型枚举
# ============================================================

class FormatType(Enum):
    UNKNOWN = "unknown"
    CODE_PYTHON = "code_python"
    CODE_CNSH = "code_cnsh"
    CODE_JAVASCRIPT = "code_javascript"
    CODE_BASH = "code_bash"
    CODE_SQL = "code_sql"
    CODE_YAML = "code_yaml"
    FLOWCHART = "flowchart"        # Mermaid流程图
    SEQUENCE = "sequence"          # Mermaid时序图
    CLASS_DIAGRAM = "class_diagram"
    GANTT = "gantt"                # 甘特图
    STATE_DIAGRAM = "state_diagram"
    TABLE = "table"
    LIST = "list"
    TIMELINE = "timeline"
    MARKDOWN = "markdown"
    JSON_DATA = "json"
    PROSE = "prose"                # 普通文本
    MINDMAP = "mindmap"            # 思维导图

# ============================================================
# 格式识别器
# ============================================================

class FormatDetector:
    """自动识别输入内容的格式类型"""

    PATTERNS = {
        FormatType.CODE_PYTHON: [
            r'^\s*(import\s+\w+|from\s+\w+\s+import)',
            r'^\s*def\s+\w+\s*\(.*\)\s*:',
            r'^\s*class\s+\w+\s*[:\(]',
            r'^\s*print\(',
            r'^\s*(if|elif|else)\s+.*:',
            r'^\s*(for|while)\s+.*:',
            r'^\s*(with|async|await)\s+',
            r'^\s*@\w+',
        ],
        FormatType.CODE_CNSH: [
            r'^\s*函数\s+\w+\s*\(.*\)',
            r'^\s*类\s+\w+',
            r'^\s*如果\s+.*:',
            r'^\s*循环\s+.*:',
            r'^\s*输出\(',
            r'^\s*返回\s+',
            r'^\s*导入\s+',
            r'^\s*定义\s+',
        ],
        FormatType.CODE_JAVASCRIPT: [
            r'^\s*(function|const|let|var)\s+\w+',
            r'^\s*console\.(log|error|warn)',
            r'^\s*export\s+(default\s+)?',
            r'^\s*import\s+.*\s+from\s+',
            r'^\s*(async\s+)?\w+\s*=\s*\(.*\)\s*=>',
        ],
        FormatType.CODE_BASH: [
            r'^#!(/bin/|/usr/bin/)',
            r'^\s*echo\s+',
            r'^\s*export\s+\w+=',
            r'^\s*sudo\s+',
            r'^\s*\$\{.*\}',
            r'^\s*(cd|ls|mkdir|rm|cp|mv)\s+',
        ],
        FormatType.CODE_SQL: [
            r'^\s*(SELECT|INSERT|UPDATE|DELETE|CREATE|ALTER|DROP)\s+',
        ],
        FormatType.CODE_YAML: [
            r'^\s*\w+:\s*$',
            r'^\s*-\s+\w+:',
        ],
        FormatType.FLOWCHART: [
            r'[开始|流程|步骤|节点|判断|结束|输入|输出]',
            r'[├└│─]',
            r'→.*→',
        ],
        FormatType.SEQUENCE: [
            r'->>|-->|->',
            r'participant\s+',
            r'(用户|系统|API|服务器|客户端)\s*[-=]>',
        ],
        FormatType.GANTT: [
            r'(甘特|周计划|月计划|排期|进度|里程碑)',
            r'(第[一二三四五六七八九十\d]+周|Week\s*\d+)',
        ],
        FormatType.MINDMAP: [
            r'(思维导图|脑图|大纲|mindmap)',
            r'^\s*[-*]\s+.*\n\s{2,}[-*]\s+',
        ],
        FormatType.TABLE: [
            r'\|.*\|.*\|',
            r'\+\-+\+.*\|',
        ],
        FormatType.LIST: [
            r'^\s*[-*+]\s+',
            r'^\s*\d+[.、)]\s+',
        ],
        FormatType.JSON_DATA: [
            r'^\s*[\[{].*[\]}]\s*$',
            r'"\w+":\s*("[^"]*"|\d+|true|false|null)',
        ],
        FormatType.TIMELINE: [
            r'\d{4}[-/年]\d{1,2}[-/月]\d{1,2}[日号]',
            r'(上午|下午|晚上|凌晨)\d{1,2}:\d{2}',
            r'(昨天|今天|明天|上周|下周)',
        ],
    }

    @classmethod
    def detect(cls, text: str) -> FormatType:
        """检测文本格式类型"""
        lines = text.strip().split('\n')
        if not lines:
            return FormatType.PROSE

        # 先全局检查——看是否已有markdown代码块标记
        if text.strip().startswith('```') or '```' in text:
            # 提取代码块语言标签
            m = re.match(r'^```(\w+)', text.strip())
            if m:
                lang = m.group(1).lower()
                lang_map = {
                    'python': FormatType.CODE_PYTHON,
                    'cnsh': FormatType.CODE_CNSH,
                    'javascript': FormatType.CODE_JAVASCRIPT,
                    'js': FormatType.CODE_JAVASCRIPT,
                    'bash': FormatType.CODE_BASH,
                    'sh': FormatType.CODE_BASH,
                    'sql': FormatType.CODE_SQL,
                    'yaml': FormatType.CODE_YAML,
                    'yml': FormatType.CODE_YAML,
                    'json': FormatType.JSON_DATA,
                    'mermaid': FormatType.FLOWCHART,
                }
                if lang in lang_map:
                    return lang_map[lang]
            return FormatType.MARKDOWN

        # 前10行逐行检测
        scores = {}
        for line in lines[:10]:
            line = line.strip()
            if not line:
                continue
            for fmt, patterns in cls.PATTERNS.items():
                for pattern in patterns:
                    if re.search(pattern, line, re.IGNORECASE):
                        scores[fmt] = scores.get(fmt, 0) + 1
                        # CNSH关键字一票优先
                        if fmt == FormatType.CODE_CNSH:
                            return fmt

        if not scores:
            # 全文本分析
            full_text = text.strip()
            if '→' in full_text and ('开始' in full_text or '结束' in full_text or '流程' in full_text):
                return FormatType.FLOWCHART
            if '→' in full_text and ('->>' in full_text or '用户' in full_text or '系统' in full_text):
                return FormatType.SEQUENCE
            if re.search(r'\|.*\|.*\|', full_text):
                return FormatType.TABLE
            if re.match(r'^\s*[-*+]\s+', full_text):
                return FormatType.LIST
            return FormatType.PROSE

        # 最高分
        best = max(scores, key=scores.get)
        return best


# ============================================================
# 排版引擎核心
# ============================================================

class FormattingEngine:
    """智能排版引擎"""

    def __init__(self, dna: str = None):
        self.dna = dna or generate_dna()
        self.timestamp = datetime.now().isoformat()

    def format(self, content: str, target_type: Optional[FormatType] = None) -> Dict:
        """
        主入口：自动识别 + 排版
        返回：{"type": "xxx", "rendered": "xxx", "raw": "xxx", "dna": "xxx"}
        """
        # 1. 识别格式
        if target_type:
            fmt_type = target_type
        else:
            fmt_type = FormatDetector.detect(content)

        # 2. 根据类型选择排版方式
        renderers = {
            FormatType.CODE_PYTHON: self._render_code("python", content),
            FormatType.CODE_CNSH: self._render_code_cnsh,
            FormatType.CODE_JAVASCRIPT: self._render_code("javascript", content),
            FormatType.CODE_BASH: self._render_code("bash", content),
            FormatType.CODE_SQL: self._render_code("sql", content),
            FormatType.CODE_YAML: self._render_code("yaml", content),
            FormatType.FLOWCHART: self._render_flowchart,
            FormatType.SEQUENCE: self._render_sequence,
            FormatType.CLASS_DIAGRAM: self._render_class_diagram,
            FormatType.GANTT: self._render_gantt,
            FormatType.STATE_DIAGRAM: self._render_state_diagram,
            FormatType.TABLE: self._render_table,
            FormatType.LIST: self._render_list,
            FormatType.TIMELINE: self._render_timeline,
            FormatType.JSON_DATA: self._render_json,
            FormatType.PROSE: self._render_prose,
            FormatType.MARKDOWN: self._render_markdown,
            FormatType.MINDMAP: self._render_mindmap,
        }

        renderer = renderers.get(fmt_type, self._render_prose)
        if callable(renderer):
            rendered = renderer(content)
        else:
            rendered = renderer  # 已预计算

        # 3. 添加统一头尾
        final = self._wrap_output(rendered, fmt_type, content)

        return {
            "type": fmt_type.value,
            "rendered": final,
            "raw": content,
            "dna": self.dna,
            "timestamp": self.timestamp,
            "hash": hashlib.sha256(rendered.encode()).hexdigest()[:16]
        }

    # ============================================================
    # 各格式渲染器
    # ============================================================

    def _render_code(self, lang: str, content: str) -> str:
        """通用代码块渲染"""
        lines = [f"```{lang}", content.strip(), "```"]
        return "\n".join(lines)

    def _render_code_cnsh(self, content: str) -> str:
        """CNSH代码块（带DNA注释）"""
        lines = [
            "```cnsh",
            f"# DNA: {self.dna}",
            content.strip(),
            "```",
        ]
        return "\n".join(lines)

    def _render_flowchart(self, content: str) -> str:
        """自动生成 Mermaid 流程图"""
        text = content.strip()
        # 如果已经有 ```mermaid，直接返回
        if text.startswith("```mermaid"):
            return text

        lines = text.split('\n')
        nodes = {}
        edges = []
        node_id = 0

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # 检测 → 关系
            if '→' in line:
                parts = [p.strip() for p in re.split(r'[→]+', line)]
                # 过滤空白
                parts = [p for p in parts if p]
                for i in range(len(parts) - 1):
                    a = parts[i].replace(' ', '_')
                    b = parts[i + 1].replace(' ', '_')
                    if a not in nodes:
                        nodes[a] = f"n{len(nodes)}"
                    if b not in nodes:
                        nodes[b] = f"n{len(nodes)}"
                    edges.append(f"    {nodes[a]}[\"{parts[i]}\"] --> {nodes[b]}[\"{parts[i+1]}\"]")

            # 检测树形 ├ └ │
            elif re.search(r'[├└│]', line):
                clean = re.sub(r'[├└│─\s]+', ' ', line).strip()
                node_name = clean.replace(' ', '_')
                if node_name not in nodes:
                    nodes[node_name] = f"n{len(nodes)}"
                edges.append(f"    {nodes[node_name]}[\"{clean}\"]")

            # 独立节点
            elif line and not line.startswith('#') and not line.startswith('//'):
                node_name = line.replace(' ', '_')
                if node_name not in nodes:
                    nodes[node_name] = f"n{len(nodes)}"

        if not edges and len(nodes) > 1:
            # 自动串成链
            node_list = list(nodes.keys())
            for i in range(len(node_list) - 1):
                edges.append(f"    {nodes[node_list[i]]}[\"{node_list[i]}\"] --> {nodes[node_list[i+1]]}[\"{node_list[i+1]}\"]")

        mermaid_lines = ["```mermaid", "flowchart TD"]
        mermaid_lines.extend(edges if edges else ["    Start[开始] --> End[结束]"])
        mermaid_lines.append("```")
        return "\n".join(mermaid_lines)

    def _render_sequence(self, content: str) -> str:
        """Mermaid 时序图"""
        text = content.strip()
        if text.startswith("```mermaid"):
            return text

        lines = ["```mermaid", "sequenceDiagram"]
        for line in text.split('\n'):
            line = line.strip()
            if line and not line.startswith('#'):
                if '->>' in line or '-->' in line or '->' in line:
                    lines.append(f"    {line}")
                else:
                    lines.append(f"    participant {line}")
        lines.append("```")
        return "\n".join(lines)

    def _render_class_diagram(self, content: str) -> str:
        """Mermaid 类图"""
        text = content.strip()
        if text.startswith("```mermaid"):
            return text
        lines = ["```mermaid", "classDiagram"]
        for line in text.split('\n'):
            line = line.strip()
            if line:
                lines.append(f"    {line}")
        lines.append("```")
        return "\n".join(lines)

    def _render_gantt(self, content: str) -> str:
        """Mermaid 甘特图"""
        text = content.strip()
        if text.startswith("```mermaid"):
            return text
        lines = ["```mermaid", "gantt", "    title 项目计划", "    dateFormat  YYYY-MM-DD"]
        for line in text.split('\n'):
            line = line.strip()
            if line and not line.startswith('#'):
                lines.append(f"    {line}")
        lines.append("```")
        return "\n".join(lines)

    def _render_state_diagram(self, content: str) -> str:
        """Mermaid 状态图"""
        text = content.strip()
        if text.startswith("```mermaid"):
            return text
        lines = ["```mermaid", "stateDiagram-v2"]
        for line in text.split('\n'):
            line = line.strip()
            if line and '-->' in line:
                lines.append(f"    {line}")
        lines.append("```")
        return "\n".join(lines)

    def _render_mindmap(self, content: str) -> str:
        """Mermaid 思维导图"""
        text = content.strip()
        if text.startswith("```mermaid"):
            return text
        lines = ["```mermaid", "mindmap"]
        for line in text.split('\n'):
            line = line.strip()
            if line:
                # 计算缩进层级
                indent = len(line) - len(line.lstrip('-* '))
                level = max(1, indent // 2)
                prefix = "  " * level
                clean_line = re.sub(r'^[-*\s]+', '', line)
                lines.append(f"{prefix}{clean_line}")
        lines.append("```")
        return "\n".join(lines)

    def _render_table(self, content: str) -> str:
        """Markdown 表格增强"""
        text = content.strip()
        if '|' in text:
            return text
        # 尝试把对齐文本转成表格
        lines = text.split('\n')
        if len(lines) >= 2:
            # 简单检测：逗号/制表符分隔
            if '\t' in lines[0] or (',' in lines[0] and len(lines[0].split(',')) >= 2):
                sep = '\t' if '\t' in lines[0] else ','
                headers = [h.strip() for h in lines[0].split(sep)]
                rows = []
                for line in lines[1:]:
                    cells = [c.strip() for c in line.split(sep)]
                    rows.append(cells)
                # 生成 markdown 表格
                md_lines = ['| ' + ' | '.join(headers) + ' |']
                md_lines.append('| ' + ' | '.join(['---'] * len(headers)) + ' |')
                for row in rows:
                    # 补齐列
                    while len(row) < len(headers):
                        row.append('')
                    md_lines.append('| ' + ' | '.join(row[:len(headers)]) + ' |')
                return '\n'.join(md_lines)
        return text

    def _render_list(self, content: str) -> str:
        """保持列表格式，规范化为 Markdown"""
        return content.strip()

    def _render_timeline(self, content: str) -> str:
        """时间线格式 → Mermaid timeline"""
        text = content.strip()
        if text.startswith("```mermaid"):
            return text

        lines = ["```mermaid", "timeline"]
        # 按行检测日期前缀
        for line in text.split('\n'):
            line = line.strip()
            if not line:
                continue
            # 检测日期格式
            date_match = re.match(r'(\d{4}[-/]\d{1,2}[-/]\d{1,2})', line)
            if date_match:
                date = date_match.group(1)
                rest = line[date_match.end():].strip(' :：')
                lines.append(f"    {date} : {rest}")
            else:
                lines.append(f"    {line}")
        lines.append("```")
        return "\n".join(lines)

    def _render_json(self, content: str) -> str:
        """JSON 格式化输出"""
        try:
            data = json.loads(content)
            formatted = json.dumps(data, ensure_ascii=False, indent=2)
            return f"```json\n{formatted}\n```"
        except (json.JSONDecodeError, ValueError):
            return content.strip()

    def _render_markdown(self, content: str) -> str:
        """Markdown 原样输出，但规范化"""
        return content.strip()

    def _render_prose(self, content: str) -> str:
        """普通文本 → 段落格式，增强排版"""
        paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]
        return "\n\n".join(paragraphs)

    # ============================================================
    # 统一包装器
    # ============================================================

    def _wrap_output(self, content: str, fmt_type: FormatType, raw: str) -> str:
        """添加 DNA 追溯 + 时间戳 + 格式标记"""

        # 图标映射
        fmt_icons = {
            FormatType.CODE_PYTHON: "🐍",
            FormatType.CODE_CNSH: "🐉",
            FormatType.CODE_JAVASCRIPT: "📜",
            FormatType.CODE_BASH: "💻",
            FormatType.CODE_SQL: "🗄️",
            FormatType.CODE_YAML: "⚙️",
            FormatType.FLOWCHART: "📊",
            FormatType.SEQUENCE: "🔄",
            FormatType.CLASS_DIAGRAM: "🏗️",
            FormatType.GANTT: "📅",
            FormatType.STATE_DIAGRAM: "🔀",
            FormatType.MINDMAP: "🧠",
            FormatType.TABLE: "📋",
            FormatType.LIST: "📝",
            FormatType.TIMELINE: "⏱️",
            FormatType.JSON_DATA: "📦",
            FormatType.MARKDOWN: "📄",
            FormatType.PROSE: "✍️",
        }
        icon = fmt_icons.get(fmt_type, "📌")

        lines = [
            "---",
            f"🧬 DNA: {self.dna}",
            f"{icon} 格式: {fmt_type.value}",
            f"⏰ 时间: {self.timestamp}",
            f"🔐 确认: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z",
            f"🛡️ 主权: 中国自主知识产权 · CC BY-NC-SA 4.0",
            "---",
            "",
            content,
            "",
            "---",
            f"📥 原始输入: {len(raw)} 字符",
            f"📤 输出哈希: {hashlib.sha256(content.encode()).hexdigest()[:16]}",
            f"  {TIME_STAMP}",
        ]
        return "\n".join(lines)


# ============================================================
# 终端彩色输出
# ============================================================

class TerminalFormatter:
    """终端彩色输出"""

    COLORS = {
        "red": "\033[91m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "magenta": "\033[95m",
        "cyan": "\033[96m",
        "white": "\033[97m",
        "reset": "\033[0m",
        "bold": "\033[1m",
        "dim": "\033[2m",
    }

    @classmethod
    def _use_color(cls) -> bool:
        """检测终端是否支持颜色"""
        return hasattr(sys.stdout, 'isatty') and sys.stdout.isatty()

    @classmethod
    def colorize(cls, text: str, color: str = "white", bold: bool = False) -> str:
        if not cls._use_color():
            return text
        prefix = cls.COLORS.get(color, "") + (cls.COLORS["bold"] if bold else "")
        return f"{prefix}{text}{cls.COLORS['reset']}"

    @classmethod
    def print_rendered(cls, result: Dict):
        """打印排版结果到终端"""
        print(cls.colorize("=" * 60, "cyan", bold=True))
        print(cls.colorize(f"🧬 DNA: {result['dna']}", "yellow"))
        print(cls.colorize(f"📌 格式: {result['type']}", "green"))
        print(cls.colorize(f"⏰ 时间: {result['timestamp']}", "dim"))
        print(cls.colorize("=" * 60, "cyan", bold=True))
        print(result['rendered'])
        print(cls.colorize("=" * 60, "cyan", bold=True))


# ============================================================
# 便捷函数
# ============================================================

def format_output(content: str, target_type: Optional[str] = None, raw: bool = False) -> Dict:
    """
    便捷调用入口

    Args:
        content: 待排版的内容
        target_type: 可选 'auto', 'python', 'cnsh', 'javascript', 'bash',
                     'sql', 'yaml', 'flowchart', 'sequence', 'class_diagram',
                     'gantt', 'state_diagram', 'mindmap', 'table', 'list',
                     'timeline', 'json', 'markdown', 'prose'
        raw: 是否只输出内容不含DNA头

    Returns:
        {"type": "xxx", "rendered": "xxx", "raw": "xxx", "dna": "xxx"}
    """
    type_map = {
        "auto": None,
        "python": FormatType.CODE_PYTHON,
        "cnsh": FormatType.CODE_CNSH,
        "javascript": FormatType.CODE_JAVASCRIPT,
        "js": FormatType.CODE_JAVASCRIPT,
        "bash": FormatType.CODE_BASH,
        "sh": FormatType.CODE_BASH,
        "sql": FormatType.CODE_SQL,
        "yaml": FormatType.CODE_YAML,
        "yml": FormatType.CODE_YAML,
        "flowchart": FormatType.FLOWCHART,
        "sequence": FormatType.SEQUENCE,
        "class_diagram": FormatType.CLASS_DIAGRAM,
        "class": FormatType.CLASS_DIAGRAM,
        "gantt": FormatType.GANTT,
        "state_diagram": FormatType.STATE_DIAGRAM,
        "state": FormatType.STATE_DIAGRAM,
        "mindmap": FormatType.MINDMAP,
        "table": FormatType.TABLE,
        "list": FormatType.LIST,
        "timeline": FormatType.TIMELINE,
        "json": FormatType.JSON_DATA,
        "markdown": FormatType.MARKDOWN,
        "md": FormatType.MARKDOWN,
        "prose": FormatType.PROSE,
        "text": FormatType.PROSE,
    }
    fmt = type_map.get(target_type) if target_type else None
    engine = FormattingEngine()
    result = engine.format(content, fmt)

    if raw:
        # 提取纯内容（去掉DNA包装）
        rendered = result['rendered']
        # 提取 --- --- 之间的内容
        parts = rendered.split('---\n')
        if len(parts) >= 5:
            result['rendered'] = parts[3].strip() + '\n\n' + parts[4].split('---')[0].strip()

    return result


# ============================================================
# 命令行入口
# ============================================================

def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="🐉 龍魂智能排版引擎 v1.0",
        epilog="示例: lh --format '开始→处理→结束' --type flowchart"
    )
    parser.add_argument("--input", "-i", type=str, help="输入内容")
    parser.add_argument("--file", "-f", type=str, help="从文件读取输入")
    parser.add_argument("--type", "-t", type=str,
                        choices=['auto', 'python', 'cnsh', 'javascript', 'js', 'bash', 'sh',
                                 'sql', 'yaml', 'yml', 'flowchart', 'sequence',
                                 'class_diagram', 'class', 'gantt', 'state_diagram', 'state',
                                 'mindmap', 'table', 'list', 'timeline',
                                 'json', 'markdown', 'md', 'prose', 'text'],
                        default='auto',
                        help="输出格式类型（默认自动识别）")
    parser.add_argument("--output", "-o", type=str, help="输出到文件")
    parser.add_argument("--raw", action="store_true", help="只输出内容（不含DNA头尾）")
    parser.add_argument("--list-types", action="store_true", help="列出所有支持的格式类型")

    args = parser.parse_args()

    if args.list_types:
        print("🐉 龍魂排版引擎 · 支持的格式类型\n")
        print("  📊 图表类: flowchart, sequence, class_diagram, gantt, state_diagram, mindmap")
        print("  💻 代码类: python, cnsh, javascript, bash, sql, yaml")
        print("  📋 数据类: table, list, json")
        print("  📄 文本类: markdown, prose, timeline")
        print("  🤖 自动识别: auto\n")
        return

    # 读取输入
    if args.file:
        with open(args.file, 'r', encoding='utf-8') as f:
            content = f.read()
    elif args.input:
        content = args.input
    else:
        content = sys.stdin.read()

    if not content.strip():
        print("❌ 请输入内容（--input 或 --file 或 管道）")
        sys.exit(1)

    # 执行排版
    target = None if args.type == 'auto' else args.type
    result = format_output(content, target, raw=args.raw)

    # 输出
    output = result['rendered']

    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(output)
        print(f"✅ 已保存到: {args.output}")
    else:
        TerminalFormatter.print_rendered(result)


if __name__ == "__main__":
    main()
