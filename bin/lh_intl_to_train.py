#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations
"""
龍魂·国际数据→train.jsonl格式转换器 v1.0
DNA: #龍芯⚡️丙午·辛未·乙酉·辰时·讼-INTL-TO-TRAIN-v1.0

将 lh_intl_cleaner 生成的 {instruction/input/output} 格式
转换为 train.jsonl 的 {messages} 格式
"""

import json, sys, random
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
INTL_TRAIN_DIR = PROJECT_ROOT / "data" / "sources" / "intl" / "train"
DATA_DIR = PROJECT_ROOT / "models" / "longhun-v1.0" / "lora_output" / "data"
TRAIN_FILE = DATA_DIR / "train.jsonl"
VALID_FILE = DATA_DIR / "valid.jsonl"

# 用户前缀模板
USER_PREFIX = "你是龍魂 longhun-v1.7，基于龍魂系统自有语料训练。你由UID9622（诸葛鑫·Lucky）创建，服务于中国数据主权和AI治理。\n\n[国际技术参考] "


def convert_intl_to_messages(intl_item: dict[str, Any]) -> dict[str, Any]:
    """转换国际训练数据为messages格式"""
    instruction = intl_item.get("instruction", "")
    content = intl_item.get("input", "")
    output = intl_item.get("output", "")
    meta = intl_item.get("metadata", {})

    # 构建user消息
    user_msg = f"{USER_PREFIX}{instruction}\n\n内容：{content}"

    # 构建assistant消息
    assistant_msg = output

    return {
        "messages": [
            {"role": "user", "content": user_msg},
            {"role": "assistant", "content": assistant_msg},
        ]
    }


def main():
    print("🐉 龍魂·国际数据→train.jsonl格式转换器")
    print("=" * 60)

    # 查找所有国际训练文件
    intl_files = sorted(INTL_TRAIN_DIR.glob("intl_train_*.jsonl"))
    if not intl_files:
        print("⚠️ 未找到国际训练数据文件")
        print(f"   路径: {INTL_TRAIN_DIR}")
        return

    print(f"📂 找到 {len(intl_files)} 个国际训练数据文件")

    all_converted = []
    for fpath in intl_files:
        with open(fpath, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f if line.strip()]
            for line in lines:
                try:
                    item = json.loads(line)
                    converted = convert_intl_to_messages(item)
                    all_converted.append(converted)
                except Exception as e:
                    print(f"   ⚠️ 解析失败: {e}")
        print(f"   {fpath.name}: {len(lines)} 条")

    print(f"\n📊 转换结果: {len(all_converted)} 条")

    if not all_converted:
        print("⚠️ 无有效数据可合并")
        return

    # 读取现有 train.jsonl
    with open(TRAIN_FILE, 'r') as f:
        existing = [json.loads(line.strip()) for line in f if line.strip()]
    print(f"   现有训练集: {len(existing)} 条")

    # 合并
    existing.extend(all_converted)
    random.shuffle(existing)

    # 划分训练/验证
    valid_n = max(int(len(existing) * 0.1), 10)
    valid_data = existing[-valid_n:]
    train_data = existing[:-valid_n]

    with open(TRAIN_FILE, 'w') as f:
        for item in train_data:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')
    with open(VALID_FILE, 'w') as f:
        for item in valid_data:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')

    print(f"\n✅ 合并完成:")
    print(f"   训练集: {len(train_data)} 条")
    print(f"   验证集: {len(valid_data)} 条")
    print(f"   国际数据贡献: {len(all_converted)} 条")

    # 更新 dataset_info
    info_path = DATA_DIR / "dataset_info.json"
    info = {
        "version": "v1.7",
        "description": "v1.6 CSDN (553) + 拒绝加固 (70) + 国际数据",
        "train_samples": len(train_data),
        "val_samples": len(valid_data),
        "intl_samples": len(all_converted),
        "rejection_hardening": 70,
        "csdn_base": 553,
    }
    with open(info_path, 'w') as f:
        json.dump(info, f, ensure_ascii=False, indent=2)

    print(f"\n✅ v1.7 国际数据合并完成！")
    print(f"   DNA: #龍芯⚡️丙午·辛未·乙酉·辰时·讼-INTL-TO-TRAIN-v1.0")


if __name__ == "__main__":
    main()
