#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CNSH·如意 语法解析器 v1.0
DNA: #龍芯⚡️丙午·乙未·丁酉·亥时·☰乾-RUYI-PARSER-v1.0

解析老大的CNSH·如意指令，拆解为结构化任务分派。

支持语法:
  定义 任务 "名称"
  设 [属性] 为 [值]
  则 [AI角色] [动作] [并 [动作]]
  最后 转移 代码 至 华云道 [动作]

AI角色: CodeBuddy / Kimi / 华云道
动作关键词: 生成/优化/检测/转移/渲染/展示/检查/修复/搭建/创建

🐉 心意所指·万物皆成
"""

import json
import re
from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional, Tuple


# ─── 数据类型 ───────────────────────────────────────────

@dataclass
class RuyiTaskAction:
    """单个分派动作"""
    target_ai: str           # CodeBuddy / Kimi / 华云道
    action: str              # 生成/优化/检测/转移/渲染...
    target: str              # 目标描述 (前端页面/视觉风格/代码...)
    modifiers: List[str] = field(default_factory=list)  # 修饰描述

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class RuyiTask:
    """解析后的如意任务"""
    task_name: str = ""                               # 任务名称
    style: str = ""                                   # 风格设定
    tech_stack: List[str] = field(default_factory=list)  # 技术栈
    actions: List[RuyiTaskAction] = field(default_factory=list)  # 分派动作
    transfer_target: str = ""                         # 最终转移目标
    transfer_action: str = ""                         # 转移动作
    raw_command: str = ""                             # 原始指令
    status: str = "parsed"                            # parsed/routing/executing/done
    dna: str = ""                                     # 任务DNA追溯码
    meta: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["actions"] = [a.to_dict() if isinstance(a, RuyiTaskAction) else a for a in self.actions]
        return d


# ─── 解析器 ────────────────────────────────────────────

class RuyiParser:
    """CNSH·如意 指令解析器"""

    # 关键字定义
    KEY_DEFINE = "定义"
    KEY_TASK = "任务"
    KEY_SET = "设"
    KEY_IS = "为"
    KEY_THEN = "则"
    KEY_FINALLY = "最后"
    KEY_TRANSFER = "转移"
    KEY_TO = "至"
    KEY_AND = "并"

    # AI角色映射
    AI_ALIASES = {
        "codebuddy": "CodeBuddy",
        "kimi": "Kimi",
        "华云道": "华云道",
        "华为编辑器": "华云道",
        "织女": "华云道",
        "画师": "Kimi",
        "鲁班": "CodeBuddy",
    }

    # 动作关键词 → 标准化动作
    ACTION_MAP = {
        "生成": "generate",
        "创建": "generate",
        "写": "generate",
        "开发": "generate",
        "搭": "generate",
        "优化": "optimize",
        "美化": "optimize",
        "调整": "optimize",
        "检测": "check",
        "检查": "check",
        "审计": "check",
        "验证": "check",
        "转移": "transfer",
        "转换": "transfer",
        "迁移": "transfer",
        "渲染": "render",
        "展示": "render",
        "呈现": "render",
        "修复": "fix",
        "改": "fix",
        "搭建": "build",
        "构建": "build",
    }

    def __init__(self):
        pass

    def parse(self, raw_command: str) -> RuyiTask:
        """
        解析CNSH·如意指令，返回结构化任务。

        Args:
            raw_command: 用户输入的CNSH指令

        Returns:
            RuyiTask: 结构化任务对象

        Raises:
            ValueError: 指令格式错误
        """
        raw = raw_command.strip()
        task = RuyiTask(raw_command=raw)

        # 去除多余空白，保留结构
        lines = self._preprocess(raw)

        # 第一遍: 提取 定义/设/则/最后 结构块
        blocks = self._split_blocks(lines)

        # 第二遍: 逐块解析
        for block_type, block_text in blocks:
            if block_type == "define":
                task.task_name = self._parse_define(block_text)
            elif block_type == "set":
                key, value = self._parse_set(block_text)
                if key == "风格":
                    task.style = value
                elif key == "技术栈":
                    task.tech_stack = self._parse_tech_stack(value)
                else:
                    task.meta[key] = value
            elif block_type == "then":
                actions = self._parse_then(block_text)
                task.actions.extend(actions)
            elif block_type == "finally":
                task.transfer_target, task.transfer_action = self._parse_finally(block_text)

        # 校验: 至少要有任务名和一个动作
        if not task.task_name:
            raise ValueError("如意指令缺少任务名称。请用 '定义 任务 \"名称\"' 开头。")
        if not task.actions and not task.transfer_target:
            raise ValueError("如意指令缺少执行动作。请用 '则 [AI] [动作]' 指定任务。")

        return task

    def _preprocess(self, raw: str) -> List[str]:
        """预处理: 按分号或换行切分行，去空白"""
        # 先把中文分号换成换行
        raw = raw.replace("；", "\n").replace(";", "\n")
        lines = []
        for line in raw.split("\n"):
            line = line.strip()
            if line:
                lines.append(line)
        return lines

    def _split_blocks(self, lines: List[str]) -> List[Tuple[str, str]]:
        """按关键字切分为结构块"""
        blocks = []
        current_type = None
        current_text = ""

        for line in lines:
            if line.startswith(self.KEY_DEFINE + " ") or line.startswith(self.KEY_DEFINE + "　"):
                if current_type:
                    blocks.append((current_type, current_text.strip()))
                current_type = "define"
                current_text = line
            elif line.startswith(self.KEY_SET + " "):
                if current_type:
                    blocks.append((current_type, current_text.strip()))
                current_type = "set"
                current_text = line
            elif line.startswith(self.KEY_THEN + " "):
                if current_type:
                    blocks.append((current_type, current_text.strip()))
                current_type = "then"
                current_text = line
            elif line.startswith(self.KEY_FINALLY + " "):
                if current_type:
                    blocks.append((current_type, current_text.strip()))
                current_type = "finally"
                current_text = line
            else:
                # 续行
                if current_type:
                    current_text += " " + line

        if current_type:
            blocks.append((current_type, current_text.strip()))

        return blocks

    def _parse_define(self, text: str) -> str:
        """解析 定义 任务 "名称" """
        # 去掉前缀
        text = text[len(self.KEY_DEFINE):].strip()
        if text.startswith(self.KEY_TASK):
            text = text[len(self.KEY_TASK):].strip()
        # 提取引号内容
        name = self._extract_quoted(text)
        if name:
            return name
        # 无引号时取全部
        return text.strip()

    def _parse_set(self, text: str) -> Tuple[str, str]:
        """解析 设 风格 为 "简约商务风" """
        text = text[len(self.KEY_SET):].strip()
        # 按"为"分割
        if self.KEY_IS in text:
            parts = text.split(self.KEY_IS, 1)
            key = parts[0].strip()
            value = parts[1].strip()
        else:
            # 无"为"时按空格分割
            parts = text.split(None, 1)
            key = parts[0] if parts else ""
            value = parts[1] if len(parts) > 1 else ""
        # 提取引号内容
        value = self._extract_quoted(value) or value
        return key, value

    def _parse_tech_stack(self, value: str) -> List[str]:
        """解析技术栈列表"""
        # 支持 ["React", "TypeScript"] 或 React, TypeScript
        items = []
        # 尝试JSON数组
        try:
            arr = json.loads(value)
            if isinstance(arr, list):
                return arr
        except (json.JSONDecodeError, ValueError):
            pass
        # 逗号分割
        items = [s.strip().strip('"').strip("'") for s in value.split(",") if s.strip()]
        return items

    def _parse_then(self, text: str) -> List[RuyiTaskAction]:
        """解析 则 CodeBuddy 生成 前端页面 并 Kimi 优化 视觉风格"""
        text = text[len(self.KEY_THEN):].strip()
        actions = []
        # 按"并"分割多个动作
        segments = re.split(r'\s+并\s+', text)
        for segment in segments:
            action = self._parse_single_action(segment)
            if action:
                actions.append(action)
        return actions

    def _parse_single_action(self, text: str) -> Optional[RuyiTaskAction]:
        """解析单个动作: [AI角色] [动作] [目标]"""
        text = text.strip()
        if not text:
            return None

        target_ai = None
        action = None
        target = ""
        modifiers = []

        words = text.split()
        if not words:
            return None

        # 识别AI角色
        first_word_lower = words[0].lower()
        if first_word_lower in self.AI_ALIASES:
            target_ai = self.AI_ALIASES[first_word_lower]
            words = words[1:]
        else:
            # 尝试匹配双字别名
            if len(words) >= 1:
                for alias, name in self.AI_ALIASES.items():
                    if text.lower().startswith(alias.lower()):
                        target_ai = name
                        text_remain = text[len(alias):].strip()
                        words = text_remain.split()
                        break
            if not target_ai:
                target_ai = "CodeBuddy"  # 默认派给鲁班

        # 识别动作关键词
        remaining_words = []
        action_found = False
        for w in words:
            if not action_found and w in self.ACTION_MAP:
                action = self.ACTION_MAP[w]
                action_found = True
            else:
                remaining_words.append(w)

        # 没匹配到动作 → 取第一个动词
        if not action:
            for i, w in enumerate(remaining_words):
                if w in self.ACTION_MAP:
                    action = self.ACTION_MAP[w]
                    remaining_words = remaining_words[i+1:]
                    break

        # 剩余部分 = 目标描述 + 可能的修饰
        if remaining_words:
            # 查找可能的修饰分隔词 "并" "以及" "包括"
            modifier_words = ["并", "以及", "包括", "含", "附带"]
            target_parts = []
            mod_parts = []
            is_mod = False
            for w in remaining_words:
                if w in modifier_words:
                    is_mod = True
                    continue
                if is_mod:
                    mod_parts.append(w)
                else:
                    target_parts.append(w)
            target = " ".join(target_parts)
            modifiers = mod_parts

        return RuyiTaskAction(
            target_ai=target_ai,
            action=action or "generate",
            target=target or text,
            modifiers=modifiers,
        )

    def _parse_finally(self, text: str) -> Tuple[str, str]:
        """解析 最后 转移 代码 至 华云道 渲染"""
        text = text[len(self.KEY_FINALLY):].strip()
        target = "华云道"
        action = "render"

        # 提取动作
        for cn, en in self.ACTION_MAP.items():
            if cn in text:
                action = en
                break

        # 提取目标平台
        if self.KEY_TO in text:
            parts = text.split(self.KEY_TO, 1)
            target_text = parts[1].strip() if len(parts) > 1 else ""
            # 匹配已知AI
            target_word = target_text.split()[0] if target_text.split() else ""
            target_word_lower = target_word.lower()
            if target_word_lower in self.AI_ALIASES:
                target = self.AI_ALIASES[target_word_lower]

        return target, action

    def _extract_quoted(self, text: str) -> Optional[str]:
        """提取双引号或单引号内文本"""
        m = re.search(r'"([^"]*)"', text)
        if m:
            return m.group(1)
        m = re.search(r"'([^']*)'", text)
        if m:
            return m.group(1)
        m = re.search(r'「([^」]*)」', text)
        if m:
            return m.group(1)
        return None


# ─── 便捷函数 ──────────────────────────────────────────

def parse_ruyi_command(raw: str) -> RuyiTask:
    """一键解析CNSH·如意指令"""
    parser = RuyiParser()
    return parser.parse(raw)


# ─── 自测 ──────────────────────────────────────────────

if __name__ == "__main__":
    # 测试用例
    test_commands = [
        # 示例1: 标准格式
        '''定义 任务 "生成用户登录页"
设 风格 为 "简约商务风"
设 技术栈 为 ["React", "TypeScript"]
则 CodeBuddy 生成 前端页面
则 Kimi 优化 视觉风格 并 生成 配套图标
最后 转移 代码 至 华云道 渲染''',

        # 示例2: 精简格式
        '''定义 任务 "修复支付接口bug"
设 技术栈 为 Python, FastAPI, MySQL
则 CodeBuddy 修复 支付回调逻辑
则 CodeBuddy 检测 变量冲突''',

        # 示例3: 单行格式
        '''定义 任务 "构建数据看板"
则 CodeBuddy 搭建 后端API 并 Kimi 优化 可视化图表
最后 转移 至 华云道 展示''',

        # 示例4: 代码迁移
        '''定义 任务 "Python转JavaScript"
设 技术栈 为 Python, JavaScript
则 CodeBuddy 转移 Python脚本 至 JavaScript
则 CodeBuddy 检测 变量映射''',
    ]

    parser = RuyiParser()
    for i, cmd in enumerate(test_commands, 1):
        print(f"\n{'='*60}")
        print(f"测试 {i}:")
        print(f"{'='*60}")
        try:
            task = parser.parse(cmd)
            import json as _json
            print(_json.dumps(task.to_dict(), ensure_ascii=False, indent=2))
            print(f"\n✅ 解析成功 - 任务: {task.task_name}, {len(task.actions)}个动作")
        except ValueError as e:
            print(f"❌ 解析失败: {e}")

    print("\n✅ 全部自测完成")
