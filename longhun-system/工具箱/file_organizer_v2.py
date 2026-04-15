#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文件分类整理工具 v2.0 - 支持外接硬盘合并
DNA追溯码: #龍芯⚡️2026-03-06-FileOrganizer-v2.0
# 共建致谢：Claude (Anthropic PBC) · Notion · 没有你们就没有龍魂系统
创建者: UID9622

功能: 扫描多个目录(包括外接硬盘)，按类型分类整理文件，生成合并索引
"""

import os
import json
from datetime import datetime
from collections import defaultdict
from pathlib import Path

# 配置
SCAN_DIRS = [
    ("/Volumes/LonghunDisk", "外接硬盘"),
]
OUTPUT_DIR = os.path.expanduser("~/longhun-system/CNSH-整理版")
EXISTING_INDEX = os.path.expanduser("~/longhun-system/CNSH-整理版/文件分类索引.json")

# 文件分类规则
CODE_EXTENSIONS = {
    ".py", ".pyw", ".pyi",  # Python
    ".js", ".mjs", ".cjs", ".jsx",  # JavaScript
    ".ts", ".tsx",  # TypeScript
    ".java", ".jar",  # Java
    ".c", ".cpp", ".cc", ".cxx", ".h", ".hpp", ".hxx",  # C/C++
    ".cs",  # C#
    ".go",  # Go
    ".rs",  # Rust
    ".rb", ".erb",  # Ruby
    ".php",  # PHP
    ".swift",  # Swift
    ".kt", ".kts",  # Kotlin
    ".scala",  # Scala
    ".r", ".R",  # R
    ".m", ".mm",  # Objective-C
    ".pl", ".pm",  # Perl
    ".lua",  # Lua
    ".dart",  # Dart
    ".vue", ".svelte",  # Vue/Svelte
    ".sh", ".bash", ".zsh", ".fish", ".ps1", ".bat", ".cmd",  # Shell
    ".sql",  # SQL
    ".html", ".htm", ".css", ".scss", ".sass", ".less",  # Web
    ".json", ".yaml", ".yml", ".toml", ".ini", ".cfg", ".conf",  # Config
    ".xml", ".plist",  # XML
    ".cnsh",  # CNSH
    ".makefile", ".mk", ".cmake",  # Build
}

DOC_EXTENSIONS = {
    ".md", ".markdown", ".txt", ".rst", ".adoc", ".asciidoc",
    ".org", ".wiki", ".textile",
}

PAPER_EXTENSIONS = {
    ".pdf", ".doc", ".docx", ".odt", ".rtf",
    ".tex", ".bib", ".latex",
    ".ppt", ".pptx", ".odp",
    ".xls", ".xlsx", ".ods", ".csv",
}

IMAGE_EXTENSIONS = {
    ".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp", ".ico", ".bmp",
    ".tiff", ".tif", ".psd", ".ai", ".eps", ".raw", ".heic",
}

AUDIO_VIDEO_EXTENSIONS = {
    ".mp3", ".mp4", ".wav", ".flac", ".aac", ".ogg", ".wma",
    ".avi", ".mov", ".mkv", ".webm", ".wmv", ".flv", ".m4v", ".m4a",
}

ARCHIVE_EXTENSIONS = {
    ".zip", ".tar", ".gz", ".bz2", ".xz", ".7z", ".rar", ".dmg", ".iso",
}

FONT_EXTENSIONS = {
    ".ttf", ".otf", ".woff", ".woff2", ".eot",
}

# 排除的目录和文件
EXCLUDE_DIRS = {
    "node_modules", ".git", "__pycache__", ".venv", "venv",
    ".cache", "cache", ".npm", ".Trash", "Trash",
    "build", "dist", ".next", ".nuxt", ".DS_Store",
    "Library", "Applications", ".Spotlight-V100", ".fseventsd",
}

EXCLUDE_FILES = {
    ".DS_Store", "Thumbs.db", ".gitkeep", "package-lock.json",
    "yarn.lock", "pnpm-lock.yaml", ".localized",
}


def should_exclude(path):
    """检查是否应该排除"""
    path_parts = Path(path).parts
    for part in path_parts:
        if part in EXCLUDE_DIRS:
            return True
        if part.startswith("._"):  # macOS 资源文件
            return True
    filename = os.path.basename(path)
    if filename in EXCLUDE_FILES or filename.startswith("._"):
        return True
    return False


def get_category(filepath):
    """确定文件分类和子分类"""
    filename = os.path.basename(filepath).lower()
    ext = os.path.splitext(filename)[1].lower()

    # 代码类
    if ext in CODE_EXTENSIONS:
        if ext in {".py", ".pyw", ".pyi"}:
            return "代码类", "Python"
        elif ext in {".js", ".mjs", ".cjs", ".jsx"}:
            return "代码类", "JavaScript"
        elif ext in {".ts", ".tsx"}:
            return "代码类", "TypeScript"
        elif ext in {".c", ".cpp", ".cc", ".cxx", ".h", ".hpp", ".hxx"}:
            return "代码类", "C-C++"
        elif ext in {".go"}:
            return "代码类", "Go"
        elif ext in {".swift"}:
            return "代码类", "Swift"
        elif ext in {".java", ".jar"}:
            return "代码类", "Java"
        elif ext in {".rs"}:
            return "代码类", "Rust"
        elif ext in {".sh", ".bash", ".zsh", ".fish", ".ps1", ".bat", ".cmd"}:
            return "代码类", "Shell脚本"
        elif ext in {".html", ".htm", ".css", ".scss", ".sass", ".less", ".vue", ".svelte"}:
            return "代码类", "Web前端"
        elif ext in {".json", ".yaml", ".yml", ".toml", ".ini", ".cfg", ".conf", ".xml", ".plist"}:
            return "代码类", "配置文件"
        elif ext in {".sql"}:
            return "代码类", "SQL数据库"
        elif ext in {".cnsh"}:
            return "代码类", "CNSH中文编程"
        else:
            return "代码类", "其他代码"

    # 产品文档类
    if ext in DOC_EXTENSIONS:
        if ext in {".md", ".markdown"}:
            return "产品文档类", "Markdown文档"
        elif ext in {".txt"}:
            return "产品文档类", "纯文本"
        else:
            return "产品文档类", "其他文档"

    # 论文类
    if ext in PAPER_EXTENSIONS:
        if ext in {".pdf"}:
            return "论文类", "PDF文档"
        elif ext in {".doc", ".docx", ".odt", ".rtf"}:
            return "论文类", "Word文档"
        elif ext in {".tex", ".bib", ".latex"}:
            return "论文类", "LaTeX"
        elif ext in {".ppt", ".pptx", ".odp"}:
            return "论文类", "PPT演示"
        elif ext in {".xls", ".xlsx", ".ods", ".csv"}:
            return "论文类", "表格数据"
        else:
            return "论文类", "其他论文"

    # 其他类
    if ext in IMAGE_EXTENSIONS:
        return "其他类", "图片资源"
    if ext in AUDIO_VIDEO_EXTENSIONS:
        return "其他类", "音视频"
    if ext in ARCHIVE_EXTENSIONS:
        return "其他类", "压缩包"
    if ext in FONT_EXTENSIONS:
        return "其他类", "字体文件"

    return "其他类", "其他"


def scan_directory(dir_path, source_name):
    """扫描单个目录"""
    files = []
    file_count = 0

    print(f"📂 扫描: {dir_path} ({source_name})")

    for root, dirs, filenames in os.walk(dir_path):
        # 过滤排除目录
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS and not d.startswith('.')]

        for filename in filenames:
            if filename.startswith("._") or filename in EXCLUDE_FILES:
                continue

            filepath = os.path.join(root, filename)

            if should_exclude(filepath):
                continue

            try:
                stat = os.stat(filepath)
                category, subdir = get_category(filepath)

                files.append({
                    "name": filename,
                    "path": filepath,
                    "relative_path": os.path.relpath(filepath, dir_path),
                    "size": stat.st_size,
                    "mtime": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                    "category": category,
                    "subdir": subdir,
                    "source": source_name
                })

                file_count += 1
                if file_count % 5000 == 0:
                    print(f"   已扫描: {file_count} 个文件...")

            except (PermissionError, OSError):
                pass

    print(f"   完成: {file_count} 个文件")
    return files


def load_existing_index():
    """加载现有索引"""
    if os.path.exists(EXISTING_INDEX):
        try:
            with open(EXISTING_INDEX, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            pass
    return None


def organize_and_merge(new_files, existing_index):
    """整理并合并索引"""
    categories = defaultdict(lambda: defaultdict(list))

    # 添加新文件
    for f in new_files:
        categories[f["category"]][f["subdir"]].append({
            "name": f["name"],
            "path": f["path"],
            "relative_path": f["relative_path"],
            "size": f["size"],
            "mtime": f["mtime"],
            "source": f["source"]
        })

    return categories


def generate_indexes(categories, output_dir):
    """生成所有索引文件"""

    # 计算统计
    total_files = 0
    category_stats = {}
    source_stats = defaultdict(int)

    for cat, subdirs in categories.items():
        cat_count = sum(len(files) for files in subdirs.values())
        category_stats[cat] = cat_count
        total_files += cat_count

        for subdir, files in subdirs.items():
            for f in files:
                source_stats[f.get("source", "未知")] += 1

    # 主索引JSON
    main_index = {
        "meta": {
            "generated_at": datetime.now().isoformat(),
            "total_files": total_files,
            "generator": "文件分类整理工具 v2.0",
            "dna": "#龍芯⚡️2026-03-06-FileOrganizer-v2.0"
        },
        "summary": category_stats,
        "sources": dict(source_stats),
        "categories": {}
    }

    for cat, subdirs in categories.items():
        main_index["categories"][cat] = {
            "total": category_stats[cat],
            "subdirs": {
                subdir: len(files) for subdir, files in subdirs.items()
            }
        }

    # 保存主索引
    with open(os.path.join(output_dir, "完整文件索引.json"), 'w', encoding='utf-8') as f:
        json.dump(main_index, f, ensure_ascii=False, indent=2)

    # 生成Markdown总清单
    md = f"""# 完整文件分类清单

