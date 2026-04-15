#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
☰☰ 龍🇨🇳魂 ☷ · 字体系统总索引
DNA: #龍芯⚡️2026-04-13-FONT-INDEX-v1.0
作者: 诸葛鑫（UID9622）
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
理论指导: 曾仕强老师（永恒显示）
献礼: 乔布斯·曾仕强·历代传递和平与爱的人

龍魂字体系统 · 五层架构 · 一键诊断
════════════════════════════════════════
  L1  CJK核心（Noto/思源）     → brew安装
  L2  中文美学（霞鹜文楷）     → brew安装
  L3  代码字体（JetBrains等）  → brew安装
  L4  Unicode兜底（Unifont）   → brew安装
  L5  CNSH龍魂自制（私有区）   → font_builder生成

脚本分布:
  bin/install_fonts.sh          五层Mac字体一键安装
  bin/font_manager.py           Flask字体管理中枢 :8081
  CNSH引擎/cnsh_font_engine_uid9622.py    原始引擎（贝塞尔→SVG）
  CNSH引擎/cnsh_font_builder.py           v1打包器（SVG→TTF）
  CNSH引擎/cnsh_font_builder_v2_LU.py     v2打包器（LU四层全链路）
  CNSH引擎/CNSH_字元库_v0001-v0015.json   15版字元库定义

DNA: #龍芯⚡️2026-04-13-FONT-INDEX-v1.0
"""

import json
import os
from pathlib import Path

DNA = "#龍芯⚡️2026-04-13-FONT-INDEX-v1.0"
BASE = Path.home() / "longhun-system"


def scan_glyph_libs():
    """扫描所有字元库JSON"""
    engine_dir = BASE / "CNSH引擎"
    libs = []
    for f in sorted(engine_dir.glob("CNSH_字元库_v*.json")):
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
            chars = data.get("字符集_cnsh9622", {})
            libs.append({
                "file": f.name,
                "version": f.stem.split("_v")[-1],
                "dna": data.get("DNA追溯码", "N/A"),
                "stage": data.get("阶段标识", "N/A"),
                "chars": len(chars),
            })
        except Exception as e:
            libs.append({"file": f.name, "error": str(e)})
    return libs


def scan_font_scripts():
    """扫描所有字体相关脚本"""
    scripts = [
        ("bin/install_fonts.sh", "五层Mac字体一键安装"),
        ("bin/font_manager.py", "Flask字体管理中枢"),
        ("CNSH引擎/cnsh_font_engine_uid9622.py", "原始贝塞尔引擎"),
        ("CNSH引擎/cnsh_font_builder.py", "v1 SVG→TTF打包器"),
        ("CNSH引擎/cnsh_font_builder_v2_LU.py", "v2 LU四层全链路打包器"),
    ]
    result = []
    for rel, desc in scripts:
        p = BASE / rel
        result.append({
            "path": rel,
            "desc": desc,
            "exists": p.exists(),
            "size_kb": round(p.stat().st_size / 1024, 1) if p.exists() else 0,
        })
    return result


def scan_font_outputs():
    """扫描已生成的字体文件"""
    out_dir = BASE / "CNSH引擎" / "CNSH_字体输出"
    fonts = []
    if out_dir.exists():
        for f in out_dir.glob("*.ttf"):
            fonts.append({
                "file": f.name,
                "size_kb": round(f.stat().st_size / 1024, 1),
            })
    return fonts


def scan_system_fonts():
    """检查系统已安装的关键字体"""
    font_dir = Path.home() / "Library" / "Fonts"
    check_list = [
        ("NotoSansCJK", "Noto Sans CJK"),
        ("NotoSerifCJK", "Noto Serif CJK"),
        ("SourceHanSans", "思源黑体"),
        ("SourceHanSerif", "思源宋体"),
        ("LXGWWenKai", "霞鹜文楷"),
        ("JetBrainsMono", "JetBrains Mono"),
        ("FiraCode", "Fira Code"),
        ("SarasaGothic", "更纱黑体"),
        ("cnsh_uid9622", "CNSH龍魂自制"),
    ]
    result = []
    all_fonts = list(font_dir.glob("*")) if font_dir.exists() else []
    all_names = [f.name for f in all_fonts]
    for key, name in check_list:
        found = any(key.lower() in fn.lower() for fn in all_names)
        result.append({"name": name, "key": key, "installed": found})
    return result


def diagnose():
    """一键诊断 · 全景报告"""
    print(f"🐉 龍魂字体系统 · 一键诊断")
    print(f"DNA: {DNA}")
    print("=" * 55)

    # 1. 字元库
    libs = scan_glyph_libs()
    print(f"\n📦 字元库: {len(libs)} 个版本")
    for l in libs:
        if "error" in l:
            print(f"   🔴 {l['file']}: {l['error']}")
        else:
            print(f"   🟢 {l['file']} | {l['chars']}字符 | {l['stage']}")

    # 2. 脚本
    scripts = scan_font_scripts()
    print(f"\n🔧 脚本: {len(scripts)} 个")
    for s in scripts:
        icon = "🟢" if s["exists"] else "🔴"
        print(f"   {icon} {s['path']} ({s['size_kb']}KB) — {s['desc']}")

    # 3. 已生成字体
    fonts = scan_font_outputs()
    print(f"\n🎨 已生成TTF: {len(fonts)} 个")
    for f in fonts:
        print(f"   🟢 {f['file']} ({f['size_kb']}KB)")

    # 4. 系统字体
    sys_fonts = scan_system_fonts()
    installed = sum(1 for f in sys_fonts if f["installed"])
    print(f"\n🖥️ 系统字体检测: {installed}/{len(sys_fonts)}")
    for f in sys_fonts:
        icon = "🟢" if f["installed"] else "⚪"
        print(f"   {icon} {f['name']}")

    # 汇总
    all_ok = all(s["exists"] for s in scripts) and len(libs) > 0
    print(f"\n{'=' * 55}")
    print(f"三色审计: {'🟢 全绿' if all_ok else '🟡 部分缺失'}")
    print(f"字元库演进: v0001 → v{libs[-1]['version'] if libs else '????'} ({len(libs)}个版本)")
    print(f"DNA: {DNA}")
    print(f"GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F")


if __name__ == "__main__":
    diagnose()
