#!/usr/bin/env python3
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# -*- coding: utf-8 -*-
"""
龍魂本地训练引擎 · 训练收尾脚本
DNA: #龍芯⚡️丙午·甲午·癸酉·戊午·䷨损-LONGHUN-TRAIN-FINALIZE-v1.0

职责：
  1. 检查训练是否完成（模型文件存在 + 报告存在）
  2. 加载模型做文本生成测试（验证模型真的能说话）
  3. 汇总训练报告（含 loss 曲线、参数量、生成样例）
  4. 供自动化任务调用，全程无人值守
"""
import sys
import json
import time
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from config import Config
from tokenizer import CharTokenizer
from model import LonghunLM
import torch

cfg = Config()
MODEL_PATH = cfg.model_dir / f"{cfg.model_name}.pt"
TOKENIZER_PATH = cfg.tokenizer_path
REPORT_PATH = cfg.output_dir / f"{cfg.model_name}_train_report.json"

TEST_PROMPTS = ["龍魂", "为人民服务", "数据主权归用户", "天行健，君子以自强不息"]


def wait_for_done(timeout_min=120, poll_s=30):
    deadline = time.time() + timeout_min * 60
    while time.time() < deadline:
        if MODEL_PATH.exists() and REPORT_PATH.exists():
            return True
        time.sleep(poll_s)
    return False


def load_model():
    ckpt = torch.load(MODEL_PATH, map_location="cpu", weights_only=False)
    model_cfg = ckpt["config"]
    from types import SimpleNamespace
    mcfg = SimpleNamespace(
        vocab_size=model_cfg.get("vocab_size", 12000),
        hidden_size=model_cfg.get("hidden_size", 512),
        max_seq_len=model_cfg.get("max_seq_len", 512),
        pad_id=model_cfg.get("pad_id", 0),
        dropout=model_cfg.get("dropout", 0.1),
        num_layers=model_cfg.get("num_layers", 4),
    )
    model = LonghunLM(mcfg)
    model.load_state_dict(ckpt["model_state_dict"])
    return model, ckpt, model_cfg


def run_generation(model, tokenizer):
    device = "mps" if torch.backends.mps.is_available() else "cpu"
    model = model.to(device)
    samples = []
    for prompt in TEST_PROMPTS:
        try:
            out = model.generate(tokenizer, prompt, max_new_tokens=40, temperature=0.8)
            samples.append({"prompt": prompt, "output": out})
        except Exception as e:
            samples.append({"prompt": prompt, "error": str(e)})
    return samples


def main():
    print("=" * 60)
    print("龍魂训练收尾脚本启动")
    print(f"   模型: {cfg.model_name}")
    print(f"   时间: {datetime.now().isoformat()}")
    print("=" * 60)

    ok = wait_for_done()
    if not ok:
        print("等待超时，训练尚未完成或模型文件缺失")
        print(f"   模型路径: {MODEL_PATH}")
        sys.exit(1)

    print(f"检测到训练产物: {MODEL_PATH.name}")

    model, ckpt, model_cfg = load_model()
    tokenizer = CharTokenizer().load(TOKENIZER_PATH)
    total_params = sum(p.numel() for p in model.parameters())
    print(f"   模型参数量: {total_params:,} ({total_params / 1e6:.2f} M)")
    print(f"   词表大小: {len(tokenizer)}")
    print(f"   DNA: {ckpt.get('dna', 'N/A')}")

    samples = run_generation(model, tokenizer)
    print("\n--- 文本生成测试 ---")
    for s in samples:
        if "output" in s:
            print(f"\n[提示] {s['prompt']}\n[输出] {s['output'][:120]}")
        else:
            print(f"\n[提示] {s['prompt']}\n[错误] {s['error']}")

    train_report = json.loads(REPORT_PATH.read_text(encoding="utf-8")) if REPORT_PATH.exists() else {}

    final_report = {
        "model_name": cfg.model_name,
        "dna": ckpt.get("dna", "N/A"),
        "finalize_time": datetime.now().isoformat(),
        "total_params": total_params,
        "vocab_size": len(tokenizer),
        "train_report": train_report,
        "generation_samples": samples,
        "loss_history": train_report.get("history", []),
        "final_loss": train_report.get("history", [{}])[-1].get("loss") if train_report.get("history") else None,
    }
    final_path = cfg.output_dir / f"{cfg.model_name}_final_report.json"
    final_path.write_text(json.dumps(final_report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n收尾报告: {final_path}")

    loss_curve = " -> ".join(f"E{int(h.get('epoch', i + 1))}:{h.get('loss', 0):.3f}" for i, h in enumerate(train_report.get("history", [])))
    summary = f"""
# 龍魂-0.5B 训练总结（{datetime.now().strftime('%Y-%m-%d %H:%M')}）

- 参数量: {total_params / 1e6:.2f}M
- 词表: {len(tokenizer)}
- Loss 曲线: {loss_curve or '无'}

## 生成测试
"""
    for s in samples:
        if "output" in s:
            summary += f"- **{s['prompt']}**: {s['output'][:80]}\n"
    summary_path = cfg.output_dir / f"{cfg.model_name}_summary.md"
    summary_path.write_text(summary, encoding="utf-8")
    print(f"摘要: {summary_path}")
    print("=" * 60)
    print("收尾完成")


if __name__ == "__main__":
    main()
