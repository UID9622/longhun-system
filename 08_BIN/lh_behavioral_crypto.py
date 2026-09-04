#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
"""
🐉 龍魂·行為密碼學 CLI 入口（lh.py 調度用）
DNA: #龍芯⚡️丙午·甲申·丁酉·丙午·䷳艮-BCM-CLI-V2.0-UID9622
License: MulanPSL v2
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "04_ENGINES"))

from behavioral_crypto.seven_factor_model import (
    SevenFactorEngine, quick_fingerprint, verify_fingerprint,
    FACTOR_DEFINITIONS, SOVEREIGN_ANCHOR,
)
from behavioral_crypto.experiment_runner import ExperimentRunner, ATTACK_LEVELS, CORPUS_TYPES
from behavioral_crypto.visualizer import Visualizer


def run_demo():
    """運行完整演示"""
    print("\n" + "=" * 72)
    print("  🐉 龍魂·行為密碼學引擎 v2.0 · 七因子來源追溯")
    print("=" * 72)
    
    # 示例文本
    sample = """
DNA: #龍芯⚡️丙午·甲申·丁酉·丙午·䷳艮-BEHAVIORAL-CRYPTO-V2.0-UID9622
確認碼: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

龍魂系統的行為密碼學引擎基於七因子模型。每個文檔都有一個不可偽造的行為指紋。
七個因子分別是：身份DNA（誰寫的）、時間錨定（何時寫的）、內容哈希（寫了什麼）、
風格向量（怎麼寫的）、保護詞彙（核心術語）、長期風格（歷史一致性）、糾錯賬本（修正模式）。

這七層合在一起，攻擊者無法同時偽造所有層。即使AI完全重寫，前幾層的痕跡依然可追溯。
這是AIGC時代內容來源追溯的核心技術，也是龍魂信息主權體系的重要組成部分。
"""
    
    # F1: 提取指紋
    print("\n📌 步驟1: 提取七因子行為指紋")
    print("-" * 72)
    
    engine = SevenFactorEngine()
    engine.update_author_profile("UID9622", sample)
    fp = engine.extract(sample, "UID9622")
    
    print(f"  DNA: {fp.dna}")
    print(f"  綜合得分: {fp.composite_score:.4f}  {fp.audit_mark}")
    print()
    
    for f in fp.factors:
        bar_len = int(f.raw_value * 30)
        bar = "█" * bar_len + "░" * (30 - bar_len)
        name = FACTOR_DEFINITIONS[f.factor_id]["icon"] + " " + f.factor_name
        print(f"  {f.status} {name:14s} [{bar}] {f.raw_value:.3f} "
              f"(x{FACTOR_DEFINITIONS[f.factor_id]['weight']:.2f} = {f.weighted_value:.4f})")
    
    # F2: 雷達圖
    print("\n\n📌 步驟2: 七因子雷達圖")
    print("-" * 72)
    
    factor_scores = {f.factor_id: f.raw_value for f in fp.factors}
    viz = Visualizer()
    print(viz.render_radar(factor_scores, width=72))
    
    # F3: 攻擊模擬
    print("\n\n📌 步驟3: 五級攻擊模擬")
    print("-" * 72)
    
    from behavioral_crypto.experiment_runner import AttackSimulator
    simulator = AttackSimulator(seed=42)
    
    for level in ["L1", "L2", "L4"]:
        attacked_text, meta = simulator.apply_attack(sample, level)
        attacked_fp = engine.extract(attacked_text, "UID9622")
        
        orig_dict = fp.to_dict()
        att_dict = attacked_fp.to_dict()
        
        print(viz.render_comparison(orig_dict, att_dict, level))
        print()
    
    # F4: 最終簽名
    print("=" * 72)
    print("🐉 龍魂·行為密碼學引擎 v2.0 · 演示完成")
    print(f"  核心邏輯: 七因子行為指紋 → 五級攻擊測試 → 來源追溯驗證")
    print(f"  DNA: {SOVEREIGN_ANCHOR['dna_prefix']}{SOVEREIGN_ANCHOR['uid']}")
    print(f"  確認碼: {SOVEREIGN_ANCHOR['confirm']}")
    print(f"  GPG: {SOVEREIGN_ANCHOR['gpg']}")
    print("=" * 72)


def run_experiment_cli(num_docs=50, output_json=None):
    """命令行運行實驗"""
    print(f"🐉 運行實驗: {num_docs} 文檔 × 5 級攻擊...")
    
    runner = ExperimentRunner(num_docs=num_docs, seed=42)
    results = runner.run_full_experiment()
    summary = runner.generate_summary()
    
    viz = Visualizer()
    print(viz.render_summary(summary))
    
    if output_json:
        os.makedirs(os.path.dirname(output_json) or ".", exist_ok=True)
        with open(output_json, "w", encoding="utf-8") as f:
            json.dump({"summary": summary, "results": results[:20]}, f, ensure_ascii=False, indent=2)
        print(f"\n📄 JSON 報告: {output_json}")


def show_help():
    """顯示幫助"""
    print("""
