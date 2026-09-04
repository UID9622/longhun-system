# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# #龍芯⚡️丙午·乙未·丙申·乙未·䷊泰-AUTO-DNA-LUBAN-INIT
#!/usr/bin/env python3
# 龍魂·六层来源链 / LongHun Six-Layer Source Chain
# DNA追溯码:#龍芯⚡️丙午·乙未·丙申·甲午·䷙大畜-LUBAN-UNIVERSAL-CALLIGRAPHY-v1.0
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""
鲁班大师 · 万字体书法渲染引擎

让任意中文字体（TTF/OTF/WOFF/WOFF2/系统字体）在任何设备上
都能渲染出中国书法效果。龍魂字体开源基础设施的通用扩展层。

P04 鲁班技术执行 · P01 诸葛亮战略推理 · P11 李白创意爆发
P05 上帝之眼三色审计 · P03 雯雯结构归档 · P14 吕蒙快速成长
"""

from pathlib import Path

DNA = "#龍芯⚡️丙午·乙未·丙申·甲午·䷙大畜-LUBAN-UNIVERSAL-CALLIGRAPHY-v1.0"
CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"

BASE_DIR = Path(__file__).parent.parent
LUBAN_DIR = BASE_DIR / "luban"
OUTPUT_DIR = BASE_DIR / "output" / "luban"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

__all__ = ["DNA", "CONFIRM", "BASE_DIR", "LUBAN_DIR", "OUTPUT_DIR"]
