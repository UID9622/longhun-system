#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·乙申·甲寅·壬午·同人-MIGRATION-SCRIPT-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 创建者: 诸葛鑫（UID9622）
# 协议: CC BY-NC-SA 4.0
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# 三色: 🟢 批量迁移·旧文件清理·DNA嵌入

"""
龍魂待整理 → longhun-system 批量迁移脚本 v1.0
=============================================
功能：
  1. 扫描源目录，识别旧/测试/重复文件 → 标记删除
  2. 迁移有价值的文本文件到对应 longhun-system 目录
  3. 为所有文本文件嵌入 DNA 头部
  4. 生成迁移报告

迁移映射（源目录 → 目标目录）：
  01-CNSH-协议规范 → docs/cnsh/ + 01_protocols/
  02-流场可视化  → web/flow/ + papers/
  03-身份安全-DNA → 01_protocols/ + docs/
  04-审计治理    → audit/ + 01_protocols/
  05-AI人格-Agent → 02_SKILLS/ + bin/
  06-工具脚本    → bin/ + backend/
  07-论文PDF     → papers/
  08-浏览器插件   → extensions/
  09-杂项备忘    → docs/ + web/ + tools/

清理规则：
  - v1~v6.html（旧版本）→ 删除
  - *_bak.* / *.bak → 删除
  - 测试目录内容 → 评估后决定
  - 重复文件 → 保留最新版本
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone, timedelta
from pathlib import Path
import argparse
import hashlib
import json
import os
import re
import shutil
import sys

# ── 北京时区 ──
北京时区 = timezone(timedelta(hours=8))

# ── 路径配置 ──
源根 = Path("/Users").joinpath("zuimeidedeyihan", "龍魂待整理")
目标根 = Path(__file__).resolve().parent.parent


@dataclass
class 迁移结果:
    迁移: int = 0
    跳过: int = 0
    删除: int = 0
    错误: list = field(default_factory=list)


# ── 要删除的文件模式 ──
删除模式: list[tuple[str, str]] = [
    # (glob/路径片段, 原因)
    # 旧版本HTML
    ("v1.html", "旧版本文件"),
    ("v2.html", "旧版本文件"),
    ("v3.html", "旧版本文件"),
    ("v4.html", "旧版本文件"),
    ("v5_神经版.html", "旧版本文件"),
    ("v6_优化版.html", "旧版本文件"),
    # 备份文件
    ("_before_v8_", "版本快照备份"),
    # .bak 文件
    (".py.bak", "备份文件"),
    # .numbers 文件（二进制格式，移入archives）
    (".numbers", "二进制格式，归档处理"),
    # 空/占位文件
    ("test.txt", "测试文件"),
    ("便签.txt", "临时笔记"),
    # 大型重复文件
    ("level-f_0102.pdf", "大文件重复"),
]
要删除的文件名 = [
    "current_before_v8_20260419_223447.html",
    "notion-scan-report-v8.md",
    "extraction-report-v8.md",
    "宝宝娱乐t.html",
]

# ── 文件扩展名处理 ──
文本扩展名 = {".md", ".txt", ".html", ".htm", ".cnsh", ".json", ".yaml", ".yml",
            ".py", ".sh", ".js", ".css", ".xml", ".svg", ".toml", ".ini", ".cfg"}
复制扩展名 = {".pdf", ".png", ".jpg", ".jpeg", ".gif", ".ico", ".woff",
            ".woff2", ".ttf", ".otf", ".zip", ".wav", ".mp3", ".mp4"}
跳过扩展名 = {".docx", ".numbers", ".key", ".pages", ".pptx", ".xlsx", ".pem"}


# ── DNA模板 ──
DNA_HEADER_TEMPLATE = """\
<!--
  DNA: #龍芯⚡️{日期}-迁移-{模块}-v1.0
  创建者: 诸葛鑫（UID9622）
  协议: CC BY-NC-SA 4.0
  来源: 龍魂待整理/{源文件}
  迁移日期: {日期}
  GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
  三色: 🟢 旧档案吸收·DNA嵌入
