#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂命名统一工具
DNA: #龍芯⚡️2026-06-29-LONGHUN-UNIFY-NAMING-v1.0

把全机龍魂相关路径里的简化字、中英混用目录名，通过“重命名 + 符号链接”方式统一成 CNSH 规范。
只做本地路径层级的统一，不动代码内部变量名（避免破坏运行）。
"""
import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

from cnsh_unified import 文字规范, DNA工具, 系统路径

REPORT_PATH = 系统路径.工作数据目录() / "naming_unification_report.json"
BACKUP_ROOT = 系统路径.龍魂配置目录() / "backups" / "naming-unify" / datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")


def 主函数(dry_run: bool = False):
    改动 = []
    跳过 = []
    失败 = []

    if not dry_run:
        BACKUP_ROOT.mkdir(parents=True, exist_ok=True)

    # 1. 重命名简化字目录
    待处理目录 = [
        系统路径.龍魂系统根目录() / "龍魂洛书369引擎",
    ]
    for 目录 in 待处理目录:
        if not 目录.exists():
            continue
        新名 = 文字规范.繁体龍(目录.name)
        新路径 = 目录.parent / 新名
        if 新路径.exists():
            跳过.append({"类型": "目录重命名", "原路径": str(目录), "原因": "目标已存在"})
            continue
        if dry_run:
            改动.append({"类型": "目录重命名", "原路径": str(目录), "新路径": str(新路径)})
            continue
        try:
            目录.rename(新路径)
            改动.append({"类型": "目录重命名", "原路径": str(目录), "新路径": str(新路径)})
        except Exception as e:
            失败.append({"类型": "目录重命名", "原路径": str(目录), "原因": str(e)})

    # 2. 创建统一别名符号链接（不删原路径）
    别名映射 = {
        "龍魂根目录": 系统路径.龍魂系统根目录(),
        "龍魂配置": 系统路径.龍魂配置目录(),
        "龍魂长记忆": 系统路径.龍魂长记忆目录(),
        "CNSH核心": 系统路径.CNSH核心目录(),
        "工作数据": 系统路径.工作数据目录(),
    }
    别名根 = 系统路径.龍魂系统根目录() / "统一入口"
    if not dry_run:
        别名根.mkdir(parents=True, exist_ok=True)

    for 别名, 目标 in 别名映射.items():
        链接 = 别名根 / 别名
        if 链接.exists() or 链接.is_symlink():
            跳过.append({"类型": "符号链接", "链接": str(链接), "原因": "已存在"})
            continue
        if dry_run:
            改动.append({"类型": "符号链接", "链接": str(链接), "目标": str(目标)})
            continue
        try:
            链接.symlink_to(目标, target_is_directory=True)
            改动.append({"类型": "符号链接", "链接": str(链接), "目标": str(目标)})
        except Exception as e:
            失败.append({"类型": "符号链接", "链接": str(链接), "原因": str(e)})

    # 3. 规范化 .longhun/memory/latest_digest.json 中的简化字 DNA
    digest_path = 系统路径.龍魂长记忆目录() / "memory" / "latest_digest.json"
    if digest_path.exists():
        try:
            文本 = digest_path.read_text(encoding="utf-8")
            新文本 = DNA工具.规范化(文本)
            if 新文本 != 文本:
                if not dry_run:
                    备份路径 = BACKUP_ROOT / digest_path.relative_to(Path.home())
                    备份路径.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(digest_path, 备份路径)
                    digest_path.write_text(新文本, encoding="utf-8")
                改动.append({"类型": "DNA规范化", "路径": str(digest_path)})
            else:
                跳过.append({"类型": "DNA规范化", "路径": str(digest_path), "原因": "无需修改"})
        except Exception as e:
            失败.append({"类型": "DNA规范化", "路径": str(digest_path), "原因": str(e)})

    报告 = {
        "时间": datetime.now(timezone.utc).isoformat(),
        "dry_run": dry_run,
        "改动": 改动,
        "跳过": 跳过,
        "失败": 失败,
    }
    REPORT_PATH.write_text(json.dumps(报告, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"\n🐉 龍魂命名统一报告")
    print(f"模式: {'预览' if dry_run else '实际执行'}")
    print(f"改动: {len(改动)}，跳过: {len(跳过)}，失败: {len(失败)}")
    print(f"报告已保存: {REPORT_PATH}\n")
    for item in 改动:
        print(f"  ✅ {item['类型']}: {item}")
    for item in 失败:
        print(f"  ❌ {item['类型']}: {item}")


if __name__ == "__main__":
    dry = "--dry-run" in sys.argv
    主函数(dry_run=dry)
