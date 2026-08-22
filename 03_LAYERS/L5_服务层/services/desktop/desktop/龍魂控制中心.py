#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# -*- coding: utf-8 -*-
"""
龍魂控制中心 v1.0

所有按钮都有说明，不用靠脑子记。
普通人也能用，点一下就知道干什么。

DNA:#龍芯⚡️丙午·甲午·癸亥·戊午·䷚颐-LONGHUN-CONTROL-CENTER-FILE1-v1.0
"""

import json
import os
import subprocess
import sys
import tkinter as tk
from pathlib import Path
from tkinter import ttk, scrolledtext


ROOT = Path(__file__).resolve().parent.parent
REGISTRY = ROOT / "desktop" / "menu-registry.json"

CATEGORY_NAMES = {
    "desktop": "🐉 龍魂核心",
    "crypto-stack": "🔐 加密堆栈",
    "editor": "📝 编辑器",
    "cnsh-terminal": "🖥️ 终端与翻译",
    "xpay": "💱 主权支付",
    "executors/kimi-agent-v2": "🤖 Kimi Agent v2",
    "cnsh": "📚 CNSH 底座",
}


def load_items():
    """读取总注册表与所有模块 desktop-menu.json"""
    items = []

    # 总表
    if REGISTRY.exists():
        data = json.loads(REGISTRY.read_text(encoding="utf-8"))
        for item in data.get("items", []):
            item["source"] = "desktop"
            items.append(item)

    # 扫描模块菜单
    exclude = {".git", "__pycache__", ".pytest_cache", "node_modules", "venv", ".venv"}
    for path in ROOT.rglob("desktop-menu.json"):
        if any(part in exclude for part in path.parts):
            continue
        if path.resolve() == REGISTRY.resolve():
            continue
        data = json.loads(path.read_text(encoding="utf-8"))
        source = path.parent.relative_to(ROOT).as_posix()
        for item in data.get("items", []):
            item["source"] = source
            items.append(item)

    return items


def group_items(items):
    groups = {}
    for item in items:
        src = item.get("source", "other")
        groups.setdefault(src, []).append(item)
    return groups


def replace_root(cmd):
    return cmd.replace("{root}", str(ROOT))


class Tooltip:
    """简单悬浮提示"""
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tip = None
        widget.bind("<Enter>", self.show)
        widget.bind("<Leave>", self.hide)

    def show(self, event=None):
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 20
        y += self.widget.winfo_rooty() + 20
        self.tip = tk.Toplevel(self.widget)
        self.tip.wm_overrideredirect(True)
        self.tip.wm_geometry(f"+{x}+{y}")
        label = tk.Label(
            self.tip,
            text=self.text,
            justify=tk.LEFT,
            bg="#ffffcc",
            fg="#000000",
            relief=tk.SOLID,
            borderwidth=1,
            font=("PingFang SC", 12),
            wraplength=400,
        )
        label.pack()

    def hide(self, event=None):
        if self.tip:
            self.tip.destroy()
            self.tip = None


