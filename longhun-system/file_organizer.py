#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文件分类整理工具 v1.0
DNA追溯码: #龍芯⚡️2026-03-06-FileOrganizer-v1.0
# 共建致谢：Claude (Anthropic PBC) · Notion · 没有你们就没有龍魂系统
创建者: UID9622

功能: 扫描目录，按类型分类整理文件
"""

import os
import json
import shutil
import hashlib
from datetime import datetime
from collections import defaultdict
from pathlib import Path

# 配置
SCAN_DIRS = [
    os.path.expanduser("~/longhun-system"),
    os.path.expanduser("~/Desktop")
]
OUTPUT_DIR = os.path.expanduser("~/longhun-system/CNSH-整理版")

# 文件分类规则
FILE_CATEGORIES = {
    "代码类": {
        "extensions": [
            # 编程语言
            ".py", ".js", ".ts", ".jsx", ".tsx", ".mjs", ".cjs",
            ".java", ".c", ".cpp", ".h", ".hpp", ".cs", ".go",
            ".rs", ".rb", ".php", ".swift", ".kt", ".scala",
            ".r", ".m", ".mm", ".pl", ".pm", ".lua", ".dart",
            ".vue", ".svelte", ".elm",
            # 脚本
            ".sh", ".bash", ".zsh", ".fish", ".ps1", ".bat", ".cmd",
            # 配置/数据
            ".json", ".yaml", ".yml", ".toml", ".ini", ".cfg",
            ".xml", ".plist",
            # Web
            ".html", ".htm", ".css", ".scss", ".sass", ".less",
            # 数据库
            ".sql", ".db", ".sqlite", ".sqlite3",
            # CNSH
            ".cnsh",
            # 其他
            ".makefile", ".dockerfile", ".gitignore", ".env",
        ],
        "subdirs": {
            "Python": [".py", ".pyw", ".pyi"],
            "JavaScript": [".js", ".mjs", ".cjs", ".jsx"],
            "TypeScript": [".ts", ".tsx"],
            "Shell脚本": [".sh", ".bash", ".zsh"],
            "Go": [".go"],
            "C-C++": [".c", ".cpp", ".h", ".hpp"],
            "Swift": [".swift"],
            "CNSH中文编程": [".cnsh"],
            "Web前端": [".html", ".htm", ".css", ".scss", ".vue"],
            "配置文件": [".json", ".yaml", ".yml", ".toml", ".xml", ".plist"],
            "SQL数据库": [".sql", ".db", ".sqlite"],
            "其他代码": []  # 兜底
        }
    },
    "论文类": {
        "extensions": [".pdf", ".doc", ".docx", ".tex", ".bib", ".rtf"],
        "keywords": ["论文", "paper", "thesis", "研究", "report", "学术", "学位"],
        "subdirs": {
            "PDF文档": [".pdf"],
            "Word文档": [".doc", ".docx"],
            "LaTeX": [".tex", ".bib"],
            "其他论文": [".rtf"]
        }
    },
    "产品文档类": {
        "extensions": [".md", ".txt", ".rst", ".adoc"],
        "keywords": [
            "readme", "文档", "说明", "指南", "guide", "manual", "spec",
            "架构", "设计", "api", "changelog", "license", "规范",
            "产品", "需求", "prd", "使用", "教程", "tutorial"
        ],
        "subdirs": {
            "Markdown文档": [".md"],
            "纯文本": [".txt"],
            "其他文档": [".rst", ".adoc"]
        }
    },
    "其他类": {
        "extensions": [],  # 兜底
        "subdirs": {
            "图片资源": [".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp", ".ico", ".bmp"],
            "字体文件": [".ttf", ".otf", ".woff", ".woff2", ".eot"],
            "音视频": [".mp3", ".mp4", ".wav", ".avi", ".mov", ".mkv", ".webm"],
            "压缩包": [".zip", ".tar", ".gz", ".rar", ".7z", ".bz2"],
            "数据文件": [".csv", ".xlsx", ".xls"],
            "二进制": [".exe", ".dll", ".so", ".dylib", ".bin"],
            "其他": []
        }
    }
}

# 排除的目录和文件
EXCLUDE_DIRS = [
    "node_modules", ".git", "__pycache__", ".venv", "venv",
    ".cache", "cache", ".npm", ".Trash", "Trash",
    "build", "dist", ".next", ".nuxt"
]

EXCLUDE_FILES = [
    ".DS_Store", "Thumbs.db", ".gitkeep", "package-lock.json",
    "yarn.lock", "pnpm-lock.yaml"
]


def should_exclude(path):
    """检查是否应该排除"""
    path_parts = Path(path).parts
    for part in path_parts:
        if part in EXCLUDE_DIRS:
            return True
    filename = os.path.basename(path)
    if filename in EXCLUDE_FILES:
        return True
    # 排除隐藏文件夹中的文件
    if any(part.startswith('.') and part not in ['.cnsh', '.env'] for part in path_parts):
        return True
    return False


def get_file_hash(filepath, block_size=65536):
    """计算文件MD5哈希（用于去重）"""
    try:
        hasher = hashlib.md5()
        with open(filepath, 'rb') as f:
            buf = f.read(block_size)
            while len(buf) > 0:
                hasher.update(buf)
                buf = f.read(block_size)
        return hasher.hexdigest()
    except:
        return None


def categorize_file(filepath):
    """确定文件分类"""
    filename = os.path.basename(filepath).lower()
    ext = os.path.splitext(filename)[1].lower()

    # 检查代码类
    if ext in FILE_CATEGORIES["代码类"]["extensions"]:
        for subdir, exts in FILE_CATEGORIES["代码类"]["subdirs"].items():
            if ext in exts:
                return "代码类", subdir
        return "代码类", "其他代码"

    # 检查论文类
    if ext in FILE_CATEGORIES["论文类"]["extensions"]:
        for subdir, exts in FILE_CATEGORIES["论文类"]["subdirs"].items():
            if ext in exts:
                return "论文类", subdir
        return "论文类", "其他论文"

    # 检查产品文档类
    if ext in FILE_CATEGORIES["产品文档类"]["extensions"]:
        # 检查关键词确认是文档
        keywords = FILE_CATEGORIES["产品文档类"]["keywords"]
        filepath_lower = filepath.lower()
        if any(kw in filepath_lower for kw in keywords):
            for subdir, exts in FILE_CATEGORIES["产品文档类"]["subdirs"].items():
                if ext in exts:
                    return "产品文档类", subdir
            return "产品文档类", "其他文档"
        # MD文件默认归入产品文档
        if ext == ".md":
            return "产品文档类", "Markdown文档"
        if ext == ".txt":
            return "产品文档类", "纯文本"

    # 检查其他类的子分类
    for subdir, exts in FILE_CATEGORIES["其他类"]["subdirs"].items():
        if ext in exts:
            return "其他类", subdir

    return "其他类", "其他"


def scan_directories(dirs):
    """扫描目录收集文件"""
    files = []
    for dir_path in dirs:
        print(f"📂 扫描: {dir_path}")
        for root, dirs_list, files_list in os.walk(dir_path):
            # 过滤排除目录
            dirs_list[:] = [d for d in dirs_list if d not in EXCLUDE_DIRS and not d.startswith('.')]

            for filename in files_list:
                filepath = os.path.join(root, filename)
                if not should_exclude(filepath):
                    try:
                        stat = os.stat(filepath)
                        files.append({
                            "path": filepath,
                            "name": filename,
                            "size": stat.st_size,
                            "mtime": stat.st_mtime
                        })
                    except:
                        pass
    return files


def organize_files(files, output_dir):
    """整理文件到目标目录"""
    categories = defaultdict(lambda: defaultdict(list))
    seen_hashes = set()
    duplicates = []

    print(f"\n🔄 分类整理 {len(files)} 个文件...")

    for i, file_info in enumerate(files):
        if (i + 1) % 1000 == 0:
            print(f"   处理进度: {i + 1}/{len(files)}")

        filepath = file_info["path"]
        category, subdir = categorize_file(filepath)

        # 创建目标目录
        target_dir = os.path.join(output_dir, category, subdir)
        os.makedirs(target_dir, exist_ok=True)

        # 记录分类
        categories[category][subdir].append({
            "name": file_info["name"],
            "original_path": filepath,
            "size": file_info["size"],
            "mtime": datetime.fromtimestamp(file_info["mtime"]).isoformat()
        })

    return categories


def generate_index(categories, output_dir):
    """生成索引文件"""
    # 统计
    total_files = 0
    category_counts = {}

    for cat, subdirs in categories.items():
        cat_count = sum(len(files) for files in subdirs.values())
        category_counts[cat] = cat_count
        total_files += cat_count

    # 生成JSON索引
    index_data = {
        "meta": {
            "generated_at": datetime.now().isoformat(),
            "total_files": total_files,
            "generator": "文件分类整理工具 v1.0",
            "dna": "#龍芯⚡️2026-03-06-FileOrganizer-v1.0"
        },
        "summary": category_counts,
        "categories": {}
    }

    for cat, subdirs in categories.items():
        index_data["categories"][cat] = {
            "total": category_counts[cat],
            "subdirs": {
                subdir: len(files)
                for subdir, files in subdirs.items()
            }
        }

    # 写入主索引
    with open(os.path.join(output_dir, "文件分类索引.json"), 'w', encoding='utf-8') as f:
        json.dump(index_data, f, ensure_ascii=False, indent=2)

    # 生成Markdown索引
    md_content = f"""# 文件分类整理索引

