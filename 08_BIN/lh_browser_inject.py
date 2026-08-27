#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ═══════════════════════════════════════════════════════════
# lh_browser_inject.py — 龍魂定制层注入器
# DNA: #龍芯⚡️2026-08-24-LONGHUN-BROWSER-DEPLOY-v1.0-UID9622
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# 用途: 向 Chromium 源码注入 CNSH 翻译/审计/导出/DNA 模块 + 品牌替换
# ═══════════════════════════════════════════════════════════
"""龍魂浏览器注入器：品牌替换 + 龍魂模块落位 + 构建GN钩子。"""

import argparse
import os
import shutil
import sys
from pathlib import Path

# 龍魂模块清单（源 → Chromium 源码内落位）
LH_MODULES = {
    'lh_cnsh_transpiler.py': 'chrome/browser/longhun/cnsh_transpiler.py',
    'lh_browser_audit_middleware.py': 'chrome/browser/longhun/audit_middleware.py',
    'lh_export_engine.py': 'chrome/browser/longhun/export_engine.py',
    'lh_dna_verify.py': 'chrome/browser/longhun/dna_verify.py',
}

# 品牌替换（Chromium 显示名 → 龍魂品牌）
BRAND_OVERRIDES = {
    'PRODUCT_NAME': 'LonghunBrowser',
    'PRODUCT_STRING': 'LonghunBrowser',
    'Chromium': 'LonghunBrowser',
}

AUDIT = {'injected': [], 'errors': [], 'skipped': []}


def find_tool(tool_name: str, search_dirs: list):
    """在多目录中查找工具源文件。"""
    for d in search_dirs:
        p = Path(d) / tool_name
        if p.exists():
            return p
    return None


def inject_modules(src_dir: Path, lh_tools: list) -> None:
    """注入龍魂模块到 chrome/browser/longhun/。"""
    target_dir = src_dir / 'chrome' / 'browser' / 'longhun'
    target_dir.mkdir(parents=True, exist_ok=True)
    (target_dir / '__init__.py').touch()

    for tool_name, rel in LH_MODULES.items():
        source = find_tool(tool_name, lh_tools)
        if not source:
            AUDIT['skipped'].append(f'{tool_name} (源未找到)')
            continue
        dest = src_dir / rel
        shutil.copy2(source, dest)
        AUDIT['injected'].append(rel)


def inject_brand(src_dir: Path, version: str) -> None:
    """品牌替换：修改 app 名称相关常量（仅改开源显示名，不碰商标）。"""
    ver_file = src_dir / 'chrome' / 'VERSION'
    if ver_file.exists():
        txt = ver_file.read_text()
        major = version.split('.')[0]
        txt = txt.replace('MAJOR=1', f'MAJOR={major}') \
                 .replace('MAJOR=2', f'MAJOR={major}') \
                 .replace('MAJOR=3', f'MAJOR={major}')
        ver_file.write_text(txt)
        AUDIT['injected'].append('chrome/VERSION 品牌化')

    # 主要品牌常量文件
    targets = [
        src_dir / 'chrome' / 'app' / 'chrome_strings.grd',
        src_dir / 'chrome' / 'app' / 'theme' / 'BRANDING',
    ]
    for t in targets:
        if not t.exists():
            continue
        try:
            txt = t.read_text(encoding='utf-8', errors='ignore')
            for old, new in BRAND_OVERRIDES.items():
                txt = txt.replace(old, new)
            t.write_text(txt, encoding='utf-8')
            AUDIT['injected'].append(f'{t.relative_to(src_dir)} 品牌化')
        except Exception as e:
            AUDIT['errors'].append(f'{t}: {e}')


def write_gn_hook(src_dir: Path, brand: str) -> None:
    """生成龍魂构建 GN 文件。"""
    lh_dir = src_dir / 'chrome' / 'browser' / 'longhun'
    gn = lh_dir / 'BUILD.gn'
    gn.write_text(f'''# 龍魂浏览器模块构建
# DNA: #龍芯⚡️2026-08-24-LONGHUN-BROWSER-DEPLOY-v1.0-UID9622

import("//chrome/common/features.gni")

python_library("cnsh_transpiler") {{
  sources = [ "cnsh_transpiler.py" ]
}}

python_library("audit_middleware") {{
  sources = [ "audit_middleware.py" ]
}}

python_library("export_engine") {{
  sources = [ "export_engine.py" ]
}}

brand = "{brand}"
''')
    AUDIT['injected'].append('BUILD.gn 生成')


def main():
    ap = argparse.ArgumentParser(description='龍魂浏览器定制层注入器')
    ap.add_argument('--src', required=True, help='Chromium 源码根目录 (src/)')
    ap.add_argument('--lh-tools', action='append', default=[],
                    help='龍魂工具目录（可多次指定）')
    ap.add_argument('--inject-cnsh', action='store_true')
    ap.add_argument('--inject-audit', action='store_true')
    ap.add_argument('--inject-export', action='store_true')
    ap.add_argument('--inject-dna', action='store_true')
    ap.add_argument('--brand', default='LonghunBrowser')
    ap.add_argument('--version', default='1.0.0')
    args = ap.parse_args()

    src_dir = Path(args.src).expanduser().resolve()
    if not (src_dir / 'chrome').exists():
        print(f'[🔴] 无效 Chromium 源码目录: {src_dir} '
              f'(缺少 chrome/ 子目录)')
        sys.exit(2)

    # 默认龍魂工具路径
    lh_tools = list(args.lh_tools)
    default_dirs = [
        Path(__file__).parent,                      # 本脚本所在目录
        Path.home() / 'lh-tools' / 'bin',
        Path(__file__).parent.parent / '08_BIN',
    ]
    for d in default_dirs:
        if d not in lh_tools:
            lh_tools.append(str(d))

    any_flag = (args.inject_cnsh or args.inject_audit
                or args.inject_export or args.inject_dna)
    if any_flag:
        inject_modules(src_dir, lh_tools)
    else:
        inject_modules(src_dir, lh_tools)

    inject_brand(src_dir, args.version)
    write_gn_hook(src_dir, args.brand)

    print('龍魂定制层注入完成:')
    for item in AUDIT['injected']:
        print(f'  [🟢] {item}')
    for item in AUDIT['skipped']:
        print(f'  [🟡] 跳过: {item}')
    for item in AUDIT['errors']:
        print(f'  [🔴] {item}')

    if AUDIT['errors']:
        sys.exit(1)


if __name__ == '__main__':
    main()
