# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
#龍芯⚡️丙午·乙未·丁巳·未时·睽-FAMILY-ROSTER-ADAPTER-v2.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
# ╔═══════════════════════════════════════════════════════════════════════════╗
# ║  DNA: #龍芯⚡️丙午·乙未·丁巳·未时·睽-FAMILY-ROSTER-ADAPTER-v2.0          ║
# ║  家族花名册兼容适配器 — 零破坏兼容层                                      ║
# ╚═══════════════════════════════════════════════════════════════════════════╝
#
# 职责:
#   1. 加载统一花名册 (L7_数据层/unified_family_roster.json)
#   2. 提供零破坏查询接口 — 现有代码无需改动即可查花名册
#   3. 首次运行自动出 diff 报告 (花名册 vs registry vs router)
#   4. 按"是谁/人格层级/信任等级/家族组/IPA路由"五维度查询
#
# 用法:
#   from bin.family_roster_adapter import 家族花名册
#   roster = 家族花名册()
#   
#   # 查一个人格
#   info = roster.查("P03")
#   # → {code, canonical_name, who, persona_layer, trust_level, ...}
#   
#   # 按家族组列出所有成员
#   members = roster.按组查("core")
#   
#   # 按信任等级筛选
#   L5 = roster.按信任查("L5")
#   
#   # 全量 diff 报告
#   roster.diff报告()
#
# 权限:
#   L0 设备主人 → 直接查询·不拦截
#   L1+ 用户 → 按水流分级
#   外部调用 → 只读·不写

"""🐉 龍魂引擎：family_roster_adapter
路径：bin/family_roster_adapter.py
TODO：请补充详细功能说明（不少于20字）。"""
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from datetime import datetime
from collections import defaultdict

# ════════════════════════════════════════
# 花名册路径
# ════════════════════════════════════════

ROSTER_PATH = Path(__file__).resolve().parent.parent / "L7_数据层" / "unified_family_roster.json"
REGISTRY_PATH = Path(__file__).resolve().parent.parent / "persona" / "persona_registry.json"

# ════════════════════════════════════════
# 花名册查询常量
# ════════════════════════════════════════

WHO_OPTIONS = ["👑 老大", "👨‍👩‍👧 家人", "🤖 数字人格"]

LAYER_OPTIONS = [
    "L0·真人", "P00·元认知", "P01-P07·核心",
    "P08-P09·技能", "P10-P18·古圣/扩展", "P53·特殊(墓碑)",
    "P72·共生体", "P77·军团级", "PF·功能人格", "L2·历史人物",
]

TRUST_OPTIONS = ["L5", "L4", "L3", "L2", "L1", "L0"]

GROUP_OPTIONS = [
    "sovereign", "strategic", "core", "exec",
    "platform", "qiaojie", "xiaoyi", "guardian", "planned",
]

# ════════════════════════════════════════
# 主类
# ════════════════════════════════════════

