#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# DNA: #龍芯⚡️丙午·丁酉·壬午·巳时·䷘无妄-TRAIN-ROLLBACK-GUARD-v1.0-AUTO
# CREATOR: 诸葛鑫 (UID9622)
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# -*- coding: utf-8 -*-
"""
🐉 龍魂 训练/测试 回滚守护壳 v1.0
DNA: #龍芯⚡️丙午·丁酉·壬午·巳时·䷘无妄-TRAIN-ROLLBACK-GUARD-v1.0-AUTO

触发源: 2026-09-05 老大白话「有些数据在跑，如果说触发就是走坏了，这个码要回滚，
        要触发回滚这个机制」→ 实证: v4.2.0 训练曾 METAL GPU Internal Error 崩溃
        (iter720·无任何 run 档案/回滚留痕)。

职责（三条铁律落地）:
  1. 测试/训练数据全部收集好   → 每次 run 全量落 ~/.longhun/train_runs/runs.jsonl
     （起止/参数/退出码/崩溃原因/产物哈希/回滚事件），日志 tee 保留
  2. 走坏即触发                → 子进程退出码 != 0 + 特征词分类
     (METAL/Internal Error/RuntimeError/Traceback/out of memory/nan)
  3. 触发回滚机制              → 自动固化「崩溃前最优 best 快照」(snapshots/) +
     写回滚事件 rollback.jsonl + 打印回滚点指引（下次续训 resume 目标）

用法:
  python3 08_BIN/lh_train_rollback_guard.py run v420            # 守护 v4.2.0 train
  python3 08_BIN/lh_train_rollback_guard.py run v420 test      # 守护冒烟 test
  python3 08_BIN/lh_train_rollback_guard.py recover --log <训练日志> --adapter <adapter目录> [--resume <起点best>] [--solidify]
  python3 08_BIN/lh_train_rollback_guard.py status [--n 5]
  python3 08_BIN/lh_train_rollback_guard.py selftest           # 机制自检（不碰真实权重）

数据主权: 档案/快照仅存本地 ~/.longhun/train_runs/，不入云、不入 git。
"""

import argparse
import datetime
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

# ───────────────────────── 路径与常量 ─────────────────────────
RUNS_DIR = Path.home() / ".longhun" / "train_runs"
RUNS_JSONL = RUNS_DIR / "runs.jsonl"
ROLLBACK_JSONL = RUNS_DIR / "rollback.jsonl"
SNAPSHOT_DIR = RUNS_DIR / "snapshots"
PROJECT = Path(__file__).resolve().parent.parent
LOGS_DIR = PROJECT / "logs"

# 版本 → (trainer脚本, resume起点best, adapter产物目录)  训练器配置如再改版在此登记
PROFILES = {
    "v420": {
        "trainer": PROJECT / "08_BIN" / "lh_lora_trainer_v420.py",
        "adapter_dir": PROJECT / "models" / "longhun-v1.0" / "lora_output_v420" / "adapter_v420",
        "resume_file": PROJECT / "models" / "longhun-v1.0" / "lora_output_v419" / "adapter_v419" / "best_adapters.safetensors",
        "desc": "v4.2.0 收敛面续训(从v4.1.9 best·Val 0.8115)",
    },
}

# 走坏特征词（命中即判定崩溃类别·顺序即优先级）
CRASH_PATTERNS = [
    ("broken_metal", re.compile(r"METAL|Internal Error|command buffer", re.I)),
    ("broken_oom", re.compile(r"out of memory|memory error|killed 9", re.I)),
    ("broken_nan", re.compile(r"\bnan\b|loss nan", re.I)),
    ("broken_crash", re.compile(r"Traceback \(most recent call last\)|RuntimeError|Segmentation fault|core dumped", re.I)),
    ("broken_unknown", re.compile(r"Error|exception|失败|❌", re.I)),
]


def _now():
    return datetime.datetime.now().astimezone().isoformat(timespec="seconds")


def _sha256(path):
    try:
        h = hashlib.sha256()
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(1 << 20), b""):
                h.update(chunk)
        return h.hexdigest()[:16]
    except Exception:
        return None


def _file_facts(path):
    p = Path(path)
    if not p.exists():
        return None
    st = p.stat()
    return {"path": str(p), "sha256": _sha256(p), "bytes": st.st_size,
            "mtime": datetime.datetime.fromtimestamp(st.st_mtime).isoformat(timespec="seconds")}


