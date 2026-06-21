#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍碼中文編輯器 v1.0

沒有黑箱，代碼全部公開。
中文就是變量名，中文就是註釋，中文就是邏輯。
每個國家的語言都能跑在計算機裡面，那才叫牛逼。

DNA:#龍芯⚡️2026-06-18-LONGHUN-CHINESE-EDITOR-FILE1-FILE1-v1.0-1
"""

import os
import subprocess
import sys
import tkinter as tk
from pathlib import Path
from tkinter import messagebox, scrolledtext, filedialog, ttk


class 龍碼編輯器:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("龍碼中文編輯器 v1.0")
        self.root.geometry("1200x800")
        self.root.configure(bg="#1e1e1e")

        self.當前文件 = None
        self.已修改 = False

        self._建立菜單()
        self._建立工具欄()
        self._建立編輯區()
        self._建立輸出區()
        self._建立狀態欄()

        self.編輯區.bind("<KeyRelease>", self._標記已修改)
        self.編輯區.bind("<ButtonRelease>", self._更新游標位置)

        self._設置字體()
        self._新建文件()

    def _設置字體(self):
        """統一字型，優先支持中文"""
        self.字體 = ("PingFang SC", 16)  # macOS 中文字型
        self.編輯區.configure(font=self.字體)
        self.輸出區.configure(font=self.字體)

    def _建立菜單(self):
        menubar = tk.Menu(self.root)

        文件 = tk.Menu(menubar, tearoff=0)
        文件.add_command(label="新建", command=self._新建文件, accelerator="Cmd+N")
        文件.add_command(label="打開", command=self._打開文件, accelerator="Cmd+O")
        文件.add_command(label="保存", command=self._保存文件, accelerator="Cmd+S")
        文件.add_command(label="另存為", command=self._另存為)
        文件.add_separator()
        文件.add_command(label="退出", command=self._退出)
        menubar.add_cascade(label="文件", menu=文件)

        編輯 = tk.Menu(menubar, tearoff=0)
        編輯.add_command(label="撤銷", command=self._撤銷, accelerator="Cmd+Z")
        編輯.add_command(label="重做", command=self._重做, accelerator="Cmd+Shift+Z")
        編輯.add_separator()
        編輯.add_command(label="剪切", command=self._剪切, accelerator="Cmd+X")
        編輯.add_command(label="複製", command=self._複製, accelerator="Cmd+C")
        編輯.add_command(label="粘貼", command=self._粘貼, accelerator="Cmd+V")
        menubar.add_cascade(label="編輯", menu=編輯)

        運行 = tk.Menu(menubar, tearoff=0)
        運行.add_command(label="運行 Python", command=self._運行Python, accelerator="F5")
        運行.add_command(label="運行 Shell 命令", command=self._運行Shell)
        運行.add_command(label="清空輸出", command=self._清空輸出)
        menubar.add_cascade(label="運行", menu=運行)

        通心译 = tk.Menu(menubar, tearoff=0)
        通心译.add_command(label="英→中", command=lambda: self._通心译翻譯("en2zh"), accelerator="F9")
        通心译.add_command(label="中→英", command=lambda: self._通心译翻譯("zh2en"), accelerator="F10")
        通心译.add_command(label="雙語", command=lambda: self._通心译翻譯("bilingual"), accelerator="F11")
        通心译.add_command(label="加密選中內容", command=self._加密選中)
        通心译.add_command(label="解密選中內容", command=self._解密選中)
        menubar.add_cascade(label="通心译", menu=通心译)

        幫助 = tk.Menu(menubar, tearoff=0)
        幫助.add_command(label="關於龍碼", command=self._關於)
        menubar.add_cascade(label="幫助", menu=幫助)

        self.root.config(menu=menubar)

        # 快捷鍵綁定
        self.root.bind("<Command-n>", lambda e: self._新建文件())
        self.root.bind("<Command-o>", lambda e: self._打開文件())
        self.root.bind("<Command-s>", lambda e: self._保存文件())
        self.root.bind("<F5>", lambda e: self._運行Python())
        self.root.bind("<F9>", lambda e: self._通心译翻譯("en2zh"))
        self.root.bind("<F10>", lambda e: self._通心译翻譯("zh2en"))
        self.root.bind("<F11>", lambda e: self._通心译翻譯("bilingual"))

    def _建立工具欄(self):
        toolbar = ttk.Frame(self.root)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        buttons = [
            ("新建", self._新建文件),
            ("打開", self._打開文件),
            ("保存", self._保存文件),
            ("運行", self._運行Python),
            ("英→中", lambda: self._通心译翻譯("en2zh")),
            ("中→英", lambda: self._通心译翻譯("zh2en")),
            ("清空", self._清空輸出),
        ]

        for label, cmd in buttons:
            btn = ttk.Button(toolbar, text=label, command=cmd)
            btn.pack(side=tk.LEFT, padx=2, pady=2)

    def _建立編輯區(self):
        frame = ttk.Frame(self.root)
        frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        scrollbar_y = ttk.Scrollbar(frame)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)

        scrollbar_x = ttk.Scrollbar(frame, orient=tk.HORIZONTAL)
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)

        self.編輯區 = tk.Text(
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
        self.編輯區.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar_y.config(command=self.編輯區.yview)
        scrollbar_x.config(command=self.編輯區.xview)

    def _建立輸出區(self):
        self.輸出區 = scrolledtext.ScrolledText(
            self.root,
            height=10,
            wrap=tk.WORD,
            bg="#0e0e0e",
            fg="#cccccc",
            insertbackground="#ffffff",
            state=tk.DISABLED,
        )
        self.輸出區.pack(side=tk.BOTTOM, fill=tk.X)

    def _建立狀態欄(self):
        self.狀態欄 = ttk.Label(self.root, text="就緒", anchor=tk.W)
        self.狀態欄.pack(side=tk.BOTTOM, fill=tk.X)

    def _標記已修改(self, event=None):
        if not self.已修改:
            self.已修改 = True
            self._更新標題()
        self._更新游標位置()

    def _更新標題(self):
        name = self.當前文件.name if self.當前文件 else "未命名.龍"
        mark = " *" if self.已修改 else ""
        self.root.title(f"龍碼中文編輯器 v1.0 - {name}{mark}")

    def _更新游標位置(self, event=None):
        try:
            pos = self.編輯區.index(tk.INSERT)
            line, col = pos.split(".")
            self.狀態欄.config(text=f"位置: 第 {line} 行, 第 {int(col)+1} 列 | 文件: {self.當前文件 or '未命名.龍'}")
        except Exception:
            pass

    def _輸出(self, text: str):
        self.輸出區.configure(state=tk.NORMAL)
        self.輸出區.insert(tk.END, text + "\n")
        self.輸出區.see(tk.END)
        self.輸出區.configure(state=tk.DISABLED)

    def _清空輸出(self):
        self.輸出區.configure(state=tk.NORMAL)
        self.輸出區.delete(1.0, tk.END)
        self.輸出區.configure(state=tk.DISABLED)

    def _新建文件(self):
        if self._詢問保存():
            return
        self.編輯區.delete(1.0, tk.END)
        self.當前文件 = None
        self.已修改 = False
        self._更新標題()
        self._輸出("[文件] 新建文件完成")

    def _打開文件(self):
        if self._詢問保存():
            return
        path = filedialog.askopenfilename(
            title="打開文件",
            filetypes=[("所有文件", "*.*"), ("龍碼文件", "*.龍"), ("Python", "*.py")],
        )
        if not path:
            return
        try:
            content = Path(path).read_text(encoding="utf-8")
            self.編輯區.delete(1.0, tk.END)
            self.編輯區.insert(1.0, content)
            self.當前文件 = Path(path)
            self.已修改 = False
            self._更新標題()
            self._輸出(f"[文件] 已打開: {path}")
        except Exception as e:
            messagebox.showerror("錯誤", f"無法打開文件:\n{e}")

    def _保存文件(self):
        if self.當前文件:
            self._寫入文件(self.當前文件)
        else:
            self._另存為()

    def _另存為(self):
        path = filedialog.asksaveasfilename(
            title="另存為",
            defaultextension=".龍",
            filetypes=[("龍碼文件", "*.龍"), ("Python", "*.py"), ("所有文件", "*.*")],
        )
        if not path:
            return
        self._寫入文件(Path(path))

    def _寫入文件(self, path: Path):
        try:
            content = self.編輯區.get(1.0, tk.END)
            path.write_text(content, encoding="utf-8")
            self.當前文件 = path
            self.已修改 = False
            self._更新標題()
            self._輸出(f"[文件] 已保存: {path}")
        except Exception as e:
            messagebox.showerror("錯誤", f"無法保存文件:\n{e}")

    def _詢問保存(self):
        if not self.已修改:
            return False
        answer = messagebox.askyesnocancel("未保存", "當前文件已修改，是否保存？")
        if answer is True:
            self._保存文件()
            return False
        elif answer is False:
            return False
        else:
            return True

    def _撤銷(self):
        try:
            self.編輯區.edit_undo()
        except tk.TclError:
            pass

    def _重做(self):
        try:
            self.編輯區.edit_redo()
        except tk.TclError:
            pass

    def _剪切(self):
        self.編輯區.event_generate("<<Cut>>")

    def _複製(self):
        self.編輯區.event_generate("<<Copy>>")

    def _粘貼(self):
        self.編輯區.event_generate("<<Paste>>")

    def _運行Python(self):
        content = self.編輯區.get(1.0, tk.END)
        if not content.strip():
            self._輸出("[運行] 編輯區為空")
            return

        # 優先保存當前文件再運行
        if self.當前文件:
            self._保存文件()
            script_path = self.當前文件
        else:
            # 臨時文件運行
            script_path = Path.home() / ".longhun" / "editor_tmp.py"
            script_path.parent.mkdir(parents=True, exist_ok=True)
            script_path.write_text(content, encoding="utf-8")

        self._輸出(f"[運行] 正在執行: {script_path}")
        try:
            result = subprocess.run(
                [sys.executable, str(script_path)],
                capture_output=True,
                text=True,
                timeout=30,
            )
            if result.stdout:
                self._輸出(result.stdout)
            if result.stderr:
                self._輸出("[錯誤輸出]\n" + result.stderr)
            self._輸出(f"[運行] 退出碼: {result.returncode}")
        except subprocess.TimeoutExpired:
            self._輸出("[錯誤] 運行超時")
        except Exception as e:
            self._輸出(f"[錯誤] {e}")

    def _運行Shell(self):
        content = self.編輯區.get("sel.first", "sel.last") if self.編輯區.tag_ranges("sel") else ""
        if not content.strip():
            self._輸出("[Shell] 請先選中要運行的命令")
            return
        try:
            result = subprocess.run(
                content.strip(),
                shell=True,
                capture_output=True,
                text=True,
                timeout=30,
            )
            self._輸出(result.stdout + result.stderr)
        except Exception as e:
            self._輸出(f"[Shell 錯誤] {e}")

    def _通心译翻譯(self, mode: str):
        """調用 CNSH 通心译引擎翻譯選中文字"""
        if not self.編輯區.tag_ranges("sel"):
            self._輸出("[通心译] 請先選中要翻譯的文字")
            return

        text = self.編輯區.get("sel.first", "sel.last").strip()
        if not text:
            self._輸出("[通心译] 選中內容為空")
            return

        root = Path(__file__).resolve().parent.parent
        terminal = root / "cnsh-terminal" / "cnsh_terminal_v5.py"

        self._輸出(f"[通心译] 模式: {mode} | 原文: {text[:60]}")
        try:
            result = subprocess.run(
                [sys.executable, str(terminal), "translate", text],
                capture_output=True,
                text=True,
                timeout=30,
            )
            if result.stdout:
                self._輸出(result.stdout)
            if result.stderr:
                self._輸出("[通心译 錯誤]\n" + result.stderr)
        except Exception as e:
            self._輸出(f"[通心译 錯誤] {e}")

    def _加密選中(self):
        """調用 CNSH 終端加密選中內容"""
        if not self.編輯區.tag_ranges("sel"):
            self._輸出("[加密] 請先選中要加密的文字")
            return
        text = self.編輯區.get("sel.first", "sel.last").strip()
        root = Path(__file__).resolve().parent.parent
        terminal = root / "cnsh-terminal" / "cnsh_terminal_v5.py"
        self._輸出(f"[加密] 原文: {text[:60]}")
        try:
            result = subprocess.run(
                [sys.executable, str(terminal), "encrypt", text],
                capture_output=True,
                text=True,
                timeout=30,
            )
            self._輸出(result.stdout + result.stderr)
        except Exception as e:
            self._輸出(f"[加密 錯誤] {e}")

    def _解密選中(self):
        """調用 CNSH 終端解密選中內容"""
        if not self.編輯區.tag_ranges("sel"):
            self._輸出("[解密] 請先選中要解密的密文")
            return
        text = self.編輯區.get("sel.first", "sel.last").strip()
        root = Path(__file__).resolve().parent.parent
        terminal = root / "cnsh-terminal" / "cnsh_terminal_v5.py"
        self._輸出("[解密] 正在解密...")
        try:
            result = subprocess.run(
                [sys.executable, str(terminal), "decrypt", text],
                capture_output=True,
                text=True,
                timeout=30,
            )
            self._輸出(result.stdout + result.stderr)
        except Exception as e:
            self._輸出(f"[解密 錯誤] {e}")

    def _關於(self):
        messagebox.showinfo(
            "關於龍碼",
            "龍碼中文編輯器 v1.0\n\n"
            "沒有黑箱，代碼全部公開。\n"
            "中文就是變量名，中文就是註釋，中文就是邏輯。\n\n"
            "已接入通心译與 CNSH 加密通信。\n\n"
            "DNA:#龍芯⚡️2026-06-18-LONGHUN-CHINESE-EDITOR-v1.0"
        )

    def _退出(self):
        if self._詢問保存():
            return
        self.root.destroy()


def main():
    root = tk.Tk()
    app = 龍碼編輯器(root)
    root.mainloop()


if __name__ == "__main__":
    main()
