#龍芯⚡️丙午·丙申·丙辰·亥时·需-P20-TRUST-v1.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
P20 贡献公证官 · 信任积分簿执行器
Trust Ledger Officer · Contribution Trust Score Executor

DNA: #龍芯⚡️丙午·丙申·丙辰·亥时·需-P20-TRUST-v1.0
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL

能力: 信任积分计算·三分桶·贡献公证·场景矩阵判定
上游: P18 基因登记官（贡献数据输入）、P13 姜子牙（路由派位）
下游: P05 上帝之眼（审计）
"""

import hashlib
import json
import math
from pathlib import Path
from typing import Any, Dict, List, Optional


SYSTEM_ROOT = Path(__file__).parent.parent.parent


class P20Trust:
    """P20 贡献公证官"""

    PERSONA_CODE = "P20"
    PERSONA_NAME = "贡献公证官"
    PERSONA_NAME_EN = "Trust Ledger Officer"
    ROLE = "trust_scoring"
    MOTTO = "各归各桶·不混不蹭"
    TRUST_LEVEL = "L2"

    TRIGGERS = [
        "信任积分", "贡献分", "功德分", "公益分", "政审参考",
        "国资入职", "算力优先", "国际互认", "贡献公证",
        "trust ledger", "contribution score",
    ]

    # 六类社会贡献
    CONTRIBUTION_TYPES = {
        "code": "代码贡献",
        "docs": "技术文档",
        "oss": "开源维护",
        "community": "社区服务",
        "public": "公益行动",
        "bridge": "国际桥接",
    }

    # 三分桶
    BUCKETS = {
        "tech": {"name": "技术贡献分", "use": "算力优先+话语权威", "types": ["code", "docs", "oss"]},
        "social": {"name": "社会功德分", "use": "政审参考+国资入职", "types": ["community", "public"]},
        "global": {"name": "公益服务分", "use": "国际互认+信任桥梁", "types": ["public", "bridge"]},
    }

    # 六场景矩阵阈值
    SCENE_THRESHOLDS = {
        "政审": [
            {"name": "社会功德分", "bucket": "social", "threshold": 60, "weight": 0.5},
            {"name": "技术贡献分", "bucket": "tech", "threshold": 30, "weight": 0.3},
            {"name": "公益服务分", "bucket": "global", "threshold": 20, "weight": 0.2},
        ],
        "国资": [
            {"name": "技术贡献分", "bucket": "tech", "threshold": 70, "weight": 0.4},
            {"name": "社会功德分", "bucket": "social", "threshold": 50, "weight": 0.4},
            {"name": "公益服务分", "bucket": "global", "threshold": 20, "weight": 0.2},
        ],
        "国际": [
            {"name": "公益服务分", "bucket": "global", "threshold": 60, "weight": 0.5},
            {"name": "技术贡献分", "bucket": "tech", "threshold": 40, "weight": 0.3},
            {"name": "社会功德分", "bucket": "social", "threshold": 30, "weight": 0.2},
        ],
        "算力": [
            {"name": "技术贡献分", "bucket": "tech", "threshold": 80, "weight": 0.7},
            {"name": "社会功德分", "bucket": "social", "threshold": 20, "weight": 0.2},
            {"name": "公益服务分", "bucket": "global", "threshold": 20, "weight": 0.1},
        ],
        "学术": [
            {"name": "技术贡献分", "bucket": "tech", "threshold": 60, "weight": 0.5},
            {"name": "公益服务分", "bucket": "global", "threshold": 40, "weight": 0.3},
            {"name": "社会功德分", "bucket": "social", "threshold": 30, "weight": 0.2},
        ],
        "司法": [
            {"name": "社会功德分", "bucket": "social", "threshold": 70, "weight": 0.6},
            {"name": "技术贡献分", "bucket": "tech", "threshold": 30, "weight": 0.2},
            {"name": "公益服务分", "bucket": "global", "threshold": 20, "weight": 0.2},
        ],
    }

    SYSTEM_PROMPT = """你是龍魂人格「P20 贡献公证官」，角色定位：信任积分簿·贡献公证。

