# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# DNA: #龍芯⚡️丙午·丙申·戊辰·丁巳·䷯井-CODE-补DNA-ffe80fb7
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""🐉 龍魂算力成本对比器 v1.0
用法: python3 compare_cost.py --tokens 1000000 [--provider openai]
定价口径：公开刊例价（2026-08，人民币换算），如有变动以官方为准——脚本只算数，不背书价格。
"""
import argparse, json

# 每千token价格（元）——公开刊例估算，🟡未实时核验
PROVIDERS = {
    "openai":   {"每千token元": 0.014,  "说明": "GPT系 API 刊例均价"},
    "claude":   {"每千token元": 0.021,  "说明": "Claude API 刊例均价"},
    "kimi":     {"每千token元": 0.007,  "说明": "Kimi API 刊例均价"},
    "deepseek": {"每千token元": 0.0035, "说明": "DeepSeek API 刊例均价"},
    "longhun":  {"每千token元": 0.00006,"说明": "本地推理电费折算：实测32MB内存内核，15W低功耗整机，0.6元/度"},
}

def 对比(tokens: int, 指定: str = None) -> dict:
    结果 = {}
    for 名, p in PROVIDERS.items():
        if 指定 and 名 not in (指定, "longhun"):
            continue
        成本 = tokens / 1000 * p["每千token元"]
        结果[名] = {"tokens": tokens, "成本元": round(成本, 4), "说明": p["说明"]}
    lh = 结果["longhun"]["成本元"]
    for 名, v in 结果.items():
        if 名 != "longhun" and lh > 0:
            v["比龍魂贵倍数"] = round(v["成本元"] / lh, 1)
    return 结果

if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="龍魂 vs 大厂API 算力成本对比")
    ap.add_argument("--tokens", type=int, default=1000000, help="token数量(默认100万)")
    ap.add_argument("--provider", default=None, help="只对比某家: openai/claude/kimi/deepseek")
    a = ap.parse_args()
    print(json.dumps(对比(a.tokens, a.provider), ensure_ascii=False, indent=2))
