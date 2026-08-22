#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
🐉 CNSH 可视化执行器 v2.0
DNA: #龍芯⚡️丙午·乙未·甲辰·庚午·䷝离为火-CNSH-UI-v2.0
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0

功能：点按钮选择 .cnsh 文件 → 执行 → 显示输出 + 日志
结构：Tkinter UI + CNSH v2.0 解释器（变量/条件/AI接口/日志）
"""

import os
import sys
import re
import json
import ast
import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any, Callable
try:
    import tkinter as tk
    from tkinter import filedialog, messagebox, scrolledtext
    HAS_TKINTER = True
except ImportError:
    HAS_TKINTER = False
import threading

# ============================================================
# 一、CNSH v2.0 核心引擎
# ============================================================

class CNSHRuntime:
    """运行时 - 变量环境"""
    def __init__(self):
        self.vars: Dict[str, str] = {}
        self.logs: List[str] = []
        self.output_lines: List[str] = []
    
    def set(self, key: str, value: str) -> None:
        self.vars[key] = value
    
    def get(self, key: str) -> str:
        return self.vars.get(key, "")
    
    def get_all(self) -> Dict[str, str]:
        return self.vars.copy()
    
    def log(self, msg: str) -> None:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {msg}"
        self.logs.append(log_entry)
    
    def output(self, msg: str) -> None:
        self.output_lines.append(msg)


class CNSHAI:
    """AI接口 - 可替换为真实API"""
    _custom_ask: Optional[Callable[[str], str]] = None

    @classmethod
    def set_custom_ask(cls, callback: Optional[Callable[[str], str]]):
        """设置外部 AI 回调（例如 CNSH IDE 的多厂商路由）"""
        cls._custom_ask = callback

    @staticmethod
    def ask(prompt: str, use_real_ai: bool = False) -> str:
        if CNSHAI._custom_ask is not None:
            return CNSHAI._custom_ask(prompt)
        if use_real_ai:
            # TODO: 接入真实AI API
            return f"[AI真实理解] {prompt}"
        else:
            return f"[AI理解] {prompt}"


class CNSHParserV2:
    """CNSH v2.0 解析器 - 支持变量/条件/AI/嵌套"""
    
    @staticmethod
    def parse(content: str) -> List:
        lines = content.strip().split('\n')
        instructions = []
        i = 0
        
        while i < len(lines):
            line = lines[i].strip()
            
            if not line or line.startswith('#'):
                i += 1
                continue
            
            # 设 变量 = 值
            if line.startswith('设'):
                parts = line.replace('设', '').strip().split('=', 1)
                if len(parts) == 2:
                    key = parts[0].strip()
                    value = parts[1].strip()
                    if value.startswith('"') and value.endswith('"'):
                        value = value[1:-1]
                    instructions.append(('set', key, value))
                else:
                    match = re.match(r'设\s+(\S+)\s*=\s*(.+)', line)
                    if match:
                        key = match.group(1).strip()
                        value = match.group(2).strip()
                        if value.startswith('"') and value.endswith('"'):
                            value = value[1:-1]
                        instructions.append(('set', key, value))
            
            # 打印 内容
            elif line.startswith('打印'):
                value = line.replace('打印', '').strip()
                if value.startswith('"') and value.endswith('"'):
                    value = value[1:-1]
                instructions.append(('print', value))
            
            # 如果 条件
            elif line.startswith('如果'):
                condition = line.replace('如果', '').strip()
                # 收集条件块
                block_lines = []
                i += 1
                while i < len(lines):
                    block_line = lines[i].strip()
                    if block_line.startswith('结束'):
                        break
                    block_lines.append(lines[i])
                    i += 1
                block_content = '\n'.join(block_lines)
                instructions.append(('if', condition, CNSHParserV2.parse(block_content)))
            
            # 理解 "内容"
            elif line.startswith('理解'):
                match = re.search(r'"(.*?)"', line)
                if match:
                    instructions.append(('ai', match.group(1)))
                else:
                    value = line.replace('理解', '').strip()
                    instructions.append(('ai', value))
            
            # 记录 内容
            elif line.startswith('记录'):
                value = line.replace('记录', '').strip()
                if value.startswith('"') and value.endswith('"'):
                    value = value[1:-1]
                instructions.append(('log', value))
            
            # @任务 标记
            elif line.startswith('@任务'):
                instructions.append(('task', line))
            
            # 执行 命令
            elif line.startswith('执行'):
                value = line.replace('执行', '').strip()
                instructions.append(('exec', value))
            
            i += 1
        
        return instructions


class CNSHExecutorV2:
    """CNSH v2.0 执行器"""
    
    @staticmethod
    def _safe_eval(expr: str) -> Any:
        """安全表达式求值：仅允许数字字面量与基础运算符。"""
        if not expr or not expr.strip():
            return True
        tree = ast.parse(expr.strip(), mode='eval')
        allowed_nodes = (ast.Expression, ast.BinOp, ast.UnaryOp, ast.Constant,
                         ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Mod, ast.Pow,
                         ast.FloorDiv, ast.USub, ast.UAdd)
        for node in ast.walk(tree):
            if not isinstance(node, allowed_nodes):
                return None
        return eval(compile(tree, '<safe>', 'eval'))

    @staticmethod
    def eval_condition(cond: str, runtime: CNSHRuntime) -> bool:
        try:
            # 替换变量
            for k, v in runtime.get_all().items():
                cond = cond.replace(k, str(v))
            # 安全评估：先把剩余标识符替换为 0，再走安全求值
            if re.search(r'[a-zA-Z_]', cond):
                cond = re.sub(r'[a-zA-Z_][a-zA-Z0-9_]*', '0', cond)
            result = CNSHExecutorV2._safe_eval(cond)
            return bool(result) if result is not None else False
        except Exception:
            return False
    
    @staticmethod
    def execute(instructions: List, runtime: CNSHRuntime, 
                use_real_ai: bool = False, depth: int = 0) -> None:
        
        for inst in instructions:
            cmd = inst[0]
            
            if cmd == 'set':
                _, key, value = inst
                runtime.set(key, value)
                runtime.log(f"变量设置: {key} = {value}")
            
            elif cmd == 'print':
                value = inst[1]
                if value in runtime.get_all():
                    value = runtime.get(value)
                output = f"[输出] {value}"
                runtime.output(output)
                print(output)
            
            elif cmd == 'if':
                _, condition, block = inst
                if CNSHExecutorV2.eval_condition(condition, runtime):
                    CNSHExecutorV2.execute(block, runtime, use_real_ai, depth + 1)
                runtime.log(f"条件判断: {condition} -> {'通过' if CNSHExecutorV2.eval_condition(condition, runtime) else '跳过'}")
            
            elif cmd == 'ai':
                prompt = inst[1]
                result = CNSHAI.ask(prompt, use_real_ai)
                runtime.set('AI结果', result)
                runtime.output(result)
                print(result)
                runtime.log(f"AI理解: {prompt} -> {result[:50]}...")
            
            elif cmd == 'log':
                value = inst[1]
                if value in runtime.get_all():
                    value = runtime.get(value)
                runtime.log(value)
            
            elif cmd == 'task':
                runtime.log(f"任务标记: {inst[1]}")
            
            elif cmd == 'exec':
                runtime.log(f"执行命令: {inst[1]}")
                runtime.output(f"[执行] {inst[1]}")


class CNSHInterpreterV2:
    """CNSH v2.0 主解释器"""
    
    @staticmethod
    def run_script(content: str, use_real_ai: bool = False) -> Tuple[str, List[str]]:
        runtime = CNSHRuntime()
        instructions = CNSHParserV2.parse(content)
        
        if not instructions:
            return "[提示] 无有效指令", []
        
        CNSHExecutorV2.execute(instructions, runtime, use_real_ai)
        
        output = '\n'.join(runtime.output_lines)
        logs = runtime.logs
        
        return output, logs
    
    @staticmethod
    def run_file(file_path: str, use_real_ai: bool = False) -> Tuple[str, List[str]]:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return CNSHInterpreterV2.run_script(content, use_real_ai)
        except FileNotFoundError:
            return f"[错误] 文件不存在: {file_path}", []
        except Exception as e:
            return f"[错误] {e}", []


# ============================================================
# 二、可视化界面 (Tkinter)
# ============================================================

class CNSHApp:
    def __init__(self, root):
        if not HAS_TKINTER:
            raise RuntimeError("Tkinter 不可用，无法启动 CNSH 桌面控制台。请使用 CNSH Web IDE 或安装 Tkinter。")
        self.root = root
        self.root.title("🐉 CNSH 控制台 v2.0")
        self.root.geometry("700x500")
        self.root.minsize(600, 400)
        
        self.file_path = None
        self.use_real_ai = False
        
        # ---------- 顶部 ----------
        top_frame = tk.Frame(root)
        top_frame.pack(pady=10, fill='x', padx=20)
        
        tk.Label(top_frame, text="🐉 CNSH 执行器", font=("Arial", 18, "bold")).pack(side='left')
        
        # AI切换
        self.ai_var = tk.BooleanVar(value=False)
        ai_check = tk.Checkbutton(top_frame, text="启用真实AI", 
                                   variable=self.ai_var, command=self._toggle_ai)
        ai_check.pack(side='right')
        
        # ---------- 文件选择 ----------
        file_frame = tk.Frame(root)
        file_frame.pack(pady=5, fill='x', padx=20)
        
        self.file_label = tk.Label(file_frame, text="📄 未选择文件", 
                                    font=("Arial", 10), anchor='w', width=50)
        self.file_label.pack(side='left')
        
        tk.Button(file_frame, text="选择文件", command=self.select_file).pack(side='right', padx=5)
        tk.Button(file_frame, text="📂 示例", command=self.load_demo).pack(side='right', padx=5)
        
        # ---------- 运行按钮 ----------
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=5)
        
        self.run_btn = tk.Button(btn_frame, text="▶ 运行", font=("Arial", 12, "bold"),
                                  bg="#4CAF50", fg="white", padx=20, pady=5,
                                  command=self.run)
        self.run_btn.pack(side='left', padx=10)
        
        self.clear_btn = tk.Button(btn_frame, text="🗑 清空", 
                                    command=self.clear_output)
        self.clear_btn.pack(side='left', padx=10)
        
        # ---------- 输出区 ----------
        output_frame = tk.Frame(root)
        output_frame.pack(pady=5, padx=20, fill='both', expand=True)
        
        tk.Label(output_frame, text="📋 输出:", font=("Arial", 10, "bold"), anchor='w').pack(fill='x')
        
        self.output_text = scrolledtext.ScrolledText(
            output_frame, height=15, font=("Courier New", 10),
            wrap=tk.WORD, bg="#1e1e1e", fg="#d4d4d4"
        )
        self.output_text.pack(fill='both', expand=True)
        
        # ---------- 日志区 ----------
        log_frame = tk.Frame(root)
        log_frame.pack(pady=5, padx=20, fill='x')
        
        tk.Label(log_frame, text="📜 日志:", font=("Arial", 10, "bold"), anchor='w').pack(fill='x')
        
        self.log_text = scrolledtext.ScrolledText(
            log_frame, height=4, font=("Courier New", 8),
            wrap=tk.WORD, bg="#2d2d2d", fg="#808080"
        )
        self.log_text.pack(fill='x')
        
        # ---------- 状态栏 ----------
        self.status_label = tk.Label(root, text="就绪", font=("Arial", 8), anchor='w')
        self.status_label.pack(fill='x', padx=10, pady=2)
    
    def _toggle_ai(self):
        self.use_real_ai = self.ai_var.get()
        self.status_label.config(text=f"AI模式: {'真实' if self.use_real_ai else '模拟'}")
    
    def select_file(self):
        path = filedialog.askopenfilename(
            initialdir=os.path.expanduser("~/longhun-system"),
            filetypes=[("CNSH 文件", "*.cnsh"), ("所有文件", "*.*")]
        )
        if path:
            self.file_path = path
            self.file_label.config(text=f"📄 {os.path.basename(path)}")
            self.status_label.config(text=f"已选择: {path}")
    
    def load_demo(self):
        demo_content = '''@任务 开始

设 名字 = "龍魂"
打印 名字

设 时间 = 12

如果 时间 > 10
    打印 "晚上逻辑触发"
结束

理解 "把这句话换一种说法"
记录 AI结果

打印 AI结果

@任务 结束'''
        
        # 写入 demo 文件
        demo_path = os.path.join(os.path.expanduser("~/longhun-system"), "demo_v2.cnsh")
        os.makedirs(os.path.dirname(demo_path), exist_ok=True)
        with open(demo_path, 'w', encoding='utf-8') as f:
            f.write(demo_content)
        
        self.file_path = demo_path
        self.file_label.config(text="📄 demo_v2.cnsh")
        self.status_label.config(text="已加载示例脚本")
    
    def run(self):
        if not self.file_path:
            messagebox.showerror("错误", "请先选择 .cnsh 文件")
            return
        
        self.run_btn.config(state='disabled', text='▶ 运行中...')
        self.output_text.delete(1.0, tk.END)
        self.log_text.delete(1.0, tk.END)
        
        def run_in_thread():
            try:
                output, logs = CNSHInterpreterV2.run_file(self.file_path, self.use_real_ai)
                
                # 更新输出
                self.output_text.insert(tk.END, output)
                # 更新日志
                for log in logs:
                    self.log_text.insert(tk.END, log + '\n')
                self.log_text.see(tk.END)
                
                self.status_label.config(text=f"✅ 执行完成: {len(logs)} 条日志")
            except Exception as e:
                self.output_text.insert(tk.END, f"[错误] {e}\n")
                self.status_label.config(text=f"❌ 执行失败")
            finally:
                self.run_btn.config(state='normal', text='▶ 运行')
        
        threading.Thread(target=run_in_thread, daemon=True).start()
    
    def clear_output(self):
        self.output_text.delete(1.0, tk.END)
        self.log_text.delete(1.0, tk.END)
        self.status_label.config(text="已清空")


# ============================================================
# 三、启动入口
# ============================================================

def main():
    root = tk.Tk()
    app = CNSHApp(root)
    
    # 默认加载demo
    demo_path = os.path.join(os.path.expanduser("~/longhun-system"), "demo_v2.cnsh")
    if os.path.exists(demo_path):
        app.file_path = demo_path
        app.file_label.config(text="📄 demo_v2.cnsh")
    
    root.mainloop()


if __name__ == "__main__":
    main()