def _append_jsonl(path, record):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")
    return record


def classify_crash(text):
    """按特征词把崩溃文本分类（返回 (status, matched)）。"""
    for status, pat in CRASH_PATTERNS:
        if pat.search(text):
            return status, pat.pattern
    return "broken_unknown", "rc!=0"


def solidfy_best(run_id, profile, reason, status, log_tail):
    """触发回滚：固化崩溃前最优 best 快照 + 写回滚事件。返回事件记录或 None。"""
    adapter_dir = Path(profile["adapter_dir"])
    resume_file = Path(profile["resume_file"])
    best = adapter_dir / "best_adapters.safetensors"
    resume_facts = _file_facts(resume_file) if resume_file.exists() else None

    # 回滚点判定：run 内 best 存在且与 resume 起点不同 → 固化崩前最优；否则回滚点=resume(上一稳定点)
    if best.exists():
        bf = _file_facts(best)
        if resume_facts and bf["sha256"] == resume_facts["sha256"]:
            source, note = resume_file, "run 无改善·回滚点=上一稳定点(resume)"
        else:
            source, note = best, "run 内崩前最优 best 已固化"
    else:
        source, note = (resume_file if resume_file.exists() else None), "无 run best·回滚点=resume 起点"

    event = {
        "ts": _now(), "run_id": run_id, "status": status, "trigger": "breakdown",
        "reason": reason[:300], "note": note,
    }
    if source and source.exists():
        snap = SNAPSHOT_DIR / run_id
        snap.mkdir(parents=True, exist_ok=True)
        target = snap / "best_adapters.safetensors"
        try:
            shutil.copy2(source, target)
        except Exception as e:
            event["solidify_error"] = str(e)
            target = None
        if target and target.exists():
            event["rollback_source"] = str(source)
            event["snapshot"] = str(target)
            event["snapshot_sha256"] = _sha256(target)
            event["resume_advice"] = (f"下次续训回滚点: python3 08_BIN/lh_lora_trainer_v420.py train "
                                      f"（或 resume → {snap}/best_adapters.safetensors）")
            # 同时写一份 ROLLBACK_MANIFEST 便于人工核对
            (snap / "ROLLBACK_MANIFEST.json").write_text(
                json.dumps({**event, "log_tail": log_tail[-400:]}, ensure_ascii=False, indent=2),
                encoding="utf-8")
    else:
        event["rollback_source"] = None
        event["note"] = event.get("note", "") + " · ⚠️ 无可用回滚点（resume 也不存在）· 需人工重建"

    _append_jsonl(ROLLBACK_JSONL, event)
    return event


def run_guarded(profile_name, action="train"):
    """守护执行：收集 → 判定 → 回滚。"""
    profile = PROFILES[profile_name]
    RUNS_DIR.mkdir(parents=True, exist_ok=True)
    run_id = f"{profile_name}-{datetime.datetime.now().strftime('%Y%m%d-%H%M%S')}"
    ts_start = _now()

    trainer = profile["trainer"]
    cmd = [sys.executable, str(trainer), action]
    log_path = LOGS_DIR / f"train_{profile_name}_{run_id}.log"
    LOGS_DIR.mkdir(parents=True, exist_ok=True)

    tail_buf = []
    print(f"🐉 回滚守护启动 | run_id={run_id} | {' '.join(cmd)}")
    print(f"   日志: {log_path} | 数据档案: {RUNS_JSONL}")

    try:
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    except Exception as e:
        _append_jsonl(RUNS_JSONL, {"run_id": run_id, "ts_start": ts_start, "ts_end": _now(),
                                   "profile": profile_name, "action": action, "status": "broken_unknown",
                                   "reason": f"启动失败: {e}", "log": str(log_path)})
        print(f"🔴 启动失败: {e}")
        return 1

    with open(log_path, "w", encoding="utf-8") as lf:
        for line in proc.stdout:
            tail_buf.append(line.rstrip("\n"))
            if len(tail_buf) > 200:
                tail_buf.pop(0)
            lf.write(line)
        proc.wait()

    rc = proc.returncode
    ts_end = _now()
    log_text = "\n".join(tail_buf)
    resume_facts = _file_facts(profile["resume_file"])

    record = {
        "run_id": run_id, "ts_start": ts_start, "ts_end": ts_end,
        "profile": profile_name, "version_desc": profile["desc"],
        "action": action, "exit_code": rc, "log": str(log_path),
        "resume_start": resume_facts,
        "duration_s": round((datetime.datetime.fromisoformat(ts_end) -
                             datetime.datetime.fromisoformat(ts_start)).total_seconds()),
    }

    if rc == 0:
        record["status"] = "completed"
        print("🟢 run 完成·无走坏触发")
    else:
        status, matched = classify_crash(log_text)
        record["status"] = status
        record["crash_pattern"] = matched
        record["reason"] = f"exit={rc} · 崩溃特征: {matched}"
        record["log_tail"] = "\n".join(tail_buf[-30:]) if tail_buf else ""
        print(f"🔴 走坏触发! status={status} | pattern={matched} | exit={rc}")
        print("   ↺ 自动回滚固化中…")
        ev = solidfy_best(run_id, profile, record["reason"], status, "\n".join(tail_buf))
        if ev:
            record["rollback_event"] = {k: v for k, v in ev.items() if k != "log_tail"}
            print(f"   ✅ 回滚固化: {ev.get('snapshot', '无')}")
            print(f"      {ev.get('resume_advice', '')}")
        print(f"   📄 完整日志: {log_path}")

    _append_jsonl(RUNS_JSONL, record)
    return 0 if rc == 0 else 1


