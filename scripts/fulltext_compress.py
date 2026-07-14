#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UID9622 全文压缩系统 - 本地最小可执行版
LU-FULLTEXT-COMPRESS-AUTO-COLLECT v1.1 - Local Demo

DNA:#龍芯⚡️2026-06-03-FULLTEXT-COMPRESS-LOCAL-v1.0
用法: python3 fulltext_compress.py input.txt
输出:
  - input.compress.md     (压缩卡)
  - input.compress.json   (机器结构)
  - input.shortcode       (短码)
"""

import sys
import json
import hashlib
from datetime import datetime
from pathlib import Path


def generate_shortcode(content: str) -> str:
    """生成短码（用内容的前20个字符 + hash8位）"""
    prefix = content[:20].replace("\n", "").replace(" ", "")[:10]
    hash_val = hashlib.md5(content.encode()).hexdigest()[:8]
    return f"COMPRESS-{datetime.now().strftime('%Y%m%d')}-{prefix}-{hash_val}".upper()


def extract_skeleton(content: str) -> dict:
    """提取骨架（问题、结论、方法、行动、下一步）"""
    lines = content.split('\n')

    # 简单启发式：找有号的行
    skeleton = {
        "problem": "",
        "solution": "",
        "key_points": [],
        "next_action": "",
        "context": ""
    }

    current_section = "context"

    for line in lines:
        line = line.strip()
        if not line:
            continue

        if any(kw in line for kw in ["问题", "Problem", "Issue", "错误"]):
            current_section = "problem"
        elif any(kw in line for kw in ["方案", "Solution", "解决", "方法"]):
            current_section = "solution"
        elif any(kw in line for kw in ["下一步", "Next", "Action", "TODO"]):
            current_section = "next_action"
        elif line.startswith("-") or line.startswith("*"):
            skeleton["key_points"].append(line.lstrip("-*").strip())
            continue

        if current_section == "problem":
            skeleton["problem"] += line + "\n"
        elif current_section == "solution":
            skeleton["solution"] += line + "\n"
        elif current_section == "next_action":
            skeleton["next_action"] += line + "\n"
        else:
            skeleton["context"] += line + "\n"

    # 清理
    for key in skeleton:
        if isinstance(skeleton[key], str):
            skeleton[key] = skeleton[key].strip()

    return skeleton


def generate_compress_card(content: str, shortcode: str, skeleton: dict) -> str:
    """生成Markdown压缩卡"""

    # 一句话压缩
    first_line = content.split('\n')[0].strip()
    if len(first_line) > 100:
        one_liner = first_line[:100] + "..."
    else:
        one_liner = first_line

    # 核心结论（前3个有意义的句子）
    conclusions = []
    for line in content.split('\n'):
        line = line.strip()
        if line and len(line) > 10 and not line.startswith("#"):
            conclusions.append(line)
            if len(conclusions) >= 3:
                break

    card = f"""【UID9622全文压缩卡】

**标题**: {one_liner}

**来源**: 本地输入

**时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S CST')}

**短码**: /{shortcode}

---

## 一｜一句话压缩

{one_liner}

---

## 二｜核心结论

1. {conclusions[0] if len(conclusions) > 0 else "（暂无）"}
2. {conclusions[1] if len(conclusions) > 1 else "（暂无）"}
3. {conclusions[2] if len(conclusions) > 2 else "（暂无）"}

---

## 三｜核心骨架

### 背景
{skeleton['context'][:200] or "（暂无）"}

### 问题
{skeleton['problem'][:200] or "（暂无）"}

### 方案
{skeleton['solution'][:200] or "（暂无）"}

### 关键点
{chr(10).join(f"- {pt}" for pt in skeleton['key_points'][:5]) or "- （暂无）"}

### 下一步
{skeleton['next_action'][:200] or "（暂无）"}

---

## 四｜系统分类

- **语义抽屉**: 通用
- **八卦分类**: 待确认
- **三色判定**: 🟢 可召回
- **项目模块**: 未分配
- **风险等级**: 低
- **状态**: 已压缩·可召回

---

## 五｜机器结构

见 `{shortcode}.json`

---

## 六｜短码

```
/{shortcode}
```

---

DNA: #龍芯⚡️{datetime.now().strftime('%Y-%m-%d')}-FULLTEXT-COMPRESS-v1.0
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
审计: 🟢 通过
"""
    return card


def generate_machine_structure(content: str, shortcode: str, skeleton: dict) -> dict:
    """生成M::机器结构"""

    structure = {
        "schemaVersion": "lu-fulltext-compress/v1.1",
        "id": f"M::{shortcode}",
        "type": "compress-card",
        "ts": datetime.now().isoformat(),
        "status": "active",
        "payload": {
            "summary": content[:200],
            "source": "local_input",
            "shortcode": shortcode,
            "skeleton": skeleton,
            "word_count": len(content),
            "line_count": len(content.split('\n'))
        },
        "meta": {
            "dna": f"#龍芯⚡️{datetime.now().strftime('%Y-%m-%d')}-FULLTEXT-COMPRESS-v1.0",
            "gate": "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z",
            "seal": "#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL",
            "audit": "🟢",
            "route": "IPA-FULLTEXT-COMPRESS"
        }
    }

    return structure


def main():
    """主入口"""

    if len(sys.argv) < 2:
        print("❌ 用法: python3 fulltext_compress.py <input_file>")
        print("例: python3 fulltext_compress.py long_text.txt")
        sys.exit(1)

    input_file = Path(sys.argv[1])

    if not input_file.exists():
        print(f"❌ 文件不存在: {input_file}")
        sys.exit(1)

    print(f"📖 读取文件: {input_file}")
    content = input_file.read_text(encoding='utf-8')

    if len(content) < 10:
        print("❌ 文件内容太短")
        sys.exit(1)

    print(f"✅ 读取成功，{len(content)} 字符")

    # 生成短码
    shortcode = generate_shortcode(content)
    print(f"✅ 生成短码: /{shortcode}")

    # 提取骨架
    skeleton = extract_skeleton(content)
    print(f"✅ 提取骨架: {len(skeleton)} 个字段")

    # 生成压缩卡
    card_md = generate_compress_card(content, shortcode, skeleton)
    card_file = input_file.with_suffix('.compress.md')
    card_file.write_text(card_md, encoding='utf-8')
    print(f"✅ 压缩卡: {card_file}")

    # 生成机器结构
    machine = generate_machine_structure(content, shortcode, skeleton)
    machine_file = input_file.with_suffix('.compress.json')
    machine_file.write_text(json.dumps(machine, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f"✅ 机器结构: {machine_file}")

    # 生成短码文件
    shortcode_file = input_file.with_suffix('.shortcode')
    shortcode_file.write_text(f"/{shortcode}\n", encoding='utf-8')
    print(f"✅ 短码文件: {shortcode_file}")

    print("\n" + "="*50)
    print(f"📦 压缩完成！")
    print(f"   卡片: {card_file}")
    print(f"   机器: {machine_file}")
    print(f"   短码: /{shortcode}")
    print("="*50)


if __name__ == '__main__':
    main()
