#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# DNA: #龍芯⚡️丙午·丙酉·丙寅·申时-AUTO-FACTORY-UID9622
# 创建者: 诸葛鑫（UID9622）
"""
🐉 龍魂 · 全自动工厂系统 v2.1（完整可运维版）
DNA: #龍芯⚡️丙午·丙酉·丙寅·申时-AUTO-FACTORY-v2.1-UID9622
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
三色: 🟢 通过

功能: 造零件 → 质检 → 质量门禁 → 自动修复 → 发布 → 部署 → 反馈闭环
v1.0: BuildPipeline / TestPipeline / RepairPipeline / DeployPipeline / FeedbackLoop
v2.0: QualityGate / RollbackPipeline / ReleaseStrategy / SelfMonitor / CircuitBreaker / Notifier / KunpengSync
"""

import json
import os
import queue
import shutil
import subprocess
import sys
import time
from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Any

# 引入 factory 包（兼容两种运行方式：脚本直跑 / 包导入）
_FACTORY_PKG = Path(__file__).resolve().parent / "factory"
if str(_FACTORY_PKG.parent) not in sys.path:
    sys.path.insert(0, str(_FACTORY_PKG.parent))

from factory.generate_dna import generate_dna  # noqa: E402

# ============================================================
# 主权锚定
# ============================================================

UID = "9622"
CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
GPG = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"


# ============================================================
# 工厂状态
# ============================================================

class FactoryStatus(Enum):
    IDLE = "idle"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class BuildResult(Enum):
    PASSED = "passed"
    FAILED = "failed"
    NEEDS_REPAIR = "needs_repair"


# ============================================================
# 数据模型
# ============================================================

@dataclass
class FactoryTask:
    """工厂任务"""
    id: str
    type: str  # build | test | gate | repair | release | deploy | feedback
    status: str
    created_at: str
    updated_at: str
    dna: str
    details: Dict
    result: Optional[str] = None

    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class BuildArtifact:
    """构建产物"""
    id: str
    name: str
    path: str
    version: str
    size: int
    hash: str
    created_at: str
    dna: str

    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class TestReport:
    """测试报告"""
    task_id: str
    total: int
    passed: int
    failed: int
    skipped: int
    errors: int
    coverage: float
    tricolor: str
    dna: str
    timestamp: str
    details: List[Dict]

    def to_dict(self) -> Dict:
        return asdict(self)


# ============================================================
# 零件生产线 (Build Pipeline)
# ============================================================

class BuildPipeline:
    """零件生产线 - 代码构建"""

    def __init__(self, workspace: Path):
        self.workspace = workspace
        self.artifacts_dir = workspace / "artifacts"
        self.artifacts_dir.mkdir(parents=True, exist_ok=True)
        self.index_file = workspace / "artifacts_index.json"
        self.history: List[BuildArtifact] = []
        self._load_index()

    def _load_index(self):
        """加载持久化产物索引（跨进程可见）"""
        try:
            if self.index_file.exists():
                with open(self.index_file, encoding="utf-8") as f:
                    data = json.load(f)
                self.history = [BuildArtifact(**a) for a in data]
        except Exception:
            self.history = []

    def _save_index(self):
        """保存产物索引"""
        try:
            with open(self.index_file, "w", encoding="utf-8") as f:
                json.dump([a.to_dict() for a in self.history], f,
                          indent=2, ensure_ascii=False)
        except Exception:
            pass

    def build(self, source_path: Path, version: str = None) -> BuildArtifact:
        """构建单个零件"""
        dna = generate_dna("BUILD")
        if version is None:
            version = datetime.now().strftime("%Y%m%d.%H%M%S")

        # 统一时间戳，避免跨秒导致 path 与目录不一致
        build_ts = int(time.time())
        build_dir = self.artifacts_dir / f"build_{build_ts}"
        build_dir.mkdir(parents=True, exist_ok=True)

        if source_path.is_file():
            shutil.copy2(source_path, build_dir / source_path.name)
        elif source_path.is_dir():
            shutil.copytree(source_path, build_dir, dirs_exist_ok=True)

        artifact = BuildArtifact(
            id=f"ART-{build_ts}",
            name=source_path.name,
            path=str(build_dir),
            version=version,
            size=self._compute_size(build_dir),
            hash=self._compute_hash(build_dir),
            created_at=datetime.now().isoformat(),
            dna=dna
        )
        self.history.append(artifact)
        self._save_index()
        return artifact

    def _compute_hash(self, path: Path) -> str:
        """计算目录 SHA-256（系统禁 MD5）"""
        sha256 = __import__("hashlib").sha256()
        for f in sorted(path.rglob("*")):
            if f.is_file():
                sha256.update(f.read_bytes())
        return sha256.hexdigest()[:16]

    def _compute_size(self, path: Path) -> int:
        """计算目录大小"""
        total = 0
        for f in path.rglob("*"):
            if f.is_file():
                total += f.stat().st_size
        return total

    def get_artifacts(self, limit: int = 20) -> List[Dict]:
        return [a.to_dict() for a in self.history[-limit:]]


