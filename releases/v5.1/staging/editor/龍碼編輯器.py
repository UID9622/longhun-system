#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍码中文编辑器 v1.0

没有黑箱，代码全部公开。
中文就是变量名，中文就是注释，中文就是逻辑。
每个国家的语言都能跑在计算机里面，那才叫牛逼。

DNA:#龍芯⚡️2026-06-18-LONGHUN-CHINESE-EDITOR-FILE1-v1.0-1
"""

import os
import subprocess
import sys
import tkinter as tk
from pathlib import Path
from tkinter import messagebox, scrolledtext, filedialog, ttk


class 龍码编辑器:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("龍码中文编辑器 v1.0")
        self.root.geometry("1200x800")
        self.root.configure(bg="#1e1e1e")

        self.当前文件 = None
        self.已修改 = False

        self._建立菜单()
        self._建立工具栏()
        self._建立编辑区()
        self._建立输出区()
        self._建立状态栏()

        self.编辑区.bind("<KeyRelease>", self._标记已修改)
        self.编辑区.bind("<ButtonRelease>", self._更新游标位置)

        self._设置字体()
        self._新建文件()

    def _设置字体(self):
        """统一字型，优先支持中文"""
        self.字体 = ("PingFang SC", 16)  # macOS 中文字型
        self.编辑区.configure(font=self.字体)
        self.输出区.configure(font=self.字体)

    def _建立菜单(self):
        menubar = tk.Menu(self.root)

        文件 = tk.Menu(menubar, tearoff=0)
        文件.add_command(label="新建", command=self._新建文件, accelerator="Cmd+N")
        文件.add_command(label="打开", command=self._打开文件, accelerator="Cmd+O")
        文件.add_command(label="保存", command=self._保存文件, accelerator="Cmd+S")
        文件.add_command(label="另存为", command=self._另存为)
        文件.add_separator()
        文件.add_command(label="退出", command=self._退出)
        menubar.add_cascade(label="文件", menu=文件)

        编辑 = tk.Menu(menubar, tearoff=0)
        编辑.add_command(label="撤销", command=self._撤销, accelerator="Cmd+Z")
        编辑.add_command(label="重做", command=self._重做, accelerator="Cmd+Shift+Z")
        编辑.add_separator()
        编辑.add_command(label="剪切", command=self._剪切, accelerator="Cmd+X")
        编辑.add_command(label="复制", command=self._复制, accelerator="Cmd+C")
        编辑.add_command(label="粘贴", command=self._粘贴, accelerator="Cmd+V")
        menubar.add_cascade(label="编辑", menu=编辑)

        运行 = tk.Menu(menubar, tearoff=0)
        运行.add_command(label="运行 Python", command=self._运行Python, accelerator="F5")
        运行.add_command(label="运行 Shell 命令", command=self._运行Shell)
        运行.add_command(label="清空输出", command=self._清空输出)
        menubar.add_cascade(label="运行", menu=运行)

        通心译 = tk.Menu(menubar, tearoff=0)
        通心译.add_command(label="英→中", command=lambda: self._通心译翻译("en2zh"), accelerator="F9")
        通心译.add_command(label="中→英", command=lambda: self._通心译翻译("zh2en"), accelerator="F10")
        通心译.add_command(label="双语", command=lambda: self._通心译翻译("bilingual"), accelerator="F11")
        通心译.add_command(label="加密选中内容", command=self._加密选中)
        通心译.add_command(label="解密选中内容", command=self._解密选中)
        menubar.add_cascade(label="通心译", menu=通心译)

        帮助 = tk.Menu(menubar, tearoff=0)
        帮助.add_command(label="关于龍码", command=self._关于)
        menubar.add_cascade(label="帮助", menu=帮助)

        self.root.config(menu=menubar)

        # 快捷键绑定
        self.root.bind("<Command-n>", lambda e: self._新建文件())
        self.root.bind("<Command-o>", lambda e: self._打开文件())
        self.root.bind("<Command-s>", lambda e: self._保存文件())
        self.root.bind("<F5>", lambda e: self._运行Python())
        self.root.bind("<F9>", lambda e: self._通心译翻译("en2zh"))
        self.root.bind("<F10>", lambda e: self._通心译翻译("zh2en"))
        self.root.bind("<F11>", lambda e: self._通心译翻译("bilingual"))

    def _建立工具栏(self):
        toolbar = ttk.Frame(self.root)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        buttons = [
            ("新建", self._新建文件),
            ("打开", self._打开文件),
            ("保存", self._保存文件),
            ("运行", self._运行Python),
            ("英→中", lambda: self._通心译翻译("en2zh")),
            ("中→英", lambda: self._通心译翻译("zh2en")),
            ("清空", self._清空输出),
        ]

        for label, cmd in buttons:
            btn = ttk.Button(toolbar, text=label, command=cmd)
            btn.pack(side=tk.LEFT, padx=2, pady=2)

    def _建立编辑区(self):
        frame = ttk.Frame(self.root)
        frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        scrollbar_y = ttk.Scrollbar(frame)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)

        scrollbar_x = ttk.Scrollbar(frame, orient=tk.HORIZONTAL)
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)

        self.编辑区 = tk.Text(
            frame,
            wrap=tk.NONE,
            undo=True,
            bg="#1e1e1e",
            fg="#d4d4d4",
            insertbackground="#ffffff",
            selectbackground="#264f78",
            yscrollcommand=scrollbar_y.set,
            xscrollcommand=scrollbar_x.set,
        )
        self.编辑区.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar_y.config(command=self.编辑区.yview)
        scrollbar_x.config(command=self.编辑区.xview)

    def _建立输出区(self):
        self.输出区 = scrolledtext.ScrolledText(
            self.root,
            height=10,
            wrap=tk.WORD,
            bg="#0e0e0e",
            fg="#cccccc",
            insertbackground="#ffffff",
            state=tk.DISABLED,
        )
        self.输出区.pack(side=tk.BOTTOM, fill=tk.X)

    def _建立状态栏(self):
        self.状态栏 = ttk.Label(self.root, text="就绪", anchor=tk.W)
        self.状态栏.pack(side=tk.BOTTOM, fill=tk.X)

    def _标记已修改(self, event=None):
        if not self.已修改:
            self.已修改 = True
            self._更新标题()
        self._更新游标位置()

    def _更新标题(self):
        name = self.当前文件.name if self.当前文件 else "未命名.龍"
        mark = " *" if self.已修改 else ""
        self.root.title(f"龍码中文编辑器 v1.0 - {name}{mark}")

    def _更新游标位置(self, event=None):
        try:
            pos = self.编辑区.index(tk.INSERT)
            line, col = pos.split(".")
            self.状态栏.config(text=f"位置: 第 {line} 行, 第 {int(col)+1} 列 | 文件: {self.当前文件 or '未命名.龍'}")
        except Exception:
            pass

    def _输出(self, text: str):
        self.输出区.configure(state=tk.NORMAL)
        self.输出区.insert(tk.END, text + "\n")
        self.输出区.see(tk.END)
        self.输出区.configure(state=tk.DISABLED)

    def _清空输出(self):
        self.输出区.configure(state=tk.NORMAL)
        self.输出区.delete(1.0, tk.END)
        self.输出区.configure(state=tk.DISABLED)

    def _新建文件(self):
        if self._询问保存():
            return
        self.编辑区.delete(1.0, tk.END)
        self.当前文件 = None
        self.已修改 = False
        self._更新标题()
        self._输出("[文件] 新建文件完成")

    def _打开文件(self):
        if self._询问保存():
            return
        path = filedialog.askopenfilename(
            title="打开文件",
            filetypes=[("所有文件", "*.*"), ("龍码文件", "*.龍"), ("Python", "*.py")],
        )
        if not path:
            return
        try:
            content = Path(path).read_text(encoding="utf-8")
            self.编辑区.delete(1.0, tk.END)
            self.编辑区.insert(1.0, content)
            self.当前文件 = Path(path)
            self.已修改 = False
            self._更新标题()
            self._输出(f"[文件] 已打开: {path}")
        except Exception as e:
            messagebox.showerror("错误", f"无法打开文件:\n{e}")

    def _保存文件(self):
        if self.当前文件:
            self._写入文件(self.当前文件)
        else:
            self._另存为()

    def _另存为(self):
        path = filedialog.asksaveasfilename(
            title="另存为",
            defaultextension=".龍",
            filetypes=[("龍码文件", "*.龍"), ("Python", "*.py"), ("所有文件", "*.*")],
        )
        if not path:
            return
        self._写入文件(Path(path))

    def _写入文件(self, path: Path):
        try:
            content = self.编辑区.get(1.0, tk.END)
            path.write_text(content, encoding="utf-8")
            self.当前文件 = path
            self.已修改 = False
            self._更新标题()
            self._输出(f"[文件] 已保存: {path}")
        except Exception as e:
            messagebox.showerror("错误", f"无法保存文件:\n{e}")

    def _询问保存(self):
        if not self.已修改:
            return False
        answer = messagebox.askyesnocancel("未保存", "当前文件已修改，是否保存？")
        if answer is True:
            self._保存文件()
            return False
        elif answer is False:
            return False
        else:
            return True

    def _撤销(self):
        try:
            self.编辑区.edit_undo()
        except tk.TclError:
            pass

    def _重做(self):
        try:
            self.编辑区.edit_redo()
        except tk.TclError:
            pass

    def _剪切(self):
        self.编辑区.event_generate("<<Cut>>")

    def _复制(self):
        self.编辑区.event_generate("<<Copy>>")

    def _粘贴(self):
        self.编辑区.event_generate("<<Paste>>")

    def _运行Python(self):
        content = self.编辑区.get(1.0, tk.END)
        if not content.strip():
            self._输出("[运行] 编辑区为空")
            return

        # 优先保存当前文件再运行
        if self.当前文件:
            self._保存文件()
            script_path = self.当前文件
        else:
            # 临时文件运行
            script_path = Path.home() / ".longhun" / "editor_tmp.py"
            script_path.parent.mkdir(parents=True, exist_ok=True)
            script_path.write_text(content, encoding="utf-8")

        self._输出(f"[运行] 正在执行: {script_path}")
        try:
            result = subprocess.run(
                [sys.executable, str(script_path)],
                capture_output=True,
                text=True,
                timeout=30,
            )
            if result.stdout:
                self._输出(result.stdout)
            if result.stderr:
                self._输出("[错误输出]\n" + result.stderr)
            self._输出(f"[运行] 退出码: {result.returncode}")
        except subprocess.TimeoutExpired:
            self._输出("[错误] 运行超时")
        except Exception as e:
            self._输出(f"[错误] {e}")

    def _运行Shell(self):
        content = self.编辑区.get("sel.first", "sel.last") if self.编辑区.tag_ranges("sel") else ""
        if not content.strip():
            self._输出("[Shell] 请先选中要运行的命令")
            return
        try:
            result = subprocess.run(
                content.strip(),
                shell=True,
                capture_output=True,
                text=True,
                timeout=30,
            )
            self._输出(result.stdout + result.stderr)
        except Exception as e:
            self._输出(f"[Shell 错误] {e}")

    def _通心译翻译(self, mode: str):
        """调用 CNSH 通心译引擎翻译选中文字"""
        if not self.编辑区.tag_ranges("sel"):
            self._输出("[通心译] 请先选中要翻译的文字")
            return

        text = self.编辑区.get("sel.first", "sel.last").strip()
        if not text:
            self._输出("[通心译] 选中内容为空")
            return

        root = Path(__file__).resolve().parent.parent
        terminal = root / "cnsh-terminal" / "cnsh_terminal_v5.py"

        self._输出(f"[通心译] 模式: {mode} | 原文: {text[:60]}")
        try:
            result = subprocess.run(
                [sys.executable, str(terminal), "translate", text],
                capture_output=True,
                text=True,
                timeout=30,
            )
            if result.stdout:
                self._输出(result.stdout)
            if result.stderr:
                self._输出("[通心译 错误]\n" + result.stderr)
        except Exception as e:
            self._输出(f"[通心译 错误] {e}")

    def _加密选中(self):
        """调用 CNSH 终端加密选中内容"""
        if not self.编辑区.tag_ranges("sel"):
            self._输出("[加密] 请先选中要加密的文字")
            return
        text = self.编辑区.get("sel.first", "sel.last").strip()
        root = Path(__file__).resolve().parent.parent
        terminal = root / "cnsh-terminal" / "cnsh_terminal_v5.py"
        self._输出(f"[加密] 原文: {text[:60]}")
        try:
            result = subprocess.run(
                [sys.executable, str(terminal), "encrypt", text],
                capture_output=True,
                text=True,
                timeout=30,
            )
            self._输出(result.stdout + result.stderr)
        except Exception as e:
            self._输出(f"[加密 错误] {e}")

    def _解密选中(self):
        """调用 CNSH 终端解密选中内容"""
        if not self.编辑区.tag_ranges("sel"):
            self._输出("[解密] 请先选中要解密的密文")
            return
        text = self.编辑区.get("sel.first", "sel.last").strip()
        root = Path(__file__).resolve().parent.parent
        terminal = root / "cnsh-terminal" / "cnsh_terminal_v5.py"
        self._输出("[解密] 正在解密...")
        try:
            result = subprocess.run(
                [sys.executable, str(terminal), "decrypt", text],
                capture_output=True,
                text=True,
                timeout=30,
            )
            self._输出(result.stdout + result.stderr)
        except Exception as e:
            self._输出(f"[解密 错误] {e}")

    def _关于(self):
        messagebox.showinfo(
            "关于龍码",
            "龍码中文编辑器 v1.0\n\n"
            "没有黑箱，代码全部公开。\n"
            "中文就是变量名，中文就是注释，中文就是逻辑。\n\n"
            "已接入通心译与 CNSH 加密通信。\n\n"
            "DNA:#龍芯⚡️2026-06-18-LONGHUN-CHINESE-EDITOR-v1.0"
        )

    def _退出(self):
        if self._询问保存():
            return
        self.root.destroy()


def main():
    root = tk.Tk()
    app = 龍码编辑器(root)
    root.mainloop()


if __name__ == "__main__":
    main()
