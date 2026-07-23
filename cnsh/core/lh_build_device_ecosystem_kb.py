#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂设备生态知识库入库脚本
=============================
DNA: #龍芯⚡️2026-07-01-LONGHUN-DEVICE-ECOSYSTEM-KB-BUILD-v1.0

1. 读取 ~/.kimi-code/skills/longhun-device-ecosystem/data/device_kb.json
2. 写入 CS KB SQLite（longhun-system/backups/cs-kb-enhanced-20260701/cs_kb.db）
3. 生成长hun-system/knowledge/device-ecosystem/ Markdown 文档
4. 编入全局知识索引
5. 注册到技能内核注册表
"""

import hashlib
import json
import os
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

HOME = Path.home()
KB_PATH = HOME / ".kimi-code/skills/longhun-device-ecosystem/data/device_kb.json"
CS_KB_DB = HOME / "longhun-system/backups/cs-kb-enhanced-20260701/cs_kb.db"
KG_DIR = HOME / "longhun-system/knowledge/device-ecosystem"
GLOBAL_INDEX_SERVICE = HOME / ".longhun/scripts/global_index_service.py"
GLOBAL_INDEX_DB = HOME / ".longhun/global_index/global_index.db"
SKILL_REGISTRY = HOME / "longhun-system/data/forensic_kernel/skill_kernel_registry.json"

DNA_PREFIX = "#龍芯⚡️"


def _dna(主题: str) -> str:
    ts = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S%f")
    short = hashlib.sha256(f"{主题}:{ts}".encode()).hexdigest()[:8].upper()
    return f"{DNA_PREFIX}{ts}-{主题}-{short}"


def _dr(idx: int) -> str:
    drs = [
        "DR=6·木→震宫(东·木)",
        "DR=6·火→离宫(南·火)",
        "DR=6·土→中宫(中·土)",
        "DR=6·金→兑宫(西·金)",
        "DR=6·水→坎宫(北·水)",
    ]
    return drs[idx % len(drs)]


def load_kb():
    with open(KB_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def 写入_cs_kb(cards):
    conn = sqlite3.connect(str(CS_KB_DB))
    cur = conn.cursor()
    cur.execute('SELECT MAX(CAST(card_id AS INTEGER)) FROM cs_kb')
    start_id = (cur.fetchone()[0] or 0) + 1
    inserted = 0
    for i, card in enumerate(cards):
        cid = str(start_id + i)
        name = card["name"]
        row = {
            "card_id": cid,
            "name": name,
            "category": card.get("category", "设备生态"),
            "subcategory": card.get("subcategory", "通用"),
            "description": card.get("description", ""),
            "core_formula": "",
            "misconceptions": "; ".join(card.get("pitfalls", [])),
            "status": "已完成",
            "difficulty": "L2 进阶",
            "priority": "高优先级",
            "context_trigger": card.get("context_trigger", ""),
            "persona_route": json.dumps({"route": "设备生态工程师"}, ensure_ascii=False),
            "architecture_layer": "L4 应用层",
            "is_core": "是",
            "is_in_system": "是",
            "dr_wuxing_gong": _dr(i),
            "alpha_san yi": "",
            "short_dna": _dna(name),
            "ipa_abbr": card.get("ipa_abbr", ""),
            "tri_color_audit": "🟢可用🟡注意🔴需手动授权",
            "related_knowledge": "龍魂设备生态知识库 v1.0",
            "source_ref": _dna("CS-KB-" + name),
            "formula": "",
            "routing_params": json.dumps({
                "skill": "longhun-device-ecosystem",
                "module": "device_ecosystem_cli",
                "action": "search",
            }, ensure_ascii=False),
            "py_example": card.get("cli_example", "") + "\n# CNSH: " + card.get("cnsh_command", ""),
        }
        cols = ", ".join(f'"{k}"' for k in row.keys())
        placeholders = ", ".join(["?"] * len(row))
        cur.execute(f"INSERT OR REPLACE INTO cs_kb ({cols}) VALUES ({placeholders})", tuple(row.values()))
        inserted += 1
    conn.commit()
    conn.close()
    return inserted, start_id


def 生成_markdown_文档(cards):
    KG_DIR.mkdir(parents=True, exist_ok=True)
    paths = []
    overview = KG_DIR / "README.md"
    overview.write_text(
        f"""# 龍魂设备生态知识库

DNA: {_dna('device-ecosystem-overview')}

本目录汇总 iOS / macOS / 华为鸿蒙的真实设置路径、备份恢复、字体渲染、开发调试与操作坑位。
对应可执行 CLI 位于 `~/.kimi-code/skills/longhun-device-ecosystem/scripts/device_ecosystem_cli.py`。

## 核心原则

1. 不破解任何商业闭环，只做干净映射。
2. 权限弹窗、设备信任必须用户手动确认。
3. 本地备份优先，数据根留本机。
4. 中文语义命令 + 英文技术原名别名。

## 快速命令

```bash
python3 ~/.kimi-code/skills/longhun-device-ecosystem/scripts/device_ecosystem_cli.py version
python3 .../device_ecosystem_cli.py macos 电池
python3 .../device_ecosystem_cli.py ios 设备 列表
python3 .../device_ecosystem_cli.py huawei 检查
python3 .../device_ecosystem_cli.py 坑位 字体
python3 .../device_ecosystem_cli.py 搜索 备份密码
```
""",
        encoding="utf-8",
    )
    paths.append(overview)

    for card in cards:
        safe = card["name"].replace("/", "-").replace(":", "-")
        md_path = KG_DIR / f"{safe}.md"
        steps = "\n".join(f"{n+1}. {s}" for n, s in enumerate(card.get("plain_steps", [])))
        pitfalls = "\n".join(f"- ⚠️ {p}" for p in card.get("pitfalls", []))
        urls = ""
        if card.get("common_urls"):
            urls = "\n".join(f"- **{k}**: `{v}`" for k, v in card["common_urls"].items())
        md_path.write_text(
            f"""# {card['name']}

