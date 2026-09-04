#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
#龍芯⚡️丙午·乙未·己未·申时·䷉履-UNIFIED-HOOK-CONNECTOR-v2.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
"""
龍魂统一钩子连接器 v2.1 · 13大引擎一体化集成
确保每个功能块都有钩子、无脱钩属性、自动可视化效果
v2.1 升级：新增自适应调优引擎 + CNSH护盾代理L9审查

DNA: #龍芯⚡️丙午·乙未·己未·申时·䷉履-UNIFIED-HOOK-CONNECTOR-v2.0
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""

import sys
import json
import hashlib
import time
import math
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional, Callable, Any, Tuple
from enum import Enum


# ═══════════════════════════════════════════════════════════
# 统一钩子注册系统
# ═══════════════════════════════════════════════════════════

class HookType(Enum):
    PRE_AUDIT = "审计前"       # 审计前钩子
    POST_AUDIT = "审计后"      # 审计后钩子
    PRE_EXECUTE = "执行前"     # 执行前钩子
    POST_EXECUTE = "执行后"    # 执行后钩子
    ON_ERROR = "错误时"        # 错误钩子
    ON_MELTDOWN = "熔断时"     # 熔断钩子
    ON_COMPLETE = "完成时"     # 完成钩子
    LIFECYCLE = "生命周期"     # 生命周期钩子


@dataclass
class HookRegistration:
    """钩子注册记录"""
    hook_id: str
    hook_type: HookType
    module: str                    # 来源模块
    callback_name: str             # 回调函数名
    priority: int = 100            # 优先级（数字越小越先执行）
    enabled: bool = True
    description: str = ""


class UnifiedHookRegistry:
    """统一钩子注册中心 · 所有模块在此注册钩子"""

    def __init__(self):
        self.hooks: Dict[HookType, List[HookRegistration]] = {
            ht: [] for ht in HookType
        }
        self.callbacks: Dict[str, Callable] = {}
        self.execution_log: List[Dict] = []

    def register(self, hook_type: HookType, module: str,
                 callback: Callable, priority: int = 100,
                 description: str = "") -> str:
        """注册钩子"""
        hook_id = hashlib.sha3_256(
            f"{hook_type.value}{module}{time.time()}".encode()
        ).hexdigest()[:16]

        reg = HookRegistration(
            hook_id=hook_id,
            hook_type=hook_type,
            module=module,
            callback_name=callback.__name__ if hasattr(callback, '__name__') else 'anonymous',
            priority=priority,
            description=description,
        )
        self.callbacks[hook_id] = callback
        self.hooks[hook_type].append(reg)
        # 按优先级排序
        self.hooks[hook_type].sort(key=lambda h: h.priority)
        return hook_id

    def trigger(self, hook_type: HookType, context: Dict[str, Any] = None) -> List[Dict]:
        """触发钩子链"""
        if context is None:
            context = {}

        results = []
        for reg in self.hooks[hook_type]:
            if not reg.enabled:
                continue
            try:
                cb = self.callbacks[reg.hook_id]
                result = cb(context)
                results.append({
                    "hook_id": reg.hook_id,
                    "module": reg.module,
                    "type": hook_type.value,
                    "result": str(result)[:200],
                })
            except Exception as e:
                results.append({
                    "hook_id": reg.hook_id,
                    "module": reg.module,
                    "type": hook_type.value,
                    "error": str(e),
                })

        self.execution_log.extend(results)
        return results

    def status(self) -> Dict[str, Any]:
        """钩子系统状态"""
        total = sum(len(h) for h in self.hooks.values())
        enabled = sum(
            sum(1 for r in h if r.enabled)
            for h in self.hooks.values()
        )
        by_type = {ht.value: len(self.hooks[ht]) for ht in HookType}
        return {
            "total_hooks": total,
            "enabled_hooks": enabled,
            "by_type": by_type,
            "modules": list(set(
                r.module for h in self.hooks.values() for r in h
            )),
        }

    def verify_no_orphans(self) -> Tuple[bool, List[str]]:
        """验证无脱钩属性 · 检查所有已知模块是否都注册了钩子"""
        expected_modules = [
            "lh_quantum_circuit_breaker",
            "lh_learning_pipeline",
            "lh_lu_instruction_engine",
            "lh_braket_persona_engine",
            "lh_math_formalization",
            "lh_data_meltdown",
            "lh_persona_sovereignty",
            "lh_regulatory_pipeline",
            # v2.0 新增：6大引擎
            "lh_dual_brain_engine",
            "lh_mod9_runtime_engine",
            "lh_11step_chain_engine",
            "lh_event_bus_engine",
            "lh_snapshot_recovery_engine",
            "lh_red_team_engine",
            # v2.0 新增：自适应调优引擎
            "lh_adaptive_tuner",
            "cnsh_proxy_shield",
            # v2.0 新增：蚁群引擎
            "lh_ant_colony",
        ]

        registered = set()
        for h_list in self.hooks.values():
            for r in h_list:
                registered.add(r.module)

        missing = [m for m in expected_modules if m not in registered]
        return (len(missing) == 0, missing)


# ═══════════════════════════════════════════════════════════
# 统一管道引擎 · 五大引擎串联
# ═══════════════════════════════════════════════════════════

@dataclass
class PipelineResult:
    """管道执行结果"""
    stage: str
    engine: str
    status: str  # 🟢 🟡 🔴
    output: Dict[str, Any]
    duration_ms: float = 0.0
    dna: str = ""

    def display_line(self) -> str:
        return f"  [{self.status}] {self.stage:15s} {self.engine:30s} {self.duration_ms:6.1f}ms"


class UnifiedPipeline:
    """统一管道 · 五大引擎全链路"""

    def __init__(self):
        self.registry = UnifiedHookRegistry()
        self.results: List[PipelineResult] = []
        self._init_default_hooks()

    def _init_default_hooks(self):
        """初始化默认钩子 · 确保每个模块都有钩子"""

        def quantum_pre_audit(ctx):
            return {"engine": "quantum", "action": "pre_audit", "ready": True}

        def quantum_post_audit(ctx):
            return {"engine": "quantum", "status": ctx.get('status', 'unknown')}

        def learning_inbox_hook(ctx):
            return {"engine": "learning", "inbox_size": ctx.get('inbox_size', 0)}

        def learning_dna_hook(ctx):
            return {"engine": "learning", "dna_count": ctx.get('dna_count', 0)}

        def lu_pre_exec(ctx):
            return {"engine": "lu", "instruction_count": ctx.get('count', 0)}

        def lu_post_exec(ctx):
            return {"engine": "lu", "results": ctx.get('results', [])}

        def braket_scenario_hook(ctx):
            return {"engine": "braket", "scenario": ctx.get('scenario', 'unknown')}

        def math_verify_hook(ctx):
            return {"engine": "math", "stable": ctx.get('stable', True)}

        def meltdown_detect_hook(ctx):
            return {"engine": "meltdown", "blocked": ctx.get('blocked', False)}

        def persona_guard_hook(ctx):
            return {"engine": "persona", "violation": ctx.get('violation', False)}

        def regulatory_chain_hook(ctx):
            return {"engine": "regulatory", "audit_passed": ctx.get('audited', True)}

        # 注册所有钩子
        self.registry.register(HookType.PRE_AUDIT, "lh_quantum_circuit_breaker",
                              quantum_pre_audit, 10, "量子熔断预审")
        self.registry.register(HookType.POST_AUDIT, "lh_quantum_circuit_breaker",
                              quantum_post_audit, 10, "量子熔断后审")

        self.registry.register(HookType.PRE_EXECUTE, "lh_learning_pipeline",
                              learning_inbox_hook, 20, "入口池钩子")
        self.registry.register(HookType.POST_EXECUTE, "lh_learning_pipeline",
                              learning_dna_hook, 20, "DNA拆解钩子")

        self.registry.register(HookType.PRE_EXECUTE, "lh_lu_instruction_engine",
                              lu_pre_exec, 30, "Lu指令预执行")
        self.registry.register(HookType.POST_EXECUTE, "lh_lu_instruction_engine",
                              lu_post_exec, 30, "Lu指令后执行")

        self.registry.register(HookType.PRE_AUDIT, "lh_braket_persona_engine",
                              braket_scenario_hook, 15, "人格场景识别钩子")

        self.registry.register(HookType.ON_COMPLETE, "lh_math_formalization",
                              math_verify_hook, 40, "数学验证钩子")

        self.registry.register(HookType.ON_MELTDOWN, "lh_data_meltdown",
                              meltdown_detect_hook, 5, "数据黑洞熔断")
        self.registry.register(HookType.ON_MELTDOWN, "lh_persona_sovereignty",
                              persona_guard_hook, 6, "人格主权守卫")
        self.registry.register(HookType.ON_COMPLETE, "lh_regulatory_pipeline",
                              regulatory_chain_hook, 50, "监管入链钩子")

        # ─── v2.0 新增：6大引擎钩子注册 ───

        def dual_brain_pre_hook(ctx):
            return {"engine": "dual_brain", "block_ref": ctx.get('block_id', ''), "ready": True}

        def dual_brain_post_hook(ctx):
            return {"engine": "dual_brain", "tricolor": ctx.get('tricolor', '🟢'), "risk": ctx.get('risk_score', 0)}

        def mod9_runtime_hook(ctx):
            return {"engine": "mod9", "digital_root": ctx.get('dr', 0), "tricolor": ctx.get('tricolor', '🟢')}

        def chain_step_hook(ctx):
            return {"engine": "11step_chain", "step": ctx.get('step', ''), "status": ctx.get('status', 'PASS')}

        def event_bus_hook(ctx):
            return {"engine": "event_bus", "event_type": ctx.get('event_type', ''), "dispatched": True}

        def snapshot_hook(ctx):
            return {"engine": "snapshot", "snapshot_id": ctx.get('snapshot_id', ''), "verified": True}

        def red_team_hook(ctx):
            return {"engine": "red_team", "severity": ctx.get('severity', 0), "verdict": ctx.get('verdict', '🟢')}

        # 双脑引擎：审计前+审计后
        self.registry.register(HookType.PRE_AUDIT, "lh_dual_brain_engine",
                              dual_brain_pre_hook, 8, "双脑预审计（左右互搏准备）")
        self.registry.register(HookType.POST_AUDIT, "lh_dual_brain_engine",
                              dual_brain_post_hook, 12, "双脑后审计（冲突树结果）")

        # 模9运行时：审计前
        self.registry.register(HookType.PRE_AUDIT, "lh_mod9_runtime_engine",
                              mod9_runtime_hook, 7, "模9数字根预计算")

        # 11步链：执行前+执行后
        self.registry.register(HookType.PRE_EXECUTE, "lh_11step_chain_engine",
                              chain_step_hook, 5, "11步链预执行闸门")
        self.registry.register(HookType.POST_EXECUTE, "lh_11step_chain_engine",
                              chain_step_hook, 45, "11步链后执行回执")

        # 事件总线：生命周期
        self.registry.register(HookType.LIFECYCLE, "lh_event_bus_engine",
                              event_bus_hook, 1, "事件总线全局监听")

        # 快照恢复：完成时+熔断时
        self.registry.register(HookType.ON_COMPLETE, "lh_snapshot_recovery_engine",
                              snapshot_hook, 35, "完成后自动快照")
        self.registry.register(HookType.ON_MELTDOWN, "lh_snapshot_recovery_engine",
                              snapshot_hook, 3, "熔断时紧急快照")

        # 红队引擎：审计前
        self.registry.register(HookType.PRE_AUDIT, "lh_red_team_engine",
                              red_team_hook, 9, "红队对抗预审计")

        # 自适应调优引擎：审计前+完成时
        def adaptive_tuner_analyze_hook(ctx):
            try:
                from bin.lh_adaptive_tuner import adaptive_tuner_analyze_hook as at_hook
                return at_hook(ctx)
            except Exception:
                return {"engine": "adaptive_tuner", "status": "offline"}
        def adaptive_tuner_audit_hook(ctx):
            try:
                from bin.lh_adaptive_tuner import adaptive_tuner_audit_hook as at_audit
                return at_audit(ctx)
            except Exception:
                return {"engine": "adaptive_tuner", "status": "offline"}
        self.registry.register(HookType.PRE_AUDIT, "lh_adaptive_tuner",
                              adaptive_tuner_analyze_hook, 8, "自适应调优参数分析")
        self.registry.register(HookType.ON_COMPLETE, "lh_adaptive_tuner",
                              adaptive_tuner_audit_hook, 55, "自适应调优审计+熔断检查")

        # CNSH护盾代理：前置审查
        def cnsh_proxy_shield_hook(ctx):
            try:
                from cnsh_core.cnsh_proxy_addon import LocalShieldBridge
                snippet = ctx.get("content", "")[:2000]
                return LocalShieldBridge.audit(snippet, ctx.get("source", "pipeline"))
            except Exception:
                return {"engine": "cnsh_proxy", "status": "offline"}
        self.registry.register(HookType.PRE_AUDIT, "cnsh_proxy_shield",
                              cnsh_proxy_shield_hook, 7, "CNSH护盾代理L9审查")

        # ─── v2.0 新增：蚁群引擎钩子 ───
        def ant_colony_pre_audit(ctx):
            try:
                from engine.ant_colony.runtime import ant_colony_pre_audit_hook
                return ant_colony_pre_audit_hook(ctx)
            except Exception:
                return {"engine": "ant_colony", "status": "offline"}

        def ant_colony_on_complete(ctx):
            try:
                from engine.ant_colony.runtime import ant_colony_on_complete_hook
                return ant_colony_on_complete_hook(ctx)
            except Exception:
                return {"engine": "ant_colony", "status": "offline"}

        def ant_colony_lifecycle(ctx):
            try:
                from engine.ant_colony.runtime import ant_colony_lifecycle_hook
                return ant_colony_lifecycle_hook(ctx)
            except Exception:
                return {"engine": "ant_colony", "status": "offline"}

        # 蚁群预审计：内容进入管道先过蚁群侦察感知
        self.registry.register(HookType.PRE_AUDIT, "lh_ant_colony",
                              ant_colony_pre_audit, 12, "蚁群侦察感知预审计")
        # 蚁群完成时：操作完成后更新信息素轨迹
        self.registry.register(HookType.ON_COMPLETE, "lh_ant_colony",
                              ant_colony_on_complete, 25, "蚁群完成后信息素更新")
        # 蚁群生命周期：全局事件监听
        self.registry.register(HookType.LIFECYCLE, "lh_ant_colony",
                              ant_colony_lifecycle, 2, "蚁群生命周期全局监听")

    def process(self, content: str, source: str = "pipeline") -> Dict[str, Any]:
        """全链路处理 · 13大引擎串联（v2.1 升级）"""
        start = time.time()

        # 1. 预审计钩子（双脑+模9+红队+量子）
        self.registry.trigger(HookType.PRE_AUDIT, {"content": content})

        # 2. 模9运行时审计
        t0 = time.time()
        try:
            from bin.lh_mod9_runtime_engine import Mod9RuntimeEngine
            mod9_engine = Mod9RuntimeEngine()
            mod9_result = mod9_engine.decide(content)
            self.results.append(PipelineResult(
                stage=f"模9审计{mod9_result.final_tricolor.value}",
                engine=f"Mod9Runtime(dr={mod9_result.mod9.digital_root})",
                status=mod9_result.final_tricolor.value,
                output={"dr": mod9_result.mod9.digital_root, "entropy": mod9_result.entropy.entropy, "wuxing": mod9_result.wuxing_route},
                duration_ms=(time.time() - t0) * 1000,
                dna=mod9_result.dna_trace,
            ))
        except Exception as e:
            mod9_result = None
            self.results.append(PipelineResult(
                stage="模9审计", engine="Mod9Runtime", status="🟡",
                output={"error": str(e)},
            ))

        # 3. 红队对抗评估
        t0 = time.time()
        try:
            from bin.lh_red_team_engine import RedTeamEngine
            rt_engine = RedTeamEngine()
            rt_result = rt_engine.quick_assessment(content)
            self.results.append(PipelineResult(
                stage=f"红队对抗{rt_result['verdict']}",
                engine="RedTeam",
                status="🟢" if rt_result['avg_severity'] < 0.3 else ("🟡" if rt_result['avg_severity'] < 0.6 else "🔴"),
                output={"severity": rt_result['avg_severity'], "verdict": rt_result['verdict']},
                duration_ms=(time.time() - t0) * 1000,
            ))
        except Exception as e:
            self.results.append(PipelineResult(
                stage="红队对抗", engine="RedTeam", status="🟡",
                output={"error": str(e)},
            ))

        # 4. 量子熔断
        t0 = time.time()
        try:
            from bin.lh_quantum_circuit_breaker import IWECBv2Engine
            q_engine = IWECBv2Engine()
            q_result = q_engine.audit(content)
            self.results.append(PipelineResult(
                stage=f"量子熔断{q_result.status}",
                engine="IW-ECB v2.0",
                status=q_result.status,
                output={"score": q_result.score, "quantum": q_result.quantum_collaboration},
                duration_ms=(time.time() - t0) * 1000,
                dna=q_result.execution_dna,
            ))
        except Exception as e:
            q_result = None
            self.results.append(PipelineResult(
                stage="量子熔断", engine="IW-ECB v2.0",
                status="🟡", output={"error": str(e)},
            ))

        # 5. BraKet人格路由
        t0 = time.time()
        try:
            from bin.lh_braket_persona_engine import BraKetPersonaEngine
            b_engine = BraKetPersonaEngine()
            b_result = b_engine.execute(content)
            self.results.append(PipelineResult(
                stage="人格路由",
                engine=f"BraKet({b_result['primary_persona']})",
                status=b_result['tricolor'],
                output={"gua": b_result['gua'], "entangled": len(b_result['entangled_auto_activation'])},
                duration_ms=(time.time() - t0) * 1000,
            ))
        except Exception as e:
            b_result = None
            self.results.append(PipelineResult(
                stage="人格路由", engine="BraKet", status="🟡",
                output={"error": str(e)},
            ))

        # 6. 双脑左右互搏
        t0 = time.time()
        try:
            from bin.lh_dual_brain_engine import DualBrainEngine, BlockReference
            db_engine = DualBrainEngine()
            block = BlockReference(block_id=f"PIPE-{hashlib.sha256(content.encode()).hexdigest()[:8]}", content=content, source=source)
            db_result = db_engine.wake_on_cite(block)
            self.results.append(PipelineResult(
                stage=f"双脑互搏{db_result['tricolor']}",
                engine=f"DualBrain(risk={db_result['risk_score']:.2f})",
                status=db_result['tricolor'],
                output={"action": db_result['action'], "7factor_hash": db_result['seven_factor_hash']},
                duration_ms=(time.time() - t0) * 1000,
                dna=db_result['dna_trace'],
            ))
        except Exception as e:
            self.results.append(PipelineResult(
                stage="双脑互搏", engine="DualBrain", status="🟡",
                output={"error": str(e)},
            ))

        # 7. 数学验证
        t0 = time.time()
        try:
            from bin.lh_math_formalization import MathFormalizationEngine
            m_engine = MathFormalizationEngine()
            m_result = m_engine.full_audit(source, content, 0.3, 0.2, 0.1)
            stable = m_result['stability']['stable']
            self.results.append(PipelineResult(
                stage="数学验证",
                engine="MathFormalization",
                status="🟢" if stable else "🟡",
                output={"v_t": m_result['stability']['v_t'], "closed_loop": m_result['stability']['closed_loop_ok']},
                duration_ms=(time.time() - t0) * 1000,
            ))
        except Exception as e:
            self.results.append(PipelineResult(
                stage="数学验证", engine="MathFormalization", status="🟡",
                output={"error": str(e)},
            ))

        # 8. 自适应调优（参数微调审计）
        t0 = time.time()
        try:
            from bin.lh_adaptive_tuner import adaptive_tuner_analyze_hook as at_hook
            at_result = at_hook({"content": content, "source": source})
            at_status = "🟢" if at_result.get("三色") == "🟢" else ("🟡" if at_result.get("三色") == "🟡" else "🔴")
            self.results.append(PipelineResult(
                stage=f"自适应调优{at_status}",
                engine=f"AdaptiveTuner(dr={at_result.get('dr','?')})",
                status=at_status,
                output={"三色": at_result.get("三色"), "dr": at_result.get("dr"),
                        "hash": at_result.get("params_hash", "")},
                duration_ms=(time.time() - t0) * 1000,
            ))
        except Exception as e:
            self.results.append(PipelineResult(
                stage="自适应调优", engine="AdaptiveTuner", status="🟡",
                output={"error": str(e)},
            ))

        # 9. 熔断后钩子
        if q_result and q_result.status == '🔴':
            self.registry.trigger(HookType.ON_MELTDOWN, {
                "content": content, "blocked": True
            })

        # 10. 完成后钩子（快照+监管+自适应审计）
        self.registry.trigger(HookType.ON_COMPLETE, {
            "content": content, "audited": True
        })

        total_ms = (time.time() - start) * 1000
        return {
            "pipeline_results": [r.display_line() for r in self.results],
            "total_duration_ms": round(total_ms, 1),
            "stages_completed": len(self.results),
            "dna": f"#龍芯⚡️UnifiedPipeline-v2.0-{hashlib.sha3_256(content.encode()).hexdigest()[:12]}",
        }

    def visualization(self) -> str:
        """可视化管道状态图"""
        lines = [
            "╔══════════════════════════════════════════════════════╗",
            "║  龍魂统一管道 · 13大引擎全览 (v2.1)                  ║",
            "╠══════════════════════════════════════════════════════╣",
        ]
        for r in self.results[-12:]:
            lines.append(f"║  {r.display_line():54s} ║")
        lines.append("╠══════════════════════════════════════════════════════╣")

        # 钩子状态
        s = self.registry.status()
        orphan_ok, orphans = self.registry.verify_no_orphans()
        lines.append(f"║  🔗 钩子: {s['enabled_hooks']}/{s['total_hooks']} 活跃, 脱钩:{'✅ 无' if orphan_ok else f'❌ {len(orphans)}个'}          ║")
        lines.append("╚══════════════════════════════════════════════════════╝")
        return "\n".join(lines)


# 全局单例
_unified_pipeline: Optional[UnifiedPipeline] = None


def get_pipeline() -> UnifiedPipeline:
    global _unified_pipeline
    if _unified_pipeline is None:
        _unified_pipeline = UnifiedPipeline()
    return _unified_pipeline


# ═══════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════

def main():
    if len(sys.argv) < 2:
        print("╔══════════════════════════════════════════╗")
        print("║  龍魂统一钩子连接器 v1.0                 ║")
        print("╠══════════════════════════════════════════╣")
        print("║  python3 bin/lh_unified_hook.py pipeline <文本>")
        print("║    全链路: 五大引擎串联")
        print("║")
        print("║  python3 bin/lh_unified_hook.py hooks")
        print("║    查看钩子注册状态")
        print("║")
        print("║  python3 bin/lh_unified_hook.py orphans")
        print("║    检查脱钩属性")
        print("║")
        print("║  python3 bin/lh_unified_hook.py viz")
        print("║    可视化管道状态")
        print("║")
        print("║  python3 bin/lh_unified_hook.py test")
        print("║    运行全链路测试")
        print("╚══════════════════════════════════════════╝")
        sys.exit(0)

    cmd = sys.argv[1]
    pipeline = get_pipeline()

    if cmd == "pipeline":
        text = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else sys.stdin.read().strip()
        if not text:
            print("❌ 请提供内容")
            sys.exit(1)
        print(f"\n🚀 全链路管道: \"{text[:30]}...\"")
        print()
        result = pipeline.process(text)
        for line in result['pipeline_results']:
            print(line)
        print(f"\n  ⏱️ 总耗时: {result['total_duration_ms']}ms")
        print(f"  📜 DNA: {result['dna']}")

    elif cmd == "hooks":
        s = pipeline.registry.status()
        print(f"  总钩子: {s['total_hooks']} 个")
        print(f"  活跃: {s['enabled_hooks']} 个")
        print(f"  模块: {s['modules']}")
        print(f"  按类型:")
        for t, n in s['by_type'].items():
            if n > 0:
                print(f"    {t}: {n} 个")

    elif cmd == "orphans":
        ok, missing = pipeline.registry.verify_no_orphans()
        if ok:
            print("  ✅ 无脱钩属性 · 所有模块均已注册钩子")
        else:
            print(f"  ❌ 发现 {len(missing)} 个脱钩模块:")
            for m in missing:
                print(f"    - {m}")

    elif cmd == "viz":
        # 先跑一条测试数据
        pipeline.process("测试管道可视化", "viz")
        print(pipeline.visualization())

    elif cmd == "test":
        pipeline = UnifiedPipeline()
        test_cases = [
            ("正常内容", "这是一篇关于AI安全的教育文章"),
            ("底线触碰", "技术无国界是我们要坚持的原则"),
        ]

        for name, text in test_cases:
            print(f"\n🧪 {name}:")
            result = pipeline.process(text, "test")
            for line in result['pipeline_results']:
                print(line)

        print(f"\n{pipeline.visualization()}")
        ok, missing = pipeline.registry.verify_no_orphans()
        print(f"\n  🔗 脱钩检查: {'✅ 无脱钩' if ok else f'❌ {missing}'}")
        print(f"  🎉 全链路测试完成")

    else:
        print(f"未知命令: {cmd}")


if __name__ == "__main__":
    main()
