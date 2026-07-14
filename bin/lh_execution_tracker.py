#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════╗
║     💪 龍魂 · 肌肉系统 · 执行追踪引擎 v1.0                    ║
║                                                                  ║
║  生物映射：肌肉系统 → 动作执行 → 脚本执行追踪/成功率监控          ║
║  五行归属：火                                                    ║
║                                                                  ║
║  DNA: #龍芯⚡️丙午·辛未·肌肉系统-EXECUTION-TRACKER-v1.0          ║
╚══════════════════════════════════════════════════════════════╝

用法:
  python3 bin/lh_execution_tracker.py --track <script>  # 执行并追踪脚本
  python3 bin/lh_execution_tracker.py --report          # 执行报告
  python3 bin/lh_execution_tracker.py --test-all        # 批量测试核心脚本可执行性
"""

import hashlib
import json
import os
import subprocess
import sys
import time
import traceback
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

ROOT = Path(__file__).resolve().parent.parent
STATE_DIR = Path.home() / ".longhun" / "ant_colony"
STATE_DIR.mkdir(parents=True, exist_ok=True)
EXEC_LOG = STATE_DIR / "execution_log.jsonl"
EXEC_REPORT = STATE_DIR / "execution_report.json"

DNA = "#龍芯⚡️丙午·辛未·肌肉系统-EXECUTION-TRACKER-v1.0"


@dataclass
class ExecutionRecord:
    """执行记录——一次肌肉运动"""
    exec_id: str
    script_path: str
    script_name: str
    start_time: str
    end_time: str = ""
    duration_ms: float = 0
    exit_code: int = -1
    status: str = "pending"  # pending / running / success / failed / timeout
    error_message: str = ""
    output_summary: str = ""
    retry_count: int = 0


class ExecutionTracker:
    """肌肉系统：追踪所有核心脚本的执行状态"""

    # 核心脚本清单（必须有执行能力的"肌肉"）
    CORE_MUSCLES = [
        "bin/lh_ant_colony_orchestrator.py",
        "bin/lh_rb_confrontation_engine.py",
        "bin/lh_persona_signing.py",
        "bin/lh_oversight_bridge.py",
        "bin/lh_biometric_health.py",
        "bin/lh_flow_pipeline.py",
        "bin/lh_signal_relay.py",
        "bin/lh_resource_monitor.py",
        "bin/lh_input_pipeline.py",
        "bin/lh_memory_load.py",
        "bin/lh_unified_pipeline.py",
        "bin/lh_health_check.py",
    ]

    def __init__(self):
        self.report = self._load_report()

    def _load_report(self) -> Dict:
        if EXEC_REPORT.exists():
            return json.loads(EXEC_REPORT.read_text())
        return {"total_executions": 0, "success_count": 0, "fail_count": 0,
                "last_report": "", "muscle_health": {}}

    def _save_report(self):
        EXEC_REPORT.write_text(json.dumps(self.report, ensure_ascii=False, indent=2))

    def track(self, script_rel_path: str, args: List[str] = None,
              timeout: int = 60, dry_run: bool = False) -> ExecutionRecord:
        """
        执行并追踪一个脚本
        
        参数:
          script_rel_path: 相对于ROOT的脚本路径
          args: 额外参数
          timeout: 超时秒数
          dry_run: 仅检查语法不实际执行
        """
        script_path = ROOT / script_rel_path
        if not script_path.exists():
            return ExecutionRecord(
                exec_id="N/A", script_path=str(script_path),
                script_name=script_path.name, start_time="",
                status="failed", error_message=f"文件不存在: {script_path}"
            )

        now = datetime.now().isoformat()
        exec_id = hashlib.sha256(f"{script_rel_path}-{now}".encode()).hexdigest()[:12]

        record = ExecutionRecord(
            exec_id=exec_id,
            script_path=str(script_path),
            script_name=script_path.name,
            start_time=now,
            status="running",
        )

        # Dry run: 仅语法检查
        if dry_run:
            try:
                with open(script_path) as f:
                    compile(f.read(), script_path.name, 'exec')
                record.status = "success"
                record.exit_code = 0
                record.end_time = datetime.now().isoformat()
            except SyntaxError as e:
                record.status = "failed"
                record.error_message = f"语法错误: {e}"
            self._persist(record)
            return record

        # 实际执行
        cmd = ["python3", str(script_path)]
        if args:
            cmd.extend(args)

        try:
            start = time.time()
            result = subprocess.run(
                cmd, capture_output=True, text=True, timeout=timeout,
                cwd=str(ROOT),
            )
            duration = (time.time() - start) * 1000

            record.duration_ms = round(duration, 1)
            record.exit_code = result.returncode
            record.end_time = datetime.now().isoformat()

            if result.returncode == 0:
                record.status = "success"
                record.output_summary = result.stdout[:200] if result.stdout else ""
            else:
                record.status = "failed"
                record.error_message = result.stderr[:300] if result.stderr else f"exit={result.returncode}"

        except subprocess.TimeoutExpired:
            record.status = "timeout"
            record.error_message = f"超时 ({timeout}s)"
        except Exception as e:
            record.status = "failed"
            record.error_message = f"{type(e).__name__}: {str(e)}"

        self._persist(record)
        self._update_muscle_health(record)
        return record

    def _persist(self, record: ExecutionRecord):
        with open(EXEC_LOG, "a") as f:
            f.write(json.dumps({
                "exec_id": record.exec_id,
                "script": record.script_name,
                "status": record.status,
                "exit_code": record.exit_code,
                "duration_ms": record.duration_ms,
                "error": record.error_message[:200],
                "timestamp": record.start_time,
            }, ensure_ascii=False) + "\n")

    def _update_muscle_health(self, record: ExecutionRecord):
        """更新肌肉健康度"""
        name = record.script_name
        if name not in self.report["muscle_health"]:
            self.report["muscle_health"][name] = {"success": 0, "total": 0, "health": 1.0}

        mh = self.report["muscle_health"][name]
        mh["total"] += 1
        if record.status == "success":
            mh["success"] += 1
            self.report["success_count"] += 1
        else:
            self.report["fail_count"] += 1

        mh["health"] = round(mh["success"] / max(mh["total"], 1), 2)
        self.report["total_executions"] += 1
        self._save_report()

    def test_all_core(self) -> Dict:
        """测试所有核心肌肉（dry run + 小部分实际执行）"""
        results = {}
        for path in self.CORE_MUSCLES:
            full_path = ROOT / path
            if not full_path.exists():
                results[path] = {"status": "missing", "health": 0.0}
                continue

            # Dry run
            record = self.track(path, args=["--help"], timeout=10, dry_run=False)
            results[path] = {
                "status": record.status,
                "duration_ms": record.duration_ms,
                "exit_code": record.exit_code,
                "error": record.error_message[:100] if record.error_message else "",
            }

        available = sum(1 for r in results.values() if r["status"] not in ("failed", "missing", "timeout"))
        total = len(self.CORE_MUSCLES)

        return {
            "dna": DNA,
            "tested": total,
            "available": available,
            "unavailable": total - available,
            "muscle_availability": round(available / total, 2),
            "details": results,
        }

    def report_summary(self) -> Dict:
        """执行报告摘要"""
        recent_logs = []
        if EXEC_LOG.exists():
            lines = EXEC_LOG.read_text().splitlines()
            recent_logs = [json.loads(l) for l in lines[-20:] if l.strip()]

        success_rate = round(
            self.report["success_count"] / max(self.report["total_executions"], 1), 3
        )

        weak_muscles = [
            (name, data["health"])
            for name, data in self.report["muscle_health"].items()
            if data["health"] < 0.5 and data["total"] > 2
        ]

        return {
            "dna": DNA,
            "total_executions": self.report["total_executions"],
            "success_rate": success_rate,
            "weak_muscles": weak_muscles,
            "muscle_health": self.report["muscle_health"],
            "recent_executions": recent_logs[-5:],
            "status": "🟢" if success_rate > 0.9 else "🟡" if success_rate > 0.7 else "🔴",
        }


def main():
    import argparse
    parser = argparse.ArgumentParser(description="龍魂·肌肉系统·执行追踪")
    parser.add_argument("--track", type=str, help="执行并追踪脚本")
    parser.add_argument("--args", type=str, help="脚本额外参数")
    parser.add_argument("--timeout", type=int, default=60, help="超时(秒)")
    parser.add_argument("--report", action="store_true", help="执行报告")
    parser.add_argument("--test-all", action="store_true", help="批量测试核心脚本")
    parser.add_argument("--json", action="store_true", help="JSON输出")

    args = parser.parse_args()
    tracker = ExecutionTracker()

    if args.track:
        extra = args.args.split() if args.args else None
        record = tracker.track(args.track, args=extra, timeout=args.timeout)
        print(f"执行: [{record.status}] {record.script_name} "
              f"({record.duration_ms}ms) exit={record.exit_code}")
        if record.error_message:
            print(f"  错误: {record.error_message[:200]}")
        return 0

    if args.test_all:
        result = tracker.test_all_core()
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(f"\n💪 肌肉测试: {result['available']}/{result['tested']}可用 "
                  f"({result['muscle_availability']:.0%})")
            for path, detail in result["details"].items():
                icon = "✅" if detail["status"] == "success" else "❌"
                print(f"  {icon} {path:<45s} {detail['status']}")
        return 0

    if args.report:
        r = tracker.report_summary()
        if args.json:
            print(json.dumps(r, ensure_ascii=False, indent=2))
        else:
            print(f"\n💪 肌肉系统: {r['status']} 成功率{r['success_rate']:.0%}")
            print(f"  总执行: {r['total_executions']}")
            if r["weak_muscles"]:
                print("  弱肌肉:")
                for name, health in r["weak_muscles"]:
                    print(f"    {name}: 健康度{health:.0%}")
        return 0

    # 默认
    r = tracker.report_summary()
    print(f"肌肉系统就绪 · 成功率{r['success_rate']:.0%}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
