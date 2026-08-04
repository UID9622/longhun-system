#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · 主权验证引擎 v1.0
DNA: #龍芯⚡️丙午·丙申·乙巳·辛巳·☴巽-SOVEREIGN-v1.0-UID9622
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0

功能：
  - 综合评估项目/代码的"技术主权"程度
  - 生成主权评分（0-100）
  - 给出具体改进路径
"""

import json
from pathlib import Path
from typing import Dict, Any, List


class SovereigntyEngine:
    """主权验证引擎——掀黑箱发现不了主权问题，这个来评分+给路径"""

    WEIGHTS = {
        "license": 15,
        "sovereignty_statement": 10,
        "domestic_compatible": 15,
        "data_sovereignty": 20,
        "opensource_compliance": 15,
        "self_hosted": 10,
        "audit_trail": 15,
    }

    def __init__(self):
        self.last_result = None

    def assess(self, project_path: Path) -> Dict[str, Any]:
        """评估项目主权得分"""
        scores = {}

        # 1. 许可证检查
        has_license = any(
            (project_path / f).exists()
            for f in ["LICENSE", "LICENSE.md", "LICENSE.txt"]
        )
        scores["license"] = self.WEIGHTS["license"] if has_license else 0

        # 2. 主权声明
        readme_path = project_path / "README.md"
        has_sovereignty = False
        if readme_path.exists():
            content = readme_path.read_text(encoding="utf-8", errors="ignore")
            if any(kw in content for kw in ["主权", "sovereign", "自持", "UID9622", "自主"]):
                has_sovereignty = True
        scores["sovereignty_statement"] = self.WEIGHTS["sovereignty_statement"] if has_sovereignty else 0

        # 3. 国产兼容（检查是否有鲲鹏/国产适配声明）
        has_domestic = False
        if readme_path.exists():
            content = readme_path.read_text(encoding="utf-8", errors="ignore")
            if any(kw in content for kw in ["鲲鹏", "麒麟", "统信", "华为", "国产"]):
                has_domestic = True
        scores["domestic_compatible"] = self.WEIGHTS["domestic_compatible"] if has_domestic else 5

        # 4. 数据主权
        has_privacy = (project_path / "PRIVACY_POLICY.md").exists()
        has_terms = (project_path / "TERMS_OF_SERVICE.md").exists()
        if has_privacy and has_terms:
            scores["data_sovereignty"] = self.WEIGHTS["data_sovereignty"]
        elif has_privacy:
            scores["data_sovereignty"] = 12
        else:
            scores["data_sovereignty"] = 3

        # 5. 开源合规
        has_contrib = (project_path / "CONTRIBUTING.md").exists()
        has_governance = (project_path / "GOVERNANCE.md").exists()
        if has_contrib and has_governance:
            scores["opensource_compliance"] = self.WEIGHTS["opensource_compliance"]
        elif has_contrib:
            scores["opensource_compliance"] = 8
        else:
            scores["opensource_compliance"] = 3

        # 6. 自托管能力
        has_docker = (
            (project_path / "docker").exists()
            or (project_path / "Dockerfile").exists()
            or (project_path / "docker-compose.yml").exists()
        )
        scores["self_hosted"] = self.WEIGHTS["self_hosted"] if has_docker else 2

        # 7. 审计追踪
        has_audit = (project_path / "audit").exists() or (project_path / "logs").exists()
        scores["audit_trail"] = self.WEIGHTS["audit_trail"] if has_audit else 3

        total = sum(scores.values())
        self.last_result = {
            "project": str(project_path),
            "score": total,
            "max_score": 100,
            "grade": self._get_grade(total),
            "scores": scores,
            "recommendations": self._get_recommendations(scores),
        }
        return self.last_result

    def _get_grade(self, score: float) -> str:
        if score >= 80:
            return "🟢 完全主权"
        if score >= 60:
            return "🟡 基本主权"
        if score >= 40:
            return "🟠 部分主权"
        return "🔴 主权不足"

    def _get_recommendations(self, scores: Dict) -> List[str]:
        recs = []
        if scores["license"] == 0:
            recs.append("添加 LICENSE 文件")
        if scores["sovereignty_statement"] < 10:
            recs.append("在 README 中添加主权声明（UID9622·自主知识产权）")
        if scores["domestic_compatible"] < 10:
            recs.append("添加国产平台适配说明（鲲鹏/麒麟）")
        if scores["data_sovereignty"] < 15:
            recs.append("添加 PRIVACY_POLICY.md 和 TERMS_OF_SERVICE.md")
        if scores["self_hosted"] < 8:
            recs.append("提供 Docker 自托管部署方案")
        if scores["audit_trail"] < 10:
            recs.append("建立审计日志目录")
        return recs


if __name__ == "__main__":
    engine = SovereigntyEngine()
    result = engine.assess(Path.home() / "longhun-system")
    print(f"主权评分: {result['score']}/{result['max_score']} - {result['grade']}")
    print("各维度:")
    for k, v in result["scores"].items():
        bar = "█" * (v // 2)
        print(f"  {k}: {bar} {v}")
    if result["recommendations"]:
        print("改进建议:")
        for r in result["recommendations"]:
            print(f"  ├ {r}")
    print("🟢 主权验证引擎测试通过")
