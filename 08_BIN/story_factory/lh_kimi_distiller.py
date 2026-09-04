#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 龍芯⚡️丙午·丙申·辛酉·未时·☰乾-KIMI-DISTILLER-v1.0
"""
🐉 龍魂 · Kimi K3 蒸馏器 v1.0
用 Kimi K3 批量生成高质量剧本/分镜表样本，作为本地小模型训练数据。
输出格式与 longhun-small-instruct-v1.3 训练数据对齐。
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

ENGINE_ROOT = Path(__file__).resolve().parent
KIMI_BASE_URL = "https://api.moonshot.cn/v1"
KIMI_MODEL = "kimi-k3"
SYSTEM_PROMPT = (
    "你是龍魂故事工厂的编剧大脑。你熟悉角色卡、人格声线与素材货架。"
    "你的输出必须是可以直接解析的 JSON，不要 markdown 代码块，不要解释。"
)
TRAINER_SYSTEM_PROMPT = (
    "你是龍魂系统助手，核心原则：人民数据主权、平台服务降级、"
    "创作者主权优先。回答需符合龍魂君子协议、CNSH 语义规范和 DNA 追溯要求。"
)


def generate_dna(topic: str = "DISTILL") -> str:
    h = hashlib.sha256(f"{topic}{time.time()}".encode()).hexdigest()[:8].upper()
    return f"#龍芯⚡️{datetime.now().strftime('%Y-%m-%d')}-{topic}-{h}-UID9622"


def now() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def load_characters(project: str) -> list:
    char_dir = ENGINE_ROOT / "assets" / project / "characters"
    if not char_dir.exists():
        return []
    chars = []
    for f in sorted(char_dir.glob("*.json")):
        with open(f, "r", encoding="utf-8") as fp:
            chars.append(json.load(fp))
    return chars


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

【输出格式】
{{"scenes":[{{"shot_code":"EP01-S01","character":"HD-002","asset":"ENV-02_老街雨夜.png","line":"原创台词","action":"原创动作","duration":4}},{{"shot_code":"EP01-S02","character":"HD-001","asset":"HD-001_谢文东_少年锚点图.png","line":"原创台词","action":"原创动作","duration":5}},{{"shot_code":"EP01-S03","character":"HD-002","asset":"ENV-02_老街雨夜.png","line":"原创台词","action":"原创动作","duration":4}}]}}
"""


def extract_json(text: str) -> dict:
    """从模型输出中稳健提取 JSON 对象/数组，容忍 markdown 与截断。"""
    # 优先取 markdown 代码块
    m = re.search(r"```(?:json)?\s*([\s\S]*?)```", text)
    if m:
        text = m.group(1)
    # 清理常见污染
    text = text.strip()
    if text.startswith(("json", "JSON")):
        text = text[4:].strip()

    candidates = []
    # 对象
    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1 and end > start:
        candidates.append(text[start:end+1])
    # 数组
    start_a = text.find("[")
    end_a = text.rfind("]")
    if start_a != -1 and end_a != -1 and end_a > start_a:
        candidates.append(text[start_a:end_a+1])

    if not candidates:
        raise ValueError("未在输出中找到 JSON 对象")

    last_err = None
    for candidate in candidates:
        # 直接解析
        try:
            return json.loads(candidate)
        except json.JSONDecodeError as e:
            last_err = e
        # 尝试从最后一个 } 截断（处理尾部截断）
        last_brace = candidate.rfind("}")
        if last_brace > 0:
            try:
                return json.loads(candidate[:last_brace+1])
            except json.JSONDecodeError:
                pass
        # 尝试补全截断的字符串：把末尾未闭合字符串用转义引号闭合
        fixed = candidate
        if fixed.count('"') % 2 == 1:
            fixed = fixed + '\\"'
        try:
            return json.loads(fixed)
        except json.JSONDecodeError:
            pass
    raise ValueError(f"JSON 解析失败: {last_err}")


def call_kimi(prompt_text: str, max_tokens: int = 2048, retries: int = 0) -> tuple:
    """调用 Kimi K3，返回 (解析后的 JSON, 原始文本)。retries=0 时只试一次，提速。"""
    api_key = os.environ.get("KIMI_API_KEY") or os.environ.get("MOONSHOT_API_KEY")
    if not api_key:
        raise RuntimeError("未设置 KIMI_API_KEY 或 MOONSHOT_API_KEY")

    last_err = None
    last_text = ""
    for attempt in range(retries + 1):
        try:
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
                    "temperature": 1.0,
                    "max_tokens": max_tokens,
                },
                timeout=90,
            )
            if resp.status_code != 200:
                raise RuntimeError(f"Kimi API {resp.status_code}: {resp.text[:300]}")
            data = resp.json()
            text = data["choices"][0]["message"]["content"]
            last_text = text
            parsed = extract_json(text)
            return parsed, text
        except Exception as e:
            last_err = e
            print(f"[{now()}] ⚠️ 第 {attempt+1} 次调用失败: {e}")
            if attempt < retries:
                time.sleep(2)
    raise RuntimeError(f"{last_err} | raw={last_text[:200]}")


