#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""
龍魂 · 华为 eNSP 官方依赖下载助手 v1.0
DNA: #龍芯⚡️丙午·甲午·己卯·庚午·䷚颐-ENSP-DOWNLOADER-v1.0

功能：
- 自动从官方渠道下载 eNSP 所需的三大依赖：
  VirtualBox 5.2.44、Wireshark 4.4.5 x64、WinPcap 4.1.3。
- 下载完成后立即校验 SHA-256，防止篡改。
- eNSP 主程序因华为官网需登录，不提供自动下载，只输出官方指引。

用法：
    python3 ensp_downloader.py --output ~/Downloads/龍魂_eNSP_套件
    python3 ensp_downloader.py --output ~/Downloads/龍魂_eNSP_套件 --skip-verify
"""

import argparse
import hashlib
import json
import os
import sys
import urllib.request
from pathlib import Path

DNA = "#龍芯⚡️丙午·甲午·己卯·庚午·䷚颐-ENSP-DOWNLOADER-v1.0"
CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"


def load_hash_library(json_path: Path) -> dict[str, Any]:
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)


def compute_sha256(file_path: Path) -> str:
    h = hashlib.sha256()
    with open(file_path, "rb") as f:
        while True:
            chunk = f.read(8192 * 1024)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def download(url: str, dest: Path, timeout: int = 300) -> bool:
    """使用 urllib 下载文件，返回是否成功。"""
    try:
        print(f"   ⬇️  开始下载: {url}")
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (LongHun-ENSP-Downloader/1.0)"})
        with urllib.request.urlopen(req, timeout=timeout) as response:
            total = response.headers.get("Content-Length")
            total = int(total) if total else None
            downloaded = 0
            block = 128 * 1024
            with open(dest, "wb") as f:
                while True:
                    chunk = response.read(block)
                    if not chunk:
                        break
                    f.write(chunk)
                    downloaded += len(chunk)
                    if total:
                        pct = downloaded / total * 100
                        print(f"\r   📥 {pct:6.2f}% ({downloaded:,}/{total:,} 字节)", end="", flush=True)
            print()  # newline after progress
        return True
    except Exception as e:
        print(f"\n   ❌ 下载失败: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="龍魂 · 华为 eNSP 官方依赖下载助手",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--output",
        type=str,
        default="~/Downloads/龍魂_eNSP_套件",
        help="下载保存目录（默认：~/Downloads/龍魂_eNSP_套件）",
    )
    parser.add_argument(
        "--skip-verify",
        action="store_true",
        help="跳过下载后的哈希校验（不推荐）",
    )
    parser.add_argument(
        "--json",
        type=str,
        default=None,
        help="指定哈希库 JSON 文件路径",
    )
    args = parser.parse_args()

    output_dir = Path(args.output).expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    # 定位哈希库
    if args.json:
        json_path = Path(args.json).expanduser().resolve()
    else:
        json_path = Path(__file__).with_name("ensp_hashes.json").resolve()

    if not json_path.exists():
        print(f"❌ 找不到哈希库文件: {json_path}")
        sys.exit(1)

    library = load_hash_library(json_path)
    sources = library.get("sources", {})

    print("=" * 70)
    print("龍魂 · 华为 eNSP 官方依赖下载助手")
    print("=" * 70)
    print(f"保存目录: {output_dir}")
    print(f"哈希库:   {json_path}")
    print()

    # 自动下载三大公开依赖
    auto_download_keys = [
        "VirtualBox-5.2.44-139111-Win.exe",
        "Wireshark-4.4.5-x64.exe",
        "WinPcap_4_1_3.exe",
    ]

    all_ok = True
    for key in auto_download_keys:
        entry = sources.get(key)
        if not entry:
            print(f"⚠️  哈希库中缺少 {key}，跳过。")
            all_ok = False
            continue

        url = entry.get("url")
        expected_sha256 = entry.get("sha256")
        dest = output_dir / key

        print(f"\n📦 {entry.get('name', key)}")
        print(f"   官方链接: {url}")

        if dest.exists():
            print(f"   ℹ️  文件已存在: {dest}")
        else:
            if not download(url, dest):
                all_ok = False
                continue

        if not args.skip_verify and expected_sha256:
            actual_sha256 = compute_sha256(dest)
            if actual_sha256.lower() == expected_sha256.lower():
                print(f"   ✅ SHA-256 校验通过")
            else:
                print(f"   ❌ SHA-256 校验失败")
                print(f"      期望: {expected_sha256}")
                print(f"      实际: {actual_sha256}")
                all_ok = False

    # eNSP 主程序特殊处理
    ensp_entry = sources.get("eNSP_Setup.exe")
    if ensp_entry:
        print("\n📦 华为 eNSP 主程序（V100R003C00SPC100）")
        print("   ⚠️  该软件需登录华为企业技术支持后下载，本工具不自动下载。")
        print(f"   官方下载页: {ensp_entry.get('url')}")
        print("   下载完成后，请将其放入同一目录，再运行 ensp_hash_checker.py 校验。")

    print("\n" + "=" * 70)
    if all_ok:
        print("🎉 全部官方依赖下载并校验完成。")
    else:
        print("⚠️  部分步骤未完成，请根据上方提示处理。")
    print(f"DNA: {DNA}")
    print(f"CONFIRM: {CONFIRM}")
    print("=" * 70)


if __name__ == "__main__":
    main()