# ============================================================
# 质检流水线 (Test Pipeline)
# ============================================================

class TestPipeline:
    """质检流水线 - 自动测试（兼容 json-report 缺失插件）"""

    def __init__(self, workspace: Path):
        self.workspace = workspace
        self.test_dir = workspace / "tests"
        self.reports_dir = workspace / "reports"
        self.test_dir.mkdir(parents=True, exist_ok=True)
        self.reports_dir.mkdir(parents=True, exist_ok=True)

    def _json_report_available(self) -> bool:
        """探测 pytest-json-report 插件"""
        try:
            import pytest_jsonreport  # noqa: F401
            return True
        except ImportError:
            return False

    def run_tests(self, artifact: BuildArtifact) -> TestReport:
        """运行质检"""
        dna = generate_dna("TEST")
        test_target = Path(artifact.path) / "tests"

        # 无测试目录 → 返回 🟡 空报告（不崩溃）
        if not test_target.exists():
            return TestReport(
                task_id=artifact.id, total=0, passed=0, failed=0, skipped=0,
                errors=0, coverage=0.0, tricolor="🟡", dna=dna,
                timestamp=datetime.now().isoformat(),
                details=[{"message": "无测试目录，跳过质检"}]
            )

        # 运行 pytest（有 json-report 用结构化，否则文本解析）
        json_report_file = Path(artifact.path) / ".pytest_report.json"
        cmd = [sys.executable, "-m", "pytest", str(test_target), "-v"]
        if self._json_report_available():
            cmd += ["--json-report", f"--json-report-file={json_report_file}"]
        else:
            cmd += ["-p", "no:cacheprovider"]

        result = subprocess.run(cmd, capture_output=True, text=True,
                                cwd=artifact.path, timeout=300)

        # 解析结果
        total = passed = failed = skipped = errors = 0
        details: List[Dict] = []

        if json_report_file.exists():
            with open(json_report_file, encoding="utf-8") as f:
                report_data = json.load(f)
            summary = report_data.get("summary", {})
            total = summary.get("total", 0)
            passed = summary.get("passed", 0)
            failed = summary.get("failed", 0)
            skipped = summary.get("skipped", 0)
            errors = summary.get("errors", 0)
            details = report_data.get("tests", [])
        else:
            # 文本解析回退: 统计 PASSED/FAILED/SKIPPED 行
            for line in result.stdout.splitlines():
                if "PASSED" in line:
                    passed += 1
                elif "FAILED" in line:
                    failed += 1
                elif "SKIPPED" in line:
                    skipped += 1
            total = passed + failed + skipped
            if result.returncode == 0 and total == 0:
                # 收集阶段无测试
                details = [{"message": result.stdout[-300:]}]
            else:
                for line in result.stdout.splitlines():
                    if "FAILED" in line:
                        details.append({"name": line.split()[0], "outcome": "failed",
                                        "call": {"crash": {"message": result.stdout[-500:]}}})

        coverage = self._run_coverage(artifact.path)
        tricolor = self._tricolor_audit(passed, failed, total)

        report = TestReport(
            task_id=artifact.id, total=total, passed=passed, failed=failed,
            skipped=skipped, errors=errors, coverage=coverage, tricolor=tricolor,
            dna=dna, timestamp=datetime.now().isoformat(), details=details
        )

        report_path = self.reports_dir / f"test_report_{int(time.time())}.json"
        with open(report_path, "w", encoding="utf-8") as f:
            json.dump(report.to_dict(), f, indent=2, ensure_ascii=False)

        return report

    def _run_coverage(self, path: Path) -> float:
        """运行覆盖率检查（缺 pytest-cov 返回 0.0）"""
        try:
            result = subprocess.run(
                [sys.executable, "-m", "pytest", "--cov=.", "--cov-report=json"],
                capture_output=True, text=True, cwd=path, timeout=120
            )
            cov_file = path / "coverage.json"
            if cov_file.exists():
                with open(cov_file, encoding="utf-8") as f:
                    data = json.load(f)
                    return data.get("totals", {}).get("percent_covered", 0.0)
        except Exception:
            pass
        return 0.0

    def _tricolor_audit(self, passed: int, failed: int, total: int) -> str:
        """三色审计: 全过🟢 / 失败≤10%🟡 / 其他🔴"""
        if total == 0:
            return "🟡"
        if failed == 0:
            return "🟢"
        if failed <= total * 0.1:
            return "🟡"
        return "🔴"


