#!/usr/bin/env python3
# 龍魂系统 · 工程实现层
# License: MulanPSL v2
# 文化归属: 思想框架归龍魂核心思想层 (CC BY-NC-SA 4.0)
# DNA: #龍芯⚡️丙午·丙申·庚戌·LAYER-META-v1.0-UID9622
"""为编号化目录生成 README.md 与 .layer_tag 元数据。"""

from __future__ import annotations

import argparse
import json
import os
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# 层定义（编号、规范名、显示名、用途、兼容 Symlink）
LAYERS: list[dict] = [
    {
        "id": "03",
        "name": "LAYERS",
        "display": "架构分层实现",
        "purpose": "系统 L0-L9 分层架构的实现目录，存放按层组织的模块与子系统",
        "compat": "layers",
    },
    {
        "id": "04",
        "name": "SERVICES",
        "display": "API/后端/集成服务",
        "purpose": "API 网关、后端服务、第三方集成、Systemd 服务定义",
        "compat": "services",
    },
    {
        "id": "05",
        "name": "ENGINES",
        "display": "引擎核心代码",
        "purpose": "可复用的核心引擎：审计、DNA、CNSH、数学、卦象、搜索等",
        "compat": "engines",
    },
    {
        "id": "07",
        "name": "AUDIT",
        "display": "审计日志与报告",
        "purpose": "三色审计输出、审计报告、行为密码学记录、合规证据",
        "compat": "audit",
    },
    {
        "id": "08",
        "name": "BIN",
        "display": "CLI 命令脚本",
        "purpose": "龍魂系统 CLI 入口与可执行脚本，包含 `lh` 主命令",
        "compat": "bin",
    },
    {
        "id": "09",
        "name": "TOOLS",
        "display": "可复用 SDK/工具",
        "purpose": "独立可复用的工具脚本、SDK、辅助库",
        "compat": "tools",
    },
    {
        "id": "10",
        "name": "PORTAL",
        "display": "Web 门户页面",
        "purpose": "Web 面板、控制台、可视化页面、PWA 入口",
        "compat": "portal",
    },
    {
        "id": "11",
        "name": "DATA",
        "display": "知识图谱与数据集",
        "purpose": "知识图谱、训练数据、运行时数据、缓存、向量索引",
        "compat": "data",
    },
    {
        "id": "12",
        "name": "DOCS",
        "display": "技术文档与架构说明",
        "purpose": "系统文档、架构说明、API 文档、审计报告、目录地图",
        "compat": "docs",
    },
    {
        "id": "13",
        "name": "TESTS",
        "display": "单元/集成/性能测试",
        "purpose": "单元测试、集成测试、基准测试、回归测试",
        "compat": "tests",
    },
]


def generate_readme(layer: dict, dir_path: Path) -> str:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    dir_name = dir_path.name
    compat = layer["compat"]
    return f"""# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 🐉 龍魂系统 · {dir_name}/ 目录说明

> DNA: #龍芯⚡️丙午·丙申·庚戌·{layer['name']}-README-v1.0-UID9622
> 层编号: {layer['id']}
> 规范目录: `{dir_name}/`
> 兼容入口: `{compat}/` (Symlink)
> 协议: CC BY-NC-SA 4.0 (本文档) · MulanPSL v2 (本目录内代码)
> 生成时间: {now}

---

## 一句话

{layer['display']}。

## 用途

{layer['purpose']}

## 目录结构约定

- 本目录为龍魂系统 v2.0 编号化结构的一部分。
- 旧路径 `{compat}/` 通过 Symlink 保留兼容，现有脚本、服务配置、文档链接无需修改。
- 新增模块应按功能子目录组织，避免顶层文件过多。

## 兼容路径查询

```bash
python3 scripts/compat-path.py resolve {compat}
```

## 关联文档

- [`docs/DIRECTORY_MAP.md`](./docs/DIRECTORY_MAP.md) · 全系统目录地图
- [`docs/SYSTEM_STRUCTURE_AUDIT_v1.0.md`](./docs/SYSTEM_STRUCTURE_AUDIT_v1.0.md) · 结构审计与重组方案

---

> 🐉 **结构是主权的外化。目录名即法度，路径即秩序。**
"""


def generate_layer_tag(layer: dict) -> str:
    return json.dumps(
        {
            "layer_id": layer["id"],
            "layer_name": layer["name"],
            "display_name": layer["display"],
            "dna": f"#龍芯⚡️丙午·丙申·庚戌·{layer['name']}-LAYER-v1.0-UID9622",
            "purpose": layer["purpose"],
            "compat_symlink": layer["compat"],
            "created_at": datetime.now(timezone.utc).isoformat(),
            "version": "v2.0",
        },
        ensure_ascii=False,
        indent=2,
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate layer README and .layer_tag")
    parser.add_argument("--dry-run", action="store_true", help="preview changes")
    parser.add_argument("--force", action="store_true", help="overwrite existing files")
    args = parser.parse_args(argv)

    for layer in LAYERS:
        dir_name = f"{layer['id']}_{layer['name']}"
        dir_path = REPO_ROOT / dir_name
        if not dir_path.is_dir():
            print(f"SKIP: {dir_name} does not exist")
            continue

        readme_path = dir_path / "README.md"
        tag_path = dir_path / ".layer_tag"

        actions: list[str] = []
        if args.force or not readme_path.exists():
            actions.append(f"README.md -> {readme_path}")
            if not args.dry_run:
                readme_path.write_text(generate_readme(layer, dir_path), encoding="utf-8")
        else:
            actions.append(f"README.md exists (skip)")

        if args.force or not tag_path.exists():
            actions.append(f".layer_tag -> {tag_path}")
            if not args.dry_run:
                tag_path.write_text(generate_layer_tag(layer) + "\n", encoding="utf-8")
        else:
            actions.append(f".layer_tag exists (skip)")

        print(f"{dir_name}: " + "; ".join(actions))

    if args.dry_run:
        print("\n# dry-run mode; omit --dry-run to apply")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