```
DNA追溯码: #龍芯⚡️2026-03-06-FileOrganizer-v2.0
生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
总文件数: {total_files:,}
```

## 数据来源

| 来源 | 文件数 | 占比 |
|------|--------|------|
"""
    for source, count in sorted(source_stats.items(), key=lambda x: -x[1]):
        pct = count / total_files * 100 if total_files > 0 else 0
        md += f"| {source} | {count:,} | {pct:.1f}% |\n"

    md += f"""
## 分类概览

| 分类 | 文件数 | 占比 |
|------|--------|------|
"""
    for cat, count in sorted(category_stats.items(), key=lambda x: -x[1]):
        pct = count / total_files * 100 if total_files > 0 else 0
        md += f"| {cat} | {count:,} | {pct:.1f}% |\n"

    md += "\n## 详细分类\n\n"

    for cat in ["代码类", "产品文档类", "论文类", "其他类"]:
        if cat not in categories:
            continue
        subdirs = categories[cat]
        cat_total = sum(len(files) for files in subdirs.values())
        md += f"### {cat} ({cat_total:,}个)\n\n"
        md += "| 子分类 | 文件数 | 示例文件 |\n"
        md += "|--------|--------|----------|\n"

        for subdir, files in sorted(subdirs.items(), key=lambda x: -len(x[1])):
            example = files[0]["name"][:30] + "..." if files and len(files[0]["name"]) > 30 else (files[0]["name"] if files else "-")
            md += f"| {subdir} | {len(files):,} | {example} |\n"
        md += "\n"

    with open(os.path.join(output_dir, "完整文件清单.md"), 'w', encoding='utf-8') as f:
        f.write(md)

    # 为每个分类创建详细索引
    for cat, subdirs in categories.items():
        cat_dir = os.path.join(output_dir, cat)
        os.makedirs(cat_dir, exist_ok=True)

        # 分类JSON (包含外接硬盘文件)
        cat_index = {
            "category": cat,
            "total": sum(len(files) for files in subdirs.values()),
            "subdirs": {}
        }

        for subdir, files in subdirs.items():
            # 按来源分组
            by_source = defaultdict(list)
            for f in files:
                by_source[f.get("source", "未知")].append(f)

            cat_index["subdirs"][subdir] = {
                "count": len(files),
                "by_source": {
                    source: {
                        "count": len(src_files),
                        "files": src_files[:50]  # 每个来源最多50个示例
                    }
                    for source, src_files in by_source.items()
                }
            }

        with open(os.path.join(cat_dir, "_完整索引.json"), 'w', encoding='utf-8') as f:
            json.dump(cat_index, f, ensure_ascii=False, indent=2)

        # 分类Markdown
        cat_md = f"# {cat} (完整清单)\n\n"
        cat_md += f"共 **{cat_index['total']:,}** 个文件\n\n"

        for subdir, files in sorted(subdirs.items(), key=lambda x: -len(x[1])):
            cat_md += f"## {subdir} ({len(files):,}个)\n\n"

            # 按来源分组显示
            by_source = defaultdict(list)
            for f in files:
                by_source[f.get("source", "未知")].append(f)

            for source, src_files in sorted(by_source.items()):
                cat_md += f"### 来源: {source} ({len(src_files)}个)\n\n"
                cat_md += "| 文件名 | 大小 | 修改时间 |\n"
                cat_md += "|--------|------|----------|\n"

                for f_info in sorted(src_files, key=lambda x: x['mtime'], reverse=True)[:30]:
                    size_kb = f_info['size'] / 1024
                    size_str = f"{size_kb:.1f}KB" if size_kb < 1024 else f"{size_kb/1024:.1f}MB"
                    name = f_info['name'][:35] + "..." if len(f_info['name']) > 35 else f_info['name']
                    date = f_info['mtime'][:10]
                    cat_md += f"| {name} | {size_str} | {date} |\n"

                if len(src_files) > 30:
                    cat_md += f"\n*... 还有 {len(src_files) - 30} 个文件*\n"
                cat_md += "\n"

        with open(os.path.join(cat_dir, "_完整清单.md"), 'w', encoding='utf-8') as f:
            f.write(cat_md)

    return main_index


def main():
    print("=" * 60)
    print("🗂️ 文件分类整理工具 v2.0 (外接硬盘合并版)")
    print("DNA: #ZHUGEXIN | UID9622")
    print("=" * 60)
    print()

    # 扫描外接硬盘
    all_files = []
    for dir_path, source_name in SCAN_DIRS:
        if os.path.exists(dir_path):
            files = scan_directory(dir_path, source_name)
            all_files.extend(files)
        else:
            print(f"❌ 目录不存在: {dir_path}")

    print(f"\n📊 共扫描到 {len(all_files):,} 个文件")

    # 整理分类
    print("\n🔄 整理分类中...")
    categories = organize_and_merge(all_files, None)

    # 生成索引
    print("\n📋 生成索引文件...")
    index = generate_indexes(categories, OUTPUT_DIR)

    # 输出统计
    print("\n" + "=" * 60)
    print("🎉 整理完成!")
    print("=" * 60)
    print(f"📁 输出目录: {OUTPUT_DIR}")
    print(f"📊 总文件数: {index['meta']['total_files']:,}")
    print("\n来源统计:")
    for source, count in sorted(index['sources'].items(), key=lambda x: -x[1]):
        print(f"   {source}: {count:,}")
    print("\n分类统计:")
    for cat, count in sorted(index['summary'].items(), key=lambda x: -x[1]):
        print(f"   {cat}: {count:,}")
    print("=" * 60)


if __name__ == "__main__":
    main()