# ============================================================
# 自动修复线 (Repair Pipeline)
# ============================================================

class RepairPipeline:
    """自动修复线 - AI修复"""

    def __init__(self, workspace: Path):
        self.workspace = workspace
        self.repair_log: List[Dict] = []

    def repair(self, report: TestReport) -> Dict:
        """自动修复（返回修复建议）"""
        dna = generate_dna("REPAIR")
        repairs = []

        if report.tricolor == "🟢":
            return {"dna": dna, "status": "ok", "message": "无需修复",
                    "repairs": [], "timestamp": datetime.now().isoformat()}

        for test in report.details:
            if test.get("outcome") == "failed":
                repairs.append(self._repair_test(test))

        return {
            "dna": dna,
            "status": "repaired" if repairs else "no_repair_needed",
            "repairs": repairs,
            "timestamp": datetime.now().isoformat()
        }

    def _repair_test(self, test: Dict) -> Dict:
        """修复单个测试（生成修复建议，实际可接入 AI 修复引擎）"""
        test_name = test.get("name", "unknown")
        crash = (test.get("call") or {}).get("crash") or {}
        error = crash.get("message", "") or ""

        fix_suggestions = []
        el = error.lower()
        if "dna" in el or "确认码" in el or "gpg" in el:
            fix_suggestions.append("添加或修复 DNA 追溯码/确认码/GPG 头")
        if "import" in el or "modulenotfound" in el:
            fix_suggestions.append("检查模块导入路径或缺失依赖")
        if "assert" in el:
            fix_suggestions.append("检查断言逻辑与期望值")
        if "syntaxerror" in el:
            fix_suggestions.append("检查语法错误与缩进")

        return {
            "test": test_name,
            "error": error[:200],
            "fixes": fix_suggestions,
            "priority": "HIGH" if fix_suggestions else "LOW"
        }


# ============================================================
# 部署上线线 (Deploy Pipeline)
# ============================================================

class DeployPipeline:
    """部署上线线 - 打包 + 本地部署"""

    def __init__(self, workspace: Path):
        self.workspace = workspace
        self.deploy_dir = workspace / "deploy"
        self.deploy_dir.mkdir(parents=True, exist_ok=True)

    def deploy(self, artifact: BuildArtifact, target: str = "local") -> Dict:
        """部署"""
        dna = generate_dna("DEPLOY")
        package_path = self.deploy_dir / f"{artifact.name}_{artifact.version}.tar.gz"
        shutil.make_archive(
            str(package_path).replace('.tar.gz', ''),
            'gztar', artifact.path
        )

        if target == "local":
            deploy_path = self.deploy_dir / "current"
            if deploy_path.exists():
                shutil.rmtree(deploy_path)
            shutil.copytree(artifact.path, deploy_path)

        return {
            "dna": dna, "status": "success", "target": target,
            "package": str(package_path),
            "timestamp": datetime.now().isoformat()
        }


# ============================================================
# 反馈闭环 (Feedback Loop)
# ============================================================