🐉 龍魂·行為密碼學引擎 v2.0
═══════════════════════════════════════════════════════════════

用法:
  lh bcm                  — 完整演示（七因子提取+攻擊模擬+可視化）
  lh bcm --experiment     — 運行攻擊模擬實驗
  lh bcm --experiment --docs 100  — 指定文檔數
  lh bcm --experiment --json output.json  — 輸出JSON報告
  lh bcm --verify "文本"  — 驗證一段文本的行為指紋
  lh bcm --json "文本"    — JSON輸出（供 lh-station 安全審計調用）
  lh bcm --radar          — 顯示七因子雷達圖
  lh bcm --status         — 顯示引擎狀態
  lh bcm --help           — 顯示此幫助

API端點 (:8775):
  POST /api/v2/bcm/extract       — 提取七因子指紋
  POST /api/v2/bcm/verify        — 驗證行為指紋
  GET  /api/v2/bcm/experiment/run — 運行攻擊模擬實驗
  GET  /api/v2/bcm/status         — 引擎狀態
  GET  /api/v2/bcm/sovereignty    — 主權驗證

主權: 🇨🇳 中華人民共和國法律為唯一準繩
許可: 思想層 CC BY-NC-SA 4.0 · 工程層 MulanPSL v2
═══════════════════════════════════════════════════════════════
""")


if __name__ == "__main__":
    args = sys.argv[1:]
    
    if "--help" in args or "-h" in args:
        show_help()
    elif "--experiment" in args:
        num_docs = 50
        output_json = None
        
        for i, a in enumerate(args):
            if a == "--docs" and i + 1 < len(args):
                num_docs = int(args[i + 1])
            if a == "--json" and i + 1 < len(args):
                output_json = args[i + 1]
        
        run_experiment_cli(num_docs, output_json)
    elif "--verify" in args or "--json" in args:
        # --json 模式：輸出機器可讀 JSON（給 Rust/lh-station 調用）
        use_json = "--json" in args
        
        if "--verify" in args:
            idx = args.index("--verify")
        else:
            idx = args.index("--json") if "--json" in args else -1
        text = args[idx + 1] if idx + 1 < len(args) else ""
        
        if text:
            result = quick_fingerprint(text)
            verified = verify_fingerprint(result, 0.30)
            
            if use_json:
                # 機器可讀 JSON 輸出（供 lh-station security.rs 調用）
                output = {
                    "engine": "behavioral-crypto-v2",
                    "verified": verified.get("verified", False),
                    "score": verified.get("score", 0),
                    "composite_score": result.get("composite_score", 0),
                    "audit_mark": result.get("audit_mark", "🟡"),
                    "factors": result.get("factors", []),
                    "warnings": verified.get("warnings", []),
                    "recommendation": verified.get("recommendation", ""),
                    "sovereignty": SOVEREIGN_ANCHOR["confirm"],
                }
                print(json.dumps(output, ensure_ascii=False))
            else:
                print(json.dumps(verified, ensure_ascii=False, indent=2))
        else:
            print("用法: lh bcm --verify \"待验证文本\" 或 lh bcm --json \"待验证文本\"")
    elif "--radar" in args:
        engine = SevenFactorEngine()
        sample = "DNA: #龍芯⚡️UID9622\n確認碼: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
        fp = engine.extract(sample)
        factor_scores = {f.factor_id: f.raw_value for f in fp.factors}
        viz = Visualizer()
        print(viz.render_radar(factor_scores))
    elif "--status" in args:
        print("🐉 行為密碼學引擎狀態")
        print(f"  版本: v2.0")
        print(f"  因子: {len(FACTOR_DEFINITIONS)} 個")
        print(f"  攻擊級別: {len(ATTACK_LEVELS)} 級")
        print(f"  語料類型: {len(CORPUS_TYPES)} 類")
        print(f"  主權: {SOVEREIGN_ANCHOR['jurisdiction']}")
        print(f"  GPG: {SOVEREIGN_ANCHOR['gpg']}")
    else:
        run_demo()
