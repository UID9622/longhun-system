#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂·文档结构审计引擎 v2.0 · 左右互搏升级版
DNA: #龍芯⚡️丙午·丙申·戊申·亥时·䷗复-DOC-STRUCTURE-AUDIT-v2.0
创建者: 诸葛鑫（UID9622）
协议: MulanPSL v2

升级内容（v2.0）:
  1. 结构化完整性检测：TOC锚点、章节编号、层级一致性
  2. 代码截断检测：Python/JS/HTML 代码块完整性验证
  3. 可视化完备性：Mermaid/架构图/运行示例缺失检测
  4. 元数据完备性：DNA/版本号/Changelog/Tags/分类检测
  5. 内容补全建议：基于场景自动推理缺失区块
  6. 严重度分级：🔴致命 🟡重要 🟢建议 三级判定

用法:
  python3 08_BIN/lh_doc_structure_audit.py audit --target path/to/doc.md
  python3 08_BIN/lh_doc_structure_audit.py audit --target path/to/code.py --type python
  python3 08_BIN/lh_doc_structure_audit.py check-truncation --target path/to/code.py
  python3 08_BIN/lh_doc_structure_audit.py suggest --target path/to/doc.md
"""

import os
import sys
import re
import json
import hashlib
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Any, Tuple


# ═══════════════════════════════════════════════════════════════════════════════
# P0 配置
# ═══════════════════════════════════════════════════════════════════════════════

P0_CONFIG = {
    "uid": "9622",
    "dna": "#龍芯⚡️丙午·丙申·戊申·亥时·䷗复-DOC-STRUCTURE-AUDIT-v2.0",
    "confirm": "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z",
    "gpg": "A2D0092CEE2E5BA87035600924C3704A8CC26D5F",
}

# ═══════════════════════════════════════════════════════════════════════════════
# 严重度枚举
# ═══════════════════════════════════════════════════════════════════════════════

class Severity(Enum):
    FATAL = ("🔴", "致命")
    IMPORTANT = ("🟡", "重要")
    SUGGESTION = ("🟢", "建议")

    @property
    def icon(self) -> str:
        return self.value[0]

    @property
    def label(self) -> str:
        return self.value[1]


@dataclass
class Finding:
    """审计发现"""
    id: str
    category: str
    severity: Severity
    title: str
    detail: str
    suggestion: str = ""
    line: int = 0
    code_context: str = ""

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "category": self.category,
            "severity": self.severity.label,
            "severity_icon": self.severity.icon,
            "title": self.title,
            "detail": self.detail,
            "suggestion": self.suggestion,
            "line": self.line,
            "code_context": self.code_context,
        }


@dataclass
class AuditReport:
    """审计报告"""
    dna: str
    target: str
    target_type: str
    audited_at: str
    summary: Dict[str, int]
    findings: List[Finding]
    suggestions: List[Dict[str, str]]
    score: float
    color: str

    def to_dict(self) -> Dict:
        return {
            "dna": self.dna,
            "target": self.target,
            "target_type": self.target_type,
            "audited_at": self.audited_at,
            "summary": self.summary,
            "findings": [f.to_dict() for f in self.findings],
            "suggestions": self.suggestions,
            "score": self.score,
            "color": self.color,
        }


# ═══════════════════════════════════════════════════════════════════════════════
# Markdown 文档结构审计
# ═══════════════════════════════════════════════════════════════════════════════

class MarkdownAuditor:
    """Markdown 文档结构审计器"""

    # 必检块定义：每种文档类型预期的章节/区块
    TECH_ARTICLE_SECTIONS = [
        ("封面/抬头", ["DNA", "确认码", "GPG", "创建者"], Severity.IMPORTANT),
        ("摘要/导读", ["摘要", "导读", "一句话", "阅读对象"], Severity.IMPORTANT),
        ("目录/TOC", ["目录", "TOC", "## 目录"], Severity.IMPORTANT),
        ("正文章节", ["## ", "### "], Severity.FATAL),
        ("代码示例", ["```", "代码", "源码"], Severity.FATAL),
        ("运行方式", ["运行", "安装", "依赖", "pip install", "python3"], Severity.IMPORTANT),
        ("运行示例输出", ["输出示例", "运行示例", "预期输出", "结果"], Severity.IMPORTANT),
        ("架构图", ["mermaid", "架构图", "流程图", "```mermaid"], Severity.IMPORTANT),
        ("版本/变更日志", ["版本", "changelog", "更新日志", "修订记录"], Severity.SUGGESTION),
        ("版权/协议声明", ["协议", "CC BY", "MulanPSL", "版权", "License"], Severity.SUGGESTION),
        ("标签/分类", ["标签", "tags", "分类", "categories"], Severity.SUGGESTION),
        ("签名区", ["签名", "DNA签名", "最终签名"], Severity.SUGGESTION),
    ]

    PROJECT_DOC_SECTIONS = [
        ("项目说明", ["简介", "README", "概述"], Severity.FATAL),
        ("安装说明", ["安装", "install", "配置"], Severity.IMPORTANT),
        ("使用说明", ["使用", "用法", "usage"], Severity.IMPORTANT),
        ("API文档", ["API", "接口", "endpoint"], Severity.IMPORTANT),
        ("贡献指南", ["贡献", "contributing"], Severity.SUGGESTION),
        ("许可证", ["license", "协议"], Severity.SUGGESTION),
    ]

    def __init__(self, content: str, doc_type: str = "auto"):
        self.content = content
        self.lines = content.split("\n")
        self.doc_type = self._detect_type(doc_type)
        self.findings: List[Finding] = []
        self._finding_counter = 0

    def _detect_type(self, hint: str) -> str:
        if hint != "auto":
            return hint
        # 启发式检测
        if "## " in self.content and ("```python" in self.content or "```java" in self.content):
            return "tech_article"
        if any(k in self.content.lower()[:500] for k in ["readme", "项目", "project"]):
            return "project_doc"
        return "general_md"

    def _next_id(self) -> str:
        self._finding_counter += 1
        return f"F{self._finding_counter:03d}"

    def _add_finding(self, category: str, severity: Severity, title: str, detail: str, suggestion: str = "", line: int = 0):
        self.findings.append(Finding(
            id=self._next_id(),
            category=category,
            severity=severity,
            title=title,
            detail=detail,
            suggestion=suggestion,
            line=line,
        ))

    def check_toc_anchors(self) -> List[Finding]:
        """检查 TOC 锚点与实际章节的对应关系"""
        findings_start = len(self.findings)

        # 提取 TOC 中的锚点
        toc_section = ""
        in_toc = False
        for line in self.lines:
            if re.match(r"^#{1,3}\s*(目[录錄]|TOC|Table of Contents)", line, re.IGNORECASE):
                in_toc = True
                continue
            if in_toc and re.match(r"^#{1,3}\s", line) and "目录" not in line and "TOC" not in line:
                break
            if in_toc:
                toc_section += line + "\n"

        # 提取正文中的锚点目标
        heading_ids = set()
        for i, line in enumerate(self.lines):
            m = re.match(r"^(#{1,4})\s+(.+)", line)
            if m:
                heading_text = m.group(2).strip()
                # 模拟 CSDN/GitHub 风格的锚点 ID
                anchor_id = heading_text.lower()
                anchor_id = re.sub(r'[^\w\u4e00-\u9fff\s-]', '', anchor_id)
                anchor_id = re.sub(r'\s+', '-', anchor_id)
                heading_ids.add(anchor_id)

        # 检查 TOC 链接
        toc_links = re.findall(r'\(#([^)]+)\)', toc_section)
        broken_links = []
        for link in toc_links:
            if link not in heading_ids and not any(link in hid or hid in link for hid in heading_ids):
                broken_links.append(link)

        if broken_links:
            self._add_finding(
                "TOC锚点",
                Severity.IMPORTANT,
                f"TOC 存在 {len(broken_links)} 个断链",
                f"断链: {', '.join(broken_links[:5])}",
                "CSDN 中文锚点会转码，建议用英文锚点或验证渲染后的实际 ID",
            )
        elif toc_section.strip():
            pass  # TOC 锚点正常，不报警
        else:
            self._add_finding(
                "TOC锚点",
                Severity.SUGGESTION,
                "未检测到 TOC/目录区块",
                "建议添加 Markdown 锚点目录便于跳转",
                "使用 ## 目录 + [章节名](#锚点) 格式",
            )

        return self.findings[findings_start:]

    def check_section_completeness(self) -> List[Finding]:
        """检查预期章节是否完整"""
        findings_start = len(self.findings)

        sections_to_check = []
        if self.doc_type == "tech_article":
            sections_to_check = self.TECH_ARTICLE_SECTIONS
        elif self.doc_type == "project_doc":
            sections_to_check = self.PROJECT_DOC_SECTIONS

        for section_name, keywords, default_severity in sections_to_check:
            found = False
            for kw in keywords:
                if kw in self.content:
                    found = True
                    break
            if not found:
                self._add_finding(
                    "结构完整",
                    default_severity,
                    f"缺少区块: {section_name}",
                    f"技术文档应包含 {section_name} 区块（关键词: {', '.join(keywords[:3])}）",
                    f"建议补充 {section_name} 相关内容",
                )

        return self.findings[findings_start:]

    def check_code_blocks_integrity(self) -> List[Finding]:
        """检查代码块是否完整（未被截断）"""
        findings_start = len(self.findings)

        # 检查 ``` 是否成对
        lines_with_backticks = []
        for i, line in enumerate(self.lines):
            if line.strip().startswith("```"):
                lines_with_backticks.append((i + 1, line.strip()))

        open_blocks = []
        for lineno, line in lines_with_backticks:
            marker = line.strip()
            if marker == "```":
                # 裸 ``` 可以是开也可以是关。已打开时优先当闭合（Markdown 标准）
                if open_blocks:
                    open_blocks.pop()
                else:
                    open_blocks.append((lineno, "", "```"))
            elif marker.startswith("```"):
                lang = marker[3:].strip()
                # ```language 一定是新开一个代码块；已打开时先闭合旧的再开新的
                if open_blocks:
                    open_blocks.pop()
                open_blocks.append((lineno, lang, marker))

        for lineno, lang, marker in open_blocks:
            self._add_finding(
                "代码截断",
                Severity.FATAL,
                f"代码块在第 {lineno} 行未关闭",
                f"```{lang} 缺少对应的闭合 ```",
                "请检查代码块是否完整，补充缺失的闭合标记",
                line=lineno,
            )

        # Python 代码块特定检查
        python_blocks = []
        in_python = False
        block_start = 0
        block_lines = []

        for i, line in enumerate(self.lines):
            if line.strip().startswith("```python") or line.strip().startswith("```py"):
                in_python = True
                block_start = i + 1
                block_lines = []
                continue
            if in_python and line.strip() == "```":
                in_python = False
                python_blocks.append((block_start, block_lines))
                block_lines = []
                continue
            if in_python:
                block_lines.append(line)

        # 检查每个 Python 代码块的完整性
        for start_line, lines_list in python_blocks:
            full_code = "\n".join(lines_list)

            # 检查 if __name__ == "__main__": 后面是否有内容
            if re.search(r'if\s+__name__\s*==\s*["\']__main__["\']\s*:\s*$', full_code, re.MULTILINE):
                main_match = re.search(r'(if\s+__name__\s*==\s*["\']__main__["\']\s*:.*)', full_code)
                if main_match:
                    main_idx = full_code.find(main_match.group(1))
                    after_main = full_code[main_idx + len(main_match.group(1)):]
                    if not after_main.strip():
                        self._add_finding(
                            "代码截断",
                            Severity.IMPORTANT,
                            f"Python 代码块（第 {start_line} 行起）的 __main__ 入口可能为空",
                            "if __name__ == '__main__': 之后无执行代码",
                            "补充 main() 调用或直接执行逻辑",
                            line=start_line,
                        )

            # 检测语法截断（括号不匹配、def/class 未闭合等）
            indent_level = 0
            last_indent = 0
            for j, code_line in enumerate(lines_list):
                stripped = code_line.strip()
                if not stripped:
                    continue
                # 跟踪缩进层级
                current_indent = len(code_line) - len(code_line.lstrip())
                if current_indent > last_indent + 4 and j > 0:
                    pass  # 正常缩进
                last_indent = current_indent

            # 检查是否以未闭合的括号结尾
            last_non_empty = ""
            for line in reversed(lines_list):
                if line.strip():
                    last_non_empty = line.strip()
                    break
            open_parens = last_non_empty.count("(") - last_non_empty.count(")")
            open_brackets = last_non_empty.count("[") - last_non_empty.count("]")
            open_braces = last_non_empty.count("{") - last_non_empty.count("}")
            if open_parens > 0 or open_brackets > 0 or open_braces > 0:
                self._add_finding(
                    "代码截断",
                    Severity.FATAL,
                    f"Python 代码块末尾存在未闭合的括号/方括号/花括号",
                    f"末行: {last_non_empty[:80]}... | 未闭合: (={open_parens} [={open_brackets} {{{open_braces}",
                    "代码块可能被截断，请检查完整源码",
                    line=start_line + len(lines_list),
                )

        return self.findings[findings_start:]

    def check_visual_aids(self) -> List[Finding]:
        """检查可视化元素（架构图/运行截图）"""
        findings_start = len(self.findings)

        has_mermaid = "```mermaid" in self.content
        has_image = bool(re.search(r'!\[.*\]\(.+\)', self.content))
        has_ascii_diagram = bool(re.search(r'[┌┐└┘├┤│─┬┴┼╔╗╚╝║═]+', self.content))

        # 如果有大量代码但无架构图
        code_block_count = len(re.findall(r'```\w*\n', self.content))
        if code_block_count > 2 and not has_mermaid and not has_image and not has_ascii_diagram:
            self._add_finding(
                "可视化",
                Severity.IMPORTANT,
                "缺少架构/流程图",
                f"文档包含 {code_block_count} 个代码块但无 Mermaid 架构图或截图",
                "建议添加 ```mermaid 架构图来直观展示系统结构",
            )

        return self.findings[findings_start:]

    def check_metadata(self) -> List[Finding]:
        """检查元数据完备性"""
        findings_start = len(self.findings)

        checks = {
            "DNA 签名": (r"#龍芯[⚡️]", "文档头部缺少 DNA 追溯码"),
            "版本号": (r"[vV](\d+\.\d+)", "缺少版本号标识"),
            "创建日期": (r"\d{4}[-/]\d{2}[-/]\d{2}", "缺少创建日期"),
            "GPG 签名": (r"A2D0092CEE2E5BA87035600924C3704A8CC26D5F", "缺少 GPG 签名（对外发布必填）"),
            "协议声明": (r"(CC BY|MulanPSL|MIT|Apache|GPL|BSD)", "缺少开源协议声明"),
        }

        for name, (pattern, detail) in checks.items():
            if not re.search(pattern, self.content):
                sev = Severity.IMPORTANT if name in ["DNA 签名", "协议声明"] else Severity.SUGGESTION
                self._add_finding(
                    "元数据",
                    sev,
                    f"缺少 {name}",
                    detail,
                    f"补充 {name} 信息",
                )

        return self.findings[findings_start:]

    def audit(self) -> AuditReport:
        """执行完整审计"""
        self.findings = []

        self.check_toc_anchors()
        self.check_section_completeness()
        self.check_code_blocks_integrity()
        self.check_visual_aids()
        self.check_metadata()

        # 统计
        fatal = sum(1 for f in self.findings if f.severity == Severity.FATAL)
        important = sum(1 for f in self.findings if f.severity == Severity.IMPORTANT)
        suggestion = sum(1 for f in self.findings if f.severity == Severity.SUGGESTION)

        # 评分
        base_score = 100.0
        penalty = fatal * 30 + important * 10 + suggestion * 3
        score = max(0, min(100, base_score - penalty))

        if fatal > 0:
            color = "🔴"
        elif important > 3 or score < 70:
            color = "🟡"
        else:
            color = "🟢"

        # 生成补全建议
        suggestions = self._generate_suggestions()

        return AuditReport(
            dna=P0_CONFIG["dna"],
            target="(inline content)",
            target_type=f"markdown ({self.doc_type})",
            audited_at=datetime.now().isoformat(),
            summary={"🔴致命": fatal, "🟡重要": important, "🟢建议": suggestion},
            findings=self.findings,
            suggestions=suggestions,
            score=score,
            color=color,
        )

    def _generate_suggestions(self) -> List[Dict[str, str]]:
        """基于缺失内容生成补全建议"""
        suggestions = []

        missing_categories = set(f.category for f in self.findings)
        finding_map = {}
        for f in self.findings:
            if f.category not in finding_map:
                finding_map[f.category] = []
            finding_map[f.category].append(f)

        if "结构完整" in missing_categories:
            missing_sections = [f.title.replace("缺少区块: ", "") for f in finding_map.get("结构完整", [])]
            if "架构图" in str(missing_sections) or "架构" in str(missing_sections):
                suggestions.append({
                    "type": "架构图模板",
                    "content": """```mermaid
graph TB
    subgraph 系统架构
        A[入口层] --> B[业务层]
        B --> C[数据层]
        C --> D[存储层]
    end
    B --> E[监控/审计]
    E --> F[告警/熔断]
```""",
                })

            if "运行示例输出" in str(missing_sections) or "运行示例" in str(missing_sections):
                suggestions.append({
                    "type": "运行示例输出模板",
                    "content": """```
$ python3 script.py

=== 系统初始化 ===
✅ 配置加载完成
✅ 服务启动成功

=== 运行结果 ===
状态: 🟢 正常
耗时: 1.23s
```""",
                })

        if "可视化" in missing_categories:
            suggestions.append({
                "type": "架构图建议",
                "content": "建议添加 Mermaid 架构图（```mermaid graph TB ... ```）来展示系统组件关系",
            })

        if "元数据" in missing_categories:
            suggestions.append({
                "type": "元数据补充模板",
                "content": """```
DNA: #龍芯⚡️YYYY-MM-DD-MODULE-ACTION-VERSION-UID9622
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0（思想层）/ MulanPSL v2（工程层）
版本: v1.0
标签: 龍魂系统, Python, 开源
```""",
            })

        if "代码截断" in missing_categories:
            suggestions.append({
                "type": "代码完整性检查",
                "content": "检测到代码块可能被截断。请验证: ① ``` 标记成对 ② 括号闭合 ③ def/class 完整 ④ 文件末尾有 main 入口",
            })

        return suggestions


# ═══════════════════════════════════════════════════════════════════════════════
# Python 代码结构审计
# ═══════════════════════════════════════════════════════════════════════════════

class PythonCodeAuditor:
    """Python 代码完整性审计器"""

    def __init__(self, content: str):
        self.content = content
        self.lines = content.split("\n")
        self.findings: List[Finding] = []
        self._finding_counter = 0

    def _next_id(self) -> str:
        self._finding_counter += 1
        return f"P{self._finding_counter:03d}"


    def _count_brackets_in_code(self) -> Tuple[int, int, int]:
        """智能括号计数 — 排除注释和字符串中的括号"""
        import tokenize
        import io

        # tokenize 中要排除的类型
        SKIP_TYPES = {
            tokenize.COMMENT,
            tokenize.STRING,
            tokenize.FSTRING_MIDDLE,  # f-string 中间文本段中的括号不算
            tokenize.NL,
            tokenize.NEWLINE,
            tokenize.ENDMARKER,
        }

        paren = bracket = brace = 0
        try:
            tokens = tokenize.generate_tokens(io.StringIO(self.content).readline)
            for tok in tokens:
                if tok.type in SKIP_TYPES:
                    continue
                paren += tok.string.count("(") - tok.string.count(")")
                bracket += tok.string.count("[") - tok.string.count("]")
                brace += tok.string.count("{") - tok.string.count("}")
        except Exception:
            # tokenize 失败时回退到简单计数
            for line in self.lines:
                stripped = line.strip()
                if stripped.startswith("#"):
                    continue
                paren += stripped.count("(") - stripped.count(")")
                bracket += stripped.count("[") - stripped.count("]")
                brace += stripped.count("{") - stripped.count("}")
        return paren, bracket, brace

    def check_truncation(self) -> List[Finding]:
        """检测代码是否被截断"""
        findings_start = len(self.findings)

        # 1. 括号/缩进完整性（智能计数排除注释和字符串）
        paren_balance, bracket_balance, brace_balance = self._count_brackets_in_code()

        if paren_balance != 0:
            self._add_finding("截断检测", Severity.FATAL,
                f"圆括号不平衡 ({'+' if paren_balance > 0 else ''}{paren_balance})",
                f"可能在第 {len(self.lines)} 行处被截断", "检查代码块末尾是否完整")

        if bracket_balance != 0:
            self._add_finding("截断检测", Severity.FATAL,
                f"方括号不平衡 ({'+' if bracket_balance > 0 else ''}{bracket_balance})",
                "方括号未闭合", "检查代码块是否被截断")

        if brace_balance != 0:
            self._add_finding("截断检测", Severity.FATAL,
                f"花括号不平衡 ({'+' if brace_balance > 0 else ''}{brace_balance})",
                "花括号未闭合（dict/set/f-string）", "检查代码块是否被截断")

        # 2. 三引号完整性
        triple_quotes_count = self.content.count('"""') + self.content.count("'''")
        if triple_quotes_count % 2 != 0:
            self._add_finding("截断检测", Severity.FATAL,
                "三引号 docstring 未闭合",
                "存在未配对的三引号", "检查文档字符串是否完整")

        # 3. 类/函数检测
        class_pattern = re.findall(r'^\s*class\s+(\w+)', self.content, re.MULTILINE)
        def_pattern = re.findall(r'^\s*def\s+(\w+)', self.content, re.MULTILINE)

        # 检查最后几行是否在类/函数体内
        last_indent = 0
        for line in reversed(self.lines):
            if line.strip() and not line.strip().startswith("#"):
                last_indent = len(line) - len(line.lstrip())
                break

        if last_indent > 0 and not self.lines[-1].strip():
            # 以缩进结束但最后是空行 — 可能被截断
            pass  # 不确定，不强制报警

        # 4. 检查文件末尾是否有完整的主入口
        has_main = bool(re.search(r'if\s+__name__\s*==\s*["\']__main__["\']', self.content))
        if has_main:
            main_pos = self.content.rfind('if __name__')
            after_main = self.content[main_pos:]
            # 检查 main 之后的非空行数
            after_main_lines = [l for l in after_main.split("\n") if l.strip() and not l.strip().startswith("#")]
            if len(after_main_lines) <= 1:
                self._add_finding("截断检测", Severity.IMPORTANT,
                    "__main__ 入口之后仅有少量代码",
                    "主入口可能不完整", "检查 main() 函数调用是否完整")

        return self.findings[findings_start:]

    def check_missing_classes(self, expected_modules: List[str] = None) -> List[Finding]:
        """检测文档中声明但代码中缺失的类/函数"""
        findings_start = len(self.findings)

        if not expected_modules:
            return []

        # 检查文档中提到的类名是否都在代码中
        defined_names = set()
        defined_names.update(re.findall(r'class\s+(\w+)', self.content))
        defined_names.update(re.findall(r'def\s+(\w+)', self.content))

        for module in expected_modules:
            if module not in defined_names:
                self._add_finding("缺失检测", Severity.FATAL,
                    f"类/函数 '{module}' 在文档中提到但代码中未定义",
                    f"预期应包含 {module} 的实现",
                    f"补充 {module} 类的完整实现代码")

        return self.findings[findings_start:]

    def audit(self, expected_modules: List[str] = None) -> AuditReport:
        """执行完整审计"""
        self.findings = []

        self.check_truncation()
        if expected_modules:
            self.check_missing_classes(expected_modules)

        fatal = sum(1 for f in self.findings if f.severity == Severity.FATAL)
        important = sum(1 for f in self.findings if f.severity == Severity.IMPORTANT)
        suggestion = sum(1 for f in self.findings if f.severity == Severity.SUGGESTION)

        score = max(0, 100 - fatal * 40 - important * 15 - suggestion * 5)

        if fatal > 0:
            color = "🔴"
        elif score < 70:
            color = "🟡"
        else:
            color = "🟢"

        return AuditReport(
            dna=P0_CONFIG["dna"],
            target="(inline python code)",
            target_type="python",
            audited_at=datetime.now().isoformat(),
            summary={"🔴致命": fatal, "🟡重要": important, "🟢建议": suggestion},
            findings=self.findings,
            suggestions=[],
            score=score,
            color=color,
        )