class FeedbackLoop:
    """反馈闭环 - 学习进化"""

    def __init__(self, workspace: Path):
        self.workspace = workspace
        self.feedback_dir = workspace / "feedback"
        self.feedback_dir.mkdir(parents=True, exist_ok=True)

    def collect(self, report: TestReport, repair_result: Dict) -> Dict:
        """收集反馈"""
        dna = generate_dna("FEEDBACK")
        feedback = {
            "dna": dna,
            "test_report": report.to_dict(),
            "repair_result": repair_result,
            "timestamp": datetime.now().isoformat()
        }
        feedback_path = self.feedback_dir / f"feedback_{int(time.time())}.json"
        with open(feedback_path, "w", encoding="utf-8") as f:
            json.dump(feedback, f, indent=2, ensure_ascii=False)
        return feedback

    def learn(self) -> Dict:
        """从历史反馈中学习"""
        pattern_map: Dict[str, Dict] = {}
        for f in self.feedback_dir.glob("*.json"):
            with open(f, encoding="utf-8") as fp:
                data = json.load(fp)
            for repair in (data.get("repair_result", {}) or {}).get("repairs", []):
                key = repair.get("test", "unknown")
                if key not in pattern_map:
                    pattern_map[key] = {"test": key, "fixes": repair.get("fixes", []), "count": 0}
                pattern_map[key]["count"] += 1

        return {
            "total_patterns": len(pattern_map),
            "top_patterns": sorted(pattern_map.values(),
                                   key=lambda x: x["count"], reverse=True)[:10]
        }


# ============================================================
# 工厂主控制器 (整合 v1.0 + v2.0)
# ============================================================

class AutoFactory:
    """全自动工厂主控制器"""

    def __init__(self, workspace: Path = None):
        if workspace is None:
            workspace = Path.home() / ".longhun" / "factory"
        self.workspace = workspace
        self.workspace.mkdir(parents=True, exist_ok=True)

        self.build_pipeline = BuildPipeline(workspace)
        self.test_pipeline = TestPipeline(workspace)
        self.repair_pipeline = RepairPipeline(workspace)
        self.deploy_pipeline = DeployPipeline(workspace)
        self.feedback_loop = FeedbackLoop(workspace)

        # v2.0 模块
        from factory.quality_gate import QualityGate
        from factory.rollback_pipeline import RollbackPipeline
        from factory.release_strategy import ReleaseStrategy
        from factory.self_monitor import SelfMonitor
        from factory.circuit_breaker import CircuitBreaker, BreakerLevel
        from factory.notifier import Notifier
        from factory.kunpeng_sync import KunpengSync

        self.quality_gate = QualityGate()
        self.rollback_pipeline = RollbackPipeline(workspace / "deploy")
        self.release_strategy = ReleaseStrategy("canary")
        self.self_monitor = SelfMonitor(workspace)
        self.circuit_breaker = CircuitBreaker()
        self.BreakerLevel = BreakerLevel
        self.notifier = Notifier(workspace / "logs" / "factory.log")
        self.kunpeng = KunpengSync()

        self.status = "idle"
        self.current_task: Optional[FactoryTask] = None
        self.history: List[Dict] = []
        self.dna = generate_dna("FACTORY-INIT")

    def run_full_cycle(self, source_path: Path, version: str = None,
                       target: str = "local", notify: bool = False) -> Dict:
        """完整工厂流程: 造零件 → 质检 → 门禁 → 修复 → 发布 → 部署 → 反馈"""
        task_dna = generate_dna("FULL-CYCLE")
        self.status = "running"
        results: Dict[str, Any] = {"dna": task_dna, "steps": {}}

        try:
            # Step 1: 造零件
            print("🏗️ ① 造零件...")
            artifact = self.build_pipeline.build(source_path, version)
            results["steps"]["build"] = {
                "artifact_id": artifact.id, "version": artifact.version,
                "size": artifact.size, "dna": artifact.dna
            }
            v_str = artifact.version if artifact.version.startswith("v") else f"v{artifact.version}"
            print(f"   ✅ 零件已造: {artifact.name} {v_str}")

            # Step 2: 质检
            print("🔍 ② 质检流水线...")
            report = self.test_pipeline.run_tests(artifact)
            results["steps"]["test"] = {
                "total": report.total, "passed": report.passed,
                "failed": report.failed, "coverage": report.coverage,
                "tricolor": report.tricolor, "dna": report.dna
            }
            print(f"   ✅ 质检: {report.tricolor} ({report.passed}/{report.total}) cov={report.coverage}%")

            # Step 3: 质量门禁 (P0: 不过不发布)
            print("🚧 ③ 质量门禁...")
            gate = self.quality_gate.evaluate(report.to_dict())
            results["steps"]["gate"] = gate
            print(f"   ✅ 门禁: {gate['overall']}")
            if gate["overall"] != "PASS":
                self.circuit_breaker.register_failure(
                    "gate", self.BreakerLevel.L3)
                results["status"] = "blocked_by_gate"
                self.status = "failed"
                print("   ❌ 质量门禁未通过，已拦截发布（gate 不过不发布）")
                if notify:
                    self.notifier.send("log", "工厂门禁拦截",
                                       f"门禁 FAIL: {gate['overall']}", "warning")
                self.history.append(results)
                return results

            # Step 4: 自动修复
            print("🔧 ④ 自动修复...")
            repair_result = self.repair_pipeline.repair(report)
            results["steps"]["repair"] = repair_result
            print(f"   ✅ 修复: {repair_result.get('status')}")

            # Step 5: 发布策略
            print("🚀 ⑤ 发布策略 (canary)...")
            release_result = self.release_strategy.execute(Path(artifact.path))
            results["steps"]["release"] = release_result
            print(f"   ✅ 发布: {release_result['strategy']}")

            # Step 6: 部署
            print("📦 ⑥ 部署上线...")
            deploy_result = self.deploy_pipeline.deploy(artifact, target)
            results["steps"]["deploy"] = deploy_result
            print(f"   ✅ 部署完成: {deploy_result['target']}")

            # Step 7: 反馈闭环
            print("📊 ⑦ 收集反馈...")
            feedback = self.feedback_loop.collect(report, repair_result)
            results["steps"]["feedback"] = {
                "dna": feedback["dna"], "timestamp": feedback["timestamp"]
            }
            learn_result = self.feedback_loop.learn()
            results["steps"]["learn"] = learn_result
            print(f"   ✅ 反馈已收集 (学习模式: {learn_result['total_patterns']} 模式)")

            self.status = "completed"
            results["status"] = "success"
            if notify:
                self.notifier.send("log", "工厂流程完成",
                                   f"🟢 {artifact.name} v{artifact.version} 全链路通过", "info")

        except Exception as e:
            self.status = "failed"
            results["status"] = "failed"
            results["error"] = str(e)
            print(f"❌ 工厂流程失败: {e}")
            if notify:
                self.notifier.send("log", "工厂流程失败", str(e)[:300], "error")

        self.history.append(results)
        return results

    def get_status(self) -> Dict:
        """获取工厂状态"""
        return {
            "dna": self.dna, "status": self.status,
            "workspace": str(self.workspace),
            "build_count": len(self.build_pipeline.history),
            "history_count": len(self.history),
            "breaker": self.circuit_breaker.status(),
            "timestamp": datetime.now().isoformat()
        }

    def get_artifacts(self) -> List[Dict]:
        return self.build_pipeline.get_artifacts()

    def get_feedback_patterns(self) -> Dict:
        return self.feedback_loop.learn()


