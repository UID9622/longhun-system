#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ═══════════════════════════════════════════════════════════
# lh_browser_package.py — 龍魂浏览器打包器
# DNA: #龍芯⚡️2026-08-24-LONGHUN-BROWSER-DEPLOY-v1.0-UID9622
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# 用途: 将编译产物打包为 .deb/.dmg/.zip，带 DNA 清单
# ═══════════════════════════════════════════════════════════
"""龍魂浏览器打包器：Linux .deb / macOS .dmg / 通用 .zip 打包。"""

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime
from pathlib import Path

BRAND = 'LonghunBrowser'
VERSION = '1.0.0'


def checksum_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def make_manifest(binary: Path, out_dir: Path) -> Path:
    """生成 DNA 追溯清单。"""
    manifest = {
        'brand': BRAND,
        'version': VERSION,
        'build_time': datetime.now().isoformat(),
        'binary': binary.name,
        'binary_sha256': checksum_file(binary),
        'source': 'chromium(BSD3)+ungoogled+longhun-layer',
        'dna': '#龍芯⚡️2026-08-24-LONGHUN-BROWSER-DEPLOY-v1.0-UID9622',
        'licenses': ['BSD 3-Clause (Chromium)', 'MulanPSL v2 (龍魂工程层)',
                     'CC BY-NC-SA 4.0 (龍魂思想层)'],
    }
    mf = out_dir / f'{BRAND}-{VERSION}-manifest.json'
    mf.write_text(json.dumps(manifest, ensure_ascii=False, indent=2))
    return mf


def pack_zip(binary: Path, out_dir: Path) -> Path:
    with tempfile.TemporaryDirectory() as td:
        appdir = Path(td) / f'{BRAND}.app' / 'Contents' / 'MacOS'
        appdir.mkdir(parents=True)
        shutil.copy2(binary, appdir / BRAND)
        zip_path = out_dir / f'{BRAND}-{VERSION}-macos-universal.zip'
        subprocess.run(['zip', '-qr', str(zip_path), '.'],
                       cwd=td, check=True)
    return zip_path


def pack_dmg(binary: Path, out_dir: Path) -> Path:
    """macOS 打包 .dmg（需 hdiutil；签名需 Apple 开发者账号）。"""
    dmg = out_dir / f'{BRAND}-{VERSION}-macos.dmg'
    with tempfile.TemporaryDirectory() as td:
        app = Path(td) / f'{BRAND}.app' / 'Contents' / 'MacOS'
        app.mkdir(parents=True)
        shutil.copy2(binary, app / BRAND)
        dmg_src = Path(td) / 'app'
        shutil.copytree(Path(td) / f'{BRAND}.app', dmg_src)
        subprocess.run([
            'hdiutil', 'create', '-volname', BRAND,
            '-srcfolder', str(dmg_src), '-ov', '-format', 'UDZO',
            str(dmg),
        ], check=True)
    return dmg


def pack_deb(binary: Path, out_dir: Path) -> Path:
    """Linux .deb 打包。"""
    deb = out_dir / f'{BRAND}-{VERSION}-linux-amd64.deb'
    with tempfile.TemporaryDirectory() as td:
        root = Path(td) / 'pkg'
        bindir = root / 'usr' / 'bin'
        bindir.mkdir(parents=True)
        shutil.copy2(binary, bindir / BRAND)
        debdir = root / 'DEBIAN'
        debdir.mkdir(parents=True)
        (debdir / 'control').write_text(
            f'Package: {BRAND}\nVersion: {VERSION}\n'
            f'Section: web\nPriority: optional\nArchitecture: amd64\n'
            f'Maintainer: Zhuge Xin <346045695@qq.com>\n'
            f'Description: LonghunBrowser - 中国自主数据主权浏览器\n'
            f' 基于Chromium(BSD3)+ungoogled+龍魂定制层\n')
        subprocess.run(['dpkg-deb', '--build', '--root-owner-group',
                        str(root), str(deb)], check=True)
    return deb


def main():
    ap = argparse.ArgumentParser(description='龍魂浏览器打包器')
    ap.add_argument('--binary', required=True, help='编译产物路径 (chrome)')
    ap.add_argument('--platform', choices=['macos', 'linux'],
                    default='macos')
    ap.add_argument('--output', default='.',
                    help='输出目录（默认当前目录）')
    ap.add_argument('--version', default=VERSION)
    args = ap.parse_args()

    global VERSION
    VERSION = args.version

    binary = Path(args.binary).expanduser().resolve()
    if not binary.exists():
        print(f'[🔴] 编译产物不存在: {binary}')
        sys.exit(2)

    out_dir = Path(args.output).expanduser().resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f'打包 {BRAND} v{VERSION} ({args.platform})')
    if args.platform == 'macos':
        pkg = pack_zip(binary, out_dir)
        print(f'  [🟢] {pkg.name} ({pkg.stat().st_size/1024/1024:.1f}MB)')
    elif args.platform == 'linux':
        try:
            pkg = pack_deb(binary, out_dir)
            print(f'  [🟢] {pkg.name} ({pkg.stat().st_size/1024/1024:.1f}MB)')
        except FileNotFoundError:
            print('  [🟡] dpkg-deb 不可用，回退 zip')
            pkg = pack_zip(binary, out_dir)
            print(f'  [🟡] 回退包: {pkg.name}')

    mf = make_manifest(binary, out_dir)
    print(f'  [🟢] DNA 清单: {mf.name}')
    print('打包完成')


if __name__ == '__main__':
    main()
