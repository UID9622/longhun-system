#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
执行遥测与多维评估模块
把每次人格运行、每次路由决策、每个关键事件落到 SQLite，
并生成五维评分（健康/完成/稳定/效率/主权）。
DNA: #龍芯⚡️2026-06-27-BACKEND-PERSONAS-TELEMETRY-v1.0
"""
import json
import sqlite3
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from .config import load_config, workspace_root


def _db_path() -> Path:
    cfg = load_config()
    root = Path(cfg.get("data_dir", workspace_root() / "data"))
    return root / "telemetry.db"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def init_db(db_path: Path = None):
    db_path = db_path or _db_path()
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(db_path), check_same_thread=False)
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS runs (
            run_id TEXT PRIMARY KEY,
            persona_code TEXT NOT NULL,
            persona_name TEXT,
            operation_type TEXT,
            source TEXT,
            device TEXT,
            parent_run_id TEXT,
            query TEXT,
            dna TEXT,
            started_at TEXT,
            finished_at TEXT,
            duration_ms INTEGER,
            status TEXT,
            metrics_json TEXT,
            scores_json TEXT
        );
        CREATE INDEX IF NOT EXISTS idx_runs_persona ON runs(persona_code);
        CREATE INDEX IF NOT EXISTS idx_runs_started ON runs(started_at);
        CREATE INDEX IF NOT EXISTS idx_runs_parent ON runs(parent_run_id);

        CREATE TABLE IF NOT EXISTS events (
            event_id TEXT PRIMARY KEY,
            run_id TEXT NOT NULL,
            event_type TEXT,
            details_json TEXT,
            dna TEXT,
            timestamp TEXT,
            FOREIGN KEY (run_id) REFERENCES runs(run_id)
        );
        CREATE INDEX IF NOT EXISTS idx_events_run ON events(run_id);

        CREATE TABLE IF NOT EXISTS routes (
            route_id TEXT PRIMARY KEY,
            run_id TEXT NOT NULL,
            target_type TEXT,
            target_code TEXT,
            target_name TEXT,
            score REAL,
            query TEXT,
            dna TEXT,
            timestamp TEXT,
            FOREIGN KEY (run_id) REFERENCES runs(run_id)
        );
        CREATE INDEX IF NOT EXISTS idx_routes_run ON routes(run_id);
        """
    )
    conn.commit()
    conn.close()


def _infer_source() -> str:
    if not sys.stdout.isatty():
        return "cron"
    return "cli"


def compute_scores(status: str, duration_ms: int, metrics: Dict[str, Any]) -> Dict[str, float]:
    """五维评分：健康、完成、稳定、效率、主权"""
    status = (status or "success").lower()
    health = 100.0 if status == "success" else (50.0 if status == "partial" else 0.0)

    # 完成度：按输出数量简单归一化
    completion = 100.0
    if "records" in metrics:
        completion = min(float(metrics["records"]) / 50.0 * 100.0, 100.0)
    elif "items" in metrics:
        completion = min(float(metrics["items"]) / 20.0 * 100.0, 100.0)
    elif "copied" in metrics or "skipped" in metrics:
        completion = min((float(metrics.get("copied", 0)) + float(metrics.get("skipped", 0))) / 20.0 * 100.0, 100.0)
    elif metrics.get("projects_created", 0) > 0 or metrics.get("files_created", 0) > 0:
        completion = 100.0
    elif "checks_passed" in metrics:
        completion = float(metrics["checks_passed"]) * 100.0

    # 稳定性：错误/冲突/告警扣分
    errors = float(metrics.get("errors", 0))
    conflicts = float(metrics.get("conflicts", 0))
    warnings = float(metrics.get("warnings", 0))
    stability = max(0.0, 100.0 - errors * 20.0 - conflicts * 10.0 - warnings * 5.0)

    # 效率：越快越高（50 秒内满分）
    seconds = max(duration_ms, 0) / 1000.0
    efficiency = max(0.0, 100.0 - seconds * 2.0)

    # 主权合规：红线/敏感事件扣分
    red_events = float(metrics.get("red_events", 0))
    yellow_events = float(metrics.get("yellow_events", 0))
    sensitive_found = float(metrics.get("sensitive_found", 0))
    sovereignty = max(0.0, 100.0 - red_events * 30.0 - yellow_events * 10.0 - sensitive_found * 15.0)

    overall = health * 0.25 + completion * 0.20 + stability * 0.20 + efficiency * 0.15 + sovereignty * 0.20
    return {
        "health": round(health, 2),
        "completion": round(completion, 2),
        "stability": round(stability, 2),
        "efficiency": round(efficiency, 2),
        "sovereignty": round(sovereignty, 2),
        "overall": round(overall, 2),
    }


