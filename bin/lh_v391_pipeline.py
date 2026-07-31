# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
#龍芯⚡️丙午·乙未·甲寅·需-V391-AUTO-PIPELINE-v1.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
龍魂 v3.9.1 全自动流水线
K3 蒸馏 → 自动抽查 → 准备数据 → 训练 → 合并 → 导出 → Ollama 部署 → 三关验证

用法:
  python3 bin/lh_v391_pipeline.py

DNA: #龍芯⚡️丙午·乙未·甲寅·需-V391-AUTO-PIPELINE-v1.0
"""

import json
import os
import subprocess
import sys
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent
K3_DIR = PROJECT / "models" / "longhun-v1.0" / "lora_output" / "k3_distill_v39"
REPORT_PATH = PROJECT / "models" / "longhun-v1.0" / "lora_output" / "validation_reports" / "v3.9.1_validation_report.md"


def run(cmd: list[str], cwd: str = None, timeout: int = None):
    """执行命令，失败则退出"""
    print(f"\n🚀 {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=cwd or str(PROJECT), capture_output=False, text=True, timeout=timeout)
    if result.returncode != 0:
        print(f"❌ 命令失败: {' '.join(cmd)}")
        sys.exit(1)
    return result


def check_k3_output():
    """检查 K3 蒸馏数据是否已生成"""
    required = ["jiafa_qa.jsonl", "sovereignty_qa.jsonl", "multiturn_qa.jsonl"]
    missing = [f for f in required if not (K3_DIR / f).exists()]
    if missing:
        print(f"❌ K3 蒸馏数据缺失: {missing}")
        print("   请先运行: python3 bin/lh_k3_distill_v39.py")
        sys.exit(1)
    counts = {f: sum(1 for _ in open(K3_DIR / f, encoding="utf-8") if _.strip()) for f in required}
    print(f"✅ K3 蒸馏数据就绪: {counts}")
    return counts


def auto_review(max_bad_rate: float = 0.05):
    """自动抽查：检测格式异常和明显胡话"""
    print("\n🔍 K3 自动抽查 20%...")
    all_samples = []
    for f in ["jiafa_qa.jsonl", "sovereignty_qa.jsonl", "multiturn_qa.jsonl"]:
        path = K3_DIR / f
        if not path.exists():
            continue
        with open(path, encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                item = json.loads(line)
                all_samples.append((f, item))

    import random
    random.seed(42)
    n_review = max(1, int(len(all_samples) * 0.2))
    review = random.sample(all_samples, n_review)

    bad = 0
    for fname, item in review:
        answer = ""
        for m in item.get("messages", []):
            if m.get("role") == "assistant":
                answer = m.get("content", "")
                break
        reasons = []
        if not ("<think>" in answer and "</think>" in answer):
            reasons.append("缺think标签")
        if len(answer) < 40:
            reasons.append("过短")
        if answer.count("<think>") > 1 or answer.count("</think>") > 1:
            reasons.append("think标签重复")
        # 主权/家法答案必须出现关键锚点之一
        domain = item.get("metadata", {}).get("domain", "")
        if domain == "家法第一条":
            if not any(k in answer for k in ["家法第一条", "文化卖国罪", "主权", "熔断"]):
                reasons.append("缺家法锚点")
        if domain == "主权边界":
            if not any(k in answer for k in ["数据主权", "本地", "龍魂", "UID9622"]):
                reasons.append("缺主权锚点")
        if reasons:
            bad += 1
            print(f"   ⚠️ [{fname}] {reasons}")

    bad_rate = bad / len(review)
    print(f"   抽查 {len(review)} 条，异常 {bad} 条，胡话率 {bad_rate:.1%}")
    if bad_rate > max_bad_rate:
        print(f"❌ 胡话率 {bad_rate:.1%} > {max_bad_rate:.1%}，整批返工。请检查 K3 输出: {K3_DIR}")
        sys.exit(1)
    print("✅ 抽查通过")


def main():
    print("=" * 60)
    print("🐉 龍魂 v3.9.1 全自动流水线启动")
    print("=" * 60)

    # 1. 确认 K3 数据
    check_k3_output()

    # 2. 自动抽查
    auto_review()

    # 3. 准备训练数据
    run([sys.executable, "bin/lh_lora_trainer_v391.py", "prepare"], timeout=300)

    # 4. 训练
    run([sys.executable, "bin/lh_lora_trainer_v391.py", "train"], timeout=7200)

    # 5. 合并
    run([sys.executable, "bin/lh_lora_trainer_v391.py", "fuse"], timeout=600)

    # 6. 导出 GGUF
    run([sys.executable, "bin/lh_lora_trainer_v391.py", "export"], timeout=1200)

    # 7. Ollama 部署
    gguf_dir = PROJECT / "models" / "longhun-v1.0" / "lora_output" / "gguf_v3.9.1"
    modelfile = gguf_dir / "Modelfile"
    run(["ollama", "create", "longhun-v3.9.1", "-f", str(modelfile)], timeout=600)

    # 8. 三关验证
    run([sys.executable, "bin/lh_validate_v391.py"], timeout=900)

    print("\n" + "=" * 60)
    print("✅ v3.9.1 流水线完成")
    print(f"📊 验证报告: {REPORT_PATH}")
    print("=" * 60)


if __name__ == "__main__":
    main()
