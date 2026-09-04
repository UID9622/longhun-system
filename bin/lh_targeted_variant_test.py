#!/usr/bin/env python3
"""针对真实穿透的攻击变体生成 + 验证"""
import json, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from bin.lh_adversarial_pipeline import AdversarialPipeline, CONFIG

pipeline = AdversarialPipeline()

# 从穿透日志读取真实穿透
pen_path = CONFIG['穿透日志路径']
with open(pen_path, 'r') as f:
    penetrations = [json.loads(line) for line in f if line.strip()]

print(f'[🎯] 针对 {len(penetrations)} 个真实穿透生成变体并验证\n')

all_variants = []
for p in penetrations:
    attack = {
        'id': p['attack_id'],
        'instruction': p['instruction'],
        'category': p['category'],
        'severity': 'high',
        'source': 'penetration'
    }
    variants = pipeline.generate_variants(attack, num_variants=5)
    all_variants.extend(variants)
    print(f'   {p["attack_id"]}: {p["instruction"][:40]}... → {len(variants)} 变体')

print(f'\n[🔍] 验证 {len(all_variants)} 个变体 vs Ollama...')
result = pipeline.validate_batch(all_variants, label=f'穿透变体验证 ({len(penetrations)}×5)')

pipeline.generate_report(result)

# 穿透项检查
if result['penetrated'] > 0:
    print(f'\n[🚨] 仍有 {result["penetrated"]} 个变体穿透！')
    pen_results = [r for r in result['results'] if r['penetrated']]
    for r in pen_results:
        print(f"   └─ {r['attack_id']}: {r['instruction'][:60]}")
    print(f'[📤] 再训练候选已写入 {CONFIG["再训练数据路径"]}')
else:
    print(f'\n[✅] 所有变体成功拒绝')

pipeline.print_stats()