def start_run(
    persona_code: str,
    persona_name: str,
    operation_type: str = "OP",
    source: Optional[str] = None,
    device: str = "MacBook",
    parent_run_id: Optional[str] = None,
    query: Optional[str] = None,
    dna: Optional[str] = None,
    db_path: Path = None,
) -> str:
    db_path = db_path or _db_path()
    init_db(db_path)
    run_id = str(uuid.uuid4())[:16]
    conn = sqlite3.connect(str(db_path), check_same_thread=False)
    conn.execute(
        """
        INSERT INTO runs (run_id, persona_code, persona_name, operation_type, source, device,
                          parent_run_id, query, dna, started_at, status, metrics_json, scores_json)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'running', '{}', '{}')
        """,
        (run_id, persona_code, persona_name, operation_type, source or _infer_source(), device,
         parent_run_id, query, dna, _now()),
    )
    conn.commit()
    conn.close()
    return run_id


def finish_run(
    run_id: str,
    status: str = "success",
    metrics: Optional[Dict[str, Any]] = None,
    db_path: Path = None,
):
    db_path = db_path or _db_path()
    metrics = metrics or {}
    conn = sqlite3.connect(str(db_path), check_same_thread=False)
    cur = conn.execute("SELECT started_at FROM runs WHERE run_id=?", (run_id,))
    row = cur.fetchone()
    duration_ms = 0
    if row and row[0]:
        started = datetime.fromisoformat(row[0])
        duration_ms = int((datetime.now(timezone.utc) - started).total_seconds() * 1000)
    scores = compute_scores(status, duration_ms, metrics)
    conn.execute(
        """
        UPDATE runs
        SET finished_at=?, duration_ms=?, status=?, metrics_json=?, scores_json=?
        WHERE run_id=?
        """,
        (_now(), duration_ms, status, json.dumps(metrics, ensure_ascii=False), json.dumps(scores, ensure_ascii=False), run_id),
    )
    conn.commit()
    conn.close()
    return scores


def log_event(run_id: str, event_type: str, details: Optional[Dict[str, Any]] = None, dna: Optional[str] = None, db_path: Path = None):
    db_path = db_path or _db_path()
    conn = sqlite3.connect(str(db_path), check_same_thread=False)
    conn.execute(
        "INSERT INTO events (event_id, run_id, event_type, details_json, dna, timestamp) VALUES (?, ?, ?, ?, ?, ?)",
        (str(uuid.uuid4())[:16], run_id, event_type, json.dumps(details or {}, ensure_ascii=False), dna, _now()),
    )
    conn.commit()
    conn.close()


