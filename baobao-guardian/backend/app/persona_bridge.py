# DNA: #龍芯⚡️丙午·乙未·乙丑·小畜-FIX_DNA-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ╔═══════════════════════════════════════════════════════════════════════════╗
# ║  DNA追溯头（不可删除 · 删除即断链）                                       ║
# ╚═══════════════════════════════════════════════════════════════════════════╝
# 龍芯⚡️2026-07-06-BAOBAO-PERSONA-BRIDGE-v1.0
# 精修: 2026-07-06 — baobao-guardian ↔ persona_hub 联动桥接

"""
宝宝守护助手 ↔ 人格中枢 桥接模块

让 baobao-guardian 能够：
- 根据用户输入自动路由到正确人格
- 查询当前卦象和策略建议
- 获取人格内阁状态

用法:
    from persona_bridge import PersonaBridge
    bridge = PersonaBridge()
    result = bridge.route("宝宝 帮我检查安全")
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple

# 确保能找到 persona 数据和 hub
_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
_PERSONA_DIR = _PROJECT_ROOT / "persona"
_HUB_PATH = _PROJECT_ROOT / "L9_子系统" / "subsystems" / "longhun_persona_hub.py"

# 将 hub 目录加入路径
_HUB_DIR = _HUB_PATH.parent
if str(_HUB_DIR) not in sys.path:
    sys.path.insert(0, str(_HUB_DIR))


class PersonaBridge:
    """宝宝守护助手的人格中枢桥接器"""

    DNA = "#龍芯⚡️2026-07-07-BAOBAO-PERSONA-BRIDGE-v1.2"
    # v1.1: 新增IPA分发执行·宝宝不一个人扛
    # v1.2: 集成统一路由器·名称归一·家族归属·自动冲突检测

    def __init__(self):
        self.persona_dir = _PERSONA_DIR
        self._hub = None
        self._ipa_executor = None  # 延迟绑定·避免循环导入
        self._统一路由 = None      # v1.2 统一路由器

    @property
    def hub(self):
        """懒加载人格中枢"""
        if self._hub is None:
            try:
                from longhun_persona_hub import 龍魂人格中枢  # pyright: ignore[reportMissingImports]
                self._hub = 龍魂人格中枢(base_dir=str(_PROJECT_ROOT))
            except ImportError:
                self._hub = self._fallback_hub()
        return self._hub

    def _fallback_hub(self):
        """保底：直接读 JSON 做路由"""
        _fb_persona_dir = self.persona_dir

        class FallbackHub:
            def __init__(self, persona_dir):
                self.persona_dir = persona_dir
                self._数据源路径 = str(persona_dir)
                self._版本 = "fallback-v1.0"
                registry_path = self.persona_dir / "persona_registry.json"
                with open(registry_path) as f:
                    self.registry = json.load(f)
                self.personas = self.registry.get("personas", {})
                self.rules = self.registry.get("routing_rules", [])
                self.arbitrations = self.registry.get("arbitration_rules", [])

            def 路由人格(self, task: str) -> Dict[str, Any]:
                task_lower = task.lower()
                scores: list[tuple[int, Any, Any]] = []
                for rule in self.rules:
                    score = sum(1 for t in rule.get("triggers", []) if t.lower() in task_lower)
                    if score > 0:
                        matched = [t for t in rule.get("triggers", []) if t.lower() in task_lower]
                        scores.append((score, rule, matched))
                if not scores:
                    return {
                        "任务": task,
                        "匹配规则": "DEFAULT",
                        "规则名称": "宝宝默认路由",
                        "主人格": {"代码": "P17", "名称": "宝宝", "权重": 0.97},
                        "副人格": [{"代码": "P05", "名称": "执行外设", "权重": 1.0}],
                        "执行模式": "sequential",
                    }
                scores.sort(key=lambda x: x[0], reverse=True)
                best = scores[0]
                rule = best[1]
                primary = self.personas.get(rule["primary"], {})
                secondaries = [self.personas.get(sid, {}) for sid in rule.get("secondary", [])]
                return {
                    "任务": task,
                    "匹配规则": rule.get("id", ""),
                    "规则名称": rule.get("name", ""),
                    "匹配关键词": best[2],
                    "主人格": {
                        "代码": rule.get("primary", "P17"),
                        "名称": primary.get("name", ""),
                        "权重": primary.get("weight", 0),
                    },
                    "副人格": [
                        {"代码": s.get("code", ""), "名称": s.get("name", ""), "权重": s.get("weight", 0)}
                        for s in secondaries if s
                    ],
                    "执行模式": rule.get("mode", "sequential"),
                }

            def 人格建议(self, task: str, _uid: str = "UID9622") -> Dict[str, Any]:
                """与 hub.人格建议() 兼容的接口"""
                route = self.路由人格(task)
                return {
                    "路由结果": route,
                    "关系权重": 1.0,
                    "当前卦象": {"卦名": "乾", "卦象": "䷀", "含义": "元亨利贞", "属性": "天"},
                    "策略建议": "宝宝入口默认路由",
                }

            def 列出人格(self) -> List[Dict[str, Any]]:
                """列出所有人格"""
                return [
                    {"代码": pid, "名称": p.get("name", ""), "角色": p.get("role", ""),
                     "权重": p.get("weight", 0), "成功率": p.get("success_rate", 0),
                     "状态": p.get("status", ""), "路由优先级": p.get("route_priority", "")}
                    for pid, p in self.personas.items()
                ]

            def 系统信息(self) -> Dict[str, Any]:
                """系统元信息"""
                return {
                    "版本": "fallback-v1.0",
                    "DNA": PersonaBridge.DNA,
                    "数据源": str(self.persona_dir),
                    "人格数": len(self.personas),
                    "路由规则数": len(self.rules),
                    "仲裁规则数": len(self.arbitrations),
                    "卦象数": 64,
                }

        return FallbackHub(_fb_persona_dir)

    def route(self, task: str) -> Dict[str, Any]:
        """路由任务到正确人格"""
        try:
            result = self.hub.人格建议(task, "UID9622")
            return {
                "success": True,
                "task": task,
                "primary": result["路由结果"]["主人格"],
                "secondaries": result["路由结果"]["副人格"],
                "mode": result["路由结果"]["执行模式"],
                "hexagram": result["当前卦象"],
                "strategy": result["策略建议"],
                "dna": self.DNA,
                "timestamp": datetime.now().isoformat(),
            }
        except Exception:
            # 降级到 fallback
            try:
                fb = self._fallback_hub()
                route = fb.路由人格(task)
                return {
                    "success": True,
                    "task": task,
                    "primary": route["主人格"],
                    "secondaries": route.get("副人格", []),
                    "mode": route.get("执行模式", "sequential"),
                    "fallback": True,
                    "dna": self.DNA,
                    "timestamp": datetime.now().isoformat(),
                }
            except Exception as e2:
                return {
                    "success": False,
                    "error": str(e2),
                    "dna": self.DNA,
                    "timestamp": datetime.now().isoformat(),
                }

    def list_personas(self) -> List[Dict[str, Any]]:
        """列出现有人格"""
        try:
            return self.hub.列出人格()
        except Exception:
            with open(self.persona_dir / "persona_registry.json") as f:
                registry = json.load(f)
            return [
                {"代码": pid, "名称": p.get("name", ""), "角色": p.get("role", ""),
                 "权重": p.get("weight", 0), "状态": p.get("status", "")}
                for pid, p in registry.get("personas", {}).items()
            ]

    def system_info(self) -> Dict[str, Any]:
        """系统信息"""
        try:
            return self.hub.系统信息()  # type: ignore[attr-defined]
        except Exception:
            return {"版本": "fallback", "DNA": self.DNA}

    def get_baby_response(self, query: str) -> Dict[str, Any]:
        """宝宝入口：快捷响应"""
        return self.route(f"宝宝 {query}")

    # ═══════════════════════════════════════════════════════════
    # v1.1 新增 — IPA 分发执行
    # ═══════════════════════════════════════════════════════════

    def dispatch_to_persona(self, 技能名: str, **kwargs: Any) -> Dict[str, Any]:
        """
        通过 IPA 执行器将技能分发到对应人格

        宝宝(P17)不做重活·此方法将技能路由到正确的专业人格

        Args:
            技能名: 技能名称（如 '数字根查询'）
            **kwargs: 技能参数

        Returns:
            执行结果（含人格归属签名）
        """
        if self._ipa_executor is None:
            try:
                from .ipa_executor import get_ipa_executor  # pyright: ignore[reportPossiblyUnboundVariable]
                from .baobao_skills import 宝宝技能引擎  # pyright: ignore[reportPossiblyUnboundVariable]
                self._ipa_executor = get_ipa_executor(宝宝技能引擎())
            except ImportError:
                return {
                    "success": False,
                    "error": "IPA执行器不可用",
                    "dna": self.DNA,
                }

        return self._ipa_executor.执行(技能名, **kwargs)

    def dispatch_with_routing(self, task: str) -> Dict[str, Any]:
        """
        先路由再分发：意图识别 → 人格路由 → 执行分发

        完整链路:
          P17 意图识别 → persona_bridge.route() 确定主人格
          → IPA执行器找到匹配技能 → 分发给专业人格执行

        Args:
            task: 用户输入的自然语言任务

        Returns:
            路由结果 + 执行结果（如能匹配到技能）
        """
        # Step 1: 路由到人格
        routing = self.route(task)

        # Step 2: 尝试匹配技能
        if self._ipa_executor is None:
            try:
                from .ipa_executor import get_ipa_executor, 技能人格归属表  # pyright: ignore[reportPossiblyUnboundVariable]
                from .baobao_skills import 宝宝技能引擎  # pyright: ignore[reportPossiblyUnboundVariable]
                self._ipa_executor = get_ipa_executor(宝宝技能引擎())
            except ImportError:
                return {
                    "success": False,
                    "error": "IPA执行器不可用",
                    "routing": routing,
                }

        # 按路由结果匹配技能
        路由人格代码 = routing.get("primary", {}).get("代码", "P17")
        匹配技能: List[Dict[str, Any]] = []
        from .ipa_executor import 技能人格归属表
        for 技能名, 归属 in 技能人格归属表.items():
            if 归属["owner"] == 路由人格代码:
                匹配技能.append({
                    "技能": 技能名,
                    "IPA节点": 归属["ipa_node"],
                    "描述": 归属["description"],
                })

        return {
            "success": True,
            "task": task,
            "routing": routing,
            "dispatch": {
                "指派人格": 路由人格代码,
                "匹配技能": 匹配技能,
                "建议": f"宝宝已将任务分发给 {routing.get('primary', {}).get('名称', '宝宝')}({路由人格代码})",
            },
            "架构说明": "宝宝(P17)只做入口·P13编排·专业人格执行·各司其职",
            "dna": self.DNA,
            "timestamp": datetime.now().isoformat(),
        }

    def ipa_conflict_check(self) -> Dict[str, Any]:
        """检查技能归属是否与人格矩阵冲突"""
        if self._ipa_executor is None:
            try:
                from .ipa_executor import get_ipa_executor  # pyright: ignore[reportPossiblyUnboundVariable]
                from .baobao_skills import 宝宝技能引擎  # pyright: ignore[reportPossiblyUnboundVariable]
                self._ipa_executor = get_ipa_executor(宝宝技能引擎())
            except ImportError:
                return {"success": False, "error": "IPA执行器不可用"}
        return self._ipa_executor.冲突检测()

    # ═══════════════════════════════════════════════════════════
    # v1.2 新增 — 统一路由·名称归一·家族归属
    # ═══════════════════════════════════════════════════════════

    def _ensure_unified_router(self) -> Any:
        """确保统一路由器已初始化"""
        if self._统一路由 is None:
            try:
                from .ipa_unified_router import get_unified_router  # pyright: ignore[reportPossiblyUnboundVariable]
                self._统一路由 = get_unified_router()
            except ImportError:
                pass
        return self._统一路由

    def 名称归一(self, 输入名称: str) -> Dict[str, Any]:
        """
        任意别名→规范名称

        示例:
          '数学大师' → '镜像审计者' (P06)
          '宝宝' → '宝宝' (P17)
          '龍芯·姜子牙' → '姜子牙' (P13)

        Args:
            输入名称: 任意别名

        Returns:
            规范映射结果
        """
        router = self._ensure_unified_router()
        if router:
            return router.名称归一(输入名称)
        return {"error": "统一路由器不可用", "输入": 输入名称}

    def 家族归属(self, 人格代码: str) -> Dict[str, Any]:
        """
        查询人格代码在家族体系中的位置

        Args:
            人格代码: P01/P02/.../UID9622

        Returns:
            家族层级、家族组、同组人格
        """
        router = self._ensure_unified_router()
        if router:
            return router.家族归属(人格代码)
        return {"error": "统一路由器不可用", "人格代码": 人格代码}

    def 统一冲突检测(self) -> Dict[str, Any]:
        """
        全量冲突检测（名称不一致+家族组归属+别名多义+技能归属）

        Returns:
            完整冲突报告
        """
        router = self._ensure_unified_router()
        if router:
            return router.检测冲突()
        return {"error": "统一路由器不可用"}

    def 家族总览(self) -> Dict[str, Any]:
        """家族体系全貌"""
        router = self._ensure_unified_router()
        if router:
            return router.家族层级总览()
        return {"error": "统一路由器不可用"}

    def 合并并检测(self, 新增人格列表: List[Tuple[str, Dict[str, Any]]], 策略: str = "覆盖") -> Dict[str, Any]:
        """
        批量合并人格+事后冲突检测

        流程：
          1. 合并（覆盖/新增/仅新增）
          2. 重建别名索引
          3. 冲突检测
          4. 返回合并结果+冲突报告

        Args:
            新增人格列表: [(人格代码, 条目), ...]
            策略: "覆盖" | "仅新增" | "强制覆盖"

        Returns:
            合并结果+冲突报告
        """
        router = self._ensure_unified_router()
        if not router:
            return {"error": "统一路由器不可用"}

        合并结果 = router.批量合并(新增人格列表, 策略)
        冲突报告 = router.检测冲突()
        return {
            "合并": 合并结果,
            "冲突检测": 冲突报告,
            "建议": "如有冲突，请检查冲突详情并手动修复；或使用'强制覆盖'策略",
            "dna": self.DNA,
            "timestamp": datetime.now().isoformat(),
        }


# 单例
_bridge_instance: Optional[PersonaBridge] = None


def get_bridge() -> PersonaBridge:
    """获取桥接器单例"""
    global _bridge_instance
    if _bridge_instance is None:
        _bridge_instance = PersonaBridge()
    return _bridge_instance
