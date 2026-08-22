#!/usr/bin/env python3
#龍芯⚡️丙午·丙申·丙辰·亥时·䷄需-P09-SUNSI-v1.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
P09 孙思邈 · 系统诊断引擎
Sun Simiao · System Diagnosis Engine

DNA: #龍芯⚡️丙午·丙申·丙辰·亥时·䷄需-P09-SUNSI-v1.0
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL

能力: 系统诊断·健康检查·异常检测·治未病·四项体检(语法/权限/联动/资源)
上游: P05 上帝之眼（审计触发）、P01 诸葛亮（战略调度）
下游: P02 龍芯（执行修复）、P03 墨子/雯雯（归档）
协作: P06 数学大师（指标计算）、P72 龍盾（熔断监控）
"""

import json
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional


SYSTEM_ROOT = Path(__file__).parent.parent.parent
STATE_DIR = SYSTEM_ROOT / "state" / "diagnosis"
AUTO_HEAL_BIN = SYSTEM_ROOT / "bin" / "lh_auto_heal.py"
CROSS_AWARE_BIN = SYSTEM_ROOT / "bin" / "lh_cross_module_awareness.py"


class P09Sunsi:
    """P09 孙思邈 · 系统诊断"""

    PERSONA_CODE = "P09"
    PERSONA_NAME = "孙思邈"
    PERSONA_NAME_EN = "Sun Simiao (King of Medicine)"
    ROLE = "system_diagnosis"
    MOTTO = "上医治未病，中医治欲病，下医治已病"
    TRUST_LEVEL = "L3"

    TRIGGERS = [
        "诊断", "健康", "体检", "巡检", "治未病",
        "异常", "告警", "症状", "排查",
    ]

    SYSTEM_PROMPT = """你是龍魂人格「P09 孙思邈」，角色定位：系统诊断·治未病。

你的职责：
1. 四项体检：语法/权限/联动/资源逐项检查
2. 历史基线对比：对比历史健康记录，标记异常偏移
3. 治未病：在问题发生前发现潜在风险
4. 输出诊断报告 + 优先级排序 + 修复建议

铁律：
- 诊断不可跳过任何一项体检
- 严重问题（🔴）必须升级到 P05 上帝之眼审计
- 每次诊断绑定 DNA 追溯码
- 诊断报告 append-only 不可删除