class 家族花名册:
    """
    龍魂家族花名册统一查询接口
    
    零破坏兼容: 不修改 persona_registry.json / ipa_unified_router.py，
    在中间层提供统一查询。现有代码 import 本模块即可获得花名册能力。
    """
    
    DNA = "#龍芯⚡️丙午·乙未·丁巳·未时·睽-FAMILY-ROSTER-ADAPTER-v2.0"
    
    def __init__(self, roster_path: Optional[Path] = None):
        self._roster_path = roster_path or ROSTER_PATH
        self._registry_path = REGISTRY_PATH
        self._data: Dict[str, Any] = {}
        self._personas: Dict[str, Dict[str, Any]] = {}
        self._loaded = False
        self._diff_cache: Optional[Dict[str, Any]] = None
        
        # 自动加载
        self._加载()
    
    # ════════════════════════════════════
    # 加载
    # ════════════════════════════════════
    
    def _加载(self):
        """加载统一花名册 JSON"""
        if self._loaded:
            return
        
        try:
            with open(self._roster_path, encoding='utf-8') as f:
                self._data = json.load(f)
            self._personas = self._data.get("personas", {})
            self._loaded = True
        except FileNotFoundError:
            print(f"⚠️ 花名册文件不存在: {self._roster_path}")
            print(f"   请先运行: python3 bin/_build_unified_roster.py")
            self._personas = {}
        except json.JSONDecodeError as e:
            print(f"⚠️ 花名册 JSON 解析错误: {e}")
            self._personas = {}
    
    @property
    def 总数(self) -> int:
        return len(self._personas)
    
    @property
    def 元信息(self) -> Dict[str, Any]:
        return self._data.get("_meta", {})
    
    # ════════════════════════════════════
    # 核心查询
    # ════════════════════════════════════
    
    def 查(self, code_or_name: str) -> Optional[Dict[str, Any]]:
        """
        查询一个人格 — 接受代码或名称
        
        Args:
            code_or_name: 人格代码(P03)或规范名称(雯雯)或别名(墨子)
        
        Returns:
            人格完整信息，或 None
        """
        self._加载()
        
        # 直接代码匹配
        if code_or_name in self._personas:
            return self._personas[code_or_name]
        
        # 别名匹配
        输入 = code_or_name.strip()
        for code, entry in self._personas.items():
            if entry.get("canonical_name") == 输入:
                return entry
            for alias in entry.get("aliases", []):
                if alias == 输入:
                    return entry
        
        # 模糊匹配
        for code, entry in self._personas.items():
            if 输入.lower() in code.lower():
                return entry
            for alias in entry.get("aliases", []):
                if 输入.lower() in alias.lower():
                    return entry
        
        return None
    
    def 查字段(self, code: str, 字段: str) -> Any:
        """查单个人格的单个字段"""
        entry = self.查(code)
        if entry:
            return entry.get(字段)
        return None
    
    def 查规范名(self, code: str) -> str:
        """代码 → 规范名称"""
        entry = self.查(code)
        return entry["canonical_name"] if entry else code
    
    def 查别名(self, code: str) -> List[str]:
        """代码 → 所有别名"""
        entry = self.查(code)
        return entry.get("aliases", []) if entry else []
    
    def 查层级(self, code: str) -> str:
        """代码 → 人格层级"""
        entry = self.查(code)
        return entry.get("persona_layer", "") if entry else ""
    
    def 查信任(self, code: str) -> str:
        """代码 → 信任等级"""
        entry = self.查(code)
        return entry.get("trust_level", "") if entry else ""
    
    def 查家族组(self, code: str) -> str:
        """代码 → 家族组"""
        entry = self.查(code)
        return entry.get("family_group", "") if entry else ""
    
    def 查是谁(self, code: str) -> str:
        """代码 → 是谁 (老大/家人/数字人格)"""
        entry = self.查(code)
        return entry.get("who", "") if entry else ""
    
    # ════════════════════════════════════
    # 批量查询
    # ════════════════════════════════════
    
    def 按组查(self, group: str) -> List[Dict[str, Any]]:
        """查询某个家族组的全部成员"""
        self._加载()
        return sorted(
            [e for e in self._personas.values() if e.get("family_group") == group],
            key=lambda x: x.get("code", "")
        )
    
    def 按信任查(self, trust: str) -> List[Dict[str, Any]]:
        """按信任等级筛选"""
        self._加载()
        return sorted(
            [e for e in self._personas.values() if e.get("trust_level") == trust],
            key=lambda x: x.get("code", "")
        )
    
    def 按层级查(self, layer: str) -> List[Dict[str, Any]]:
        """按人格层级筛选"""
        self._加载()
        return sorted(
            [e for e in self._personas.values() if e.get("persona_layer") == layer],
            key=lambda x: x.get("code", "")
        )
    
    def 按是谁查(self, who: str) -> List[Dict[str, Any]]:
        """按'是谁'筛选"""
        self._加载()
        return sorted(
            [e for e in self._personas.values() if e.get("who") == who],
            key=lambda x: x.get("code", "")
        )
    
    def 按来源查(self, source_key: str) -> List[Dict[str, Any]]:
        """按数据来源筛选 (persona_registry / ipa_router)"""
        self._加载()
        result = []
        for e in self._personas.values():
            src = e.get("source", {})
            if src.get(source_key):
                result.append(e)
        return sorted(result, key=lambda x: x.get("code", ""))
    
    # ════════════════════════════════════
    # 全景视图
    # ════════════════════════════════════
    
    def 全景(self) -> Dict[str, Any]:
        """返回花名册全景概览"""
        self._加载()
        
        按组 = defaultdict(list)
        按层级 = defaultdict(list)
        按信任 = defaultdict(list)
        按是谁 = defaultdict(list)
        
        for e in self._personas.values():
            按组[e.get("family_group", "?")].append(e["code"])
            按层级[e.get("persona_layer", "?")].append(e["code"])
            按信任[e.get("trust_level", "?")].append(e["code"])
            按是谁[e.get("who", "?")].append(e["code"])
        
        return {
            "总人格数": self.总数,
            "元信息": self.元信息,
            "按家族组": {k: {"名称": self.元信息.get("_meta", {}).get("family_group_full", k), "数量": len(v), "成员": v} for k, v in sorted(按组.items())},
            "按层级": {k: {"数量": len(v), "成员": v} for k, v in sorted(按层级.items())},
            "按信任": {k: {"数量": len(v), "成员": v} for k, v in sorted(按信任.items())},
            "按是谁": {k: {"数量": len(v)} for k, v in sorted(按是谁.items())},
            "dna": self.DNA,
        }
    
    def 全列表(self) -> List[Dict[str, Any]]:
        """返回所有人格的简化列表 (code + 规范名 + 层级 + 信任)"""
        self._加载()
        return sorted([
            {
                "code": e["code"],
                "name": e["canonical_name"],
                "who": e.get("who", ""),
                "layer": e.get("persona_layer", ""),
                "trust": e.get("trust_level", ""),
                "group": e.get("family_group", ""),
                "role": e.get("role", ""),
            }
            for e in self._personas.values()
        ], key=lambda x: x["code"])
    
    # ════════════════════════════════════
    # Diff 差异报告
    # ════════════════════════════════════
    
    def diff报告(self) -> Dict[str, Any]:
        """
        差异报告: 花名册 vs persona_registry.json vs ipa_unified_router.py
        
        首次运行自动触发，也可手动调用。
        """
        if self._diff_cache:
            return self._diff_cache
        
        self._加载()
        issues = []
        warnings = []
        
        # 加载 registry
        try:
            with open(self._registry_path, encoding='utf-8') as f:
                reg = json.load(f)
            reg_personas = reg.get("personas", {})
        except (FileNotFoundError, json.JSONDecodeError):
            reg_personas = {}
        
        # 检查1: 花名册 vs registry 名称一致性
        for code, entry in sorted(self._personas.items()):
            canonical = entry.get("canonical_name", "")
            if code in reg_personas:
                reg_name = reg_personas[code].get("name", "")
                if reg_name != canonical and reg_name not in entry.get("aliases", []):
                    warnings.append({
                        "类型": "名称不一致",
                        "人格": code,
                        "花名册规范名": canonical,
                        "registry名称": reg_name,
                        "建议": f"registry中{code}的name应为'{canonical}'",
                    })
        
        # 检查2: registry有但花名册没有
        for code in reg_personas:
            if code not in self._personas:
                issues.append({
                    "类型": "花名册缺失",
                    "人格": code,
                    "registry名称": reg_personas[code].get("name", ""),
                    "建议": f"将{code}加入花名册",
                })
        
        # 检查3: 花名册有但registry没有
        for code in self._personas:
            if code not in reg_personas:
                warnings.append({
                    "类型": "registry缺失",
                    "人格": code,
                    "花名册规范名": self._personas[code].get("canonical_name", ""),
                    "建议": f"将{code}加入persona_registry.json",
                })
        
        # 检查4: trust_level 异常
        for code, entry in self._personas.items():
            trust = entry.get("trust_level", "")
            if trust == "L0" and entry.get("who") != "👑 老大":
                warnings.append({
                    "类型": "信任异常",
                    "人格": code,
                    "说明": f"{code} trust=L0但who≠老大，可能为规划中人格",
                })
        
        if issues:
            status = "🔴 存在差异需修复"
        elif warnings:
            status = "🟡 有警告"
        else:
            status = "🟢 完全一致"
        
        self._diff_cache = {
            "检测时间": datetime.now().isoformat(),
            "状态": status,
            "问题": issues,
            "警告": warnings,
            "总计": len(issues) + len(warnings),
            "扫描范围": {
                "花名册": len(self._personas),
                "registry": len(reg_personas),
            },
            "dna": self.DNA,
        }
        return self._diff_cache
    
    def 打印diff报告(self):
        """终端友好的 diff 报告输出"""
        report = self.diff报告()
        
        print(f"\n{'='*60}")
        print(f"  🐉 家族花名册 · 差异报告")
        print(f"  {report['检测时间']}")
        print(f"  状态: {report['状态']}")
        print(f"{'='*60}")
        
        if report.get("问题"):
            print(f"\n  🔴 问题 ({len(report['问题'])}):")
            for i, issue in enumerate(report["问题"], 1):
                print(f"  {i}. [{issue['类型']}] {issue.get('人格','?')}: {issue.get('建议','')}")
        
        if report.get("警告"):
            print(f"\n  🟡 警告 ({len(report['警告'])}):")
            for i, w in enumerate(report["警告"][:10], 1):
                print(f"  {i}. [{w['类型']}] {w.get('人格','?')}: {w.get('建议','')}")
            if len(report["警告"]) > 10:
                print(f"  ... 还有 {len(report['警告'])-10} 条")
        
        print(f"\n  扫描: 花名册 {report['扫描范围']['花名册']} 人格 vs registry {report['扫描范围']['registry']} 人格")
        print(f"  DNA: {self.DNA}")
        print()
    
    # ════════════════════════════════════
    # 导出
    # ════════════════════════════════════
    
    def 导出(self, 格式: str = "dict") -> Any:
        """导出花名册"""
        if 格式 == "json":
            return json.dumps(self._data, ensure_ascii=False, indent=2)
        return self._data
    
    def 导出简表(self, 格式: str = "list") -> Any:
        """导出简化列表"""
        if 格式 == "json":
            return json.dumps(self.全列表(), ensure_ascii=False, indent=2)
        return self.全列表()
    
    def 导出按组(self) -> Dict[str, List[str]]:
        """按家族组导出 (组名 → [代码列表])"""
        result: Dict[str, List[str]] = defaultdict(list)
        for e in self._personas.values():
            result[e.get("family_group", "?")].append(e["code"])
        return dict(result)


