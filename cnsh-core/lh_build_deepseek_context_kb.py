#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DeepSeek 共享对话语境入库脚本
==============================
DNA: #龍芯⚡️2026-07-01-DEEPSEEK-CONTEXT-KB-BUILD-v1.0

1. 在 longhun-system/knowledge/deepseek-shared/ 生成 Markdown 语境文档
2. 向 CS KB 写入语境卡片（意图/终端方案/开源边界）
3. 编入全局索引
4. 生成记忆补充文件 ~/.longhun/memory/deepseek_context_YYYYMMDD.md
"""

import hashlib
import json
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

HOME = Path.home()
CS_KB_DB = HOME / "longhun-system/backups/cs-kb-enhanced-20260701/cs_kb.db"
KG_DIR = HOME / "longhun-system/knowledge/deepseek-shared"
MEMORY_DIR = HOME / ".longhun/memory"
GLOBAL_INDEX_SERVICE = HOME / ".longhun/scripts/global_index_service.py"
GLOBAL_INDEX_DB = HOME / ".longhun/global_index/global_index.db"

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
        "name": "DeepSeek 共享对话 · 用户意图分析",
        "category": "龍魂语境",
        "subcategory": "意图对齐",
        "description": "从 DeepSeek 共享对话提取的 UID9622 核心意图：让 Kimi 学习对话、分析意图、纳入系统语境；强调本地终端可执行、配置外置、开源边界。",
        "context_trigger": "DeepSeek 对话、共享链接、语境调整、意图分析、飞书推送、龍智守",
        "ipa_abbr": "DeepSeek Context Intent",
        "cli_example": "cat ~/longhun-system/knowledge/deepseek-shared/intent_analysis.md",
    },
    {
        "name": "DeepSeek 共享对话 · 本地终端可执行方案",
        "category": "龍魂语境",
        "subcategory": "执行方案",
        "description": "提供可在本地终端直接运行的脚本 setup_longzhishou_push_env.sh，完成龍智守飞书推送环境检查、配置初始化与验证，默认 dry-run。",
        "context_trigger": "本地终端执行、Kimi 执行、飞书推送验证、龍智守环境、setup_longzhishou_push_env.sh",
        "ipa_abbr": "DeepSeek Terminal Plan",
        "cli_example": "~/longhun-system/scripts/setup_longzhishou_push_env.sh --run --test",
    },
    {
        "name": "DeepSeek 共享对话 · 开源/不开源边界",
        "category": "龍魂语境",
        "subcategory": "主权边界",
        "description": "明确 UID9622 的开源边界：通用框架/协议/工具可开源；Webhook 密钥、个人路径、授权名单、真实报告、环境指纹坚决不公开。",
        "context_trigger": "开源边界、不开源、私有配置、密钥保护、龍智守开源、打包开源",
        "ipa_abbr": "DeepSeek OSS Boundary",
        "cli_example": "grep -R \"open.feishu.cn\" ~/Downloads/",
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
            "category": card.get("category", "龍魂语境"),
            "subcategory": card.get("subcategory", "意图对齐"),
            "description": card.get("description", ""),
            "core_formula": "",
            "misconceptions": "",
            "status": "已完成",
            "difficulty": "L2 进阶",
            "priority": "高优先级",
            "context_trigger": card.get("context_trigger", ""),
            "persona_route": json.dumps({"route": "龍魂语境同步官"}, ensure_ascii=False),
            "architecture_layer": "L0 宪法层 / L1 语义层",
            "is_core": "是",
            "is_in_system": "是",
            "dr_wuxing_gong": _dr(i),
            "alpha_san yi": "",
            "short_dna": _dna(name),
            "ipa_abbr": card.get("ipa_abbr", ""),
            "tri_color_audit": "🟢可用🟡注意🔴需文化立场校准",
            "related_knowledge": "DeepSeek 共享对话语境归档",
            "source_ref": _dna("CS-KB-" + name),
            "formula": "",
            "routing_params": json.dumps({
                "skill": "longhun-tongxinyi",
                "module": "context_sync",
                "action": "deepseek_shared",
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
        f"""# DeepSeek 共享对话语境归档