class 龍魂控制中心:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("龍魂控制中心 v1.0 · 点一下就懂")
        self.root.geometry("1400x900")
        self.root.configure(bg="#f5f5f5")

        self._建立标题()
        self._建立主区域()
        self._建立输出区()

    def _建立标题(self):
        header = tk.Frame(self.root, bg="#1a1a2e", height=60)
        header.pack(side=tk.TOP, fill=tk.X)
        tk.Label(
            header,
            text="🐉 龍魂控制中心 · 所有按钮都有说明",
            fg="white",
            bg="#1a1a2e",
            font=("PingFang SC", 20, "bold"),
        ).pack(side=tk.LEFT, padx=20, pady=10)

        ttk.Button(
            header,
            text="🔄 刷新菜单",
            command=self._刷新菜单,
        ).pack(side=tk.RIGHT, padx=10, pady=10)

    def _建立主区域(self):
        container = tk.Frame(self.root, bg="#f5f5f5")
        container.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)

        canvas = tk.Canvas(container, bg="#f5f5f5", highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient=tk.VERTICAL, command=canvas.yview)
        self.滚动框架 = tk.Frame(canvas, bg="#f5f5f5")

        self.滚动框架.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all")),
        )
        canvas.create_window((0, 0), window=self.滚动框架, anchor="nw", width=1360)
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self._填充卡片()

    def _填充卡片(self):
        # 清空旧卡片
        for widget in self.滚动框架.winfo_children():
            widget.destroy()

        items = load_items()
        groups = group_items(items)

        row = 0
        for source in sorted(groups.keys(), key=lambda s: list(CATEGORY_NAMES.keys()).index(s) if s in CATEGORY_NAMES else 999):
            group_items_list = groups[source]
            title = CATEGORY_NAMES.get(source, source)

            # 分类标题
            tk.Label(
                self.滚动框架,
                text=title,
                bg="#f5f5f5",
                fg="#1a1a2e",
                font=("PingFang SC", 16, "bold"),
                anchor="w",
            ).grid(row=row, column=0, columnspan=4, sticky="w", pady=(20, 10), padx=10)
            row += 1

            col = 0
            for item in group_items_list:
                if item.get("type") == "quit":
                    continue
                card = self._建立卡片(self.滚动框架, item)
                card.grid(row=row, column=col, padx=10, pady=10, sticky="nw")
                col += 1
                if col >= 4:
                    col = 0
                    row += 1
            if col != 0:
                row += 1

    def _建立卡片(self, parent, item):
        frame = tk.Frame(
            parent,
            bg="white",
            bd=1,
            relief=tk.SOLID,
            highlightbackground="#ddd",
            highlightthickness=1,
            width=320,
            height=160,
        )
        frame.grid_propagate(False)
        frame.pack_propagate(False)

        label = item.get("label", "未命名")
        desc = item.get("description", "")

        title_lbl = tk.Label(
            frame,
            text=label,
            bg="white",
            fg="#1a1a2e",
            font=("PingFang SC", 14, "bold"),
            anchor="w",
            wraplength=300,
        )
        title_lbl.pack(fill=tk.X, padx=10, pady=(10, 2))

        desc_lbl = tk.Label(
            frame,
            text=desc,
            bg="white",
            fg="#666666",
            font=("PingFang SC", 11),
            anchor="w",
            justify=tk.LEFT,
            wraplength=300,
        )
        desc_lbl.pack(fill=tk.X, padx=10, pady=(0, 8))

        btn = ttk.Button(
            frame,
            text="▶ 执行",
            command=lambda it=item: self._执行(it),
        )
        btn.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)

        Tooltip(frame, desc)

        return frame

    def _执行(self, item):
        item_type = item.get("type", "shell")
        label = item.get("label", "未命名")
        self._输出(f"\n>>> 正在执行：{label}")

        if item_type == "shell":
            cmd = replace_root(item.get("command", ""))
            self._运行(cmd, shell=True)
        elif item_type == "open_url":
            url = item.get("url", "")
            self._运行(f"open '{url}'", shell=True)
        elif item_type == "open_app":
            app = item.get("app", "Terminal")
            path = replace_root(item.get("path", ""))
            self._运行(f"open -a '{app}' '{path}'", shell=True)
        else:
            self._输出(f"未支持的类型：{item_type}")

    def _运行(self, cmd, shell=False):
        self._输出(f"$ {cmd}")
        try:
            proc = subprocess.Popen(
                cmd if shell else cmd.split(),
                shell=shell,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                cwd=ROOT,
            )
            for line in proc.stdout:
                self._输出(line.rstrip())
            proc.wait()
            self._输出(f"[退出码: {proc.returncode}]")
        except Exception as e:
            self._输出(f"[错误] {e}")

    def _建立输出区(self):
        tk.Label(
            self.root,
            text="📋 执行输出",
            bg="#f5f5f5",
            fg="#333",
            font=("PingFang SC", 12, "bold"),
            anchor="w",
        ).pack(side=tk.TOP, fill=tk.X, padx=10, pady=(5, 0))

        self.输出区 = scrolledtext.ScrolledText(
            self.root,
            height=10,
            wrap=tk.WORD,
            bg="#0e0e0e",
            fg="#cccccc",
            font=("PingFang SC", 12),
            state=tk.NORMAL,
        )
        self.输出区.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)

    def _输出(self, text):
        self.输出区.configure(state=tk.NORMAL)
        self.输出区.insert(tk.END, text + "\n")
        self.输出区.see(tk.END)
        self.输出区.configure(state=tk.DISABLED)

    def _刷新菜单(self):
        self._输出("🔄 正在刷新菜单...")
        try:
            subprocess.run(
                ["bash", str(ROOT / "bin" / "build-desktop-switch.sh")],
                cwd=ROOT,
                check=True,
            )
            self._填充卡片()
            self._输出("✅ 菜单刷新完成")
        except Exception as e:
            self._输出(f"[刷新失败] {e}")


def main():
    root = tk.Tk()
    app = 龍魂控制中心(root)
    root.mainloop()


if __name__ == "__main__":
    main()