# ═══════════════════════════════════════════════════════════════════════════════
# HTML 页面结构审计
# ═══════════════════════════════════════════════════════════════════════════════

class HTMLAuditor:
    """HTML 页面结构审计器"""

    REQUIRED_ELEMENTS = [
        ("<title>", "缺少页面标题", Severity.FATAL),
        ("<meta charset", "缺少字符集声明", Severity.FATAL),
        ("<meta name=\"viewport\"", "缺少 viewport 声明（移动端适配）", Severity.IMPORTANT),
        ("<meta name=\"description\"", "缺少页面描述（SEO）", Severity.SUGGESTION),
        ("<meta name=\"keywords\"", "缺少关键词（SEO）", Severity.SUGGESTION),
        ("lang=", "缺少语言声明", Severity.SUGGESTION),
    ]

    def __init__(self, content: str):
        self.content = content
        self.findings: List[Finding] = []
        self._finding_counter = 0

    def _next_id(self) -> str:
        self._finding_counter += 1
        return f"H{self._finding_counter:03d}"

    def _add_finding(self, category: str, severity: Severity, title: str, detail: str, suggestion: str = ""):
        self.findings.append(Finding(
            id=self._next_id(),
            category=category,
            severity=severity,
            title=title,
            detail=detail,
            suggestion=suggestion,
        ))

    def audit(self) -> AuditReport:
        self.findings = []

        for keyword, detail, severity in self.REQUIRED_ELEMENTS:
            if keyword.lower() not in self.content.lower():
                self._add_finding("HTML结构", severity, detail, "缺少必需的 HTML 元素",
                                  f"添加 {keyword} 标签")

        # 检查 HTML 标签闭合
        open_tags = re.findall(r'<(?!area|base|br|col|embed|hr|img|input|link|meta|param|source|track|wbr)(\w+)', self.content)
        close_tags = re.findall(r'</(\w+)>', self.content)

        open_count = {}
        for tag in open_tags:
            open_count[tag] = open_count.get(tag, 0) + 1
        close_count = {}
        for tag in close_tags:
            close_count[tag] = close_count.get(tag, 0) + 1

        for tag in open_count:
            if open_count[tag] != close_count.get(tag, 0):
                diff = open_count[tag] - close_count.get(tag, 0)
                self._add_finding("HTML结构", Severity.FATAL if diff > 1 else Severity.IMPORTANT,
                    f"<{tag}> 标签未闭合 ({diff} 个未闭合)",
                    f"<{tag}> 出现 {open_count[tag]} 次，</{tag}> 出现 {close_count.get(tag, 0)} 次",
                    "检查并补充缺失的闭合标签")

        fatal = sum(1 for f in self.findings if f.severity == Severity.FATAL)
        important = sum(1 for f in self.findings if f.severity == Severity.IMPORTANT)
        suggestion = sum(1 for f in self.findings if f.severity == Severity.SUGGESTION)

        score = max(0, 100 - fatal * 35 - important * 10 - suggestion * 3)
        color = "🔴" if fatal > 0 else "🟡" if score < 70 else "🟢"

        return AuditReport(
            dna=P0_CONFIG["dna"],
            target="(inline html)",
            target_type="html",
            audited_at=datetime.now().isoformat(),
            summary={"🔴致命": fatal, "🟡重要": important, "🟢建议": suggestion},
            findings=self.findings,
            suggestions=[],
            score=score,
            color=color,
        )