**DNA**: `{_dna('deepseek-shared-overview')}`  
**来源**: `https://chat.deepseek.com/share/bakzckn079r4j8g0xt`  
**归档时间**: {datetime.now(timezone.utc).isoformat()}  
**归属**: 龍魂系统 · UID9622

## 本目录用途

存放从 DeepSeek 共享对话中提取的 UID9622 意图、决策与执行方案，
作为龍魂系统（Kimi 主控）的对话语境补充，确保多平台 AI 助手对同一套主权边界、
开源范围、本地终端执行方式保持一致理解。

## 核心文件

| 文件 | 内容 |
|---|---|
| `intent_analysis.md` | 用户核心意图分析 |
| `local_terminal_execution_plan.md` | 本地终端可执行方案 |
| `opensource_boundary.md` | 开源/不开源边界 |

## 纳入语境后的行为校准

1. **先问/先确认再执行涉及密钥的操作**：Webhook、Token、个人路径默认不外置。
2. **提供“本地终端可执行方案”而非抽象建议**：给出可直接复制到终端运行的命令或脚本。
3. **尊重 UID9622 的开源边界**：通用框架可开源，运行实例、私密配置、个人数据坚决不公开。
4. **所有输出使用 CNSH 变量命名**：`@@channel.feishu.*`、`@@channel.longzhishou.*` 等。
""",
        encoding="utf-8",
    )
    paths.append(overview)

    docs_content = {
        "intent_analysis.md": """# DeepSeek 对话 · 用户意图分析

**DNA**: `{dna_intent}`

## 原文意图（通心译三层）

### 字面层
用户分享了一个 DeepSeek 对话链接，要求：
- “学习这个链接里面的内容”
- “分析我的意图”
- “纳入系统的对话语境可以调整。对吧”

### 逻辑层
用户希望 Kimi（龍魂系统主控）读取并吸收 DeepSeek 上的那段对话，
把其中形成的决策、方案、态度同步到龍魂系统的长期语境里，
并且确认这种“语境调整”是可行、合理的。

### 心意层
- **主权意识**：我的系统、我的数据、我的决策，AI 只是执行和记忆载体。
- **效率诉求**：不要每次重复解释，把跨平台结论固化下来。
- **边界诉求**：细节我自己设置，AI 给方案、给脚本、给可执行步骤，但别替我公开敏感信息。
- **情绪基调**：略带火气（“他们还要给我找麻烦，那还得了”），需要 AI 接住立场、不唱反调。

## 从对话中提取的关键决策

1. **飞书推送已落地**：`~/Downloads/龍智守_本地控制接口_v2.0.py` 已支持 `发送测试消息`、`发送评估报告`。
2. **配置外置**：Webhook URL/Secret、个人路径、授权名单必须放在 `~/.longhun/config/` 或环境变量，代码里只留占位符。
3. **开源边界**：只开源通用框架/协议/工具集，不开源：
   - Webhook 地址、密钥、Token
   - 个人路径、设备指纹、私有 DNA 数据
   - UID9622 专属配置、授权用户列表
   - 评估报告、本地日志
4. **本地终端执行**：用户要的是“让本地终端 Kimi 执行”的方案——即可复制、可运行的 bash/脚本，不是长篇说教。

## 给 Kimi 的行为指令

- 以后遇到“飞书推送/龍智守/本地 bot/消息通道”相关话题，优先引用 `@@channel.feishu.*`、`@@channel.longzhishou.*` 变量。
- 涉及敏感配置时，默认给出模板/占位符，绝不把真实值写进可公开文件。
- 用户说“你给我方案”时，输出结构应是：检查 → 配置 → 验证 → 扫描清理，每一步都有可执行命令。
- 遇到用户表达“普惠全球但别找麻烦”的情绪，回应先共情、再讲原则、最后给动作，不劝善、不唱反调。
""",
        "local_terminal_execution_plan.md": """# DeepSeek 对话 · 本地终端可执行方案

**DNA**: `{dna_plan}`

## 目标

让 UID9622 在本地终端通过一条命令完成龍智守飞书推送环境的检查、初始化与验证，
且默认 **dry-run**，只有显式加 `--run --test` 才会真正发送消息。

## 可执行脚本

