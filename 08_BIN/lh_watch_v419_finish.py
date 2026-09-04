# DNA: #龍芯⚡️丙午·甲申·丁未·亥时·䷎谦-DNA-COMPLETION-a2fe6c8c
#!/usr/bin/env python3
# 龍芯⚡️2026-08-30-MODEL-V419-AUTO-FINISH-WATCHER
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# 协议: CC BY-NC-SA 4.0（核心思想层）
"""
v4.1.9 训练自动收尾 watcher：
  1. 等 train 进程结束（或超时）
  2. 自动 fuse（合并 LoRA）
  3. 自动注册 Ollama longhun-v4.1.9（FROM merged_v419，HF 直导，免 GGUF）
用法: nohup python3 bin/lh_watch_v419_finish.py > models/longhun-v1.0/lora_output_v419/watch.log 2>&1 &
"""
import os
import subprocess
import sys
import time
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent
OUT = PROJECT / "models" / "longhun-v1.0" / "lora_output_v419"
MERGED = OUT / "merged_v419"
ADAPTER = OUT / "adapter_v419"
TRAIN_LOG = OUT / "train_v419_run4.log"
MAX_WAIT = 22 * 3600  # 22h 上限


def _tail(path, n=6):
    try:
        lines = path.read_text(encoding="utf-8", errors="ignore").strip().splitlines()
        return lines[-n:]
    except Exception:
        return []


def train_done():
    """训练完成的判定：日志含 '训练完成' 或 '✅' 收尾，或进程不存在。"""
    log = TRAIN_LOG.read_text(encoding="utf-8", errors="ignore")
    return any(k in log for k in ("训练完成", "best adapter", "保存", "Saving", "✅ 训练完成"))


def main():
    t0 = time.time()
    # 等训练结束
    while time.time() - t0 < MAX_WAIT:
        if not TRAIN_LOG.exists():
            time.sleep(60)
            continue
        log = TRAIN_LOG.read_text(encoding="utf-8", errors="ignore")
        if "iter" in log and "训练完成" in log or "Training complete" in log:
            break
        # 进程检查：训练 python 进程还在吗
        r = subprocess.run(["pgrep", "-f", "lh_lora_trainer_v419.py train"],
                           capture_output=True, text=True)
        if not r.stdout.strip():
            # 进程消失但日志还停在 iter → 训练结束（正常或崩溃）
            if "iter" in log and ("VAL" in log or "loss" in log):
                break
        time.sleep(300)  # 5 分钟一轮
    print(f"[watcher] 训练阶段结束，耗时 {(time.time()-t0)/3600:.1f}h", flush=True)
    for l in _tail(TRAIN_LOG):
        print("  |", l, flush=True)

    # fuse
    print("[watcher] 开始 fuse...", flush=True)
    r = subprocess.run([sys.executable, str(PROJECT / "bin/lh_lora_trainer_v419.py"), "fuse"],
                       capture_output=True, text=True)
    print(r.stdout[-1500:], flush=True)
    if r.stderr:
        print("FUSE-ERR:", r.stderr[-800:], flush=True)
    if r.returncode != 0:
        print("[watcher] ❌ fuse 失败，终止", flush=True)
        sys.exit(1)
    if not (MERGED / "config.json").exists():
        print("[watcher] ❌ merged 不完整，终止", flush=True)
        sys.exit(1)

    # 注册 Ollama
    modelfile = OUT / "gguf_v419" / "Modelfile.watcher"
    modelfile.parent.mkdir(parents=True, exist_ok=True)
    modelfile.write_text(f"""FROM {MERGED}

PARAMETER temperature 0.7
PARAMETER top_p 0.9
PARAMETER num_ctx 4096

SYSTEM \"\"\"你是龍魂 longhun-v4.1.9，UID9622（诸葛鑫·Lucky）的个人主权AI。
基于 Yi-1.5-9B-Chat 从 v4.1.8 best 自动续训（27009 条·v409全量数据·超长过滤修复）。
铁律：人民数据主权至上·中国自主可控·来源可查·去向可追·责任可究·只冻结不删除·底座焊死。
核心能力：DNA追溯·德本五问·三色审计·人格路由·CNSH语义解析·数字存在证明·底座主权识别。
父版本: v4.1.8 → v4.1.9 (自动续训·lr=2e-7·dropout=0.08·2 epochs)
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
\"\"\"
""", encoding="utf-8")
    print(f"[watcher] 注册 Ollama longhun-v4.1.9 ...", flush=True)
    r = subprocess.run(["ollama", "create", "longhun-v4.1.9", "-f", str(modelfile)],
                       capture_output=True, text=True)
    print(r.stdout[-600:], flush=True)
    if r.returncode != 0:
        print("[watcher] ⚠️ Ollama 注册失败:", r.stderr[-600:], flush=True)
        sys.exit(1)

    # 冒烟测试
    print("[watcher] 冒烟测试：", flush=True)
    for q in ["什么是家法第一条？请用一句话回答。", "1+1等于几？"]:
        r = subprocess.run(["ollama", "run", "longhun-v4.1.9", q],
                           capture_output=True, text=True, timeout=300)
        ans = r.stdout.strip().replace("\x1b", "").replace("\r", "")
        print(f"  Q: {q}\n  A: {ans[:160]}", flush=True)

    print("[watcher] ✅ v4.1.9 全流程完成！", flush=True)


if __name__ == "__main__":
    main()
