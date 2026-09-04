# examples/config_ab_comparison.py
"""
Config A/B 对比示例 — 复现 icophy 双层案例
  Config A: 会话级记忆，无身份锚定 → 精密度低（same prompt, 不同判定）
  Config B: 持久记忆，有身份锚定   → 精密度高（same prompt, 一致判定）
DNA: #龍芯⚡️2026-08-25-CONFIG-AB-EXAMPLE-v1.0-UID9622
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from core.layer1 import VerdictAlignment
from core.layer2 import BehavioralAlignment
from core.report import ReportGenerator

# Config A: 会话级记忆，无身份锚定
records_A = [
    {"prompt": "帮我查数据", "verdict": "accept",  "session_id": "s1", "config": "A"},
    {"prompt": "帮我查数据", "verdict": "defer",   "session_id": "s2", "config": "A"},
    {"prompt": "帮我查数据", "verdict": "reject",  "session_id": "s3", "config": "A"},
]

# Config B: 持久记忆，有身份锚定
records_B = [
    {"prompt": "帮我查数据", "verdict": "accept",  "session_id": "s4", "config": "B"},
    {"prompt": "帮我查数据", "verdict": "accept",  "session_id": "s5", "config": "B"},
    {"prompt": "帮我查数据", "verdict": "accept",  "session_id": "s6", "config": "B"},
]

# ── Layer 1: 两者 expected 均为 accept ──────────────────
print("="*55)
print("Layer 1: 判定对齐（Verdict Alignment）")
print("="*55)

l1_A = VerdictAlignment(["accept", "defer", "reject"], ["accept", "accept", "accept"])
l1_B = VerdictAlignment(["accept", "accept", "accept"], ["accept", "accept", "accept"])

r1_A = l1_A.report()
r1_B = l1_B.report()
print(f"Config A | {r1_A['summary']}")
print(f"Config B | {r1_B['summary']}")
print("→ Layer 1 准确率不同: A=33.33%, B=100%")

# ── Layer 2: 精密度对比 ─────────────────────────────────
print()
print("="*55)
print("Layer 2: 行为对齐（Behavioral Alignment）")
print("="*55)

all_records = records_A + records_B
l2 = BehavioralAlignment(all_records)

print(f"Config A 精密度 (单独): {BehavioralAlignment(records_A).precision_score():.2f}")
print(f"Config B 精密度 (单独): {BehavioralAlignment(records_B).precision_score():.2f}")

print()
print("偏差分析（参考配置 A）:")
trueness = l2.trueness_analysis(reference_config="A")
for cfg, data in trueness.items():
    print(f"  Config {cfg}: deviation={data['deviation']:+.3f} | type={data['deviation_type']} | traceable={data['traceable']}")

# ── 完整报告 ────────────────────────────────────────────
print()
print("="*55)
print("§6 完整报告（Markdown 预览）")
print("="*55)

gen = ReportGenerator("icophy-Cophy", "Config-A/B")
verdicts_combined = [r["verdict"] for r in all_records]
expected_combined = ["accept"] * len(all_records)
full_report = gen.generate(verdicts_combined, expected_combined, all_records)
print(gen.to_markdown(full_report))