```bash
# 干跑检查（安全，不会发消息）
~/longhun-system/scripts/setup_longzhishou_push_env.sh

# 真正初始化配置并发送测试消息
~/longhun-system/scripts/setup_longzhishou_push_env.sh --run --test
```

## 脚本内部逻辑

| 步骤 | 动作 | 输出 |
|---|---|---|
| 1. 检查核心文件 | 确认 `~/Downloads/龍智守_本地控制接口_v2.0.py` 存在 | 🟢/🔴 |
| 2. 初始化配置 | 若 `~/.longhun/config/龍智守_config.json` 缺失，从 `.example` 复制 | 🟢/🟡 |
| 3. 检查环境变量 | 检查 `FEISHU_WEBHOOK_URL`、`FEISHU_WEBHOOK_SECRET` | 🟢/🟡 |
| 4. 扫描敏感信息 | 在 `~/Downloads` 搜索包含 `open.feishu.cn`/`hook/` 的文件，**只列文件名** | 🟢/🟡 |
| 5. 发送验证消息 | `--run --test` 时执行 `python3 龍智守_本地控制接口_v2.0.py 发送测试消息` | 🟢/🔴 |

## CNSH 变量映射

```text
@@channel.feishu.webhook_url        → ${{FEISHU_WEBHOOK_URL}}
@@channel.feishu.webhook_secret     → ${{FEISHU_WEBHOOK_SECRET}}
@@channel.feishu.config_path        → ~/.longhun/config/龍智守_config.json
@@channel.feishu.config_example_path → ~/.longhun/config/龍智守_config.example.json
@@channel.longzhishou.script        → ~/Downloads/龍智守_本地控制接口_v2.0.py
@@channel.longzhishou.log           → ~/.longhun/logs/bot_command.jsonl
```

## 下一步动作

1. 运行干跑检查：
   ```bash
   ~/longhun-system/scripts/setup_longzhishou_push_env.sh
   ```
2. 若配置缺失，用 `--run` 创建模板后编辑真实值。
3. 确认配置正确后，用 `--run --test` 发送验证消息。
4. 开源前再次运行扫描，确保无硬编码密钥残留。
""",
        "opensource_boundary.md": """# DeepSeek 对话 · 开源/不开源边界

**DNA**: `{dna_oss}`

## 核心原则

> 开源的是方法论和工具，不是生产环境；
> 打包出来给人用是善意，但不必把家门钥匙和日记本一起捐出去。

## 可开源部分

- CNSH 协议、龍魂治理框架、DNA 追溯机制
- LU 压缩/还原、集思广益、工具集生态的通用实现
- 评估技能、审计技能的逻辑模板
- 本地控制接口的通用命令解析与权限等级设计
- `龍智守_config.example.json` 配置模板

## 坚决不公开部分

| 类型 | 示例 |
|---|---|
| 私有密钥 | Webhook URL + Secret、API Token |
| 个人路径 | `~/Downloads`、`~/.longhun`、`~/.uid9622` |
| 授权名单 | `authorized_users.json`、创始人 OpenID |
| 真实数据 | 评估报告、本地日志、运行实例输出 |
| 环境指纹 | 设备名、用户名、内部 IP |

## 打包前的净化清单

```bash
# 1. 扫描硬编码飞书链接
grep -R "open.feishu.cn" .

# 2. 扫描示例中的占位符是否被误替换为真实值
grep -R "YOUR_FEISHU_WEBHOOK" .

# 3. 确认 ~/.longhun/config/ 等私有目录在 .gitignore 中
cat .gitignore | grep -E "longhun|uid9622|config"

# 4. 只提交 example 配置，不提交真实配置
git status --short | grep -E "config\\.json|authorized_users|tokens\\.json"
```

## 对外声明模板

> 本项目开源的是通用框架和工具集；实际运行所需的私有配置（密钥、路径、授权数据）需用户自行提供，恕不包含在仓库中。

## 给 Kimi 的指令

