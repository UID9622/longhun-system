#!/usr/bin/env python3
#龍芯⚡️2026-07-21-LONGHUN-ISOLATED-FILE-SCANNER-v1.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
龍魂孤立文件扫描器 v1.0
扫描 /Users/zuimeidedeyihan 下所有可能成为 v4.1.3 训练数据的孤立文件，
按来源分类、标记是否已索引、输出融合候选清单。

DNA: #龍芯⚡️2026-07-21-LONGHUN-ISOLATED-FILE-SCANNER-v1.0
"""
import hashlib
import json
import os
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path

ROOT = Path("/Users/zuimeidedeyihan")
OUT_DIR = Path("/Users/zuimeidedeyihan/.longhun/memory")
OUT_DIR.mkdir(parents=True, exist_ok=True)

DNA = f"#龍芯⚡️{datetime.utcnow().strftime('%Y%m%d%H%M%S')}-ISOLATED-SCAN"

# 已纳入训练/索引的目录（不算孤立）
INDEXED_PATHS = {
    "longhun-system/data/training",
    "longhun-system/data/sources",
    "longhun-system/public-content",
    "longhun-system/01_protocols",
    "_work/public_content_unified",
    "_work/public_content",
    "_work/claude_training_data",
    ".longhun/memory",
}

# 需要重点扫描的潜在孤立区域
CANDIDATE_AREAS = {
    "_work": "工作区/知识库/审计报告",
    ".longhun": "记忆/语音/学习管道/审计日志",
    ".cnsh": "CNSH 运行时数据与知识库",
    ".dragonsoul": "DNA 操作链",
    ".龍魂": "龍魂规则账本/审计/记忆空间",
    "longhun-system/_work/repos": "仓库镜像",
    "longhun-system/data/claude_extracted": "Claude 提取语料",
    "longhun-core": "longhun-core 子系统",
    "longhun-data": "longhun-data 子系统",
    "longhun-models": "longhun-models 子系统",
    "longhun-kimi-skills": "longhun-kimi-skills 子系统",
    "longhun-lu": "longhun-lu 子系统",
    "龍魂待整理": "待整理龍魂文档",
    "DragonSoul": "DragonSoul 数据",
    "dragon_soul": "dragon_soul 数据",
}

# 排除的目录名
EXCLUDED_DIR_NAMES = {
    ".git", "node_modules", ".venv", "venv", "__pycache__", ".tox", "build", "dist",
    ".pytest_cache", ".mypy_cache", ".eggs", "models", "lora_output_v411", "lora_output_v412",
    "lora_output_v413", "yi1.5-9b-chat-mlx", "gguf", "checkpoints", ".cache", ".local",
    ".npm", ".nvm", ".ollama", "Applications", "Desktop", "Documents", "Movies",
    "Music", "Pictures", "Public", "Library", "Downloads", "nltk_data",
    "voice-twin", "brain_old", "mirror", "site-packages",
}

# 路径子串排除（任何路径包含这些子串之一即跳过）
EXCLUDED_PATH_SUBSTRINGS = {
    "/_archive/", "/archive/", "/logs/", "/.archive/", "/longhun_memory_backup/",
    "/workspaceStorage/", "/venv_", "/site-packages/", "/mirror/",
    "/brain_old/", "/voice-twin/",
}

# 排除的扩展名（二进制/非文本/已处理）
EXCLUDED_EXTENSIONS = {
    ".otf", ".ttf", ".woff", ".woff2", ".png", ".jpg", ".jpeg", ".gif", ".bmp",
    ".ico", ".mp3", ".mp4", ".m4a", ".wav", ".avi", ".mov", ".zip", ".tar",
    ".gz", ".bz2", ".xz", ".7z", ".rar", ".bin", ".exe", ".dll", ".so", ".dylib",
    ".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".pyc", ".pyo",
    ".class", ".jar", ".war", ".ear", ".safetensors", ".gguf", ".pt", ".pth", ".onnx",
    ".h5", ".pb", ".ckpt", ".npy", ".npz", ".pkl", ".pickle",
    ".db", ".sqlite", ".sqlite3", ".bundle", ".qta", ".aiff", ".dmg", ".vscdb",
    ".cubin", ".asm", ".backup",
}

# 文本扩展名优先级
TEXT_EXTENSIONS = {".md", ".txt", ".json", ".jsonl", ".yaml", ".yml", ".csv", ".tsv", ".py", ".sh"}


def is_indexed(path: Path) -> bool:
    """判断文件是否位于已索引目录下。"""
    rel = path.relative_to(ROOT)
    rel_str = str(rel).replace("\\", "/")
    for indexed in INDEXED_PATHS:
        if rel_str.startswith(indexed):
            return True
    return False


def classify_by_area(path: Path) -> str:
    """根据相对路径判断所属区域。"""
    rel = path.relative_to(ROOT)
    rel_str = str(rel).replace("\\", "/")
    for area, desc in CANDIDATE_AREAS.items():
        if rel_str.startswith(area):
            return desc
    if is_indexed(path):
        return "已索引/训练数据"
    return "其他孤立文件"


def classify_by_extension(path: Path) -> str:
    """根据扩展名判断文件类型。"""
    ext = path.suffix.lower()
    if ext in {".md"}:
        return "Markdown"
    if ext in {".txt"}:
        return "纯文本"
    if ext in {".json", ".jsonl"}:
        return "JSON/JSONL"
    if ext in {".yaml", ".yml"}:
        return "YAML"
    if ext in {".csv", ".tsv"}:
        return "表格数据"
    if ext in {".py", ".sh", ".js", ".ts", ".html", ".css"}:
        return "代码脚本"
    return "其他文本"


def quick_hash(path: Path, size: int = 8192) -> str:
    """快速计算文件前 8KB 的 MD5，用于去重。"""
    try:
        with open(path, "rb") as f:
            data = f.read(size)
        return hashlib.md5(data).hexdigest()[:16]
    except Exception:
        return ""


def scan():
    files_by_area = defaultdict(list)
    files_by_type = defaultdict(list)
    total_size = 0
    count = 0

    print(f"[{DNA}] 开始扫描 {ROOT} ...", file=sys.stderr)

    for dirpath, dirnames, filenames in os.walk(ROOT):
        # 原地修改 dirnames 以跳过排除目录
        dirnames[:] = [d for d in dirnames if d not in EXCLUDED_DIR_NAMES and not d.startswith(".")]

        current = Path(dirpath)
        for fname in filenames:
            fpath = current / fname
            rel_str = str(fpath.relative_to(ROOT)).replace("\\", "/")
            ext = fpath.suffix.lower()

            # 路径子串排除
            if any(sub in rel_str for sub in EXCLUDED_PATH_SUBSTRINGS):
                continue
            if ext in EXCLUDED_EXTENSIONS:
                continue
            if fname.startswith("."):
                continue

            try:
                stat = fpath.stat()
                size = stat.st_size
            except (OSError, PermissionError):
                continue

            if size == 0:
                continue

            area = classify_by_area(fpath)
            ftype = classify_by_extension(fpath)
            indexed = is_indexed(fpath)
            fhash = quick_hash(fpath)

            record = {
                "path": str(fpath),
                "relative": str(fpath.relative_to(ROOT)).replace("\\", "/"),
                "size": size,
                "mtime": datetime.utcfromtimestamp(stat.st_mtime).isoformat() + "Z",
                "area": area,
                "type": ftype,
                "indexed": indexed,
                "hash_prefix": fhash,
            }

            files_by_area[area].append(record)
            files_by_type[ftype].append(record)
            total_size += size
            count += 1

    result = {
        "dna": DNA,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "root": str(ROOT),
        "total_files": count,
        "total_size_bytes": total_size,
        "total_size_mb": round(total_size / 1024 / 1024, 2),
        "by_area": {k: len(v) for k, v in files_by_area.items()},
        "by_type": {k: len(v) for k, v in files_by_type.items()},
        "files": sorted(
            [f for group in files_by_area.values() for f in group],
            key=lambda x: x["size"],
            reverse=True,
        ),
    }

    json_path = OUT_DIR / "isolated_files_inventory.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    md_path = OUT_DIR / "isolated_files_inventory.md"
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(f"# 龍魂孤立文件扫描报告\n\n")
        f.write(f"> DNA: `{DNA}`\n\n")
        f.write(f"> 扫描时间: {result['timestamp']}\n\n")
        f.write(f"## 汇总\n\n")
        f.write(f"- 总文件数: **{count}**\n")
        f.write(f"- 总大小: **{result['total_size_mb']} MB**\n")
        f.write(f"- 已索引文件: **{sum(1 for x in result['files'] if x['indexed'])}**\n")
        f.write(f"- 孤立候选文件: **{sum(1 for x in result['files'] if not x['indexed'])}**\n\n")

        f.write("## 按区域分布\n\n")
        f.write("| 区域 | 文件数 | 大小 (MB) |\n")
        f.write("|:---|---:|---:|\n")
        for area, records in sorted(files_by_area.items(), key=lambda x: -len(x[1])):
            area_size = sum(r["size"] for r in records) / 1024 / 1024
            f.write(f"| {area} | {len(records)} | {area_size:.2f} |\n")

        f.write("\n## 按类型分布\n\n")
        f.write("| 类型 | 文件数 | 大小 (MB) |\n")
        f.write("|:---|---:|---:|\n")
        for ftype, records in sorted(files_by_type.items(), key=lambda x: -len(x[1])):
            type_size = sum(r["size"] for r in records) / 1024 / 1024
            f.write(f"| {ftype} | {len(records)} | {type_size:.2f} |\n")

        f.write("\n## 孤立候选文件 Top 100（按大小）\n\n")
        f.write("| 路径 | 区域 | 类型 | 大小 (KB) | 已索引 |\n")
        f.write("|:---|:---|---:|---:|:---:|\n")
        for r in result["files"][:100]:
            if r["indexed"]:
                continue
            size_kb = r["size"] / 1024
            f.write(
                f"| `{r['relative']}` | {r['area']} | {r['type']} | {size_kb:.1f} | {'✅' if r['indexed'] else '❌'} |\n"
            )

    print(f"[{DNA}] 扫描完成。", file=sys.stderr)
    print(f"JSON: {json_path}", file=sys.stderr)
    print(f"MD:   {md_path}", file=sys.stderr)
    print(f"文件数: {count}, 总大小: {result['total_size_mb']} MB", file=sys.stderr)


if __name__ == "__main__":
    scan()
