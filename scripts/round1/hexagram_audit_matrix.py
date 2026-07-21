#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
64卦审计矩阵
DNA: #龍芯⚡️2026-07-05-ROUND1-HEXAGRAM-AUDIT-MATRIX-v1.0
"""

import json
from pathlib import Path
from typing import Dict, List, Any

DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data" / "round1"

DIMS = ["来源", "意图", "影响", "价值观", "主权", "可追溯", "可修正", "可解释"]


class HexagramAuditMatrix:
    def __init__(self, map_path: Path = None):
        self.map_path = map_path or (DATA_DIR / "hexagram_8d_audit_map.json")
        with open(self.map_path, "r", encoding="utf-8") as f:
            self.audit_map = json.load(f)
        self.rules = self.audit_map.get("default_rules", {})

    def audit(
        self,
        hexagram_id: int,
        hexagram_name: str,
        audit_dims: List[str],
        fuse_result: Dict[str, Any],
        scene_tags: List[str]
    ) -> Dict[str, Any]:
        """
        根据卦象、熔断结果、场景标签生成8维审计矩阵。
        简化规则：
        - 高风险卦 + 主权/价值观维度 → 红
        - 中风险卦 + 可修正/可解释 → 黄
        - 其他 → 绿
        """
        # 风险等级
        risk_level = "low"
        high_risk_ids = {6, 7, 12, 18, 21, 23, 29, 36, 38, 39, 47, 59}
        medium_risk_ids = {3, 4, 5, 9, 16, 20, 22, 27, 30, 33, 34, 44, 48, 51, 52, 54, 56, 57, 60, 62, 64}
        if hexagram_id in high_risk_ids:
            risk_level = "high"
        elif hexagram_id in medium_risk_ids:
            risk_level = "medium"

        hexagram_audit = []
        red_count = 0
        yellow_count = 0

        for dim in DIMS:
            if dim in audit_dims:
                if risk_level == "high" and dim in {"主权", "价值观", "意图"}:
                    color = "🔴"
                    red_count += 1
                elif risk_level == "medium" and dim in {"可修正", "可解释", "影响"}:
                    color = "🟡"
                    yellow_count += 1
                else:
                    color = "🟢"
            else:
                # 该维度非本卦重点审计项，按场景标签判断
                if any(tag in {"主权", "安全", "隐私"} for tag in scene_tags) and dim == "主权":
                    color = "🟡"
                    yellow_count += 1
                else:
                    color = "🟢"

            hexagram_audit.append({"dim": dim, "result": color})

        # 熔断触发强制变红
        if fuse_result.get("fused"):
            for item in hexagram_audit:
                if item["dim"] == "价值观":
                    item["result"] = "🔴"
            red_count += 1
            overall = "🔴"
        elif red_count > 0:
            overall = "🔴"
        elif yellow_count > 0:
            overall = "🟡"
        else:
            overall = "🟢"

        return {
            "hexagram_audit": hexagram_audit,
            "overall_status": overall,
            "fuse_triggered": fuse_result.get("fused", False),
            "risk_level": risk_level
        }


if __name__ == "__main__":
    matrix = HexagramAuditMatrix()
    result = matrix.audit(
        hexagram_id=11,
        hexagram_name="泰",
        audit_dims=["可追溯", "可解释", "主权"],
        fuse_result={"fused": False},
        scene_tags=["知足", "不争"]
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
