#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂·行为密码学训练器
通过交互式输入采集 UID9622 的打字节奏，生成行为轮廓。

DNA: #龍芯⚡️丙午·乙未·丁酉·亥时·☰乾-IDENTITY-BEHAVIOR-v1.0
"""
import os
import sys
import json
import tty
import termios
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lh_identity_core import BehaviorCollector, BehaviorProfile, collect_device_fingerprint, now_utc


STATE_DIR = Path(__file__).resolve().parent.parent.parent / "state"
TRAINING_TEXT = "龍魂系统为人民服务，UID9622 守住数字主权。"


def read_single_key() -> str:
    """读取单个按键（不等待回车）。"""
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setcbreak(fd)
        ch = os.read(fd, 4).decode("utf-8", errors="ignore")
        return ch
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)


def train_session(rounds: int = 3) -> BehaviorProfile:
    """多轮训练，合并所有按键事件生成行为轮廓。"""
    collector = BehaviorCollector()
    print(f"[🧠] 行为密码学训练开始，共 {rounds} 轮。")
    print(f"[📌] 训练文案: 「{TRAINING_TEXT}」")
    print("[📌] 每轮请完整输入上述文案，按回车结束。按 Ctrl+C 可随时退出。\n")

    for r in range(1, rounds + 1):
        print(f"[第 {r}/{rounds} 轮] 请开始输入...")
        typed = ""
        while True:
            key = read_single_key()
            if key in ("\r", "\n"):
                break
            if key == "\x7f":  # backspace
                if typed:
                    typed = typed[:-1]
                    sys.stdout.write("\b \b")
                    sys.stdout.flush()
                continue
            if len(key) == 1 and key.isprintable():
                collector.record(key, "down")
                typed += key
                sys.stdout.write(key)
                sys.stdout.flush()
                collector.record(key, "up")

        print()  # newline
        if typed != TRAINING_TEXT:
            print(f"[⚠️] 输入不匹配，本轮作废。你输入的是: {typed}")
            continue

    # 命令习惯：从 bash history 提取高频命令
    top_commands = _extract_top_commands()

    profile = collector.build_profile(top_commands=top_commands)
    profile.updated_at = now_utc()
    return profile


def _extract_top_commands(max_commands: int = 10) -> list[str]:
    """从 bash history 提取高频命令动词。"""
    history_path = Path.home() / ".bash_history"
    if not history_path.exists():
        return []

    counts: dict[str, int] = {}
    try:
        for line in history_path.read_text(encoding="utf-8", errors="ignore").splitlines():
            cmd = line.strip().split()[0] if line.strip() else ""
            if cmd and not cmd.startswith("#"):
                counts[cmd] = counts.get(cmd, 0) + 1
    except Exception:
        return []

    return [cmd for cmd, _ in sorted(counts.items(), key=lambda x: x[1], reverse=True)[:max_commands]]


def main() -> int:
    import argparse
    parser = argparse.ArgumentParser(description="龍魂行为密码学训练器")
    parser.add_argument("--rounds", "-r", type=int, default=3, help="训练轮数")
    args = parser.parse_args()

    STATE_DIR.mkdir(parents=True, exist_ok=True)

    profile = train_session(args.rounds)
    print("\n[✅] 行为轮廓已生成:")
    print(json.dumps(profile.to_dict(), ensure_ascii=False, indent=2))

    behavior_path = STATE_DIR / "identity_behavior.json"
    behavior_path.write_text(json.dumps(profile.to_dict(), ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n[💾] 行为轮廓已保存: {behavior_path}")

    # 同时保存当前设备指纹哈希
    fp = collect_device_fingerprint()
    fp_path = STATE_DIR / "identity_device_fp.hash"
    fp_path.write_text(fp.fingerprint_hash, encoding="utf-8")
    print(f"[💾] 设备指纹哈希已保存: {fp_path}")

    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n[⚠️] 训练已取消。")
        sys.exit(1)
