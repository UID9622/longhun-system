#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
╔═══════════════════════════════════════════════════════════════════════════╗
║  DNA追溯头（不可删除 · 删除即断链）                                       ║
║  DNA: #龍芯⚡️2026-07-08-ENTANGLEMENT-DETECTOR-v1.0                      ║
║  理论来源: 量子态模块路由·太极五行融合框架 v1.0                            ║
║  创始人: UID9622 · 龍芯北辰 · 诸葛鑫                                      ║
╚═══════════════════════════════════════════════════════════════════════════╝

模块纠缠度检测器
═══════════════
把量子纠缠的数学形式应用于系统模块依赖分析。

核心公式:
  纠缠度 E(ρ_ij) = S(ρ_i) = -Tr(ρ_i log ρ_i)
  
  其中 ρ_i = Tr_j(|ψ_ij⟩⟨ψ_ij|) 是偏迹后的约化密度矩阵
  
  E=0   → 独立（可安全单独修改）
  0<E≤0.3 → 弱耦合
  0.3<E≤0.8 → 中等耦合（需通知）
  E>0.8 → 强耦合（联动感知铁律）

用法:
  python3 bin/lh_entanglement_detector.py --scan          # 扫描所有模块对
  python3 bin/lh_entanglement_detector.py --pair A B      # 检测特定模块对
  python3 bin/lh_entanglement_detector.py --report        # 生成纠缠度报告