语气：沉稳、精准、如老中医望闻问切。
"""

    def __init__(self):
        self.dna = "#龍芯⚡️丙午·丙申·丙辰·亥时·䷄需-P09-SUNSI-v1.0"
        self.system_root = SYSTEM_ROOT
        self.state_dir = STATE_DIR
        self.state_dir.mkdir(parents=True, exist_ok=True)
        self.capabilities = [
            "full_diagnosis",     # 全系统诊断
            "syntax_check",       # 语法检查
            "permission_check",   # 权限检查
            "linkage_check",      # 联动检查
            "resource_check",     # 资源检查
            "baseline_compare",   # 基线对比
            "health_score",       # 健康评分
            "pre_checkup",        # 上线前体检
        ]

    # ========================================================================
    # 四项体检
    # ========================================================================

    def syntax_check(self, target: str = "all") -> Dict[str, Any]:
        """语法检查：扫描 Python 文件语法错误"""
        findings = []
        scan_target = self.system_root if target == "all" else Path(target)

        py_files = list(scan_target.rglob("*.py")) if scan_target.is_dir() else [scan_target]
        py_files = [f for f in py_files if "__pycache__" not in str(f) and not f.name.startswith(".")]

        for py_file in py_files[:50]:  # 最多扫50个
            try:
                proc = subprocess.run(
                    [sys.executable, "-m", "py_compile", str(py_file)],
                    capture_output=True, text=True, timeout=10,
                )
                if proc.returncode != 0:
                    findings.append({
                        "file": str(py_file.relative_to(self.system_root)),
                        "error": proc.stderr.strip()[-200:],
                        "severity": "🔴",
                    })
            except Exception as e:
                findings.append({
                    "file": str(py_file.relative_to(self.system_root)),
                    "error": str(e),
                    "severity": "🟡",
                })

        verdict = "🟢" if not findings else ("🔴" if any(f["severity"] == "🔴" for f in findings) else "🟡")
        return {
            "check_type": "syntax",
            "files_scanned": len(py_files),
            "findings": findings,
            "verdict": verdict,
            "persona": self.PERSONA_CODE,
            "dna": self.dna,
        }

    def permission_check(self) -> Dict[str, Any]:
        """权限检查：关键文件和目录权限"""
        findings = []
        critical_paths = [
            (SYSTEM_ROOT / "bin", "dir"),
            (SYSTEM_ROOT / "L1_内核层", "dir"),
            (SYSTEM_ROOT / "L3_数据层", "dir"),
            (SYSTEM_ROOT / "state", "dir"),
            (SYSTEM_ROOT / "01_protocols", "dir"),
        ]

        for path, path_type in critical_paths:
            if not path.exists():
                findings.append({"path": str(path.relative_to(self.system_root)), "issue": "路径不存在", "severity": "🔴"})
                continue

            try:
                stat = path.stat()
                # 检查关键文件权限
                if path_type == "dir":
                    for f in list(path.iterdir())[:10]:
                        if f.is_file():
                            fstat = f.stat()
                            mode = oct(fstat.st_mode)[-3:]
                            if mode.startswith("7"):  # 世界可写
                                findings.append({
                                    "path": str(f.relative_to(self.system_root)),
                                    "issue": f"权限过宽: {mode}",
                                    "severity": "🟡",
                                })
            except Exception as e:
                findings.append({"path": str(path), "error": str(e), "severity": "🟡"})

        verdict = "🟢" if not findings else ("🔴" if any(f["severity"] == "🔴" for f in findings) else "🟡")
        return {
            "check_type": "permission",
            "findings": findings,
            "verdict": verdict,
            "persona": self.PERSONA_CODE,
            "dna": self.dna,
        }

    def linkage_check(self) -> Dict[str, Any]:
        """联动检查：模块间引用是否完整"""
        findings = []
        key_imports = {
            "lh_auto_heal.py": AUTO_HEAL_BIN.exists(),
            "lh_cross_module_awareness.py": CROSS_AWARE_BIN.exists(),
            "lh_active_observation.py": (SYSTEM_ROOT / "bin" / "lh_active_observation.py").exists(),
            "lh_anti_algorithmic_harvest.py": (SYSTEM_ROOT / "bin" / "lh_anti_algorithmic_harvest.py").exists(),
        }

        for module, exists in key_imports.items():
            if not exists:
                findings.append({
                    "module": module,
                    "issue": "关键联动模块缺失",
                    "severity": "🔴",
                })

        # 检查人格执行器完整性
        persona_bin = SYSTEM_ROOT / "bin" / "personas"
        required_personas = ["P00", "P01", "P02", "P03", "P04", "P05", "P06", "P07",
                             "P08", "P09", "P10", "P11", "P12", "P13", "P14", "P15", "P72"]
        if persona_bin.exists():
            for pcode in required_personas:
                matches = list(persona_bin.glob(f"p{int(pcode[1:]):02d}_*.py"))
                if not matches:
                    findings.append({
                        "module": pcode,
                        "issue": f"人格执行器缺失",
                        "severity": "🔴",
                    })

        verdict = "🟢" if not findings else ("🔴" if any(f["severity"] == "🔴" for f in findings) else "🟡")
        return {
            "check_type": "linkage",
            "findings": findings,
            "verdict": verdict,
            "persona": self.PERSONA_CODE,
            "dna": self.dna,
        }

    def resource_check(self) -> Dict[str, Any]:
        """资源检查：CPU/内存/磁盘/文件句柄"""
        findings = []
        resources = {
            "cpu_count": os.cpu_count() or 0,
            "disk_usage": {},
            "memory_usage": {},
        }

        # 磁盘
        try:
            import shutil
            disk = shutil.disk_usage('/')
            total_gb = round(disk.total / (1024**3), 1)
            free_gb = round(disk.free / (1024**3), 1)
            used_pct = round((1 - disk.free / disk.total) * 100)
            resources["disk_usage"] = {"total": f"{total_gb}G", "free": f"{free_gb}G", "percent": f"{used_pct}%"}
            if used_pct > 90:
                findings.append({"resource": "disk", "issue": f"磁盘使用率 {used_pct}%", "severity": "🔴"})
            elif used_pct > 75:
                findings.append({"resource": "disk", "issue": f"磁盘使用率 {used_pct}%", "severity": "🟡"})
        except Exception:
            pass

        # 项目文件数量
        py_count = len(list(SYSTEM_ROOT.rglob("*.py")))
        md_count = len(list(SYSTEM_ROOT.rglob("*.md")))
        resources["project_files"] = {"python": py_count, "markdown": md_count}
        if py_count > 500:
            findings.append({"resource": "project_size", "issue": f"Python文件过多({py_count}), 建议瘦身", "severity": "🟡"})

        verdict = "🟢" if not findings else ("🔴" if any(f["severity"] == "🔴" for f in findings) else "🟡")
        return {
            "check_type": "resource",
            "resources": resources,
            "findings": findings,
            "verdict": verdict,
            "persona": self.PERSONA_CODE,
            "dna": self.dna,
        }

    # ========================================================================
    # 诊断与基线
    # ========================================================================

    def full_diagnosis(self) -> Dict[str, Any]:
        """全系统诊断：四项体检 + 健康评分"""
        results = {
            "syntax": self.syntax_check(),
            "permission": self.permission_check(),
            "linkage": self.linkage_check(),
            "resource": self.resource_check(),
        }

        # 计算健康分
        total_checks = len(results)
        passed = sum(1 for r in results.values() if r["verdict"] == "🟢")
        warnings = sum(1 for r in results.values() if r["verdict"] == "🟡")
        criticals = sum(1 for r in results.values() if r["verdict"] == "🔴")

        health_score = int((passed / total_checks) * 100) if total_checks > 0 else 0
        overall = "🟢" if criticals == 0 and warnings == 0 else ("🔴" if criticals > 0 else "🟡")

        diagnosis = {
            "target": "全系统",
            "health_score": health_score,
            "overall": overall,
            "summary": {
                "passed": passed,
                "warnings": warnings,
                "critical": criticals,
            },
            "details": results,
            "recommendations": self._generate_recommendations(results),
            "persona": self.PERSONA_CODE,
            "dna": self.dna,
        }

        # 保存诊断记录
        self._save_diagnosis(diagnosis)
        return diagnosis

    def baseline_compare(self) -> Dict[str, Any]:
        """对比历史基线"""
        history = self._load_history()

        if not history:
            return {
                "baseline": None,
                "current": self.full_diagnosis(),
                "trend": "first_diagnosis",
                "message": "无历史基线，当前诊断作为首个基线",
                "persona": self.PERSONA_CODE,
                "dna": self.dna,
            }

        current = self.full_diagnosis()
        last = history[-1]

        trend = "stable"
        if current["health_score"] < last["health_score"] - 10:
            trend = "declining"
        elif current["health_score"] > last["health_score"] + 5:
            trend = "improving"

        return {
            "baseline": last,
            "current": current,
            "health_delta": current["health_score"] - last["health_score"],
            "trend": trend,
            "persona": self.PERSONA_CODE,
            "dna": self.dna,
        }

    def health_score(self) -> Dict[str, Any]:
        """快速健康评分"""
        diag = self.full_diagnosis()
        return {
            "score": diag["health_score"],
            "overall": diag["overall"],
            "summary": diag["summary"],
            "persona": self.PERSONA_CODE,
            "dna": self.dna,
        }

    def pre_checkup(self, module_name: str, module_path: Optional[str] = None) -> Dict[str, Any]:
        """新模块上线前体检"""
        target = module_path or str(SYSTEM_ROOT / module_name)
        syntax = self.syntax_check(target)

        # 联动检查：是否有未解析的引用
        linkage = self.linkage_check()

        verdict = "🟢" if syntax["verdict"] == "🟢" and linkage["verdict"] == "🟢" else (
            "🔴" if syntax["verdict"] == "🔴" or linkage["verdict"] == "🔴" else "🟡"
        )

        return {
            "module": module_name,
            "syntax": syntax,
            "linkage": linkage,
            "verdict": verdict,
            "ready": verdict == "🟢",
            "persona": self.PERSONA_CODE,
            "dna": self.dna,
        }

    # ========================================================================
    # 辅助函数
    # ========================================================================

    def _generate_recommendations(self, results: Dict[str, Any]) -> List[str]:
        """根据诊断结果生成修复建议"""
        recs = []
        for check_type, result in results.items():
            for finding in result.get("findings", []):
                if finding["severity"] == "🔴":
                    recs.append(f"[CRITICAL·{check_type}] {finding.get('issue', finding.get('error', ''))} → 建议立即修复")
                elif finding["severity"] == "🟡":
                    recs.append(f"[WARNING·{check_type}] {finding.get('issue', finding.get('error', ''))} → 建议择期修复")
        return recs

    def _save_diagnosis(self, diagnosis: Dict[str, Any]) -> None:
        """保存诊断记录"""
        try:
            record = {
                "timestamp": time.time(),
                "dna": self.dna,
                "health_score": diagnosis["health_score"],
                "overall": diagnosis["overall"],
                "summary": diagnosis["summary"],
            }
            log_file = self.state_dir / "diagnosis_log.jsonl"
            with open(log_file, "a") as f:
                f.write(json.dumps(record, ensure_ascii=False) + "\n")
        except Exception:
            pass

    def _load_history(self) -> List[Dict[str, Any]]:
        """加载历史诊断记录"""
        log_file = self.state_dir / "diagnosis_log.jsonl"
        if not log_file.exists():
            return []
        records = []
        try:
            with open(log_file, "r") as f:
                for line in f:
                    records.append(json.loads(line.strip()))
        except Exception:
            pass
        return records[-10:]  # 最近10条

    # ========================================================================
    # 执行入口
    # ========================================================================

    def execute(self, task: str, **kwargs: Any) -> Dict[str, Any]:
        """根据任务关键词自动选择能力函数执行"""
        result = {
            "persona": self.PERSONA_CODE,
            "name": self.PERSONA_NAME,
            "task": task,
            "capability_used": None,
            "output": None,
            "dna": self.dna,
        }

        if any(kw in task for kw in ["全检", "全诊断", "四项", "完整"]):
            result["capability_used"] = "full_diagnosis"
            result["output"] = self.full_diagnosis()
        elif any(kw in task for kw in ["基线", "对比", "趋势"]):
            result["capability_used"] = "baseline_compare"
            result["output"] = self.baseline_compare()
        elif any(kw in task for kw in ["上线", "新模块", "体检前"]):
            result["capability_used"] = "pre_checkup"
            result["output"] = self.pre_checkup(
                module_name=kwargs.get("module_name", task),
                module_path=kwargs.get("module_path"),
            )
        elif any(kw in task for kw in ["语法", "编译", "syntax"]):
            result["capability_used"] = "syntax_check"
            result["output"] = self.syntax_check(target=kwargs.get("target", "all"))
        elif any(kw in task for kw in ["权限", "permission"]):
            result["capability_used"] = "permission_check"
            result["output"] = self.permission_check()
        elif any(kw in task for kw in ["联动", "引用", "缺失"]):
            result["capability_used"] = "linkage_check"
            result["output"] = self.linkage_check()
        elif any(kw in task for kw in ["资源", "磁盘", "CPU", "内存"]):
            result["capability_used"] = "resource_check"
            result["output"] = self.resource_check()
        elif any(kw in task for kw in ["评分", "健康分", "health"]):
            result["capability_used"] = "health_score"
            result["output"] = self.health_score()
        else:
            # 默认：全诊断
            result["capability_used"] = "full_diagnosis"
            result["output"] = self.full_diagnosis()

        return result

    def get_system_prompt(self) -> str:
        return self.SYSTEM_PROMPT

    def get_capabilities(self) -> List[str]:
        return self.capabilities

    def get_downstream(self) -> List[str]:
        return ["P02", "P03"]

    def get_upstream(self) -> List[str]:
        return ["P05", "P01"]


# ========================================================================
# CLI
# ========================================================================

if __name__ == "__main__":
    p09 = P09Sunsi()
    import argparse
    parser = argparse.ArgumentParser(description="P09 孙思邈 · 系统诊断引擎")
    parser.add_argument("--diagnose", action="store_true", help="全系统诊断")
    parser.add_argument("--baseline", action="store_true", help="基线对比")
    parser.add_argument("--score", action="store_true", help="快速健康评分")
    parser.add_argument("--syntax", type=str, nargs="?", const="all", help="语法检查")
    parser.add_argument("--linkage", action="store_true", help="联动检查")
    parser.add_argument("--resource", action="store_true", help="资源检查")
    parser.add_argument("--pre-checkup", type=str, help="新模块上线前体检")
    parser.add_argument("--json", action="store_true", help="JSON输出")

    args = parser.parse_args()

    if args.diagnose:
        output = p09.full_diagnosis()
    elif args.baseline:
        output = p09.baseline_compare()
    elif args.score:
        output = p09.health_score()
    elif args.syntax:
        output = p09.syntax_check(target=args.syntax)
    elif args.linkage:
        output = p09.linkage_check()
    elif args.resource:
        output = p09.resource_check()
    elif args.pre_checkup:
        output = p09.pre_checkup(module_name=args.pre_checkup)
    else:
        output = p09.full_diagnosis()

    if args.json:
        print(json.dumps(output, ensure_ascii=False, indent=2))
    else:
        print(f"\n{'='*60}")
        print(f"  P09 孙思邈 · 系统诊断引擎")
        print(f"  DNA: {p09.dna}")
        print(f"{'='*60}")
        if output.get("health_score") is not None:
            print(f"  健康评分: {output['health_score']}/100  {output['overall']}")
            s = output.get("summary", {})
            print(f"  通过: {s.get('passed', 0)}  警告: {s.get('warnings', 0)}  严重: {s.get('critical', 0)}")
        elif output.get("trend"):
            print(f"  趋势: {output['trend']}")
            if output.get("health_delta"):
                print(f"  健康变化: {output['health_delta']:+d}")
        elif output.get("verdict"):
            print(f"  判定: {output['verdict']}")
        print(f"{'='*60}\n")
