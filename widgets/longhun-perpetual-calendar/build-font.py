# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂万年历字体构建脚本
DNA: #龍芯⚡️2026-06-27-LONGHUN-CALENDAR-FONT-BUILD-v1.0

原始 LonghunFont-Regular.otf 为品牌占位字体（不含完整 CJK 字形），
本脚本基于 SIL OFL 1.1 授权的 Noto Sans SC 生成带 LonghunFont 品牌名的
实用 TTF/WOFF2，确保日历在网页端仅使用 LonghunFont 即可正确渲染中文。
"""

import os
import sys
from pathlib import Path

from fontTools.ttLib import TTFont
from fontTools.varLib import instancer
from fontTools.subset import Subsetter


def load_needed_chars(widget_dir: Path) -> str:
    """从万年历源文件中提取所有需要渲染的字符。"""
    chars = set()
    for filename in ['index.html', 'calendar.js', 'sovereignty.js', 'styles.css']:
        path = widget_dir / filename
        if not path.exists():
            continue
        text = path.read_text(encoding='utf-8')
        for ch in text:
            if ord(ch) > 127:
                chars.add(ch)
    # 导航箭头
    for ch in '◀▶':
        chars.add(ch)
    # 补充常用 ASCII（DNA、日期格式、分隔符）
    ascii_needed = ''' !"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~'''
    return ''.join(chars) + ascii_needed


def find_noto_sans_sc() -> Path:
    """在常见位置查找 Noto Sans SC 可变字体。"""
    candidates = [
        Path('/Library/Fonts/NotoSansSC-VariableFont_wght.ttf'),
        Path.home() / 'Library/Fonts/NotoSansSC-VariableFont_wght.ttf',
        Path('/usr/share/fonts/truetype/noto/NotoSansSC-Regular.ttf'),
        Path('/usr/share/fonts/opentype/noto/NotoSansSC-Regular.ttf'),
    ]
    for c in candidates:
        if c.exists():
            return c
    raise FileNotFoundError('未找到 Noto Sans SC 字体，请安装后重试')


def build_font(widget_dir: Path) -> tuple[Path, Path]:
    """生成 LonghunFont-Regular.ttf 与 .woff2。"""
    noto_path = find_noto_sans_sc()
    print(f'📦 基础字体: {noto_path}')

    # 1. 实例化为 Regular (wght=400)
    vf = TTFont(noto_path)
    static = instancer.instantiateVariableFont(vf, {'wght': 400})
    vf.close()

    # 2. 子集化
    chars = load_needed_chars(widget_dir)
    subsetter = Subsetter()
    subsetter.populate(text=chars)
    subsetter.subset(static)
    print(f'🔤 子集字形数: {len(static.getGlyphOrder())}')

    # 3. 重命名为 LonghunFont（保留 SIL OFL 授权声明）
    name_table = static['name']
    win_names = {
        0: 'Copyright 2026 LongHun System (UID9622). Based on Noto Sans SC by Google, licensed under SIL Open Font License 1.1.',
        1: 'LonghunFont',
        2: 'Regular',
        3: '2.000;UID9622;LonghunFont-Regular',
        4: 'LonghunFont Regular',
        5: 'Version 2.0; UID9622',
        6: 'LonghunFont-Regular',
        8: 'LongHun System · UID9622',
        9: 'LongHun System · Based on Noto Sans SC (SIL OFL 1.1)',
        13: 'Licensed under SIL Open Font License 1.1',
    }
    mac_names = {
        0: 'Copyright 2026 LongHun System (UID9622). Based on Noto Sans SC by Google, licensed under SIL Open Font License 1.1.',
        1: 'LonghunFont',
        2: 'Regular',
        3: '2.000;UID9622;LonghunFont-Regular',
        4: 'LonghunFont Regular',
        5: 'Version 2.0; UID9622',
        6: 'LonghunFont-Regular',
        8: 'LongHun System',
        9: 'LongHun System',
        13: 'Licensed under SIL Open Font License 1.1',
    }
    name_table.names = []
    for nid, val in win_names.items():
        name_table.setName(val, nid, 3, 1, 0x409)
    for nid, val in mac_names.items():
        name_table.setName(val, nid, 1, 0, 0)

    # 4. 保存 TTF
    ttf_path = widget_dir / 'LonghunFont-Regular.ttf'
    static.save(str(ttf_path))
    print(f'✅ TTF 已保存: {ttf_path} ({ttf_path.stat().st_size} bytes)')

    # 5. 生成 WOFF2
    woff2_path = widget_dir / 'LonghunFont-Regular.woff2'
    static.flavor = 'woff2'
    static.save(str(woff2_path))
    print(f'✅ WOFF2 已保存: {woff2_path} ({woff2_path.stat().st_size} bytes)')

    return ttf_path, woff2_path


if __name__ == '__main__':
    widget_dir = Path(__file__).resolve().parent
    try:
        build_font(widget_dir)
    except Exception as e:
        print(f'❌ 字体构建失败: {e}', file=sys.stderr)
        sys.exit(1)
