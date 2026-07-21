#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
通心译 v2.0 + 龍魂标签 + CNSH 变量知识入库脚本
=================================================
DNA: #龍芯⚡️2026-07-01-LONGHUN-TONGXINYI-V2-KB-BUILD-v1.0

1. 向 CS KB 写入通心译 v2.0、龍魂标签体系、CNSH 变量与龍魂字体知识卡片
2. 在 longhun-system/knowledge/tongxinyi-v2/ 生成 Markdown 文档
3. 编入全局索引
4. 更新技能注册表 SKILL-0014 到 v2.0
"""

import hashlib
import json
import os
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

HOME = Path.home()
CS_KB_DB = HOME / "longhun-system/backups/cs-kb-enhanced-20260701/cs_kb.db"
KG_DIR = HOME / "longhun-system/knowledge/tongxinyi-v2"
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
        "DR=3·木→震宫(东·木)",
        "DR=3·火→离宫(南·火)",
        "DR=3·土→中宫(中·土)",
        "DR=3·金→兑宫(西·金)",
        "DR=3·水→坎宫(北·水)",
    ]
    return drs[idx % len(drs)]


知识卡片清单 = [
    {
        "name": "通心译 v2.0 语义心意映射引擎",
        "category": "龍魂语义",
        "subcategory": "通心译",
        "description": "通心译不是传统 NMT，而是语义心意映射引擎。输入人话、情绪、碎片后，输出 L0-L5 六层结构与可执行意图骨架，并附带三色审计。",
        "context_trigger": "通心译、先翻译再执行、意图识别、情绪净化、人话转可执行结构",
        "ipa_abbr": "Tongxin Translation v2.0",
        "cli_example": "python3 ~/.kimi-code/skills/longhun-tongxinyi/scripts/tongxin_cli.py translate \"画龍点睛\"",
    },
    {
        "name": "三层语义传递（字面/逻辑/心意）",
        "category": "龍魂语义",
        "subcategory": "通心译",
        "description": "字面层保留术语与语法；逻辑层推导语义蕴含与语篇连贯；心意层映射文化意图、意象与文明安全评分。三层相互约束，防止断章取义。",
        "context_trigger": "三层语义、字面层、逻辑层、心意层、文化意图、意象映射",
        "ipa_abbr": "Tri-Layer Transfer",
        "cli_example": "python3 ~/.kimi-code/skills/longhun-tongxinyi/scripts/tongxin_cli.py eval --limit 3",
    },
    {
        "name": "七维训练维度与 R-Score",
        "category": "龍魂语义",
        "subcategory": "通心译",
        "description": "通心译 v2.0 将翻译质量拆为 D1-D7 七个维度：文化负载词、语义-语法、古代汉语、语篇完整、文明安全、创造性策略、语义精确。R-Score = Σ(w_i×Dim_i) + 创造性奖励 - 安全惩罚。",
        "context_trigger": "七维评估、R-Score、D1-D7、翻译质量、文明安全评分",
        "ipa_abbr": "R-Score / D1-D7",
        "cli_example": "python3 ~/.kimi-code/skills/longhun-tongxinyi/scripts/tongxin_v2.py",
    },
    {
        "name": "龍魂文化标签体系 v1.0",
        "category": "龍魂文化标签",
        "subcategory": "标签总览",
        "description": "龍魂文化标签体系用于替代西方 emoji，覆盖状态、情绪、功能、等级、系统组件。共 112 个标签：五行 20 + 八卦 24 + 甲骨文 40 + 二十八星宿 28。",
        "context_trigger": "龍魂标签、文化标签、替代 emoji、五行标签、八卦标签、甲骨文、星宿",
        "ipa_abbr": "LongHun Tag System",
        "cli_example": "python3 ~/.kimi-code/skills/longhun-tongxinyi/scripts/tongxin_cli.py tag 火·旺 HTML",
    },
    {
        "name": "五行标签（20 变体）",
        "category": "龍魂文化标签",
        "subcategory": "五行",
        "description": "金木水火土 × 生旺休囚 = 20 个标签。每个标签含 Unicode 字符、颜色 hex、使用场景与代码（如 METAL_PEAK）。支持五行生克组合验证。",
        "context_trigger": "五行标签、金木水火土、生旺休囚、五行生克、METAL_PEAK",
        "ipa_abbr": "Wuxing Tags",
        "cli_example": "python3 ~/.kimi-code/skills/longhun-tongxinyi/scripts/tongxin_cli.py tag-combo 木 火",
    },
    {
        "name": "八卦标签（24 变体）",
        "category": "龍魂文化标签",
        "subcategory": "八卦",
        "description": "乾坤震巽坎离艮兑 × 正反动 = 24 个标签。映射现代系统状态：stable/degraded/alert、starting/failed/urgent、connected/disconnected/high_freq 等。",
        "context_trigger": "八卦标签、乾坤震巽坎离艮兑、正反动、系统状态",
        "ipa_abbr": "Bagua Tags",
        "cli_example": "python3 ~/.kimi-code/skills/longhun-tongxinyi/scripts/tongxin_cli.py tag-search 系统",
    },
    {
        "name": "甲骨文标签（40 字）",
        "category": "龍魂文化标签",
        "subcategory": "甲骨文",
        "description": "精选 40 个甲骨文字，分状态（启止行立生等）、情绪（喜怒哀乐恐等）、功能（见闻言思守等）、等级（上中下大小等）四类，每个字有 Unicode、拼音、现代映射与颜色。",
        "context_trigger": "甲骨文标签、甲骨文字、状态情绪功能等级、Unicode",
        "ipa_abbr": "Oracle Bone Tags",
        "cli_example": "python3 ~/.kimi-code/skills/longhun-tongxinyi/scripts/longhun_tags.py",
    },
    {
        "name": "二十八星宿标签（28 宿）",
        "category": "龍魂文化标签",
        "subcategory": "星宿",
        "description": "东方青龍、北方玄武、西方白虎、南方朱雀各七宿，共 28 个标签。映射初始化、防御、存储、调度、计算、风险、缓存、完成等系统组件与阶段。",
        "context_trigger": "二十八星宿、青龍白虎朱雀玄武、星宿标签、系统组件",
        "ipa_abbr": "28 Xiu Tags",
        "cli_example": "python3 ~/.kimi-code/skills/longhun-tongxinyi/scripts/tongxin_cli.py tag-search 调度",
    },
    {
        "name": "CNSH 变量注册表",
        "category": "龍魂语义",
        "subcategory": "CNSH 变量",
        "description": "统一变量命名：`@@tongxin.*` 表示通心译层与七维评分，`@@tag.*` 表示标签体系，`@@font.*` 表示龍魂字体路径/仓库。所有渲染、脚本、文档统一引用这些变量，避免硬编码。",
        "context_trigger": "CNSH 变量、@@变量、通心译变量、标签变量、字体变量、统一命名",
        "ipa_abbr": "CNSH Variables",
        "cli_example": "python3 ~/.kimi-code/skills/longhun-tongxinyi/scripts/tongxin_cli.py var @@tongxin.r_score",
    },
    {
        "name": "龍魂字体注册表",
        "category": "龍魂文化标签",
        "subcategory": "字体渲染",
        "description": "龍魂中文字体 LonghunFont v0019 已开源（SIL OFL 1.1），本地输出文件包括 Regular、WuwuColor、v3 试验版。注册表变量 `@@font.longhun.*` 指向本地路径与 Gitee/GitHub 仓库。",
        "context_trigger": "龍魂字体、LonghunFont、字体注册表、WuwuColor、中文字体、文化主权字体",
        "ipa_abbr": "LonghunFont",
        "cli_example": "python3 ~/.kimi-code/skills/longhun-tongxinyi/scripts/tongxin_cli.py font",
    },
]


def 写入_cs_kb():
    conn = sqlite3.connect(str(CS_KB_DB))
    cur = conn.cursor()
    cur.execute('SELECT MAX(CAST(card_id AS INTEGER)) FROM cs_kb')
    start_id = (cur.fetchone()[0] or 0) + 1
    inserted = 0
    for i, card in enumerate(知识卡片清单):
        cid = str(start_id + i)
        name = card["name"]
        row = {
            "card_id": cid,
            "name": name,
            "category": card.get("category", "龍魂语义"),
            "subcategory": card.get("subcategory", "通心译"),
            "description": card.get("description", ""),
            "core_formula": "",
            "misconceptions": "",
            "status": "已完成",
            "difficulty": "L2 进阶",
            "priority": "高优先级",
            "context_trigger": card.get("context_trigger", ""),
            "persona_route": json.dumps({"route": "通心译语义工程师"}, ensure_ascii=False),
            "architecture_layer": "L1 语义层",
            "is_core": "是",
            "is_in_system": "是",
            "dr_wuxing_gong": _dr(i),
            "alpha_san yi": "",
            "short_dna": _dna(name),
            "ipa_abbr": card.get("ipa_abbr", ""),
            "tri_color_audit": "🟢可用🟡注意🔴需文化立场校准",
            "related_knowledge": "通心译 v2.0 + 龍魂标签体系",
            "source_ref": _dna("CS-KB-" + name),
            "formula": "",
            "routing_params": json.dumps({
                "skill": "longhun-tongxinyi",
                "module": "tongxin_cli",
                "action": "translate",
            }, ensure_ascii=False),
            "py_example": card.get("cli_example", ""),
        }
        cols = ", ".join(f'"{k}"' for k in row.keys())
        placeholders = ", ".join(["?"] * len(row))
        cur.execute(f"INSERT OR REPLACE INTO cs_kb ({cols}) VALUES ({placeholders})", tuple(row.values()))
        inserted += 1
    conn.commit()
    conn.close()
    return inserted, start_id


def 生成_markdown_文档():
    KG_DIR.mkdir(parents=True, exist_ok=True)
    paths = []
    overview = KG_DIR / "README.md"
    overview.write_text(
        f"""# 通心译 v2.0 + 龍魂标签 + CNSH 变量知识库