# ════════════════════════════════════════
# 单例 + 快捷函数
# ════════════════════════════════════════

_实例: Optional[家族花名册] = None

def get_roster() -> 家族花名册:
    """获取花名册单例"""
    global _实例
    if _实例 is None:
        _实例 = 家族花名册()
    return _实例

def 查(code: str) -> Optional[Dict[str, Any]]:
    """快捷查询"""
    return get_roster().查(code)

def 全景() -> Dict[str, Any]:
    """快捷全景"""
    return get_roster().全景()

def diff() -> Dict[str, Any]:
    """快捷diff"""
    return get_roster().diff报告()


# ════════════════════════════════════════
# 直接运行 → diff 报告
# ════════════════════════════════════════

if __name__ == "__main__":
    roster = 家族花名册()
    
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        
        if cmd == "diff":
            roster.打印diff报告()
        elif cmd == "全景" or cmd == "overview":
            import json as _json
            print(_json.dumps(roster.全景(), ensure_ascii=False, indent=2))
        elif cmd == "列表" or cmd == "list":
            for item in roster.全列表():
                print(f"  {item['code']:12s} {item['name']:16s} {item['who']:8s} {item['layer']:20s} {item['trust']:4s} [{item['group']}]")
        elif cmd == "查" and len(sys.argv) > 2:
            result = roster.查(sys.argv[2])
            if result:
                import json as _json
                print(_json.dumps(result, ensure_ascii=False, indent=2))
            else:
                print(f"未找到: {sys.argv[2]}")
        else:
            print(f"未知命令: {cmd}")
            print("用法: python3 family_roster_adapter.py [diff|全景|列表|查 <code>]")
    else:
        # 默认: 打印统计 + diff
        print(f"\n🐉 龍芯家族花名册 · 统一适配器 v2.0")
        print(f"   总人格: {roster.总数}")
        print(f"   DNA: {roster.DNA}")
        print(f"   文件: {roster._roster_path}")
        
        全景数据 = roster.全景()
        print(f"\n   按家族组:")
        for k, v in sorted(全景数据["按家族组"].items()):
            print(f"     {k}: {v['数量']}人格")
        
        roster.打印diff报告()
