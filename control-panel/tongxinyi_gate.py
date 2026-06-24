#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂通心译闸门 | Tongxinyi Gate v1.0

所有用户输入进入 control-panel 技能执行前，先经过此闸门：
  L0 原话保留 → L1 情绪净化 → L2 意图骨架 → L3 SAST → L4 三色审计 → L5 适配输出

DNA: #龍芯⚡️2026-06-23-TONGXINYI-GATE-v1.0
"""

import hashlib
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

DRAWERS_PATH = Path(__file__).with_name("tongxinyi_drawers.json")


class TongxinyiGate:
    """龍魂前置翻译闸门：先翻译，再执行。"""

    def __init__(self, skill_metadata: Optional[Dict[str, Any]] = None):
        self.skill_metadata = skill_metadata or {}
        self.drawers = self._load_drawers()

    def _load_drawers(self) -> List[Dict[str, Any]]:
        if DRAWERS_PATH.exists():
            try:
                data = json.loads(DRAWERS_PATH.read_text(encoding="utf-8"))
                return data.get("drawers", [])
            except Exception:
                pass
        return []

    def translate(self, raw_input: str, uid: str = "UID9622") -> Dict[str, Any]:
        """执行六层翻译，返回结构化结果。"""
        ts = datetime.now().isoformat()
        input_hash = hashlib.sha256(raw_input.encode("utf-8")).hexdigest()[:16]
        dna = f"#龍芯⚡️{ts}-TONGXINYI-{input_hash}-{uid}"

        # L0 ~ L5
        l0 = self._layer0_raw(raw_input, input_hash, ts)
        l1 = self._layer1_emotion(raw_input)
        l2 = self._layer2_intent(raw_input, uid)
        l3 = self._layer3_sast(raw_input, l2)
        l4 = self._layer4_audit(raw_input, l2)
        l5 = self._layer5_adapter(raw_input, l2, l4)

        return {
            "dna": dna,
            "L0_原话保留": l0,
            "L1_情绪净化": l1,
            "L2_意图骨架": l2,
            "L3_SAST": l3,
            "L4_三色审计": l4,
            "L5_适配输出": l5,
        }

    # ═══════════════════════════════════════════════════════════
    # L0 原话保留
    # ═══════════════════════════════════════════════════════════
    def _layer0_raw(self, raw_input: str, input_hash: str, ts: str) -> Dict[str, Any]:
        return {
            "raw_input": raw_input,
            "input_hash": input_hash,
            "timestamp": ts,
            "note": "老大原话一字不改·先存起来",
        }

    # ═══════════════════════════════════════════════════════════
    # L1 情绪净化
    # ═══════════════════════════════════════════════════════════
    def _layer1_emotion(self, text: str) -> Dict[str, Any]:
        intensifiers = {
            "我操": 8,
            "卧槽": 8,
            "他妈": 7,
            "草": 6,
            "嘿嘿": 3,
            "哈哈": 3,
            "呜呜": 5,
            "气死": 7,
            "牛逼": 5,
            "赞": 4,
            "棒": 3,
            "烦": 5,
        }
        intensity = 0
        matched = []
        for word, score in intensifiers.items():
            if word in text:
                intensity = max(intensity, score)
                matched.append(word)

        if intensity >= 7:
            label = "强烈"
        elif intensity >= 4:
            label = "明显"
        elif intensity > 0:
            label = "轻微"
        else:
            label = "平静"

        return {
            "intensity": intensity,
            "label": label,
            "matched_words": matched,
            "decoupled_text": text,
            "note": "情绪是情绪，指令是指令，分开处理",
        }

    # ═══════════════════════════════════════════════════════════
    # L2 意图骨架
    # ═══════════════════════════════════════════════════════════
    def _layer2_intent(self, text: str, uid: str = "UID9622") -> Dict[str, Any]:
        action = "general"
        for cand, keywords in {
            "execute": ["执行", "运行", "启动", "调用", "跑", "开启"],
            "query": ["查", "看", "列出", "显示", "汇报", "搜索", "找"],
            "create": ["写", "创建", "生成", "新建", "做", "画"],
            "update": ["改", "更新", "修改", "修", "升级", "迭代"],
            "delete": ["删", "清理", "去掉", "移除"],
            "backup": ["备份", "恢复", "回滚"],
        }.items():
            if any(kw in text for kw in keywords):
                action = cand
                break

        priority = 5
        if any(kw in text for kw in ["立刻", "马上", "现在", "赶紧", "必须", "锁死"]):
            priority = 9
        elif any(kw in text for kw in ["看看", "帮我", "能不能", "试试"]):
            priority = 4

        # 简单目标抽取：找引号内或“把/将”后的对象
        target = ""
        m = re.search(r"[\"'""']([^\"'""']+)[\"'""']", text)
        if m:
            target = m.group(1)
        else:
            m2 = re.search(r"[把将]([^，。；]+)[给做]", text)
            if m2:
                target = m2.group(1).strip()

        missing = []
        if not target:
            missing.append("操作目标")
        if action == "general":
            missing.append("具体动作")

        return {
            "subject": uid,
            "action": action,
            "target": target,
            "priority": priority,
            "missing": "、".join(missing) if missing else "无",
        }

    # ═══════════════════════════════════════════════════════════
    # L3 SAST 语义抽象语法树
    # ═══════════════════════════════════════════════════════════
    def _layer3_sast(self, text: str, skeleton: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "root_type": skeleton["action"],
            "nodes": [
                {"type": "subject", "value": skeleton["subject"], "layer": "L2"},
                {"type": "action", "value": skeleton["action"], "layer": "L2"},
                {"type": "target", "value": skeleton["target"] or "未指定", "layer": "L2"},
                {"type": "priority", "value": skeleton["priority"], "layer": "L2"},
            ],
            "note": "把人话变成结构化的「这是什么操作」",
        }

    # ═══════════════════════════════════════════════════════════
    # L4 三色审计
    # ═══════════════════════════════════════════════════════════
    def _layer4_audit(self, text: str, skeleton: Dict[str, Any]) -> Dict[str, Any]:
        high_risk = ["密码", "token", "secret", "私钥", "删除全部", "rm -rf", "格式化", "清空", "drop"]
        if any(kw in text.lower() for kw in high_risk):
            return {
                "color": "🔴",
                "label": "熔断",
                "action": "FUSE-DNA 留痕，暂停执行，等待 UID9622 确认",
                "预判": "高风险操作，可能涉及数据安全或破坏性命令",
            }

        if skeleton["action"] in ("delete", "backup") or skeleton.get("priority", 0) >= 8:
            return {
                "color": "🟡",
                "label": "待审",
                "action": "追问边界/来源/影响范围，5 分钟超时降级",
                "预判": "操作影响较大，需要补充确认",
            }

        return {
            "color": "🟢",
            "label": "通行",
            "action": "继续执行",
            "预判": "常规操作，通心译闸门放行",
        }

    # ═══════════════════════════════════════════════════════════
    # L5 适配输出
    # ═══════════════════════════════════════════════════════════
    def _layer5_adapter(self, text: str, skeleton: Dict[str, Any], audit: Dict[str, Any]) -> Dict[str, Any]:
        recommendations = self._recommend_skills(text, skeleton)
        top_ids = [r["id"] for r in recommendations[:3]]

        if audit["color"] == "🔴":
            confirm_msg = "已熔断，必须等待 UID9622 手动确认"
        elif audit["color"] == "🟡":
            confirm_msg = "待审状态，建议 UID9622 确认后再执行"
        else:
            confirm_msg = "已通过通心译闸门，可继续执行"

        return {
            "style": "Kimi 主控",
            "output_format": "executable_struct",
            "recommended_skills": recommendations,
            "recommended_drawers": self._recommend_drawers(text, skeleton),
            "five_part_receipt": {
                "理解": f"识别为「{skeleton['action']}」意图",
                "补全": skeleton.get("missing") or "无",
                "预判": audit.get("预判", "继续执行"),
                "路径": top_ids,
                "确认": confirm_msg,
            },
        }

    def _recommend_skills(self, text: str, skeleton: Dict[str, Any]) -> List[Dict[str, Any]]:
        keywords = set(text.lower().split())
        action_keywords = {
            "execute": ["执行", "运行", "启动"],
            "query": ["查", "看", "列出", "搜索"],
            "create": ["创建", "生成", "新建"],
            "update": ["修改", "更新", "升级"],
            "delete": ["删除", "清理"],
            "backup": ["备份", "恢复"],
        }
        for term in action_keywords.get(skeleton["action"], []):
            keywords.add(term)

        scored = []
        for sk_id, meta in self.skill_metadata.items():
            desc = f"{sk_id} {meta.get('name', '')} {meta.get('description', '')}".lower()
            score = 0
            for kw in keywords:
                if kw in desc:
                    score += len(kw)
            if score > 0:
                scored.append((score, sk_id, meta))
        scored.sort(key=lambda x: x[0], reverse=True)

        return [
            {
                "id": sk_id,
                "name": meta.get("name"),
                "type": meta.get("type"),
                "score": score,
            }
            for score, sk_id, meta in scored[:5]
        ]

    def _recommend_drawers(self, text: str, skeleton: Dict[str, Any]) -> List[str]:
        hits = []
        action_map = {
            "execute": ["D-011"],
            "query": ["D-007", "D-033"],
            "create": ["D-031", "D-051"],
            "update": ["D-008", "D-032"],
            "delete": ["D-009"],
            "backup": ["D-046", "D-048"],
        }
        hits.extend(action_map.get(skeleton["action"], []))

        # 按关键词命中抽屉 trigger_word / name
        for drawer in self.drawers:
            search_text = f"{drawer.get('name', '')} {drawer.get('trigger_word', '')}"
            if any(kw in search_text for kw in text.split()):
                hits.append(drawer["drawer_id"])

        # 去重并保持顺序
        seen = set()
        result = []
        for d in hits:
            if d not in seen:
                seen.add(d)
                result.append(d)
        return result[:5]


if __name__ == "__main__":
    gate = TongxinyiGate()
    sample = "帮我查一下备份有没有成功"
    print(json.dumps(gate.translate(sample), ensure_ascii=False, indent=2))
