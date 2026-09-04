# DNA: #龍芯⚡️2026-08-25-RENDER-ENV-v1.0-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""lh render 统一入口 v1.1 — M75 服务渲染 + 女娲五彩石图像引擎

- wuxing/audit/flow/health → wuwu_renderer.py（龍魂风格图像 · PNG/SVG/HTML）
- status/open/run/batch/server/log → M75 渲染引擎（:8788）
"""

import sys
from pathlib import Path

_可视化类型 = {"wuxing", "audit", "flow", "health"}

if __name__ == "__main__":
    argv = sys.argv[1:]
    if argv and argv[0] in _可视化类型:
        from wuwu_renderer import main as wuwu_main
        sys.argv = ["wuwu_renderer"] + argv
        wuwu_main()
    else:
        sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
        from render.lh_render import main
        main()
