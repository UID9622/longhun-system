#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""
🐉 龍魂桥接器 — seal.rs ↔ MemoryLifecycle

用法:
  python3 longhun_bridge.py '<JSON_SEAL_RECORD>'

  从 stdin 读取 JSON 也可以:
  echo '<JSON>' | python3 longhun_bridge.py

功能:
  将 lh-station seal 记录存入龍魂 MemoryLifecycle 记忆系统，
  形成不可篡改的审计链路。
"""

import sys
import json
import os

# 添加当前目录到 Python 路径（确保能找到 longhun_evolution_engine）
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from longhun_evolution_engine import MemoryLifecycle, MemoryPriority


def store_seal(json_str: str) -> dict:
    """
    将 seal JSON 记录存入龍魂记忆系统

    Args:
        json_str: seal_record 的 JSON 字符串

    Returns:
        包含 status/dna/entry_id 的结果字典
    """
    try:
        data = json.loads(json_str)
    except json.JSONDecodeError as e:
        return {"status": "error", "reason": f"JSON 解析失败: {e}"}

    dna = data.get("dna", "unknown")
    if dna == "unknown":
        return {"status": "error", "reason": "缺少 dna 字段"}

    # 格式化 content — 生成人类可读的记忆文本
    content = """🐉 龍魂代码主权转换封印记录

DNA: {dna}
时间: {transformed_at}
语言: {language}
芯片目标: {chip_target}
文件总数: {total_files}
注入主权头: {injected_count}
编译产物: {compiled_count}
GPG 签名: {signed_count}
安全审查: {security_status}
安全违规: {security_violations}
殖民评分: {colonial_score}
月成本: ¥{cost_monthly}
成本风险: {cost_risk}
封印哈希: {seal_hash}
""".format(
        dna=dna,
        transformed_at=data.get('transformed_at', 'unknown'),
        language=data.get('language', 'unknown'),
        chip_target=data.get('chip_target', 'unknown'),
        total_files=data.get('total_files', 0),
        injected_count=data.get('injected_count', 0),
        compiled_count=data.get('compiled_count', 0),
        signed_count=data.get('signed_count', 0),
        security_status='通过' if data.get('security_passed') else '未通过',
        security_violations=data.get('security_violations', 0),
        colonial_score=data.get('colonial_score', 'N/A'),
        cost_monthly=data.get('cost_monthly', 0),
        cost_risk=data.get('cost_risk', 'N/A'),
        seal_hash=data.get('seal_hash', 'unknown'),
    )

    try:
        lifecycle = MemoryLifecycle()
        entry = lifecycle.store(
            content=content,
            category="scene_memory",
            priority=MemoryPriority.P1_IMPORTANT,
            tags=["lh-station", "seal", "主权转换", dna[:16]],
        )
        return {
            "status": "ok",
            "dna": dna,
            "entry_id": entry.entry_id,
            "category": entry.category,
            "priority": entry.priority.value,
        }
    except Exception as e:
        return {"status": "error", "reason": str(e)}


def main():
    """命令行入口"""
    json_str = ""

    # 优先使用命令行参数
    if len(sys.argv) > 1:
        json_str = sys.argv[1]
    else:
        # 从 stdin 读取
        json_str = sys.stdin.read().strip()

    if not json_str or json_str == "[]":
        print(json.dumps({
            "status": "error",
            "reason": "没有输入数据。用法: echo '<JSON>' | python3 longhun_bridge.py"
        }, ensure_ascii=False))
        sys.exit(1)

    result = store_seal(json_str)
    print(json.dumps(result, ensure_ascii=False))
    sys.exit(0 if result["status"] == "ok" else 1)


if __name__ == "__main__":
    main()
