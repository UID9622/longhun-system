#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·丁酉·乙亥·巳时·䷝离-REVERSE-TRACE-V1.0
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
"""
🔎 龍魂反向追溯 v1.0 — lh trace <node_id> [--json]

功能: 输入 node_id，查询该节点是否来自龍魂系统。
  输出: 创建时间 · 数字根 · 五行 · 审计色 · 原始输入摘要

数据源: ~/.longhun/nodes_registry.jsonl（网关 lh_api 归一回流自动记录全部调用）
判定: ① node_id 格式校验（<前缀>-9622-<sha8>）→ 龍魂系
      ② 本地节点注册表命中 → 完整溯源信息
      ③ 格式合法但无本地记录 → 龍魂系·无本地调用记录
      ④ 格式不合法 → 未归一·非龍魂节点
"""

import argparse
import json
import re
import sys
from pathlib import Path

NODES_REG = Path.home() / ".longhun" / "nodes_registry.jsonl"

NODE_ID_RE = re.compile(r"^([A-Za-z]{2,16})-9622-([0-9A-F]{8})$")

ENGINES = {
    "FLOW": "流场引擎", "BAZI": "八字排盘", "HEALTH": "健康自检",
    "SEC": "安全自检", "BENCH": "性能基准", "CIL": "CIL网关",
    "LH": "龍魂网关", "GATEWAY": "龍魂网关", "WITNESS": "证据固化",
    "BENCH": "性能基准", "NODE": "通用节点", "DR": "数字根",
}


def lookup(node_id: str) -> dict | None:
    if not NODES_REG.exists():
        return None
    try:
        with NODES_REG.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    rec = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if rec.get("node_id") == node_id:
                    return rec
    except OSError:
        pass
    return None


def trace(node_id: str) -> dict:
    m = NODE_ID_RE.match(node_id.strip())
    if not m:
        return {
            "status": "not_normalized",
            "node_id": node_id,
            "verdict": "未归一 - 非龍魂节点（node_id 格式不合法）",
            "audit": "🔴",
        }
    prefix, digest = m.group(1).upper(), m.group(2)
    engine = ENGINES.get(prefix, "龍魂引擎")
    rec = lookup(node_id)
    if rec:
        return {
            "status": "normalized",
            "node_id": node_id,
            "verdict": "已归一 - 屬龍魂系統",
            "audit": rec.get("audit", "🟡"),
            "engine": engine,
            "prefix": prefix,
            "created_at": rec.get("timestamp"),
            "digital_root": rec.get("digital_root"),
            "element": rec.get("element"),
            "gua": rec.get("gua"),
            "audit_color": rec.get("audit"),
            "action": rec.get("action"),
            "input_summary": rec.get("input_summary"),
            "origin_ip": rec.get("ip"),
            "digest": digest,
        }
    return {
        "status": "normalized",
        "node_id": node_id,
        "verdict": "已归一 - 屬龍魂系統（本地无调用记录）",
        "audit": "🟢",
        "engine": engine,
        "prefix": prefix,
        "digest": digest,
        "created_at": None,
        "note": "node_id 格式为龍魂标准（前缀-9622-哈希8）；详细调用记录需经网关 lh_api 调用过",
    }


def main() -> int:
    ap = argparse.ArgumentParser(prog="lh trace", description="反向追溯·按 node_id 查龍魂来源")
    ap.add_argument("node_id", help="要追溯的节点标识（如 FLOW-9622-47720A8E）")
    ap.add_argument("--json", action="store_true", help="JSON 输出")
    args = ap.parse_args()

    result = trace(args.node_id)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0

    print(f"{result['audit']} {result['verdict']}")
    print(f"  节点: {args.node_id}")
    if result.get("engine"):
        print(f"  引擎: {result['engine']}")
    if result.get("created_at"):
        print(f"  创建: {result['created_at']}")
    if result.get("digital_root") is not None:
        print(f"  数字根: {result['digital_root']} · 五行: {result.get('element')}"
              f" · 八卦: {result.get('gua')} · 审计: {result.get('audit_color')}")
    if result.get("action"):
        print(f"  行为: {result['action']}")
    if result.get("input_summary"):
        print(f"  原始输入: {result['input_summary']}")
    if result.get("origin_ip"):
        print(f"  来源IP: {result['origin_ip']}")
    if result.get("note"):
        print(f"  备注: {result['note']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
