# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂能力与训练自动迭代系统 · 训练自动迭代管线
DNA: #龍芯⚡️2026-06-28-LONGHUN-CAPABILITY-TRAIN-PIPELINE-v1.0

流程：监控 raw/ → 触发训练 → 测试生成质量 → 评估 → 备份旧模型 → 上线新模型
"""
import json
import shutil
import subprocess
import time
import hashlib
from pathlib import Path
from datetime import datetime

from config import Config
from auditor import Auditor


class TrainPipeline:
    """训练自动迭代管线。"""

    def __init__(self):
        self.auditor = Auditor(Config.train_log)
        self.raw_dir = Config.train_raw_dir
        self.train_script = Config.train_script
        self.report_path = Config.train_report_path
        self.active_marker = Config.active_model_marker
        self.backup_dir = Config.model_backup_dir

    def _compute_dir_hash(self):
        """计算 raw/ 目录内容哈希，用于判断是否有变化。"""
        h = hashlib.sha256()
        if not self.raw_dir.exists():
            return ""
        for file in sorted(self.raw_dir.rglob("*.txt")) + sorted(self.raw_dir.rglob("*.md")):
            try:
                stat = file.stat()
                h.update(f"{file}:{stat.st_size}:{stat.st_mtime}".encode())
            except Exception:
                pass
        return h.hexdigest()

    def get_state(self):
        if Config.train_state.exists():
            return json.loads(Config.train_state.read_text(encoding="utf-8"))
        return {"last_raw_hash": "", "last_train_at": None, "active_model": None}

    def save_state(self, state):
        Config.train_state.write_text(
            json.dumps(state, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )

    def has_new_corpus(self):
        state = self.get_state()
        current_hash = self._compute_dir_hash()
        return current_hash and current_hash != state.get("last_raw_hash")

    def trigger_train(self):
        """触发一次训练。"""
        dna = self.auditor.log(
            "train_trigger", input_data={"raw_dir": str(self.raw_dir)},
            status="running"
        )
        print(f"🚀 训练触发 DNA: {dna}")

        if not self.train_script.exists():
            msg = f"训练脚本不存在: {self.train_script}"
            self.auditor.log("train_failed", input_data={"dna": dna}, status="failed",
                             metadata={"reason": msg})
            return {"status": "failed", "error": msg, "dna": dna}

        # 执行训练脚本
        try:
            result = subprocess.run(
                [str(self.train_script)],
                capture_output=True, text=True, timeout=1800
            )
            if result.returncode != 0:
                raise RuntimeError(result.stderr or "训练脚本异常退出")
        except Exception as e:
            self.auditor.log("train_failed", input_data={"dna": dna}, status="failed",
                             metadata={"reason": str(e)})
            return {"status": "failed", "error": str(e), "dna": dna}

        # 读取训练报告
        if not self.report_path.exists():
            msg = "训练报告未生成"
            self.auditor.log("train_failed", input_data={"dna": dna}, status="failed",
                             metadata={"reason": msg})
            return {"status": "failed", "error": msg, "dna": dna}

        report = json.loads(self.report_path.read_text(encoding="utf-8"))
        self.auditor.log("train_done", input_data={"dna": dna},
                         output_data=report, status="success")

        # 更新状态
        state = self.get_state()
        state["last_raw_hash"] = self._compute_dir_hash()
        state["last_train_at"] = datetime.now().isoformat()
        state["last_report"] = report
        self.save_state(state)

        return {"status": "success", "report": report, "dna": dna}

    def test_generation(self):
        """简单测试生成质量：这里用 loss 作为代理指标。"""
        state = self.get_state()
        report = state.get("last_report")
        if not report:
            return {"status": "failed", "error": "没有训练报告"}
        history = report.get("history", [])
        if not history:
            return {"status": "failed", "error": "训练历史为空"}
        final_loss = history[-1].get("loss", float("inf"))
        test_dna = self.auditor.log(
            "train_test", input_data={"final_loss": final_loss},
            output_data={"passed": final_loss < 10.0}, status="success"
        )
        return {
            "status": "success",
            "final_loss": final_loss,
            "passed": final_loss < 10.0,
            "dna": test_dna,
        }

    def evaluate_and_deploy(self):
        """评估新模型并决定是否上线。"""
        state = self.get_state()
        report = state.get("last_report")
        if not report:
            return {"status": "failed", "error": "没有训练报告"}

        current_loss = report["history"][-1]["loss"]
        active = self.get_active_model()
        active_loss = active.get("loss") if active else None

        # 决定是否上线
        should_deploy = False
        if active_loss is None:
            should_deploy = True
            reason = "首次上线"
        elif active_loss == 0:
            should_deploy = False
            reason = "当前模型 loss 为 0，不替换"
        else:
            improvement = (active_loss - current_loss) / active_loss
            if improvement > Config.deploy_improvement_threshold:
                should_deploy = True
                reason = f"loss 下降 {improvement:.2%}，超过阈值"
            else:
                reason = f"loss 下降 {improvement:.2%}，未超过阈值 {Config.deploy_improvement_threshold}"

        deploy_dna = self.auditor.log(
            "train_evaluate",
            input_data={"current_loss": current_loss, "active_loss": active_loss},
            output_data={"should_deploy": should_deploy, "reason": reason},
            status="success"
        )

        if should_deploy:
            deploy_result = self.deploy(report)
            return {
                "status": "deployed",
                "reason": reason,
                "report": report,
                "deploy": deploy_result,
                "dna": deploy_dna,
            }

        return {
            "status": "kept",
            "reason": reason,
            "report": report,
            "dna": deploy_dna,
        }

    def deploy(self, report=None):
        """上线新模型：备份旧模型，复制新模型到 models/。"""
        report = report or self.get_state().get("last_report")
        if not report:
            return {"status": "failed", "error": "没有训练报告"}

        src_model = Path(report["model_path"])
        src_tokenizer = Path(report["tokenizer_path"])
        if not src_model.exists():
            return {"status": "failed", "error": f"模型文件不存在: {src_model}"}

        # 备份旧模型
        active = self.get_active_model()
        if active:
            old_model = Path(active.get("model_path", ""))
            old_tokenizer = Path(active.get("tokenizer_path", ""))
            if old_model.exists():
                ts = datetime.now().strftime("%Y%m%d%H%M%S")
                backup_path = self.backup_dir / f"model_{ts}.pt"
                shutil.copy2(old_model, backup_path)
                # 清理旧备份
                backups = sorted(self.backup_dir.glob("model_*.pt"))
                while len(backups) > Config.max_model_backups:
                    backups.pop(0).unlink()

        # 复制新模型
        dst_model = Config.model_dir / src_model.name
        dst_tokenizer = Config.model_dir / src_tokenizer.name
        shutil.copy2(src_model, dst_model)
        if src_tokenizer.exists():
            shutil.copy2(src_tokenizer, dst_tokenizer)

        active_info = {
            "model_path": str(dst_model),
            "tokenizer_path": str(dst_tokenizer),
            "loss": report["history"][-1]["loss"],
            "train_dna": report.get("dna"),
            "deployed_at": datetime.now().isoformat(),
        }
        self.active_marker.write_text(
            json.dumps(active_info, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )

        state = self.get_state()
        state["active_model"] = active_info
        self.save_state(state)

        dna = self.auditor.log(
            "train_deploy", input_data=report,
            output_data=active_info, status="success"
        )
        return {"status": "success", "active_model": active_info, "dna": dna}

    def rollback(self):
        """回滚到上一个备份模型。"""
        backups = sorted(self.backup_dir.glob("model_*.pt"))
        if not backups:
            return {"status": "failed", "error": "没有可回滚的备份"}
        latest_backup = backups[-1]
        dst = Config.model_dir / "龍魂-0.1B.pt"
        shutil.copy2(latest_backup, dst)

        dna = self.auditor.log(
            "train_rollback", input_data={"from": str(latest_backup)},
            output_data={"to": str(dst)}, status="success"
        )
        return {"status": "success", "from": str(latest_backup), "dna": dna}

    def get_active_model(self):
        if self.active_marker.exists():
            return json.loads(self.active_marker.read_text(encoding="utf-8"))
        return None

    def run_full_pipeline(self):
        """执行完整管线：训练 → 测试 → 评估 → 上线。"""
        train_result = self.trigger_train()
        if train_result["status"] != "success":
            return train_result

        test_result = self.test_generation()
        if not test_result.get("passed"):
            return test_result

        return self.evaluate_and_deploy()

    def status(self):
        state = self.get_state()
        active = self.get_active_model()
        return {
            "raw_dir": str(self.raw_dir),
            "has_new_corpus": self.has_new_corpus(),
            "last_train_at": state.get("last_train_at"),
            "active_model": active,
            "last_report": state.get("last_report"),
        }

    def logs(self, limit=20):
        if not Config.train_log.exists():
            return []
        lines = []
        with open(Config.train_log, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    lines.append(json.loads(line))
        return lines[-limit:]
