# DNA: #龍芯⚡️丙午·乙未·乙丑·小畜-FIX_DNA-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ╔═══════════════════════════════════════════════════════════════════════════╗
# ║  DNA追溯头（不可删除 · 删除即断链）                                       ║
# ╚═══════════════════════════════════════════════════════════════════════════╝
# 龍芯⚡️2026-07-07-IPA-EXECUTOR-v2.0
# 精修: 2026-07-07 — v2.0 统一到 ipa_unified_router · 名称规范·家族体系·自动冲突检测

"""
IPA 路由执行器 v2.0 — 已统一到 ipa_unified_router

v2.0 重大变更:
  - 技能归属表/人格名称从 ipa_unified_router.技能人格归属表 读取（唯一真相源）
  - 名称规范从 人格名称规范表 读取
  - 家族体系集成：每个分发带家族签章
  - 冲突检测委托给统一路由器

向后兼容:
  - 旧的 技能人格归属表 已映射到 ipa_unified_router.技能人格归属表
  - 旧接口 .执行() / .编排执行() / .冲突检测() 保持可用
"""

import hashlib
import time
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

# 从统一路由器导入权威数据
from .ipa_unified_router import (
    技能人格归属表 as _统一技能归属表,
    人格名称规范表,
    家族组定义,
    get_unified_router,
)

# ═══════════════════════════════════════════════════════════
# 向后兼容：导出旧格式的 技能人格归属表
# ═══════════════════════════════════════════════════════════

def _构建旧格式归属表() -> Dict[str, Dict[str, Any]]:
    """从统一格式转换为旧 ipa_executor v1.0 格式（向后兼容）"""
    旧格式: Dict[str, Dict[str, Any]] = {}
    for 技能名, 归属 in _统一技能归属表.items():
        人格代码 = 归属["人格代码"]
        规范名称 = 归属["规范名称"]
        人格条目 = 人格名称规范表.get(人格代码, {})
        旧格式[技能名] = {
            "owner": 人格代码,
            "owner_name": 规范名称,
            "owner_role": 人格条目.get("角色", ""),
            "ipa_node": 归属["ipa_node"],
            "description": 归属.get("描述", ""),
            "requires_audit": 归属.get("需要审计", False),
        }
    return 旧格式

# 旧格式兼容导出（供 main.py 等引用）
技能人格归属表 = _构建旧格式归属表()

# 人格能力边界（从统一路由器推导）
人格能力边界 = {
    "P01": {"专属技能": ["三才决策", "易经推演决策"], "协作技能": [], "禁止技能": ["数字根查询", "五行关系查询"], "说明": "战略推演·不做具体计算"},
    "P02": {"专属技能": ["数字根查询", "五行关系查询", "河图洛书展示", "DNA生成", "四柱五行强度", "公式速查", "CNSH64状态空间"], "协作技能": [], "禁止技能": ["三才决策", "三色审计查询"], "说明": "数学引擎·不做战略决策"},
    "P03": {"专属技能": [], "协作技能": ["计算机诊断", "三色审计查询"], "禁止技能": [], "说明": "逻辑验证·协作审计"},
    "P05": {"专属技能": ["三色审计查询", "综合诊断"], "协作技能": [], "禁止技能": ["数字根查询", "易经推演决策"], "说明": "元控制·不做底层计算"},
    "P06": {"专属技能": ["计算机诊断"], "协作技能": ["三色审计查询"], "禁止技能": [], "说明": "对抗模拟·独立审计"},
    "P13": {"专属技能": ["BraKet人格分析"], "协作技能": [], "禁止技能": ["数字根查询"], "说明": "人格编排·不做数学计算"},
    "P17": {"专属技能": ["八卦查询", "Lu指令翻译"], "协作技能": [], "禁止技能": ["三才决策", "易经推演决策", "数字根查询", "四柱五行强度", "DNA生成", "BraKet人格分析", "CNSH64状态空间"], "说明": "入口人格·只做意图识别+轻量查询·不扛重活"},
    "P72": {"专属技能": [], "协作技能": ["所有技能-旁路仲裁"], "禁止技能": [], "说明": "龍盾·一票否决·不参与常规计算"},
}


# ═══════════════════════════════════════════════════════════
# IPA 执行器
# ═══════════════════════════════════════════════════════════