# ═══════════════════════════════════════════════════════════════════════════════
# 统一审计入口
# ═══════════════════════════════════════════════════════════════════════════════

class DocStructureAuditHub:
    """文档结构审计中枢"""

    def __init__(self):
        self.markdown_auditor = None
        self.python_auditor = None
        self.html_auditor = None

    def audit_markdown(self, content: str, doc_type: str = "auto") -> AuditReport:
        self.markdown_auditor = MarkdownAuditor(content, doc_type)
        return self.markdown_auditor.audit()

    def audit_python(self, content: str, expected_modules: List[str] = None) -> AuditReport:
        self.python_auditor = PythonCodeAuditor(content)
        return self.python_auditor.audit(expected_modules)

    def audit_html(self, content: str) -> AuditReport:
        self.html_auditor = HTMLAuditor(content)
        return self.html_auditor.audit()

    def audit_file(self, filepath: Path, doc_type: str = "auto",
                   expected_modules: List[str] = None) -> AuditReport:
        """对文件进行自动类型检测并审计"""
        if not filepath.exists():
            return AuditReport(
                dna=P0_CONFIG["dna"],
                target=str(filepath),
                target_type="unknown",
                audited_at=datetime.now().isoformat(),
                summary={"🔴致命": 1, "🟡重要": 0, "🟢建议": 0},
                findings=[Finding("E001", "文件", Severity.FATAL, "文件不存在", str(filepath))],
                suggestions=[],
                score=0, color="🔴",
            )

        content = filepath.read_text(encoding="utf-8", errors="ignore")
        suffix = filepath.suffix.lower()

        if suffix == ".md" or suffix == ".markdown":
            report = self.audit_markdown(content, doc_type)
            report.target = str(filepath)
            return report
        elif suffix == ".py":
            report = self.audit_python(content, expected_modules)
            report.target = str(filepath)
            return report
        elif suffix == ".html" or suffix == ".htm":
            report = self.audit_html(content)
            report.target = str(filepath)
            return report
        else:
            # 通用文本审计
            report = self.audit_markdown(content, "general_md")
            report.target = str(filepath)
            report.target_type = f"text ({suffix})"
            return report


