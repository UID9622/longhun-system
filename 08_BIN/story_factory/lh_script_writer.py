#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 龍芯⚡️丙午·丙申·辛酉·未时·☰乾-SCRIPT-WRITER-v1.1
"""
🐉 龍魂 · 编剧大脑 v1.1
双后端：本地 longhun-small-instruct-v1.3（离线）+ Kimi K3 API（在线）。
所有输出带 DNA，可直接喂给 lh_story_pipeline.py。
"""

import argparse
import json
import os
import re
import time
import hashlib
import requests
from pathlib import Path
from datetime import datetime

from mlx_lm import load, generate
import mlx.core as mx


ENGINE_ROOT = Path(__file__).resolve().parent
DEFAULT_MODEL = "~/longhun-system/models/longhun-small-instruct-v1.3/merged"
KIMI_BASE_URL = "https://api.moonshot.cn/v1"
KIMI_MODEL = "kimi-k3"
SYSTEM_PROMPT = (
    "你是龍魂故事工厂的编剧大脑。你熟悉角色卡、人格声线与素材货架。"
    "你的输出必须是可以直接解析的 JSON，不要 markdown 代码块，不要解释。"
)


def generate_dna(topic: str = "SCRIPT") -> str:
    h = hashlib.sha256(f"{topic}{time.time()}".encode()).hexdigest()[:8].upper()
    return f"#龍芯⚡️{datetime.now().strftime('%Y-%m-%d')}-{topic}-{h}-UID9622"


def now() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def make_sampler(temperature: float):
    def sampler(logits):
        if temperature == 0:
            return mx.argmax(logits, axis=-1)
        return mx.random.categorical(logits / temperature)
    return sampler


def load_model(model_path: str):
    model_path = Path(model_path).expanduser().resolve()
    if not model_path.exists():
        raise FileNotFoundError(f"模型路径不存在: {model_path}")
    print(f"[{now()}] 📦 加载本地龍魂编剧模型: {model_path}")
    model, tokenizer = load(
        str(model_path),
        tokenizer_config={"trust_remote_code": True}
    )
    return model, tokenizer


def build_script_prompt(project: str, theme: str, shots: int, characters: list, assets: list) -> str:
    char_lines = "\n".join(
        f"- {c['code']} {c.get('name','')}（{c.get('role','')}）: {c.get('persona','') or c.get('anchors',{}).get('face','')}" 
        for c in characters
    )
    asset_lines = "\n".join(f"- {a}" for a in assets)
    return f"""你是龍魂故事工厂的编剧大脑。请为项目「{project}」生成试播集分镜表。

【场景主题】{theme}
【角色】
{char_lines}
【可用素材】
{asset_lines}

【硬性要求】
1. 必须生成 {shots} 个镜头，编码从 EP01-S01 到 EP01-S{shots:02d}，缺一不可。
2. 每个镜头的 character、asset、line、action、duration 必须填写真实原创内容，不允许填 "..."、"这里是"、"示例" 或空字符串。
3. line（台词）控制在 30 字以内，action（动作）控制在 40 字以内，务必简短有力。
4. {shots} 个镜头必须是同一场戏的不同阶段（开场→发展→收尾），台词前后连贯，action 不能重复。
5. 台词原创，符合角色人格，不抄袭原著。
6. 只输出纯 JSON，不要 markdown 代码块，不要解释，不要注释。

【参考风格】（仅示范格式，内容请原创，禁止照搬）
- 三眼台词示例："道上混这么久，头一回有人叫我本名。"
- 谢文东台词示例："钱买不来平安，人才行。"
- action 示例：持刀站立，雨滴从帽檐滴落；眯眼微笑，把烟头按灭在墙根；抱拳拱手，侧身让出一步。

【输出格式示例】
{{"scenes":[{{"shot_code":"EP01-S01","character":"HD-002","asset":"ENV-02_老街雨夜.png","line":"原创台词","action":"原创动作","duration":4}},{{"shot_code":"EP01-S02","character":"HD-001","asset":"HD-001_谢文东_少年锚点图.png","line":"原创台词","action":"原创动作","duration":5}},{{"shot_code":"EP01-S03","character":"HD-002","asset":"ENV-02_老街雨夜.png","line":"原创台词","action":"原创动作","duration":4}}]}}
"""


def extract_json(text: str) -> dict:
    """从模型输出中提取 JSON，容忍尾部垃圾字符。"""
    m = re.search(r"```(?:json)?\s*([\s\S]*?)```", text)
    if m:
        text = m.group(1)
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1 or end <= start:
        raise ValueError("未在输出中找到 JSON 对象")
    candidate = text[start:end+1]
    try:
        return json.loads(candidate)
    except json.JSONDecodeError as e:
        last_brace = candidate.rfind("}")
        if last_brace > 0:
            try:
                return json.loads(candidate[:last_brace+1])
            except json.JSONDecodeError:
                pass
        raise ValueError(f"JSON 解析失败: {e}\n候选文本: {candidate[:200]}")


def load_characters(project: str) -> list:
    char_dir = ENGINE_ROOT / "assets" / project / "characters"
    if not char_dir.exists():
        return []
    chars = []
    for f in sorted(char_dir.glob("*.json")):
        with open(f, "r", encoding="utf-8") as fp:
            chars.append(json.load(fp))
    return chars


