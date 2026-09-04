#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂·数字人五行档案桥接 v1.0（最小闭环）
DNA: #龍芯⚡️2026-09-01-花名册五行桥接-v1.0-UID9622
创建者: 诸葛鑫（UID9622）
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
协议: CC BY-NC-SA 4.0（核心思想层）
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

最小闭环：让五行引擎被系统数据实际调用。
读 digital_humans/registry.json → 每个数字人名字生成流场节点（数字根→河图五行）
→ 输出 digital_humans/wuxing_profile.json（不改 registry.json 本体·最小侵入）。

用法：
    python3 lh_wuxing_bridge.py [--out 输出路径]
"""
import json
import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lh_wuxing_core import 计算数字根, 数字根五行, 三色审计, 生成节点ID, 生成DNA

仓库根 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
花名册路径 = os.path.join(仓库根, "digital_humans", "registry.json")
默认输出 = os.path.join(仓库根, "digital_humans", "wuxing_profile.json")

# 常用汉字简体笔画表（姓名五格剖象法·笔画→数字根→河图五行·有据可依）
# 未收录字回退码位求和数字根（fallback=True 透明标注）
_笔画表 = {
    "诸": 10, "葛": 12, "鑫": 24, "至": 6, "诚": 8, "智": 12, "魂": 13,
    "军": 6, "师": 6, "亮": 9, "龙": 5, "魂": 13, "系": 7, "统": 9,
    "小": 3, "白": 5, "张": 7, "三": 3, "李": 7, "四": 5, "王": 4,
}


def _姓名数字根(名字: str) -> tuple:
    """名字 → 笔画数 → 数字根（复用引擎计算数字根）· 返回 (数字根, 是否回退)"""
    笔画 = []
    回退 = False
    for c in 名字:
        if c in _笔画表:
            笔画.append(_笔画表[c])
        elif c.isdigit():
            笔画.append(int(c))
        elif "\u4e00" <= c <= "\u9fff":
            回退 = True
            笔画.append(ord(c) % 10)  # 未收录汉字回退：码位末位（透明标注）
        # 标点/间隔符不参与计算
    if not 笔画:
        笔画 = [0]
    return 计算数字根("".join(str(p) for p in 笔画)), 回退


def 构建档案(花名册: dict) -> dict:
    档案 = {}
    for ipa, 信息 in 花名册.get("digital_humans", {}).items():
        名字 = 信息.get("name", ipa)
        数字根, 回退 = _姓名数字根(名字)
        五行 = 数字根五行[数字根]
        审计 = 三色审计(数字根)
        动作 = {"🟢": "enter", "🟡": "hold"}.get(审计, "fuse")
        档案[ipa] = {
            "name": 名字,
            "persona": (信息.get("metadata") or {}).get("persona", ""),
            "status": 信息.get("status", ""),
            "数字根": 数字根,
            "五行": 五行,
            "fallback": 回退,
            "审计": 审计,
            "动作": 动作,
            "node_id": 生成节点ID(名字),
            "DNA": 生成DNA(f"{ipa} {名字}"),
        }
    return 档案


def main():
    输出路径 = 默认输出
    if len(sys.argv) > 2 and sys.argv[1] == "--out":
        输出路径 = sys.argv[2]
    with open(花名册路径, encoding="utf-8") as f:
        花名册 = json.load(f)
    档案 = 构建档案(花名册)
    结果 = {
        "档案": 档案,
        "meta": {
            "generated_at": datetime.now().isoformat(timespec="seconds"),
            "engine": "lh_wuxing_core v4.0（数字根→河图五行）",
            "count": len(档案),
        },
    }
    os.makedirs(os.path.dirname(输出路径), exist_ok=True)
    with open(输出路径, "w", encoding="utf-8") as f:
        json.dump(结果, f, ensure_ascii=False, indent=2)
    print(f"✅ 数字人五行档案 {len(档案)} 人 → {输出路径}")
    for ipa, v in 档案.items():
        print(f"  {ipa} {v['name']}: 数字根={v['数字根']} 五行={v['五行']} {v['审计']}")


if __name__ == "__main__":
    main()