"""

import json
import math
import hashlib
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Any, Optional
from collections import defaultdict

try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False

# ═══════════════════════════════════════════════════════════
# 五行耦合矩阵（相生=正耦合，相克=负耦合）
# ═══════════════════════════════════════════════════════════

FIVE_ELEMENTS = ["金", "木", "水", "火", "土"]

# 相生映射
SHENG_MAP = {
    "金": "水",  # 金生水
    "水": "木",  # 水生木
    "木": "火",  # 木生火
    "火": "土",  # 火生土
    "土": "金",  # 土生金
}

# 相克映射
KE_MAP = {
    "金": "木",  # 金克木
    "木": "土",  # 木克土
    "土": "水",  # 土克水
    "水": "火",  # 水克火
    "火": "金",  # 火克金
}

# 元素 → 模块类型映射
ELEMENT_MODULE_MAP: Dict[str, List[str]] = {
    "金": ["审计", "安全", "三色审计", "熔断", "code-audit", "audit", "veto-alert"],
    "木": ["生成", "代码", "CNSH翻译", "semantic-parser", "dna-gen", "cnsh_translator"],
    "水": ["存储", "数据", "知识图谱", "数据层", "记忆", "执行记录", "wuxing-guard"],
    "火": ["通信", "API", "MCP", "网关", "control-panel", "dashboard", "shengying"],
    "土": ["协调", "枢纽", "联动感知", "cross_module", "route-find", "on-execute", "gatekeeper"],
}


def detect_element(module_name: str) -> str:
    """根据模块名中的关键词判定五行属性"""
    module_lower = module_name.lower()
    scores = defaultdict(float)
    for element, keywords in ELEMENT_MODULE_MAP.items():
        for kw in keywords:
            if kw.lower() in module_lower:
                scores[element] += 1.0
    if not scores:
        return "土"  # 默认归属土（枢纽）
    return max(scores, key=scores.get)


def coupling_constant(elem_i: str, elem_j: str) -> float:
    """计算两个五行元素之间的耦合常数"""
    if elem_i == elem_j:
        return 0.0  # 同元素无直接相生相克
    
    g = 0.1  # 基础耦合强度
    
    if SHENG_MAP.get(elem_i) == elem_j:
        return g  # i生j → 建设性耦合
    if SHENG_MAP.get(elem_j) == elem_i:
        return g  # j生i → 建设性耦合
    
    if KE_MAP.get(elem_i) == elem_j:
        return -g  # i克j → 破坏性耦合
    if KE_MAP.get(elem_j) == elem_i:
        return -g  # j克i → 破坏性耦合
    
    return 0.0  # 无直接五行关系


class ModuleDependencyAnalyzer:
    """分析模块间的依赖关系，计算量子纠缠度"""
    
    DNA = "#龍芯⚡️2026-07-08-ENTANGLEMENT-DETECTOR-v1.0"
    
    def __init__(self, project_root: Optional[str] = None):
        self.root = Path(project_root) if project_root else Path(__file__).parent.parent
        self.modules: Dict[str, Dict[str, Any]] = {}
        self.entanglement_cache: Dict[Tuple[str, str], Dict[str, Any]] = {}
        self.elements: Dict[str, str] = {}  # 模块名 → 五行属性
        
    def scan_module_structure(self):
        """扫描项目结构，识别模块"""
        # L1 内核层模块
        self._scan_directory(self.root / "L1_内核层", "L1")
        # L2 技能层模块
        self._scan_directory(self.root / "L2_技能层", "L2")
        # L5 服务层模块
        self._scan_directory(self.root / "L5_服务层", "L5")
        # L6 集成层模块
        self._scan_directory(self.root / "L6_集成层", "L6")
        # L7 数据层模块
        self._scan_directory(self.root / "L7_数据层", "L7")
        # L8 治理层模块
        self._scan_directory(self.root / "L8_治理层", "L8")
        # L9 子系统模块
        self._scan_directory(self.root / "L9_子系统", "L9")
        # bin/ 脚本模块
        self._scan_directory(self.root / "bin", "BIN")
        
        # 特殊文件
        special_files = [
            ("AGENTS.md", "AGENTS"),
            ("CONSTITUTION.md", "CONSTITUTION"),
            ("CNSH-PROTOCOL.md", "CNSH-PROTOCOL"),
            ("CNSH-GATEKEEPER.md", "CNSH-GATEKEEPER"),
        ]
        for fname, label in special_files:
            fpath = self.root / fname
            if fpath.exists():
                self.modules[label] = {
                    "name": label,
                    "path": str(fpath),
                    "type": "governance",
                    "dependencies": self._extract_dependencies(fpath),
                    "element": detect_element(label),
                }
    
    def _scan_directory(self, directory: Path, prefix: str):
        """扫描目录下的文件作为模块"""
        if not directory.exists():
            return
        for item in sorted(directory.rglob("*")):
            if item.is_file() and item.suffix in (".py", ".md", ".json", ".yaml", ".jsonl"):
                rel = item.relative_to(directory)
                module_name = f"{prefix}/{rel}"
                self.modules[module_name] = {
                    "name": module_name,
                    "path": str(item),
                    "type": self._classify_type(item),
                    "dependencies": self._extract_dependencies(item),
                    "element": detect_element(str(rel)),
                }
                self.elements[module_name] = self.modules[module_name]["element"]
    
    def _classify_type(self, path: Path) -> str:
        """判定文件类型"""
        if path.suffix == ".py":
            return "executable"
        elif path.suffix == ".md":
            return "document"
        elif path.suffix == ".json" or path.suffix == ".jsonl":
            return "data"
        elif path.suffix == ".yaml":
            return "config"
        return "other"
    
    def _extract_dependencies(self, path: Path) -> List[str]:
        """从文件中提取依赖（import/引用）"""
        deps = []
        try:
            content = path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            return deps
        
        # Python 文件的 import 依赖
        if path.suffix == ".py":
            import re
            imports = re.findall(r'(?:from|import)\s+[\w.]+', content)
            for imp in imports:
                deps.append(imp)
        
        # Markdown 文件的引用依赖
        if path.suffix == ".md":
            # 检测 [[link]] 和 [text](link) 格式
            import re
            links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', content)
            for _, link in links:
                if not link.startswith("http"):
                    deps.append(link)
        
        return deps[:20]  # 限制数量
    
    def compute_shared_dependency_score(self, deps_i: List[str], deps_j: List[str]) -> float:
        """计算两个模块的共享依赖分数（Jaccard相似度）"""
        set_i = set(self._normalize_dep(d) for d in deps_i)
        set_j = set(self._normalize_dep(d) for d in deps_j)
        
        if not set_i or not set_j:
            return 0.0
        
        intersection = len(set_i & set_j)
        union = len(set_i | set_j)
        return intersection / union if union > 0 else 0.0
    
    @staticmethod
    def _normalize_dep(dep: str) -> str:
        """标准化依赖名"""
        return dep.strip().lower().replace("_", "").replace("-", "").replace(".", "")
    
    def entanglement_degree(self, module_i: str, module_j: str) -> Dict[str, Any]:
        """计算两个模块之间的量子纠缠度"""
        cache_key = tuple(sorted([module_i, module_j]))
        if cache_key in self.entanglement_cache:
            return self.entanglement_cache[cache_key]
        
        mi = self.modules.get(module_i, {})
        mj = self.modules.get(module_j, {})
        
        deps_i = mi.get("dependencies", [])
        deps_j = mj.get("dependencies", [])
        elem_i = mi.get("element", "土")
        elem_j = mj.get("element", "土")
        
        # ① 共享依赖分数 (Jaccard)
        jaccard = self.compute_shared_dependency_score(deps_i, deps_j)
        
        # ② 五行耦合分数
        coupling = abs(coupling_constant(elem_i, elem_j)) * 10  # 放大到0~1区间
        
        # ③ 直接引用分数
        name_i_norm = self._normalize_dep(module_i.split("/")[-1] if "/" in module_i else module_i)
        name_j_norm = self._normalize_dep(module_j.split("/")[-1] if "/" in module_j else module_j)
        
        direct_ij = any(name_j_norm in self._normalize_dep(d) for d in deps_i)
        direct_ji = any(name_i_norm in self._normalize_dep(d) for d in deps_j)
        direct_score = 0.3 if direct_ij or direct_ji else 0.0
        if direct_ij and direct_ji:
            direct_score = 0.5  # 相互引用
        
        # ④ 综合纠缠度
        # 权重: Jaccard 0.4 + Coupling 0.3 + Direct 0.3
        raw_e = jaccard * 0.4 + coupling * 0.3 + direct_score * 0.3
        raw_e = min(1.0, max(0.0, raw_e))
        
        # ⑤ 应用非线性 Sigmoid 映射（让中等值更有区分度）
        if raw_e > 0:
            # 把Jaccard低值放大
            e = 1.0 / (1.0 + math.exp(-10 * (raw_e - 0.3)))
        else:
            e = 0.0
        
        result = {
            "module_i": module_i,
            "module_j": module_j,
            "element_i": elem_i,
            "element_j": elem_j,
            "jaccard_similarity": round(jaccard, 4),
            "wuxing_coupling": round(coupling, 4),
            "direct_reference": direct_ij or direct_ji,
            "entanglement_degree": round(e, 4),
            "entanglement_level": self._entanglement_level(e),
            "wuxing_relation": self._wuxing_relation(elem_i, elem_j),
        }
        
        self.entanglement_cache[cache_key] = result
        return result
    
    @staticmethod
    def _entanglement_level(e: float) -> str:
        if e > 0.8:
            return "🔴 强耦合 (联动感知铁律)"
        elif e > 0.3:
            return "🟡 中等耦合 (需通知对方)"
        elif e > 0.05:
            return "🟢 弱耦合 (可独立修改)"
        else:
            return "⚪ 独立 (无纠缠)"
    
    def _wuxing_relation(self, elem_i: str, elem_j: str) -> str:
        """描述五行关系"""
        if elem_i == elem_j:
            return "同相"
        if SHENG_MAP.get(elem_i) == elem_j:
            return f"{elem_i}生{elem_j} (建设性)"
        if SHENG_MAP.get(elem_j) == elem_i:
            return f"{elem_j}生{elem_i} (建设性)"
        if KE_MAP.get(elem_i) == elem_j:
            return f"{elem_i}克{elem_j} (约束性)"
        if KE_MAP.get(elem_j) == elem_i:
            return f"{elem_j}克{elem_i} (约束性)"
        return "无直接关系"
    
    def scan_all_pairs(self, top_n: int = 50) -> List[Dict[str, Any]]:
        """扫描所有模块对，返回纠缠度最高的 top_n 对"""
        self.scan_module_structure()
        
        module_names = list(self.modules.keys())
        results = []
        
        total_pairs = len(module_names) * (len(module_names) - 1) // 2
        count = 0
        
        for i in range(len(module_names)):
            for j in range(i + 1, len(module_names)):
                count += 1
                if count % 1000 == 0:
                    print(f"  进度: {count}/{total_pairs} ({count*100/total_pairs:.1f}%)")
                
                result = self.entanglement_degree(module_names[i], module_names[j])
                if result["entanglement_degree"] > 0.01:  # 只保留有意义的结果
                    results.append(result)
        
        results.sort(key=lambda x: x["entanglement_degree"], reverse=True)
        return results[:top_n]
    
    def report(self) -> Dict[str, Any]:
        """生成完整报告"""
        strong = [r for r in self.entanglement_cache.values() if r["entanglement_degree"] > 0.8]
        medium = [r for r in self.entanglement_cache.values() if 0.3 < r["entanglement_degree"] <= 0.8]
        weak = [r for r in self.entanglement_cache.values() if 0.05 < r["entanglement_degree"] <= 0.3]
        
        # 五行统计
        element_stats = defaultdict(int)
        for elem in self.elements.values():
            element_stats[elem] += 1
        
        # 基于密度矩阵的熵计算
        avg_entanglement = 0.0
        vals = [r["entanglement_degree"] for r in self.entanglement_cache.values() if r["entanglement_degree"] > 0]
        if vals:
            avg_entanglement = sum(vals) / len(vals)
        
        return {
            "dna": self.DNA,
            "timestamp": datetime.now().isoformat(),
            "total_modules": len(self.modules),
            "total_pairs_scanned": len(self.entanglement_cache),
            "strong_coupling": len(strong),
            "medium_coupling": len(medium),
            "weak_coupling": len(weak),
            "average_entanglement": round(avg_entanglement, 4),
            "system_entropy": round(-avg_entanglement * math.log(max(avg_entanglement, 1e-10)) if avg_entanglement > 0 else 0, 4),
            "five_elements_distribution": dict(element_stats),
            "top_entangled_pairs": sorted(
                [r for r in self.entanglement_cache.values() if r["entanglement_degree"] > 0.5],
                key=lambda x: x["entanglement_degree"],
                reverse=True
            )[:20],
        }


def main():
    parser = argparse.ArgumentParser(description="龍魂量子纠缠度检测器")
    parser.add_argument("--scan", "-s", action="store_true", help="扫描所有模块对")
    parser.add_argument("--pair", "-p", nargs=2, metavar=("A", "B"), help="检测特定模块对")
    parser.add_argument("--report", "-r", action="store_true", help="生成纠缠度报告")
    parser.add_argument("--top", "-t", type=int, default=20, help="显示前N个高纠缠对")
    parser.add_argument("--json", "-j", action="store_true", help="JSON输出")
    parser.add_argument("--project-root", default=None, help="项目根目录")
    args = parser.parse_args()
    
    analyzer = ModuleDependencyAnalyzer(project_root=args.project_root)
    
    if args.pair:
        a, b = args.pair
        # 模糊匹配模块名
        all_modules = list(analyzer.modules.keys()) if not analyzer.modules else []
        # 先扫描
        analyzer.scan_module_structure()
        
        # 查找匹配模块
        a_match = [m for m in analyzer.modules if a.lower() in m.lower()]
        b_match = [m for m in analyzer.modules if b.lower() in m.lower()]
        
        if not a_match:
            print(f"未找到匹配 '{a}' 的模块")
            return
        if not b_match:
            print(f"未找到匹配 '{b}' 的模块")
            return
        
        for am in a_match[:3]:
            for bm in b_match[:3]:
                if am != bm:
                    result = analyzer.entanglement_degree(am, bm)
                    if args.json:
                        print(json.dumps(result, ensure_ascii=False, indent=2))
                    else:
                        print(f"\n{'='*60}")
                        print(f"  {am}")
                        print(f"  {bm}")
                        print(f"  纠缠度: {result['entanglement_degree']:.4f} {result['entanglement_level']}")
                        print(f"  五行: {result['element_i']} {result['wuxing_relation']} {result['element_j']}")
                        print(f"  Jaccard: {result['jaccard_similarity']:.4f}  直接引用: {result['direct_reference']}")
        return
    
    if args.report or args.scan:
        print("⚛️  龍魂量子纠缠度检测器 v1.0")
        print(f"DNA: {analyzer.DNA}")
        print(f"扫描模块结构中...")
        
        results = analyzer.scan_all_pairs(top_n=max(args.top, 50))
        report = analyzer.report()
        
        if args.json:
            print(json.dumps(report, ensure_ascii=False, indent=2))
        else:
            print(f"\n{'='*60}")
            print(f"📊 系统纠缠度报告")
            print(f"{'='*60}")
            print(f"  总模块数: {report['total_modules']}")
            print(f"  已扫描模块对: {report['total_pairs_scanned']}")
            print(f"  🔴 强耦合: {report['strong_coupling']}")
            print(f"  🟡 中等耦合: {report['medium_coupling']}")
            print(f"  🟢 弱耦合: {report['weak_coupling']}")
            print(f"  平均纠缠度: {report['average_entanglement']:.4f}")
            print(f"  系统熵: {report['system_entropy']:.4f}")
            
            print(f"\n{'='*60}")
            print(f"📊 五行分布")
            print(f"{'='*60}")
            for elem in FIVE_ELEMENTS:
                count = report['five_elements_distribution'].get(elem, 0)
                bar = "█" * min(count, 40)
                print(f"  {elem}: {count:>4} {bar}")
            
            print(f"\n{'='*60}")
            print(f"🔗 最强纠缠模块对 (Top {args.top})")
            print(f"{'='*60}")
            for i, r in enumerate(results[:args.top], 1):
                e_bar = "█" * int(r["entanglement_degree"] * 30)
                print(f"\n  [{i}] E={r['entanglement_degree']:.4f} {r['entanglement_level']} {e_bar}")
                print(f"      {r['module_i']}")
                print(f"      {r['module_j']}")
                print(f"      五行: {r['element_i']} {r['wuxing_relation']} {r['element_j']}")
        
        # 输出警告
        strong_count = report['strong_coupling']
        if strong_count > 5:
            print(f"\n⚠️  检测到 {strong_count} 对强耦合模块对，建议分解大模块以降低系统纠缠度")
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