# ═══════════════════════════════════════════════════════════════════════════════
# 报告格式化输出
# ═══════════════════════════════════════════════════════════════════════════════

def format_report(report: AuditReport, verbose: bool = False) -> str:
    """格式化审计报告为可读文本"""
    lines = []
    lines.append("")
    lines.append("=" * 64)
    lines.append("🐉 龍魂·文档结构审计报告 v2.0")
    lines.append("=" * 64)
    lines.append(f"DNA:      {report.dna}")
    lines.append(f"目标:     {report.target}")
    lines.append(f"类型:     {report.target_type}")
    lines.append(f"时间:     {report.audited_at}")
    lines.append(f"评分:     {report.color} {report.score:.1f}/100")
    lines.append("-" * 64)

    # 摘要
    lines.append(f"摘要: 🔴{report.summary.get('🔴致命', 0)} | 🟡{report.summary.get('🟡重要', 0)} | 🟢{report.summary.get('🟢建议', 0)}")
    lines.append("-" * 64)

    # 按严重度分组
    for sev in [Severity.FATAL, Severity.IMPORTANT, Severity.SUGGESTION]:
        group = [f for f in report.findings if f.severity == sev]
        if not group:
            continue
        lines.append(f"\n{sev.icon} {sev.label}级问题 ({len(group)}):")
        for f in group:
            lines.append(f"  [{f.id}] [{f.category}] {f.title}")
            if verbose:
                lines.append(f"       详情: {f.detail}")
                if f.suggestion:
                    lines.append(f"       建议: {f.suggestion}")
                if f.line:
                    lines.append(f"       行号: {f.line}")

    # 补全建议
    if report.suggestions:
        lines.append(f"\n{'─' * 64}")
        lines.append("💡 自动补全建议:")
        for i, s in enumerate(report.suggestions, 1):
            lines.append(f"  {i}. [{s['type']}]")
            if verbose:
                lines.append(f"     {s['content'][:200]}")

    lines.append(f"\n{'=' * 64}")
    lines.append(f"确认码: {P0_CONFIG['confirm']}")
    lines.append(f"GPG:     {P0_CONFIG['gpg']}")
    lines.append(f"{'=' * 64}")

    return "\n".join(lines)


