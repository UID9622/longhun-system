#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·丙酉·癸亥·巳时·䷫姤-CNSH-IDE-v1.0-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
"""
🐉 CNSH 集成开发环境 (IDE) v1.0

把 CNSH 编辑器、编译器、执行器统一到一个桌面应用。

功能：
  - 项目/文件浏览器
  - 带行号的代码编辑器
  - CNSH 语法高亮
  - 一键纠错（370条规则）
  - 一键编译为 Python
  - 一键运行 CNSH 脚本
  - 输出/日志/编译结果面板

用法：
  python3 08_BIN/cnsh_ide.py
  python3 08_BIN/cnsh_ide.py /path/to/project
"""

import os
import sys
import re
import json
import subprocess
import threading
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict, Tuple

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext

# 让导入能找到同目录模块
sys.path.insert(0, str(Path(__file__).resolve().parent))

try:
    from cnsh_editor import CNSHEditor, SecurityFilter
    from cnsh_compiler import CNSHCompiler
    from cnsh_ui import CNSHInterpreterV2
    HAS_ENGINES = True
except Exception as e:
    print(f"⚠️ 引擎导入失败: {e}", file=sys.stderr)
    HAS_ENGINES = False


# ═══════════════════════════════════════════════════════
# 配置
# ═══════════════════════════════════════════════════════
APP_NAME = "🐉 CNSH IDE"
APP_VERSION = "1.0.0"
DEFAULT_WORKSPACE = Path.home() / "longhun-system" / "cnsh_projects"
CONFIG_DIR = Path.home() / ".longhun" / "cnsh_ide"
CONFIG_FILE = CONFIG_DIR / "config.json"
RECENT_FILES_FILE = CONFIG_DIR / "recent.json"

CNSH_KEYWORDS = [
    "功能", "返回", "如果", "否则", "循环", "当", "跳出", "继续",
    "导入", "从", "类型", "类", "空", "真", "假", "设", "打印",
    "理解", "记录", "执行", "任务", "整数", "小数", "文本", "布尔",
    "列表", "字典", "集合", "元组", "和", "或", "非", "在", "是",
]

CNSH_BUILTINS = [
    "DNA", "确认码",
]

DEMO_PROJECT = '''@任务 欢迎

# 设变量
设 名字 = "龍魂"
设 版本 = 1.0

打印 名字
打印 版本

# 条件
如果 版本 >= 1.0
    打印 "正式版"
结束

# AI 理解（模拟）
理解 "把 CNSH 编译成 Python"
记录 AI结果

打印 AI结果

@任务 结束
'''


# ═══════════════════════════════════════════════════════
# 配置管理
# ═══════════════════════════════════════════════════════
def load_config() -> Dict:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    if CONFIG_FILE.exists():
        try:
            return json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {
        "workspace": str(DEFAULT_WORKSPACE),
        "font_size": 12,
        "theme": "dark",
        "recent_files": [],
    }


def save_config(config: Dict):
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    CONFIG_FILE.write_text(json.dumps(config, ensure_ascii=False, indent=2), encoding="utf-8")


