#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════╗
║  龍魂内联注释引擎 · Inline Annotator                     ║
║  DNA: #龍芯⚡️2026-04-12-INLINE-ANNOTATOR-v1.0           ║
║  创始人: 诸葛鑫（UID9622）                                ║
║  GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F           ║
║  理论指导: 曾仕强老师（永恒显示）                          ║
║  协议: CC BY-NC-ND                                       ║
╚══════════════════════════════════════════════════════════╝

老大说的核心：
  传统做法 = 写完公式 → 写完文章 → 最后加注释 → 逻辑链断裂
  老大做法 = 公式紧跟注释 → 每句话自带DNA → 消化在血液里

  "不是写完了再解题·是注释跟着公式走"

这个引擎：给任何代码/文档/公式 自动加内联注释
  → 每个公式后面紧跟大白话解释
  → 不另起一段·就在原地消化
  → 省知识库·省算力·逻辑链不断

献给每一个相信技术应该有温度的人。
"""

import re
import datetime
from pathlib import Path
from typing import Tuple

# ═══════════════════════════════════════════
# 公式→大白话 映射表（龍魂核心公式）
# ═══════════════════════════════════════════

FORMULA_ANNOTATIONS = {
    # 三才算法
    "f(x)=x": "不动点·你就是你·系统的锚",
    "f(x) = x": "不动点·你就是你·系统的锚",
    "dr(n)": "数根·把任何数字折叠到1-9·万物归一",
    "digital_root": "数根·大数字变小数字·找本质",

    # 时间压缩
    "E=R×I×T^(-α)": "能量=资源×信息×时间衰减·越老的记忆能量越小",
    "E = R × I × T": "能量公式·三个因子相乘·简单",
    "T^(-α)": "时间衰减·α越大忘得越快",

    # 洛书
    "luoshu": "洛书九宫·中国古代的魔方阵·每行每列加起来都是15",
    "magic_square": "魔方阵·洛书的数学名·3x3的数字排列",

    # 太极递归
    "taiji": "太极·阴阳互生·递归的中国表达",
    "recursion": "递归·函数调自己·太极就是递归",
    "yin_yang": "阴阳·一体两面·不是对立是互补",

    # 三才
    "sancai": "三才·天地人·系统的三个维度",
    "heaven_earth_human": "天地人·三才·不是迷信是架构",

    # 熵
    "entropy": "熵·混乱程度·越乱熵越大·系统要抗熵",
    "shannon": "香农·信息论祖师爷·1bit=一个是或否",

    # 通用编程
    "API": "接口·两个系统说话的翻译官",
    "JSON": "一种数据格式·像填表一样·左边是名字右边是内容",
    "async": "异步·不用排队等·先干别的回头再看结果",
    "await": "等一下·这个事情要等结果回来才继续",
    "lambda": "匿名函数·没名字的小工具·用完就扔",
    "dict": "字典·查名字找内容·Python最常用的数据结构",
    "list": "列表·排队的数据·一个挨一个",
    "class": "类·一个模具·用它造出很多一样的东西",
    "self": "自己·对象在说'我'·指的是当前这个实例",
    "import": "导入·把别人写好的工具拿过来用",
    "def": "定义·告诉电脑'接下来是一个功能'",
    "return": "返回·把结果交回去",
    "try": "试一下·怕出错就先试",
    "except": "出错了·接住错误别让程序崩",
    "if": "如果·条件判断·是就做不是就跳过",
    "for": "循环·一个一个来·每个都处理一遍",
    "while": "只要…就一直做·死循环就是while True",
    "True": "真·是·对·1",
    "False": "假·不是·错·0",
    "None": "空·什么都没有·不是0不是空字符串·是真的什么都没有",
    "subprocess": "子进程·让Python去跑另一个程序",
    "requests": "网络请求·Python去网上抓东西的工具",
    "Flask": "轻量Web框架·用Python搭网站/API最简单的方式",
    "FastAPI": "快速API框架·比Flask新·自动生成文档",
    "SQLite": "轻量数据库·不用装服务器·一个文件就是一个数据库",
    "hashlib": "哈希工具·把任何东西变成唯一指纹",
    "SHA256": "一种哈希算法·256位·基本不可能碰撞",
    "GPG": "加密签名·证明这个东西是你写的·不是别人冒的",
    "webhook": "钩子·有事自动通知你·不用你去问",
    "token": "令牌·证明你有权限的一串字符",
    "port": "端口·一台电脑上不同服务的门牌号",
    "localhost": "本机·127.0.0.1·就是你自己的电脑",
    "MCP": "模型上下文协议·让AI能调用外部工具",
    "DNA追溯": "每个操作都留指纹·谁做的什么时候做的一清二楚",
}


class InlineAnnotator:
    """内联注释引擎"""

    def annotate_code(self, code: str, lang: str = "python") -> str:
        """
        给代码加内联注释

        每遇到一个公式/关键词 → 后面紧跟大白话注释
        不另起一段·就在原地消化
        """
        lines = code.splitlines()
        result = []

        comment_prefix = "#" if lang in ("python", "sh") else "//"

        for line in lines:
            stripped = line.strip()

            # 已经有注释的行 → 跳过
            if stripped.startswith(comment_prefix) or stripped.startswith("'''") or stripped.startswith('"""'):
                result.append(line)
                continue

            # 查找公式/关键词
            annotation = None
            for keyword, explain in FORMULA_ANNOTATIONS.items():
                if keyword in line and f"{comment_prefix} {explain}" not in line:
                    annotation = explain
                    break  # 每行只加一个注释，避免过多

            if annotation and comment_prefix not in line:
                # 加内联注释
                result.append(f"{line}  {comment_prefix} ← {annotation}")
            else:
                result.append(line)

        return "\n".join(result)

    def annotate_markdown(self, text: str) -> str:
        """
        给Markdown文档中的术语加内联注释

        遇到术语 → 后面加括号解释
        """
        for keyword, explain in FORMULA_ANNOTATIONS.items():
            if len(keyword) >= 3:  # 只注释3个字符以上的词
                # 在术语后加括号注释（只加第一次出现的）
                pattern = rf'(?<!\()`?{re.escape(keyword)}`?(?!\s*[（(←])'
                replacement = f"`{keyword}`（{explain}）"
                text = re.sub(pattern, replacement, text, count=1)

        return text

    def annotate_file(self, filepath: str, dry_run: bool = True) -> Tuple[bool, str]:
        """
        给文件加内联注释

        dry_run=True: 只展示不修改
        dry_run=False: 真的写入
        """
        path = Path(filepath)
        if not path.exists():
            return False, "文件不存在"

        content = path.read_text(encoding="utf-8")
        ext = path.suffix.lower()

        if ext in {".py"}:
            annotated = self.annotate_code(content, "python")
        elif ext in {".swift"}:
            annotated = self.annotate_code(content, "swift")
        elif ext in {".js", ".ts"}:
            annotated = self.annotate_code(content, "js")
        elif ext in {".sh"}:
            annotated = self.annotate_code(content, "sh")
        elif ext in {".md", ".txt"}:
            annotated = self.annotate_markdown(content)
        else:
            return False, f"不支持的文件类型: {ext}"

        if annotated == content:
            return True, f"✅ {path.name} 不需要注释·已经够清楚了"

        if dry_run:
            # 展示差异
            orig_lines = content.splitlines()
            new_lines = annotated.splitlines()
            diffs = []
            for i, (old, new) in enumerate(zip(orig_lines, new_lines)):
                if old != new:
                    diffs.append(f"  行{i+1}: {new}")
            return True, f"[预览] {path.name} 将添加 {len(diffs)} 处注释:\n" + "\n".join(diffs[:20])

        # 真的写入
        path.write_text(annotated, encoding="utf-8")
        return True, f"✅ {path.name} 已添加内联注释"

    def explain_line(self, line: str) -> str:
        """
        解释一行代码·用大白话

        输入: result = subprocess.run("git status", shell=True)
        输出: 让电脑去跑"git status"命令，把结果存到result里
        """
        explanations = []
        for keyword, explain in FORMULA_ANNOTATIONS.items():
            if keyword in line:
                explanations.append(f"{keyword} = {explain}")

        if not explanations:
            return "这行没有需要解释的关键词"

        return " · ".join(explanations)