# ============================================================
# 命令行接口
# ============================================================

def main():
    import argparse

    # 位置子命令 → flag 映射（支持 `lh factory run .` / `python3 lh_auto_factory.py status`）
    _POSITIONAL = {
        "run": ["--run"], "status": ["--status"], "artifacts": ["--artifacts"],
        "learn": ["--learn"], "monitor": ["--monitor"], "gate": ["--gate"],
        "release": ["--release"], "rollback": ["--rollback"],
        "versions": ["--versions"], "circuit": ["--circuit"],
        "kunpeng": ["--kunpeng-health"], "help": [],
    }
    argv = list(sys.argv[1:])
    if argv and argv[0] in _POSITIONAL:
        subcmd = _POSITIONAL[argv[0]]
        if subcmd:
            argv = subcmd + argv[1:]
        else:
            argv = []
    # run PATH VERSION → --run PATH --version VERSION（位置参数转 flag）
    if argv and argv[0] == "--run" and len(argv) >= 3 and not argv[2].startswith("-"):
        argv = ["--run", argv[1], "--version", argv[2]] + argv[3:]
    sys.argv = [sys.argv[0]] + argv

    parser = argparse.ArgumentParser(
        description="🐉 龍魂 · 全自动工厂系统 v2.1",
        epilog=f"DNA: {generate_dna('CLI')}"
    )
    parser.add_argument("--run", metavar="SOURCE_PATH", help="运行完整工厂流程")
    parser.add_argument("--version", help="版本号")
    parser.add_argument("--target", default="local", choices=["local", "kunpeng"],
                        help="部署目标 (local/kunpeng)")
    parser.add_argument("--status", action="store_true", help="查看工厂状态")
    parser.add_argument("--artifacts", action="store_true", help="查看构建产物")
    parser.add_argument("--learn", action="store_true", help="学习反馈模式")
    parser.add_argument("--monitor", action="store_true", help="工厂自监控")
    parser.add_argument("--gate", action="store_true", help="质量门禁检查")
    parser.add_argument("--release", metavar="STRATEGY", help="发布策略 (canary|gray|full)")
    parser.add_argument("--rollback", metavar="VERSION", help="回滚到指定版本")
    parser.add_argument("--versions", action="store_true", help="列出可回滚版本")
    parser.add_argument("--circuit", action="store_true", help="熔断器状态")
    parser.add_argument("--kunpeng-health", action="store_true", help="鲲鹏健康检查")
    parser.add_argument("--notify", action="store_true", help="流程完成时通知")

    args = parser.parse_args()
    factory = AutoFactory()

    def _print(title: str, lines: List[str]):
        print(f"\n{title}")
        print("=" * 50)
        for line in lines:
            print(f"  {line}")

    if args.status:
        s = factory.get_status()
        _print("🏭 龍魂 · 全自动工厂状态", [
            f"DNA: {s['dna']}", f"状态: {s['status']}",
            f"构建次数: {s['build_count']}", f"历史记录: {s['history_count']}",
            f"熔断事件: {s['breaker']['event_count']}",
            f"工作区: {s['workspace']}"
        ])
        return

    if args.artifacts:
        artifacts = factory.get_artifacts()
        _print("📦 构建产物", [
            f"{a['name']} {a['version']} ({a['size']} bytes)\n    DNA: {a['dna']}"
            for a in artifacts
        ] or ["（暂无产物）"])
        return

    if args.learn:
        patterns = factory.get_feedback_patterns()
        _print("🧠 学习模式", [
            f"总模式数: {patterns['total_patterns']}"
        ] + [f"- {p['test']}: 出现 {p['count']} 次"
             for p in patterns.get('top_patterns', [])])
        return

    if args.monitor:
        check = factory.self_monitor.check()
        _print("🔬 工厂自监控", [
            f"整体: {check['overall']}",
            f"磁盘: {check['disk']}",
            f"内存: {check['memory']}",
            f"进程: {check['process']}",
            f"网络: {check['network']}"
        ])
        return

    if args.gate:
        _print("🚧 质量门禁规则", [
            f"{r.name} ({r.condition}) 阈值={r.threshold} 级别={r.severity}"
            for r in factory.quality_gate.rules
        ])
        return

    if args.release:
        factory.release_strategy = factory.release_strategy.__class__(args.release)
        result = factory.release_strategy.execute()
        _print(f"🚀 发布策略: {result['strategy']}", [
            f"DNA: {result['dna']}", f"状态: {result['status']}",
            f"流量: {result['percentage']}%"
        ] + [f"- {s['step']}: {s['status']}" for s in result.get('steps', [])])
        return

    if args.rollback:
        result = factory.rollback_pipeline.rollback(args.rollback)
        _print(f"⏪ 回滚到 {args.rollback}", [
            f"状态: {result['status']}",
            result.get('error', f"DNA: {result.get('dna', '-')}")
        ])
        return

    if args.versions:
        versions = factory.rollback_pipeline.list_versions()
        _print("📚 可回滚版本", [
            f"{v['version']} @ {v['timestamp']}" for v in versions
        ] or ["（暂无版本记录）"])
        return

    if args.circuit:
        breaker = factory.circuit_breaker.status()
        _print("🧯 熔断器状态", [
            f"DNA: {breaker['dna']}", f"熔断键: {breaker['tripped_keys']}",
            f"事件数: {breaker['event_count']}"
        ])
        return

    if args.kunpeng_health:
        result = factory.kunpeng.health_check()
        _print("🦅 鲲鹏健康检查", [
            f"状态: {result['status']}", result.get('output', '') or result.get('error', '')
        ])
        return

    if args.run:
        source_path = Path(args.run)
        if not source_path.exists():
            print(f"❌ 源路径不存在: {source_path}")
            return
        result = factory.run_full_cycle(source_path, args.version,
                                        target=args.target, notify=args.notify)
        _print("📊 工厂流程结果", [
            f"状态: {result['status']}", f"DNA: {result['dna']}"
        ] + [f"{step}: {json.dumps(data, ensure_ascii=False)[:120]}"
             for step, data in result.get('steps', {}).items()])
        return

    parser.print_help()


if __name__ == "__main__":
    main()
