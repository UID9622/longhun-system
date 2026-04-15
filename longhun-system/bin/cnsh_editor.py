#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 CNSH语法编辑器 v2.1 · 修复版
功能：伪代码检测 + 语法高亮 + 三色审计 + 一键修复
DNA: #龍芯⚡️2026-04-03-CNSH-EDITOR-v2.1
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F1E3B8A4C6D0F2E4A6B8C0D2E4F6A8B0C2
创建者: UID9622 诸葛鑫（龍芯北辰）
理论指导: 曾仕强老师（永恒显示）

继承乔布斯夙愿：让每个人可以用到最懂他的设备，在宇宙中留下痕迹
保存为: ~/longhun-system/bin/cnsh_editor.py
"""

import tkinter as tk
from tkinter import ttk, font, scrolledtext, messagebox
import re
from dataclasses import dataclass
from typing import List, Tuple, Optional
from datetime import datetime
import hashlib
import subprocess
import os
import sys

# ============================================================
# CNSH 语法引擎
# ============================================================

@dataclass
class Issue:
    """伪代码问题"""
    line: int
    fake_code: str
    correct: str
    category: str
    start: int
    end: int

@dataclass
class AuditResult:
    """审计结果"""
    level: str
    culture_count: int
    keyword_count: int
    issues: List[Issue]
    comment: str
    dna: str


class CNSHSyntaxEngine:
    """CNSH 语法检测引擎"""

    CONTROL_KEYWORDS = {"如果", "否则", "否则如果", "循环", "当", "遍历", "跳出", "继续", "返回"}
    DECLARE_KEYWORDS = {
        "函数", "类", "结构", "枚举", "协议",
        "变量", "常量", "整数", "浮点", "字符串", "布尔",
        "返回类型", "属于"
    }
    ACTION_KEYWORDS = {"打印", "输入", "导入", "抛出", "捕获", "新建", "删除", "空"}

    @classmethod
    def all_keywords(cls):
        return cls.CONTROL_KEYWORDS | cls.DECLARE_KEYWORDS | cls.ACTION_KEYWORDS

    VIOLATION_TABLE = [
        ("FiveElements", "五行", "文化主权"), ("Five Elements", "五行", "文化主权"),
        ("EightTrigrams", "八卦", "文化主权"), ("Eight Trigrams", "八卦", "文化主权"),
        ("HeavenlyStems", "天干", "文化主权"), ("EarthlyBranches", "地支", "文化主权"),
        ("YinYang", "阴阳", "文化主权"), ("Yin Yang", "阴阳", "文化主权"),
        ("SolarTerms", "节气", "文化主权"), ("Solar Terms", "节气", "文化主权"),
        ("LunarCalendar", "农历", "文化主权"), ("Lunar Calendar", "农历", "文化主权"),
        ("FengShui", "风水", "文化主权"), ("Feng Shui", "风水", "文化主权"),
        ("Zodiac", "生肖", "文化主权"), ("TaiChi", "太极", "文化主权"),
        ("Tai Chi", "太极", "文化主权"), ("Qigong", "气功", "文化主权"),
        ("Qi Gong", "气功", "文化主权"), ("DaoDeJing", "道德经", "文化主权"),
        ("Tao Te Ching", "道德经", "文化主权"), ("I Ching", "易经", "文化主权"),
        ("Wuxing", "五行", "文化主权"), ("Yijing", "易经", "文化主权"),
        ("if", "如果", "关键词"), ("else", "否则", "关键词"),
        ("for", "循环", "关键词"), ("while", "当", "关键词"),
        ("function", "函数", "关键词"), ("class", "类", "关键词"),
        ("return", "返回", "关键词"), ("print", "打印", "关键词"),
        ("var", "变量", "关键词"), ("let", "常量", "关键词"),
        ("int", "整数", "关键词"), ("float", "浮点", "关键词"),
        ("string", "字符串", "关键词"), ("bool", "布尔", "关键词"),
        ("import", "导入", "关键词"), ("break", "跳出", "关键词"),
        ("continue", "继续", "关键词"), ("struct", "结构", "关键词"),
        ("enum", "枚举", "关键词"), ("switch", "选择", "关键词"),
        ("case", "情况", "关键词"), ("true", "真", "关键词"),
        ("false", "假", "关键词"), ("null", "空", "关键词"),
        ("nil", "空", "关键词"), ("new", "新建", "关键词"),
        ("delete", "删除", "关键词"), ("try", "尝试", "关键词"),
        ("catch", "捕获", "关键词"), ("throw", "抛出", "关键词"),
    ]

    @classmethod
    def detect_issues(cls, code: str) -> List[Issue]:
        issues = []
        lines = code.split("\n")
        for line_num, line in enumerate(lines, 1):
            stripped = line.strip()
            if stripped.startswith("#") or stripped.startswith("//"):
                continue
            clean_line = cls._remove_strings(line)
            for fake, correct, category in cls.VIOLATION_TABLE:
                pattern = re.compile(re.escape(fake), re.IGNORECASE)
                for match in pattern.finditer(clean_line):
                    issues.append(Issue(
                        line=line_num,
                        fake_code=fake,
                        correct=correct,
                        category=category,
                        start=match.start(),
                        end=match.end()
                    ))
        return issues

    @classmethod
    def _remove_strings(cls, line: str) -> str:
        result = []
        in_string = False
        quote_char = None
        i = 0
        while i < len(line):
            ch = line[i]
            if not in_string:
                if ch in ('"', "'"):
                    in_string = True
                    quote_char = ch
                    result.append(ch)
                elif ch == '「':
                    in_string = True
                    quote_char = '」'
                    result.append(ch)
                elif ch == '『':
                    in_string = True
                    quote_char = '』'
                    result.append(ch)
                else:
                    result.append(ch)
            else:
                if ch == quote_char and (i == 0 or line[i-1] != '\\'):
                    in_string = False
                    result.append(ch)
                else:
                    result.append(' ')
            i += 1
        return ''.join(result)

    @classmethod
    def audit(cls, code: str) -> AuditResult:
        issues = cls.detect_issues(code)
        culture_issues = [i for i in issues if i.category == "文化主权"]
        keyword_issues = [i for i in issues if i.category == "关键词"]

        if culture_issues:
            level = "🔴"
            comment = f"文化主权被侵犯！发现 {len(culture_issues)} 处文化关键词被翻译"
        elif keyword_issues:
            level = "🟡"
            comment = f"发现 {len(keyword_issues)} 处英文关键词，建议替换为中文"
        else:
            level = "🟢"
            comment = "代码符合 CNSH 规范 ✅"

        dna = cls._generate_dna(code, level)
        return AuditResult(
            level=level,
            culture_count=len(culture_issues),
            keyword_count=len(keyword_issues),
            issues=issues,
            comment=comment,
            dna=dna
        )

    @classmethod
    def _generate_dna(cls, code: str, level: str) -> str:
        data = f"{code[:500]}|{level}|{datetime.now().isoformat()}"
        hash_part = hashlib.sha256(data.encode()).hexdigest()[:24]
        return f"#CNSH审计⚡️{datetime.now().strftime('%Y%m%d')}-{hash_part}"

    @classmethod
    def fix_issue(cls, code: str, issue: Issue) -> str:
        pattern = re.compile(re.escape(issue.fake_code), re.IGNORECASE)
        return pattern.sub(issue.correct, code, count=1)

    @classmethod
    def fix_all(cls, code: str, issues: List[Issue]) -> str:
        fixed = code
        for issue in sorted(issues, key=lambda x: (x.line, x.start), reverse=True):
            pattern = re.compile(re.escape(issue.fake_code), re.IGNORECASE)
            fixed = pattern.sub(issue.correct, fixed, count=1)
        return fixed


# ============================================================
# CNSH 编辑器主窗口
# ============================================================

class CNSHEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("🐉 CNSH 语法编辑器 v2.1 · 龍魂系统")
        self.root.geometry("1000x700")
        self.root.minsize(800, 500)

        self.default_code = '''# CNSH示例程序
# DNA追溯码：#龍芯⚡️2026-CNSH-示例

函数 主函数() 返回类型 整数 {
    打印「🇨🇳 你好，CNSH语言！」

    整数 成本 = 80
    整数 售价 = 120
    整数 利润 = 售价 - 成本

    如果【利润 > 0】{
        打印「✅ 有利润」
    } 否则 {
        打印「❌ 亏损」
    }

    循环【3】{
        打印「🔄 循环执行中...」
    }

    返回 0
}'''

        self.current_code = self.default_code
        self.audit_result = None
        self.issues = []

        self._setup_ui()
        self._update_audit()

    def _setup_ui(self):
        main_frame = ttk.Frame(self.root, padding="5")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # 工具栏
        toolbar = ttk.Frame(main_frame)
        toolbar.pack(fill=tk.X, pady=(0, 5))

        ttk.Button(toolbar, text="🔍 三色审计", command=self._update_audit).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="🔧 一键修复", command=self._fix_all).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="💾 保存", command=self._save_file).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="📂 打开", command=self._open_file).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="▶ 运行", command=self._run_code).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="🔄 重置", command=self._reset_code).pack(side=tk.LEFT, padx=2)

        # 状态栏
        self.status_frame = tk.Frame(main_frame, relief=tk.SUNKEN, bd=1)
        self.status_frame.pack(fill=tk.X, pady=(0, 5))
        self.status_label = tk.Label(self.status_frame, text="⚪ 点击审计开始检测", font=("", 10))
        self.status_label.pack(side=tk.LEFT, padx=5)
        self.dna_label = tk.Label(self.status_frame, text="", font=("", 8), fg="gray")
        self.dna_label.pack(side=tk.RIGHT, padx=5)

        # 编辑区
        text_frame = ttk.Frame(main_frame)
        text_frame.pack(fill=tk.BOTH, expand=True)

        self.line_numbers = tk.Text(text_frame, width=5, padx=3, takefocus=0, border=0,
                                    bg="#f0f0f0", fg="#888", font=("Consolas", 11))
        self.line_numbers.pack(side=tk.LEFT, fill=tk.Y)

        self.code_text = scrolledtext.ScrolledText(text_frame, wrap=tk.NONE,
                                                     font=("Consolas", 11),
                                                     undo=True,
                                                     bg="#1e1e2e",
                                                     fg="#cdd6f4",
                                                     insertbackground="#ffffff")
        self.code_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.code_text.bind("<KeyRelease>", self._on_code_change)
        self.code_text.bind("<MouseWheel>", self._sync_scroll)
        self.code_text.bind("<Button-4>", self._sync_scroll)
        self.code_text.bind("<Button-5>", self._sync_scroll)

        self.code_text.insert("1.0", self.default_code)
        self._update_line_numbers()

        # 问题列表
        self.problem_frame = ttk.LabelFrame(main_frame, text="📋 问题列表（双击修复）", padding="5")
        self.problem_frame.pack(fill=tk.X, pady=(5, 0))

        self.problem_listbox = tk.Listbox(self.problem_frame, height=6, font=("", 10))
        self.problem_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.problem_listbox.bind("<Double-Button-1>", self._fix_selected)

        scrollbar = ttk.Scrollbar(self.problem_frame, orient=tk.VERTICAL, command=self.problem_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.problem_listbox.config(yscrollcommand=scrollbar.set)

        # 底部状态
        status_bar = ttk.Frame(main_frame)
        status_bar.pack(fill=tk.X, pady=(5, 0))

        self.line_count_label = ttk.Label(status_bar, text="行数: 0", font=("", 9))
        self.line_count_label.pack(side=tk.LEFT, padx=5)
        self.char_count_label = ttk.Label(status_bar, text="字符: 0", font=("", 9))
        self.char_count_label.pack(side=tk.LEFT, padx=5)
        ttk.Label(status_bar, text="CNSH v2.1 | UID9622 | 龍魂系统", font=("", 9)).pack(side=tk.RIGHT, padx=5)

    def _update_line_numbers(self):
        self.line_numbers.delete("1.0", tk.END)
        line_count = int(self.code_text.index("end-1c").split(".")[0])
        for i in range(1, line_count + 1):
            self.line_numbers.insert("end", f"{i}\n")

    def _sync_scroll(self, event=None):
        self.line_numbers.yview_moveto(self.code_text.yview()[0])

    def _on_code_change(self, event=None):
        self._update_line_numbers()
        self._update_audit()
        self._update_counts()

    def _update_counts(self):
        code = self.code_text.get("1.0", tk.END)
        lines = len(code.split("\n"))
        chars = len(code)
        self.line_count_label.config(text=f"行数: {lines}")
        self.char_count_label.config(text=f"字符: {chars}")

    def _update_audit(self):
        code = self.code_text.get("1.0", tk.END)
        result = CNSHSyntaxEngine.audit(code)
        self.audit_result = result
        self.issues = result.issues

        colors = {"🔴": "#ffebee", "🟡": "#fff8e1", "🟢": "#e8f5e9"}
        fg_colors = {"🔴": "#c62828", "🟡": "#f57c00", "🟢": "#2e7d32"}

        bg = colors.get(result.level, "#ffffff")
        fg = fg_colors.get(result.level, "#000000")

        self.status_frame.config(bg=bg)
        self.status_label.config(text=f"{result.level} {result.comment}", bg=bg, fg=fg)
        self.dna_label.config(text=f"DNA: {result.dna[:40]}...")

        self.problem_listbox.delete(0, tk.END)
        for i, issue in enumerate(result.issues):
            prefix = "🔴" if issue.category == "文化主权" else "🟡"
            self.problem_listbox.insert(tk.END, f"{prefix} 第{issue.line}行: {issue.fake_code} → {issue.correct}")

    def _fix_selected(self, event=None):
        sel = self.problem_listbox.curselection()
        if not sel or sel[0] >= len(self.issues):
            return
        issue = self.issues[sel[0]]
        code = self.code_text.get("1.0", tk.END)
        fixed = CNSHSyntaxEngine.fix_issue(code, issue)
        self.code_text.delete("1.0", tk.END)
        self.code_text.insert("1.0", fixed)
        self._update_audit()

    def _fix_all(self):
        if not self.issues:
            messagebox.showinfo("提示", "没有需要修复的问题")
            return
        code = self.code_text.get("1.0", tk.END)
        fixed = CNSHSyntaxEngine.fix_all(code, self.issues)
        self.code_text.delete("1.0", tk.END)
        self.code_text.insert("1.0", fixed)
        self._update_audit()
        messagebox.showinfo("修复完成", f"已修复 {len(self.issues)} 个问题")

    def _save_file(self):
        code = self.code_text.get("1.0", tk.END)
        path = tk.filedialog.asksaveasfilename(defaultextension=".cnsh", filetypes=[("CNSH文件", "*.cnsh"), ("所有文件", "*.*")])
        if path:
            with open(path, "w", encoding="utf-8") as f:
                f.write(code)
            messagebox.showinfo("保存成功", f"已保存到: {path}")

    def _open_file(self):
        path = tk.filedialog.askopenfilename(filetypes=[("CNSH文件", "*.cnsh"), ("文本文件", "*.txt"), ("所有文件", "*.*")])
        if path:
            with open(path, "r", encoding="utf-8") as f:
                code = f.read()
            self.code_text.delete("1.0", tk.END)
            self.code_text.insert("1.0", code)
            self._update_audit()

    def _run_code(self):
        code = self.code_text.get("1.0", tk.END)
        result = CNSHSyntaxEngine.audit(code)
        if result.level == "🔴":
            if not messagebox.askyesno("文化主权警告", f"代码存在文化主权问题，是否仍要运行？\n\n{result.comment}"):
                return
        temp = "/tmp/cnsh_temp.cnsh"
        with open(temp, "w", encoding="utf-8") as f:
            f.write(code)
        messagebox.showinfo("运行", f"CNSH代码已保存到临时文件\n{temp}\n\n（CNSH解释器待集成）")

    def _reset_code(self):
        self.code_text.delete("1.0", tk.END)
        self.code_text.insert("1.0", self.default_code)
        self._update_audit()


def main():
    root = tk.Tk()
    app = CNSHEditor(root)
    root.mainloop()


if __name__ == "__main__":
    main()