DNA: {_dna('tongxinyi-v2-overview')}

本目录汇总通心译 v2.0 语义引擎、龍魂文化标签体系、CNSH 变量与龍魂字体注册表。
对应可执行 CLI 位于 `~/.kimi-code/skills/longhun-tongxinyi/scripts/tongxin_cli.py`。

## 核心原则

1. 先翻译再执行：把 UID9622 的人话转成可执行意图骨架。
2. 三层语义：字面 / 逻辑 / 心意，层层约束。
3. 中文文化标签替代西方 emoji，服务于龍魂渲染。
4. CNSH 变量统一命名：`@@tongxin.*`、`@@tag.*`、`@@font.*`。

## 快速命令

```bash
python3 ~/.kimi-code/skills/longhun-tongxinyi/scripts/tongxin_cli.py translate "画龍点睛"
python3 .../tongxin_cli.py eval --limit 5
python3 .../tongxin_cli.py tag 火·旺 HTML
python3 .../tongxin_cli.py tag-search 启动
python3 .../tongxin_cli.py var @@tongxin.r_score
python3 .../tongxin_cli.py font
```
""",
        encoding="utf-8",
    )
    paths.append(overview)

    for card in 知识卡片清单:
        safe = card["name"].replace("/", "-").replace(" ", "_")
        md_path = KG_DIR / f"{safe}.md"
        md_path.write_text(
            f"""# {card['name']}

