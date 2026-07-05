#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂智能体编排器 v1.1

- 读取 manifest.json 中的智能体注册表
- 根据输入文本关键词匹配最合适的智能体/人格
- 支持 L1 常驻、L2 按需、L3 人格三层模型
- 已缠尾：全部 176 个智能体/技能接入编排
- 100% 本地运行，纯标准库

DNA: #龍芯⚡️2026-06-26-AGENT-ORCHESTRATOR-v1.1
"""

import json
import re
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from agent_daemon import start_daemon as _start_daemon, stop_daemon as _stop_daemon
from agent_status_reporter import generate_report as _generate_report


SCRIPT_DIR = Path(__file__).resolve().parent
MANIFEST_PATH = SCRIPT_DIR / "manifest.json"
DNA_SIGNATURE = "#龍芯⚡️2026-06-26-AGENT-ORCHESTRATOR-v1.1"
VERSION = "v1.1"

# 可选：接入 longhun-empower-engine 进行语义路由兜底
_EMPOWER_ENGINE = None
_EMPOWER_PATH = Path.home() / ".kimi-code" / "skills" / "longhun-empower-engine" / "scripts"
if _EMPOWER_PATH.exists():
    try:
        sys.path.insert(0, str(_EMPOWER_PATH))
        from empower_engine_v2 import EmpowerEngine  # type: ignore

        _EMPOWER_ENGINE = EmpowerEngine()
    except Exception:
        _EMPOWER_ENGINE = None

# 可选：接入 longhun-agent-eco 动态调度
_AGENT_ECO = None
try:
    from agent_eco_adapter import (
        eco_route as _eco_route,
        eco_status as _eco_status,
        eco_list as _eco_list,
    )

    _AGENT_ECO = True
except Exception:
    _AGENT_ECO = None


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

    def _load_manifest(self) -> Dict[str, Any]:
        with self.manifest_path.open("r", encoding="utf-8") as f:
            return json.load(f)

    @staticmethod
    def _preprocess(text: str) -> str:
        text = str(text).strip().lower()
        text = re.sub(r"[\s\u3000]+", " ", text)
        return text[:5000]

    def route(self, text: str) -> Dict[str, Any]:
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
        if _EMPOWER_ENGINE is not None:
            try:
                empower_result = _EMPOWER_ENGINE.identify(cleaned)
                return self._build_from_empower(cleaned, empower_result, start)
            except Exception:
                pass

        # 若 empower-engine 也未命中，调用 longhun-agent-eco v2 路由引擎
        if _AGENT_ECO is not None:
            try:
                eco_result = _eco_route(cleaned)
                if eco_result.get("狀態") == "success":
                    return self._build_from_eco(cleaned, eco_result, start)
            except Exception:
                pass

        return self._fallback(cleaned, "未匹配到智能体")

    def _match_agents(self, text: str) -> List[Dict[str, Any]]:
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
        matches: List[Dict[str, Any]],
        start: float,
    ) -> Dict[str, Any]:
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
        empower_result: Dict[str, Any],
        start: float,
    ) -> Dict[str, Any]:
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
        eco_result: Dict[str, Any],
        start: float,
    ) -> Dict[str, Any]:
        """当关键词与 empower-engine 均未命中时，由 agent-eco v2 路由引擎调度。"""
        matched_ids = eco_result.get("匹配智能體", [])
        tag = eco_result.get("匹配標籤", "")
        matched_keywords = eco_result.get("匹配關鍵詞", [])

        # 把 AGENT-XXX 解析为可读名称
        name_map = {}
        if _AGENT_ECO is not None:
            try:
                for a in _eco_list():
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

    def daemon_status(self) -> Dict[str, Any]:
        """读取 L1 守护进程状态文件。"""
        from agent_daemon import _read_pid, _is_alive, read_json
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

    def eco_status(self) -> Dict[str, Any]:
        """获取 agent-eco 生态系统状态。"""
        if _AGENT_ECO is None:
            return {"available": False, "error": "agent-eco 适配器未加载"}
        return {"available": True, "data": _eco_status()}

    def show_skill(self, skill_id: str) -> Dict[str, Any]:
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

    def run_skill(self, skill_id: str, args: List[str]) -> Dict[str, Any]:
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

    def _routing_advice(self, primary: Dict[str, Any], secondary: Optional[Dict[str, Any]]) -> str:
        name = primary["name"]
        logic = primary["logic"]
        layer = primary["layer"]

        base = f"由 {layer} 智能体「{name}」主理，执行{logic}"
        if secondary:
            base += f"；「{secondary['name']}」({secondary['logic']}) 辅助"
        return base

    def _fallback(self, cleaned: str, reason: str) -> Dict[str, Any]:
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

    def _write_audit_log(self, result: Dict[str, Any]) -> None:
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

    def list_agents(self, layer: Optional[str] = None) -> List[Dict[str, Any]]:
        """列出已注册智能体。"""
        if layer:
            return [a for a in self.agents if a.get("layer") == layer]
        return self.agents


def main():
    orchestrator = AgentOrchestrator()
    print(f"龍魂智能体编排器 {VERSION} 已启动")
    print(f"已注册 {len(orchestrator.agents)} 个智能体")
    print(f"DNA: {DNA_SIGNATURE}")
    print("输入文本进行路由，输入 'q' 退出")
    print("命令: list | skill <id> | run <id> [args] | daemon-status | start-daemon | stop-daemon | report | eco-status | eco-route <文本>\n")

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
            report, json_path, md_path = _generate_report()
            sc = report["sancai"]
            print(f"三才审计报告已生成：{md_path}")
            print(f"综合评分: {sc['overall']:.3f} | dr={sc['digital_root']} | {sc['color']}")
            print()
            continue
        if cmd == "eco-status":
            print(json.dumps(orchestrator.eco_status(), ensure_ascii=False, indent=2))
            print()
            continue
        if cmd.startswith("eco-route "):
            query = text[len("eco-route "):].strip()
            if _AGENT_ECO is not None:
                print(json.dumps(_eco_route(query), ensure_ascii=False, indent=2))
            else:
                print("agent-eco 适配器未加载")
            print()
            continue

        result = orchestrator.route(text)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        print()


if __name__ == "__main__":
    main()
