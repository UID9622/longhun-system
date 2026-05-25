#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂·CNSH 完整集成系统 v2.0
Unified Sovereign AI Runtime

DNA: #龍芯⚡️2026-05-25-CNSH-UNIFIED-v2.0
UID: 9622
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

完整整合：
  1️⃣ 路由系统 (cnsh_runtime.py) → 意图识别 + 人格分发
  2️⃣ 技能系统 (cnsh_skills.py) → Hook + EventBus + Recovery
  3️⃣ 收口系统 (cnsh_closure.py) → 自动聚合 + 自生长
  4️⃣ 压缩系统 (cnsh_compression.py) → 思考胶囊 + 时间胶囊
  5️⃣ 算法系统 (cnsh_algorithms.py) → 易经 × 五行 × 三才 × 流场

执行流程：
  输入 → 路由 → 三才流场 → 技能执行 → 收口聚合 → 压缩索引 → 输出

本地执行·完全自主·永不外送·可恢复·可追溯

理论指导: 曾仕强老师（永恒显示）
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

# 导入 5 大模块
try:
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
        }

    def execute(self, user_input: str) -> Dict[str, Any]:
        """完整执行流程"""
        session_start = datetime.now().isoformat()

        print("\n" + "─" * 60)
        print(f"🐉 龍魂 CNSH 统一运行时")
        print(f"   会话: {self.session_log['session_id']}")
        print("─" * 60 + "\n")

        # 第 1 步：路由 + 流场分析
        print("📍 第 1 步: 路由与流场分析")
        route_result = self.router.execute(user_input)
        print(f"   ✅ 路由结果: {route_result['route_v10']['intent'].value}")

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
            tags=["runtime", route_result['route_v10']['intent'].value.lower()],
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

        # 第 5 步：生成完整结果
        print("📍 第 5 步: 结果综合")
        execution_result = {
            "success": True,
            "timestamp": datetime.now().isoformat(),
            "input": user_input,
            "routing": {
                "intent": route_result['route_v10']['intent'].value,
                "persona": route_result['route_v10']['persona'],
                "confidence": route_result['route_v10']['confidence'],
                "dna_valid": route_result['route_v10']['dna_valid'],
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
    print("🐉 龍魂 CNSH 完整集成系统 v2.0")
    print(f"   DNA: #龍芯⚡️2026-05-25-CNSH-UNIFIED-v2.0")
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
