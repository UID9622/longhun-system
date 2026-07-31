# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""
价格审计 - 数据模型 & 存储
DNA: #龍芯⚡️丙午·乙未·辛亥·巳时·☰乾-PRICE-MODELS-v1.0
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0
"""

import json
import os
from pathlib import Path
from datetime import datetime
from typing import Any

DATA_DIR = Path(__file__).parent.parent / "data"
REPORTS_FILE = DATA_DIR / "reports.jsonl"


def _ensure_data_dir():
    DATA_DIR.mkdir(parents=True, exist_ok=True)


def save_report(report: dict[str, Any]) -> str:
    """保存审计报告到JSONL文件。返回报告ID。"""
    _ensure_data_dir()
    report_id = datetime.now().strftime("%Y%m%d%H%M%S%f")[:16]
    report["report_id"] = report_id
    with open(REPORTS_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(report, ensure_ascii=False) + "\n")
    return report_id


def list_reports(limit: int = 20) -> list[dict]:
    """列出最近的审计报告。"""
    _ensure_data_dir()
    if not REPORTS_FILE.exists():
        return []
    reports = []
    with open(REPORTS_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                reports.append(json.loads(line))
    # 返回最近的
    reports.reverse()
    return reports[:limit]


def get_report(report_id: str) -> dict | None:
    """按ID获取单个报告。"""
    _ensure_data_dir()
    if not REPORTS_FILE.exists():
        return None
    with open(REPORTS_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                r = json.loads(line)
                if r.get("report_id") == report_id:
                    return r
    return None


def get_stats() -> dict:
    """获取全局统计信息。"""
    _ensure_data_dir()
    if not REPORTS_FILE.exists():
        return {"total_reports": 0, "suspicious_count": 0, "avg_score": 0}
    
    reports = []
    with open(REPORTS_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                reports.append(json.loads(line))
    
    total = len(reports)
    suspicious = sum(1 for r in reports if r.get("suspicious"))
    scores = [r.get("composite_assessment", {}).get("score", 0) for r in reports]
    avg_score = round(sum(scores) / len(scores), 1) if scores else 0
    
    return {
        "total_reports": total,
        "suspicious_count": suspicious,
        "suspicious_rate": f"{round(suspicious/total*100, 1)}%" if total else "0%",
        "avg_score": avg_score
    }
