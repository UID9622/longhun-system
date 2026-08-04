#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · 知识智能合并引擎 v2.1
DNA: #龍芯⚡️丙午·丙申·乙巳·壬午·☴巽-MERGE-v2.1-UID9622
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0

功能：
  智能合并 MEMORY.md —— 只更新自动生成区块，保护人工维护章节。
  - --dry-run  预览 diff，不写入
  - 默认       备份→合并→写入

用法：
  python3 bin/lh_knowledge_complete.py          # 执行合并
  python3 bin/lh_knowledge_complete.py --dry-run # 预览变更
  lh 知识补全                                    # 注册后可用
  lh 知识补全 --dry-run                          # 预览
"""

import os
import sys
import json
import difflib
import shutil
import argparse
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Tuple, Optional

# ============================================================
# 配置
# ============================================================

# 通过脚本所在位置推导项目根目录，避免硬编码 home 路径带来的移植与链式攻击风险
PROJECT_ROOT = Path(__file__).resolve().parent.parent
BIN_DIR = PROJECT_ROOT / "bin"
MEMORY_FILE = PROJECT_ROOT / ".codebuddy" / "memory" / "MEMORY.md"
HARVEST_DIR = PROJECT_ROOT / "data" / "harvested_knowledge"
REPORT_FILE = PROJECT_ROOT / "data" / "completion_report.json"
CONFIRM_CODE = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"

# MEMORY.md 中的自动区块标记
AUTO_START = "<!-- AUTO-GENERATED-START -->"
AUTO_END = "<!-- AUTO-GENERATED-END -->"

# 敏感目录创建权限：仅所有者可读写执行
DIR_MODE = 0o700

# ============================================================
# 工具函数
# ============================================================

def now_iso() -> str:
    return datetime.now().isoformat()

def dna_timestamp() -> str:
    return datetime.now().strftime("%Y%m%d%H%M%S")

def backup_timestamp() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def print_step(msg: str):
    print(f"🔹 {msg}")

def print_ok(msg: str):
    print(f"✅ {msg}")

def print_warn(msg: str):
    print(f"⚠️ {msg}")

def print_err(msg: str):
    print(f"❌ {msg}")

# ============================================================
# 数据采集
# ============================================================

def get_core_engines() -> List[str]:
    """扫描 bin/ 下 lh_*.py 引擎（排除 legacy）"""
    engines = []
    if not BIN_DIR.is_dir():
        print_warn(f"引擎目录不存在: {BIN_DIR}")
        return engines
    for f in sorted(BIN_DIR.glob("lh_*.py")):
        if "legacy" in f.name.lower():
            continue
        engines.append(f.name)
    return engines


def get_knowledge_summary() -> Dict[str, int]:
    """统计 harvested_knowledge 目录下的知识摘要"""
    counts = {"原则": 0, "规则": 0, "缺失模块": 0, "代码候选": 0}

    if not HARVEST_DIR.is_dir():
        print_warn(f"知识目录不存在: {HARVEST_DIR}")
        return counts

    principles_file = HARVEST_DIR / "PRINCIPLES.md"
    rules_file = HARVEST_DIR / "RULES.md"
    missing_file = HARVEST_DIR / "MISSING_MODULES.md"
    candidates_file = HARVEST_DIR / "CODE_CANDIDATES.md"

    if principles_file.exists():
        text = principles_file.read_text(encoding='utf-8')
        counts["原则"] = sum(1 for _ in text.split('\n') if _.strip().startswith('##'))

    if rules_file.exists():
        text = rules_file.read_text(encoding='utf-8')
        # 修复：先 strip 再判断注释，避免缩进规则行被误统计或遗漏
        counts["规则"] = sum(
            1 for _ in text.split('\n')
            if _.strip() and not _.strip().startswith('#')
        )

    if missing_file.exists():
        text = missing_file.read_text(encoding='utf-8')
        counts["缺失模块"] = sum(1 for _ in text.split('\n') if _.strip().startswith('- [ ]'))

    if candidates_file.exists():
        text = candidates_file.read_text(encoding='utf-8')
        counts["代码候选"] = sum(1 for _ in text.split('\n') if _.strip().startswith('##'))

    return counts


# ============================================================
# 自动生成区块
# ============================================================

def generate_auto_block(engines: List[str], summary: Dict[str, int]) -> str:
    """生成自动更新区块的内容"""
    dt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # 引擎列表（只列前30，防过长）
    max_display = 30
    display_engines = engines[:max_display]
    engine_lines = '\n'.join(f"- `{e}`" for e in display_engines)
    if len(engines) > max_display:
        engine_lines += f"\n- ... 还有 {len(engines) - max_display} 个"
    if not engine_lines:
        engine_lines = "_暂无核心引擎_"

    block = f"""{AUTO_START}