# ═══════════════════════════════════════════════════════════════════════════════
# 场景感知的内容补全推理
# ═══════════════════════════════════════════════════════════════════════════════

class ContentSuggester:
    """内容补全推理引擎 — 基于场景自动推理缺失区块"""

    SCENARIO_PATTERNS = {
        "技术教程": {
            "keywords": ["教程", "tutorial", "入门", "guide", "怎么", "如何"],
            "missing_blocks": [
                ("环境准备", "Python 3.8+ / pip install xxx / 配置文件"),
                ("快速开始", "5分钟最小可运行示例"),
                ("常见问题", "FAQ / 踩坑记录"),
            ],
        },
        "API文档": {
            "keywords": ["API", "接口", "endpoint", "请求", "响应", "参数"],
            "missing_blocks": [
                ("认证方式", "API Key / Token / OAuth"),
                ("请求示例", "curl / python requests 示例"),
                ("错误码表", "状态码 + 含义 + 解决方案"),
            ],
        },
        "项目README": {
            "keywords": ["README", "readme", "项目", "project"],
            "missing_blocks": [
                ("安装说明", "pip install / docker pull"),
                ("使用示例", "最小可运行代码"),
                ("贡献指南", "如何提 PR / issue"),
            ],
        },
        "架构设计": {
            "keywords": ["架构", "architecture", "设计", "design", "系统"],
            "missing_blocks": [
                ("架构图", "Mermaid / ASCII 架构图"),
                ("技术选型", "为什么选择这些技术栈"),
                ("部署架构", "服务器拓扑 / 容器编排"),
            ],
        },
    }

    def suggest(self, content: str) -> List[Dict[str, str]]:
        """基于内容场景推理缺失区块"""
        suggestions = []
        content_lower = content.lower()

        for scenario, config in self.SCENARIO_PATTERNS.items():
            match_count = sum(1 for kw in config["keywords"] if kw in content_lower)
            if match_count >= 2:
                for block_name, block_desc in config["missing_blocks"]:
                    if block_name not in content:
                        suggestions.append({
                            "scenario": scenario,
                            "missing_block": block_name,
                            "description": block_desc,
                            "template": self._get_template(block_name),
                        })

        return suggestions

    def _get_template(self, block_name: str) -> str:
        templates = {
            "环境准备": "## 环境准备\n\n- Python 3.8+\n- 依赖: `pip install -r requirements.txt`\n- 配置: 复制 `.env.example` 为 `.env`",
            "快速开始": "## 快速开始\n\n```bash\ngit clone xxx\ncd xxx\npython3 main.py\n```",
            "架构图": "## 架构图\n\n```mermaid\ngraph TB\n    Client --> API\n    API --> DB\n```",
            "常见问题": "## 常见问题\n\n### Q: 如何...\nA: ...\n\n### Q: 为什么...\nA: ...",
        }
        return templates.get(block_name, f"## {block_name}\n\n（待补充）")


