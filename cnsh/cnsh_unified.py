#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂·CNSH 完整集成系统 v2.2
Unified Sovereign AI Runtime with 道德经约束 + 引擎生长 + CNSH创造

DNA: #龍芯⚡️2026-05-25-CNSH-UNIFIED-v2.2
UID: 9622
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

核心9大系统深度融合（三大关键字升级）：
  1️⃣ 关键字提取 (cnsh_keyword_extraction.py) → 语义理解 + 369频率 + 五行映射
  2️⃣ 道德经约束 (cnsh_daodejing_engine.py) → 81章伦理框架 + 金约束木引擎
  3️⃣ 路由系统 (cnsh_runtime.py) → 意图识别 + 人格分发
  4️⃣ 路由节点v3 (cnsh_routing_node_v3.py) → 河图洛书9宫 + 不动点中心 + 智能路由
  5️⃣ 人格内核 (cnsh_persona_core_upgrade.py) → P01-P06数学核心 + 协同计算
  6️⃣ 技能系统 (cnsh_skills.py) → Hook + EventBus + Recovery
  7️⃣ 收口系统 (cnsh_closure.py) → 自动聚合 + 自生长
  8️⃣ 压缩系统 (cnsh_compression.py) → 思考胶囊 + 时间胶囊
  9️⃣ 算法系统 (cnsh_algorithms.py) → 易经 × 五行 × 三才 × 流场

三大关键字扫描结果：
  道德经(金宫7) + 引擎(木宫8) + CNSH(火宫3) = 0.571谐和度
  金克木 + 木生火 = 约束平衡创造

增强执行流程：
  输入 → 关键字提取 → 约束检查 → 9宫路由 → 三才流场 → 技能执行 → 收口聚合 → 压缩索引 → 输出

本地执行·完全自主·永不外送·可恢复·可追溯·伦理约束·UID9622不免责

理论指导: 曾仕强老师·老子道德经（永恒显示）
献礼: 龍魂系统·永恒守护·中华文化传承

用法:
    python3 cnsh_unified.py "你的问题"
    python3 cnsh_unified.py --test