**DNA**: {_dna(card['name'])}
**分类**: {card['category']} / {card['subcategory']}
**英文缩写**: {card.get('ipa_abbr', '')}

## 定义

{card['description']}

## 触发场景

{card.get('context_trigger', '')}

## CNSH 命令

```text
{card.get('cnsh_command', '')}
```

## 操作步骤

{steps or '（无需额外步骤）'}

## CLI 示例

```bash
{card.get('cli_example', '# 见对应实现脚本')}
```

{('## 常用 URL\n\n' + urls) if urls else ''}

## 坑位提醒

{pitfalls or '- 暂无'}

## 相关链接

- 龍魂设备生态 CLI: `~/.kimi-code/skills/longhun-device-ecosystem/scripts/device_ecosystem_cli.py`
- 龍魂技能 SKILL.md: `~/.kimi-code/skills/longhun-device-ecosystem/SKILL.md`
""",
            encoding="utf-8",
        )
        paths.append(md_path)
    return paths


def 编入全局索引(文档路径列表):
    sys.path.insert(0, str(GLOBAL_INDEX_SERVICE.parent))
    import importlib.util
    spec = importlib.util.spec_from_file_location("global_index_service", GLOBAL_INDEX_SERVICE)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    cfg = mod.Config(mod.CONFIG_PATH)
    db = mod.Database(GLOBAL_INDEX_DB)
    rules = mod.ExclusionRules(cfg)
    extractor = mod.MediaExtractor(cfg)
    indexer = mod.Indexer(cfg, db, rules, extractor)

    root = str(HOME / "longhun-system")
    for p in 文档路径列表:
        indexer.index_file(Path(p), root, event_type="created")
    indexer.flush()
    return len(文档路径列表)


def _next_skill_id(registry):
    ids = [int(k.split("-")[1]) for k in registry.keys() if k.startswith("SKILL-") and k.split("-")[1].isdigit()]
    return f"SKILL-{max(ids, default=-1) + 1:04d}"


def 注册技能():
    if not SKILL_REGISTRY.exists():
        return None
    with open(SKILL_REGISTRY, "r", encoding="utf-8") as f:
        registry = json.load(f)

    skill_name = "longhun-device-ecosystem"
    # 若已存在则更新
    existing_key = None
    for k, v in registry.items():
        if v.get("技能名") == skill_name:
            existing_key = k
            break

    entry = {
        "id": existing_key or _next_skill_id(registry),
        "技能名": skill_name,
        "路径": str(HOME / ".kimi-code/skills/longhun-device-ecosystem/SKILL.md"),
        "作用域": "用户",
        "版本": "1.0",
        "描述": "龍魂设备生态知识库 — 汇总 iOS / macOS / 华为鸿蒙的真实设置路径、备份恢复、字体渲染、开发调试坑位，并提供 CNSH 风格一键 CLI。",
        "DNA": _dna("SKILL-" + skill_name),
        "来源": "skills",
        "关键词": [
            "device-ecosystem",
            "龍魂设备生态",
            "iOS 设置",
            "macOS 设置",
            "华为设置",
            "鸿蒙设置",
            "字体坑位",
            "渲染坑位",
            "备份命令",
            "idevicebackup2",
            "hdc",
            "操作坑位",
        ],
        "入口": "python3 ~/.kimi-code/skills/longhun-device-ecosystem/scripts/device_ecosystem_cli.py",
        "优先级": 50,
        "状态": "已注册",
        "评分": 50.0,
        "使用次数": 0,
        "成功次数": 0,
        "失败次数": 0,
        "审计状态": "未审计",
        "注册时间": datetime.now(timezone.utc).isoformat(),
    }

    if existing_key:
        registry[existing_key] = entry
        key = existing_key
    else:
        registry[entry["id"]] = entry
        key = entry["id"]

    with open(SKILL_REGISTRY, "w", encoding="utf-8") as f:
        json.dump(registry, f, ensure_ascii=False, indent=2)
    return key


def main():
    print(f"\n{'='*60}")
    print("  龍魂设备生态知识库入库")
    print(f"  DNA: {_dna('build-device-ecosystem-kb')}")
    print(f"{'='*60}\n")

    data = load_kb()
    cards = data.get("cards", [])

    inserted, start_id = 写入_cs_kb(cards)
    print(f"🟢 CS KB 写入 {inserted} 张知识卡片，起始 ID: {start_id}")

    paths = 生成_markdown_文档(cards)
    print(f"🟢 生成 {len(paths)} 篇 Markdown 知识文档: {KG_DIR}")

    indexed = 编入全局索引(paths)
    print(f"🟢 编入全局索引 {indexed} 个文件")

    skill_key = 注册技能()
    print(f"🟢 技能注册: {skill_key}")

    print(f"\n{'='*60}")
    print("  完成。可执行验证：")
    print("  python3 ~/.kimi-code/skills/longhun-device-ecosystem/scripts/device_ecosystem_cli.py version")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
