#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 龍芯⚡️丙午·丙申·辛酉·戌时·☲離-LOCAL-LLM-v1.0
"""
🐉 龍魂 · 本地语言模型接口 v1.0

零 API 成本，调用本地 Qwen / Longhun 模型生成剧本、台词、分镜描述。
默认模型: /Users/zuimeidedeyihan/longhun-system/models/qwen-1.5b-instruct
"""

import argparse
import json
import hashlib
import time
from pathlib import Path
from datetime import datetime

DEFAULT_MODEL = "/Users/zuimeidedeyihan/longhun-system/models/qwen-1.5b-instruct"


def generate_dna(tag: str = "LLM") -> str:
    h = hashlib.sha256(f"{tag}{time.time()}".encode()).hexdigest()[:8].upper()
    return f"#龍芯⚡️{datetime.now().strftime('%Y-%m-%d')}-{tag}-{h}-UID9622"


class LocalLLM:
    def __init__(self, model_path: str = DEFAULT_MODEL, device: str = "auto"):
        self.model_path = Path(model_path)
        self.device = device
        self._tokenizer = None
        self._model = None

    def load(self):
        if self._model is not None:
            return
        try:
            from transformers import AutoTokenizer, AutoModelForCausalLM
            import torch
        except ImportError as e:
            raise RuntimeError(f"缺少依赖: {e}。请安装 transformers 和 torch。") from e

        print(f"🧠 加载本地模型: {self.model_path}")
        self._tokenizer = AutoTokenizer.from_pretrained(
            str(self.model_path), trust_remote_code=True
        )
        self._model = AutoModelForCausalLM.from_pretrained(
            str(self.model_path),
            trust_remote_code=True,
            torch_dtype=torch.float32,
            device_map=self.device if self.device != "auto" else None,
        )
        if self.device != "auto":
            self._model = self._model.to(self.device)
        print("✅ 模型加载完成")

    def chat(self, system: str, user: str, max_new_tokens: int = 200, temperature: float = 0.7) -> str:
        self.load()
        messages = [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ]
        text = self._tokenizer.apply_chat_template(
            messages, tokenize=False, add_generation_prompt=True
        )
        inputs = self._tokenizer(text, return_tensors="pt")
        if self._model.device.type != "cpu":
            inputs = {k: v.to(self._model.device) for k, v in inputs.items()}

        outputs = self._model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=temperature > 0,
            temperature=temperature,
            top_p=0.9,
            pad_token_id=self._tokenizer.pad_token_id,
            eos_token_id=self._tokenizer.eos_token_id,
        )
        full = self._tokenizer.decode(outputs[0], skip_special_tokens=True)
        # 截取出 assistant 回复
        if "assistant" in full:
            reply = full.split("assistant", 1)[-1].strip()
        else:
            reply = full.replace(text, "").strip()
        return reply

    def generate_dialogue(self, character: str, context: str, tone: str = "", max_tokens: int = 80) -> str:
        system = (
            "你是龍魂剧本助手。根据人物性格和场景，写出一句原创中文台词。"
            "只输出台词本身，不要解释、不要括号、不要动作描述。"
        )
        user = f"人物：{character}\n场景：{context}\n语气：{tone}\n请写一句台词："
        return self.chat(system, user, max_tokens, temperature=0.8)

    def generate_shot_prompt(self, scene: str, action: str, style: str = "电影感") -> str:
        system = (
            "你是龍魂分镜助手。把场景和动作翻译成适合 AI 图像生成的英文提示词。"
            "只输出英文提示词，不超过 80 词。"
        )
        user = f"场景：{scene}\n动作：{action}\n风格：{style}\n英文提示词："
        return self.chat(system, user, 120, temperature=0.6)


def main():
    parser = argparse.ArgumentParser(description="龍魂 · 本地 LLM")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="本地模型路径")
    parser.add_argument("--device", default="cpu", help="cpu / mps / cuda")
    parser.add_argument("--mode", default="chat", choices=["chat", "dialogue", "prompt"], help="任务类型")
    parser.add_argument("--system", default="你是龍魂助手。", help="system 提示")
    parser.add_argument("--user", default="", help="user 输入")
    parser.add_argument("--character", default="", help="对话模式：人物")
    parser.add_argument("--context", default="", help="对话模式：场景")
    parser.add_argument("--tone", default="", help="对话模式：语气")
    parser.add_argument("--max-tokens", type=int, default=200, help="最大生成 token")
    parser.add_argument("--output", default="", help="输出 JSON 文件路径")
    args = parser.parse_args()

    llm = LocalLLM(args.model, args.device)

    if args.mode == "chat":
        reply = llm.chat(args.system, args.user, args.max_tokens)
    elif args.mode == "dialogue":
        reply = llm.generate_dialogue(args.character, args.context, args.tone, args.max_tokens)
    elif args.mode == "prompt":
        reply = llm.generate_shot_prompt(args.context, args.user)
    else:
        reply = ""

    print(reply)

    if args.output:
        out = {
            "dna": generate_dna("LLM"),
            "model": args.model,
            "mode": args.mode,
            "input": {"system": args.system, "user": args.user},
            "output": reply,
            "created": datetime.now().isoformat(),
        }
        Path(args.output).write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