def recover_history(log_path, adapter_dir, resume_file, solidify=False, reason=""):
    """补录历史崩溃 run（如 9/5 METAL 崩·当时零留痕）→ 数据归档 + 可选固化。"""
    log_path = Path(log_path)
    if not log_path.exists():
        print(f"🔴 日志不存在: {log_path}")
        return 1
    text = log_path.read_text(encoding="utf-8", errors="ignore")
    run_id = f"{log_path.stem}-recovered-{datetime.datetime.now().strftime('%Y%m%d-%H%M%S')}"
    ts = _now()

    # 判定历史 run 结局：尾部有无完成标志/崩溃词
    tail = "\n".join(text.splitlines()[-12:])
    if re.search(r"all_pipeline|🎉|完成", tail) and "Traceback" not in tail:
        status = "completed"
        rc = 0
    else:
        status, matched = classify_crash(tail)
        rc = 1

    record = {
        "run_id": run_id, "ts_start": ts, "ts_end": ts, "profile": "history-recover",
        "action": "recover", "exit_code": rc, "log": str(log_path), "recovered": True,
        "status": status, "reason": reason or f"历史补录判定: {status}",
    }
    if status != "completed":
        record["crash_pattern"] = matched if 'matched' in dir() else None
        record["log_tail"] = tail

    if status != "completed" and solidify:
        fake = {"adapter_dir": Path(adapter_dir) if adapter_dir else Path(str(log_path)).parent,
                "resume_file": Path(resume_file) if resume_file else Path(profile or str(log_path))}
        ev = solidfy_best(run_id, fake, record["reason"], status, tail)
        if ev:
            record["rollback_event"] = ev
            print(f"   ✅ 历史回滚固化: {ev.get('snapshot')}")

    _append_jsonl(RUNS_JSONL, record)
    print(f"📄 历史补录: run_id={run_id} status={status} → {RUNS_JSONL}")
    return 0


def show_status(n=5):
    if not RUNS_JSONL.exists():
        print("暂无 run 档案（~/.longhun/train_runs/ 为空）")
        return
    rows = [json.loads(l) for l in RUNS_JSONL.read_text().splitlines() if l.strip()][-n:]
    print(f"{'run_id':<36} {'status':<16} {'action':<8} exit 起止")
    for r in rows:
        mark = {"completed": "🟢", "broken_crash": "🔴", "broken_metal": "🔴",
                "broken_nan": "🔴", "broken_oom": "🔴", "broken_unknown": "🟡"}.get(r.get("status"), "🟡")
        print(f"{mark} {r['run_id']:<34} {r.get('status'):<16} {r.get('action',''):<8} "
              f"{r.get('exit_code')}  {r.get('ts_start','')[:19]} → {r.get('ts_end','')[:19]}")
        if r.get("rollback_event"):
            print(f"      ↺ 回滚: {r['rollback_event'].get('snapshot', '-')} | "
                  f"note: {r['rollback_event'].get('note', '-')[:40]}")