"""

import sys
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import asdict

# 导入 9 大模块（含道德经引擎约束）
try:
    from cnsh_keyword_extraction import KeywordExtractionEngine
    from cnsh_routing_node_v3 import IntelligentRoutingEngineV3
    from cnsh_persona_core_upgrade import PersonaCoreCoordinationEngine
    from cnsh_daodejing_engine import DaodejingEngineConstraintSystem, CreationFlame
    from cnsh_runtime import CNSHRuntime as Router
    from cnsh_skills import CNSHSkillRuntime as SkillRuntime
    from cnsh_closure import ClosureManager
    from cnsh_compression import MemoryCompressor, CompressionLevel
    from cnsh_algorithms import FlowFieldEngine
except ImportError as e:
    print(f"❌ 导入模块失败: {e}")
    print("   请确保所有 cnsh_*.py 文件在同一目录")
    sys.exit(1)


# ════════════════════════════════════════════════════════
# 龍魂统一运行时
# ════════════════════════════════════════════════════════

class CNSHUnifiedRuntime:
    """CNSH 完整统一运行时 v2.0"""

    def __init__(self):
        # 四大新引擎：关键字 + 9宫路由 + 人格内核 + 道德经约束
        self.keyword_engine = KeywordExtractionEngine()
        self.routing_engine_v3 = IntelligentRoutingEngineV3()
        self.persona_engine = PersonaCoreCoordinationEngine()
        self.constraint_engine = DaodejingEngineConstraintSystem()

        # 原有5大系统
        self.router = Router()
        self.skill_runtime = SkillRuntime()
        self.closure_manager = ClosureManager()
        self.memory_compressor = MemoryCompressor()
        self.flow_field_engine = FlowFieldEngine()

        self.work_dir = Path("~/.cnsh/unified").expanduser()
        self.work_dir.mkdir(parents=True, exist_ok=True)

        self.session_log: Dict[str, Any] = {
            "session_id": f"session-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "created_at": datetime.now().isoformat(),
            "interactions": [],
            "dna_chain": [],
            "system_harmony": self.persona_engine.calculate_system_harmony(),
            "constraint_violations": 0,
        }

    def execute(self, user_input: str) -> Dict[str, Any]:
        """完整执行流程 (v2.1: 增强关键字 + 9宫路由 + 人格内核)"""
        session_start = datetime.now().isoformat()

        print("\n" + "─" * 60)
        print(f"🐉 龍魂 CNSH 统一运行时 v2.2")
        print(f"   会话: {self.session_log['session_id']}")
        print(f"   系统和谐度: {self.session_log['system_harmony']:.3f}/1.0")
        print(f"   约束违规: {self.session_log['constraint_violations']}")
        print("─" * 60 + "\n")

        # 新增 0 步：关键字提取与语义理解
        print("📍 第 0 步: 关键字提取与语义理解 (369 × 五行 × 易经)")
        keyword_vectors = []
        words = user_input.split()[:5]  # 取前5个词
        for word in words:
            try:
                kv = self.keyword_engine.extract_keyword(word)
                keyword_vectors.append(kv)
                print(f"   ✅ {word} → dr={kv.digital_root}, {kv.frequency_369.name}, {kv.wuxing.value[0]}")
            except Exception:
                pass  # 忽略解析失败
        text_harmony = self.keyword_engine.calculate_text_harmonic_index(keyword_vectors) if keyword_vectors else 0.5
        print(f"   ✅ 文本谐和度: {text_harmony}/1.0\n")

        # 新增 0.5 步：道德经约束检查
        print("📍 第 0.5 步: 道德经伦理约束检查 (81章约束框架)")
        flame = CreationFlame(
            flame_id=f"FLAME-{self.session_log['session_id'][-8:]}",
            intent=user_input[:30],
            engine_power_required=0.5,
            allowed_operations=["extract_keyword", "route_intent", "create_output"],
        )
        constraint_result = self.constraint_engine.execute_with_constraints(flame)
        if not constraint_result["constraint_passed"]:
            self.session_log["constraint_violations"] += 1
        print(f"   ✅ 伦理检查: {'通过✅' if constraint_result['constraint_passed'] else '警告⚠️'}\n")

        # 第 1 步：9宫路由 + 流场分析
        print("📍 第 1 步: 9宫路由与流场分析")
        route_result = self.router.execute(user_input)
        intent = route_result['route_v10']['intent']
        # Convert intent to uppercase string if needed
        if hasattr(intent, 'value'):
            intent = intent.value
        intent_str = str(intent).upper() if intent else "UNKNOWN"
        print(f"   ✅ 传统路由: {intent_str}")

        # 9宫路由增强
        try:
            node_id, primary_persona, confidence = self.routing_engine_v3.route_intent(intent_str)
            node = self.routing_engine_v3.nodes.get(node_id)
            node_name = node.bagua_name if node else "unknown"
            print(f"   ✅ 9宫路由: 节点{node_id}({node_name}) → {primary_persona} (置信度: {confidence:.2f})")
        except Exception as e:
            print(f"   ⚠️  9宫路由降级: {e}")

        flow_state = self.flow_field_engine.calculate_flow(user_input)
        flow_rec = self.flow_field_engine.generate_recommendation(flow_state)
        print(f"   ✅ 流场谐和度: {flow_state.harmony_index} ({flow_rec['harmony_level']})")
        print(f"   ✅ 推荐: {flow_rec['recommended_action']}\n")

        # 第 2 步：技能执行
        print("📍 第 2 步: 技能执行与快照")
        skill_result = self.skill_runtime.execute_skill(
            "route_dispatch",
            {
                "text": user_input,
                "route": route_result,
                "flow_state": {
                    "harmony": flow_state.harmony_index,
                    "center": flow_state.center,
                },
                "state": {"mode": "unified"},
            }
        )
        print(f"   ✅ 技能执行: {skill_result['success']}")
        print(f"   ✅ DNA: {skill_result['dna']}\n")

        # 第 3 步：收口聚合
        print("📍 第 3 步: 收口聚合")
        from cnsh_closure import PageMetadata, DrawerType

        drawer = self.closure_manager.auto_classify(
            user_input, route_result.get('description', '')
        )
        metadata = PageMetadata(
            title=user_input[:50],
            url="local",
            source="runtime",
            timestamp=datetime.now().isoformat(),
            drawer=drawer,
            tags=["runtime", intent_str.lower()],
            dna=skill_result['dna'],
        )
        page_id = self.closure_manager.add_page(metadata)
        print(f"   ✅ 页面聚合: {page_id}")
        print(f"   ✅ 分类: {drawer.value}\n")

        # 第 4 步：压缩与索引
        print("📍 第 4 步: 记忆压缩与索引")
        dialogue_turns = [
            {"text": user_input, "topic": drawer.value}
        ]
        capsule = self.memory_compressor.compress_dialogue(dialogue_turns)
        time_capsule = self.memory_compressor.create_time_capsule(capsule)
        memory_dna = self.memory_compressor.index_memory(capsule, time_capsule)
        print(f"   ✅ 思考胶囊: {capsule.capsule_id}")
        print(f"   ✅ 记忆DNA: {memory_dna}\n")

        # 第 5 步：生成完整结果 (含新系统)
        print("📍 第 5 步: 结果综合 (9系统融合)")
        execution_result = {
            "success": constraint_result["constraint_passed"],
            "timestamp": datetime.now().isoformat(),
            "input": user_input,
            "constraint_check": {
                "passed": constraint_result["constraint_passed"],
                "violations": constraint_result["violations"],
                "ethics_score": constraint_result["ethics_score"],
            },
            "semantic_analysis": {
                "keyword_vectors": len(keyword_vectors),
                "text_harmony": text_harmony,
                "frequencies": [kv.frequency_369.name for kv in keyword_vectors[:3]],
            },
            "routing": {
                "intent": intent_str,
                "persona": route_result['route_v10'].get('persona', 'unknown'),
                "confidence": route_result['route_v10'].get('confidence', 0.0),
                "dna_valid": route_result['route_v10'].get('dna_valid', False),
            },
            "wuxing_network": {
                "node_count": 9,
                "system_harmony": self.session_log['system_harmony'],
                "personas_loaded": len(self.persona_engine.personas),
            },
            "flow_field": {
                "harmony_index": flow_state.harmony_index,
                "flow_direction": flow_state.flow_direction,
                "recommendation": flow_rec['recommended_action'],
            },
            "skill_execution": {
                "skill": "route_dispatch",
                "success": skill_result['success'],
                "dna": skill_result['dna'],
            },
            "closure": {
                "page_id": page_id,
                "drawer": drawer.value,
            },
            "memory": {
                "capsule_id": capsule.capsule_id,
                "turns": capsule.turns_count,
                "dna": memory_dna,
            },
        }

        # 记录到会话日志
        self.session_log["interactions"].append(execution_result)
        self.session_log["dna_chain"].extend([
            skill_result['dna'],
            memory_dna,
        ])

        print(f"   ✅ 完整DNA链:")
        for dna in self.session_log["dna_chain"][-3:]:
            print(f"      → {dna}\n")

        return execution_result

    def save_session(self) -> str:
        """保存会话日志"""
        session_file = self.work_dir / f"{self.session_log['session_id']}.json"
        with open(session_file, "w", encoding="utf-8") as f:
            json.dump(self.session_log, f, ensure_ascii=False, indent=2)
        return str(session_file)

    def run_self_test(self) -> None:
        """自检测试"""
        print("\n" + "="*60)
        print("🧪 龍魂自检测试")
        print("="*60 + "\n")

        test_inputs = [
            "下一步怎么做系统",
            "这里有个坑要注意",
            "宝宝我有点累了",
        ]

        for i, test_input in enumerate(test_inputs, 1):
            print(f"\n🧪 测试 {i}/{ len(test_inputs)}: \"{test_input}\"")
            try:
                result = self.execute(test_input)
                print(f"   ✅ 通过")
            except Exception as e:
                print(f"   ❌ 失败: {e}")

        print("\n" + "="*60)
        print("✅ 自检测试完成")
        print("="*60)


# ════════════════════════════════════════════════════════
# 主程序入口
# ════════════════════════════════════════════════════════

def main():
    """主程序"""
    print("\n" + "="*60)
    print("🐉 龍魂 CNSH 完整集成系统 v2.2")
    print(f"   DNA: #龍芯⚡️2026-05-25-CNSH-UNIFIED-v2.2")
    print(f"   核心: 关键字 + 约束 + 9宫路由 + 人格内核 + 5大原系统")
    print(f"   三大关键字: 道德经(金) + 引擎(木) + CNSH(火)")
    print(f"   UID: 9622 | GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F")
    print("="*60)

    runtime = CNSHUnifiedRuntime()

    # 检查命令行参数
    if len(sys.argv) > 1:
        if sys.argv[1] == "--test":
            runtime.run_self_test()
        else:
            # 执行用户输入
            user_input = " ".join(sys.argv[1:])
            print(f"\n📥 输入: {user_input}")

            try:
                result = runtime.execute(user_input)
                print("\n" + "="*60)
                print("📤 执行结果")
                print("="*60)
                print(json.dumps(result, ensure_ascii=False, indent=2))
            except Exception as e:
                print(f"\n❌ 执行失败: {e}")

            # 保存会话
            session_file = runtime.save_session()
            print(f"\n💾 会话已保存: {session_file}\n")
    else:
        # 交互模式
        print("\n💬 交互模式（输入 'exit' 退出）\n")

        try:
            while True:
                try:
                    user_input = input("🐉 > ")
                    if user_input.lower() == "exit":
                        break

                    result = runtime.execute(user_input)
                except KeyboardInterrupt:
                    break
                except Exception as e:
                    print(f"❌ 错误: {e}\n")

        finally:
            session_file = runtime.save_session()
            print(f"\n💾 会话已保存: {session_file}")
            print("🐉 龍魂·永恒守护·UID9622不免责\n")


if __name__ == "__main__":
    main()
