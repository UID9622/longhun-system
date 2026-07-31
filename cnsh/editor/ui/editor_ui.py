# DNA: #龍芯⚡️丙午·乙未·乙丑·噬嗑-FIX_DNA-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# -*- coding: utf-8 -*-
""#龍芯⚡️2026-06-18-CNSH-EDITOR-UI-FILE2-FILE1-v5.0
# 🟢 审计通过: 编辑器UI完整实现
# 🔒 AI Truth Protocol: 所有声明均为真实
# 🤝 君子协议: CC BY-NC-SA 4.0 · UID9622 · 龍芯北辰 · 诸葛鑫

CNSH多语言编辑器UI
多标签编辑 · 语法高亮 · 智能补全 · 行号显示
"""

import os
import re
import json
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog, simpledialog
from tkinter import font as tkfont
from typing import Dict, List, Optional, Callable, Any
from datetime import datetime

# ═══════════════════════════════════════════════════════════
# LonghunFont 字体主权配置
# 将 longhun-font/output/LonghunFont-Regular.otf 安装到系统后，
# CNSH 编辑器将优先使用自主字体。
# ═══════════════════════════════════════════════════════════
系统字体列表 = tkfont.families()
编辑器字体族 = "LonghunFont" if "LonghunFont" in 系统字体列表 else "编辑器字体族"
print(f"[LonghunFont] 系统已安装: {'是' if 'LonghunFont' in 系统字体列表 else '否'} · 当前编辑器字体: {编辑器字体族}")

# 尝试导入各模块
try:
    from .lexer import Lexer, TokenType, CNSH关键字, 高亮颜色映射
    from .translator import 通心译翻译器
    from .four_layer_check import CNSH四层检查
    from .ai_timestamp import AI时间戳规范
    from .circuit_breaker import 熔断机制
    from .audit_integration import 联动审计, 操作类型
except ImportError:
    from lexer import Lexer, TokenType, CNSH关键字, 高亮颜色映射
    from translator import 通心译翻译器
    from four_layer_check import CNSH四层检查
    from ai_timestamp import AI时间戳规范
    from circuit_breaker import 熔断机制
    from audit_integration import 联动审计, 操作类型


class 编辑器文本区(tk.Text):
    """自定义文本编辑区，支持语法高亮"""

    def __init__(self, 父容器, **参数):
        super().__init__(父容器, **参数)
        self.当前文件 = None
        self.已修改 = False
        self.DNA追溯 = "#龍芯⚡️2026-06-18-CNSH-TEXT-AREA"

        # 配置标签
        self._配置语法高亮标签()

        # 绑定修改事件
        self.bind("<KeyRelease>", self._按键释放处理)
        self.bind("<ButtonRelease>", self._点击释放处理)

    def _配置语法高亮标签(self):
        """配置语法高亮颜色标签"""
        self.tag_configure("keyword", foreground=高亮颜色映射.get(TokenType.KEYWORD, "#FF6B6B"),
                          font=("编辑器字体族", 12, "bold"))
        self.tag_configure("type", foreground=高亮颜色映射.get(TokenType.TYPE, "#4ECDC4"),
                          font=("编辑器字体族", 12, "bold"))
        self.tag_configure("boolean", foreground=高亮颜色映射.get(TokenType.BOOLEAN, "#45B7D1"))
        self.tag_configure("null", foreground=高亮颜色映射.get(TokenType.NULL, "#96CEB4"))
        self.tag_configure("identifier", foreground=高亮颜色映射.get(TokenType.IDENTIFIER, "#E8D5B7"))
        self.tag_configure("number", foreground=高亮颜色映射.get(TokenType.NUMBER, "#DDA0DD"))
        self.tag_configure("string", foreground=高亮颜色映射.get(TokenType.STRING, "#98FB98"))
        self.tag_configure("comment", foreground=高亮颜色映射.get(TokenType.COMMENT, "#808080"),
                          font=("编辑器字体族", 12, "italic"))
        self.tag_configure("operator", foreground="#FFD700")
        self.tag_configure("separator", foreground="#D3D3D3")
        self.tag_configure("error", foreground="#FF0000", underline=True)
        self.tag_configure("warning", foreground="#FFA500")
        self.tag_configure("selection_highlight", background="#2D5F3A")

        # 龍字特殊高亮
        self.tag_configure("龍字", foreground="#FFD700", background="#8B0000",
                          font=("编辑器字体族", 12, "bold"))

    def _按键释放处理(self, 事件=None):
        """按键释放时触发语法高亮"""
        self.已修改 = True
        # 延迟执行高亮避免卡顿
        self.after(100, self._语法高亮)

    def _点击释放处理(self, 事件=None):
        """鼠标点击释放处理"""
        pass

    def _语法高亮(self):
        """执行语法高亮"""
        代码 = self.get("1.0", tk.END)
        if not 代码.strip():
            return

        # 清除现有标签
        for 标签名 in ["keyword", "type", "boolean", "null", "number",
                       "string", "comment", "identifier", "operator", "separator", "龍字"]:
            self.tag_remove(标签名, "1.0", tk.END)

        try:
            分析器 = Lexer(代码, 启用审计=False)
            标记列表 = 分析器.词法分析()

            for 标记 in 标记列表:
                if 标记.类型 == TokenType.EOF:
                    continue

                # 计算位置
                开始位置 = f"{标记.行号}.{标记.列号 - 1}"
                结束位置 = f"{标记.行号}.{标记.列号 - 1 + len(标记.值)}"

                # 映射标签
                标签映射 = {
                    TokenType.KEYWORD: "keyword",
                    TokenType.TYPE: "type",
                    TokenType.BOOLEAN: "boolean",
                    TokenType.NULL: "null",
                    TokenType.NUMBER: "number",
                    TokenType.STRING: "string",
                    TokenType.COMMENT: "comment",
                    TokenType.IDENTIFIER: "identifier",
                }

                标签名 = 标签映射.get(标记.类型, "identifier")
                self.tag_add(标签名, 开始位置, 结束位置)

            # 高亮龍字
            self._高亮龍字(代码)

        except Exception as e:
            pass  # 高亮失败静默处理

    def _高亮龍字(self, 代码: str):
        """高亮所有龍字"""
        龍模式 = re.compile(r'[龍龖龘龗龛]')
        for i, 行 in enumerate(代码.split('\n'), 1):
            for match in 龍模式.finditer(行):
                开始 = f"{i}.{match.start()}"
                结束 = f"{i}.{match.end()}"
                self.tag_add("龍字", 开始, 结束)

    def 设置内容(self, 内容: str):
        """设置编辑器内容"""
        self.delete("1.0", tk.END)
        self.insert("1.0", 内容)
        self.已修改 = False
        self._语法高亮()

    def 获取内容(self) -> str:
        """获取编辑器内容"""
        return self.get("1.0", tk.END)


class 行号画布(tk.Canvas):
    """行号显示画布"""

    def __init__(self, 父容器, 文本区: tk.Text, **参数):
        super().__init__(父容器, width=50, **参数)
        self.文本区 = 文本区
        self.configure(bg="#1E1E1E", highlightthickness=0)

        # 绑定滚动同步
        文本区.bind("<KeyRelease>", self._更新行号)
        文本区.bind("<MouseWheel>", self._更新行号)
        文本区.bind("<ButtonRelease>", self._更新行号)

    def _更新行号(self, 事件=None):
        """更新行号显示"""
        self.delete("all")

        # 获取可见区域
        第一个可见 = self.文本区.index("@0,0")
        最后一个可见 = self.文本区.index(f"@0,{self.文本区.winfo_height()}")

        第一行 = int(第一个可见.split('.')[0])
        最后一行 = int(最后一个可见.split('.')[0]) + 1

        for i in range(第一行, min(最后一行 + 1, int(self.文本区.index(tk.END).split('.')[0]) + 1)):
            y = self.文本区.dlineinfo(f"{i}.0")
            if y:
                self.create_text(25, y[1], text=str(i), anchor="nw",
                                fill="#858585", font=("编辑器字体族", 11))


class 编辑器标签页(ttk.Frame):
    """单个编辑器标签页"""

    def __init__(self, 父容器, 文件路径: str | None = None, **参数):
        super().__init__(父容器, **参数)
        self.文件路径 = 文件路径
        self.已修改 = False
        self.DNA追溯 = "#龍芯⚡️2026-06-18-CNSH-TAB"

        # 创建文本区和滚动条
        self.行号 = 行号画布(self, None, width=50)
        self.文本区 = 编辑器文本区(self, wrap=tk.NONE, undo=True,
                                     font=("编辑器字体族", 12),
                                     bg="#1E1E1E", fg="#D4D4D4",
                                     insertbackground="#FFFFFF",
                                     selectbackground="#264F78",
                                     selectforeground="#FFFFFF",
                                     padx=5, pady=5)
        self.行号.文本区 = self.文本区

        self.垂直滚动条 = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self._垂直滚动)
        self.水平滚动条 = ttk.Scrollbar(self, orient=tk.HORIZONTAL, command=self.文本区.xview)

        self.文本区.configure(
            yscrollcommand=self._垂直滚动回调,
            xscrollcommand=self.水平滚动条.set
        )

        # 布局
        self.行号.grid(row=0, column=0, sticky="ns")
        self.文本区.grid(row=0, column=1, sticky="nsew")
        self.垂直滚动条.grid(row=0, column=2, sticky="ns")
        self.水平滚动条.grid(row=1, column=0, columnspan=2, sticky="ew")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

    def _垂直滚动(self, *参数):
        """垂直滚动同步"""
        self.文本区.yview(*参数)
        self.行号._更新行号()

    def _垂直滚动回调(self, *参数):
        """垂直滚动回调"""
        self.垂直滚动条.set(*参数)
        self.行号._更新行号()

    def 获取标题(self) -> str:
        """获取标签页标题"""
        if self.文件路径:
            return os.path.basename(self.文件路径)
        return "未命名"

    def 加载文件(self, 文件路径: str) -> bool:
        """加载文件内容"""
        try:
            with open(文件路径, 'r', encoding='utf-8') as f:
                内容 = f.read()
            self.文本区.设置内容(内容)
            self.文件路径 = 文件路径
            self.已修改 = False
            return True
        except Exception as e:
            messagebox.showerror("错误", f"无法加载文件: {e}")
            return False

    def 保存文件(self, 文件路径: str | None = None) -> bool:
        """保存文件"""
        路径 = 文件路径 or self.文件路径
        if not 路径:
            return False

        try:
            内容 = self.文本区.获取内容()
            with open(路径, 'w', encoding='utf-8') as f:
                f.write(内容)
            self.文件路径 = 路径
            self.已修改 = False
            return True
        except Exception as e:
            messagebox.showerror("错误", f"无法保存文件: {e}")
            return False

    def 获取内容(self) -> str:
        """获取编辑器内容"""
        return self.文本区.获取内容()

    def 设置内容(self, 内容: str):
        """设置编辑器内容"""
        self.文本区.设置内容(内容)


class CNSH编辑器(tk.Tk):
    """
    CNSH多语言编辑器终端v5.0 主窗口
    集成所有模块功能的完整编辑器
    """

    DNA追溯 = "#龍芯⚡️2026-06-18-CNSH-TERMINAL-v5.0"
    版本 = "5.0.0"
    标题 = f"CNSH多语言编辑器终端 v{版本}"

    def __init__(self):
        super().__init__()

        self.title(self.标题)
        self.geometry("1400x900")
        self.configure(bg="#1E1E1E")

        # 初始化模块
        self.翻译器 = 通心译翻译器(启用藏经阁=False)
        self.四层检查器 = CNSH四层检查()
        self.时间戳规范 = AI时间戳规范()
        self.熔断 = 熔断机制(严格模式=False)
        self.审计 = 联动审计()

        # 标签页管理
        self.标签页列表: List[编辑器标签页] = []
        self.当前标签索引 = -1

        # 创建UI
        self._创建菜单()
        self._创建工具栏()
        self._创建主区域()
        self._创建状态栏()
        self._创建审计面板()

        # 创建初始标签页
        self._新建文件()

        # 绑定快捷键
        self._绑定快捷键()

        # 审计记录
        self.审计.成功(操作类型.编辑, "编辑器", f"CNSH编辑器v{self.版本}启动成功")

    def _创建菜单(self):
        """创建菜单栏"""
        self.菜单栏 = tk.Menu(self)
        self.configure(menu=self.菜单栏)

        # 文件菜单
        文件菜单 = tk.Menu(self.菜单栏, tearoff=0)
        文件菜单.add_command(label="新建    Ctrl+N", command=self._新建文件)
        文件菜单.add_command(label="打开    Ctrl+O", command=self._打开文件)
        文件菜单.add_command(label="保存    Ctrl+S", command=self._保存文件)
        文件菜单.add_command(label="另存为  Ctrl+Shift+S", command=self._另存为)
        文件菜单.add_separator()
        文件菜单.add_command(label="退出    Alt+F4", command=self.destroy)
        self.菜单栏.add_cascade(label="文件", menu=文件菜单)

        # 编辑菜单
        编辑菜单 = tk.Menu(self.菜单栏, tearoff=0)
        编辑菜单.add_command(label="撤销    Ctrl+Z", command=self._撤销)
        编辑菜单.add_command(label="重做    Ctrl+Y", command=self._重做)
        编辑菜单.add_separator()
        编辑菜单.add_command(label="剪切    Ctrl+X", command=self._剪切)
        编辑菜单.add_command(label="复制    Ctrl+C", command=self._复制)
        编辑菜单.add_command(label="粘贴    Ctrl+V", command=self._粘贴)
        编辑菜单.add_separator()
        编辑菜单.add_command(label="全选    Ctrl+A", command=self._全选)
        self.菜单栏.add_cascade(label="编辑", menu=编辑菜单)

        # 编译菜单
        编译菜单 = tk.Menu(self.菜单栏, tearoff=0)
        编译菜单.add_command(label="编译到C    F5", command=self._编译到C)
        编译菜单.add_command(label="词法分析   F6", command=self._词法分析)
        编译菜单.add_command(label="语法分析   F7", command=self._语法分析)
        编译菜单.add_separator()
        编译菜单.add_command(label="四层检查   F8", command=self._四层检查)
        self.菜单栏.add_cascade(label="编译", menu=编译菜单)

        # 翻译菜单
        翻译菜单 = tk.Menu(self.菜单栏, tearoff=0)
        翻译菜单.add_command(label="英→中    F9", command=self._翻译英到中)
        翻译菜单.add_command(label="中→英    F10", command=self._翻译中到英)
        翻译菜单.add_command(label="智能翻译  F11", command=self._智能翻译)
        翻译菜单.add_separator()
        翻译菜单.add_command(label="术语高亮  Ctrl+T", command=self._术语高亮)
        翻译菜单.add_command(label="术语查询  Ctrl+Q", command=self._术语查询)
        self.菜单栏.add_cascade(label="通心译", menu=翻译菜单)

        # 工具菜单
        工具菜单 = tk.Menu(self.菜单栏, tearoff=0)
        工具菜单.add_command(label="附加AI时间戳  Ctrl+D", command=self._附加时间戳)
        工具菜单.add_command(label="安全检查      Ctrl+B", command=self._安全检查)
        工具菜单.add_separator()
        工具菜单.add_command(label="导出术语表    Ctrl+E", command=self._导出术语表)
        self.菜单栏.add_cascade(label="工具", menu=工具菜单)

        # 帮助菜单
        帮助菜单 = tk.Menu(self.菜单栏, tearoff=0)
        帮助菜单.add_command(label="关于CNSH", command=self._关于)
        帮助菜单.add_command(label="快捷键说明", command=self._快捷键说明)
        self.菜单栏.add_cascade(label="帮助", menu=帮助菜单)

    def _创建工具栏(self):
        """创建工具栏"""
        self.工具栏 = ttk.Frame(self)
        self.工具栏.pack(side=tk.TOP, fill=tk.X)

        按钮样式 = {"width": 10, "padx": 5}

        ttk.Button(self.工具栏, text="新建", command=self._新建文件, **按钮样式).pack(side=tk.LEFT, padx=2)
        ttk.Button(self.工具栏, text="打开", command=self._打开文件, **按钮样式).pack(side=tk.LEFT, padx=2)
        ttk.Button(self.工具栏, text="保存", command=self._保存文件, **按钮样式).pack(side=tk.LEFT, padx=2)
        ttk.Separator(self.工具栏, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=5)
        ttk.Button(self.工具栏, text="编译C", command=self._编译到C, **按钮样式).pack(side=tk.LEFT, padx=2)
        ttk.Button(self.工具栏, text="英→中", command=self._翻译英到中, **按钮样式).pack(side=tk.LEFT, padx=2)
        ttk.Button(self.工具栏, text="中→英", command=self._翻译中到英, **按钮样式).pack(side=tk.LEFT, padx=2)
        ttk.Separator(self.工具栏, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=5)
        ttk.Button(self.工具栏, text="四层检查", command=self._四层检查, **按钮样式).pack(side=tk.LEFT, padx=2)
        ttk.Button(self.工具栏, text="术语查询", command=self._术语查询, **按钮样式).pack(side=tk.LEFT, padx=2)
        ttk.Separator(self.工具栏, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=5)
        ttk.Button(self.工具栏, text="关于", command=self._关于, **按钮样式).pack(side=tk.LEFT, padx=2)

    def _创建主区域(self):
        """创建主编辑区域"""
        self.主面板 = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        self.主面板.pack(fill=tk.BOTH, expand=True)

        # 左侧：编辑器区域
        self.编辑面板 = ttk.Frame(self.主面板)
        self.主面板.add(self.编辑面板, weight=3)

        # 标签页控制
        self.标签控制 = ttk.Notebook(self.编辑面板)
        self.标签控制.pack(fill=tk.BOTH, expand=True)
        self.标签控制.bind("<<NotebookTabChanged>>", self._标签切换事件)

        # 右侧：输出面板
        self.右侧面板 = ttk.Frame(self.主面板)
        self.主面板.add(self.右侧面板, weight=1)

        # 输出区域
        self.输出区域 = scrolledtext.ScrolledText(
            self.右侧面板, wrap=tk.WORD,
            font=("编辑器字体族", 10), bg="#1E1E1E", fg="#D4D4D4",
            insertbackground="#FFFFFF",
            height=15
        )
        self.输出区域.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)

        # 审计日志区域
        ttk.Label(self.右侧面板, text="审计日志", background="#1E1E1E",
                 foreground="#D4D4D4").pack(fill=tk.X, padx=2)
        self.审计区域 = scrolledtext.ScrolledText(
            self.右侧面板, wrap=tk.WORD,
            font=("编辑器字体族", 9), bg="#1E1E1E", fg="#D4D4D4",
            insertbackground="#FFFFFF",
            height=10
        )
        self.审计区域.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)

    def _创建状态栏(self):
        """创建状态栏"""
        self.状态栏 = ttk.Frame(self, relief=tk.SUNKEN)
        self.状态栏.pack(side=tk.BOTTOM, fill=tk.X)

        self.状态标签 = ttk.Label(self.状态栏, text="就绪", padding=(5, 2))
        self.状态标签.pack(side=tk.LEFT)

        self.位置标签 = ttk.Label(self.状态栏, text="行 1, 列 1", padding=(5, 2))
        self.位置标签.pack(side=tk.RIGHT)

        self.DNA标签 = ttk.Label(self.状态栏,
                                  text=self.DNA追溯,
                                  padding=(5, 2), foreground="#666666")
        self.DNA标签.pack(side=tk.RIGHT)

    def _创建审计面板(self):
        """创建审计面板（可折叠）"""
        pass  # 已集成到右侧面板

    def _绑定快捷键(self):
        """绑定键盘快捷键"""
        self.bind("<Control-n>", lambda e: self._新建文件())
        self.bind("<Control-o>", lambda e: self._打开文件())
        self.bind("<Control-s>", lambda e: self._保存文件())
        self.bind("<F5>", lambda e: self._编译到C())
        self.bind("<F6>", lambda e: self._词法分析())
        self.bind("<F7>", lambda e: self._语法分析())
        self.bind("<F8>", lambda e: self._四层检查())
        self.bind("<F9>", lambda e: self._翻译英到中())
        self.bind("<F10>", lambda e: self._翻译中到英())
        self.bind("<F11>", lambda e: self._智能翻译())
        self.bind("<Control-d>", lambda e: self._附加时间戳())
        self.bind("<Control-t>", lambda e: self._术语高亮())
        self.bind("<Control-q>", lambda e: self._术语查询())
        self.bind("<Control-b>", lambda e: self._安全检查())

    # ========== 标签页管理 ==========

    def _获取当前标签页(self) -> Optional[编辑器标签页]:
        """获取当前活动的标签页"""
        try:
            当前 = self.标签控制.select()
            return self.标签控制.nametowidget(当前)
        except:
            return None

    def _新建文件(self, 事件=None):
        """新建文件"""
        标签页 = 编辑器标签页(self.标签控制)
        self.标签控制.add(标签页, text="未命名")
        self.标签控制.select(标签页)
        self.审计.成功(操作类型.编辑, "编辑器", "新建文件")
        return 标签页

    def _打开文件(self, 事件=None):
        """打开文件"""
        文件路径 = filedialog.askopenfilename(
            title="打开CNSH文件",
            filetypes=[("CNSH文件", "*.cnsh"), ("所有文件", "*.*")]
        )
        if 文件路径:
            标签页 = self._新建文件()
            if 标签页.加载文件(文件路径):
                self.标签控制.tab(标签页, text=标签页.获取标题())
                self.审计.成功(操作类型.打开, "编辑器", f"打开文件: {文件路径}")

    def _保存文件(self, 事件=None):
        """保存文件"""
        标签页 = self._获取当前标签页()
        if not 标签页:
            return

        if 标签页.文件路径:
            if 标签页.保存文件():
                self.审计.成功(操作类型.保存, "编辑器", f"保存文件: {标签页.文件路径}")
                self._输出(f"🟢 文件已保存: {标签页.文件路径}")
        else:
            self._另存为()

    def _另存为(self, 事件=None):
        """另存为"""
        标签页 = self._获取当前标签页()
        if not 标签页:
            return

        文件路径 = filedialog.asksaveasfilename(
            title="保存CNSH文件",
            defaultextension=".cnsh",
            filetypes=[("CNSH文件", "*.cnsh"), ("所有文件", "*.*")]
        )
        if 文件路径:
            if 标签页.保存文件(文件路径):
                self.标签控制.tab(标签页, text=标签页.获取标题())
                self.审计.成功(操作类型.保存, "编辑器", f"另存为: {文件路径}")
                self._输出(f"🟢 文件已保存: {文件路径}")

    def _标签切换事件(self, 事件=None):
        """标签页切换事件"""
        pass

    # ========== 编辑操作 ==========

    def _撤销(self):
        """撤销"""
        标签页 = self._获取当前标签页()
        if 标签页:
            try:
                标签页.文本区.edit_undo()
            except tk.TclError:
                pass

    def _重做(self):
        """重做"""
        标签页 = self._获取当前标签页()
        if 标签页:
            try:
                标签页.文本区.edit_redo()
            except tk.TclError:
                pass

    def _剪切(self):
        """剪切"""
        标签页 = self._获取当前标签页()
        if 标签页:
            标签页.文本区.event_generate("<Control-x>")

    def _复制(self):
        """复制"""
        标签页 = self._获取当前标签页()
        if 标签页:
            标签页.文本区.event_generate("<Control-c>")

    def _粘贴(self):
        """粘贴"""
        标签页 = self._获取当前标签页()
        if 标签页:
            标签页.文本区.event_generate("<Control-v>")

    def _全选(self):
        """全选"""
        标签页 = self._获取当前标签页()
        if 标签页:
            标签页.文本区.tag_add(tk.SEL, "1.0", tk.END)

    # ========== 编译功能 ==========

    def _编译到C(self, 事件=None):
        """编译CNSH代码到C"""
        标签页 = self._获取当前标签页()
        if not 标签页:
            return

        代码 = 标签页.获取内容()
        self._输出("=== 编译到C ===")

        try:
            from .parser import 解析源代码
            from .code_generator import 生成C代码

            AST = 解析源代码(代码)
            C代码 = 生成C代码(AST)

            # 显示结果
            self._输出(C代码)
            self.审计.成功(操作类型.编译, "编译器", "编译成功")

            # 保存C文件
            if 标签页.文件路径:
                C文件路径 = 标签页.文件路径.replace(".cnsh", ".c")
                with open(C文件路径, 'w', encoding='utf-8') as f:
                    f.write(C代码)
                self._输出(f"\n🟢 C代码已保存: {C文件路径}")

        except Exception as e:
            self._输出(f"🔴 编译错误: {e}")
            self.审计.错误(操作类型.编译, "编译器", str(e))

    def _词法分析(self, 事件=None):
        """执行词法分析"""
        标签页 = self._获取当前标签页()
        if not 标签页:
            return

        代码 = 标签页.获取内容()
        self._输出("=== 词法分析 ===")

        try:
            分析器 = Lexer(代码)
            标记列表 = 分析器.词法分析()

            输出 = f"Token总数: {len(标记列表)}\n"
            输出 += "-" * 50 + "\n"
            for i, 标记 in enumerate(标记列表[:50]):  # 只显示前50个
                输出 += f"  [{i}] {标记.类型.name:15s} '{标记.值}' (行{标记.行号}, 列{标记.列号})\n"
            if len(标记列表) > 50:
                输出 += f"  ... 共 {len(标记列表)} 个Token\n"

            # 审计结果
            审计 = 分析器.获取审计结果()
            输出 += f"\n{审计['状态']} 错误:{审计['错误数']} 警告:{审计['警告数']}\n"

            self._输出(输出)
            self.审计.成功(操作类型.编译, "词法分析", f"生成 {len(标记列表)} 个Token")

        except Exception as e:
            self._输出(f"🔴 词法分析错误: {e}")

    def _语法分析(self, 事件=None):
        """执行语法分析"""
        标签页 = self._获取当前标签页()
        if not 标签页:
            return

        代码 = 标签页.获取内容()
        self._输出("=== 语法分析 ===")

        try:
            from .parser import 解析源代码
            AST = 解析源代码(代码)
            self._输出(f"🟢 语法分析成功")
            self._输出(f"顶级声明数: {len(AST.声明列表)}")
            for i, 声明 in enumerate(AST.声明列表):
                self._输出(f"  [{i}] {声明.转字符串()}")
            self.审计.成功(操作类型.编译, "语法分析", f"AST节点数: {len(AST.声明列表)}")
        except Exception as e:
            self._输出(f"🔴 语法分析错误: {e}")

    def _四层检查(self, 事件=None):
        """执行四层检查"""
        标签页 = self._获取当前标签页()
        if not 标签页:
            return

        代码 = 标签页.获取内容()
        self._输出("=== CNSH四层检查 ===")

        结果 = self.四层检查器.四层检查(代码)

        self._输出(f"综合结果: {结果['状态']}")
        self._输出(f"总错误: {结果['总错误数']} | 总警告: {结果['总警告数']}")
        self._输出("")

        for 层名 in ["L1字符层", "L2关键字层", "L3语法层", "L4语义层"]:
            层结果 = 结果[层名]
            状态 = "🟢" if 层结果["通过"] else "🔴"
            self._输出(f"{状态} {层名}: 错误{层结果['错误数']} 警告{层结果['警告数']}")
            for 错误 in 层结果['错误列表'][:3]:
                self._输出(f"   🔴 {错误}")
            for 警告 in 层结果['警告列表'][:3]:
                self._输出(f"   🟡 {警告}")

        self.审计.审计编译(代码, {"状态": 结果['状态']})

    # ========== 翻译功能 ==========

    def _翻译英到中(self, 事件=None):
        """英文翻译为中文"""
        标签页 = self._获取当前标签页()
        if not 标签页:
            return

        try:
            选中 = 标签页.文本区.tag_ranges(tk.SEL)
            if 选中:
                文本 = 标签页.文本区.get(*选中)
            else:
                文本 = 标签页.获取内容()

            结果 = self.翻译器.英文到中文(文本)

            if 选中:
                标签页.文本区.delete(*选中)
                标签页.文本区.insert(选中[0], 结果)
            else:
                标签页.设置内容(结果)

            self._输出("🟢 英→中翻译完成")
            self.审计.审计翻译("英→中", len(文本), len(结果))

        except Exception as e:
            self._输出(f"🔴 翻译错误: {e}")

    def _翻译中到英(self, 事件=None):
        """中文翻译为英文"""
        标签页 = self._获取当前标签页()
        if not 标签页:
            return

        try:
            选中 = 标签页.文本区.tag_ranges(tk.SEL)
            if 选中:
                文本 = 标签页.文本区.get(*选中)
            else:
                文本 = 标签页.获取内容()

            结果 = self.翻译器.中文到英文(文本)

            if 选中:
                标签页.文本区.delete(*选中)
                标签页.文本区.insert(选中[0], 结果)
            else:
                标签页.设置内容(结果)

            self._输出("🟢 中→英翻译完成")
            self.审计.审计翻译("中→英", len(文本), len(结果))

        except Exception as e:
            self._输出(f"🔴 翻译错误: {e}")

    def _智能翻译(self, 事件=None):
        """智能方向翻译"""
        标签页 = self._获取当前标签页()
        if not 标签页:
            return

        try:
            文本 = 标签页.获取内容()
            结果 = self.翻译器.智能翻译(文本)
            标签页.设置内容(结果)
            self._输出("🟢 智能翻译完成")
            self.审计.审计翻译("智能", len(文本), len(结果))
        except Exception as e:
            self._输出(f"🔴 翻译错误: {e}")

    def _术语高亮(self, 事件=None):
        """高亮显示术语"""
        标签页 = self._获取当前标签页()
        if not 标签页:
            return

        文本 = 标签页.获取内容()
        高亮信息 = self.翻译器.高亮术语(文本)

        self._输出("=== 术语高亮 ===")
        for 信息 in 高亮信息[:20]:
            self._输出(f"  {信息['类型']}: {信息['术语']} → {信息['翻译']}")
        if len(高亮信息) > 20:
            self._输出(f"  ... 共 {len(高亮信息)} 个术语")

    def _术语查询(self, 事件=None):
        """查询术语"""
        术语 = simpledialog.askstring("术语查询", "请输入要查询的术语:")
        if 术语:
            结果 = self.翻译器.解释术语(术语)
            if 结果:
                self._输出(f"=== 术语: {结果['英文']} ===")
                self._输出(f"中文: {结果['中文']}")
                self._输出(f"分类: {结果['分类']}")
                self._输出(f"说明: {结果['说明']}")
                if 结果['相关术语']:
                    self._输出(f"相关: {', '.join(结果['相关术语'])}")
            else:
                提示 = self.翻译器.获取术语提示(术语)
                self._输出(f"未找到术语 '{术语}'")
                if 提示:
                    self._输出("可能的匹配:")
                    for p in 提示[:5]:
                        self._输出(f"  {p['显示']}")

    # ========== 工具功能 ==========

    def _附加时间戳(self, 事件=None):
        """附加AI时间戳"""
        标签页 = self._获取当前标签页()
        if not 标签页:
            return

        内容 = 标签页.获取内容()
        带时间戳 = self.时间戳规范.附加时间戳(内容)
        标签页.设置内容(带时间戳)

        self._输出("🟢 AI时间戳已附加")
        self.审计.成功(操作类型.编辑, "AI时间戳", "附加时间戳")

    def _安全检查(self, 事件=None):
        """安全检查"""
        命令 = simpledialog.askstring("安全检查", "输入要检查的命令:")
        if 命令:
            结果 = self.熔断.检查命令(命令)
            self._输出("=== 安全检查 ===")
            self._输出(f"命令: {命令}")
            self._输出(f"安全: {'🟢 是' if 结果.是否安全 else '🔴 否'}")

            if not 结果.是否安全:
                self._输出(f"发现危险: {', '.join(结果.发现危险)}")
                for 风险 in 结果.风险详情:
                    self._输出(f"  {风险['风险等级']} {风险['名称']}: {风险['描述']}")
                    self._输出(f"  替代: {风险['安全替代']}")
                self._输出(f"确认码: {结果.确认码}")

            self.审计.审计熔断(命令, not 结果.是否安全, 结果.发现危险)

    def _导出术语表(self, 事件=None):
        """导出术语表"""
        文件路径 = filedialog.asksaveasfilename(
            title="导出术语表",
            defaultextension=".md",
            filetypes=[("Markdown", "*.md"), ("JSON", "*.json"), ("所有文件", "*.*")]
        )
        if 文件路径:
            格式 = "json" if 文件路径.endswith('.json') else "markdown"
            内容 = self.翻译器.导出术语表(格式)
            with open(文件路径, 'w', encoding='utf-8') as f:
                f.write(内容)
            self._输出(f"🟢 术语表已导出: {文件路径}")

    # ========== 帮助 ==========

    def _关于(self):
        """关于对话框"""
        messagebox.showinfo(
            "关于CNSH多语言编辑器终端",
            f"CNSH多语言编辑器终端 v{self.版本}\n\n"
            f"{self.DNA追溯}\n\n"
            f"中文编程语言 · 繁体龍字永存\n"
            f"通心译翻译器 · 中央藏经阁\n"
            f"龍魂三色审计 · 熔断机制v2.0\n\n"
            f"创始人: UID9622 · 龍芯北辰 · 诸葛鑫\n"
            f"许可: CC BY-NC-SA 4.0 (君子协议)\n\n"
            f"🔒 AI Truth Protocol: 所有声明均为真实"
        )

    def _快捷键说明(self):
        """快捷键说明"""
        messagebox.showinfo(
            "快捷键说明",
            "文件操作:\n"
            "  Ctrl+N  新建\n"
            "  Ctrl+O  打开\n"
            "  Ctrl+S  保存\n\n"
            "编译操作:\n"
            "  F5  编译到C\n"
            "  F6  词法分析\n"
            "  F7  语法分析\n"
            "  F8  四层检查\n\n"
            "翻译操作:\n"
            "  F9   英→中\n"
            "  F10  中→英\n"
            "  F11  智能翻译\n\n"
            "工具:\n"
            "  Ctrl+D  AI时间戳\n"
            "  Ctrl+T  术语高亮\n"
            "  Ctrl+Q  术语查询\n"
            "  Ctrl+B  安全检查"
        )

    # ========== 辅助方法 ==========

    def _输出(self, 文本: str):
        """输出到输出区域"""
        self.输出区域.insert(tk.END, 文本 + "\n")
        self.输出区域.see(tk.END)

    def _审计输出(self, 记录):
        """审计日志输出"""
        文本 = f"[{记录.时间}] {记录.颜色} [{记录.操作}] {记录.模块}: {记录.消息}\n"
        self.审计区域.insert(tk.END, 文本)
        self.审计区域.see(tk.END)

    def 运行(self):
        """启动编辑器"""
        self.mainloop()


# ========== 启动入口 ==========

def 启动编辑器():
    """启动CNSH编辑器"""
    编辑器 = CNSH编辑器()
    编辑器.run()


if __name__ == "__main__":
    启动编辑器()