**DNA**: {_dna(card['name'])}
**分类**: {card['category']} / {card['subcategory']}
**英文缩写**: {card.get('ipa_abbr', '')}

## 定义

{card['description']}

## 触发场景

{card.get('context_trigger', '')}

## CLI 示例

```bash
{card.get('cli_example', '# 见对应实现脚本')}
```

## 相关链接

- 通心译 v2.0 + 标签 CLI: `~/.kimi-code/skills/longhun-tongxinyi/scripts/tongxin_cli.py`
- 龍魂技能 SKILL.md: `~/.kimi-code/skills/longhun-tongxinyi/SKILL.md`
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


def 更新技能注册表():
    if not SKILL_REGISTRY.exists():
        return None
    with open(SKILL_REGISTRY, "r", encoding="utf-8") as f:
        registry = json.load(f)

    key = "SKILL-0014"
    if key not in registry:
        return None

    entry = registry[key]
    entry["版本"] = "2.0"
    entry["描述"] = (
        "龍魂前置翻译技能·通心译 v2.0。先翻译再执行、贴身常驻、钻石主干合并、M248 焊点。"
        "六层框架 + 九状态机 + 213 协议 + 55 抽屉 + 7 条铁律。"
        "新增通心译 v2.0 七维评估、龍魂文化标签体系（112 标签）、CNSH 变量/龍魂字体注册表。"
    )
    entry["DNA"] = _dna("SKILL-longhun-tongxinyi-v2.0")
    entry["关键词"] = [
        "通心译", "tongxinyi", "前置翻译", "意图识别", "情绪净化",
        "213协议", "M248", "CNSH-DOC", "七维评估", "龍魂标签",
        "CNSH变量", "龍魂字体", "translate-before-execute",
    ]
    entry["入口"] = "python3 ~/.kimi-code/skills/longhun-tongxinyi/scripts/tongxin_cli.py"
    entry["注册时间"] = datetime.now(timezone.utc).isoformat()

    with open(SKILL_REGISTRY, "w", encoding="utf-8") as f:
        json.dump(registry, f, ensure_ascii=False, indent=2)
    return key


def main():
    print(f"\n{'='*60}")
    print("  通心译 v2.0 + 龍魂标签 + CNSH 变量知识入库")
    print(f"  DNA: {_dna('build-tongxinyi-v2-kb')}")
    print(f"{'='*60}\n")

    inserted, start_id = 写入_cs_kb()
    print(f"🟢 CS KB 写入 {inserted} 张知识卡片，起始 ID: {start_id}")

    paths = 生成_markdown_文档()
    print(f"🟢 生成 {len(paths)} 篇 Markdown 知识文档: {KG_DIR}")

    indexed = 编入全局索引(paths)
    print(f"🟢 编入全局索引 {indexed} 个文件")

    key = 更新技能注册表()
    print(f"🟢 技能注册表更新: {key}")

    print(f"\n{'='*60}")
    print("  完成。可执行验证：")
    print("  python3 ~/.kimi-code/skills/longhun-tongxinyi/scripts/tongxin_cli.py version")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