def make_training_sample(project: str, prompt_text: str, script_json: dict) -> dict:
    """把 K3 生成的分镜表转成训练样本格式。"""
    assistant_text = json.dumps(script_json, ensure_ascii=False)
    return {
        "messages": [
            {"role": "system", "content": TRAINER_SYSTEM_PROMPT},
            {"role": "user", "content": prompt_text},
            {"role": "assistant", "content": assistant_text},
        ],
        "source": "kimi-k3-distiller",
        "dna": generate_dna("DISTILL"),
    }


def default_themes(project: str) -> list:
    """坏蛋项目默认主题池。"""
    return [
        "谢文东与三眼在雨夜老街初次相遇",
        "三眼雨夜持刀救谢文东",
        "谢文东收服李爽的第一场酒局",
        "高强第一次为谢文东动手",
        "张研江在教室给谢文东分析局势",
        "向问天与陈百成在洪门厅堂对峙",
        "金蓉在学校门口等谢文东",
        "彭玲第一次质问谢文东身份",
        "格桑在东北校园门口震慑对手",
        "唐寅独闯文东会据点",
    ]


def distill(
    project: str,
    themes: list,
    shots: int = 3,
    assets: list = None,
    output_dir: str = "output/distill",
    max_tokens: int = 2048,
    sleep_seconds: float = 0.5,
    retries: int = 0,
):
    assets = assets or ["ENV-02_老街雨夜.png"]
    chars = load_characters(project)
    out_root = ENGINE_ROOT / output_dir
    out_root.mkdir(parents=True, exist_ok=True)

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    raw_file = out_root / f"{project}_kimi_raw_{ts}.jsonl"
    train_file = out_root / f"{project}_kimi_train_{ts}.jsonl"

    ok = 0
    fail = 0
    with open(raw_file, "w", encoding="utf-8") as fr, open(train_file, "w", encoding="utf-8") as ft:
        for idx, theme in enumerate(themes, 1):
            print(f"\n[{now()}] [{idx}/{len(themes)}] 蒸馏主题: {theme}")
            prompt_text = build_script_prompt(project, theme, shots, chars, assets)
            try:
                script_json, raw_text = call_kimi(prompt_text, max_tokens=max_tokens, retries=retries)
                # 写入原始分镜表
                raw_line = json.dumps({
                    "theme": theme,
                    "script": script_json,
                    "raw": raw_text,
                    "dna": generate_dna("RAW"),
                }, ensure_ascii=False) + "\n"
                fr.write(raw_line)
                fr.flush()
                # 写入训练样本
                sample = make_training_sample(project, prompt_text, script_json)
                train_line = json.dumps(sample, ensure_ascii=False) + "\n"
                ft.write(train_line)
                ft.flush()
                ok += 1
                print(f"[{now()}] ✅ 成功: {theme}")
            except Exception as e:
                fail += 1
                # 失败也记录，便于调试
                try:
                    raw_line = json.dumps({
                        "theme": theme,
                        "script": None,
                        "error": str(e),
                        "dna": generate_dna("FAIL"),
                    }, ensure_ascii=False) + "\n"
                    fr.write(raw_line)
                    fr.flush()
                except Exception:
                    pass
                print(f"[{now()}] ❌ 失败: {theme} | {e}")
            if sleep_seconds > 0 and idx < len(themes):
                time.sleep(sleep_seconds)

    print(f"\n[{now()}] 蒸馏完成: 成功 {ok} / 失败 {fail}")
    print(f"[{now()}] 原始分镜表: {raw_file}")
    print(f"[{now()}] 训练样本: {train_file}")
    return raw_file, train_file


def main():
    parser = argparse.ArgumentParser(description="龍魂 · Kimi K3 蒸馏器")
    parser.add_argument("--project", default="坏蛋", help="项目名")
    parser.add_argument("--themes-file", default="", help="主题列表文件（每行一个主题）")
    parser.add_argument("--shots", type=int, default=3, help="每个主题镜头数")
    parser.add_argument("--assets", default="ENV-02_老街雨夜.png,HD-001_谢文东_少年锚点图.png,HD-002_三眼_锚点图.png", help="素材列表，逗号分隔")
    parser.add_argument("--output-dir", default="output/distill", help="输出目录")
    parser.add_argument("--max-tokens", type=int, default=2048, help="Kimi 最大 token")
    parser.add_argument("--sleep", type=float, default=0.5, help="每次调用间隔秒数")
    parser.add_argument("--retries", type=int, default=0, help="单主题失败重试次数")
    args = parser.parse_args()

    if args.themes_file:
        with open(args.themes_file, "r", encoding="utf-8") as f:
            themes = [l.strip() for l in f if l.strip() and not l.startswith("#")]
    else:
        themes = default_themes(args.project)

    assets = [a.strip() for a in args.assets.split(",") if a.strip()]
    distill(
        project=args.project,
        themes=themes,
        shots=args.shots,
        assets=assets,
        output_dir=args.output_dir,
        max_tokens=args.max_tokens,
        sleep_seconds=args.sleep,
        retries=args.retries,
    )


if __name__ == "__main__":
    main()