```
DNA追溯码: #龍芯⚡️2026-03-06-FileOrganizer-v1.0
生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
总文件数: {total_files:,}
```

## 分类概览

| 分类 | 文件数 | 占比 |
|------|--------|------|
"""

    for cat, count in sorted(category_counts.items(), key=lambda x: -x[1]):
        pct = count / total_files * 100 if total_files > 0 else 0
        md_content += f"| {cat} | {count:,} | {pct:.1f}% |\n"

    md_content += f"\n## 详细分类\n\n"

    for cat, subdirs in sorted(categories.items()):
        md_content += f"### {cat}\n\n"
        md_content += "| 子分类 | 文件数 |\n"
        md_content += "|--------|--------|\n"
        for subdir, files in sorted(subdirs.items(), key=lambda x: -len(x[1])):
            md_content += f"| {subdir} | {len(files):,} |\n"
        md_content += "\n"

    with open(os.path.join(output_dir, "文件分类索引.md"), 'w', encoding='utf-8') as f:
        f.write(md_content)

    # 为每个分类生成详细索引
    for cat, subdirs in categories.items():
        cat_dir = os.path.join(output_dir, cat)
        os.makedirs(cat_dir, exist_ok=True)

        # 分类JSON
        with open(os.path.join(cat_dir, "_INDEX.json"), 'w', encoding='utf-8') as f:
            json.dump({
                "category": cat,
                "total": category_counts[cat],
                "subdirs": {
                    subdir: {
                        "count": len(files),
                        "files": files[:100]  # 只保存前100个文件详情
                    }
                    for subdir, files in subdirs.items()
                }
            }, f, ensure_ascii=False, indent=2)

        # 分类Markdown
        md = f"# {cat}\n\n共 **{category_counts[cat]:,}** 个文件\n\n"
        for subdir, files in sorted(subdirs.items(), key=lambda x: -len(x[1])):
            md += f"## {subdir} ({len(files):,}个)\n\n"
            md += "| 文件名 | 大小 | 修改时间 |\n"
            md += "|--------|------|----------|\n"
            for f_info in sorted(files, key=lambda x: x['mtime'], reverse=True)[:50]:
                size_kb = f_info['size'] / 1024
                size_str = f"{size_kb:.1f}KB" if size_kb < 1024 else f"{size_kb/1024:.1f}MB"
                name = f_info['name'][:40] + "..." if len(f_info['name']) > 40 else f_info['name']
                date = f_info['mtime'][:10]
                md += f"| {name} | {size_str} | {date} |\n"
            if len(files) > 50:
                md += f"\n*... 还有 {len(files) - 50} 个文件*\n"
            md += "\n"

        with open(os.path.join(cat_dir, "_索引.md"), 'w', encoding='utf-8') as f:
            f.write(md)

    return index_data


def main():
    print("=" * 60)
    print("🗂️ 文件分类整理工具 v1.0")
    print("DNA: #ZHUGEXIN | UID9622")
    print("=" * 60)
    print()

    # 扫描文件
    print("📂 开始扫描目录...")
    files = scan_directories(SCAN_DIRS)
    print(f"   找到 {len(files):,} 个文件")

    # 分类整理
    categories = organize_files(files, OUTPUT_DIR)

    # 生成索引
    print("\n📋 生成索引...")
    index = generate_index(categories, OUTPUT_DIR)

    # 输出统计
    print("\n" + "=" * 60)
    print("🎉 整理完成!")
    print("=" * 60)
    print(f"📁 输出目录: {OUTPUT_DIR}")
    print(f"📊 总文件数: {index['meta']['total_files']:,}")
    print("\n分类统计:")
    for cat, count in sorted(index['summary'].items(), key=lambda x: -x[1]):
        print(f"   {cat}: {count:,}")
    print("=" * 60)


if __name__ == "__main__":
    main()
