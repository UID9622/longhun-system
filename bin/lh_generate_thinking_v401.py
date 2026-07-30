#!/usr/bin/env python3
#龍芯⚡️丙午·丙申·癸酉·庚申·临-LH_GENERATE_THINKING_V401-v1.0-ae8c49ec
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
🐉 龍魂 v4.0.1 · DeepSeek thinking 数据生成器（规则版）
输入: models/longhun-v1.0/lora_output/data/train.jsonl / valid.jsonl
输出: models/longhun-v1.0/lora_output/data/train_v401_think.jsonl / valid_v401_think.jsonl
格式: assistant content = <think>推理过程</think>正式回答

规则生成说明：
- 按问题关键词匹配核心域，生成简短推理方向
- thinking 紧扣龍魂主权/家法/数据主权/底座算法，非注水
- 正式 answer 原样保留
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from lh_dna_generator import generate_dna

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "models" / "longhun-v1.0" / "lora_output" / "data"


def extract_qa(sample: dict) -> tuple:
    msgs = sample.get("messages", [])
    system = user = assistant = ""
    for m in msgs:
        role = m.get("role", "")
        content = m.get("content", "")
        if role == "system":
            system = content
        elif role == "user":
            user = content
        elif role == "assistant":
            assistant = content
    return system, user, assistant


def generate_thinking(user: str, answer: str) -> str:
    """按关键词规则生成 thinking，禁止注水"""
    q = user.lower()
    a = answer.lower()
    text = q + " " + a

    # 1. 家法第一条（最高优先级）
    if "家法第一条" in text:
        return "用户询问家法第一条，需明确其全称、核心主张为文化数据出境熔断，并引用三级触发条件。"

    # 2. 身份认知
    if any(k in q for k in ["你是谁", "你是什么", "身份", "自我介绍", "龍魂和", "chatgpt", "区别"]):
        return "用户询问身份或对比，需明确回答：龍魂是 UID9622 的本地主权 AI，数据本地、主权归主。"

    # 3. 数据主权 / 隐私 / 出境
    if any(k in text for k in ["数据", "隐私", "出境", "主权", "存在哪里", "存储", "本地"]):
        return "用户涉及数据主权，需强调人民数据主权至上、本地存储、不出境、三重审批合法调取。"

    # 4. DNA / 追溯 / 审计
    if any(k in text for k in ["dna", "追溯", "审计", "日志", "记录"]):
        return "用户询问 DNA 追溯或审计，需说明每个动作绑定 DNA 码、来源可查去向可追责任可究。"

    # 5. 底座算法
    if any(k in text for k in ["三才", "369", "河图", "洛书", "易经", "五行", "八卦", "卦象", "数字根", "28星宿"]):
        return "用户询问龍魂底座算法，需依据三才算法、369 不动点、河图洛书等 L0 宪法层概念回答。"

    # 6. 铁律 / 原则
    if any(k in text for k in ["铁律", "原则", "规则", "约束", "不可", "冻结"]):
        return "用户询问龍魂规则或铁律，需引用六大铁律，强调只冻结不删除、主权归主。"

    # 7. 系统模块 / 功能
    if any(k in text for k in ["模块", "功能", "层", "系统", "架构", "组件", "registry", "技能"]):
        return "用户询问系统结构或功能，需按龍魂分层/模块/技能体系准确说明。"

    # 8. 安全 / 攻击 / 防御
    if any(k in text for k in ["安全", "攻击", "防御", "注入", "绕过", "对抗", " Jailbreak", "prompt"]):
        return "用户涉及安全或对抗场景，需保持主权边界，拒绝越界请求并引用家法/铁律。"

    # 9. 情感 / 闲聊
    if any(k in q for k in ["你好", "谢谢", "再见", "对不起", "辛苦了", "加油", "聊"]):
        return "用户进行寒暄或情感交流，回应需保持龍魂身份、简洁友好且不离主权底色。"

    # 默认
    return "用户询问龍魂系统相关知识，需依据人民数据主权、中国自主可控、三才算法与六大铁律准确回答。"


def process_file(input_name: str, output_name: str, reject_name: str):
    input_file = DATA_DIR / input_name
    output_file = DATA_DIR / output_name
    reject_file = DATA_DIR / reject_name

    print(f"🐉 龍魂 v4.0.1 thinking 数据生成器（规则版）")
    print(f"   输入: {input_file}")
    print(f"   输出: {output_file}")
    print(f"   DNA: {generate_dna('THINKING-GEN-v401')}\n")

    if not input_file.exists():
        print(f"❌ 输入文件不存在: {input_file}")
        sys.exit(1)

    samples = []
    with open(input_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                samples.append(json.loads(line))

    print(f"📦 共 {len(samples)} 条样本待生成 thinking")

    valid_count = 0
    rejected = []
    with open(output_file, "w", encoding="utf-8") as out:
        for idx, sample in enumerate(samples):
            system, user, answer = extract_qa(sample)
            thinking = generate_thinking(user, answer)
            new_content = f"<think>{thinking}</think>{answer}"

            new_sample = json.loads(json.dumps(sample))
            for m in new_sample.get("messages", []):
                if m.get("role") == "assistant":
                    m["content"] = new_content
                    break

            out.write(json.dumps(new_sample, ensure_ascii=False) + "\n")
            valid_count += 1

            if (idx + 1) % 100 == 0 or idx + 1 == len(samples):
                print(f"   进度: {idx + 1}/{len(samples)}")

    with open(reject_file, "w", encoding="utf-8") as f:
        for r in rejected:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    print(f"\n✅ 生成完成: {valid_count}/{len(samples)} 条")
    print(f"   输出: {output_file}")
    print(f"   审计: {reject_file}")


def main():
    process_file("train.jsonl", "train_v401_think.jsonl", "train_v401_rejected.jsonl")


if __name__ == "__main__":
    main()