def load_recent_files() -> List[str]:
    if RECENT_FILES_FILE.exists():
        try:
            return json.loads(RECENT_FILES_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return []


def save_recent_files(files: List[str]):
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    RECENT_FILES_FILE.write_text(json.dumps(files[-20:], ensure_ascii=False, indent=2), encoding="utf-8")


# ═══════════════════════════════════════════════════════
# 文本编辑器（带行号 + 语法高亮）
# ═══════════════════════════════════════════════════════
class LineNumberCanvas(tk.Canvas):
    def __init__(self, parent, text_widget, **kwargs):
        super().__init__(parent, width=40, bg="#252526", highlightthickness=0, **kwargs)
        self.text_widget = text_widget
        self.text_widget.bind("<KeyRelease>", self._on_change)
        self.text_widget.bind("<MouseWheel>", self._on_change)
        self.text_widget.bind("<Configure>", self._on_change)
        self.text_widget.bind("<ButtonRelease-1>", self._on_change)

    def _on_change(self, event=None):
        self.after(10, self.redraw)

    def redraw(self):
        self.delete("all")
        i = self.text_widget.index("@0,0")
        line_num = int(i.split(".")[0])
        dline = self.text_widget.dlineinfo(i)
        while dline:
            x = 35
            y = dline[1]
            self.create_text(x, y, anchor="ne", text=str(line_num),
                             font=("Courier New", 11), fill="#858585")
            line_num += 1
            i = self.text_widget.index(f"{i}+1line")
            dline = self.text_widget.dlineinfo(i)


class CNSHTextEditor(tk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        self.text = tk.Text(self, wrap=tk.NONE, undo=True, maxundo=100,
                            font=("Courier New", 12),
                            bg="#1e1e1e", fg="#d4d4d4",
                            insertbackground="#ffffff",
                            selectbackground="#264f78",
                            padx=5, pady=5,
                            borderwidth=0, highlightthickness=0)
        self.text.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.line_numbers = LineNumberCanvas(self, self.text)
        self.line_numbers.pack(side=tk.LEFT, fill=tk.Y)

        # 滚动条
        self.scroll_y = tk.Scrollbar(self, command=self.text.yview)
        self.scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.text.config(yscrollcommand=self._on_scroll)

        self.scroll_x = tk.Scrollbar(self, orient=tk.HORIZONTAL, command=self.text.xview)
        self.scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.text.config(xscrollcommand=self.scroll_x.set)

        # 标签颜色
        self.text.tag_config("keyword", foreground="#569cd6", font=("Courier New", 12, "bold"))
        self.text.tag_config("builtin", foreground="#4ec9b0")
        self.text.tag_config("string", foreground="#ce9178")
        self.text.tag_config("number", foreground="#b5cea8")
        self.text.tag_config("comment", foreground="#6a9955")
        self.text.tag_config("dna", foreground="#dcdcaa")
        self.text.tag_config("error", background="#5a1d1d")
        self.text.tag_config("warning", background="#5a4a1d")

        # 绑定高亮
        self.text.bind("<KeyRelease>", self._on_key_release)
        self.text.bind("<Tab>", self._on_tab)

    def _on_scroll(self, *args):
        self.scroll_y.set(*args)
        self.line_numbers.redraw()

    def _on_key_release(self, event=None):
        if event and event.keysym in ("Shift_L", "Shift_R", "Control_L", "Control_R",
                                       "Alt_L", "Alt_R", "Caps_Lock"):
            return
        self.highlight()

    def _on_tab(self, event):
        self.text.insert(tk.INSERT, "    ")
        return "break"

    def highlight(self):
        """CNSH 语法高亮"""
        text = self.text.get("1.0", tk.END)

        # 清除旧标签
        for tag in ("keyword", "builtin", "string", "number", "comment", "dna"):
            self.text.tag_remove(tag, "1.0", tk.END)

        lines = text.split("\n")
        for line_num, line in enumerate(lines, start=1):
            # 注释
            if line.strip().startswith("#"):
                start_idx = f"{line_num}.0"
                end_idx = f"{line_num}.end"
                self.text.tag_add("comment", start_idx, end_idx)
                continue

            # 字符串
            for m in re.finditer(r'"[^"]*"', line):
                self.text.tag_add("string", f"{line_num}.{m.start()}", f"{line_num}.{m.end()}")

            # 数字
            for m in re.finditer(r'\b\d+(?:\.\d+)?\b', line):
                self.text.tag_add("number", f"{line_num}.{m.start()}", f"{line_num}.{m.end()}")

            # DNA / 确认码
            for m in re.finditer(r'#龍芯⚡️\S+|#CONFIRM🌌\S+', line):
                self.text.tag_add("dna", f"{line_num}.{m.start()}", f"{line_num}.{m.end()}")

            # 关键字和内置函数
            for word in CNSH_KEYWORDS + CNSH_BUILTINS:
                for m in re.finditer(r'\b' + re.escape(word) + r'\b', line):
                    tag = "builtin" if word in CNSH_BUILTINS else "keyword"
                    self.text.tag_add(tag, f"{line_num}.{m.start()}", f"{line_num}.{m.end()}")

    def get_text(self) -> str:
        return self.text.get("1.0", tk.END)

    def set_text(self, text: str):
        self.text.delete("1.0", tk.END)
        self.text.insert("1.0", text)
        self.highlight()
        self.line_numbers.redraw()

    def insert_text(self, text: str):
        self.text.insert(tk.INSERT, text)

    def is_modified(self) -> bool:
        return self.text.edit_modified()

    def reset_modified(self):
        self.text.edit_modified(False)


# ═══════════════════════════════════════════════════════
# 文件浏览器
# ═══════════════════════════════════════════════════════
class FileBrowser(tk.Frame):
    def __init__(self, parent, on_select, **kwargs):
        super().__init__(parent, **kwargs)
        self.on_select = on_select
        self.root_path: Optional[Path] = None

        self.tree = ttk.Treeview(self, show="tree", selectmode="browse")
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scroll = tk.Scrollbar(self, command=self.tree.yview)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.config(yscrollcommand=scroll.set)

        self.tree.bind("<<TreeviewSelect>>", self._on_select)
        self.tree.bind("<Double-1>", self._on_double_click)

    def load(self, path: Path):
        self.root_path = path
        for item in self.tree.get_children():
            self.tree.delete(item)
        self._add_node("", path)

    def _add_node(self, parent: str, path: Path):
        name = path.name or str(path)
        node = self.tree.insert(parent, "end", text=name, open=True,
                                values=(str(path), path.is_file()))
        if path.is_dir():
            try:
                for child in sorted(path.iterdir(), key=lambda x: (x.is_file(), x.name)):
                    if child.name.startswith("."):
                        continue
                    if child.is_dir() and child.name in ("__pycache__", "venv", ".venv"):
                        continue
                    self._add_node(node, child)
            except PermissionError:
                pass

    def _on_select(self, event=None):
        selection = self.tree.selection()
        if not selection:
            return
        item = selection[0]
        values = self.tree.item(item, "values")
        if values and values[1] == "True":
            self.on_select(values[0])

    def _on_double_click(self, event=None):
        self._on_select(event)


# ═══════════════════════════════════════════════════════
# 主应用
# ═══════════════════════════════════════════════════════
class CNSHIDE:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title(APP_NAME)
        self.root.geometry("1200x800")
        self.root.minsize(900, 600)

        self.config = load_config()
        self.current_file: Optional[Path] = None
        self.current_project: Path = Path(self.config.get("workspace", str(DEFAULT_WORKSPACE)))
        self.recent_files = load_recent_files()

        self.correction_engine = CNSHEditor() if HAS_ENGINES else None
        self.compiler = CNSHCompiler() if HAS_ENGINES else None

        self._build_menu()
        self._build_toolbar()
        self._build_layout()
        self._build_statusbar()

        self._ensure_demo_project()
        self.file_browser.load(self.current_project)

    def _build_menu(self):
        menubar = tk.Menu(self.root)

        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="新建文件", command=self.new_file, accelerator="Ctrl+N")
        file_menu.add_command(label="打开文件", command=self.open_file, accelerator="Ctrl+O")
        file_menu.add_command(label="保存", command=self.save_file, accelerator="Ctrl+S")
        file_menu.add_command(label="另存为", command=self.save_as)
        file_menu.add_separator()
        file_menu.add_command(label="打开项目", command=self.open_project)
        file_menu.add_command(label="最近文件", command=self.show_recent)
        file_menu.add_separator()
        file_menu.add_command(label="退出", command=self.root.quit)
        menubar.add_cascade(label="文件", menu=file_menu)

        edit_menu = tk.Menu(menubar, tearoff=0)
        edit_menu.add_command(label="撤销", command=self.editor.text.edit_undo, accelerator="Ctrl+Z")
        edit_menu.add_command(label="重做", command=self.editor.text.edit_redo, accelerator="Ctrl+Y")
        edit_menu.add_separator()
        edit_menu.add_command(label="查找/替换", command=self.find_replace)
        menubar.add_cascade(label="编辑", menu=edit_menu)

        run_menu = tk.Menu(menubar, tearoff=0)
        run_menu.add_command(label="纠错", command=self.correct_code, accelerator="F5")
        run_menu.add_command(label="编译", command=self.compile_code, accelerator="F6")
        run_menu.add_command(label="运行", command=self.run_code, accelerator="F7")
        menubar.add_cascade(label="运行", menu=run_menu)

        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="关于", command=self.show_about)
        help_menu.add_command(label="CNSH 语法", command=self.show_syntax_help)
        menubar.add_cascade(label="帮助", menu=help_menu)

        self.root.config(menu=menubar)

        # 快捷键
        self.root.bind("<Control-n>", lambda e: self.new_file())
        self.root.bind("<Control-o>", lambda e: self.open_file())
        self.root.bind("<Control-s>", lambda e: self.save_file())
        self.root.bind("<F5>", lambda e: self.correct_code())
        self.root.bind("<F6>", lambda e: self.compile_code())
        self.root.bind("<F7>", lambda e: self.run_code())

    def _build_toolbar(self):
        toolbar = tk.Frame(self.root, bg="#333333", height=40)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        buttons = [
            ("🆕 新建", self.new_file),
            ("📂 打开", self.open_file),
            ("💾 保存", self.save_file),
            ("✨ 纠错", self.correct_code),
            ("🔨 编译", self.compile_code),
            ("▶ 运行", self.run_code),
        ]

        for text, cmd in buttons:
            btn = tk.Button(toolbar, text=text, command=cmd,
                            bg="#444444", fg="white", activebackground="#555555",
                            relief=tk.FLAT, padx=10, pady=5)
            btn.pack(side=tk.LEFT, padx=2, pady=2)

    def _build_layout(self):
        paned = tk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        paned.pack(fill=tk.BOTH, expand=True)

        # 左侧面板：文件浏览器
        left_frame = tk.Frame(paned, width=250, bg="#252526")
        paned.add(left_frame, minsize=150)

        tk.Label(left_frame, text="📁 项目", bg="#252526", fg="white",
                 font=("Arial", 10, "bold")).pack(fill=tk.X, padx=5, pady=5)
        self.file_browser = FileBrowser(left_frame, self._on_file_select, bg="#252526")
        self.file_browser.pack(fill=tk.BOTH, expand=True)

        # 右侧面板：编辑器 + 输出
        right_paned = tk.PanedWindow(paned, orient=tk.VERTICAL)
        paned.add(right_paned, minsize=400)

        # 编辑器区域
        editor_frame = tk.Frame(right_paned, bg="#1e1e1e")
        right_paned.add(editor_frame, minsize=300)

        self.file_label = tk.Label(editor_frame, text="未命名.cnsh",
                                    bg="#1e1e1e", fg="#cccccc", anchor="w", padx=5)
        self.file_label.pack(fill=tk.X)

        self.editor = CNSHTextEditor(editor_frame)
        self.editor.pack(fill=tk.BOTH, expand=True)

        # 输出区域（Notebook）
        self.notebook = ttk.Notebook(right_paned)
        right_paned.add(self.notebook, minsize=150)

        self.output_text = self._create_output_tab("输出")
        self.compile_text = self._create_output_tab("编译结果")
        self.log_text = self._create_output_tab("日志")

    def _create_output_tab(self, title: str) -> scrolledtext.ScrolledText:
        frame = tk.Frame(self.notebook)
        self.notebook.add(frame, text=title)
        text = scrolledtext.ScrolledText(frame, wrap=tk.WORD,
                                          font=("Courier New", 10),
                                          bg="#1e1e1e", fg="#d4d4d4",
                                          insertbackground="white")
        text.pack(fill=tk.BOTH, expand=True)
        return text

    def _build_statusbar(self):
        self.status = tk.Label(self.root, text="就绪", bd=1, relief=tk.SUNKEN, anchor="w")
        self.status.pack(side=tk.BOTTOM, fill=tk.X)

    def _ensure_demo_project(self):
        demo_dir = self.current_project / "demo"
        demo_file = demo_dir / "welcome.cnsh"
        if not demo_file.exists():
            demo_dir.mkdir(parents=True, exist_ok=True)
            demo_file.write_text(DEMO_PROJECT, encoding="utf-8")

    def _on_file_select(self, path: str):
        p = Path(path)
        if p.suffix.lower() == ".cnsh" or p.is_file():
            self.load_file(p)

    def _add_recent(self, path: str):
        if path in self.recent_files:
            self.recent_files.remove(path)
        self.recent_files.append(path)
        save_recent_files(self.recent_files)

    def load_file(self, path: Path):
        try:
            text = path.read_text(encoding="utf-8")
            self.editor.set_text(text)
            self.current_file = path
            self.file_label.config(text=f"📄 {path.name}")
            self.status.config(text=f"已加载: {path}")
            self.editor.reset_modified()
            self._add_recent(str(path))
        except Exception as e:
            messagebox.showerror("错误", f"无法读取文件: {e}")

    def new_file(self):
        if self.editor.is_modified():
            if not messagebox.askyesno("未保存", "当前文件未保存，确认新建？"):
                return
        self.editor.set_text("")
        self.current_file = None
        self.file_label.config(text="未命名.cnsh")
        self.status.config(text="新建文件")
        self.editor.reset_modified()

    def open_file(self):
        path = filedialog.askopenfilename(
            initialdir=str(self.current_project),
            filetypes=[("CNSH 文件", "*.cnsh"), ("所有文件", "*.*")]
        )
        if path:
            self.load_file(Path(path))

    def open_project(self):
        path = filedialog.askdirectory(initialdir=str(self.current_project))
        if path:
            self.current_project = Path(path)
            self.config["workspace"] = str(self.current_project)
            save_config(self.config)
            self.file_browser.load(self.current_project)
            self.status.config(text=f"项目: {self.current_project}")

    def save_file(self):
        if not self.current_file:
            return self.save_as()
        try:
            self.current_file.write_text(self.editor.get_text(), encoding="utf-8")
            self.editor.reset_modified()
            self.status.config(text=f"已保存: {self.current_file}")
            return True
        except Exception as e:
            messagebox.showerror("错误", f"保存失败: {e}")
            return False

    def save_as(self):
        path = filedialog.asksaveasfilename(
            initialdir=str(self.current_project),
            defaultextension=".cnsh",
            filetypes=[("CNSH 文件", "*.cnsh"), ("所有文件", "*.*")]
        )
        if path:
            self.current_file = Path(path)
            self.file_label.config(text=f"📄 {self.current_file.name}")
            return self.save_file()
        return False

    def show_recent(self):
        if not self.recent_files:
            messagebox.showinfo("最近文件", "没有最近文件")
            return
        top = tk.Toplevel(self.root)
        top.title("最近文件")
        top.geometry("500x300")
        listbox = tk.Listbox(top)
        listbox.pack(fill=tk.BOTH, expand=True)
        for f in reversed(self.recent_files):
            listbox.insert(tk.END, f)

        def open_selected(event=None):
            sel = listbox.curselection()
            if sel:
                self.load_file(Path(listbox.get(sel[0])))
                top.destroy()
        listbox.bind("<Double-1>", open_selected)
        tk.Button(top, text="打开", command=open_selected).pack(pady=5)

    def find_replace(self):
        top = tk.Toplevel(self.root)
        top.title("查找/替换")
        top.geometry("400x150")
        tk.Label(top, text="查找:").grid(row=0, column=0, padx=5, pady=5)
        find_entry = tk.Entry(top, width=30)
        find_entry.grid(row=0, column=1, padx=5, pady=5)
        tk.Label(top, text="替换:").grid(row=1, column=0, padx=5, pady=5)
        replace_entry = tk.Entry(top, width=30)
        replace_entry.grid(row=1, column=1, padx=5, pady=5)

        def do_replace():
            find = find_entry.get()
            replace = replace_entry.get()
            if not find:
                return
            text = self.editor.get_text()
            new_text = text.replace(find, replace)
            self.editor.set_text(new_text)
            top.destroy()

        tk.Button(top, text="替换全部", command=do_replace).grid(row=2, column=1, pady=10)

    def correct_code(self):
        if not self.correction_engine:
            messagebox.showerror("错误", "纠错引擎未加载")
            return
        text = self.editor.get_text()
        try:
            corrected, rules, warnings = self.correction_engine.correct(text)
            self.editor.set_text(corrected)
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert(tk.END, f"✅ 纠错完成\n")
            self.output_text.insert(tk.END, f"应用规则: {len(rules)} 条\n")
            self.output_text.insert(tk.END, f"警告: {len(warnings)} 条\n")
            if warnings:
                self.output_text.insert(tk.END, "\n".join(warnings[:10]) + "\n")
            self.status.config(text=f"纠错完成: {len(rules)} 条规则")
        except Exception as e:
            messagebox.showerror("错误", f"纠错失败: {e}")

    def compile_code(self):
        if not self.compiler:
            messagebox.showerror("错误", "编译器未加载")
            return
        text = self.editor.get_text()
        try:
            result = self.compiler.compile(text, self.current_file.name if self.current_file else "untitled.cnsh")
            self.compile_text.delete("1.0", tk.END)
            if result.get("success"):
                self.compile_text.insert(tk.END, "✅ 编译成功\n\n")
                self.compile_text.insert(tk.END, result.get("python_code", ""))
                self.status.config(text="编译成功")
            else:
                self.compile_text.insert(tk.END, "❌ 编译失败\n\n")
                for err in result.get("errors", []):
                    self.compile_text.insert(tk.END, f"  {err}\n")
                self.status.config(text="编译失败")
        except Exception as e:
            messagebox.showerror("错误", f"编译失败: {e}")

    def run_code(self):
        if not HAS_ENGINES:
            messagebox.showerror("错误", "执行引擎未加载")
            return
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, "▶ 运行中...\n")
        self.status.config(text="运行中...")

        def run_in_thread():
            text = self.editor.get_text()
            try:
                output, logs = CNSHInterpreterV2.run_script(text, use_real_ai=False)
                self.root.after(0, lambda: self._show_run_result(output, logs))
            except Exception as e:
                self.root.after(0, lambda: self._show_run_result(f"[错误] {e}", []))

        threading.Thread(target=run_in_thread, daemon=True).start()

    def _show_run_result(self, output: str, logs: List[str]):
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, output)
        self.log_text.delete("1.0", tk.END)
        for log in logs:
            self.log_text.insert(tk.END, log + "\n")
        self.status.config(text=f"运行完成: {len(logs)} 条日志")

    def show_about(self):
        messagebox.showinfo("关于", f"{APP_NAME} v{APP_VERSION}\n\nCNSH 中文语义超逻辑 IDE\n由 UID9622 创建")

    def show_syntax_help(self):
        help_text = """CNSH 核心语法：

设 变量 = 值
打印 变量

如果 条件
    打印 "成立"
结束

循环 i 在 范围(10)
    打印 i
结束

功能 函数名(参数)
    返回 结果
结束

理解 "自然语言描述"
记录 AI结果
"""
        top = tk.Toplevel(self.root)
        top.title("CNSH 语法")
        top.geometry("500x400")
        text = scrolledtext.ScrolledText(top, wrap=tk.WORD, font=("Courier New", 11))
        text.pack(fill=tk.BOTH, expand=True)
        text.insert("1.0", help_text)
        text.config(state=tk.DISABLED)


# ═══════════════════════════════════════════════════════
# 启动
# ═══════════════════════════════════════════════════════
def main():
    root = tk.Tk()
    app = CNSHIDE(root)

    # 如果命令行传入项目路径
    if len(sys.argv) > 1:
        project = Path(sys.argv[1])
        if project.exists() and project.is_dir():
            app.current_project = project
            app.file_browser.load(project)

    root.mainloop()


if __name__ == "__main__":
    main()