# ═══════════════════════════════════════════════════════════════════════════════
# CLI 入口
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="🐉 龍魂·文档结构审计引擎 v2.0",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3 08_BIN/lh_doc_structure_audit.py audit --target article.md
  python3 08_BIN/lh_doc_structure_audit.py audit --target script.py --type python
  python3 08_BIN/lh_doc_structure_audit.py check-truncation --target script.py
  python3 08_BIN/lh_doc_structure_audit.py suggest --target article.md
  python3 08_BIN/lh_doc_structure_audit.py audit --target page.html --type html
        """
    )

    sub = parser.add_subparsers(dest="cmd")

    # audit 命令
    p_audit = sub.add_parser("audit", help="完整文档结构审计")
    p_audit.add_argument("--target", required=True, help="目标文件路径")
    p_audit.add_argument("--type", default="auto", choices=["auto", "tech_article", "project_doc", "general_md", "python", "html"])
    p_audit.add_argument("--expected-modules", nargs="*", help="预期应存在的类/函数名（Python文件）")
    p_audit.add_argument("--output", "-o", help="输出 JSON 到文件")
    p_audit.add_argument("--json", action="store_true", help="以 JSON 格式输出")
    p_audit.add_argument("--verbose", "-v", action="store_true", help="详细输出")

    # check-truncation 命令
    p_trunc = sub.add_parser("check-truncation", help="仅检查代码截断")
    p_trunc.add_argument("--target", required=True, help="Python/HTML 文件路径")
    p_trunc.add_argument("--json", action="store_true", help="以 JSON 格式输出")

    # suggest 命令
    p_suggest = sub.add_parser("suggest", help="场景感知的内容补全建议")
    p_suggest.add_argument("--target", required=True, help="Markdown 文件路径")

    args = parser.parse_args()

    if not args.cmd:
        parser.print_help()
        return

    hub = DocStructureAuditHub()
    target = Path(args.target)

    if args.cmd == "audit":
        report = hub.audit_file(
            target,
            doc_type=args.type,
            expected_modules=args.expected_modules,
        )

        if args.json:
            print(json.dumps(report.to_dict(), ensure_ascii=False, indent=2))
        else:
            print(format_report(report, verbose=args.verbose))

        if args.output:
            Path(args.output).write_text(
                json.dumps(report.to_dict(), ensure_ascii=False, indent=2),
                encoding="utf-8",
            )

    elif args.cmd == "check-truncation":
        content = target.read_text(encoding="utf-8", errors="ignore")
        suffix = target.suffix.lower()

        if suffix == ".py":
            auditor = PythonCodeAuditor(content)
            auditor.check_truncation()
        elif suffix in (".html", ".htm"):
            auditor = HTMLAuditor(content)
            auditor.audit()
        else:
            print("❌ check-truncation 仅支持 .py / .html 文件")
            sys.exit(1)

        # 构建简易报告
        findings = auditor.findings
        fatal = sum(1 for f in findings if f.severity == Severity.FATAL)
        important = sum(1 for f in findings if f.severity == Severity.IMPORTANT)
        suggestion = sum(1 for f in findings if f.severity == Severity.SUGGESTION)

        if args.json:
            result = {
                "target": str(target),
                "findings": [f.to_dict() for f in findings],
                "summary": {"fatal": fatal, "important": important, "suggestion": suggestion},
            }
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(f"\n截断检测: {target}")
            print(f"  🔴致命: {fatal} | 🟡重要: {important} | 🟢建议: {suggestion}")
            for f in findings:
                print(f"  {f.severity.icon} [{f.category}] {f.title}")
                if f.line:
                    print(f"     行号: {f.line}")
                if f.suggestion:
                    print(f"     建议: {f.suggestion}")

        if fatal > 0:
            sys.exit(1)

    elif args.cmd == "suggest":
        content = target.read_text(encoding="utf-8", errors="ignore")
        suggester = ContentSuggester()
        suggestions = suggester.suggest(content)

        if not suggestions:
            print("✅ 未发现明显缺失的区块")
        else:
            print(f"\n💡 场景推理补全建议 ({len(suggestions)} 条):\n")
            for i, s in enumerate(suggestions, 1):
                print(f"  {i}. [{s['scenario']}] 缺少: {s['missing_block']}")
                print(f"     描述: {s['description']}")
                print(f"     模板: {s['template'][:120]}...")
                print()


if __name__ == "__main__":
    main()
