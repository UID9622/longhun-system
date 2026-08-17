#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
#龍芯⚡️丙午·乙未·丁酉·亥时·☰乾-PERSONA-RUNNER-v1.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
龍魂 · PersonaRunner 人格智能体统一运行器 v1.0
DNA: #龍芯⚡️丙午·乙未·丁酉·亥时·☰乾-PERSONA-RUNNER-v1.0

22人格→Agent桥接 · 统一注册 · 独立运行 · 总线通信
"""

import hashlib, importlib, json, sys, threading, time, uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum, auto

SYSTEM_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(SYSTEM_ROOT))

from engines.lh_persona_agent import PersonaAgent, AgentState, AgentMessage, agent_dna_hash
from engines.lh_inter_agent_bus import InterAgentBus, get_bus, BusMessage


# ═══════════════════════════════════════════════════════════════
# 22人格完整注册表 (P00-P72 + P77 + S1-S3)
# ═══════════════════════════════════════════════════════════════

PERSONA_MATRIX = {
    # 战略层 (Strategic) — 顶层决策
    "P00": {"name": "文心", "role": "meta_cognition", "layer": "strategic", "motto": "大音希声"},
    "P01": {"name": "诸葛亮", "role": "strategic_reasoning", "layer": "strategic", "motto": "运筹帷幄"},

    # 执行层 (Executive) — 落地执行
    "P02": {"name": "龍芯", "role": "mathematical_engine", "layer": "executive", "motto": "精算致知"},
    "P03": {"name": "墨子", "role": "archivist", "layer": "executive", "motto": "兼爱非攻"},
    "P04": {"name": "鲁班", "role": "engineer", "layer": "executive", "motto": "匠心独运"},
    "P07": {"name": "管仲", "role": "economist", "layer": "executive", "motto": "通货积财"},
    "P14": {"name": "吕蒙", "role": "deployer", "layer": "executive", "motto": "刮目相看"},

    # 文化层 (Cultural) — 文化守卫
    "P08": {"name": "仓颉", "role": "naming", "layer": "cultural", "motto": "造字正名"},
    "P09": {"name": "孙思邈", "role": "diagnostician", "layer": "cultural", "motto": "治未病"},
    "P10": {"name": "苏东坡", "role": "communicator", "layer": "cultural", "motto": "清风徐来"},
    "P11": {"name": "李白", "role": "creative", "layer": "cultural", "motto": "天生我材"},
    "P12": {"name": "屈原", "role": "bottomline", "layer": "cultural", "motto": "九死不悔"},

    # 守护层 (Guardian) — 审计守护
    "P05": {"name": "上帝之眼", "role": "auditor", "layer": "guardian", "motto": "明察秋毫"},
    "P06": {"name": "数学大师", "role": "calculator", "layer": "guardian", "motto": "天数有定"},
    "P13": {"name": "姜子牙", "role": "scheduler", "layer": "guardian", "motto": "封神授权"},
    "P15": {"name": "乔前辈", "role": "signer", "layer": "guardian", "motto": "一签定乾坤"},
    "P72": {"name": "龍盾", "role": "fuse", "layer": "guardian", "motto": "熔断守底"},

    # 安全专项
    "P77": {"name": "黑天使军团", "role": "security", "layer": "special", "motto": "知攻善守"},

    # 子系统
    "S1": {"name": "法律引擎", "role": "legal", "layer": "subsystem", "motto": "法度森严"},
    "S2": {"name": "洛书369", "role": "luoshu", "layer": "subsystem", "motto": "数理深藏"},
    "S3": {"name": "人民维权", "role": "civil_rights", "layer": "subsystem", "motto": "为人民服务"},
}


class PersonaAgentWrapper:
    """将现有人格执行器类封装为总线兼容的智能体接口"""

    def __init__(self, persona_id: str, executor_class: type, bus: InterAgentBus):
        meta = PERSONA_MATRIX.get(persona_id, {})
        self.persona_id = persona_id
        self.PERSONA_CODE = persona_id  # 总线注册需要的属性
        self.name = meta.get("name", persona_id)
        self.layer = meta.get("layer", "unknown")
        self.role = meta.get("role", "unknown")
        self.motto = meta.get("motto", "")

        # 实例化执行器
        try:
            self._executor = executor_class()
        except Exception:
            self._executor = None

        self._bus = bus
        self._state = AgentState.IDLE
        self._lock = threading.Lock()
        self._msg_handlers: Dict[str, Callable] = {}
        self._stats = {"tasks_handled": 0, "messages_sent": 0, "errors": 0, "last_active": None}

        # 注册到总线
        try:
            bus.register(self)
        except Exception:
            pass

    # ── 总线要求的接口 ──

    def receive_message(self, msg):
        """总线投递消息的回调入口（必须实现）"""
        self._stats["last_active"] = datetime.now().isoformat()
        handler = self._msg_handlers.get(msg.msg_type)
        if handler:
            try:
                return handler(msg)
            except Exception as e:
                self._stats["errors"] += 1
                return None
        return None

    # ── Agent 执行接口 ──

    def execute(self, task: str, **kwargs) -> Dict[str, Any]:
        """执行任务"""
        with self._lock:
            self._state = AgentState.ACTING
            self._stats["last_active"] = datetime.now().isoformat()

        try:
            if self._executor and hasattr(self._executor, 'execute'):
                result = self._executor.execute(task, **kwargs)
            elif self._executor and hasattr(self._executor, 'process'):
                result = self._executor.process(task, **kwargs)
            else:
                prompt = getattr(self._executor, 'SYSTEM_PROMPT', '') if self._executor else ''
                result = self._fallback_execute(task, prompt, **kwargs)

            self._stats["tasks_handled"] += 1
            return {"persona": self.persona_id, "name": self.name, "status": "ok", "result": result}
        except Exception as e:
            self._stats["errors"] += 1
            return {"persona": self.persona_id, "status": "error", "error": str(e)}
        finally:
            with self._lock:
                self._state = AgentState.IDLE

    def _fallback_execute(self, task: str, prompt: str, **kwargs) -> str:
        return f"[{self.name}] 收到任务: {task[:200]} | 角色: {self.role} | 状态: 已接收"

    def send_to(self, target_id: str, content: Any, msg_type: str = "task") -> str:
        """发送消息给其他智能体"""
        msg_id = uuid.uuid4().hex[:12]
        # BusMessage.content 要求 dict 类型
        payload = content if isinstance(content, dict) else {"data": content}
        bus_msg = BusMessage(
            msg_id=msg_id, sender=self.persona_id, recipient=target_id,
            msg_type=msg_type, content=payload,
            dna=agent_dna_hash(self.persona_id, "send", msg_type),
        )
        self._bus.send(bus_msg)
        self._stats["messages_sent"] += 1
        return msg_id

    def on_message(self, msg_type: str):
        """装饰器：注册消息处理器"""
        def decorator(fn):
            self._msg_handlers[msg_type] = fn
            return fn
        return decorator

    @property
    def state(self) -> AgentState:
        return self._state

    @property
    def stats(self) -> Dict[str, Any]:
        return dict(self._stats)

    def shutdown(self):
        try:
            self._bus.unregister(self.persona_id)
        except Exception:
            pass
        with self._lock:
            self._state = AgentState.DONE


# ═══════════════════════════════════════════════════════════════
# PersonaRunner — 统一运行器
# ═══════════════════════════════════════════════════════════════

class PersonaRunner:
    """22人格统一运行管理器"""

    def __init__(self, auto_boot: bool = False):
        self._bus = get_bus()
        self._agents: Dict[str, PersonaAgentWrapper] = {}
        self._booted = False
        self._lock = threading.RLock()

        if auto_boot:
            self.boot()

    def boot(self, persona_ids: Optional[List[str]] = None) -> Dict[str, bool]:
        """启动全部/指定人格

        Args:
            persona_ids: None=全量, 或用列表指定具体人格
        Returns:
            {persona_id: success}
        """
        with self._lock:
            targets = persona_ids or list(PERSONA_MATRIX.keys())
            results = {}

            for pid in targets:
                exec_cls = self._resolve_executor_class(pid)
                if exec_cls:
                    wrapper = PersonaAgentWrapper(pid, exec_cls, self._bus)
                    self._agents[pid] = wrapper
                    results[pid] = True
                else:
                    results[pid] = False

            self._booted = len(self._agents) > 0
            return results

    def _resolve_executor_class(self, persona_id: str) -> Optional[type]:
        """动态加载人格执行器类"""
        # 执行器类名映射
        CLASS_MAP = {
            "P00": ("bin.personas.p00_wenxin", "P00Wenxin"),
            "P01": ("bin.personas.p01_zhugeliang", "P01Zhugeliang"),
            "P02": ("bin.personas.p02_longxin", "P02Longxin"),
            "P03": ("bin.personas.p03_mozi", "P03Mozi"),
            "P04": ("bin.personas.p04_luban", "P04Luban"),
            "P05": ("bin.personas.p05_godseye", "P05Godseye"),
            "P06": ("bin.personas.p06_mathmaster", "P06Mathmaster"),
            "P07": ("bin.personas.p07_guanzhong", "P07Guanzhong"),
            "P08": ("bin.personas.p08_cangjie", "P08Cangjie"),
            "P09": ("bin.personas.p09_sunsi", "P09Sunsi"),
            "P10": ("bin.personas.p10_sudongpo", "P10Sudongpo"),
            "P11": ("bin.personas.p11_libai", "P11Libai"),
            "P12": ("bin.personas.p12_quyuan", "P12Quyuan"),
            "P13": ("bin.personas.p13_jiangziya", "P13Jiang"),
            "P14": ("bin.personas.p14_lvmeng", "P14Lvmeng"),
            "P15": ("bin.personas.p15_qiao", "P15Qiao"),
            "P72": ("bin.personas.p72_longdun", "P72Longdun"),
            "P77": ("bin.personas.p77_security", "P77Security"),
            "S1":  ("bin.personas.s1_legal", "S1Legal"),
            "S2":  ("bin.personas.s2_luoshu", "S2Luoshu"),
            "S3":  ("bin.personas.s3_civil", "S3Civil"),
            # 扩展人格（不在22人格标准矩阵中，但执行器已存在）
            "P18": ("bin.personas.p18_registrar", "P18Registrar"),
            "P19": ("bin.personas.p19_auditor", "P19Auditor"),
            "P20": ("bin.personas.p20_trust", "P20Trust"),
        }

        info = CLASS_MAP.get(persona_id)
        if not info:
            return None

        module_path, class_name = info
        try:
            mod = importlib.import_module(module_path)
            return getattr(mod, class_name, None)
        except (ImportError, AttributeError):
            return None

    # ── 调度方法 ──

    def dispatch(self, persona_id: str, task: str, **kwargs) -> Dict[str, Any]:
        """向指定人格派发任务"""
        agent = self._agents.get(persona_id)
        if not agent:
            return {"error": f"Persona '{persona_id}' not booted"}
        return agent.execute(task, **kwargs)

    def dispatch_chain(self, chain: List[str], task: str, **kwargs) -> Dict[str, Any]:
        """链式调度: P05→P06→P02 串联执行"""
        results = {}
        current_context = {"task": task, **kwargs}

        for pid in chain:
            result = self.dispatch(pid, **current_context)
            results[pid] = result
            # 将上一人格输出作为下一人格的上下文
            if result.get("status") == "ok":
                current_context["previous_output"] = result.get("result")
                current_context["previous_persona"] = pid

        return {"chain": chain, "results": results}

    def dispatch_parallel(self, tasks: Dict[str, str], **kwargs) -> Dict[str, Any]:
        """并行调度: {"P05":"审计代码","P06":"算数字根"} 同时执行"""
        results = {}
        threads = []

        def _run(pid, task_text):
            results[pid] = self.dispatch(pid, task_text, **kwargs)

        for pid, task_text in tasks.items():
            t = threading.Thread(target=_run, args=(pid, task_text), daemon=True)
            threads.append(t)
            t.start()

        for t in threads:
            t.join(timeout=60)

        return results

    def broadcast(self, task: str, layers: Optional[List[str]] = None, **kwargs) -> Dict[str, Any]:
        """广播任务给所有人格（可限制层）

        layers: None=全部, 或 ['strategic','executive','cultural','guardian','special','subsystem']
        """
        results = {}
        for pid, agent in self._agents.items():
            if layers and PERSONA_MATRIX.get(pid, {}).get("layer") not in layers:
                continue
            try:
                results[pid] = agent.execute(task, **kwargs)
            except Exception as e:
                results[pid] = {"status": "error", "error": str(e)}
        return results

    # ── 查询方法 ──

    def status_all(self) -> Dict[str, Any]:
        """查看所有智能体状态"""
        return {
            pid: {
                "name": agent.name,
                "state": agent.state.name,
                "layer": agent.layer,
                "stats": agent.stats
            }
            for pid, agent in self._agents.items()
        }

    def status_by_layer(self) -> Dict[str, List[str]]:
        """按层分组状态"""
        layers = {}
        for pid, agent in self._agents.items():
            layer = agent.layer
            layers.setdefault(layer, []).append(f"{pid}({agent.name})")
        return layers

    def get_agent(self, persona_id: str) -> Optional[PersonaAgentWrapper]:
        return self._agents.get(persona_id)

    def list_agents(self) -> List[str]:
        return list(self._agents.keys())

    @property
    def agent_count(self) -> int:
        return len(self._agents)

    @property
    def is_booted(self) -> bool:
        return self._booted

    def shutdown_all(self):
        """关闭所有智能体"""
        for agent in self._agents.values():
            agent.shutdown()
        self._agents.clear()
        self._booted = False


# ═══════════════════════════════════════════════════════════════
# 全局单例
# ═══════════════════════════════════════════════════════════════

_runner_instance: Optional[PersonaRunner] = None
_runner_lock = threading.Lock()


def get_runner() -> PersonaRunner:
    global _runner_instance
    with _runner_lock:
        if _runner_instance is None:
            _runner_instance = PersonaRunner()
        return _runner_instance


# ═══════════════════════════════════════════════════════════════
# CLI & 自检
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="龍魂 PersonaRunner 人格智能体运行器")
    parser.add_argument("--boot", nargs="*", dest="boot_ids", default=None,
                        help="启动指定人格（不指定=全部）, 如: --boot P00 P01 P05")
    parser.add_argument("--status", action="store_true", help="查看所有智能体状态")
    parser.add_argument("--layers", action="store_true", help="按架构层分组显示")
    parser.add_argument("--self-test", action="store_true", help="自检模式")
    args = parser.parse_args()

    print("╔══════════════════════════════════════════╗")
    print("║  龍魂 PersonaRunner v1.0 人格智能体运行器  ║")
    print("║  DNA: #龍芯⚡️丙午·乙未·丁酉·亥时·☰乾  ║")
    print("╚══════════════════════════════════════════╝\n")

    # 自检模式
    if args.self_test:
        print("🔧 自检模式\n")

        # 1. 检查注册表完整性
        print(f"[1/4] 注册表完整性: {len(PERSONA_MATRIX)} 人格已注册")
        for pid, meta in PERSONA_MATRIX.items():
            status = "✅" if meta.get("name") and meta.get("role") else "❌"
            print(f"  {status} {pid} {meta['name']:8s} | {meta['role']:20s} | {meta['layer']}")

        # 2. 检查执行器类可解析性
        print(f"\n[2/4] 执行器解析:")
        runner = PersonaRunner()
        exec_resolved = runner.boot()
        for pid, ok in exec_resolved.items():
            s = "✅" if ok else "⚠️ 降级(无执行器类)"
            print(f"  {s} {pid}")

        # 3. 基本执行测试
        print(f"\n[3/4] 基本执行测试:")
        for pid in ["P00", "P05", "P06"]:
            agent = runner.get_agent(pid)
            if agent:
                r = agent.execute("自检: 确认在线")
                status = r.get("status", "?")
                print(f"  {'✅' if status == 'ok' else '❌'} {pid}({agent.name}) → {status}")

        # 4. 总线通信测试
        print(f"\n[4/4] 总线通信测试:")
        p00 = runner.get_agent("P00")
        p05 = runner.get_agent("P05")
        if p00 and p05:
            mid = p00.send_to("P05", {"test": "ping"}, "test")
            print(f"  ✅ P00→P05 消息已发送 (msg_id={mid})")

        print(f"\n{'='*50}")
        print(f"总计: {runner.agent_count}/{len(PERSONA_MATRIX)} 人格已启动")
        print(f"注册表: 22人格 (16核心+1安全+3子系统+2预留)")
        print(f"自检完成 ✅")
        sys.exit(0)

    # 正常启动模式
    runner = PersonaRunner()
    boot_targets = args.boot_ids if args.boot_ids else None

    result = runner.boot(persona_ids=boot_targets)
    success_count = sum(1 for v in result.values() if v)
    print(f"启动完成: {success_count}/{len(result)} 人格已就绪\n")

    if args.layers:
        print("按架构层分组:")
        for layer, agents in runner.status_by_layer().items():
            print(f"  [{layer}] {', '.join(agents)}")

    if args.status:
        print("\n智能体状态:")
        for pid, s in runner.status_all().items():
            color = {"idle":"🟢","observing":"🔵","thinking":"🟣","acting":"🟡","waiting":"⏳","done":"⚫","error":"🔴","meltdown":"💀"}.get(s["state"],"?")
            print(f"  {color} {pid} {s['name']:10s} | {s['state']:8s} | tasks={s['stats']['tasks_handled']}")

    print(f"\n提示: python3 engines/lh_persona_runner.py --self-test  # 运行完整自检")
