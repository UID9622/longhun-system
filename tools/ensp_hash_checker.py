#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂 · 华为 eNSP 套件哈希校验工具 v1.0
DNA: #龍芯⚡️2026-07-04-ENSP-HASH-CHECKER-v1.0

功能：
- 批量校验 eNSP 安装包及其依赖的 SHA-256 / MD5 哈希值。
- 与 tools/ensp_hashes.json 中的官方指纹比对。
- 识别文件名，自动匹配已知软件。

用法：
    python3 ensp_hash_checker.py --file VirtualBox-5.2.44-139111-Win.exe
    python3 ensp_hash_checker.py --dir ~/Downloads/龍魂_eNSP_套件
    python3 ensp_hash_checker.py --dir . --json ../tools/ensp_hashes.json
"""

import argparse
import hashlib
import json
import os
import sys
from pathlib import Path

DNA = "#龍芯⚡️2026-07-04-ENSP-HASH-CHECKER-v1.0"
CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"


def load_hash_library(json_path: Path) -> dict:
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)


def compute_hash(file_path: Path, algorithm: str = "sha256") -> str:
    h = hashlib.new(algorithm)
    with open(file_path, "rb") as f:
        while True:
            chunk = f.read(8192 * 1024)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def match_known_file(filename: str, library: dict) -> tuple:
    """根据文件名在哈希库中查找对应条目，返回 (key, entry) 或 (None, None)。"""
    lower = filename.lower()
    for key, entry in library.get("sources", {}).items():
        if key.lower() in lower or lower in key.lower():
            return key, entry
    return None, None


def check_file(file_path: Path, library: dict) -> dict:
    filename = file_path.name
    key, entry = match_known_file(filename, library)
    result = {
        "file": str(file_path),
        "filename": filename,
        "known": entry is not None,
        "matched_key": key,
        "size": file_path.stat().st_size,
        "sha256_ok": None,
        "md5_ok": None,
        "size_ok": None,
        "messages": [],
    }

    if not entry:
        result["messages"].append("⚠️  未在哈希库中找到该文件的官方指纹，请核对文件名或手动校验。")
        return result

    actual_sha256 = compute_hash(file_path, "sha256")
    result["actual_sha256"] = actual_sha256
    expected_sha256 = entry.get("sha256")
    if expected_sha256:
        result["sha256_ok"] = actual_sha256.lower() == expected_sha256.lower()
        if result["sha256_ok"]:
            result["messages"].append("✅ SHA-256 校验通过")
        else:
            result["messages"].append(f"❌ SHA-256 不匹配：期望 {expected_sha256}，实际 {actual_sha256}")
    else:
        result["messages"].append("ℹ️  哈希库中未记录该文件的 SHA-256，请从官方渠道下载后手动补充。")

    expected_md5 = entry.get("md5")
    if expected_md5:
        actual_md5 = compute_hash(file_path, "md5")
        result["actual_md5"] = actual_md5
        result["md5_ok"] = actual_md5.lower() == expected_md5.lower()
        if result["md5_ok"]:
            result["messages"].append("✅ MD5 校验通过")
        else:
            result["messages"].append(f"❌ MD5 不匹配：期望 {expected_md5}，实际 {actual_md5}")

    expected_size = entry.get("size_bytes")
    if expected_size:
        result["size_ok"] = result["size"] == expected_size
        if result["size_ok"]:
            result["messages"].append("✅ 文件大小匹配")
        else:
            result["messages"].append(f"⚠️  文件大小不匹配：期望 {expected_size} 字节，实际 {result['size']} 字节")

    return result


def scan_directory(dir_path: Path, library: dict) -> list:
    results = []
    for item in dir_path.iterdir():
        if item.is_file():
            results.append(check_file(item, library))
    return results


def print_report(results: list):
    print("\n" + "=" * 70)
    print("龍魂 · 华为 eNSP 套件哈希校验报告")
    print("=" * 70)
    all_pass = True
    for r in results:
        print(f"\n📦 {r['filename']}")
        print(f"   路径: {r['file']}")
        print(f"   大小: {r['size']:,} 字节")
        if not r["known"]:
            print("   " + "\n   ".join(r["messages"]))
            all_pass = False
            continue
        if r["sha256_ok"] is False or r["md5_ok"] is False or r["size_ok"] is False:
            all_pass = False
        for msg in r["messages"]:
            print(f"   {msg}")

    print("\n" + "=" * 70)
    if all_pass:
        print("🎉 全部已知文件校验通过，文件未被篡改。")
    else:
        print("⚠️  存在校验失败或未知的文件，请重新从官方渠道下载。")
    print(f"DNA: {DNA}")
    print(f"CONFIRM: {CONFIRM}")
    print("=" * 70)


def main():
    parser = argparse.ArgumentParser(
        description="龍魂 · 华为 eNSP 套件哈希校验工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--file", type=str, help="校验单个文件")
    parser.add_argument("--dir", type=str, help="校验整个目录")
    parser.add_argument(
        "--json",
        type=str,
        default=None,
        help="指定哈希库 JSON 文件路径（默认：工具同目录下的 ensp_hashes.json）",
    )
    args = parser.parse_args()

    if not args.file and not args.dir:
        parser.print_help()
        sys.exit(1)

    # 定位哈希库
    if args.json:
        json_path = Path(args.json).expanduser().resolve()
    else:
        json_path = Path(__file__).with_name("ensp_hashes.json").resolve()

    if not json_path.exists():
        print(f"❌ 找不到哈希库文件: {json_path}")
        print("请确保 ensp_hashes.json 与本工具在同一目录，或使用 --json 指定路径。")
        sys.exit(2)

    library = load_hash_library(json_path)
    results = []

    if args.file:
        file_path = Path(args.file).expanduser().resolve()
        if not file_path.exists():
            print(f"❌ 文件不存在: {file_path}")
            sys.exit(3)
        results.append(check_file(file_path, library))

    if args.dir:
        dir_path = Path(args.dir).expanduser().resolve()
        if not dir_path.exists():
            print(f"❌ 目录不存在: {dir_path}")
            sys.exit(4)
        results.extend(scan_directory(dir_path, library))

    print_report(results)


if __name__ == "__main__":
    main()