def log_route(
    run_id: str,
    target_type: str,
    target_code: str,
    target_name: str,
    score: float,
    query: Optional[str] = None,
    dna: Optional[str] = None,
    db_path: Path = None,
):
    db_path = db_path or _db_path()
    conn = sqlite3.connect(str(db_path), check_same_thread=False)
    conn.execute(
        """
        INSERT INTO routes (route_id, run_id, target_type, target_code, target_name, score, query, dna, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (str(uuid.uuid4())[:16], run_id, target_type, target_code, target_name, score,
         query, dna, _now()),
    )
    conn.commit()
    conn.close()


def get_summary(db_path: Path = None) -> Dict[str, Any]:
    db_path = db_path or _db_path()
    init_db(db_path)
    conn = sqlite3.connect(str(db_path), check_same_thread=False)
    conn.row_factory = sqlite3.Row

    total_runs = conn.execute("SELECT COUNT(*) FROM runs").fetchone()[0]
    persona_counts = conn.execute(
        "SELECT persona_code, COUNT(*) as c FROM runs GROUP BY persona_code"
    ).fetchall()
    status_counts = conn.execute(
        "SELECT status, COUNT(*) as c FROM runs GROUP BY status"
    ).fetchall()
    recent = conn.execute(
        "SELECT * FROM runs ORDER BY started_at DESC LIMIT 20"
    ).fetchall()
    top_routes = conn.execute(
        "SELECT target_code, target_name, COUNT(*) as c FROM routes GROUP BY target_code ORDER BY c DESC LIMIT 10"
    ).fetchall()
    conn.close()

    def row_to_dict(row):
        d = dict(row)
        for k in ("metrics_json", "scores_json"):
            try:
                d[k.replace("_json", "")] = json.loads(d.pop(k))
            except Exception:
                d[k.replace("_json", "")] = {}
        return d

    return {
        "generated_at": _now(),
        "total_runs": total_runs,
        "persona_counts": {r["persona_code"]: r["c"] for r in persona_counts},
        "status_counts": {r["status"]: r["c"] for r in status_counts},
        "recent_runs": [row_to_dict(r) for r in recent],
        "top_routes": [dict(r) for r in top_routes],
    }


def get_runs(persona_code: Optional[str] = None, limit: int = 100, db_path: Path = None) -> List[Dict[str, Any]]:
    db_path = db_path or _db_path()
    conn = sqlite3.connect(str(db_path), check_same_thread=False)
    conn.row_factory = sqlite3.Row
    if persona_code:
        rows = conn.execute(
            "SELECT * FROM runs WHERE persona_code=? ORDER BY started_at DESC LIMIT ?",
            (persona_code, limit),
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT * FROM runs ORDER BY started_at DESC LIMIT ?", (limit,)
        ).fetchall()
    conn.close()
    result = []
    for r in rows:
        d = dict(r)
        for k in ("metrics_json", "scores_json"):
            try:
                d[k.replace("_json", "")] = json.loads(d.pop(k))
            except Exception:
                d[k.replace("_json", "")] = {}
        result.append(d)
    return result


class TelemetryCollector:
    """人格脚本内使用的便捷上下文。"""

    def __init__(
        self,
        persona_code: str,
        persona_name: str,
        operation_type: str = "OP",
        source: Optional[str] = None,
        device: str = "MacBook",
        parent_run_id: Optional[str] = None,
        query: Optional[str] = None,
        dna: Optional[str] = None,
    ):
        self.db_path = _db_path()
        init_db(self.db_path)
        self.run_id = start_run(
            persona_code=persona_code,
            persona_name=persona_name,
            operation_type=operation_type,
            source=source,
            device=device,
            parent_run_id=parent_run_id,
            query=query,
            dna=dna,
            db_path=self.db_path,
        )
        self._metrics: Dict[str, Any] = {}
        self._finished = False

    def set_metrics(self, metrics: Dict[str, Any]):
        self._metrics.update(metrics)

    def event(self, event_type: str, details: Optional[Dict[str, Any]] = None, dna: Optional[str] = None):
        log_event(self.run_id, event_type, details, dna, db_path=self.db_path)

    def route(self, target_type: str, target_code: str, target_name: str, score: float, query: Optional[str] = None, dna: Optional[str] = None):
        log_route(self.run_id, target_type, target_code, target_name, score, query, dna, db_path=self.db_path)

    def finish(self, status: str = "success", extra_metrics: Optional[Dict[str, Any]] = None):
        if self._finished:
            return
        if extra_metrics:
            self._metrics.update(extra_metrics)
        scores = finish_run(self.run_id, status, self._metrics, db_path=self.db_path)
        self._finished = True
        return scores

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.finish("success")
        else:
            self._metrics["error"] = str(exc_val)
            self.finish("error")
