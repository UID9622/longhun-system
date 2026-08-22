#!/usr/bin/env python3
# DNA: #龍芯⚡️丙午·丙申·庚戌·壬午·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# #龍芯⚡️丙午·甲午·己巳·乙丑·䷮困-AUTO-DNA-A0E5EEB9 自动注入·分层治理自愈引擎 · 来源可查
#!/usr/bin/env python3
# 龍魂·六层来源链 / LongHun Six-Layer Source Chain
# DNA追溯码:#龍芯⚡️丙午·甲午·戊辰·戊午·䷑蛊-LONGHUN-FONT-WORK-ID-v1.0
"""
书法作品编号系统

格式：LH-CAL-{书体代码}-{名家代码}-{典籍代码}-{序号}-{哈希}
示例：LH-CAL-KA-YZQ-YIJING-00001-A7F3D2
"""

import hashlib
import json
import os
from datetime import datetime
from pathlib import Path

DNA = "#龍芯⚡️丙午·甲午·戊辰·戊午·䷑蛊-LONGHUN-FONT-WORK-ID-v1.0"

COUNTER_FILE = Path(__file__).parent / ".work_counter.json"


def _load_counter():
    if COUNTER_FILE.exists():
        with open(COUNTER_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def _save_counter(counter):
    with open(COUNTER_FILE, "w", encoding="utf-8") as f:
        json.dump(counter, f, ensure_ascii=False, indent=2)


def generate_work_id(category_code: str, artist_code: str, text: str, classic: str = "GENERAL") -> str:
    """
    生成书法作品编号。

    Args:
        category_code: 书体代码，如 KA/XS/CS/LS/ZS
        artist_code: 名家代码，如 YZQ/WXZ
        text: 作品内容，用于生成哈希
        classic: 典籍代码，如 YIJING/DAODEJING/HUANGDI/GENERAL
    """
    counter = _load_counter()
    key = f"{category_code}-{artist_code}-{classic}"
    seq = counter.get(key, 0) + 1
    counter[key] = seq
    _save_counter(counter)

    seq_str = f"{seq:05d}"
    content_hash = hashlib.sha256(f"{text}{DNA}{seq_str}".encode("utf-8")).hexdigest()[:6].upper()

    work_id = f"LH-CAL-{category_code}-{artist_code}-{classic.upper()}-{seq_str}-{content_hash}"
    return work_id


def parse_work_id(work_id: str) -> dict[str, Any]:
    """解析作品编号。"""
    parts = work_id.split("-")
    if len(parts) != 7 or parts[0] != "LH" or parts[1] != "CAL":
        raise ValueError(f"非法作品编号格式: {work_id}")
    return {
        "prefix": "LH-CAL",
        "category_code": parts[2],
        "artist_code": parts[3],
        "classic_code": parts[4],
        "sequence": parts[5],
        "hash": parts[6],
    }


if __name__ == "__main__":
    sample = generate_work_id("KA", "YZQ", "自强不息", "YIJING")
    print("示例编号:", sample)
    print("解析:", parse_work_id(sample))
    print("DNA:", DNA)