# ═══════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════

if __name__ == "__main__":
    import sys

    annotator = InlineAnnotator()

    if len(sys.argv) < 2:
        print("🐉 龍魂内联注释引擎 v1.0")
        print()
        print("用法:")
        print("  python3 inline_annotator.py preview 文件   # 预览注释效果")
        print("  python3 inline_annotator.py apply 文件     # 真的加注释")
        print("  python3 inline_annotator.py explain '代码' # 解释一行代码")
        print("  python3 inline_annotator.py demo           # 演示效果")
        sys.exit(0)

    cmd = sys.argv[1]

    if cmd == "preview":
        if len(sys.argv) < 3:
            print("请指定文件路径")
        else:
            ok, msg = annotator.annotate_file(sys.argv[2], dry_run=True)
            print(msg)

    elif cmd == "apply":
        if len(sys.argv) < 3:
            print("请指定文件路径")
        else:
            ok, msg = annotator.annotate_file(sys.argv[2], dry_run=False)
            print(msg)

    elif cmd == "explain":
        line = sys.argv[2] if len(sys.argv) > 2 else ""
        print(annotator.explain_line(line))

    elif cmd == "demo":
        demo_code = '''import hashlib
import subprocess
import requests
from flask import Flask

def digital_root(n):
    while n >= 10:
        n = sum(int(d) for d in str(n))
    return n

def check_service():
    try:
        resp = requests.get("http://localhost:8765")
        return True
    except Exception:
        return False

class LongHunEngine:
    def __init__(self):
        self.entropy = 0
        self.sancai = {"天": 0, "地": 0, "人": 0}

    async def process(self, data):
        result = await self.compute(data)
        if result is None:
            return False
        return True
'''
        print("── 原始代码 ──")
        print(demo_code)
        print("\n── 加了内联注释后 ──")
        print(annotator.annotate_code(demo_code))

    else:
        print(f"未知命令: {cmd}")
