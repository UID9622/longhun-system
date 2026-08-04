#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · 个性化引擎 v1.0
DNA: #龍芯⚡️丙午·丙申·乙巳·辛巳·☴巽-PERSONALIZE-v1.0-UID9622
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0

功能：
  - 用户画像（偏好、历史行为、专业领域）
  - 响应风格适配（简洁/详细/技术/通俗）
  - 推荐系统（根据历史推荐下一步操作）
"""

import json
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime


class PersonalizationEngine:
    """个性化引擎——不同场景不同风格，千篇一律→千人千面"""

    STYLES = ["concise", "detailed", "technical", "beginner", "veteran"]

    def __init__(self):
        self.profiles = {}
        self._load_profiles()

    def _load_profiles(self):
        profile_file = Path.home() / "longhun-system/data/profiles.json"
        if profile_file.exists():
            try:
                self.profiles = json.loads(profile_file.read_text(encoding="utf-8"))
            except Exception:
                pass

    def get_profile(self, user_id: str) -> Dict:
        if user_id not in self.profiles:
            self.profiles[user_id] = self._create_default_profile(user_id)
            self._save_profiles()
        return self.profiles[user_id]

    def _create_default_profile(self, user_id: str) -> Dict:
        return {
            "user_id": user_id,
            "preferred_style": "concise",
            "expertise_level": 2,
            "frequent_actions": [],
            "last_interaction": None,
            "interaction_count": 0,
            "created_at": datetime.now().isoformat(),
        }

    def update_from_interaction(self, user_id: str, action: str, result: Dict):
        profile = self.get_profile(user_id)
        profile["frequent_actions"].append({
            "action": action,
            "result": result.get("status", "unknown"),
            "timestamp": datetime.now().isoformat(),
        })
        if len(profile["frequent_actions"]) > 100:
            profile["frequent_actions"] = profile["frequent_actions"][-100:]
        profile["last_interaction"] = datetime.now().isoformat()
        profile["interaction_count"] += 1
        self._save_profiles()

    def _save_profiles(self):
        profile_dir = Path.home() / "longhun-system/data"
        profile_dir.mkdir(parents=True, exist_ok=True)
        profile_file = profile_dir / "profiles.json"
        profile_file.write_text(json.dumps(self.profiles, ensure_ascii=False, indent=2))

    def set_style(self, user_id: str, style: str) -> bool:
        if style not in self.STYLES:
            return False
        profile = self.get_profile(user_id)
        profile["preferred_style"] = style
        self._save_profiles()
        return True

    def adapt_response(self, response: str, user_id: str) -> str:
        """根据用户偏好调整响应"""
        profile = self.get_profile(user_id)
        style = profile.get("preferred_style", "concise")
        level = profile.get("expertise_level", 2)

        if style == "concise":
            # 精简版：只保留核心信息
            lines = response.split("\n")
            if len(lines) > 10:
                return "\n".join(lines[:8] + ["... (精简模式)"])
        elif style == "beginner" or level < 2:
            # 新手模式：加备注
            return f"📖 新手引导：\n{response}"
        elif style == "technical":
            return f"🔧 技术模式：\n{response}"
        return response

    def recommend(self, user_id: str) -> List[str]:
        """根据历史推荐下一步操作"""
        profile = self.get_profile(user_id)
        actions = [a.get("action", "") for a in profile["frequent_actions"][-20:]]
        if not actions:
            return ["健康检查", "审计项目", "查看状态"]

        recs = []
        # 如果最近频繁审计，推荐签名
        if any("审计" in a for a in actions[-5:]):
            recs.append("签章")
        # 如果最近在开发，推荐测试
        if any("代码" in a for a in actions[-5:]):
            recs.append("测试")
        if not recs:
            recs = ["状态查看", "最新日志"]
        return recs

    def list_profiles(self) -> List[Dict]:
        return [
            {"user_id": uid, "style": p.get("preferred_style"), "interactions": p.get("interaction_count", 0)}
            for uid, p in self.profiles.items()
        ]


if __name__ == "__main__":
    engine = PersonalizationEngine()
    # 创建测试用户
    profile = engine.get_profile("test_user")
    print(f"默认画像: {profile['preferred_style']} (等级: {profile['expertise_level']})")

    engine.update_from_interaction("test_user", "健康检查", {"status": "🟢 通过"})
    recs = engine.recommend("test_user")
    print(f"推荐: {recs}")

    adapted = engine.adapt_response("系统状态正常\nCPU: 15%\n内存: 45%\n", "test_user")
    print(f"适配: {adapted[:60]}...")
    print("🟢 个性化引擎测试通过")