class IPA执行器:
    """
    IPA路由执行器·技能分发管道

    流程:
      用户输入 → P17 意图识别 → P13 人格编排 → 目标人格执行 → P05 审计 → P17 展示结果
    """

    DNA = "#龍芯⚡️2026-07-07-IPA-EXECUTOR-v2.0"

    def __init__(self, 技能引擎: Any = None):
        self.技能引擎 = 技能引擎
        self._执行日志: List[Dict[str, Any]] = []
        self._审计缓存: Dict[str, Any] = {}
        self._统一路由 = get_unified_router(技能引擎)

    # ── 核心：执行分发 ──

    def 执行(self, 技能名: str, **kwargs: Any) -> Dict[str, Any]:
        """
        按人格归属执行技能

        流程:
          1. 查归属表 → 确定主人格
          2. 验证边界 → 检查主人格是否有权执行该技能
          3. P17 入口校验 → 如果技能属于重活·P17不能抢
          4. 调用技能函数
          5. 审计（如需要）
          6. 记录执行日志
          7. 返回带人格签名的结果

        Args:
            技能名: 技能函数名（如 '数字根查询'）
            **kwargs: 传递给技能函数的参数

        Returns:
            带执行追踪的结果字典
        """
        归属 = 技能人格归属表.get(技能名)
        if not 归属:
            return {
                "success": False,
                "error": f"未知技能: {技能名}",
                "可用技能": list(技能人格归属表.keys()),
                "dna": self.DNA,
            }

        owner_id = 归属["owner"]
        owner_name = 归属["owner_name"]
        ipa_node = 归属["ipa_node"]

        # 验证技能函数存在
        func = getattr(self.技能引擎, 技能名, None)
        if not func or not callable(func):
            return {
                "success": False,
                "error": f"技能函数不存在: {技能名}",
                "dna": self.DNA,
            }

        # 记录执行开始
        开始时间 = time.time()
        执行记录: Dict[str, Any] = {
            "技能": 技能名,
            "主人格": {"代码": owner_id, "名称": owner_name},
            "IPA节点": ipa_node,
            "时间": datetime.now().isoformat(),
            "参数摘要": {k: str(v)[:50] for k, v in kwargs.items()},
        }

        # 实际调用技能函数
        try:
            结果 = func(**kwargs)
            耗时 = round((time.time() - 开始时间) * 1000, 2)
        except Exception as e:
            执行记录["状态"] = "失败"
            执行记录["错误"] = str(e)
            self._执行日志.append(执行记录)
            return {
                "success": False,
                "error": str(e),
                "技能": 技能名,
                "执行人格": {"代码": owner_id, "名称": owner_name},
                "追踪": 执行记录,
                "dna": self.DNA,
            }

        # 后审计（如技能需要）
        审计结果 = None
        if 归属.get("requires_audit", False) and isinstance(结果, dict):
            审计结果 = self._审计(技能名, 结果, owner_id)

        # 完成记录
        执行记录["状态"] = "完成"
        执行记录["耗时_ms"] = 耗时
        执行记录["审计"] = 审计结果
        self._执行日志.append(执行记录)

        # v2.0: 注入人格归属+家族签章
        if isinstance(结果, dict):
            结果["_执行人格"] = {
                "代码": owner_id,
                "名称": owner_name,
                "角色": 归属.get("owner_role", ""),
                "IPA节点": ipa_node,
            }
            # 家族签章
            家族信息 = self._统一路由.家族归属(owner_id)
            结果["_家族签章"] = {
                "家族层级": 家族信息.get("家族层级", ""),
                "家族组": 家族信息.get("家族组", ""),
                "家族组名称": 家族信息.get("家族组名称", ""),
            }
            结果["_执行审计"] = 审计结果
            结果["_执行耗时_ms"] = 耗时
            if "DNA" not in 结果:
                结果["DNA"] = self._生成执行DNA(技能名, owner_id)
            return 结果
        else:
            return {
                "success": True,
                "技能": 技能名,
                "value": 结果,
                "执行人格": {"代码": owner_id, "名称": owner_name},
                "IPA节点": ipa_node,
                "_执行耗时_ms": 耗时,
                "dna": self.DNA,
            }

    # ── 批量执行（多步任务·P13编排）──

    def 编排执行(self, 任务描述: str, 技能序列: List[Tuple[str, Dict[str, Any]]]) -> Dict[str, Any]:
        """
        P13 姜子牙编排多步任务

        流程:
          P13 → 拆解任务 → 逐个分发 → 汇总结果 → 审计

        Args:
            任务描述: 任务描述
            技能序列: [(技能名1, 参数1), (技能名2, 参数2), ...]

        Returns:
            多维结果汇总
        """
        编排结果 = {
            "任务": 任务描述,
            "编排人格": {"代码": "P13", "名称": "姜子牙", "角色": "merit_gatekeeper"},
            "IPA节点": "IPA-L2-FLOW-PALACE-ROUTER-008",
            "步骤数": len(技能序列),
            "步骤结果": [],
            "成功数": 0,
            "失败数": 0,
        }

        for i, (技能名, 参数) in enumerate(技能序列):
            归属 = 技能人格归属表.get(技能名, {})
            步骤结果 = self.执行(技能名, **参数)

            步骤记录 = {
                "步骤": i + 1,
                "技能": 技能名,
                "指派人格": 归属.get("owner", "P13"),
                "成功": 步骤结果.get("success", True) if isinstance(步骤结果, dict) else True,
                "结果": {k: v for k, v in (步骤结果.items() if isinstance(步骤结果, dict) else {}) if not k.startswith("_")},
            }

            if 步骤记录["成功"]:
                编排结果["成功数"] += 1
            else:
                编排结果["失败数"] += 1

            编排结果["步骤结果"].append(步骤记录)

        编排结果["timestamp"] = datetime.now().isoformat()
        编排结果["DNA"] = self._生成执行DNA(任务描述[:12], "P13")

        return 编排结果

    # ── 路由建议（给前端展示用）──

    def 路由建议(self, 查询文本: str) -> Dict[str, Any]:
        """
        根据用户输入建议分发的人格

        Args:
            查询文本: 用户输入的自然语言

        Returns:
            推荐人格·匹配技能·分发说明
        """
        from .persona_bridge import get_bridge
        bridge = get_bridge()
        route = bridge.route(查询文本)

        # 找出匹配的技能
        匹配技能: List[Dict[str, Any]] = []
        for 技能名, 归属 in 技能人格归属表.items():
            # 简单关键词匹配
            if any(kw in 查询文本 for kw in ["数字根", "五行", "河图", "洛书", "八卦", "卦", "算", "数学", "算法"]):
                if 归属["owner"] in ["P02"]:
                    匹配技能.append({"技能": 技能名, "归属人格": 归属["owner_name"], "IPA节点": 归属["ipa_node"]})
            if any(kw in 查询文本 for kw in ["审计", "检查", "安全", "风险"]):
                if 归属["owner"] in ["P05", "P06"]:
                    匹配技能.append({"技能": 技能名, "归属人格": 归属["owner_name"], "IPA节点": 归属["ipa_node"]})
            if any(kw in 查询文本 for kw in ["决策", "三才", "易经", "战略", "推演"]):
                if 归属["owner"] in ["P01"]:
                    匹配技能.append({"技能": 技能名, "归属人格": 归属["owner_name"], "IPA节点": 归属["ipa_node"]})
            if any(kw in 查询文本 for kw in ["人格", "BraKet", "叠加"]):
                if 归属["owner"] in ["P13"]:
                    匹配技能.append({"技能": 技能名, "归属人格": 归属["owner_name"], "IPA节点": 归属["ipa_node"]})

        return {
            "输入": 查询文本,
            "意图路由": route,
            "推荐分发": {
                "主人格": route.get("primary", {}),
                "副人格": route.get("secondaries", []),
                "匹配技能": 匹配技能[:3] if 匹配技能 else "未精确匹配·宝宝将根据意图推荐",
            },
            "提示": "宝宝(P17)只做入口展示·具体计算由对应人格执行",
            "dna": self.DNA,
            "timestamp": datetime.now().isoformat(),
        }

    # ── 冲突检测（v2.0 委托统一路由器）──

    def 冲突检测(self) -> Dict[str, Any]:
        """
        全局冲突检测（委托统一路由器）

        Returns:
            冲突报告
        """
        统一结果 = self._统一路由.检测冲突()

        # 附加旧版人格边界检查
        边界冲突: List[Dict[str, Any]] = []
        for 技能名, 归属 in 技能人格归属表.items():
            owner = 归属["owner"]
            boundary = 人格能力边界.get(owner, {})
            禁止技能 = boundary.get("禁止技能", [])
            if 技能名 in 禁止技能:
                边界冲突.append({
                    "类型": "人格边界违反",
                    "技能": 技能名,
                    "归属人格": owner,
                    "边界说明": boundary.get("说明", ""),
                    "严重性": "高",
                })

        总冲突 = 统一结果["总冲突/警告"] + len(边界冲突)
        return {
            "检测时间": datetime.now().isoformat(),
            "冲突数": 总冲突,
            "统一路由冲突": 统一结果,
            "边界冲突": 边界冲突,
            "状态": "🟢 无冲突" if 总冲突 == 0 else "🔴 存在冲突·需修复",
            "dna": self.DNA,
        }

    # ── 技能归属总览（v2.0 家族层级视角）──

    def 归属总览(self) -> Dict[str, Any]:
        """返回技能→人格→家族归属总览表"""
        按人格分组: Dict[str, List[str]] = {}
        for 技能名, 归属 in 技能人格归属表.items():
            owner_id = 归属["owner"]
            owner_name = 归属["owner_name"]
            家族信息 = self._统一路由.家族归属(owner_id)
            key = f"{owner_id}·{owner_name}·{家族信息.get('家族组', '')}"
            if key not in 按人格分组:
                按人格分组[key] = []
            按人格分组[key].append(技能名)

        return {
            "技能总数": len(技能人格归属表),
            "人格_家族分布": 按人格分组,
            "家族层级": self._统一路由.家族层级总览(),
            "P17宝宝定位": "入口人格·只负责意图识别+情感缓冲+结果展示·具体计算由各专业人格执行",
            "架构原则": "家族体系三层：L0设备主人→L0.5家族层→L1+人格层·各司其职",
            "dna": self.DNA,
            "timestamp": datetime.now().isoformat(),
        }

    # ── 审计与DNA ──

    def _审计(self, 技能名: str, 结果: Dict[str, Any], 操作人格: str) -> Dict[str, Any]:
        """P05 执行后审计"""
        审计 = {
            "审计人格": "P05·执行外设",
            "审计时间": datetime.now().isoformat(),
            "审计项": [],
            "通过": True,
        }

        # 检查结果完整性
        if "DNA" not in 结果 and "dna" not in 结果:
            审计["审计项"].append("警告：结果缺少DNA追溯码")

        # 五色审计（简化版）
        五色判定 = self._五色速判(结果)
        审计["五色判定"] = 五色判定

        if 五色判定 == "🔴":
            审计["通过"] = False
            审计["审计项"].append("五色审计→🔴·需人工确认")

        self._审计缓存[技能名] = 审计
        return 审计

    @staticmethod
    def _五色速判(结果: Dict[str, Any]) -> str:
        """简化版五色速判"""
        # 检查是否有风险数字
        risk = 结果.get("风险数字", 结果.get("风险等级", ""))
        if risk:
            try:
                r = int(str(risk).replace("/100", ""))
                if r >= 85:
                    return "🔴"
                elif r >= 50:
                    return "🟡"
                else:
                    return "🟢"
            except (ValueError, TypeError):
                pass

        # 检查综合得分
        score = 结果.get("综合得分", 结果.get("均衡指数", 0))
        if isinstance(score, (int, float)):
            if score >= 0.8:
                return "🟢"
            elif score >= 0.5:
                return "🟡"
            else:
                return "🟡"
        return "🟢"

    @staticmethod
    def _生成执行DNA(技能名: str, 人格代码: str) -> str:
        """生成执行DNA"""
        ts = str(int(time.time()))
        dna_input = f"{技能名}{人格代码}{ts}"
        dna_hash = hashlib.sha256(dna_input.encode()).hexdigest()[:8]
        return f"#龍芯⚡️{datetime.now().strftime('%Y%m%d-%H%M%S')}-{人格代码}-{技能名[:4]}-{dna_hash}"


# ═══════════════════════════════════════════════════════════
# 单例
# ═══════════════════════════════════════════════════════════

_ipa_executor_instance: Optional[IPA执行器] = None


def get_ipa_executor(技能引擎: Any = None) -> IPA执行器:
    """获取IPA执行器单例"""
    global _ipa_executor_instance
    if _ipa_executor_instance is None:
        if 技能引擎 is None:
            from .baobao_skills import 宝宝技能引擎  # pyright: ignore[reportPossiblyUnboundVariable]
            技能引擎 = 宝宝技能引擎()
        _ipa_executor_instance = IPA执行器(技能引擎)
    return _ipa_executor_instance
