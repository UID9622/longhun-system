#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂智能体编排器 v1.2

- 读取 manifest.json 中的智能体注册表
- 根据输入文本关键词匹配最合适的智能体/人格
- 支持 L1 常驻、L2 按需、L3 人格三层模型
- 四层路由：关键词 → empower-engine → agent-eco → 神经网络桥接
- 已缠尾：全部 213 个智能体/技能接入编排
- 100% 本地运行，纯标准库

DNA: #龍芯⚡️2026-07-06-AGENT-ORCHESTRATOR-v1.2-NEURAL
"""

import json
import re
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, List

from agent_daemon import start_daemon as _start_daemon, stop_daemon as _stop_daemon  # pyright: ignore[reportImplicitRelativeImport]
from agent_status_reporter import generate_report as _generate_report  # pyright: ignore[reportImplicitRelativeImport]


SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = SCRIPT_DIR  # agents/ 目录，ROOT.parent 即项目根
MANIFEST_PATH = SCRIPT_DIR / "manifest.json"
DNA_SIGNATURE = "#龍芯⚡️2026-07-06-AGENT-ORCHESTRATOR-v1.2-NEURAL"
VERSION = "v1.2"

# 可选：接入 longhun-empower-engine 进行语义路由兜底
_empower_engine = None
_EMPOWER_PATH = Path.home() / ".kimi-code" / "skills" / "longhun-empower-engine" / "scripts"
if _EMPOWER_PATH.exists():
    try:
        sys.path.insert(0, str(_EMPOWER_PATH))
        from empower_engine_v2 import EmpowerEngine  # pyright: ignore[reportMissingImports]

        _empower_engine = EmpowerEngine()
    except Exception:
        _empower_engine = None

# 可选：接入 longhun-agent-eco 动态调度
_agent_eco = None
_eco_route = None
_eco_status = None
_eco_list = None
try:
    from agent_eco_adapter import (  # pyright: ignore[reportImplicitRelativeImport]
        eco_route as _eco_route,
        eco_status as _eco_status,
        eco_list as _eco_list,
    )

    _agent_eco = True
except Exception:
    _agent_eco = None

# 可选：接入神经网络·智能体桥接器
_neural_bridge = None
_NEURAL_BRIDGE_PATH = SCRIPT_DIR.parent / "cnsh-core" / "neural_agent_bridge.py"
if _NEURAL_BRIDGE_PATH.exists():
    try:
        sys.path.insert(0, str(_NEURAL_BRIDGE_PATH.parent))
        from neural_agent_bridge import NeuralAgentBridge  # pyright: ignore[reportMissingImports]
        _neural_bridge = NeuralAgentBridge()
    except Exception:
        _neural_bridge = None


class AgentOrchestrator:
    """
    智能体编排器。

    不固化后台、不依赖外部平台，新增智能体只需改 manifest.json。
    """

    def __init__(self, manifest_path: Path = MANIFEST_PATH):
        self.manifest_path = manifest_path
        self.manifest = self._load_manifest()
        self.agents = self.manifest.get("agents", [])
        self.audit_log_path = Path.home() / ".longhun" / "agents" / "orchestrator_audit.jsonl"
        self.audit_log_path.parent.mkdir(parents=True, exist_ok=True)

    def _load_manifest(self) -> dict[str, Any]:
        with self.manifest_path.open("r", encoding="utf-8") as f:
            return json.load(f)

    @staticmethod
    def _preprocess(text: str) -> str:
        text = str(text).strip().lower()
        text = re.sub(r"[\s\u3000]+", " ", text)
        return text[:5000]

    def route(self, text: str) -> dict[str, Any]:
        """根据输入文本匹配最合适的智能体。"""
        start = time.time()
        cleaned = self._preprocess(text)

        if len(cleaned) < 2:
            return self._fallback(cleaned, "输入过短")

        matches = self._match_agents(cleaned)
        if matches:
            # 排序：L1 优先于 L2 优先于 L3；同层内匹配词越多越靠前
            layer_order = {"L1": 0, "L2": 1, "L3": 2}
            matches.sort(
                key=lambda a: (
                    layer_order.get(a["layer"], 99),
                    -a["match_count"],
                    -a["priority_score"],
                )
            )
            return self._build_result(cleaned, matches, start)

        # 无直接关键词匹配时，尝试用 empower-engine 做语义兜底
        if _empower_engine is not None:
            try:
                empower_result = _empower_engine.identify(cleaned)
                return self._build_from_empower(cleaned, empower_result, start)
            except Exception:
                pass

        # 若 empower-engine 也未命中，调用 longhun-agent-eco v2 路由引擎
        if _agent_eco is not None:
            try:
                eco_result = _eco_route(cleaned)  # pyright: ignore[reportOptionalCall]
                if eco_result.get("狀態") == "success":
                    return self._build_from_eco(cleaned, eco_result, start)
            except Exception:
                pass

        # 若以上均未命中，调用神经网络·智能体桥接器
        if _neural_bridge is not None:
            try:
                neural_result = _neural_bridge.route(cleaned)
                if neural_result.primary_agent:
                    return self._build_from_neural(cleaned, neural_result, start)
            except Exception:
                pass

        # v1.3: 若以上均未命中，调用流场协同引擎做多人格协同路由
        if len(cleaned) > 10:
            try:
                collab_result = self._route_via_collab_flow(cleaned)
                if collab_result:
                    return self._build_from_collab(cleaned, collab_result, start)
            except Exception:
                pass

        return self._fallback(cleaned, "未匹配到智能体")

    def _match_agents(self, text: str) -> list[dict[str, Any]]:
        results = []
        for agent in self.agents:
            keywords = agent.get("keywords", [])
            matched = [kw for kw in keywords if kw.lower() in text]
            if not matched:
                continue
            # 匹配词长度加权和：长词/短语匹配更精确（平方加权）
            priority_score = sum(len(kw.lower()) ** 2 for kw in matched)
            # 短语额外加分：包含空格的关键词命中说明更精确
            phrase_bonus = sum(len(kw.lower()) for kw in matched if " " in kw.lower())
            # 特异性加分：命中词出现在智能体 id/name 中，说明更对症
            identity = f"{agent.get('id', '')} {agent.get('name', '')}".lower()
            specificity_bonus = sum(len(kw.lower()) * 2 for kw in matched if kw.lower() in identity)
            agent_copy = dict(agent)
            agent_copy["matched_keywords"] = matched
            agent_copy["match_count"] = len(matched)
            agent_copy["priority_score"] = priority_score + phrase_bonus + specificity_bonus
            results.append(agent_copy)
        return results

    def _build_result(
        self,
        cleaned: str,
        matches: list[dict[str, Any]],
        start: float,
    ) -> dict[str, Any]:
        primary = matches[0]
        secondary = matches[1] if len(matches) > 1 else None

        result = {
            "dna": DNA_SIGNATURE,
            "version": VERSION,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "input_summary": cleaned[:20] + ("…" if len(cleaned) > 20 else ""),
            "routing_mode": "keyword",
            "matches": [
                {
                    "id": a["id"],
                    "name": a["name"],
                    "layer": a["layer"],
                    "type": a["type"],
                    "logic": a["logic"],
                    "persona_code": a["persona_code"],
                    "matched_keywords": a["matched_keywords"],
                    "description": a["description"],
                }
                for a in matches
            ],
            "primary_agent": {
                "id": primary["id"],
                "name": primary["name"],
                "layer": primary["layer"],
                "logic": primary["logic"],
                "persona_code": primary["persona_code"],
            },
            "routing_advice": self._routing_advice(primary, secondary),
            "processing_time_ms": round((time.time() - start) * 1000, 1),
        }
        self._write_audit_log(result)
        return result

    def _build_from_empower(
        self,
        cleaned: str,
        empower_result: dict[str, Any],
        start: float,
    ) -> dict[str, Any]:
        """当关键词未命中时，用 empower-engine 的语义结果映射到 L3 人格智能体。"""
        persona_code = empower_result.get("primary_persona", "P01")
        agent = next(
            (a for a in self.agents if a.get("persona_code") == persona_code),
            None,
        )
        if agent is None:
            return self._fallback(cleaned, "empower-engine 返回的人格未注册")

        result = {
            "dna": DNA_SIGNATURE,
            "version": VERSION,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "input_summary": cleaned[:20] + ("…" if len(cleaned) > 20 else ""),
            "routing_mode": "semantic",
            "empower_engine": {
                "primary_persona": persona_code,
                "primary_category": empower_result.get("primary_category"),
                "empower_level": empower_result.get("empower_level"),
                "categories": empower_result.get("categories", []),
            },
            "matches": [],
            "primary_agent": {
                "id": agent["id"],
                "name": agent["name"],
                "layer": agent["layer"],
                "logic": agent["logic"],
                "persona_code": agent["persona_code"],
            },
            "routing_advice": (
                f"由语义路由命中 {agent['layer']} 智能体「{agent['name']}」，"
                f"执行{agent['logic']}（{empower_result.get('routing_advice', '')}）"
            ),
            "processing_time_ms": round((time.time() - start) * 1000, 1),
        }
        self._write_audit_log(result)
        return result

    def _build_from_eco(
        self,
        cleaned: str,
        eco_result: dict[str, Any],
        start: float,
    ) -> dict[str, Any]:
        """当关键词与 empower-engine 均未命中时，由 agent-eco v2 路由引擎调度。"""
        matched_ids = eco_result.get("匹配智能體", [])
        tag = eco_result.get("匹配標籤", "")
        matched_keywords = eco_result.get("匹配關鍵詞", [])

        # 把 AGENT-XXX 解析为可读名称
        name_map = {}
        if _agent_eco is not None:
            try:
                for a in _eco_list():  # pyright: ignore[reportOptionalCall]
                    name_map[a["id"]] = a["name"]
            except Exception:
                pass

        matches = [
            {
                "id": aid,
                "name": name_map.get(aid, aid),
                "layer": "L2-eco",
                "type": "agent-eco",
                "logic": f"agent-eco {tag} 路由",
                "persona_code": aid,
                "matched_keywords": matched_keywords,
            }
            for aid in matched_ids
        ]
        primary = matches[0] if matches else None

        result = {
            "dna": DNA_SIGNATURE,
            "version": VERSION,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "input_summary": cleaned[:20] + ("…" if len(cleaned) > 20 else ""),
            "routing_mode": "agent-eco",
            "eco_route": eco_result,
            "matches": matches,
            "primary_agent": primary or {
                "id": "P01",
                "name": "诸葛亮",
                "layer": "L3",
                "logic": "战略推演逻辑",
                "persona_code": "P01",
            },
            "routing_advice": (
                f"由 agent-eco v2 路由命中 {tag or '混合'} 标签，"
                f"调度至 {', '.join(matched_ids)}"
            ) if matched_ids else "agent-eco 未给出明确目标",
            "processing_time_ms": round((time.time() - start) * 1000, 1),
        }
        self._write_audit_log(result)
        return result

    def _build_from_neural(
        self,
        cleaned: str,
        neural_result: Any,
        start: float,
    ) -> dict[str, Any]:
        """当关键词、empower-engine、agent-eco 均未命中时，由神经网络桥接器路由。"""
        result = {
            "dna": DNA_SIGNATURE,
            "version": VERSION,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "input_summary": cleaned[:20] + ("…" if len(cleaned) > 20 else ""),
            "routing_mode": "neural",
            "neural_status": neural_result.neural_status,
            "neural_health": neural_result.network_health,
            "constitution_ok": neural_result.constitution_ok,
            "wuxing_flow": neural_result.wuxing_flow,
            "routing_path": neural_result.routing_path,
            "matches": neural_result.matched_agents[:5],
            "primary_agent": neural_result.primary_agent or {
                "id": "P01",
                "name": "诸葛亮",
                "layer": "L3",
                "logic": "战略推演逻辑",
                "persona_code": "P01",
            },
            "routing_advice": neural_result.advice or "神经网络路由兜底",
            "processing_time_ms": round((time.time() - start) * 1000, 1),
        }
        self._write_audit_log(result)
        return result

    def daemon_status(self) -> dict[str, Any]:
        """读取 L1 守护进程状态文件。"""
        from agent_daemon import _read_pid, _is_alive, read_json  # pyright: ignore[reportImplicitRelativeImport]
        pid = _read_pid()
        alive = bool(pid and _is_alive(pid))
        state = read_json(Path.home() / "longhun-system" / "agents" / "daemon_state.json", {})
        heartbeat = read_json(Path.home() / "longhun-system" / "agents" / "daemon_logs" / "heartbeat.json", {})
        return {
            "daemon_running": alive,
            "pid": pid,
            "version": state.get("version", "unknown"),
            "started_at": state.get("started_at"),
            "agents": heartbeat.get("agents", []),
        }

    def eco_status(self) -> dict[str, Any]:
        """获取 agent-eco 生态系统状态。"""
        if _agent_eco is None:
            return {"available": False, "error": "agent-eco 适配器未加载"}
        return {"available": True, "data": _eco_status()}  # pyright: ignore[reportOptionalCall]

    def show_skill(self, skill_id: str) -> dict[str, Any]:
        """查看某个已注册技能/智能体的详情与调用方式。"""
        agent = next((a for a in self.agents if a.get("id") == skill_id), None)
        if agent is None:
            return {"error": f"未找到 {skill_id}"}
        return {
            "id": agent["id"],
            "name": agent["name"],
            "layer": agent["layer"],
            "logic": agent["logic"],
            "description": agent.get("description", ""),
            "entrypoint": agent.get("entrypoint"),
            "skill_path": agent.get("skill_path"),
            "keywords": agent.get("keywords", []),
            "dna": agent.get("dna", ""),
        }

    def run_skill(self, skill_id: str, args: list[str]) -> dict[str, Any]:
        """尝试运行技能的 entrypoint（仅限本地脚本）。"""
        agent = next((a for a in self.agents if a.get("id") == skill_id), None)
        if agent is None:
            return {"success": False, "error": f"未找到 {skill_id}"}
        entry = agent.get("entrypoint")
        if not entry:
            return {
                "success": False,
                "error": f"{skill_id} 没有可执行 entrypoint，这是一个文档/规范型技能",
                "skill": self.show_skill(skill_id),
            }
        path = Path(entry).expanduser()
        if not path.exists():
            return {"success": False, "error": f"entrypoint 不存在: {path}"}
        # 安全：只运行 home 目录下的脚本
        try:
            path.relative_to(Path.home())
        except ValueError:
            return {"success": False, "error": "entrypoint 不在用户主目录下，拒绝执行"}

        cmd = [str(path)] + args
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30,
            )
            return {
                "success": result.returncode == 0,
                "command": " ".join(cmd),
                "returncode": result.returncode,
                "stdout": result.stdout[:2000],
                "stderr": result.stderr[:1000],
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def _routing_advice(self, primary: dict[str, Any], secondary: dict[str, Any] | None) -> str:
        name = primary["name"]
        logic = primary["logic"]
        layer = primary["layer"]

        base = f"由 {layer} 智能体「{name}」主理，执行{logic}"
        if secondary:
            base += f"；「{secondary['name']}」({secondary['logic']}) 辅助"
        return base

    def _fallback(self, cleaned: str, reason: str) -> dict[str, Any]:
        result = {
            "dna": DNA_SIGNATURE,
            "version": VERSION,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "input_summary": cleaned[:20] + ("…" if len(cleaned) > 20 else ""),
            "routing_mode": "fallback",
            "matches": [],
            "primary_agent": {
                "id": "P01",
                "name": "诸葛亮",
                "layer": "L3",
                "逻辑": "战略推演逻辑",
                "persona_code": "P01",
            },
            "routing_advice": f"未匹配到智能体（{reason}），降级到 P01 诸葛亮通用咨询模式",
            "processing_time_ms": 0.0,
        }
        self._write_audit_log(result)
        return result

    # ═══════════════════════════════════════════════════════════════
    # v1.3: 流场协同引擎集成
    # ═══════════════════════════════════════════════════════════════

    _collab_engine = None

    def _get_collab_engine(self):
        """惰性加载流场协同引擎"""
        if self._collab_engine is None:
            try:
                flowfield_path = ROOT.parent / "scripts" / "round1" / "flowfield_collab_engine.py"
                if flowfield_path.exists():
                    sys.path.insert(0, str(flowfield_path.parent))
                    from flowfield_collab_engine import (  # type: ignore[import-untyped]
                        create_default_collab_field,
                        CollabTask,
                        WuxingElement,
                        CollabMode,
                        CollabTaskDistributor,
                    )
                    self._collab_engine = {
                        "field": create_default_collab_field,
                        "CollabTask": CollabTask,
                        "WuxingElement": WuxingElement,
                        "CollabMode": CollabMode,
                        "CollabTaskDistributor": CollabTaskDistributor,
                    }
            except Exception:
                self._collab_engine = {}
        return self._collab_engine

    def _route_via_collab_flow(self, text: str) -> dict[str, Any] | None:
        """
        v1.3: 通过流场协同引擎做多人格协同路由

        当单体路由都未命中时，自动启动多人格协同推演：
        1. 分析任务所需的五行属性
        2. 从默认协同场中选出最佳协同团队
        3. 检测协同冲突并给出补救建议
        """
        eng = self._get_collab_engine()
        if not eng:
            return None

        try:
            CollabTask = eng["CollabTask"]
            WuxingElement = eng["WuxingElement"]
            CollabMode = eng["CollabMode"]
            field = eng["field"]()
            distributor = eng["CollabTaskDistributor"](field)

            # 根据输入文本推断任务五行需求
            required_wuxing = _infer_task_wuxing(text)
            required_role = _infer_task_role(text)
            mode = _infer_collab_mode(text)

            task = CollabTask(
                id=f"COLLAB-{datetime.now().strftime('%H%M%S')}",
                title=text[:30],
                description=text,
                required_wuxing=required_wuxing,
                required_role=required_role,
                mode=mode,
                priority=2,
            )
            assignment = distributor.auto_assign(task)

            # 获取协同场报告
            from flowfield_collab_engine import CollabConflictDetector, FlowFieldFusionEngine  # type: ignore[import-untyped]
            fusion = FlowFieldFusionEngine(field).compute_fusion()
            conflicts = CollabConflictDetector(field).detect_all()

            return {
                "task": task,
                "assignment": assignment,
                "fusion": fusion,
                "conflicts": conflicts,
                "field": field,
            }
        except Exception:
            return None

    def _build_from_collab(
        self,
        cleaned: str,
        collab_result: dict[str, Any],
        start: float,
    ) -> dict[str, Any]:
        """将流场协同路由结果转化为标准路由响应"""
        assignment = collab_result["assignment"]
        fusion = collab_result["fusion"]

        assigned_names = [a["name"] for a in assignment.get("assigned_to", [])]
        result = {
            "dna": DNA_SIGNATURE,
            "version": VERSION,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "input_summary": cleaned[:20] + ("…" if len(cleaned) > 20 else ""),
            "routing_mode": "collab_flow",
            "fusion_index": fusion["fusion_index"],
            "fusion_status": fusion["fusion_status"],
            "dominant_wuxing": fusion["dominant_wuxing"],
            "matches": [
                {
                    "id": a["id"],
                    "name": a["name"],
                    "score": a["score"],
                    "wuxing": a.get("wuxing", "N/A"),
                }
                for a in assignment.get("assigned_to", [])
            ],
            "primary_agent": (
                {
                    "id": assignment["assigned_to"][0]["id"],
                    "name": assignment["assigned_to"][0]["name"],
                    "layer": "L3",
                    "logic": f"流场协同路由·{fusion['dominant_wuxing']}行主导",
                    "persona_code": assignment["assigned_to"][0].get("id", "N/A"),
                }
                if assignment.get("assigned_to")
                else {
                    "id": "P01",
                    "name": "诸葛亮",
                    "layer": "L3",
                    "logic": "协同路由兜底",
                    "persona_code": "P01",
                }
            ),
            "routing_advice": (
                f"流场协同路由：{', '.join(assigned_names)} 协同执行 · "
                f"融合指数 {fusion['fusion_index']:.2f} · {fusion['fusion_status']}"
            ),
            "collab_detail": {
                "team": assigned_names,
                "fusion_index": fusion["fusion_index"],
                "dominant_wuxing": fusion["dominant_wuxing"],
                "sancai": fusion["fused_sancai"],
            },
            "processing_time_ms": round((time.time() - start) * 1000, 1),
        }
        self._write_audit_log(result)
        return result

    def _write_audit_log(self, result: dict[str, Any]) -> None:
        try:
            entry = {
                "timestamp": result["timestamp"],
                "input_summary": result["input_summary"],
                "routing_mode": result.get("routing_mode", "unknown"),
                "primary_id": result["primary_agent"]["id"],
                "primary_name": result["primary_agent"]["name"],
                "primary_layer": result["primary_agent"]["layer"],
                "routing_advice": result["routing_advice"],
                "dna": result["dna"],
            }
            with self.audit_log_path.open("a", encoding="utf-8") as f:
                f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        except Exception:
            pass

    def list_agents(self, layer: str | None = None) -> list[dict[str, Any]]:
        """列出已注册智能体。"""
        if layer:
            return [a for a in self.agents if a.get("layer") == layer]
        return self.agents


# ═══════════════════════════════════════════════════════════════
# v1.3: 流场协同辅助函数（任务→五行/角色/模式推断）
# ═══════════════════════════════════════════════════════════════

def _infer_task_wuxing(text: str) -> List[Any]:
    """从任务文本推断所需五行"""
    from flowfield_collab_engine import WuxingElement  # type: ignore[import-untyped]
    wuxing_keywords = {
        WuxingElement.METAL: ["审计", "安全", "规则", "边界", "加密", "签名", "熔断", "漏洞", "合规", "裁决"],
        WuxingElement.WATER: ["记忆", "追溯", "归档", "同步", "翻译", "日志", "历史", "检索", "DNA", "索引"],
        WuxingElement.WOOD: ["创新", "构建", "编码", "设计", "架构", "扩展", "生长", "新建", "创造", "生成"],
        WuxingElement.FIRE: ["执行", "部署", "发布", "激活", "运行", "启动", "推进", "加速", "攻击", "告警"],
        WuxingElement.EARTH: ["聚合", "编排", "协调", "入口", "承载", "总控", "治理", "注册", "稳定", "锚定"],
    }
    scores = {}
    for elem, keywords in wuxing_keywords.items():
        score = sum(1 for kw in keywords if kw in text)
        scores[elem] = score
    max_score = max(scores.values()) if scores else 0
    if max_score == 0:
        return []  # 无偏好
    return [elem for elem, s in scores.items() if s >= max_score]


def _infer_task_role(text: str) -> Any:
    """从任务文本推断协同角色"""
    from flowfield_collab_engine import CollabRole  # type: ignore[import-untyped]
    role_keywords = {
        CollabRole.AUDITOR: ["审计", "检查", "漏洞", "安全", "合规"],
        CollabRole.EXECUTOR: ["执行", "部署", "运行", "发布", "构建"],
        CollabRole.STRATEGIST: ["设计", "架构", "规划", "战略", "方案"],
        CollabRole.MEMORIZER: ["记录", "归档", "备份", "日志", "索引"],
        CollabRole.GUARDIAN: ["守护", "防御", "保护", "监控", "报警"],
        CollabRole.COMMANDER: ["总控", "编排", "协调", "决策", "指挥"],
        CollabRole.BRIDGE: ["同步", "对接", "集成", "桥接", "翻译"],
        CollabRole.OBSERVER: ["观察", "分析", "调研", "评估", "扫描"],
    }
    best_role = None
    best_score = 0
    for role, keywords in role_keywords.items():
        score = sum(1 for kw in keywords if kw in text)
        if score > best_score:
            best_score = score
            best_role = role
    return best_role


def _infer_collab_mode(text: str) -> Any:
    """从任务文本推断协同模式"""
    from flowfield_collab_engine import CollabMode  # type: ignore[import-untyped]
    if any(kw in text for kw in ["并行", "同时", "分头", "各自", "多线"]):
        return CollabMode.PARALLEL
    if any(kw in text for kw in ["流水线", "串行", "先后", "传递", "接力"]):
        return CollabMode.PIPELINE
    if any(kw in text for kw in ["共识", "投票", "表决", "一致", "全体"]):
        return CollabMode.CONSENSUS
    if any(kw in text for kw in ["委派", "指派", "授权", "代理", "代表"]):
        return CollabMode.DELEGATION
    if any(kw in text for kw in ["监察", "监督", "审核", "双人", "复核"]):
        return CollabMode.WATCHDOG
    return CollabMode.PARALLEL  # 默认并行


def main():
    orchestrator = AgentOrchestrator()
    print(f"龍魂智能体编排器 {VERSION} 已启动")
    print(f"已注册 {len(orchestrator.agents)} 个智能体")
    print(f"DNA: {DNA_SIGNATURE}")
    print("输入文本进行路由，输入 'q' 退出")
    print("命令: list | skill <id> | run <id> [args] | daemon-status | start-daemon | stop-daemon | report | eco-status | eco-route <文本> | neural-status | neural-route <文本>\n")

    while True:
        try:
            text = input(">>> ")
        except (EOFError, KeyboardInterrupt):
            break
        cmd = text.strip().lower()
        if cmd in ("q", "quit", "exit"):
            break
        if cmd == "list":
            for a in orchestrator.list_agents():
                print(f"[{a['layer']}] {a['id']:20} {a['name']:10} {a['logic']}")
            print()
            continue
        if cmd.startswith("skill "):
            sid = text[len("skill "):].strip()
            print(json.dumps(orchestrator.show_skill(sid), ensure_ascii=False, indent=2))
            print()
            continue
        if cmd.startswith("run "):
            parts = text[len("run "):].strip().split()
            if not parts:
                print("用法: run <id> [args...]")
                print()
                continue
            sid, args = parts[0], parts[1:]
            print(json.dumps(orchestrator.run_skill(sid, args), ensure_ascii=False, indent=2))
            print()
            continue
        if cmd == "daemon-status":
            print(json.dumps(orchestrator.daemon_status(), ensure_ascii=False, indent=2))
            print()
            continue
        if cmd == "start-daemon":
            _start_daemon()
            print()
            continue
        if cmd == "stop-daemon":
            _stop_daemon()
            print()
            continue
        if cmd == "report":
            _report_tuple = _generate_report()
            report = _report_tuple[0]  # pyright: ignore[reportArgumentType]
            _json_path = _report_tuple[1]  # pyright: ignore[reportArgumentType]
            md_path = _report_tuple[2]  # pyright: ignore[reportArgumentType]
            sc = report["sancai"]
            print(f"三才审计报告已生成：{md_path}")
            print(f"综合评分: {sc['overall']:.3f} | dr={sc['digital_root']} | {sc['color']}")
            print()
            continue
        if cmd == "eco-status":
            print(json.dumps(orchestrator.eco_status(), ensure_ascii=False, indent=2))
            print()
            continue
        if cmd == "neural-status":
            if _neural_bridge is not None:
                pano = _neural_bridge.health_panorama()
                print(json.dumps(pano, ensure_ascii=False, indent=2))
            else:
                print("神经网络桥接器未加载（需要 cnsh-core/neural_agent_bridge.py）")
            print()
            continue
        if cmd.startswith("neural-route "):
            query = text[len("neural-route "):].strip()
            if _neural_bridge is not None:
                print(json.dumps(_neural_bridge.execute(query), ensure_ascii=False, indent=2))
            else:
                print("神经网络桥接器未加载")
            print()
            continue
        if cmd.startswith("eco-route "):
            query = text[len("eco-route "):].strip()
            if _agent_eco is not None:
                print(json.dumps(_eco_route(query), ensure_ascii=False, indent=2))  # pyright: ignore[reportOptionalCall]
            else:
                print("agent-eco 适配器未加载")
            print()
            continue

        result = orchestrator.route(text)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        print()


if __name__ == "__main__":
    main()
