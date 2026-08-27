# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# DNA: #龍芯⚡️丙午·丙申·戊辰·丁巳·䷯井-CODE-补DNA-55f1c813
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂·韬定律进阶破解之法 v2.2 分章脚本
按 `# 第X章 ` 切分为 sec01 ~ sec06
"""
import re
import sys
from pathlib import Path

CN_NUM = {
    "一": "01",
    "二": "02",
    "三": "03",
    "四": "04",
    "五": "05",
    "六": "06",
}


def split(md_path: Path, out_dir: Path):
    content = md_path.read_text(encoding="utf-8")
    lines = content.splitlines(keepends=True)
    buffers = {}
    current = "preamble"
    pattern = re.compile(r"^# 第([一二三四五六])章 ")

    for line in lines:
        m = pattern.match(line)
        if m:
            num = CN_NUM[m.group(1)]
            current = f"sec{num}"
            buffers.setdefault(current, [])
        buffers.setdefault(current, [])
        buffers[current].append(line)

    out_dir.mkdir(parents=True, exist_ok=True)
    for key in ["sec01", "sec02", "sec03", "sec04", "sec05", "sec06"]:
        if key not in buffers:
            continue
        out_path = out_dir / f"韬定律进阶破解_{key}.md"
        out_path.write_text("".join(buffers[key]), encoding="utf-8")
        print(f"✅ {out_path} ({len(buffers[key])} 行)")


if __name__ == "__main__":
    root = Path(__file__).resolve().parent.parent
    md = root / "龍魂·韬定律进阶破解之法v2.2.md"
    if not md.exists():
        print(f"❌ 主文档不存在: {md}")
        sys.exit(1)
    split(md, root)
