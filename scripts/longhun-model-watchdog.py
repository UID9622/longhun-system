#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂AI模型看门狗 v1.0
DNA: #龍芯⚡️丙午·辛未·MODEL-WATCHDOG-v1.0

实时检测人格链变更 → 自动触发重训练 → A/B验证 → 原子切换。
支持 mac LaunchAgent 守护 + crontab 双重保险。
"""

import hashlib
import json
import os
import subprocess
import sys
import threading
import time
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Optional, Dict, Any

LONGHUN_ROOT = Path.home() / "longhun-system"
PERSONA_DIR = LONGHUN_ROOT / "persona-chain"
MODEL_DIR = LONGHUN_ROOT / "models"
SCRIPTS_DIR = LONGHUN_ROOT / "scripts"
TRIGGER_FILE = MODEL_DIR / ".retrain_trigger"
STATE_FILE = MODEL_DIR / ".watchdog_state"
VERSION_FILE = MODEL_DIR / "model_version.json"

DNA = "UID9622-ONLY-ONCE🧬LK9X-772Z"
UID = "UID9622"
CST = timezone(timedelta(hours=8))

MODEL_DIR.mkdir(parents=True, exist_ok=True)


class ModelWatchdog:
    """人格链变更检测 + 自动重训练触发"""

    def __init__(self, interval: int = 60):
        self.interval = interval
        self.running = False
        self.training_in_progress = False
        self.state = self._load_state()

    def _load_state(self) -> Dict[str, Any]:
        if STATE_FILE.exists():
            try:
                return json.loads(STATE_FILE.read_text())
            except (json.JSONDecodeError, IOError):
                pass
        return {"hash": "", "timestamp": 0, "version": 0}

    def _save_state(self, hash_val: str, version: int):
        self.state = {
            "hash": hash_val,
            "timestamp": int(time.time()),
            "version": version,
            "dna": DNA,
        }
        STATE_FILE.write_text(json.dumps(self.state))

    def _compute_hash(self) -> str:
        """计算人格链目录最新文件哈希"""
        chain_files = sorted(PERSONA_DIR.glob("persona-chain-*.json"))
        if not chain_files:
            return ""
        latest = chain_files[-1]
        content = latest.read_bytes()
        return hashlib.sha256(content).hexdigest()[:16]

    def _get_current_version(self) -> int:
        """从 model_version.json 读取当前版本"""
        if VERSION_FILE.exists():
            try:
                return json.loads(VERSION_FILE.read_text()).get("current_version", 0)
            except Exception:
                pass
        return 0

    def _trigger_retrain(self, old_hash: str, new_hash: str):
        """触发重训练"""
        old_version = self._get_current_version()
        new_version = old_version + 1

        print(f"\n[{self._ts()}] 🔔 人格链变更检测!")
        print(f"    旧哈希: {old_hash}")
        print(f"    新哈希: {new_hash}")
        print(f"    旧版本: v{old_version}")

        if self.training_in_progress:
            print(f"    ⚠️ 训练进行中，跳过本次触发")
            return

        trigger = {
            "triggered_at": int(time.time()),
            "old_version": old_version,
            "new_version": new_version,
            "new_hash": new_hash,
            "reason": "persona_chain_updated",
            "dna": DNA,
        }
        TRIGGER_FILE.write_text(json.dumps(trigger))

        self.training_in_progress = True
        threading.Thread(target=self._run_retrain, args=(old_version, new_version), daemon=True).start()

    def _run_retrain(self, old_version: int, new_version: int):
        """异步执行重训练"""
        retrainer_path = SCRIPTS_DIR / "longhun-appeal-retrainer-v2.py"

        cmd = [
            sys.executable, str(retrainer_path),
            "--version", str(new_version),
            "--from-version", str(old_version),
        ]

        print(f"[{self._ts()}] 🐉 启动模型重训练: v{old_version} → v{new_version}")
        print(f"    命令: {' '.join(cmd)}")

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=600,
                cwd=str(LONGHUN_ROOT),
            )

            if result.returncode == 0:
                print(f"{result.stdout.strip()[-200:]}")
                print(f"[{self._ts()}] ✅ 重训练完成: v{new_version}")
                self._save_state(self._compute_hash(), new_version)
                if TRIGGER_FILE.exists():
                    TRIGGER_FILE.unlink()
            else:
                print(f"[{self._ts()}] ❌ 重训练失败 (exit={result.returncode})")
                print(f"    stderr: {result.stderr[:300]}")

        except subprocess.TimeoutExpired:
            print(f"[{self._ts()}] ⏱️ 重训练超时（>10分钟），保留旧版本 v{old_version}")
        except FileNotFoundError:
            print(f"[{self._ts()}] ❌ 重训练器未找到: {retrainer_path}")
            # fallback: 使用基础训练器
            fallback_path = SCRIPTS_DIR / "longhun-appeal-trainer.py"
            if fallback_path.exists():
                print(f"[{self._ts()}] 🔄 回退到基础训练器...")
                try:
                    subprocess.run(
                        [sys.executable, str(fallback_path), "--force"],
                        timeout=600,
                        cwd=str(LONGHUN_ROOT),
                    )
                except Exception as e:
                    print(f"[{self._ts()}] ❌ fallback训练也失败: {e}")
        except Exception as e:
            print(f"[{self._ts()}] ❌ 重训练异常: {e}")

        self.training_in_progress = False

    def watch(self):
        """持续监控入口"""
        self.running = True
        print(f"🐉 龍魂模型看门狗 v1.0 启动")
        print(f"   DNA: {DNA}")
        print(f"   监控路径: {PERSONA_DIR}")
        print(f"   检测间隔: {self.interval}秒")
        print(f"   当前版本: v{self._get_current_version()}")
        print(f"   上次哈希: {self.state.get('hash', '(无)')[:16]}")
        print("   按 Ctrl+C 停止")
        print(f"   [{self._ts()}] 开始监控...\n")

        while self.running:
            try:
                current_hash = self._compute_hash()
                previous_hash = self.state.get("hash", "")

                if current_hash and current_hash != previous_hash:
                    self._trigger_retrain(previous_hash, current_hash)
                else:
                    # 打印心跳（每5分钟一次）
                    if int(time.time()) % 300 < self.interval:
                        print(f"[{self._ts()}] ✅ 人格链无变更 | 当前版本 v{self._get_current_version()}")

                time.sleep(self.interval)

            except KeyboardInterrupt:
                print(f"\n[{self._ts()}] 👋 看门狗停止")
                self.running = False
            except Exception as e:
                print(f"[{self._ts()}] ⚠️ 监控异常: {e}")
                time.sleep(self.interval)

    @staticmethod
    def _ts() -> str:
        return datetime.now(CST).strftime("%H:%M:%S")


# ── 入口 ──
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="龍魂模型看门狗")
    parser.add_argument("--interval", type=int, default=60, help="检测间隔（秒）")
    parser.add_argument("--once", action="store_true", help="仅检查一次")
    args = parser.parse_args()

    watchdog = ModelWatchdog(interval=args.interval)

    if args.once:
        current_hash = watchdog._compute_hash()
        prev_hash = watchdog.state.get("hash", "")
        print(f"当前哈希: {current_hash}")
        print(f"上次哈希: {prev_hash}")
        print(f"需要重训: {current_hash != prev_hash}")
        print(f"当前版本: v{watchdog._get_current_version()}")
        if current_hash != prev_hash and prev_hash:
            watchdog._trigger_retrain(prev_hash, current_hash)
            time.sleep(2)  # 等线程输出
        sys.exit(0)

    watchdog.watch()
