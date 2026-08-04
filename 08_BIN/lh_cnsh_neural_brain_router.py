#!/usr/bin/env python3
# DNA: #龍芯⚡️丙午·丙申·庚戌·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
#龍芯⚡️丙午·丙申·癸酉·庚申·临-LH_CNSH_NEURAL_BRAIN_ROUTER-v1.0-d3ccdb94
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║           CNSH神经网络翻译引擎 · 智能路由中枢 (前额叶) v1.0                    ║
║         8大脑区→8个人格映射 · 动态路径生成 · 双向反馈 · 并行执行               ║
╚══════════════════════════════════════════════════════════════════════════════╝

DNA: #龙芯⚡️丙午·丙申·丙辰·未时·需-CNSH-NEURAL-BRAIN-ROUTER-v1.0
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
架构: 8脑区 → P01/P02/P03/P04/P05/P06/P07/P18 人格映射

四条路径:
  PATH_FAST    — 有DNA且高质量 → <1s 极速通道
  PATH_STANDARD — 质量中等 → 2-5s 标准路径
  PATH_DEEP    — 可疑或高复杂度 → 10-30s 深度分析
  PATH_OPTIMIZE — 质量差 → 5-10s 优化增强
"""

import json
import os
import sys
import hashlib
import time
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum

# ── 路径常量 ──────────────────────────────────────────────────────────────────

class Path(Enum):
    FAST = "PATH_FAST"
    STANDARD = "PATH_STANDARD"
    DEEP = "PATH_DEEP"
    OPTIMIZE = "PATH_OPTIMIZE"
    NATURAL_LANG = "PATH_NATURAL_LANG"

# ── 特征数据 ──────────────────────────────────────────────────────────────────

@dataclass
class InputFeatures:
    """感知层提取的输入特征"""
    language: str = "unknown"           # 编程语言 或 natural_language
    quality_score: int = 50             # 代码品质 0-100
    complexity_score: int = 50          # 复杂度 0-100
    suspicious_score: int = 0           # 可疑度 0-100
    has_dna: bool = False               # 是否有DNA追溯码
    dna_code: Optional[str] = None      # DNA追溯码内容
    input_type: str = "unknown"         # code / natural_language / mixed
    code_length: int = 0                # 代码行数
    imports_found: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "language": self.language,
            "quality_score": self.quality_score,
            "complexity_score": self.complexity_score,
            "suspicious_score": self.suspicious_score,
            "has_dna": self.has_dna,
            "input_type": self.input_type,
            "code_length": self.code_length
        }


# ═══════════════════════════════════════════════════════════════════════════════
# 感知层 (Perception Layer)
# ═══════════════════════════════════════════════════════════════════════════════

class PerceptionLayer:
    """感知层：快速扫描输入特征，为路由决策提供依据"""

    # 语言关键词映射（使用正则确保词边界匹配）
    LANG_PATTERNS: Dict[str, List[str]] = {
        "python":    [
            r"\bdef\s+\w+\s*\(", r"\bimport\s+\w+", r"\bclass\s+\w+.*:", r"\bself\.",
            r"\b__init__\b", r"\bprint\(", r"\bfrom\s+\w+\s+import",
            r"\breturn\b", r"=\s*\w+", r"f[\"']",  # 基基代码特征
            r"\.\w+\(.+"   # 方法调用
        ],
        "javascript": [r"\bfunction\s+\w+\s*\(", r"\bconst\s+\w+\s*=", r"\blet\s+\w+\s*=", r"=>\s*\{", r"\bconsole\.log\(", r"\brequire\("],
        "typescript": [r":\s*string\b", r":\s*number\b", r"\binterface\s+\w+", r"\bexport\s+(interface|type|class)", r"\bimport\s+\{"],
        "java":      [r"\bpublic\s+class\s+\w+", r"\bprivate\s+\w+\s+\w+", r"\bSystem\.out\.print", r"\bextends\s+\w+"],
        "cpp":       [r"#include\s*<", r"std::\w+", r"\bint\s+main\s*\(", r"->\s*\w+", r"\btemplate\s*<"],
        "go":        [r"\bfunc\s+\w+\s*\(.*\)", r"\bpackage\s+\w+", r"fmt\.\w+", r"\bdefer\s+"],
        "rust":      [r"\bfn\s+\w+\s*\(.*\)", r"\blet\s+mut\s+", r"\buse\s+\w+::", r"\bimpl\s+\w+", r"\bpub\s+fn"],
        "shell":     [r"#!/bin/", r"\bexport\s+\w+=", r"\bsource\s+", r"\bfi\b", r"\bdone\b", r"\besac\b"],
        "c":         [r"#include\s*<", r"\bprintf\(", r"\bscanf\(", r"\bmalloc\(", r"->\s*\w+"],
    }

    DNA_PATTERNS = ["#ZHUGEXIN⚡️", "#龙芯⚡️", "dna追溯码", "DNA追溯码"]

    SUSPICIOUS_MARKERS: List[str] = [
        "TODO:", "placeholder", "stub", "FIXME", "HACK:",
        "pseudocode", "伪代码", "示例代码", "// ...", "# ...",
        "var1", "var2", "temp", "xxx", "test_function"
    ]

    @classmethod
    def scan(cls, code: str) -> InputFeatures:
        """扫描输入代码，返回特征"""
        features = InputFeatures()
        features.code_length = len(code.split('\n'))

        # 1. 检测语言
        features.language = cls._detect_language(code)

        # 2. 检测输入类型
        if features.language in ("unknown",):
            features.input_type = "natural_language"
        elif features.language == "unknown_code":
            features.input_type = "code"
            features.language = "unknown"  # 归一化
        else:
            features.input_type = "code"

        # 3. 检测DNA
        for pattern in cls.DNA_PATTERNS:
            if pattern in code:
                features.has_dna = True
                # 提取DNA码
                idx = code.find(pattern)
                end = code.find('\n', idx) if idx != -1 else -1
                if end == -1:
                    end = min(idx + 120, len(code))
                features.dna_code = code[idx:end].strip()
                break

        # 4. 评估品质
        features.quality_score = cls._assess_quality(code, features)

        # 5. 评估复杂度
        features.complexity_score = cls._assess_complexity(code, features)

        # 6. 评估可疑度
        features.suspicious_score = cls._assess_suspicious(code)

        # 7. 提取导入语句
        features.imports_found = cls._extract_imports(code, features.language)

        return features

    @classmethod
    def _detect_language(cls, code: str) -> str:
        """检测编程语言（使用正则匹配）"""
        import re
        scores: Dict[str, int] = {}
        for lang, patterns in cls.LANG_PATTERNS.items():
            score = sum(1 for p in patterns if re.search(p, code))
            if score > 0:
                scores[lang] = score

        if not scores:
            # 後备：检查是否有基基代码特征（賦值、函数调用、语句结构）
            code_patterns = [
                r'^\s*\w+\s*=\s*',           # 賦值语句
                r'^\s*\w+\.\w+\(',            # 方法调用
                r'^\s*def\s+\w+\s*\(',        # 函数定义
                r'^\s*return\b',               # return语句
            ]
            if any(re.search(p, code, re.MULTILINE) for p in code_patterns):
                return "unknown_code"  # 有代码特征但语言不明
            return "unknown"

        best = max(scores, key=scores.get)
        if scores[best] >= 1:
            return best
        return "unknown"

    @classmethod
    def _assess_quality(cls, code: str, features: InputFeatures) -> int:
        """评估代码品质 (0-100)"""
        quality = 70  # 默认中等
        lines = code.split('\n')

        # 加分項
        if features.has_dna:
            quality += 15
        if features.imports_found:
            quality += 5
        if any("def " in l or "class " in l or "function " in l for l in lines):
            quality += 5

        # 扣分項
        todo_count = sum(1 for l in lines if "TODO" in l or "FIXME" in l or "HACK" in l)
        quality -= todo_count * 5

        empty_lines = sum(1 for l in lines if l.strip() == "")
        if empty_lines / max(len(lines), 1) > 0.4:
            quality -= 10

        if features.code_length < 3:
            quality -= 20

        return max(0, min(100, quality))

    @classmethod
    def _assess_complexity(cls, code: str, features: InputFeatures) -> int:
        """评估代码复杂度 (0-100)"""
        complexity = 30  # 默认低复杂度
        lines = code.split('\n')

        # 控制流嵌套
        indent_levels = [len(l) - len(l.lstrip()) for l in lines if l.strip()]
        if indent_levels:
            avg_indent = sum(indent_levels) / len(indent_levels)
            complexity += int(min(avg_indent * 2, 30))

        # 函数数量
        func_count = sum(1 for l in lines if "def " in l or "function " in l or "fn " in l)
        complexity += min(func_count * 3, 20)

        # 代码长度
        complexity += min(features.code_length // 10, 20)

        return max(0, min(100, complexity))

    @classmethod
    def _assess_suspicious(cls, code: str) -> int:
        """评估可疑度 (0-100)"""
        score = 0
        code_lower = code.lower()

        for marker in cls.SUSPICIOUS_MARKERS:
            if marker.lower() in code_lower:
                score += 15

        # 不存在的库函数检测（簡单启发式）
        if "import" in code:
            # 检查是否有可疑的导入
            if any(q in code for q in ["libdoesnotexist", "fakelib", "mocklib"]):
                score += 30

        return max(0, min(100, score))

    @classmethod
    def _extract_imports(cls, code: str, language: str) -> List[str]:
        """提取导入语句"""
        imports = []
        lines = code.split('\n')
        for line in lines:
            stripped = line.strip()
            if language == "python" and stripped.startswith(("import ", "from ")):
                imports.append(stripped)
            elif language in ("javascript", "typescript") and stripped.startswith(("import ", "require(")):
                imports.append(stripped)
            elif language in ("cpp", "c") and stripped.startswith("#include"):
                imports.append(stripped)
            elif language == "go" and stripped.startswith("import"):
                imports.append(stripped)
            elif language == "rust" and stripped.startswith("use "):
                imports.append(stripped)
        return imports


# ═══════════════════════════════════════════════════════════════════════════════
# 决策引擎 (Decision Engine)
# ═══════════════════════════════════════════════════════════════════════════════

class DecisionEngine:
    """决策引擎：根据输入特征选择最优路径"""

    # 加载脑区映射
    _brain_map: Optional[Dict] = None

    @classmethod
    def load_brain_map(cls) -> Dict[str, Any]:
        if cls._brain_map is None:
            config_path = os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                "config", "cnsh_neural_brain_map.json"
            )
            try:
                with open(config_path) as f:
                    cls._brain_map = json.load(f)
            except FileNotFoundError:
                cls._brain_map = cls._fallback_brain_map()
        return cls._brain_map

    @classmethod
    def _fallback_brain_map(cls) -> Dict[str, Any]:
        return {
            "brains": {
                f"B{i}": {"persona": f"P0{i}" if i < 8 else f"P{i+10}"}
                for i in range(1, 9)
            }
        }

    DANGEROUS_PATTERNS: List[str] = [
        r'\bos\.system\(', r'\bsubprocess\.', r'\beval\(', r'\bexec\(',
        r'password\s*=\s*["\']', r'api_key\s*=\s*["\']', r'secret\s*=\s*["\']',
        r'\brm\s+-rf\b', r'\bDROP\s+TABLE\b', r'\bDELETE\s+FROM\b',
    ]

    @classmethod
    def _has_dangerous(cls, code: str) -> bool:
        import re
        return any(re.search(p, code, re.IGNORECASE) for p in cls.DANGEROUS_PATTERNS)

    @classmethod
    def route(cls, features: InputFeatures, code: str = "") -> Dict[str, Any]:
        """
        路由决策：根据特征返回最佳路径

        规则:
          1. 有DNA且质量高 → PATH_FAST (<1s)
          2. 自然语言 → PATH_NATURAL_LANG (1-3s)
          3. 可疑度>60 或 危险代码 → PATH_DEEP (10-30s)
          4. 复杂度>80 → PATH_DEEP (10-30s)
          5. 质量<40 → PATH_OPTIMIZE (5-10s)
          6. 默认 → PATH_STANDARD (2-5s)
        """
        brain_map = cls.load_brain_map()
        routing_paths = brain_map.get("routing_paths", {})

        decision = {
            "path": Path.STANDARD.value,
            "path_name": "标准代码路径",
            "brains": [],
            "parallel_brains": [],
            "expected_time": "2-5s",
            "reason": "默认标准路径"
        }

        # 规则1: 有DNA且质量高 → 极速通道
        if features.has_dna and features.quality_score >= 80:
            path = routing_paths.get("PATH_FAST", {})
            decision.update({
                "path": Path.FAST.value,
                "path_name": "极速通道",
                "brains": ["B8", "B4"],
                "parallel_brains": ["B7"],
                "expected_time": "<1s",
                "reason": f"检测到DNA追溯码且质量分{features.quality_score}≥80，走极速通道"
            })
            return decision

        # 规则2: 自然语言 → 自然语言翻译
        if features.input_type == "natural_language":
            path = routing_paths.get("PATH_NATURAL_LANG", {})
            decision.update({
                "path": Path.NATURAL_LANG.value,
                "path_name": "自然语言翻译",
                "brains": ["B4"],
                "parallel_brains": [],
                "expected_time": "1-3s",
                "reason": f"输入类型=自然语言，走通心译直达"
            })
            return decision

        # 规则3: 可疑度>60 或 危险代码 → 深度分析
        if features.suspicious_score >= 60 or (code and cls._has_dangerous(code)):
            path = routing_paths.get("PATH_DEEP", {})
            danger_note = " · 检测到危险模式" if code and cls._has_dangerous(code) else ""
            decision.update({
                "path": Path.DEEP.value,
                "path_name": "深度分析路径",
                "brains": ["B1", "B2", "B3", "B4", "B5", "B7"],
                "parallel_brains": ["B7"],
                "expected_time": "10-30s",
                "reason": f"可疑度{features.suspicious_score}≥60{danger_note}，强制走深度分析+AI鉴定+来源追溯"
            })
            return decision

        # 规则4: 复杂度>80 → 深度分析
        if features.complexity_score >= 80:
            path = routing_paths.get("PATH_DEEP", {})
            decision.update({
                "path": Path.DEEP.value,
                "path_name": "深度分析路径",
                "brains": ["B1", "B4", "B5", "B7"],
                "parallel_brains": ["B5"],
                "expected_time": "10-30s",
                "reason": f"复杂度{features.complexity_score}≥80，需数学验证+并行性能分析"
            })
            return decision

        # 规则5: 质量<40 → 优化增强
        if features.quality_score < 40:
            path = routing_paths.get("PATH_OPTIMIZE", {})
            decision.update({
                "path": Path.OPTIMIZE.value,
                "path_name": "优化增强路径",
                "brains": ["B1", "B6", "B4", "B7"],
                "parallel_brains": [],
                "expected_time": "5-10s",
                "reason": f"质量分{features.quality_score}<40，需要代码优化"
            })
            return decision

        # 默认: 标准路径
        path = routing_paths.get("PATH_STANDARD", {})
        decision.update({
            "path": Path.STANDARD.value,
            "path_name": "标准代码路径",
            "brains": ["B1", "B4", "B7"],
            "parallel_brains": [],
            "expected_time": "2-5s",
            "reason": f"质量{features.quality_score}·可疑{features.suspicious_score}·复杂度{features.complexity_score}，走标准路径"
        })

        return decision


# ═══════════════════════════════════════════════════════════════════════════════
# 调度器 (Dispatcher / Scheduler)
# ═══════════════════════════════════════════════════════════════════════════════

class BrainDispatcher:
    """调度器：执行决策路径，调用各脑区模块"""

    # 脑区→人格映射
    BRAIN_TO_PERSONA: Dict[str, str] = {
        "B1": "P07",  # 多语言解析 → 开源守门
        "B2": "P03",  # AI鉴定 → 墨子/雯雯
        "B3": "P18",  # 来源追溯 → 凤凰
        "B4": "P04",  # CNSH翻译 → 鲁班
        "B5": "P06",  # 数学验证 → 数学大师
        "B6": "P02",  # 代码优化 → 龙芯修复师
        "B7": "P05",  # 质量检查 → 上帝之眼
        "B8": "P01",  # DNA追溯 → 诸葛亮
    }

    BRAIN_SCRIPTS: Dict[str, str] = {
        "B1": "brain_parser.py",
        "B2": "brain_ai_detector.py",
        "B3": "brain_source_tracer.py",
        "B4": "brain_cnsh_translator.py",
        "B5": "brain_math_verifier.py",
        "B6": "brain_code_optimizer.py",
        "B7": "brain_quality_auditor.py",
        "B8": "brain_dna_tracer.py",
    }

    def __init__(self):
        self.results: Dict[str, Any] = {}
        self.logs: List[str] = []
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.regions_dir = os.path.join(script_dir, "cnsh_brain_regions")

    def execute(self, decision: Dict[str, Any], code: str, features: InputFeatures) -> Dict[str, Any]:
        """执行路由决策"""
        result = {
            "input_features": features.to_dict(),
            "decision": decision,
            "brain_results": {},
            "final_output": None,
            "quality_report": {},
            "dna": None,
            "errors": [],
            "warnings": [],
            "timing": {}
        }

        brain_list = decision.get("brains", [])
        parallel_list = decision.get("parallel_brains", [])

        t_start = time.time()

        # 主路径顺序执行
        for i, brain_id in enumerate(brain_list):
            t_brain_start = time.time()
            brain_result = self._call_brain(brain_id, code, features, i, len(brain_list))
            result["brain_results"][brain_id] = brain_result
            result["timing"][brain_id] = round(time.time() - t_brain_start, 3)

            if brain_result.get("status") == "error":
                result["errors"].append(f"{brain_id}: {brain_result.get('message')}")

            # 动态路径调整：根据当前脑区结果决定是否添加後续脑区
            if brain_result.get("auto_activate"):
                for extra_brain in brain_result["auto_activate"]:
                    if extra_brain not in brain_list:
                        brain_list.append(extra_brain)
                        self.logs.append(f"🧠 {brain_id} 自动激活 {extra_brain}")

            # 更新code为当前输出（传递给下一个脑区）
            if brain_result.get("output_code"):
                code = brain_result["output_code"]

        # 并行执行輔助任务
        if parallel_list:
            for brain_id in parallel_list:
                t_brain_start = time.time()
                brain_result = self._call_brain(brain_id, code, features, -1, 0)
                result["brain_results"][f"{brain_id}_parallel"] = brain_result
                result["timing"][f"{brain_id}_parallel"] = round(time.time() - t_brain_start, 3)

        result["timing"]["total"] = round(time.time() - t_start, 3)
        result["final_output"] = code

        return result

    def _call_brain(self, brain_id: str, code: str, features: InputFeatures,
                    step: int, total: int) -> Dict[str, Any]:
        """调用单个脑区"""
        persona = self.BRAIN_TO_PERSONA.get(brain_id, "unknown")
        script_name = self.BRAIN_SCRIPTS.get(brain_id, "")
        script_path = os.path.join(self.regions_dir, script_name)

        result = {
            "brain": brain_id,
            "persona": persona,
            "status": "pending",
            "output_code": code,
            "auto_activate": [],
            "message": ""
        }

        if os.path.exists(script_path):
            try:
                # 嘗试导入并执行脑区模块
                sys.path.insert(0, self.regions_dir)
                module_name = script_name.replace('.py', '')
                mod = __import__(module_name)

                if hasattr(mod, 'execute'):
                    brain_result = mod.execute(code, features.to_dict(), step, total)
                    result.update(brain_result)
                    result["status"] = "ok"
                else:
                    result["status"] = "stub"
                    result["message"] = f"{brain_id} 模块已创建但 execute() 未实现"
                sys.path.pop(0)
            except ImportError as e:
                result["status"] = "error"
                result["message"] = f"{brain_id} 导入失敗: {e}"
            except Exception as e:
                result["status"] = "error"
                result["message"] = f"{brain_id} 执行异常: {e}"
        else:
            result["status"] = "stub"
            result["message"] = f"{brain_id} ({script_name}) 尚未实现，返回原码透传"

        self.logs.append(
            f"[{result['status']}] {brain_id} → {persona}: {result.get('message', '完成')}"
        )
        return result


# ═══════════════════════════════════════════════════════════════════════════════
# 神经中樞主入口 (Main Neural Hub)
# ═══════════════════════════════════════════════════════════════════════════════

class CNSHNeuralBrainHub:
    """CNSH神经网络翻译引擎·总入口"""

    def __init__(self):
        self.perception = PerceptionLayer()
        self.decision = DecisionEngine()
        self.dispatcher = BrainDispatcher()
        self.learning_log: List[Dict] = []

    def process(self, code: str) -> Dict[str, Any]:
        """处理输入代码的完整流程"""
        # 第①步：感知
        features = self.perception.scan(code)

        # 第②步：路由决策
        decision = self.decision.route(features, code)

        # 第③步：执行调度
        result = self.dispatcher.execute(decision, code, features)

        # 第④步：生成DNA
        result["dna"] = self._generate_dna(result)

        # 第⑤步：学習记录
        self._learn(features, decision, result)

        return result

    def process_with_report(self, code: str) -> str:
        """处理并返回可读报告"""
        result = self.process(code)

        features = result["input_features"]
        decision = result["decision"]
        brain_results = result["brain_results"]

        report = []
        report.append("╔══════════════════════════════════════════════════════════╗")
        report.append("║    🐉 CNSH神经网络翻译引擎 · 智能路由报告                ║")
        report.append("╠══════════════════════════════════════════════════════════╣")
        report.append("")
        report.append("📊 输入特征:")
        report.append(f"   语言: {features['language']} | 类型: {features['input_type']}")
        report.append(f"   品质: {features['quality_score']}/100 | 复杂度: {features['complexity_score']}/100")
        report.append(f"   可疑度: {features['suspicious_score']}/100 | 有DNA: {features['has_dna']}")
        report.append(f"   代码行数: {features['code_length']}")
        report.append("")
        report.append(f"🧭 路由决策: {decision['path_name']} ({decision['expected_time']})")
        report.append(f"   原因: {decision['reason']}")
        report.append(f"   路径: {' → '.join(decision['brains'])}")
        if decision.get('parallel_brains'):
            report.append(f"   并行: {', '.join(decision['parallel_brains'])}")
        report.append("")
        report.append("🧬 脑区执行:")
        for bid, bres in brain_results.items():
            status_icon = "✅" if bres.get('status') == 'ok' else "⚠️" if bres.get('status') == 'stub' else "❌"
            persona = bres.get('persona', '?')
            msg = bres.get('message', '')
            report.append(f"   {status_icon} {bid} → {persona}: {msg}")
        report.append("")
        if result.get("errors"):
            report.append(f"❌ 错误: {len(result['errors'])} 項")
            for e in result["errors"]:
                report.append(f"   - {e}")
        if result.get("dna"):
            report.append(f"🧬 DNA: {result['dna']}")
        report.append(f"⏱ 总耗时: {result['timing'].get('total', 'N/A')}s")
        report.append("")
        report.append("╚══════════════════════════════════════════════════════════╝")

        return "\n".join(report)

    def _generate_dna(self, result: Dict[str, Any]) -> str:
        """生成DNA追溯码"""
        path = result["decision"]["path"]
        content = json.dumps(result["input_features"], sort_keys=True)
        short_hash = hashlib.sha256(content.encode()).hexdigest()[:8].upper()
        return f"#龙芯⚡️丙午·丙申·丙辰·未时·需-CNSH-{path}-{short_hash}"

    def _learn(self, features: InputFeatures, decision: Dict[str, Any], result: Dict[str, Any]):
        """学習模块：记录决策效果"""
        self.learning_log.append({
            "features": features.to_dict(),
            "decision_path": decision["path"],
            "brain_results": {k: v.get("status") for k, v in result["brain_results"].items()},
            "total_time": result["timing"].get("total", 0),
            "errors": len(result.get("errors", []))
        })


# ═══════════════════════════════════════════════════════════════════════════════
# 命令行接口
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    hub = CNSHNeuralBrainHub()

    if len(sys.argv) > 1:
        # 文件模式
        filepath = sys.argv[1]
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                code = f.read()
        else:
            print(f"❌ 文件不存在: {filepath}")
            sys.exit(1)
    else:
        # 交互模式
        print("🐉 CNSH神经网络翻译引擎 v1.0")
        print("   输入代码 (输入 END 结束):")
        print()
        lines = []
        while True:
            try:
                line = input()
                if line.strip().upper() == "END":
                    break
                lines.append(line)
            except (EOFError, KeyboardInterrupt):
                break
        code = "\n".join(lines)

    if not code.strip():
        print("❌ 未提供任何输入")
        sys.exit(1)

    # 执行翻译
    report = hub.process_with_report(code)
    print(report)

    # 输出JSON结果（可选）
    if "--json" in sys.argv:
        result = hub.process(code)
        print("\n📋 JSON输出:")
        print(json.dumps(result, indent=2, ensure_ascii=False, default=str))

    # 输出学習统计（可选）
    if "--stats" in sys.argv:
        print(f"\n📊 学習统计: {len(hub.learning_log)} 条记录")


if __name__ == "__main__":
    main()
