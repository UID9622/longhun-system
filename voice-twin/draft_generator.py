#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂真声 · 代笔草稿器
根据 UID9622 的语音风格，生成三个版本的表达草稿。

DNA: #龍芯⚡️2026-06-25-VOICE-TWIN-DRAFT-GENERATOR-v1.0
"""

import json
import argparse
import os
import subprocess
import sys
import requests
from pathlib import Path
from typing import List, Optional, Any

ROOT = Path(__file__).resolve().parent
PROFILE_PATH = ROOT / "style_profile.json"
TRANSCRIPTS_PATH = ROOT / "all-transcripts.txt"
MODEL = "longhun-9622:latest"


def _load_deepseek_key() -> Optional[str]:
    """从龍魂 Vault 或环境变量加载 DeepSeek API Key"""
    # 优先环境变量
    env_key = os.getenv("DEEPSEEK_API_KEY")
    if env_key:
        return env_key
    # 其次 Vault
    try:
        sys.path.insert(0, str(Path.home() / ".longhun" / "multi-ai-gateway"))
        import yaml
        from vault_loader import VaultLoader
        cfg_path = Path.home() / ".longhun" / "multi-ai-gateway" / "config.yaml"
        cfg = yaml.safe_load(cfg_path.read_text(encoding="utf-8"))
        return VaultLoader(cfg).get_key("deepseek")
    except Exception:
        return None


def call_deepseek(system_prompt: str, user_prompt: str) -> str:
    """调用 DeepSeek API（龍魂 Vault 自动解密 key）"""
    key = _load_deepseek_key()
    if not key:
        return "[DeepSeek API Key 未配置]"

    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.8,
        "stream": False
    }
    try:
        resp = requests.post(
            "https://api.deepseek.com/chat/completions",
            headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
            json=payload,
            timeout=60
        )
        resp.raise_for_status()
        data = resp.json()
        return data["choices"][0]["message"]["content"]
    except Exception as e:
        return f"[DeepSeek 调用失败: {e}]"


def _ollama_available() -> bool:
    """检查 Ollama 本地服务是否可用"""
    try:
        r = requests.get("http://localhost:11434/api/tags", timeout=3)
        return r.status_code == 200
    except Exception:
        return False


def load_style_profile() -> dict[str, Any]:
    return json.loads(PROFILE_PATH.read_text(encoding="utf-8"))


def load_transcripts_sample(max_chars: int = 2000) -> str:
    text = TRANSCRIPTS_PATH.read_text(encoding="utf-8")
    return text[:max_chars]


def build_system_prompt(profile: dict[str, Any], sample: str) -> str:
    fillers = profile.get("口头禅", {})
    emotions = profile.get("情绪分布", {})
    return f"""你是 UID9622（龍芯北辰）的数字人分身。你正在模仿他的真实表达风格写作。

【风格特征】
- 总语料约 {profile.get('总字数', 0)} 字，平均句长 {profile.get('平均句长', 0)} 字
- 高频口头禅："对不对"{fillers.get('对不对', 0)}次，"是不是"{fillers.get('是不是', 0)}次，"嘛"{fillers.get('嘛', 0)}次
- 情绪倾向：愤怒{emotions.get('愤怒', 0)}、坚定{emotions.get('坚定', 0)}、关怀{emotions.get('关怀', 0)}、孤独{emotions.get('孤独', 0)}
- 说话特点：接地气、带温州口音影响、口语化、爱用反问、直接骂资本和平台、强调"为人民服务""数据主权"

【表达原则】
1. 不装精英，不书面化
2. 火气该有就有，但不乱咬人
3. 讲道理时从老百姓/底层视角出发
4. 会用"老子""他妈""狗日"等粗话，但不是为了脏而脏
5. 结尾常带"对不对""是不是""知道吧"

【参考语料片段】
{sample}

【任务】
用户给你一个话题，你要用以上风格写表达草稿。输出三个版本，用 ### 分隔：
### A. 原汁原味版
完全按 UID9622 的火气、口气、用词习惯写，不修饰。

### B. 合规表达版
保留核心观点和情绪，但去掉最可能被平台删除的粗话和敏感词，让它能发出去。

### C. 证据链版
在合规版基础上，加入"我有录音/有截图/有数据"等取证语气，适合维权、投诉、举报场景。
"""


def call_ollama(system_prompt: str, user_prompt: str, model: str = MODEL) -> str:
    """调用本地 Ollama；不可用时自动回退 DeepSeek API"""
    if not _ollama_available():
        return call_deepseek(system_prompt, user_prompt)

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
    payload = {
        "model": model,
        "messages": messages,
        "stream": False,
        "options": {"temperature": 0.8, "num_ctx": 4096}
    }
    try:
        resp = requests.post(
            "http://localhost:11434/api/chat",
            headers={"Content-Type": "application/json"},
            json=payload,
            timeout=90
        )
        resp.raise_for_status()
        data = resp.json()
        return data.get("message", {}).get("content", "[无输出]")
    except Exception as e:
        return call_deepseek(system_prompt, user_prompt)


# 统一 LLM 调用入口（保持向后兼容）
call_llm = call_ollama


def generate(topic: str) -> str:
    profile = load_style_profile()
    sample = load_transcripts_sample()
    system_prompt = build_system_prompt(profile, sample)
    user_prompt = f"话题：{topic}\n\n请按系统提示的风格生成三个版本的表达草稿。"
    return call_ollama(system_prompt, user_prompt)


def main():
    parser = argparse.ArgumentParser(description="龍魂真声代笔草稿器")
    parser.add_argument("topic", nargs="?", help="要表达的话题")
    args = parser.parse_args()

    if not args.topic:
        topic = input("请输入话题: ")
    else:
        topic = args.topic

    print(f"🎙️ 正在为话题生成草稿: {topic}\n")
    result = generate(topic)
    print(result)

    # 保存
    safe_topic = "".join(c if c.isalnum() or c in "_-" else "_" for c in topic)[:30]
    out_path = ROOT / f"draft_{safe_topic}.md"
    out_path.write_text(f"# 话题: {topic}\n\n{result}\n", encoding="utf-8")
    print(f"\n✅ 草稿已保存: {out_path}")


if __name__ == "__main__":
    main()
