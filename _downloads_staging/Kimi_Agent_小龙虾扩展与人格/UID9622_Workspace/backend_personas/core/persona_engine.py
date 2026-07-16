#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
轻量人格执行引擎
为全矩阵人格提供统一入口：日志 + 遥测 + DNA + 三色审计。
每个具体人格只需提供 code，由引擎自动从 persona_matrix.json 加载元数据。
DNA: #龍芯⚡️2026-06-27-UID9622-PERSONA-ENGINE-v1.0
"""
import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from core import AuditMark, DNATracer, SecurityFilter, TelemetryCollector, TricolorAudit, load_config, setup_logging, workspace_root


class PersonaEngine:
    """通用人格执行引擎。"""

    def __init__(self, code: str):
        self.code = code.upper()
        self.cfg = load_config()
        self.workspace = Path(self.cfg.get("workspace", workspace_root()))
        self.matrix_path = self.workspace / "backend_personas" / "persona_matrix.json"
        self.info = self._load_info()
        self.name = self.info.get("name", f"龍芯·{self.code}")
        self.agent_dna = self.info.get("dna") or f"#{self.code}-AGENT-CONFIG-20251214-001"
        self.log_file = Path(self.cfg.get("logs_dir", self.workspace / "logs")) / f"{self.code.lower()}.log"
        self.logger = setup_logging(self.code.lower(), self.log_file)
        self.dna_tracer = DNATracer(self.code, self.agent_dna)
        self.audit = TricolorAudit(Path(self.cfg.get("audit_dir", self.workspace / "logs" / "audit")))

    def _load_info(self) -> Dict[str, Any]:
        if not self.matrix_path.exists():
            return {"name": f"龍芯·{self.code}", "keywords": []}
        try:
            data = json.loads(self.matrix_path.read_text(encoding="utf-8"))
            return data.get(self.code, {"name": f"龍芯·{self.code}", "keywords": []})
        except Exception as e:
            return {"name": f"龍芯·{self.code}", "keywords": [], "load_error": str(e)}

    def _derive_task(self, text: Optional[str]) -> str:
        if text:
            return SecurityFilter.sanitize(text)
        return "heartbeat"

    def heartbeat(self, task: Optional[str] = None) -> Dict[str, Any]:
        """执行一次轻量心跳/任务，并返回遥测指标。"""
        task_label = self._derive_task(task)
        self.logger.info(AuditMark.tag(AuditMark.PURPLE, self.name, f"心跳任务: {task_label}"))
        op_dna = self.dna_tracer.generate("HEARTBEAT")
        self.audit.green(self.name, "心跳", {"task": task_label, "dna": op_dna})
        return {
            "persona": self.code,
            "name": self.name,
            "task": task_label,
            "heartbeat": 1,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "dna": op_dna,
        }

    def run(self, argv: Optional[list] = None) -> int:
        """命令行入口。"""
        parser = argparse.ArgumentParser(description=self.name)
        parser.add_argument("--heartbeat", action="store_true", help="发送一次心跳遥测")
        parser.add_argument("--task", default=None, help="执行一个简短任务描述并记录")
        parser.add_argument("--health-check", action="store_true", help="健康自检")
        parser.add_argument("--info", action="store_true", help="打印人格信息")
        parser.add_argument("--verbose", action="store_true", help="详细日志")
        args = parser.parse_args(argv)

        if args.info:
            print(json.dumps(self.info, ensure_ascii=False, indent=2))
            return 0

        if args.health_check:
            print(json.dumps({
                "code": self.code,
                "name": self.name,
                "status": "ok",
                "dna": self.agent_dna,
                "matrix_loaded": self.info.get("code") == self.code,
            }, ensure_ascii=False, indent=2))
            return 0

        operation_type = "HEARTBEAT" if args.heartbeat else ("TASK" if args.task else "HEARTBEAT")
        with TelemetryCollector(
            persona_code=self.code,
            persona_name=self.name,
            operation_type=operation_type,
            query=args.task,
            dna=self.agent_dna,
        ) as telemetry:
            try:
                result = self.heartbeat(task=args.task)
                telemetry.set_metrics({
                    "heartbeat": 1,
                    "task_recorded": 1 if args.task else 0,
                    "enabled": int(self.info.get("enabled", True)),
                })
                self.logger.info(AuditMark.tag(AuditMark.GREEN, self.name, f"完成 DNA: {result['dna']}"))
                print(json.dumps(result, ensure_ascii=False))
            except Exception as e:
                self.logger.error(AuditMark.tag(AuditMark.RED, self.name, f"运行失败: {e}"))
                telemetry.finish("error", {"error": str(e)})
                return 1
        return 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python3 persona_engine.py <CODE> [--heartbeat|--task ...]")
        sys.exit(1)
    sys.exit(PersonaEngine(sys.argv[1]).run(sys.argv[2:]))
