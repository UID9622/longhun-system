#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA追溯码:#龍芯⚡️2026-07-25-LONGHUN-FONT-RENAME-OPT-v1.0
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
"""
龍魂字体重命名与优化脚本
- 将字体显示名改为「龙魂字体」
- 保留 PostScript 名为 LonghunFont-Regular（兼容性）
- 生成 WOFF2 网页字体
- 输出优化报告
"""
import json
import os
import shutil
from datetime import datetime
from pathlib import Path

from fontTools.ttLib import TTFont


def update_name_table(font, new_family_cn="龙魂字体", ps_name="LonghunFont-Regular"):
    """更新字体名称表：中文显示名 + 英文兼容名"""
    name_table = font['name']
    version = "Version 1.001"
    full_name_cn = f"{new_family_cn} Regular"
    full_name_en = "LonghunFont Regular"
    unique_id = f"{ps_name}-1.001"
    copyright_str = "龙魂字体 by UID9622 · DNA追溯 #龍芯⚡️ · Licensed under SIL Open Font License 1.1"
    manufacturer = "龍魂系统 · UID9622"

    # platformID=1 (Mac), platformID=3 (Windows)
    # 清空旧 name 记录，重新写入
    name_table.names = []

    # Mac 平台用 ASCII-only 字符串（mac_roman 编码不支持中文）
    copyright_en = "LonghunFont by UID9622 · DNA Traceability · Licensed under SIL Open Font License 1.1"
    manufacturer_en = "LongHun System · UID9622"

    records = [
        # Mac (platformID=1, encodingID=0, languageID=0) — 仅 ASCII，兼容性
        (1, 0, 0, 0, copyright_en),
        (1, 0, 0, 1, "LonghunFont"),   # 英文族名，mac_roman 可编码
        (1, 0, 0, 2, "Regular"),
        (1, 0, 0, 3, unique_id),
        (1, 0, 0, 4, full_name_en),
        (1, 0, 0, 5, version),
        (1, 0, 0, 6, ps_name),
        (1, 0, 0, 8, manufacturer_en),
        (1, 0, 0, 9, "UID9622"),

        # Windows 英文 (platformID=3, encodingID=1, languageID=1033)
        (3, 1, 1033, 0, copyright_str),
        (3, 1, 1033, 1, "LonghunFont"),
        (3, 1, 1033, 2, "Regular"),
        (3, 1, 1033, 3, unique_id),
        (3, 1, 1033, 4, full_name_en),
        (3, 1, 1033, 5, version),
        (3, 1, 1033, 6, ps_name),
        (3, 1, 1033, 8, manufacturer),
        (3, 1, 1033, 9, "UID9622"),

        # Windows 中文 (platformID=3, encodingID=1, languageID=2052) — 主显示名
        (3, 1, 2052, 0, copyright_str),
        (3, 1, 2052, 1, new_family_cn),
        (3, 1, 2052, 2, "Regular"),
        (3, 1, 2052, 3, unique_id),
        (3, 1, 2052, 4, full_name_cn),
        (3, 1, 2052, 5, version),
        (3, 1, 2052, 6, ps_name),
        (3, 1, 2052, 8, manufacturer),
        (3, 1, 2052, 9, "UID9622"),
    ]

    for platform_id, plat_enc_id, lang_id, name_id, string in records:
        name_table.setName(string, name_id, platform_id, plat_enc_id, lang_id)


def generate_woff2(input_otf_path, output_path):
    """生成 WOFF2 字体"""
    woff2_font = TTFont(str(input_otf_path))
    woff2_font.flavor = 'woff2'
    woff2_font.save(str(output_path))
    return output_path


def main():
    base_dir = Path(__file__).resolve().parent.parent
    input_otf = base_dir / "output" / "LonghunFont-Regular.otf"
    output_otf = base_dir / "output" / "龙魂字体-Regular.otf"
    output_woff2 = base_dir / "output" / "龙魂字体-Regular.woff2"
    report_path = base_dir / "output" / "optimization_report.json"

    if not input_otf.exists():
        print(f"❌ 输入字体不存在: {input_otf}")
        return 1

    print(f"[1/5] 加载字体: {input_otf}")
    font = TTFont(input_otf)
    original_size = input_otf.stat().st_size
    glyph_count = len(font.getGlyphSet())

    print(f"[2/5] 更新名称为「龙魂字体」")
    update_name_table(font)

    print(f"[3/5] 保存新 OTF: {output_otf}")
    font.save(output_otf)
    otf_size = output_otf.stat().st_size

    print(f"[4/5] 生成 WOFF2: {output_woff2}")
    generate_woff2(output_otf, output_woff2)
    woff2_size = output_woff2.stat().st_size

    print(f"[5/5] 写入优化报告")
    report = {
        "dna": "#龍芯⚡️2026-07-25-LONGHUN-FONT-OPTIMIZE-v1.0",
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "original_file": str(input_otf),
        "original_size_bytes": original_size,
        "original_size_mb": round(original_size / 1024 / 1024, 2),
        "output_otf": str(output_otf),
        "output_otf_size_bytes": otf_size,
        "output_otf_size_mb": round(otf_size / 1024 / 1024, 2),
        "output_woff2": str(output_woff2),
        "output_woff2_size_bytes": woff2_size,
        "output_woff2_size_mb": round(woff2_size / 1024 / 1024, 2),
        "woff2_compression_ratio": round(woff2_size / original_size, 3),
        "glyph_count": glyph_count,
        "family_name_cn": "龙魂字体",
        "ps_name": "LonghunFont-Regular",
        "version": "Version 1.001"
    }

    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print("\n✅ 完成")
    print(f"   原始 OTF: {report['original_size_mb']} MB")
    print(f"   新 OTF:   {report['output_otf_size_mb']} MB")
    print(f"   WOFF2:    {report['output_woff2_size_mb']} MB (压缩率 {report['woff2_compression_ratio']})")
    print(f"   字形数:   {glyph_count}")

    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