-->
"""

DNA_HEADER_TEMPLATE_PY = """\
# DNA: #龍芯⚡️{日期}-迁移-{模块}-v1.0
# 创建者: 诸葛鑫（UID9622）
# 协议: CC BY-NC-SA 4.0
# 来源: 龍魂待整理/{源文件}
# 迁移日期: {日期}
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# 三色: 🟢 旧档案吸收·DNA嵌入
"""

DNA_HEADER_TEMPLATE_SH = """\
#
# DNA: #龍芯⚡️{日期}-迁移-{模块}-v1.0
# 创建者: 诸葛鑫（UID9622）
# 协议: CC BY-NC-SA 4.0
# 来源: 龍魂待整理/{源文件}
# 迁移日期: {日期}
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# 三色: 🟢 旧档案吸收·DNA嵌入
#
"""

DNA_HEADER_TEMPLATE_CSS = """\
/* DNA: #龍芯⚡️{日期}-迁移-{模块}-v1.0 */
/* 来源: 龍魂待整理/{源文件} · GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F */
/* 三色: 🟢 */
"""

DNA_HEADER_TEMPLATE_JSON = '{{\n    "_DNA": "#龍芯⚡️{日期}-迁移-{模块}-v1.0",\n    "_来源": "龍魂待整理/{源文件}",\n    "_三色": "🟢"\n}}'


# ── 目标目录映射 ──

def 获取目标目录(源文件: Path) -> Path | None:
    """根据源文件路径确定目标目录"""
    源路径 = str(源文件)
    目录名 = 源文件.parent.name if 源文件.parent != 源根 else ""

    # 01-CNSH协议规范
    if "01-CNSH" in 源路径:
        if 源文件.suffix in {".md", ".html"}:
            return 目标根 / "docs" / "cnsh"
        if 源文件.suffix == ".py":
            return 目标根 / "bin"
        if 源文件.suffix == ".sh":
            return 目标根 / "scripts"
        if 源文件.suffix == ".pdf":
            return 目标根 / "papers"
        return 目标根 / "docs" / "cnsh"

    # 02-流程可视化
    if "02-流场" in 源路径 or "02-" in 源路径[50:60]:
        if 源文件.suffix in {".html"}:
            return 目标根 / "web" / "flow"
        if 源文件.suffix in {".md"}:
            return 目标根 / "docs"
        if 源文件.suffix == ".py":
            return 目标根 / "bin"
        if 源文件.suffix == ".pdf":
            return 目标根 / "papers"
        if 源文件.suffix in {".json"}:
            return 目标根 / "config"
        return 目标根 / "web" / "flow"

    # 03-身份DNA安全
    if "03-身份" in 源路径 or "03-" in 源路径[50:60]:
        if 源文件.suffix in {".md", ".html"}:
            return 目标根 / "01_protocols"
        if 源文件.suffix == ".py":
            return 目标根 / "bin"
        return 目标根 / "docs" / "dna"

    # 04-审计治理
    if "04-审计" in 源路径:
        if 源文件.suffix in {".html"}:
            return 目标根 / "audit" / "docs"
        return 目标根 / "audit"

    # 05-AI人格Agent
    if "05-AI人格" in 源路径 or "05-" in 源路径[50:60]:
        if 源文件.suffix in {".md", ".html"}:
            return 目标根 / "01_技能庫"
        if 源文件.suffix == ".py":
            return 目标根 / "bin"
        if 源文件.suffix == ".sh":
            return 目标根 / "scripts"
        if 源文件.suffix == ".zip":
            return 目标根 / "dist"
        return 目标根 / "01_技能庫"

    # 06-工具脚本
    if "06-工具" in 源路径 or "06-" in 源路径[50:60]:
        if 源文件.suffix in {".py"}:
            return 目标根 / "bin"
        if 源文件.suffix in {".sh"}:
            return 目标根 / "scripts"
        if 源文件.suffix in {".js"}:
            return 目标根 / "web" / "tools"
        return 目标根 / "tools"

    # 07-论文PDF
    if "07-论文" in 源路径 or "07-" in 源路径[50:60]:
        return 目标根 / "papers"

    # 08-浏览器插件
    if "08-浏览器" in 源路径:
        return 目标根 / "extensions"

    # 09-杂项
    if "09-杂项" in 源路径 or "09-" in 源路径[50:60]:
        文件名 = 源文件.name.lower()
        if 源文件.suffix in {".html"}:
            if "portal" in 文件名 or "主页" in 文件名:
                return 目标根 / "web" / "archive"
            if "console" in 文件名 or "control" in 文件名 or "workbench" in 文件名 or "控制台" in 文件名 or "工作站" in 文件名:
                return 目标根 / "web" / "archive"
            if "memory" in 文件名 or "记忆" in 文件名 or "记忆压缩" in 文件名:
                return 目标根 / "web" / "archive"
            if "sandbox" in 文件名:
                return 目标根 / "web" / "archive"
            if "asset" in 文件名:
                return 目标根 / "tools"
            return 目标根 / "web" / "archive"
        if 源文件.suffix in {".md", ".txt"}:
            return 目标根 / "docs"
        if 源文件.suffix == ".py":
            return 目标根 / "bin"
        if 源文件.suffix in {".css"}:
            return 目标根 / "web"
        if 源文件.suffix == ".sh":
            return 目标根 / "scripts"
        return 目标根 / "docs"

    # 根目录文件
    if 源文件.suffix in {".json"}:
        return 目标根 / "config"
    if 源文件.suffix in {".md"}:
        return 目标根 / "docs"

    return None


def 应该删除(文件路径: Path) -> tuple[bool, str]:
    """检查文件是否应该删除"""
    文件名 = 文件路径.name
    路径str = str(文件路径)

    for pattern, reason in 删除模式:
        if pattern in 文件名:
            return True, reason

    if 文件名 in 要删除的文件名:
        return True, "标记为旧版本文件"

    if 文件名.endswith(".bak") or 文件名.endswith(".old"):
        return True, "备份文件"

    if 文件名 == ".DS_Store":
        return True, "系统文件"

    if 文件路径.suffix in 跳过扩展名:
        if 文件路径.stat().st_size < 1024 * 1024:  # < 1MB 的小文件归档
            return True, "不可处理格式，归档"

    return False, ""


def 嵌入DNA(内容: str, 模板: str, **kwargs) -> str:
    """为文件内容嵌入DNA头部"""
    dna_header = 模板.format(**kwargs)
    # 如果已有DNA头部，替换
    if "DNA: #龍芯" in 内容.split("\n")[0] if "\n" in 内容 else "":
        # Remove existing first few comment lines with DNA
        lines = 内容.split("\n")
        while lines and (lines[0].startswith("# DNA:") or lines[0].startswith("<!--") or lines[0].startswith("DNA:")):
            lines.pop(0)
            if lines and lines[0].strip() == "-->" and "DNA:" in 内容:
                lines.pop(0)
            # Stop after removing one header block
            if lines and not (lines[0].startswith("#") or lines[0].startswith("<!--")):
                break
        内容 = "\n".join(lines)
    return dna_header + "\n" + 内容


def 迁移文件(源文件: Path, 目标目录: Path, 日期: str, 结果: 迁移结果,
            dry_run: bool = False) -> None:
    """迁移单个文件到目标目录"""
    模块名 = 源文件.stem[:30].replace(" ", "_").replace("/", "_")
    源相对 = 源文件.relative_to(源根)

    # 构建DNA参数
    dna_kwargs = {
        "日期": 日期,
        "模块": 模块名,
        "源文件": str(源相对),
    }

    目标目录.mkdir(parents=True, exist_ok=True)
    目标文件 = 目标目录 / 源文件.name

    # 避免覆盖：如果目标已存在，加前缀
    if 目标文件.exists():
        新名称 = f"{源文件.stem}_(迁移){源文件.suffix}"
        目标文件 = 目标目录 / 新名称
        if 目标文件.exists():
            print(f"  ⚠️ 跳过（目标已存在）: {源相对} → {目标文件}")
            结果.跳过 += 1
            return

    if dry_run:
        print(f"  [DRY-RUN] {源相对} → {目标文件}")
        结果.迁移 += 1
        return

    # 文本文件：嵌入DNA
    if 源文件.suffix in {".md", ".txt"}:
        内容 = 源文件.read_text(encoding="utf-8", errors="replace")
        模板 = DNA_HEADER_TEMPLATE
        新内容 = 嵌入DNA(内容, 模板, **dna_kwargs)
        目标文件.write_text(新内容, encoding="utf-8")

    elif 源文件.suffix in {".html", ".htm"}:
        内容 = 源文件.read_text(encoding="utf-8", errors="replace")
        模板 = DNA_HEADER_TEMPLATE
        新内容 = 嵌入DNA(内容, 模板, **dna_kwargs)
        目标文件.write_text(新内容, encoding="utf-8")

    elif 源文件.suffix == ".py":
        内容 = 源文件.read_text(encoding="utf-8", errors="replace")
        模板 = DNA_HEADER_TEMPLATE_PY
        新内容 = 嵌入DNA(内容, 模板, **dna_kwargs)
        目标文件.write_text(新内容, encoding="utf-8")

    elif 源文件.suffix == ".sh":
        内容 = 源文件.read_text(encoding="utf-8", errors="replace")
        模板 = DNA_HEADER_TEMPLATE_SH
        新内容 = 嵌入DNA(内容, 模板, **dna_kwargs)
        目标文件.write_text(新内容, encoding="utf-8")

    elif 源文件.suffix == ".css":
        内容 = 源文件.read_text(encoding="utf-8", errors="replace")
        dna_header = DNA_HEADER_TEMPLATE_CSS.format(**dna_kwargs)
        目标文件.write_text(dna_header + "\n" + 内容, encoding="utf-8")

    elif 源文件.suffix in {".json", ".cnsh", ".yaml", ".yml", ".js"}:
        # 不嵌入DNA到JSON/JS/YAML（会破坏语法），仅复制
        目标文件.write_text(源文件.read_text(encoding="utf-8", errors="replace"), encoding="utf-8")

    elif 源文件.suffix in 复制扩展名:
        # 二进制文件：直接复制
        shutil.copy2(源文件, 目标文件)

    else:
        # 其他文本文件
        try:
            内容 = 源文件.read_text(encoding="utf-8", errors="replace")
            模板 = DNA_HEADER_TEMPLATE_PY
            新内容 = 嵌入DNA(内容, 模板, **dna_kwargs)
            目标文件.write_text(新内容, encoding="utf-8")
        except Exception:
            shutil.copy2(源文件, 目标文件)

    print(f"  ✅ {源相对} → {目标文件}")
    结果.迁移 += 1


def 扫描并迁移(源目录: Path, 日期: str, dry_run: bool = False) -> 迁移结果:
    """递归扫描源目录并迁移所有文件"""
    结果 = 迁移结果()

    for 根, 目录列表, 文件列表 in os.walk(源目录):
        根路径 = Path(根)
        相对根 = 根路径.relative_to(源目录)

        # 跳过 macOS 系统目录
        目录列表[:] = [d for d in 目录列表 if not d.startswith(".")]

        for 文件名 in 文件列表:
            文件路径 = 根路径 / 文件名
            源相对 = 文件路径.relative_to(源目录)

            # 检查是否跳过
            if 文件名.startswith("."):
                continue

            # 检查是否删除
            应删, 原因 = 应该删除(文件路径)
            if 应删:
                print(f"  🗑️ 删除: {源相对} ({原因})")
                结果.删除 += 1
                continue

            # 确定目标目录
            目标目录 = 获取目标目录(文件路径)
            if 目标目录 is None:
                print(f"  ⚠️ 跳过（无法确定目标目录）: {源相对}")
                结果.跳过 += 1
                continue

            迁移文件(文件路径, 目标目录, 日期, 结果, dry_run)

    return 结果


def main():
    parser = argparse.ArgumentParser(description="龍魂待整理 → longhun-system 批量迁移")
    parser.add_argument("--dry-run", action="store_true", help="预览模式，不实际写入")
    parser.add_argument("--delete-old", action="store_true", help="实际删除源目录中的旧文件")
    args = parser.parse_args()

    日期 = datetime.now(北京时区).strftime("%Y-%m-%d")

    print("=" * 70)
    print(f"龍魂待整理 → longhun-system 批量迁移 v1.0")
    print(f"日期: {日期}")
    print(f"源: {源根}")
    print(f"目标: {目标根}")
    print(f"模式: {'预览(DRY-RUN)' if args.dry_run else '实际执行'}")
    print("=" * 70)
    print()

    结果 = 扫描并迁移(源根, 日期, dry_run=args.dry_run)

    print()
    print("=" * 70)
    print("迁移完成")
    print(f"  ✅ 迁移: {结果.迁移}")
    print(f"  ⚠️  跳过: {结果.跳过}")
    print(f"  🗑️  删除: {结果.删除}")
    if 结果.错误:
        print(f"  ❌ 错误: {len(结果.错误)}")
    print("=" * 70)


if __name__ == "__main__":
    main()