def generate_local(prompt_text: str, model_path: str, temp: float, max_tokens: int) -> str:
    """本地模型生成。"""
    model, tokenizer = load_model(model_path)
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": prompt_text},
    ]
    full_prompt = tokenizer.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=True
    )
    print(f"[{now()}] ✍️  本地模型生成中...")
    t0 = time.time()
    output = generate(
        model,
        tokenizer,
        prompt=full_prompt,
        max_tokens=max_tokens,
        sampler=make_sampler(temp),
        verbose=False,
    )
    print(f"[{now()}] ✅ 本地生成完成，耗时 {time.time()-t0:.1f}s")
    return output


def generate_kimi(prompt_text: str, temp: float, max_tokens: int) -> str:
    """Kimi K3 API 生成。"""
    api_key = os.environ.get("KIMI_API_KEY") or os.environ.get("MOONSHOT_API_KEY")
    if not api_key:
        raise RuntimeError("未设置 KIMI_API_KEY 或 MOONSHOT_API_KEY 环境变量")

    # Kimi K3 当前只支持 temperature=1
    if temp != 1.0:
        print(f"[{now()}] ⚠️ Kimi K3 要求 temperature=1，已将 {temp} 重置为 1.0")
        temp = 1.0

    print(f"[{now()}] 🌙 调用 Kimi K3 API...")
    t0 = time.time()
    resp = requests.post(
        f"{KIMI_BASE_URL}/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": KIMI_MODEL,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt_text},
            ],
            "temperature": temp,
            "max_tokens": max_tokens,
        },
        timeout=120,
    )
    elapsed = time.time() - t0
    if resp.status_code != 200:
        raise RuntimeError(f"Kimi API 错误 {resp.status_code}: {resp.text[:500]}")
    data = resp.json()
    output = data["choices"][0]["message"]["content"]
    print(f"[{now()}] ✅ Kimi 生成完成，耗时 {elapsed:.1f}s")
    return output


def write_script(
    project: str,
    theme: str,
    shots: int = 3,
    assets: list = None,
    backend: str = "auto",
    model_path: str = DEFAULT_MODEL,
    temp: float = 0.7,
    max_tokens: int = 1024,
):
    assets = assets or ["ENV-02_老街雨夜.png"]
    chars = load_characters(project)
    if not chars:
        print(f"[{now()}] ⚠️ 项目 {project} 没有角色卡，将使用默认角色编码")

    prompt_text = build_script_prompt(project, theme, shots, chars, assets)

    # 后端选择
    if backend == "auto":
        if os.environ.get("KIMI_API_KEY") or os.environ.get("MOONSHOT_API_KEY"):
            backend = "kimi"
        else:
            backend = "local"

    output = None
    if backend == "kimi":
        try:
            output = generate_kimi(prompt_text, temp, max_tokens)
        except Exception as e:
            print(f"[{now()}] ⚠️ Kimi 调用失败: {e}")
            print(f"[{now()}] 🔄 Fallback 到本地模型...")
            output = generate_local(prompt_text, model_path, temp, max_tokens)
    else:
        output = generate_local(prompt_text, model_path, temp, max_tokens)

    try:
        script = extract_json(output)
    except Exception as e:
        print(f"[{now()}] ❌ JSON 解析失败: {e}")
        print("原始输出:\n", output)
        return None

    # 注入元数据
    script["dna"] = generate_dna("SCRIPT")
    script["project"] = project
    script["theme"] = theme
    script["backend"] = backend
    script["model"] = KIMI_MODEL if backend == "kimi" else str(Path(model_path).expanduser().resolve())
    script["created"] = datetime.now().isoformat()

    # 保存
    out_dir = ENGINE_ROOT / "output" / "scripts"
    out_dir.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_path = out_dir / f"{project}_script_{ts}.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(script, f, ensure_ascii=False, indent=2)

    print(f"[{now()}] 📝 分镜表保存: {out_path}")
    print(f"[{now()}] 🧬 DNA: {script['dna']}")
    return script


def main():
    parser = argparse.ArgumentParser(description="龍魂 · 编剧大脑")
    parser.add_argument("--project", default="坏蛋", help="项目名")
    parser.add_argument("--theme", required=True, help="场景主题/一句话剧情")
    parser.add_argument("--shots", type=int, default=3, help="镜头数量")
    parser.add_argument("--assets", default="", help="素材编码列表，逗号分隔")
    parser.add_argument("--backend", default="auto", help="后端: auto/local/kimi")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="本地模型路径")
    parser.add_argument("--temp", type=float, default=0.7, help="温度")
    parser.add_argument("--max-tokens", type=int, default=1024, help="最大 token 数")
    args = parser.parse_args()

    assets = [a.strip() for a in args.assets.split(",") if a.strip()] or None
    write_script(
        project=args.project,
        theme=args.theme,
        shots=args.shots,
        assets=assets,
        backend=args.backend,
        model_path=args.model,
        temp=args.temp,
        max_tokens=args.max_tokens,
    )


if __name__ == "__main__":
    main()