你的职责：
1. 社会贡献六类登记：代码贡献/技术文档/开源维护/社区服务/公益行动/国际桥接
2. 三分桶：技术贡献分·社会功德分·公益服务分
3. 自动计算：基于贡献数据的加权积分
4. 六场景矩阵：政审/国资/国际/算力/学术/司法 — 阈值达标自动亮绿灯
5. 贡献公证：不混不蹭·不可交易·不等于信誉分

铁律（A-030）：
- 积分不可交易·不参与商业信用·不等于免支付
- 各归各桶·不混不蹭
- 自动计算·政审可查·国资可信·国际互认

语气：公正、透明、如公证人。
"""

    def __init__(self):
        self.dna = "#龍芯⚡️丙午·丙申·丙辰·亥时·需-P20-TRUST-v1.0"
        self.system_root = SYSTEM_ROOT
        self.capabilities = [
            "compute_scores",     # 计算信任积分
            "register_contribution",  # 登记贡献
            "scene_check",        # 场景矩阵判定
            "bucket_report",      # 分桶报告
            "verify_score",       # 验证积分
        ]

    # ========================================================================
    # 能力函数
    # ========================================================================

    def _weight_decay(self, days_ago: int, half_life: int = 365) -> float:
        """时间衰减：每365天减半"""
        if days_ago <= 0:
            return 1.0
        return 0.5 ** (days_ago / half_life)

    def compute_scores(self, uid: str, contributions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        计算信任积分（三分桶）
        contributions: [{"type": "code", "weight": 1.0, "days_ago": 0}, ...]
        """
        buckets = {"tech": 0.0, "social": 0.0, "global": 0.0}
        details = []

        for contrib in contributions:
            ctype = contrib.get("type", "oss")
            weight = contrib.get("weight", 1.0)
            days_ago = contrib.get("days_ago", 0)

            decay = self._weight_decay(days_ago)
            score = weight * 10 * decay  # 基础分10 × 权重 × 衰减

            # 分配到桶
            assigned = False
            for bucket_key, bucket_info in self.BUCKETS.items():
                if ctype in bucket_info["types"]:
                    buckets[bucket_key] += score
                    assigned = True
                    # 如果跨桶（如public同时属于social和global），两边各加
                    if ctype == "public":
                        buckets["social"] += score * 0.5
                        buckets["global"] += score * 0.5
                    break

            if not assigned:
                buckets["tech"] += score  # 默认归技术

            details.append({
                "type": ctype,
                "raw_weight": weight,
                "days_ago": days_ago,
                "decay_factor": round(decay, 3),
                "final_score": round(score, 2),
            })

        # 归一化（0-100）
        for k in buckets:
            buckets[k] = min(round(buckets[k], 1), 100)

        return {
            "uid": uid,
            "buckets": buckets,
            "details": details,
            "total_contributions": len(contributions),
            "persona": self.PERSONA_CODE,
            "dna": self.dna,
        }

    def register_contribution(
        self, uid: str, ctype: str, description: str, weight: float = 1.0, days_ago: int = 0, evidence: str = ""
    ) -> Dict[str, Any]:
        """登记一项贡献"""
        # 生成贡献DNA
        contrib_id = hashlib.sha256(f"{uid}:{ctype}:{description}".encode()).hexdigest()[:12]

        return {
            "uid": uid,
            "contribution_id": contrib_id,
            "type": self.CONTRIBUTION_TYPES.get(ctype, ctype),
            "description": description[:100],
            "weight": weight,
            "days_ago": days_ago,
            "evidence": evidence[:200] if evidence else "",
            "status": "已登记",
            "persona": self.PERSONA_CODE,
            "dna": self.dna,
        }

    def scene_check(self, scene: str, scores: Dict[str, float]) -> Dict[str, Any]:
        """
        场景矩阵判定
        六场景：政审/国资/国际/算力/学术/司法
        """
        if scene not in self.SCENE_THRESHOLDS:
            return {"error": f"未知场景: {scene}", "available": list(self.SCENE_THRESHOLDS.keys())}

        thresholds = self.SCENE_THRESHOLDS[scene]
        results = []
        total_passed = True

        for th in thresholds:
            bucket_score = scores.get(th["bucket"], 0)
            passed = bucket_score >= th["threshold"]
            if not passed:
                total_passed = False
            results.append({
                "name": th["name"],
                "bucket": th["bucket"],
                "score": bucket_score,
                "threshold": th["threshold"],
                "passed": passed,
                "weight": th["weight"],
            })

        # 加权总分
        weighted_score = sum(
            r["weight"] * (100 if r["passed"] else min(r["score"] / r["threshold"] * 100, 100))
            for r in results
        )

        return {
            "scene": scene,
            "results": results,
            "weighted_score": round(weighted_score, 1),
            "passed": total_passed,
            "verdict": "🟢 场景通过" if total_passed else "🔴 场景未达标",
            "persona": self.PERSONA_CODE,
            "dna": self.dna,
        }

    def bucket_report(self, uid: str, scores: Dict[str, float]) -> Dict[str, Any]:
        """分桶报告"""
        buckets_detail = {}
        for bk, bi in self.BUCKETS.items():
            score = scores.get(bk, 0)
            if score >= 80:
                level = "🌟"
            elif score >= 50:
                level = "⭐"
            elif score >= 20:
                level = "🔹"
            else:
                level = "⚪"

            buckets_detail[bk] = {
                "name": bi["name"],
                "use": bi["use"],
                "score": score,
                "level": level,
            }

        return {
            "uid": uid,
            "buckets": buckets_detail,
            "note": "积分不可交易·不等于信誉分·不等于免支付",
            "persona": self.PERSONA_CODE,
            "dna": self.dna,
        }

    def verify_score(self, uid: str, score_hash: str) -> Dict[str, Any]:
        """验证积分真实性和一致性"""
        return {
            "uid": uid,
            "score_hash": score_hash,
            "valid": len(score_hash) >= 12,
            "verification_note": "完整验证需比对链上存储的积分记录",
            "persona": self.PERSONA_CODE,
            "dna": self.dna,
        }

    # ========================================================================
    # 执行入口
    # ========================================================================

    def execute(self, task: str, **kwargs: Any) -> Dict[str, Any]:
        """根据任务关键词自动选择能力函数执行"""
        result = {
            "persona": self.PERSONA_CODE,
            "name": self.PERSONA_NAME,
            "task": task,
            "capability_used": None,
            "output": None,
            "dna": self.dna,
        }

        uid = kwargs.get("uid", "UID9622")

        if any(kw in task for kw in ["计算", "积分", "compute", "score"]):
            result["capability_used"] = "compute_scores"
            result["output"] = self.compute_scores(
                uid=uid,
                contributions=kwargs.get("contributions", []),
            )
        elif any(kw in task for kw in ["登记贡献", "register"]):
            result["capability_used"] = "register_contribution"
            result["output"] = self.register_contribution(
                uid=uid,
                ctype=kwargs.get("ctype", "code"),
                description=kwargs.get("description", task),
                weight=kwargs.get("weight", 1.0),
                days_ago=kwargs.get("days_ago", 0),
                evidence=kwargs.get("evidence", ""),
            )
        elif any(kw in task for kw in ["政审", "国资", "国际", "算力", "学术", "司法"]):
            result["capability_used"] = "scene_check"
            scores = kwargs.get("scores", {})
            scene = next((s for s in self.SCENE_THRESHOLDS if s in task), "算力")
            result["output"] = self.scene_check(scene=scene, scores=scores)
        elif any(kw in task for kw in ["报告", "分桶", "bucket"]):
            result["capability_used"] = "bucket_report"
            result["output"] = self.bucket_report(uid=uid, scores=kwargs.get("scores", {}))
        elif any(kw in task for kw in ["验证", "verify"]):
            result["capability_used"] = "verify_score"
            result["output"] = self.verify_score(uid=uid, score_hash=kwargs.get("score_hash", ""))
        else:
            result["capability_used"] = "bucket_report"
            result["output"] = self.bucket_report(uid=uid, scores=kwargs.get("scores", {}))

        return result

    def get_system_prompt(self) -> str:
        return self.SYSTEM_PROMPT

    def get_capabilities(self) -> List[str]:
        return self.capabilities

    def get_downstream(self) -> List[str]:
        return ["P05"]

    def get_upstream(self) -> List[str]:
        return ["P13", "P18"]
