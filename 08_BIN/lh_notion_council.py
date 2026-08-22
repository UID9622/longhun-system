#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · Notion 对话桥 · 五行模型议事会 v1.0
DNA: #龍芯⚡️丙午·癸未·癸未·戊午·䷖剥-WUXING-COUNCIL-v1.0-UID9622
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0

功能：
  - 把本地/自训练模型 + Kimi + DeepSeek 组织成「五行议事会」
  - 木·生发、火·转化、土·承载、金·收敛、水·流动
  - 洛书矩阵特征值结构作为投票权重
  - 八卦状态机决定每轮调用哪些角色
  - 三色审计判定多模型一致性
"""
from __future__ import annotations

import re
import json
import time
import hashlib
import threading
from pathlib import Path
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed

try:
    import numpy as np
except ImportError:
    np = None


CONFIRM_CODE = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"


# 尝试加载 notion 模型注册表，用于识别自训练模型
_MODEL_REGISTRY: Dict[str, Any] = {}
try:
    _REGISTRY_PATH = Path(__file__).resolve().parent.parent / "data" / "notion_model_registry.json"
    if _REGISTRY_PATH.exists():
        _MODEL_REGISTRY = json.loads(_REGISTRY_PATH.read_text(encoding="utf-8"))
except Exception:
    _MODEL_REGISTRY = {}


def _is_self_trained(model_name: str) -> bool:
    """结合 registry 与名称前缀判定自训练模型。"""
    if not model_name:
        return False
    if any(model_name.lower().startswith(p.lower()) for p in ("longhun-", "龍魂-")):
        return True
    for m in _MODEL_REGISTRY.get("models", []):
        if m.get("id", "").lower() == model_name.lower():
            return bool(m.get("self_trained", False))
        if model_name.lower().startswith(m.get("id", "").lower() + ":"):
            return bool(m.get("self_trained", False))
    return False


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def generate_dna(prefix: str) -> str:
    ts = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S%f")[:-3]
    h = hashlib.sha256(f"{prefix}|{ts}".encode()).hexdigest()[:8].upper()
    return f"#龍芯⚡️{ts}-{prefix}-{h}"


# ============================================================
# 五行角色定义
# ============================================================

WUXING_ROLES = {
    "木": {
        "name": "木·生发",
        "emoji": "🌲",
        "function": "发散、创意、摘要扩展、联想",
        "preferred_models": ["moonshot-v1-128k", "moonshot-v1-32k", "moonshot-v1-8k", "moonshot-v1-auto"],
        "preferred_provider": "kimi",
        "weight": 0.20,
    },
    "火": {
        "name": "火·转化",
        "emoji": "🔥",
        "function": "推理、推演、漏洞发现、结构化",
        "preferred_models": ["deepseek-v4-pro", "deepseek-r1:14b"],
        "preferred_provider": "deepseek",
        "weight": 0.25,
    },
    "土": {
        "name": "土·承载",
        "emoji": "🟫",
        "function": "协议底座、主权表达、本地知识锚定",
        "preferred_models": ["longhun-v4.0", "longhun-v43-v3:latest", "longhun-v3.0", "qwen2.5"],
        "preferred_provider": "local",
        "weight": 0.35,
    },
    "金": {
        "name": "金·收敛",
        "emoji": "⚜️",
        "function": "判断、审计、去重、收敛最终结论",
        "preferred_models": [],  # 任意可用模型二次调用
        "preferred_provider": "auto",
        "weight": 0.12,
    },
    "水": {
        "name": "水·流动",
        "emoji": "💧",
        "function": "记忆召回、上下文关联、历史流动",
        "preferred_models": [],  # 轻量本地调用
        "preferred_provider": "local",
        "weight": 0.08,
    },
}

# 洛书矩阵特征值映射：实主值 15 为土，虚共轭 ±2√6·i 拆给火/木
LUOSHU_WEIGHTS = {
    "土": 15 / 60,   # 15
    "火": 12 / 60,   # ≈ 2√6
    "木": 10 / 60,
    "金": 6 / 60,
    "水": 4 / 60,
}


# ============================================================
# 八卦状态机
# ============================================================

BAGUA_STATES = {
    "乾": {"name": "乾·启", "emoji": "☰", "mood": " initiating", "roles": ["木", "火"], "desc": "开天启问，创意与推理并起"},
    "坤": {"name": "坤·承", "emoji": "☷", "mood": " grounding", "roles": ["土", "水"], "desc": "厚德载物，本地底座与记忆为主"},
    "震": {"name": "震·变", "emoji": "☳", "mood": " changing", "roles": ["火", "木"], "desc": "雷动变革，重推理与发散"},
    "巽": {"name": "巽·流", "emoji": "☴", "mood": " flowing", "roles": ["水", "木"], "desc": "风行渗透，记忆与联想为主"},
    "坎": {"name": "坎·深", "emoji": "☵", "mood": " deepening", "roles": ["火", "水"], "desc": "水险渊深，推理+记忆挖掘"},
    "离": {"name": "离·明", "emoji": "☲", "mood": " clarifying", "roles": ["火", "金"], "desc": "火光照物，推理后收敛判断"},
    "艮": {"name": "艮·止", "emoji": "☶", "mood": " stopping", "roles": ["土", "金"], "desc": "山止为界，本地底座+审计收尾"},
    "兑": {"name": "兑·悦", "emoji": "☱", "mood": " sharing", "roles": ["木", "金"], "desc": "泽悦交流，创意发散后收敛"},
}


@dataclass
class CouncilMember:
    role: str
    provider: str
    model: str
    status: str
    latency_ms: Optional[int] = None
    error: str = ""


@dataclass
class CouncilResponse:
    role: str
    provider: str
    model: str
    reply: str
    dna: str
    latency_ms: int
    weight: float


class BaguaDialogueState:
    """八卦对话状态机。"""

    INITIAL = "乾"

    def __init__(self):
        self._sessions: Dict[str, str] = {}
        self._lock = threading.Lock()

    def get(self, session_id: str) -> str:
        with self._lock:
            return self._sessions.get(session_id, self.INITIAL)

    def transition(self, session_id: str, message: str, last_audit: str = "green") -> str:
        """根据消息意图和上一轮审计结果转移状态。"""
        current = self.get(session_id)

        # 导航/查看意图 → 坤（承载/ grounded）
        if any(k in message for k in ["查看", "打开", "导航", "跳转到", "关联"]):
            next_state = "坤"
        # 为什么/分析/推演 → 坎（深）或 离（明）
        elif any(k in message for k in ["为什么", "分析", "推演", "推理", "证明"]):
            next_state = "坎" if current in ("乾", "震") else "离"
        # 总结/收敛/判断 → 艮（止）或 兑（悦）
        elif any(k in message for k in ["总结", "结论", "判断", "决定", "收敛"]):
            next_state = "艮" if last_audit == "red" else "兑"
        # 历史/记忆 → 巽（流）
        elif any(k in message for k in ["之前", "历史", "记忆", "上文", "刚才"]):
            next_state = "巽"
        # 变化/转换 → 震（变）
        elif any(k in message for k in ["变成", "转换", "修改", "调整"]):
            next_state = "震"
        # 默认：在乾/坤之间振荡，保持多样性
        else:
            next_state = "坤" if current == "乾" else "乾"

        with self._lock:
            self._sessions[session_id] = next_state
        return next_state

    def roles_for(self, state: str) -> List[str]:
        return BAGUA_STATES.get(state, BAGUA_STATES[self.INITIAL]).get("roles", ["土", "火"])

    def info(self, session_id: str) -> Dict[str, Any]:
        state = self.get(session_id)
        info = BAGUA_STATES.get(state, BAGUA_STATES[self.INITIAL])
        return {
            "state": state,
            "name": info["name"],
            "emoji": info["emoji"],
            "mood": info["mood"],
            "roles": info["roles"],
            "desc": info["desc"],
        }


class WuxingModelCouncil:
    """五行模型议事会：多模型协作决策核心。"""

    def __init__(self, model_router: Any):
        self.router = model_router
        self.bagua = BaguaDialogueState()
        self._executor = ThreadPoolExecutor(max_workers=5)

    # ── 角色分配 ──

    def assign_roles(self, probes: Optional[List[Dict[str, Any]]] = None) -> Dict[str, CouncilMember]:
        """根据可用模型把五行角色分配给实际 provider/model。"""
        if probes is None:
            probes = self.router.probe_all()
        probe_map = {p["provider"]: p for p in probes}
        available = {p: info for p, info in probe_map.items() if info.get("status") == "online"}

        assignments: Dict[str, CouncilMember] = {}
        used_models: Dict[str, str] = {}  # provider -> model

        def pick_model(provider: str, preferred: List[str], prefer_self_trained: bool = False) -> str:
            models = probe_map.get(provider, {}).get("models", [])
            # 1) 优先 registry 声明的 preferred_models
            for m in preferred:
                if any(m.lower() in x.lower() for x in models):
                    return m
            # 2) 若角色要求自训练优先（如 土·承载），先选自训练本地模型
            if prefer_self_trained:
                for m in models:
                    if _is_self_trained(m):
                        return m
            # 3) 默认自训练前缀兜底
            for m in models:
                if any(m.lower().startswith(p.lower()) for p in ["longhun-v", "longhun-", "龍魂-"]):
                    return m
            return models[0] if models else "default"

        # 1. 土：本地/自训练模型（协议底座，强制优先自训练）
        if "local" in available:
            model = pick_model("local", WUXING_ROLES["土"]["preferred_models"], prefer_self_trained=True)
            assignments["土"] = CouncilMember("土", "local", model, "online")
            used_models["local"] = model

        # 2. 火：DeepSeek 推理模型
        if "deepseek" in available:
            model = pick_model("deepseek", WUXING_ROLES["火"]["preferred_models"])
            assignments["火"] = CouncilMember("火", "deepseek", model, "online")
            used_models["deepseek"] = model

        # 3. 木：Kimi 长上下文模型
        if "kimi" in available:
            model = pick_model("kimi", WUXING_ROLES["木"]["preferred_models"])
            assignments["木"] = CouncilMember("木", "kimi", model, "online")
            used_models["kimi"] = model

        # 4. 水：复用本地轻量模型（若本地存在）
        if "local" in available:
            model = used_models.get("local") or pick_model("local", [])
            assignments["水"] = CouncilMember("水", "local", model, "online")

        # 5. 金：复用已有 provider 中延迟最低者做审计
        ranked = sorted(
            [(p, info) for p, info in available.items() if p in used_models],
            key=lambda x: x[1].get("latency_ms", 9999) or 9999,
        )
        if ranked:
            provider = ranked[0][0]
            model = used_models.get(provider, "default")
            assignments["金"] = CouncilMember("金", provider, model, "online")

        # 缺失角色由相生补位：缺金→土兼金，缺水→金兼水，缺木→水兼木，缺火→木兼火，缺土→火兼土
        sheng_cycle = {"金": "土", "水": "金", "木": "水", "火": "木", "土": "火"}
        for role in WUXING_ROLES:
            if role not in assignments:
                donor = sheng_cycle[role]
                if donor in assignments:
                    donor_m = assignments[donor]
                    assignments[role] = CouncilMember(
                        role, donor_m.provider, donor_m.model, "online",
                        latency_ms=donor_m.latency_ms,
                        error=f"由{donor}相生补位"
                    )

        return assignments

    # ── 并行调用 ──

    def _call_role(
        self,
        role: str,
        member: CouncilMember,
        messages: List[Dict[str, str]],
        system_prefix: str,
        temperature: float,
        max_tokens: int,
    ) -> CouncilResponse:
        """调用单个角色。"""
        role_info = WUXING_ROLES[role]
        system = (
            f"【龍魂宇宙论 · 五行议事会】你在本次议事中承担「{role_info['name']}」的职能：{role_info['function']}。\n"
            f"{system_prefix}\n"
            "要求：\n"
            "1. 直接回答用户问题，不要自我介绍或强调你的角色身份。\n"
            "2. 从上述职能视角出发，给出 1~3 条核心要点。\n"
            "3. 每条要点用「•」开头，保持简洁。\n"
            "4. 不编造资料外信息；若不了解，明确说明。"
        )
        msgs = [{"role": "system", "content": system}] + messages
        start = time.time()
        try:
            result = self.router.generate(
                msgs,
                provider=member.provider,
                model=member.model,
                temperature=temperature,
                max_tokens=max_tokens,
            )
            latency = int((time.time() - start) * 1000)
            return CouncilResponse(
                role=role,
                provider=result.get("provider", member.provider),
                model=result.get("model", member.model),
                reply=result.get("reply", ""),
                dna=result.get("dna", generate_dna(f"COUNCIL-{role}")),
                latency_ms=latency,
                weight=role_info["weight"],
            )
        except Exception as e:
            return CouncilResponse(
                role=role,
                provider=member.provider,
                model=member.model,
                reply=f"[{role} 角色调用失败: {str(e)[:80]}]",
                dna=generate_dna(f"COUNCIL-{role}-ERR"),
                latency_ms=int((time.time() - start) * 1000),
                weight=role_info["weight"],
            )

    def _extract_bullets(self, text: str) -> List[str]:
        """从回复中提取 bullet points。"""
        lines = [l.strip() for l in text.splitlines() if l.strip()]
        bullets = []
        for line in lines:
            # 支持 • - * 1. 等开头
            cleaned = re.sub(r"^[\s•\-\*\d\.\)）]+", "", line).strip()
            if cleaned and len(cleaned) > 6:
                bullets.append(cleaned)
        return bullets[:5]

    def _similarity(self, a: str, b: str) -> float:
        """简单语义相似度（Jaccard + 长度惩罚）。"""
        if not a or not b:
            return 0.0
        sa = set(re.findall(r"[\u4e00-\u9fa5]{2,}", a)) or set(a.split())
        sb = set(re.findall(r"[\u4e00-\u9fa5]{2,}", b)) or set(b.split())
        if not sa or not sb:
            return 0.0
        inter = len(sa & sb)
        union = len(sa | sb)
        jaccard = inter / union if union else 0.0
        # 长度差异惩罚
        len_ratio = min(len(a), len(b)) / max(len(a), len(b)) if max(len(a), len(b)) else 1.0
        return round(jaccard * 0.7 + len_ratio * 0.3, 3)

    def _synthesize(self, responses: List[CouncilResponse], weights: Dict[str, float]) -> Tuple[str, Dict[str, Any]]:
        """合成各角色输出。策略：以土为底，合并火/木新增要点，金做收尾，水提供上下文。"""
        by_role = {r.role: r for r in responses}

        # 土为底
        base = by_role.get("土")
        if not base or not base.reply.strip() or base.reply.startswith("["):
            base = next((r for r in responses if r.reply.strip() and not r.reply.startswith("[")), None)
        base_text = base.reply if base else ""

        base_bullets = self._extract_bullets(base_text) if base else []
        all_bullets: List[Tuple[str, str, float]] = []  # (text, role, weight)
        for r in responses:
            if r.role == "土" or not r.reply.strip() or r.reply.startswith("["):
                continue
            for b in self._extract_bullets(r.reply):
                all_bullets.append((b, r.role, weights.get(r.role, 0.1)))

        # 去重：与已有 bullet 相似度 > 0.72 视为重复
        merged = list(base_bullets)
        novel: List[Tuple[str, str, float]] = []
        for text, role, w in all_bullets:
            if any(self._similarity(text, m) > 0.72 for m in merged):
                continue
            merged.append(text)
            novel.append((text, role, w))

        # 金角色做收敛：若存在且回复有效，用其做最终润色
        gold = by_role.get("金")
        if gold and gold.reply.strip() and not gold.reply.startswith("["):
            gold_text = gold.reply.strip()
        else:
            gold_text = ""

        # 组装最终回复
        lines = []
        if base_text and base_text.strip() and not base_text.startswith("["):
            lines.append(base_text.strip())
        if novel:
            lines.append("\n💡 其他委员补充：")
            for text, role, _ in novel[:4]:
                lines.append(f"  • {WUXING_ROLES[role]['emoji']} {role}：{text}")
        if gold_text:
            lines.append(f"\n⚜️ 金·收敛：{gold_text}")

        final = "\n".join(lines).strip()
        if not final:
            final = "[议事会未能形成有效结论，请检查模型可用性]"

        synthesis_log = {
            "base_role": base.role if base else None,
            "base_bullets": base_bullets,
            "novel_bullets": [{"text": t, "role": r, "weight": w} for t, r, w in novel],
            "gold_summary": gold_text,
        }
        return final, synthesis_log

    def _audit(self, responses: List[CouncilResponse]) -> Tuple[str, float, List[Dict[str, Any]]]:
        """三色审计：计算多模型输出一致性。"""
        valid = [r for r in responses if r.reply.strip() and not r.reply.startswith("[")]
        if len(valid) < 2:
            return "yellow", 0.0, []

        sims = []
        for i in range(len(valid)):
            for j in range(i + 1, len(valid)):
                sim = self._similarity(valid[i].reply, valid[j].reply)
                sims.append({
                    "pair": f"{valid[i].role}-{valid[j].role}",
                    "similarity": sim,
                })
        if not sims:
            return "yellow", 0.0, []
        avg_sim = round(sum(s["similarity"] for s in sims) / len(sims), 3)

        if avg_sim >= 0.82:
            return "green", avg_sim, sims
        elif avg_sim >= 0.55:
            return "yellow", avg_sim, sims
        else:
            return "red", avg_sim, sims

    # ── 公开入口 ──

    def chat(
        self,
        session_id: str,
        message: str,
        messages: List[Dict[str, str]],
        sources: List[Dict[str, Any]],
        system_prefix: str = "",
        temperature: float = 0.35,
        max_tokens: int = 512,
    ) -> Dict[str, Any]:
        """五行议事会主入口。"""
        council_dna = generate_dna("WUXING-COUNCIL")

        # 1. 状态转移
        last_audit = "green"  # 默认，实际可由上下文传入
        state = self.bagua.transition(session_id, message, last_audit)
        state_info = self.bagua.info(session_id)
        roles = state_info["roles"]

        # 2. 角色分配
        probes = self.router.probe_all()
        assignments = self.assign_roles(probes)

        # 3. 只调用当前卦象偏好的角色（最多 3 个）+ 金审计
        # 优先保留卦象主角色；若某角色分配到的 provider 已被占用，尝试换到未占用 provider。
        candidate_roles = list(dict.fromkeys(roles + (["金"] if "金" in assignments else [])))
        active_roles = []
        used_providers = set()
        for r in candidate_roles:
            if r not in assignments:
                continue
            # 若当前分配 provider 已被占用，尝试从未占用 provider 中挑一个可用模型
            member = assignments[r]
            if member.provider in used_providers:
                available_probes = [p for p in probes if p.get("status") == "online" and p["provider"] not in used_providers]
                if available_probes:
                    # 按延迟排序，优先低延迟
                    available_probes.sort(key=lambda p: p.get("latency_ms", 9999) or 9999)
                    probe = available_probes[0]
                    models = probe.get("models", [])
                    model = models[0] if models else "default"
                    assignments[r] = CouncilMember(r, probe["provider"], model, "online", latency_ms=probe.get("latency_ms"))
                else:
                    continue
            active_roles.append(r)
            used_providers.add(assignments[r].provider)
            if len(active_roles) >= 3:
                break
        if not active_roles:
            active_roles = ["土"] if "土" in assignments else list(assignments.keys())[:1]

        # 4. 并行调用
        futures = {
            self._executor.submit(
                self._call_role, role, assignments[role], messages, system_prefix, temperature, max_tokens
            ): role
            for role in active_roles
        }
        responses: List[CouncilResponse] = []
        for fut in as_completed(futures):
            responses.append(fut.result())

        # 5. 合成
        weights = {r: LUOSHU_WEIGHTS[r] for r in active_roles}
        # 重归一化
        total = sum(weights.values())
        weights = {k: round(v / total, 3) for k, v in weights.items()}
        final_reply, synthesis_log = self._synthesize(responses, weights)

        # 6. 审计
        audit_status, consensus_score, similarities = self._audit(responses)

        # 7. 组装结果
        council_members = []
        for role, member in assignments.items():
            resp = next((r for r in responses if r.role == role), None)
            council_members.append({
                "role": role,
                "name": WUXING_ROLES[role]["name"],
                "emoji": WUXING_ROLES[role]["emoji"],
                "provider": member.provider,
                "model": member.model,
                "status": "participated" if resp else "assigned",
                "latency_ms": resp.latency_ms if resp else member.latency_ms,
                "weight": weights.get(role, 0.0),
                "reply_preview": (resp.reply[:120] + "...") if resp and len(resp.reply) > 120 else (resp.reply if resp else ""),
                "dna": resp.dna if resp else generate_dna(f"ASSIGN-{role}"),
            })

        return {
            "status": "ok",
            "audit_level": audit_status,
            "reply": final_reply,
            "provider": "council",
            "model": "wuxing-council-v1.0",
            "dna": council_dna,
            "confirm_code": CONFIRM_CODE,
            "sovereignty": "龍魂UID9622",
            "audit_status": audit_status,
            "consensus_score": consensus_score,
            "bagua_state": state_info,
            "council_members": council_members,
            "synthesis_log": synthesis_log,
            "similarities": similarities,
            "fallback_chain": [],
            "total_latency_ms": sum(r.latency_ms for r in responses),
        }

    def status(self) -> Dict[str, Any]:
        """返回议事会当前委员状态。"""
        probes = self.router.probe_all()
        assignments = self.assign_roles(probes)
        return {
            "dna": generate_dna("COUNCIL-STATUS"),
            "timestamp": _now(),
            "roles": {
                role: {
                    "name": WUXING_ROLES[role]["name"],
                    "emoji": WUXING_ROLES[role]["emoji"],
                    "provider": m.provider,
                    "model": m.model,
                    "status": m.status,
                    "latency_ms": m.latency_ms,
                }
                for role, m in assignments.items()
            },
            "probes": probes,
        }