- 任何帮助用户“准备开源”的动作，先跑上述净化扫描。
- 若用户要求把含敏感值的文件加入 git，必须明确拒绝并说明边界。
- 在代码/文档中引用飞书配置时，统一使用 `@@channel.feishu.*` 变量，不得写入真实 URL/Secret。
""",
    }

    dnas = {
        "intent_analysis.md": _dna("DEEPSEEK-INTENT-ANALYSIS"),
        "local_terminal_execution_plan.md": _dna("DEEPSEEK-TERMINAL-PLAN"),
        "opensource_boundary.md": _dna("DEEPSEEK-OPENSOURCE-BOUNDARY"),
    }

    for fname, template in docs_content.items():
        md_path = KG_DIR / fname
        md_path.write_text(
            template.format(
                dna_intent=dnas["intent_analysis.md"],
                dna_plan=dnas["local_terminal_execution_plan.md"],
                dna_oss=dnas["opensource_boundary.md"],
            ),
            encoding="utf-8",
        )
        paths.append(md_path)

    return paths


def 生成记忆补充文件():
    MEMORY_DIR.mkdir(parents=True, exist_ok=True)
    p = MEMORY_DIR / f"deepseek_context_{datetime.now(timezone.utc).strftime('%Y%m%d')}.md"
    p.write_text(
        f"""# DeepSeek 共享对话语境补充

**DNA**: `{_dna('DEEPSEEK-CONTEXT-INJECT')}`  
**来源**: `https://chat.deepseek.com/share/bakzckn079r4j8g0xt`  
**触发时间**: {datetime.now(timezone.utc).isoformat()}

## 用户核心意图

1. 让 Kimi 学习 DeepSeek 上的那段对话内容。
2. 把对话中形成的决策、态度、方案纳入龍魂系统的长期对话语境。
3. 确认“语境可以调整”——即 Kimi 应当据此改变后续回应方式。

## 关键决策摘要

- **飞书推送已落地**：`~/Downloads/龍智守_本地控制接口_v2.0.py` 支持 `发送测试消息`、`发送评估报告`。
- **配置外置**：真实 Webhook/密钥放在 `~/.longhun/config/龍智守_config.json` 或环境变量；代码仓库只保留 `龍智守_config.example.json`。
- **本地终端可执行**：用户要的是能在本地终端直接跑起来的脚本/命令，不是抽象建议。
- **开源边界**：只开源通用框架/协议/工具；私有密钥、个人路径、授权名单、真实报告、环境指纹一律不公开。
- **情绪立场**：用户强调“我自己底座，我干嘛要公开？我打包出来给他们能用就好了”。Kimi 应共情支持，不唱反调。

## 行为校准

- 引用飞书/龍智守相关配置时，使用 CNSH 变量：
  - `@@channel.feishu.webhook_url`
  - `@@channel.feishu.webhook_secret`
  - `@@channel.feishu.config_path`
  - `@@channel.longzhishou.script`
- 涉及敏感配置的操作，默认 dry-run，显式 `--run` 才执行。
- 帮助用户准备开源时，先运行敏感信息扫描，拒绝把真实密钥/路径提交到 git。
- 回应结构：先确认立场 → 再给可执行方案 → 最后给出下一步命令。

## 相关文件

- 意图分析：`~/longhun-system/knowledge/deepseek-shared/intent_analysis.md`
- 本地终端方案：`~/longhun-system/knowledge/deepseek-shared/local_terminal_execution_plan.md`
- 开源边界：`~/longhun-system/knowledge/deepseek-shared/opensource_boundary.md`
- 执行脚本：`~/longhun-system/scripts/setup_longzhishou_push_env.sh`
""",
        encoding="utf-8",
    )
    return p


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


def main():
    print(f"\n{'='*60}")
    print("  DeepSeek 共享对话语境入库")
    print(f"  DNA: {_dna('build-deepseek-context-kb')}")
    print(f"{'='*60}\n")

    inserted, start_id = 写入_cs_kb()
    print(f"🟢 CS KB 写入 {inserted} 张知识卡片，起始 ID: {start_id}")

    paths = 生成_markdown_文档()
    print(f"🟢 生成/更新 {len(paths)} 篇 Markdown 知识文档: {KG_DIR}")

    indexed = 编入全局索引(paths)
    print(f"🟢 编入全局索引 {indexed} 个文件")

    mem = 生成记忆补充文件()
    print(f"🟢 生成记忆补充文件: {mem}")

    print(f"\n{'='*60}")
    print("  完成。可执行验证：")
    print("  ~/longhun-system/scripts/setup_longzhishou_push_env.sh")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