## 核心引擎 ({len(engines)} 个)

{engine_lines}

## 知识库摘要

| 类型 | 数量 |
|------|------|
| 原则 | {summary['原则']} |
| 规则 | {summary['规则']} |
| 缺失模块 | {summary['缺失模块']} |
| 代码候选 | {summary['代码候选']} |

> 此区块由 `lh 知识补全` 自动生成
> 最后更新: {dt}
{AUTO_END}"""
    return block


# ============================================================
# 合并逻辑
# ============================================================

def read_memory() -> Optional[str]:
    """读取当前 MEMORY.md"""
    if not MEMORY_FILE.exists():
        return None
    return MEMORY_FILE.read_text(encoding='utf-8')


def split_memory(content: str) -> Tuple[str, str, str]:
    """
    将 MEMORY.md 拆分为三部分:
    - before: 自动区块之前的内容
    - auto: 自动区块内容（如果存在）
    - after: 自动区块之后的内容（人工维护部分）

    如果没有标记，则 after = 全部内容（首次运行）
    """
    has_start = AUTO_START in content
    has_end = AUTO_END in content

    if has_start and has_end:
        start_idx = content.index(AUTO_START)
        end_idx = content.index(AUTO_END)
        if end_idx < start_idx:
            raise ValueError("AUTO-GENERATED 标记顺序异常：END 出现在 START 之前")
        before = content[:start_idx]
        auto = content[start_idx:end_idx + len(AUTO_END)]
        after = content[end_idx + len(AUTO_END):]
        return before, auto, after
    elif has_start or has_end:
        # 只有一个标记：文件已损坏，必须人工介入
        missing = "END" if has_start else "START"
        raise ValueError(f"AUTO-GENERATED 标记不完整：缺少 {missing}")
    else:
        # 首次运行：找 --- 分隔线，在其后插入自动区块
        sep = "\n---\n"
        if sep in content:
            idx = content.index(sep) + len(sep)
            before = content[:idx]
            after = content[idx:]
        else:
            before = ""
            after = content
        return before, "", after


def merge_memory(before: str, auto: str, after: str) -> str:
    """拼接合并后的 MEMORY.md

    修复尾部换行符累积 bug：旧实现每次运行都会多追加一个空行，
    长时间运行会导致 MEMORY.md 尾部空行无限增长。现统一归一化为单个换行结尾。
    """
    result = before.rstrip()
    if auto.strip():
        result += "\n\n" + auto.strip()
    if after.strip():
        result += "\n\n" + after.strip()
    # 统一尾部：恰好一个换行
    result = result.rstrip() + "\n"
    return result


def generate_diff(old: str, new: str) -> str:
    """生成 unified diff"""
    old_lines = old.splitlines(keepends=True)
    new_lines = new.splitlines(keepends=True)
    diff = difflib.unified_diff(
        old_lines, new_lines,
        fromfile='MEMORY.md (old)',
        tofile='MEMORY.md (new)',
    )
    return ''.join(diff)


def backup_memory() -> Optional[Path]:
    """备份当前 MEMORY.md（带时间戳）"""
    if not MEMORY_FILE.exists():
        return None
    backup_path = MEMORY_FILE.with_suffix(f".md.bak.{backup_timestamp()}")
    shutil.copy2(MEMORY_FILE, backup_path)
    return backup_path


def verify_write(expected: str) -> bool:
    """回读 MEMORY.md 验证写入一致性"""
    if not MEMORY_FILE.exists():
        print_err("写入验证失败：文件不存在")
        return False
    actual = MEMORY_FILE.read_text(encoding='utf-8')
    if actual != expected:
        print_err("写入验证失败：回读内容与预期不一致")
        return False
    return True


# ============================================================
# 报告
# ============================================================

def save_report(engines: List[str], summary: Dict[str, int], auto_lines: int,
                total_lines: int, status: str) -> bool:
    """保存补全报告 JSON"""
    try:
        REPORT_FILE.parent.mkdir(parents=True, exist_ok=True, mode=DIR_MODE)
        report = {
            "timestamp": now_iso(),
            "dna": f"#龍芯⚡️{dna_timestamp()}-MERGE-v2.1-UID9622",
            "status": status,
            "engines_count": len(engines),
            "knowledge_summary": summary,
            "auto_block_lines": auto_lines,
            "total_lines": total_lines,
        }
        with open(REPORT_FILE, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print_err(f"保存报告失败: {e}")
        return False


# ============================================================
# 主流程
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="龍魂 · 知识智能合并引擎",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="预览 diff，不写入文件",
    )
    args = parser.parse_args()
    dry_run = args.dry_run

    print("\n🐉 龍魂 · 知识智能合并引擎")
    print(f"确认码: {CONFIRM_CODE}")

    if dry_run:
        print("🔍 预览模式（不写入文件）\n")
    else:
        print("🔄 执行智能合并...\n")

    # 1. 读取当前 MEMORY.md
    current = read_memory()
    if current is None:
        print_warn("MEMORY.md 不存在，将创建新文件")
        current = ""

    # 2. 采集数据
    print_step("扫描核心引擎...")
    engines = get_core_engines()
    print_ok(f"找到 {len(engines)} 个核心引擎")

    print_step("统计知识库摘要...")
    summary = get_knowledge_summary()
    print_ok(f"原则:{summary['原则']} 规则:{summary['规则']} 缺失:{summary['缺失模块']} 候选:{summary['代码候选']}")

    # 3. 生成自动区块
    print_step("生成自动更新区块...")
    new_auto = generate_auto_block(engines, summary)

    # 4. 拆分 & 合并
    before, old_auto, after = split_memory(current)
    new_memory = merge_memory(before, new_auto, after)

    # 5. 生成 diff
    has_auto_before = AUTO_START in current
    diff = generate_diff(current, new_memory)

    if dry_run:
        # 预览模式
        print(f"\n📄 变更预览（diff）:\n")
        if diff.strip():
            print(diff)
            print(f"\n📊 统计: {len(diff.splitlines())} 行差异")
        else:
            print_ok("无变更（内容已是最新）")

        # 显示受保护的章节
        protected_sections = [line for line in after.split('\n') if line.startswith('## §')]
        if protected_sections:
            print(f"\n🛡️ 受保护的人工章节 ({len(protected_sections)} 个):")
            for s in protected_sections:
                print(f"  {s.strip()}")

        print(f"\n📌 运行 'lh 知识补全' 执行实际合并")
        return

    # 实际执行模式
    # 6. 备份
    backup_path = backup_memory()
    if backup_path:
        print_ok(f"已备份到: {backup_path}")

    # 7. 写入
    print_step("写入合并后的 MEMORY.md...")
    MEMORY_FILE.parent.mkdir(parents=True, exist_ok=True, mode=DIR_MODE)
    MEMORY_FILE.write_text(new_memory, encoding='utf-8')

    # 8. 写入一致性验证
    if not verify_write(new_memory):
        print_err("MEMORY.md 写入后验证未通过，请检查备份与磁盘状态")
        sys.exit(1)

    new_lines = len(new_memory.splitlines())
    auto_lines = len(new_auto.splitlines())
    print_ok(f"已写入 MEMORY.md ({new_lines} 行, 自动区块 {auto_lines} 行)")

    # 9. 报告
    print_step("生成补全报告...")
    status = "merged" if has_auto_before else "initialized"
    if not save_report(engines, summary, auto_lines, new_lines, status):
        print_warn("报告保存失败，但 MEMORY.md 已成功更新")
    else:
        print_ok(f"报告: {REPORT_FILE}")

    # 10. 完成
    print("\n" + "=" * 50)
    print("✅ 知识补全完成！")
    print(f"📊 引擎: {len(engines)} 个")
    print(f"📄 MEMORY.md: {new_lines} 行")
    if backup_path:
        print(f"📦 备份: {backup_path}")
    print(f"🔑 DNA: #龍芯⚡️{dna_timestamp()}-MERGE-v2.1-UID9622")
    print("=" * 50)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print_err("\n操作已取消")
        sys.exit(130)
    except Exception as e:
        print_err(f"执行失败: {e}")
        sys.exit(1)
