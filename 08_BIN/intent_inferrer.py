# DNA: #龍芯⚡️丙午·丙申·甲子·癸酉·䷪夬-CODE-补DNA-ff35d533
#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# -*- coding: utf-8 -*-
"""
🐉 意图推断模块
基于上下文推导用户的真实意图，映射到标准动作

DNA: #龍芯⚡️丙午·丙申·壬戌·甲辰·䷤家人-INTENT-INFER-UID9622
"""

import re
from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class InferredIntent:
    """推断出的意图"""

    action: str
    target: str
    parameters: Dict
    confidence: float
    reasoning: str


class IntentInferrer:
    """意图推断器"""

    ACTION_KEYWORDS = {
        "fix": ["修复", "改正", "修正", "解决", "处理", "改", "修", "bug", "故障", "报错"],
        "execute": ["执行", "运行", "启动", "开始", "做", "实施", "跑", "调用"],
        "query": ["查询", "查看", "搜索", "找出", "告诉我", "获取", "查一下", "看看", "状态"],
        "archive": ["归档", "保存", "记录", "存", "备份", "存档"],
        "config": ["配置", "设置", "调整", "修改", "更新", "改一下"],
        "deploy": ["部署", "上线", "发布", "安装"],
        "test": ["测试", "验证", "检查", "审计", "跑一下"],
        "rollback": ["回滚", "撤销", "恢复", "还原"],
        "stop": ["停止", "终止", "关闭", "杀掉"],
    }

    TARGET_KEYWORDS = {
        "登录": "登录服务",
        "搜索": "搜索服务",
        "数据库": "数据库",
        "配置": "配置",
        "备份": "备份",
        "训练": "训练任务",
        "模型": "模型",
        "服务": "服务",
        "索引": "索引",
        "剪贴板": "剪贴板容器",
        "前端": "前端服务",
        "后端": "后端服务",
        "API": "API服务",
    }

    @classmethod
    def infer(cls, input_text: str, context: Dict) -> InferredIntent:
        """基于输入和上下文推断意图"""
        # 1. 提取动作
        action = "unknown"
        matched_keywords = []
        for act, keywords in cls.ACTION_KEYWORDS.items():
            for kw in keywords:
                if kw in input_text:
                    action = act
                    matched_keywords.append(kw)
                    break
            if action != "unknown":
                break

        # 2. 提取目标
        target = ""
        for kw, t in cls.TARGET_KEYWORDS.items():
            if kw in input_text:
                target = t
                break

        # 3. 从上下文补全目标
        likely_task = context.get("likely_task")
        if not target and likely_task:
            target = likely_task.get("target", "")

        # 4. 参数
        parameters = {}
        if context.get("state"):
            parameters["current_state"] = context["state"]
        # 简单提取“数字/文件名”等作为参数
        numbers = re.findall(r"\d+", input_text)
        if numbers:
            parameters["numbers"] = numbers
        files = re.findall(r"[\w\-/]+\.(?:py|md|json|sh|yaml|yml)", input_text)
        if files:
            parameters["files"] = files

        # 5. 置信度
        confidence = 0.5
        if action != "unknown" and target:
            confidence = 0.85
        elif action != "unknown":
            confidence = 0.65
        elif likely_task:
            confidence = 0.55
            action = likely_task.get("intent", "unknown")
            target = likely_task.get("target", "")

        reasoning = (
            f"关键词匹配动作 '{action}'（命中 {matched_keywords}），"
            f"目标 '{target}'，上下文置信度 {confidence:.2f}。"
        )

        return InferredIntent(
            action=action,
            target=target,
            parameters=parameters,
            confidence=confidence,
            reasoning=reasoning,
        )

    @classmethod
    def enhance_with_history(cls, intent: InferredIntent, history: List[Dict]) -> InferredIntent:
        """利用历史记录增强意图"""
        if intent.confidence >= 0.8:
            return intent
        for record in reversed(history):
            if record.get("intent") and record.get("intent") != "unknown":
                if not intent.target:
                    intent.target = record.get("target", intent.target)
                intent.parameters.update(record.get("parameters", {}))
                intent.confidence = min(0.85, intent.confidence + 0.15)
                intent.reasoning += " (历史增强)"
                break
        return intent


# 测试
if __name__ == "__main__":
    context = {
        "state": {"last_action": "部署失败"},
        "likely_task": {"target": "登录服务", "intent": "fix"},
    }
    result = IntentInferrer.infer("修复登录问题", context)
    print(f"意图: {result.action}, 目标: {result.target}, 置信度: {result.confidence}")
    print(f"推理: {result.reasoning}")
