#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂统一AI网关 v1.0
LongHun AI Gateway — 多模型统一入口，按任务类型智能路由

DNA: #龍芯⚡️丙午·乙未·壬辰·午时·需-AI-GATEWAY-v1.0
📇 项目身份 · 联系 · 支持 → assets/PUBLIC_IDENTITY.md

设计原则:
  - 一个入口，多种模型（Claude / DeepSeek / Kimi / ChatGPT）
  - 只用免费版 API / 自有配额，不付费
  - 按任务类型智能路由（写代码→Claude, 翻译→DeepSeek, 中文→Kimi）
  - 密钥统一从 lh_secrets_loader 加载，不硬编码
  - 所有请求带 DNA 追溯码

路由规则:
  | 任务类型 | 首选模型 | 降级模型 |
  |----------|----------|----------|
  | 代码生成 | Claude   | DeepSeek |
  | 中文对话 | Kimi     | DeepSeek |
  | 翻译     | DeepSeek | Kimi     |
  | 摘要/分析 | Claude  | Kimi     |
  | 创意写作 | Claude   | DeepSeek |
  | 数学推理 | DeepSeek | Claude   |
"""

import json
import os
import sys
import time
import hashlib
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Any
from enum import Enum

import httpx

# ═══════════════════════════════════════════════════════
# 初始化
# ═══════════════════════════════════════════════════════

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from bin.lh_secrets_loader import get_credential

LOG_DIR = Path.home() / "longhun-system" / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / "ai_gateway.log"),
        logging.StreamHandler(sys.stderr)
    ]
)
logger = logging.getLogger("lh_ai_gateway")


# ═══════════════════════════════════════════════════════
# 任务类型
# ═══════════════════════════════════════════════════════

class TaskType(Enum):
    CODE = "code"           # 代码生成/修复
    CHINESE_CHAT = "cn"     # 中文对话
    TRANSLATE = "translate" # 翻译
    ANALYZE = "analyze"     # 摘要/分析
    CREATIVE = "creative"   # 创意写作
    MATH = "math"           # 数学推理
    GENERAL = "general"     # 通用


# 路由表
ROUTE_TABLE: Dict[TaskType, List[str]] = {
    TaskType.CODE:        ["claude", "deepseek"],
    TaskType.CHINESE_CHAT:["kimi", "deepseek"],
    TaskType.TRANSLATE:   ["deepseek", "kimi"],
    TaskType.ANALYZE:     ["claude", "kimi"],
    TaskType.CREATIVE:    ["claude", "deepseek"],
    TaskType.MATH:        ["deepseek", "claude"],
    TaskType.GENERAL:     ["deepseek", "kimi", "claude"],
}


# ═══════════════════════════════════════════════════════
# 模型配置
# ═══════════════════════════════════════════════════════

MODEL_CONFIGS = {
    "claude": {
        "api_key_env": "CLAUDE_API_KEY",
        "base_url": "https://api.anthropic.com/v1",
        "endpoint": "/messages",
        "model": "claude-3-5-sonnet-20241022",
        "max_tokens": 4096,
        "auth_header": "x-api-key",
        "auth_prefix": "",
    },
    "deepseek": {
        "api_key_env": "DEEPSEEK_API_KEY",
        "base_url": "https://api.deepseek.com/v1",
        "endpoint": "/chat/completions",
        "model": "deepseek-chat",
        "max_tokens": 4096,
        "auth_header": "Authorization",
        "auth_prefix": "Bearer ",
    },
    "kimi": {
        "api_key_env": "KIMI_API_KEY",
        "base_url": "https://api.moonshot.cn/v1",
        "endpoint": "/chat/completions",
        "model": "moonshot-v1-8k",
        "max_tokens": 4096,
        "auth_header": "Authorization",
        "auth_prefix": "Bearer ",
    },
    "openai": {
        "api_key_env": "OPENAI_API_KEY",
        "base_url": "https://api.openai.com/v1",
        "endpoint": "/chat/completions",
        "model": "gpt-4o-mini",
        "max_tokens": 4096,
        "auth_header": "Authorization",
        "auth_prefix": "Bearer ",
    },
}


# ═══════════════════════════════════════════════════════
# 核心 API 调用
# ═══════════════════════════════════════════════════════

def _get_api_key(provider: str) -> Optional[str]:
    """获取指定提供商的API密钥"""
    config = MODEL_CONFIGS[provider]
    # 先从环境变量取
    env_key = os.environ.get(config["api_key_env"])
    if env_key:
        return env_key
    # 再从 vault 取
    return get_credential(config["api_key_env"])


def _build_dna() -> str:
    """生成请求 DNA 追溯码"""
    ts = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
    h = hashlib.sha256(ts.encode()).hexdigest()[:8].upper()
    return f"#龍芯⚡️{ts}-AI-GATEWAY-{h}"


def _call_openai_format(provider: str, messages: List[Dict[str, Any]], 
                         temperature: float = 0.7) -> Dict[str, Any]:
    """调用 OpenAI 兼容 API (DeepSeek/Kimi/OpenAI)"""
    config = MODEL_CONFIGS[provider]
    api_key = _get_api_key(provider)
    if not api_key:
        raise ValueError(f"❌ {provider} API Key 未配置")
    
    url = f"{config['base_url']}{config['endpoint']}"
    headers = {
        config["auth_header"]: f"{config['auth_prefix']}{api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": config["model"],
        "messages": messages,
        "max_tokens": config["max_tokens"],
        "temperature": temperature,
    }
    
    logger.info(f"📤 {provider} 请求 | model={config['model']} | msgs={len(messages)}")
    
    try:
        with httpx.Client(timeout=120.0) as client:
            resp = client.post(url, json=payload, headers=headers)
            resp.raise_for_status()
            data = resp.json()
            content = data["choices"][0]["message"]["content"]
            logger.info(f"✅ {provider} 响应 | tokens={data.get('usage', {}).get('completion_tokens', '?')}")
            return {
                "content": content,
                "model": config["model"],
                "provider": provider,
                "usage": data.get("usage", {}),
            }
    except Exception as e:
        logger.error(f"❌ {provider} 调用失败: {e}")
        raise


def _call_claude_format(provider: str, messages: List[Dict[str, Any]],
                        system: str = "", temperature: float = 0.7) -> Dict[str, Any]:
    """调用 Anthropic/Claude API"""
    config = MODEL_CONFIGS[provider]
    api_key = _get_api_key(provider)
    if not api_key:
        raise ValueError(f"❌ {provider} API Key 未配置")
    
    url = f"{config['base_url']}{config['endpoint']}"
    headers = {
        config["auth_header"]: api_key,
        "Content-Type": "application/json",
        "anthropic-version": "2023-06-01",
    }
    
    # 转换消息格式
    anthropic_msgs = []
    for msg in messages:
        role = msg.get("role")
        if role == "system":
            system = msg.get("content", "")
        else:
            anthropic_msgs.append({"role": role, "content": msg.get("content", "")})
    
    payload = {
        "model": config["model"],
        "messages": anthropic_msgs,
        "max_tokens": config["max_tokens"],
        "temperature": temperature,
    }
    if system:
        payload["system"] = system
    
    try:
        with httpx.Client(timeout=120.0) as client:
            resp = client.post(url, json=payload, headers=headers)
            resp.raise_for_status()
            data = resp.json()
            content = data["content"][0]["text"]
            logger.info(f"✅ {provider} 响应 | tokens={data.get('usage', {}).get('output_tokens', '?')}")
            return {
                "content": content,
                "model": config["model"],
                "provider": provider,
                "usage": data.get("usage", {}),
            }
    except Exception as e:
        logger.error(f"❌ {provider} 调用失败: {e}")
        raise


# ═══════════════════════════════════════════════════════
# 智能路由调用
# ═══════════════════════════════════════════════════════

def chat(messages: List[Dict[str, Any]], task_type: TaskType = TaskType.GENERAL,
         temperature: float = 0.7, system: str = "") -> Dict[str, Any]:
    """
    统一对话入口 - 自动路由到最佳模型
    
    Args:
        messages: [{"role": "user", "content": "..."}, ...]
        task_type: 任务类型（code/cn/translate/analyze/creative/math/general）
        temperature: 温度参数
        system: 系统提示词
    
    Returns:
        {"content": "...", "model": "...", "provider": "...", "dna": "..."}
    """
    dna = _build_dna()
    providers = ROUTE_TABLE.get(task_type, ROUTE_TABLE[TaskType.GENERAL])
    
    last_error = None
    for provider in providers:
        try:
            if provider == "claude":
                result = _call_claude_format(provider, messages, system, temperature)
            else:
                # DeepSeek/Kimi/OpenAI 都用 OpenAI 兼容格式
                if system:
                    messages = [{"role": "system", "content": system}] + list(messages)
                result = _call_openai_format(provider, messages, temperature)
            
            result["dna"] = dna
            result["routed_via"] = provider
            result["task_type"] = task_type.value
            return result
            
        except Exception as e:
            last_error = e
            logger.warning(f"⚠️ {provider} 失败，尝试下一个... ({e})")
            continue
    
    raise RuntimeError(f"❌ 所有模型均失败 (tried: {providers}) | last: {last_error}")


def classify_task(text: str) -> TaskType:
    """
    自动分类任务类型（简单关键词匹配）
    """
    text_lower = text.lower()
    
    # 代码相关
    code_keywords = ["代码", "code", "函数", "function", "bug", "报错", "error",
                     "编译", "compile", "实现", "implement", "算法", "algorithm",
                     "python", "c语言", "javascript", "修复", "fix"]
    if any(kw in text_lower for kw in code_keywords):
        return TaskType.CODE
    
    # 翻译
    translate_keywords = ["翻译", "translate", "英文", "中文", "日语",
                          "english", "chinese", "japanese"]
    if any(kw in text_lower for kw in translate_keywords):
        return TaskType.TRANSLATE
    
    # 数学
    math_keywords = ["计算", "公式", "方程", "证明", "推导", "数学",
                     "matrix", "矩阵", "概率", "统计"]
    if any(kw in text_lower for kw in math_keywords):
        return TaskType.MATH
    
    # 创意
    creative_keywords = ["写", "创作", "故事", "诗歌", "文案", "小说",
                         "write", "story", "create", "创意"]
    if any(kw in text_lower for kw in creative_keywords):
        return TaskType.CREATIVE
    
    # 中文 → Kimi
    if any('\u4e00' <= c <= '\u9fff' for c in text[:50]):
        return TaskType.CHINESE_CHAT
    
    return TaskType.GENERAL


# ═══════════════════════════════════════════════════════
# 可用性检查
# ═══════════════════════════════════════════════════════

def check_available() -> Dict[str, bool]:
    """检查各模型是否可用"""
    result = {}
    for provider in MODEL_CONFIGS:
        key = _get_api_key(provider)
        result[provider] = bool(key)
        if key:
            logger.info(f"🟢 {provider}: 已配置")
        else:
            logger.info(f"🔴 {provider}: 未配置（将跳过）")
    return result


# ═══════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════
if __name__ == "__main__":
    if "--check" in sys.argv:
        available = check_available()
        print(f"📊 AI 网关状态:")
        for p, ok in available.items():
            print(f"  {'🟢' if ok else '🔴'} {p}")
        sys.exit(0)
    
    if "--chat" in sys.argv:
        idx = sys.argv.index("--chat")
        prompt = " ".join(sys.argv[idx + 1:])
        if not prompt:
            print("用法: --chat \"你的问题\"")
            sys.exit(1)
        
        task = classify_task(prompt)
        print(f"🧠 任务类型: {task.value} | 路由: {' → '.join(ROUTE_TABLE[task])}")
        print(f"📤 发送中...")
        
        try:
            result = chat(
                messages=[{"role": "user", "content": prompt}],
                task_type=task
            )
            print(f"\n✅ [{result['provider']}] {result['model']}")
            print(f"   DNA: {result.get('dna', '')}")
            print(f"\n{result['content']}")
        except Exception as e:
            print(f"❌ {e}")
            sys.exit(1)
        sys.exit(0)
    
    # 默认
    print("龍魂 AI 网关 v1.0")
    print("用法: --check 检查状态 | --chat \"问题\" 对话")
    check_available()
