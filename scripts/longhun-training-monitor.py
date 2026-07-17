#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂训练状态管理器 v1.0
DNA: #龍芯⚡️丙午·辛未·TRAINING-MONITOR-v1.0

管理模型训练过程状态，通过文件系统供面板API轮询。
状态文件路径: models/.training_status / .training_lock / .training_done_vN

面板每2秒轮询 /training/status 获取进度，实现实时可视化。
"""

import json
import os
import time
from pathlib import Path
from datetime import datetime, timezone, timedelta
from typing import Optional, Dict, Any, List

LONGHUN_ROOT = Path.home() / "longhun-system"
MODEL_DIR = LONGHUN_ROOT / "models"
STATUS_FILE = MODEL_DIR / ".training_status"
LOCK_FILE = MODEL_DIR / ".training_lock"

DNA = "UID9622-ONLY-ONCE🧬LK9X-772Z"
UID = "UID9622"
CST = timezone(timedelta(hours=8))

MODEL_DIR.mkdir(parents=True, exist_ok=True)


class TrainingMonitor:
    """训练过程监控，写入状态文件供面板轮询读取"""

    def __init__(self):
        self.status: Dict[str, Any] = {
            "state": "idle",
            "from_version": 0,
            "to_version": 0,
            "progress": 0.0,
            "stage": "",
            "metrics": {},
            "started_at": 0,
            "estimated_complete": 0,
            "error": None,
            "dna": DNA,
        }

    def start(self, from_version: int, to_version: int):
        """开始训练"""
        now = int(time.time())
        self.status = {
            "state": "preparing",
            "from_version": from_version,
            "to_version": to_version,
            "progress": 0.0,
            "stage": "准备训练数据...",
            "metrics": {},
            "started_at": now,
            "estimated_complete": now + 300,
            "completed_at": 0,
            "error": None,
            "dna": DNA,
        }
        self._save()

        LOCK_FILE.write_text(
            json.dumps({
                "pid": os.getpid(),
                "started_at": now,
                "from_version": from_version,
                "to_version": to_version,
            })
        )

    def update(self, progress: float, stage: str, metrics: Optional[dict] = None):
        """更新进度"""
        self.status["progress"] = min(100.0, max(0.0, progress))
        self.status["stage"] = stage
        if metrics:
            self.status["metrics"] = metrics

        elapsed = int(time.time()) - self.status["started_at"]
        if progress > 0:
            total_estimated = elapsed / (progress / 100)
            remaining = total_estimated - elapsed
            self.status["estimated_complete"] = int(time.time()) + int(remaining)

        self._save()

    def set_state(self, state: str):
        """设置状态"""
        self.status["state"] = state
        self._save()

    def complete(self, metrics: Dict[str, Any]):
        """训练完成"""
        now = int(time.time())
        self.status["state"] = "done"
        self.status["progress"] = 100.0
        self.status["stage"] = "切换完成"
        self.status["metrics"] = metrics
        self.status["completed_at"] = now
        self._save()

        if LOCK_FILE.exists():
            LOCK_FILE.unlink()

        done_file = MODEL_DIR / f".training_done_v{self.status['to_version']}"
        done_file.write_text(json.dumps({
            "version": self.status["to_version"],
            "completed_at": now,
            "metrics": metrics,
        }))

    def error(self, message: str):
        """训练失败"""
        now = int(time.time())
        self.status["state"] = "error"
        self.status["stage"] = f"错误: {message}"
        self.status["error"] = message
        self.status["completed_at"] = now
        self._save()

        if LOCK_FILE.exists():
            LOCK_FILE.unlink()

    def _save(self):
        STATUS_FILE.write_text(json.dumps(self.status, ensure_ascii=False))

    @staticmethod
    def get_status() -> Dict[str, Any]:
        """读取当前状态（供API调用）"""
        if not STATUS_FILE.exists():
            return {"state": "idle", "dna": DNA}

        try:
            status = json.loads(STATUS_FILE.read_text())
            # 添加动态时间字段
            if status.get("started_at"):
                elapsed = int(time.time()) - status["started_at"]
                status["elapsed_seconds"] = elapsed
                status["elapsed_formatted"] = TrainingMonitor._format_time(elapsed)
            if status.get("estimated_complete"):
                remaining = max(0, status["estimated_complete"] - int(time.time()))
                status["remaining_seconds"] = remaining
                status["remaining_formatted"] = TrainingMonitor._format_time(remaining)
            return status
        except (json.JSONDecodeError, IOError):
            return {"state": "unknown", "dna": DNA}

    @staticmethod
    def is_training() -> bool:
        """检查是否正在训练"""
        if not LOCK_FILE.exists():
            return False
        try:
            lock = json.loads(LOCK_FILE.read_text())
            pid = lock.get("pid")
            if pid:
                try:
                    os.kill(pid, 0)
                    return True
                except OSError:
                    pass
            # 进程已死，清理
            LOCK_FILE.unlink()
            STATUS_FILE.write_text(json.dumps({
                "state": "error", "stage": "训练进程异常终止",
                "error": "Process died", "dna": DNA, "progress": 0,
                "from_version": 0, "to_version": 0,
                "started_at": 0, "estimated_complete": 0,
                "completed_at": int(time.time()), "metrics": {},
            }))
        except (json.JSONDecodeError, IOError):
            LOCK_FILE.unlink()
        return False

    @staticmethod
    def get_model_version() -> Dict[str, Any]:
        """获取当前模型版本信息"""
        version_file = MODEL_DIR / "model_version.json"
        default = {
            "version": 0, "previous_version": 0,
            "switched_at": 0, "metrics": {"accuracy": 0, "f1": 0},
            "training_samples": 0, "dna": DNA, "status": "not_trained",
        }

        if not version_file.exists():
            return default

        try:
            info = json.loads(version_file.read_text())
            info["status"] = "active"
            uptime = int(time.time()) - info.get("switched_at", 0)
            info["uptime_seconds"] = uptime
            info["uptime_formatted"] = TrainingMonitor._format_time(uptime)

            pending_file = MODEL_DIR / ".pending_version"
            if pending_file.exists():
                try:
                    info["pending_version"] = json.loads(pending_file.read_text())
                except Exception:
                    pass

            return info
        except (json.JSONDecodeError, IOError) as e:
            return {**default, "error": str(e)}

    @staticmethod
    def get_model_history(limit: int = 10) -> Dict[str, Any]:
        """获取模型版本历史"""
        archive_dir = MODEL_DIR / "archive"
        if not archive_dir.exists():
            return {"total": 0, "history": [], "current": TrainingMonitor.get_model_version()}

        archives = sorted(archive_dir.glob("appeal_classifier_v*.pkl"), reverse=True)
        history = []
        for archive in archives[:limit]:
            name = archive.name
            try:
                ver_str = name.split("_v")[1].split("_")[0]
                version = int(ver_str) if ver_str.isdigit() else ver_str
            except (IndexError, ValueError):
                version = "unknown"

            stat = archive.stat()
            history.append({
                "version": version,
                "file": name,
                "size_bytes": stat.st_size,
                "size_mb": round(stat.st_size / 1024 / 1024, 2),
                "archived_at": int(stat.st_mtime),
                "archived_at_str": datetime.fromtimestamp(stat.st_mtime, CST).strftime("%Y-%m-%d %H:%M"),
                "path": str(archive),
            })

        return {
            "total_archives": len(archives),
            "history": history,
            "current": TrainingMonitor.get_model_version(),
        }

    @staticmethod
    def _format_time(seconds: int) -> str:
        if seconds < 60:
            return f"{seconds}s"
        elif seconds < 3600:
            return f"{seconds // 60}m{seconds % 60}s"
        else:
            h = seconds // 3600
            m = (seconds % 3600) // 60
            return f"{h}h{m:02d}m"


HISTORY_DIR = MODEL_DIR / "history"
HISTORY_DIR.mkdir(parents=True, exist_ok=True)


class TrainingHistory:
    """训练历史记录管理 + 时间轴数据"""

    @staticmethod
    def record_version(data: Dict[str, Any]) -> Dict[str, Any]:
        """记录版本信息到历史目录"""
        version = data.get("version", 0)
        now = int(time.time())
        record = {
            "version": version,
            "previous_version": data.get("previous_version", 0),
            "trained_at": data.get("trained_at", now),
            "switched_at": data.get("switched_at", now),
            "metrics": {
                "accuracy": data.get("metrics", {}).get("accuracy", 0),
                "f1": data.get("metrics", {}).get("f1", 0),
                "training_samples": data.get("training_samples", 0),
                "training_duration": data.get("training_duration", 0),
            },
            "dna": DNA,
            "trigger_reason": data.get("trigger_reason", "manual"),
            "ab_test_result": data.get("ab_test_result", "pass"),
            "model_size_bytes": data.get("model_size_bytes", 0),
            "features": data.get("features", []),
        }

        file_path = HISTORY_DIR / f"version_{version}_{record['trained_at']}.json"
        file_path.write_text(json.dumps(record, ensure_ascii=False, indent=2))

        # 更新索引
        index_file = HISTORY_DIR / "index.json"
        index = []
        if index_file.exists():
            try:
                index = json.loads(index_file.read_text())
            except Exception:
                pass

        index = [i for i in index if i["version"] != version]
        index.append({
            "version": version,
            "trained_at": record["trained_at"],
            "accuracy": record["metrics"]["accuracy"],
            "file": file_path.name,
        })
        index.sort(key=lambda x: x["trained_at"])
        index_file.write_text(json.dumps(index, ensure_ascii=False, indent=2))

        return record

    @staticmethod
    def get_timeline(limit: int = 20) -> List[Dict[str, Any]]:
        """获取时间轴数据（带进化指标）"""
        index_file = HISTORY_DIR / "index.json"
        if not index_file.exists():
            return []

        try:
            index = json.loads(index_file.read_text())
        except Exception:
            return []

        timeline = []
        for item in index[-limit:]:
            file_path = HISTORY_DIR / item["file"]
            if file_path.exists():
                try:
                    data = json.loads(file_path.read_text())
                    timeline.append(data)
                except Exception:
                    pass

        # 计算进化指标
        for i, item in enumerate(timeline):
            if i > 0:
                prev = timeline[i - 1]
                item["evolution"] = {
                    "accuracy_delta": item["metrics"]["accuracy"] - prev["metrics"]["accuracy"],
                    "samples_delta": item["metrics"]["training_samples"] - prev["metrics"]["training_samples"],
                    "time_since_last": item["trained_at"] - prev["trained_at"],
                }
            else:
                item["evolution"] = {
                    "accuracy_delta": 0,
                    "samples_delta": 0,
                    "time_since_last": 0,
                }

        return timeline

    @staticmethod
    def get_stats() -> Dict[str, Any]:
        """获取统计摘要"""
        timeline = TrainingHistory.get_timeline(limit=1000)

        if not timeline:
            return {
                "total_versions": 0,
                "first_train": None,
                "latest_version": 0,
                "best_accuracy": 0,
                "avg_accuracy": 0,
                "total_samples_growth": 0,
                "training_frequency": 0,
            }

        accuracies = [t["metrics"]["accuracy"] for t in timeline]
        samples = [t["metrics"]["training_samples"] for t in timeline]

        total_span = max(1, timeline[-1]["trained_at"] - timeline[0]["trained_at"])
        return {
            "total_versions": len(timeline),
            "first_train": timeline[0]["trained_at"],
            "latest_version": timeline[-1]["version"],
            "best_accuracy": round(max(accuracies) * 100, 1),
            "avg_accuracy": round((sum(accuracies) / len(accuracies)) * 100, 1),
            "total_samples_growth": samples[-1] - samples[0] if len(samples) > 1 else 0,
            "training_frequency": round(len(timeline) / (total_span / 86400), 2) if total_span > 0 else 0,
        }


# ── 入口（直接运行时显示状态） ──
if __name__ == "__main__":
    print(f"🐉 龍魂训练状态管理器 v1.0")
    print(f"   DNA: {DNA}")
    print(f"   状态文件: {STATUS_FILE}")
    print(f"   锁文件: {LOCK_FILE}")
    print()

    status = TrainingMonitor.get_status()
    print(f"   当前状态: {status.get('state', 'unknown')}")
    print(f"   进度: {status.get('progress', 0):.1f}%")
    print(f"   阶段: {status.get('stage', '-')}")
    print(f"   是否训练中: {TrainingMonitor.is_training()}")

    mv = TrainingMonitor.get_model_version()
    print(f"\n   模型版本: v{mv.get('version', 0)}")
    print(f"   准确率: {mv.get('metrics', {}).get('accuracy', 0):.1%}")
    print(f"   训练样本: {mv.get('training_samples', 0)}")

    timeline = TrainingHistory.get_timeline(limit=5)
    if timeline:
        print(f"\n   训练历史 ({len(timeline)}版本):")
        for t in timeline:
            evo = t.get("evolution", {})
            delta = f" (+{evo.get('accuracy_delta', 0):.2%})" if evo.get("accuracy_delta", 0) > 0 else ""
            print(f"     v{t['version']}: {t['metrics']['accuracy']:.2%}{delta} | {t['metrics']['training_samples']}样本")