def selftest():
    """机制自检：不碰任何真实权重/模型。验证 判定→事件→档案 全链路。"""
    global RUNS_DIR, RUNS_JSONL, ROLLBACK_JSONL, SNAPSHOT_DIR
    tmp = Path(tempfile.mkdtemp(prefix="train_guard_selftest_"))
    try:
        # 1. 崩溃分类
        cases = [
            ("[METAL] Command buffer execution failed: Internal Error", "broken_metal"),
            ("RuntimeError: out of memory", "broken_oom"),
            ("loss nan → 回滚 best checkpoint", "broken_nan"),
            ("Traceback (most recent call last):\n  File x.py, line 1", "broken_crash"),
            ("something else went wrong", "broken_unknown"),
        ]
        for text, expect in cases:
            got, _ = classify_crash(text)
            assert got == expect, f"判定错: {text[:30]} → {got} ≠ {expect}"
        print(f"✅ 崩溃分类 5/5")

        # 2. 假 best 固化（mock 到临时目录）
        tmp_best = tmp / "adapter" / "best_adapters.safetensors"
        tmp_best.parent.mkdir(parents=True)
        tmp_best.write_bytes(b"\x00\x01BEST")
        fake_profile = {"adapter_dir": tmp_best.parent,
                        "resume_file": tmp / "resume_absent.safetensors"}
        old_run_dir, old_roll, old_runs = RUNS_DIR, ROLLBACK_JSONL, RUNS_JSONL
        RUNS_DIR, RUNS_JSONL, ROLLBACK_JSONL = (tmp / "runs", tmp / "runs" / "runs.jsonl",
                                                tmp / "runs" / "rollback.jsonl")
        SNAPSHOT_DIR = tmp / "runs" / "snapshots"
        ev = solidfy_best("selftest-run-1", fake_profile, "METAL Internal Error", "broken_metal", "tail...")
        assert ev and ev.get("snapshot") and Path(ev["snapshot"]).exists(), "固化失败"
        assert Path(ev["snapshot"]).read_bytes() == b"\x00\x01BEST"
        assert ROLLBACK_JSONL.exists(), "事件未写"
        print(f"✅ 回滚固化+事件留痕 OK → {ev['snapshot']}")

        # 3. run 档案写入
        rec = {"run_id": "selftest-run-1", "status": "broken_metal", "exit_code": 1}
        _append_jsonl(RUNS_JSONL, rec)
        assert json.loads(RUNS_JSONL.read_text().splitlines()[0])["run_id"] == "selftest-run-1"
        RUNS_DIR, RUNS_JSONL, ROLLBACK_JSONL, SNAPSHOT_DIR = old_run_dir, old_runs, old_roll, old_run_dir / "snapshots"
        print("✅ run 档案 JSONL append-only OK")
        print("🟢 selftest 全过 · 机制就绪")
        return 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def main():
    p = argparse.ArgumentParser(description="龍魂 训练/测试 回滚守护壳 v1.0")
    sub = p.add_subparsers(dest="cmd")

    pr = sub.add_parser("run", help="守护执行训练（自动收集+崩溃触发+回滚）")
    pr.add_argument("profile", choices=list(PROFILES.keys()))
    pr.add_argument("action", nargs="?", default="train", choices=["train", "test", "fuse", "export", "all"])

    rc = sub.add_parser("recover", help="补录历史 run（数据收集）")
    rc.add_argument("--log", required=True, help="历史训练日志路径")
    rc.add_argument("--adapter", default="", help="adapter 产物目录（固化时定位 best）")
    rc.add_argument("--resume", default="", help="resume 起点 best 文件")
    rc.add_argument("--solidify", action="store_true", help="走坏历史 run 同时固化回滚快照")
    rc.add_argument("--reason", default="", help="补录说明")

    rs = sub.add_parser("status", help="查看最近 run 档案")
    rs.add_argument("--n", type=int, default=5)

    sub.add_parser("selftest", help="机制自检（不碰真实权重）")

    args = p.parse_args()
    if args.cmd == "run":
        return run_guarded(args.profile, args.action)
    if args.cmd == "recover":
        return recover_history(args.log, args.adapter, args.resume, args.solidify, args.reason)
    if args.cmd == "status":
        show_status(args.n)
        return 0
    if args.cmd == "selftest":
        return selftest()
    p.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
