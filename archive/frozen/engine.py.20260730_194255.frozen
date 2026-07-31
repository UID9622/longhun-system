# -*- coding: utf-8 -*-
"""#龍芯⚡️2026-06-29-CNSH-EDITOR-ENGINE-v0.1
核心纠错引擎：保护代码/链接，按规则流水线处理
"""
import re
import uuid
import hashlib
from dataclasses import dataclass, field
from typing import List, Tuple, Dict, Callable, Optional


@dataclass
class Rule:
    id: str
    category: str
    pattern: str
    replacement: str
    description: str = ""
    flags: int = 0
    condition: Optional[Callable[[str], bool]] = None


class CNSHEditor:
    """CNSH 中文编辑器纠错引擎 v0.1

    已实现核心规则：
      - 01 标点纠错（001-010）
      - 02 空格规则（051-065）
      - 10 翻译避坑（301-330 中与 01/02 重叠部分）
      - 安全规则：自动保护代码块、行内代码、URL、邮箱
    """

    URL_PATTERN = re.compile(
        r"https?://[^\s\]\)\"']+|www\.[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", re.IGNORECASE
    )
    EMAIL_PATTERN = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")
    CODE_BLOCK_PATTERN = re.compile(r"```[\s\S]*?```", re.MULTILINE)
    INLINE_CODE_PATTERN = re.compile(r"`[^`\n]+`")

    def __init__(self):
        self.rules = self._build_rules()

    @staticmethod
    def _is_chinese(text: str, threshold: float = 0.3) -> bool:
        """简单语言检测：中文字符占比超过阈值视为中文文本。"""
        chinese_chars = re.findall(r"[\u4e00-\u9fa5]", text)
        if not text:
            return True
        return len(chinese_chars) / len(text) > threshold

    def _build_rules(self) -> List[Rule]:
        CJK = r"[\u4e00-\u9fa5\u3040-\u30ff\u3400-\u4dbf]"
        is_cn = self._is_chinese
        return [
            # ===== 01 标点纠错 =====
            Rule("规则001", "01 标点纠错",
                 rf"({CJK}),", r"\1，",
                 "英文逗号 → 中文逗号"),
            Rule("规则002", "01 标点纠错",
                 rf"({CJK})\.", r"\1。",
                 "英文句号 → 中文句号"),
            Rule("规则003", "01 标点纠错",
                 rf"({CJK}):", r"\1：",
                 "英文冒号 → 中文冒号"),
            Rule("规则004", "01 标点纠错",
                 rf"({CJK});", r"\1；",
                 "英文分号 → 中文分号"),
            Rule("规则005", "01 标点纠错",
                 rf"({CJK})!", r"\1！",
                 "英文感叹号 → 中文感叹号"),
            Rule("规则006", "01 标点纠错",
                 rf"({CJK})\?", r"\1？",
                 "英文问号 → 中文问号"),
            Rule("规则007", "01 标点纠错",
                 rf"({CJK})\.\.\.(?=[\u4e00-\u9fa5\s]|$)", r"\1……",
                 "英文省略号 → 中文省略号"),
            Rule("规则008", "01 标点纠错",
                 rf"({CJK})--(?={CJK})", r"\1——",
                 "英文破折号 → 中文破折号"),
            Rule("规则009", "01 标点纠错",
                 rf"({CJK}),({CJK})", r"\1、\2",
                 "并列词组英文逗号 → 顿号（启发式）"),
            Rule("规则010", "01 标点纠错",
                 r'"([^"]{1,20}?(?:红楼梦|三国|水浒|西游|史记)[^"]{0,10})"',
                 r"《\1》",
                 "书名号误用引号（示例）"),

            # ===== 02 空格规则 =====
            Rule("规则051", "02 空格规则",
                 rf"({CJK})([a-zA-Z])", r"\1 \2",
                 "中文后接英文单词间加空格"),
            Rule("规则051b", "02 空格规则",
                 rf"([a-zA-Z])({CJK})", r"\1 \2",
                 "英文单词后接中文间加空格"),
            Rule("规则052", "02 空格规则",
                 rf"({CJK})(\d)", r"\1 \2",
                 "中文后接数字间加空格"),
            Rule("规则052b", "02 空格规则",
                 rf"(\d)({CJK})", r"\1 \2",
                 "数字后接中文间加空格"),
            Rule("规则053", "02 空格规则",
                 r"([a-zA-Z])\s*([，。：；！？])", r"\1\2",
                 "英文单词与中文标点间不加空格"),
            Rule("规则054", "02 空格规则",
                 r"(\d)([a-zA-Z]{1,5})(?![a-zA-Z])", r"\1 \2",
                 "数字与单位间加空格（简单版）"),
            Rule("规则055", "02 空格规则",
                 rf"({CJK})\s*（\s*", r"\1（",
                 "中文与左括号间不加空格"),
            Rule("规则056", "02 空格规则",
                 rf"\s*）\s*({CJK})", r"）\1",
                 "中文右括号与中文间不加空格"),
            Rule("规则057", "02 空格规则",
                 rf"(?<={CJK}) (?={CJK})", r"",
                 "全角字符间不加空格"),
            Rule("规则059", "02 空格规则",
                 rf"({CJK})([A-Z]{2,}(?:/[A-Z]{2,})+)", r"\1 \2",
                 "中文与英文缩写间加空格"),
            Rule("规则060", "02 空格规则",
                 rf"({CJK})(https?://[^\s]+)({CJK})", r"\1 \2 \3",
                 "链接前后加空格（中文环境）"),
            Rule("规则061", "02 空格规则",
                 rf"({CJK})(`[^`]+`)({CJK})", r"\1 \2 \3",
                 "行内代码前后加空格"),
            Rule("规则062", "02 空格规则",
                 rf"({CJK})(\$[^$\n]+\$)({CJK})", r"\1 \2 \3",
                 "数学公式前后加空格"),
            Rule("规则065", "02 空格规则",
                 r"[ \t]{2,}", " ",
                 "连续空格压缩"),

            # ===== 11 CNSH 特殊语法保留 =====
            Rule("规则331", "11 CNSH特殊语法",
                 r"\b(if|then|else|for|in|return|import|class|def)\b(?=\s*[\u4e00-\u9fa5])",
                 lambda m: m.group(0),
                 "CNSH中文关键词保留（标记不修改）"),

            # ===== 10 翻译避坑规则 A（301-330 可执行核心）=====
            Rule("规则302", "10 翻译避坑",
                 r"“([^”]{0,80}[a-zA-Z][^”]{0,80})”", r'"\1"',
                 "英文语境中文双引号 → 英文双引号",
                 condition=lambda t: not is_cn(t)),
            Rule("规则303", "10 翻译避坑",
                 r"(?<=[\s\u4e00-\u9fa5])\((?=.{0,40}[\u4e00-\u9fa5])", "（",
                 "中文语境半角左圆括号 → 全角",
                 flags=re.MULTILINE),
            Rule("规则303b", "10 翻译避坑",
                 r"(?<=[\u4e00-\u9fa5])\)(?=[\s\u4e00-\u9fa5]|$)", "）",
                 "中文语境半角右圆括号 → 全角",
                 flags=re.MULTILINE),
            Rule("规则306", "10 翻译避坑",
                 rf"({CJK}),({CJK})(?=、|，|；|$)", r"\1、\2",
                 "中文并列词组英文逗号 → 顿号（加强版）"),
            Rule("规则308", "10 翻译避坑",
                 r"([a-zA-Z]):([a-zA-Z])", r"\1: \2",
                 "英文冒号后加空格",
                 condition=lambda t: not is_cn(t)),
            Rule("规则310", "10 翻译避坑",
                 r"([！？]){3,}", r"\1\1",
                 "中文连续感叹/问号最多保留2个"),
            Rule("规则310b", "10 翻译避坑",
                 r"([!?]){2,}", r"\1",
                 "英文连续感叹/问号最多保留1个",
                 condition=lambda t: not is_cn(t)),
            Rule("规则313", "10 翻译避坑",
                 r"([a-zA-Z])([,.;:!?])([a-zA-Z])", r"\1\2 \3",
                 "英文标点后加空格",
                 condition=lambda t: not is_cn(t)),
            Rule("规则315", "10 翻译避坑",
                 r"^(?:[-*+]|\d+\.)(?=\S)", lambda m: m.group(0) + " ",
                 "列表符号后加空格",
                 flags=re.MULTILINE),
            Rule("规则318", "10 翻译避坑",
                 r"[　]+", " ",
                 "全角空格转为半角空格（非中文排版场景）"),

            # ===== 12 智能修复规则 D（351-370 可执行核心）=====
            Rule("规则352", "12 智能修复",
                 r"^(?!#{1,6})(?!\s*[-*+\d]\.?\s)(.*?[\u4e00-\u9fa5])(?=\n|$)(?![，。！？；：、…])",
                 r"\1。",
                 "中文句末无标点自动补句号（排除标题和列表标记行）",
                 flags=re.DOTALL | re.MULTILINE,
                 condition=is_cn),
            Rule("规则358", "12 智能修复",
                 r"^(?:[-*+]|\d+\.)(?=\S)", lambda m: m.group(0) + " ",
                 "自动修复列表符号后空格",
                 flags=re.MULTILINE),
            Rule("规则359", "12 智能修复",
                 r"^(#{1,6})(?=\S)", lambda m: m.group(0) + " ",
                 "自动修复标题井号后空格",
                 flags=re.MULTILINE),
            Rule("规则365", "12 智能修复",
                 r"\n{3,}", "\n\n",
                 "连续空行压缩为最多两个",
                 flags=re.MULTILINE),
        ]

    def _protect(self, text: str) -> Tuple[str, Dict[str, str]]:
        """保护代码、链接、邮箱，返回占位后的文本和映射表。"""
        placeholders: Dict[str, str] = {}

        def _ph(token: str) -> str:
            key = f"__PH_{uuid.uuid4().hex[:8]}__"
            placeholders[key] = token
            return key

        # 代码块
        text = self.CODE_BLOCK_PATTERN.sub(lambda m: _ph(m.group(0)), text)
        # 行内代码
        text = self.INLINE_CODE_PATTERN.sub(lambda m: _ph(m.group(0)), text)
        # URL
        text = self.URL_PATTERN.sub(lambda m: _ph(m.group(0)), text)
        # 邮箱
        text = self.EMAIL_PATTERN.sub(lambda m: _ph(m.group(0)), text)
        return text, placeholders

    def _restore(self, text: str, placeholders: Dict[str, str]) -> str:
        for key, value in placeholders.items():
            text = text.replace(key, value)
        return text

    def correct_text(self, text: str) -> Tuple[str, List[str], Dict]:
        """返回 (纠错后文本, 应用的规则ID列表, 审计信息)"""
        protected, placeholders = self._protect(text)

        result = protected
        applied: List[str] = []

        for rule in self.rules:
            if rule.condition and not rule.condition(result):
                continue
            new_text, count = re.subn(rule.pattern, rule.replacement, result, flags=rule.flags)
            if count and new_text != result:
                result = new_text
                applied.append(rule.id)

        result = self._restore(result, placeholders)

        # 简单三色审计：存在未闭合引号/括号则黄/红
        audit = "🟢"
        issues = []
        if result.count('"') % 2 or result.count("'") % 2 or result.count('“') != result.count('”'):
            audit = "🟡"
            issues.append("引号疑似未闭合")
        if result.count('（') != result.count('）'):
            audit = "🟡"
            issues.append("圆括号未配对")
        # 危险模式检查
        dangerous = re.search(r"<script|javascript:|data:text|../../../", result, re.IGNORECASE)
        if dangerous:
            audit = "🔴"
            issues.append("检测到潜在安全向量")

        audit_info = {
            "audit": audit,
            "issues": issues,
            "rules_total": len(self.rules),
            "rules_applied": len(applied),
        }
        return result, applied, audit_info

    def correct_file(self, path: str) -> Tuple[str, List[str], Dict]:
        text = open(path, "r", encoding="utf-8").read()
        return self.correct_text(text)
